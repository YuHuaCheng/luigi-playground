import os
import luigi
import time
import shutil

from src.conf import OUTPUT_PATH


class TimeTaskMixin(object):
    """
    A mixin that when added to a luigi task, will print out
    the tasks execution time to standard out, when the task is
    finished
    """
    @luigi.Task.event_handler(luigi.Event.PROCESSING_TIME)
    def print_execution_time(self, processing_time):
        print('### PROCESSING TIME ###: ' + str(processing_time))

    @luigi.Task.event_handler(luigi.Event.SUCCESS)
    def celebrate_success(self):
        print ('hooray!!!')

    @luigi.Task.event_handler(luigi.Event.FAILURE)
    def mourn_failure(self, exception):
        print (exception.message)


class TaskA(luigi.ExternalTask, TimeTaskMixin):
    """
    A simple task representing a simple file with a few rows
    of dummy content
    """

    input_file = os.path.join(OUTPUT_PATH, 'inputA')

    def output(self):
        return luigi.LocalTarget(self.input_file)

    def run(self):
        time.sleep(5)
        with open(self.input_file, 'w') as f:
            f.write('some input')


class TaskB(luigi.Task, TimeTaskMixin):
    """
    A simple task that just outputs the content of its dependency
    into a new file with the the same name plus the extension .taskb
    """
    task_id = luigi.Parameter()

    def requires(self):
        return TaskA()

    def output(self):
        return luigi.LocalTarget(self.input().path + '.taskb{}'.format(self.task_id))

    def run(self):
        time.sleep(5)
        # raise Exception('you will never work!')
        with self.input().open() as infile, self.output().open('w') as outfile:
            for row in infile:
                outfile.write(row)


class TaskC(luigi.Task, TimeTaskMixin):
    """
    A simple task that just outputs the content of its dependency
    into a new file with the the same name plus the extension .taskc
    """

    task_id = luigi.Parameter()

    def requires(self):
        return TaskB(task_id=self.task_id)

    def output(self):
        return luigi.LocalTarget(self.input().path + '.taskc{}'.format(self.task_id))

    def run(self):
        for child in range(5):
            output_name = 'taskc_{task_id}_child_{child_id}'.format(
                task_id=self.task_id,
                child_id=child
            )
            yield TaskCChild(output_name)

        with self.input().open() as infile, self.output().open('w') as outfile:
            for row in infile:
                outfile.write(row)


class TaskCChild(luigi.Task, TimeTaskMixin):
    child_id = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_PATH, 'taskc_child{}'.format(self.child_id)))

    def run(self):
        time.sleep(3)
        with self.output().open('w') as outfile:
            outfile.write('child completed!')


class TaskWrapper(luigi.WrapperTask):
    def requires(self):
        for i in range(0, 10):
            yield TaskC(task_id=i)


# If this file is executed as a script, run the last class in the dependency graph, TaskC.
if __name__ == '__main__':
    os.mkdir(OUTPUT_PATH)
    luigi.run(main_task_cls=TaskWrapper)
    shutil.rmtree(OUTPUT_PATH)  # remove all outputs in output folder, so we can run the whole runner again
