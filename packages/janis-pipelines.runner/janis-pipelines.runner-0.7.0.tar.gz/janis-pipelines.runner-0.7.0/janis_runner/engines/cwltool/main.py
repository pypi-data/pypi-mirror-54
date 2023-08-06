import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, Any

import dateutil

from janis_runner.data.models.workflow import WorkflowModel
from janis_runner.engines.enginetypes import EngineType
from janis_runner.engines.engine import Engine, TaskStatus, TaskBase
from janis_runner.utils.dateutil import DateUtil
from janis_core.utils.logger import Logger


class CWLTool(Engine):

    taskid_to_process = {}

    # This is the bad version of a metadata store, this implementation really needs a rewrite to collect
    # metadata from CWLTool (and store it somewhere) to be polled by the metadata function and provide status.
    #
    # Currently, this class just watches the stdout and looks for the JSON returned by CWLTool.
    # I don't know the implications of updating this from another thread, because it should really only ever run
    # one at once (at the moment).
    metadata_by_task_id = (
        {}
    )  # format: { [wid: string]: { start: DateTime, status: Status, outputs: [] } }

    def __init__(self, logfile=None, identifier: str = "cwltool", options=None):
        super().__init__(identifier, EngineType.cwltool, logfile=logfile)
        self.options = options if options else []
        self.process = None
        self.pid = None

    def test_connection(self):
        return bool(self.pid)

    def start_engine(self):
        Logger.info(
            "Cwltool doesn't run in a server mode, an instance will "
            "automatically be started when a task is created"
        )
        return self

    def stop_engine(self):
        Logger.info(
            (
                "CWLTool doesn't run in a server mode, an instance will "
                "be automatically terminated when a task is finished"
            )
        )
        return self

    def create_task(self, source=None, inputs=None, dependencies=None) -> str:
        import uuid

        print(self.id())

        return str(uuid.uuid4())

    def poll_task(self, identifier) -> TaskStatus:
        if identifier in self.taskid_to_process:
            return TaskStatus.RUNNING
        return TaskStatus.COMPLETED

    def outputs_task(self, identifier) -> Dict[str, Any]:
        if identifier not in self.metadata_by_task_id:
            raise Exception("Couldn't find status for CWLTool task: " + identifier)

        outs = self.metadata_by_task_id[identifier].get("outputs")

        if not outs:
            return {}

        retval = {}
        for k, o in outs.items():
            if "path" in o:
                retval[k] = o["path"]
            if "secondaryFiles" in o:
                for s in o["secondaryFiles"]:
                    path = s["path"]
                    ext = path.rpartition(".")[-1]
                    retval[f"{k}_{ext}"] = path

        return retval

    def terminate_task(self, identifier) -> TaskStatus:
        """
        This CWLTool implementation is not super great. It should start the process and issue an async task
        to watch out for progress and eventually report back to the sqlite database. Then when 'terminate_task'
        is called, it could kill this process (eventually self.pid | self._process) and cleanup the metadata.

        :param identifier:
        :return:
        """
        raise NotImplementedError(
            "terminate_task needs to be implemented in CWLTool, may require rework of tool"
        )

    def metadata(self, identifier) -> WorkflowModel:
        """
        So CWLTool doesn't really have a metadata thing. See the 'terminate_task' description, but this
        implementation should instead create a thread to watch for process, and write metadata back to sqlite.
        Then this method could just read from the sqlite database.

        :param identifier:
        :return:
        """
        if identifier not in self.metadata_by_task_id:
            raise Exception("Couldn't find status for CWLTool task: " + identifier)

        meta = self.metadata_by_task_id[identifier]

        return WorkflowModel(
            identifier,
            name=identifier,
            status=meta.get("status"),
            start=meta.get("start"),
            finish=meta.get("finish"),
            # outputs=meta.get("outputs") or [],
            jobs=[],
            error=None,
            # executiondir=None,
        )

    def start_from_task(self, task: TaskBase):
        task.identifier = self.create_task(None, None, None)

        self.metadata_by_task_id[task.identifier] = {
            "start": DateUtil.now(),
            "status": TaskStatus.PROCESSING,
        }

        temps = []
        sourcepath, inputpaths, toolspath = (
            task.source_path,
            task.input_paths,
            task.dependencies_path,
        )
        if task.source:
            t = tempfile.NamedTemporaryFile(mode="w+t", suffix=".cwl", delete=False)
            t.writelines(task.source)
            t.seek(0)
            temps.append(t)
            sourcepath = t.name

        if task.inputs:
            inputs = []
            if len(task.inputs) > 1:
                raise Exception("CWLTool currently only supports 1 input file")
            for s in task.inputs:
                if isinstance(s, dict):
                    import ruamel.yaml

                    s = ruamel.yaml.dump(s, default_flow_style=False)
                t = tempfile.NamedTemporaryFile(mode="w+t", suffix=".yml")
                t.writelines(s)
                t.seek(0)
                inputs.append(t)
                inputpaths = [t.name for t in inputs]
            temps.extend(inputs)

        if task.dependencies:
            # might need to work out where to put these

            tmp_container = tempfile.tempdir + "/"
            tmpdir = tmp_container + "tools/"
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            os.mkdir(tmpdir)
            for (f, d) in task.dependencies:
                with open(tmp_container + f, "w+") as q:
                    q.write(d)
            temps.append(tmpdir)

        # start cwltool
        cmd = ["cwltool", *self.options]
        if sourcepath:
            cmd.append(sourcepath)
        if inputpaths:
            if len(inputpaths) > 1:
                raise Exception(
                    "CWLTool only accepts 1 input, Todo: Implement inputs merging later"
                )
            cmd.append(inputpaths[0])
        # if toolspath: cmd.extend(["--basedir", toolspath])

        self.metadata_by_task_id[task.identifier]["status"] = TaskStatus.RUNNING

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, preexec_fn=os.setsid, stderr=subprocess.PIPE
        )
        Logger.log("Running command: '" + " ".join(cmd) + "'")
        Logger.info("CWLTool has started with pid=" + str(process.pid))
        self.taskid_to_process[task.identifier] = process.pid

        for c in iter(process.stderr.readline, "b"):  # replace '' with b'' for Python 3
            line = c.decode("utf-8").rstrip()
            if not line.strip():
                continue
            self._logfp.write(line + "\n")
            Logger.log("cwltool: " + line)
            if b"Final process status is success" in c:
                break
        j = ""
        Logger.log("Process has completed")
        for c in iter(process.stdout.readline, "s"):  # replace '' with b'' for Python 3
            if not c:
                continue
            j += c.decode("utf-8")
            try:
                json.loads(j)
                break
            except:
                continue

        Logger.info("Workflow has completed execution")
        process.terminate()
        outputs = json.loads(j)
        Logger.info(outputs)
        self.metadata_by_task_id[task.identifier]["outputs"] = outputs
        self.metadata_by_task_id[task.identifier]["status"] = TaskStatus.COMPLETED

        # close temp files
        Logger.log(f"Closing {len(temps)} temp files")
        for t in temps:
            if hasattr(t, "close"):
                t.close()
            if isinstance(t, str):
                if os.path.exists(t) and os.path.isdir(t):
                    shutil.rmtree(t)
                else:
                    os.remove(t)

    def start_from_paths(self, wid, source_path: str, input_path: str, deps_path: str):
        self.metadata_by_task_id[wid] = {
            "start": DateUtil.now(),
            "status": TaskStatus.PROCESSING,
        }

        cmd = ["cwltool", *self.options, "--disable-color", source_path]

        if input_path:
            cmd.append(input_path)

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, preexec_fn=os.setsid, stderr=subprocess.PIPE
        )
        self.metadata_by_task_id[wid]["status"] = TaskStatus.RUNNING
        Logger.log("Running command: '" + " ".join(cmd) + "'")
        Logger.info("CWLTool has started with pid=" + str(process.pid))
        self.taskid_to_process[wid] = process.pid

        finalstatus = None
        errors = []
        for c in iter(process.stderr.readline, "b"):  # replace '' with b'' for Python 3
            line = c.decode("utf-8").rstrip()
            if not line.strip():
                continue

            lowline = line.lower().lstrip()
            if lowline.startswith("error"):

                Logger.critical("cwltool: " + line)
                errors.append(line)
            elif lowline.startswith("warn"):
                Logger.warn("cwltool: " + line)
            elif lowline.startswith("info"):
                Logger.info("cwltool: " + line)
            else:
                Logger.log("cwltool: " + line)

            if "final process status is" in lowline:
                if "fail" in line.lower():
                    finalstatus = TaskStatus.FAILED
                elif "success" in line.lower():
                    finalstatus = TaskStatus.COMPLETED
                else:
                    finalstatus = TaskStatus.ABORTED
                break

            elif process.poll() is not None:
                finalstatus = TaskStatus.ABORTED
                Logger.warn(
                    f"CWLTool finished with rc={process.returncode} but janis "
                    f"was unable to capture the workflow status"
                )

        j = ""
        Logger.log("Process has completed")
        outputs = None
        if finalstatus == TaskStatus.COMPLETED:
            for c in iter(
                process.stdout.readline, "s"
            ):  # replace '' with b'' for Python 3
                if not c:
                    continue
                j += c.decode("utf-8")
                try:
                    outputs = json.loads(j)
                    break
                except:
                    continue
        process.terminate()

        self.metadata_by_task_id[wid]["outputs"] = outputs
        self.metadata_by_task_id[wid]["status"] = finalstatus

        return wid
