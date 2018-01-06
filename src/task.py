import os
import time
import luigi

from .conf import OUTPUT_PATH


class SimpleEternalTask(luigi.ExternalTask):
    """
    A simple Eternal Task that extends luigi.ExternalTask, which has no implementation on `run`, and that means the
    `output` must be generated outside a luigi.Task

    This task sleeps a while, and write some content into the input_file

    It takes one luigi.Parameter that will be used in the input file name.
    """
    task_id = luigi.Parameter()

    @property
    def input_file(self):
        return os.path.join(OUTPUT_PATH, 'simple_external_task_{task_id}'.format(task_id=self.task_id))

    def output(self):
        return luigi.LocalTarget(self.input_file)

    def run(self):
        time.sleep(5)
        with open(self.input_file, 'w') as f:
            f.write('I am some input from SimpleExternalTask.')


class SimpleRequiresTask(luigi.Task):
    """
    A simple task that requires SimpleEternalTask, and just outputs the content of its dependency from `requires`,
    into a new file with the the same name plus the extension .task_requires

    The task takes one luigi.Parameter that will be used in the output extension name.
    """
    task_id = luigi.Parameter()

    @property
    def extension(self):
        return '.task_requires_{task_id}'.format(task_id=self.task_id)

    def requires(self):
        return SimpleEternalTask(task_id=self.task_id)

    def output(self):
        return luigi.LocalTarget(self.input().path + self.extension)

    def run(self):
        time.sleep(5)
        with self.input().open() as infile, self.output().open('w') as outfile:
            for row in infile:
                outfile.write(row)


class ManyRunTask(luigi.Task):
    """
    A task that runs many SimpleRequiresTask tasks in `run`
    """
    task_id = luigi.Parameter()

    @property
    def output_name(self):
        return 'task_many_{task_id}'.format(task_id=self.task_id)

    def output(self):
        return luigi.LocalTarget(os.path.join(OUTPUT_PATH, self.output_name))

    def run(self):
        for sub_task_id in range(5):
            yield SimpleRequiresTask(task_id='_'.join([str(_) for _ in [self.task_id, sub_task_id]]))

        with self.output().open('w') as f:
            f.write('many tasks just run/.')

