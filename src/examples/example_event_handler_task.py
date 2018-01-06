from src.task import SimpleRequiresTask
from src.event_handler import EventHandlerMixin

from src.examples import run_luigi_task


class EventHandlerTask(SimpleRequiresTask, EventHandlerMixin):
    """
    A luigi.Task that extends the EventHandlerMixin, which will apply the event handler to all the luigi.Task inside,
    including Task in `requires`

    Running this task, you will see something like this in you stdout,

        INFO: [pid 40884] Worker Worker(salt=360069767, workers=1, ...
        ### PROCESSING TIME ###: 5.00226306915
        INFO: [pid 40884] Worker Worker(salt=360069767, workers=1, ...
        the task succeeded. Hooray!!!
        DEBUG: 1 running tasks, waiting for next task to finish
        INFO: Informed scheduler that task   SimpleEternalTask_EventHandlerTask_285e63c6a8   has status   DONE
        DEBUG: Asking scheduler for work...
        DEBUG: Pending tasks: 1
        INFO: [pid 40884] Worker Worker(salt=360069767, workers=1, ...
        ### PROCESSING TIME ###: 5.00181603432
        INFO: [pid 40884] Worker Worker(salt=360069767, workers=1, ...
        the task succeeded. Hooray!!!
    """

    @property
    def extension(self):
        return '.event_handler_task_{task_id}'.format(task_id=self.task_id)


class FailedEventHandlerTask(SimpleRequiresTask, EventHandlerMixin):
    """
    A luigi.Task that extends the EventHandlerMixin, and overrode the run method to invoke luigi.Event.FAILURE

    Running this task, you will see something like this in you stdout,

        File "src/examples/example_event_handler_task.py", line 35, in run
        raise Exception("It will never succeed in the run.")
        Exception: It will never succeed in the run.
        It will never succeed in the run.
        DEBUG: 1 running tasks, waiting for next task to finish
        INFO: Informed scheduler that task   FailedEventHandlerTask_1_c30309a037   has status   FAILED
        DEBUG: Asking scheduler for work...
        DEBUG: Done
        DEBUG: There are no more tasks to run at this time
    """

    def run(self):
        """
        Purposely raise Exception to trigger luigi.Event.FAILURE
        :return:
        """
        raise Exception("It will never succeed in the run.")


if __name__ == '__main__':
    run_luigi_task()
