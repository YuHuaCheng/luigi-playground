import os
import luigi
import shutil
import webbrowser

from src.conf import OUTPUT_PATH, VISUALIZER_URL


def run_luigi_task(task=None):
    """
    A utility method to run a luigi task
    :param task: Luigi.Task
        task to run
    :return: None
    """
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)  # remove all outputs in output folder before a new run
    os.mkdir(OUTPUT_PATH)
    webbrowser.open(VISUALIZER_URL, new=2)  # open a new tab on web browser to go to Luigi Visualizer UI
    if task:
        luigi.run(main_task_cls=task)
    else:
        luigi.run()
