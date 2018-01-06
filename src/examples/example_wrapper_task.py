import luigi

from src.task import ManyRunTask
from src.examples import run_luigi_task


class WrapperTask(luigi.WrapperTask):
    """
    A wrapper task which will complete iff all the tasks in `requires` complete

    This task will require many ManyRunTask, and each ManyRunTask will have its set of `run` tasks and `require` task,
    go to the Visualizer UI and you will get a clearer picture
    """
    def requires(self):
        for i in range(0, 10):
            yield ManyRunTask(task_id=i)


if __name__ == '__main__':
    run_luigi_task(WrapperTask)
