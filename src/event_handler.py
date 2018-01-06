import luigi


class EventHandlerMixin(object):
    """
    A mixin that when added to a luigi task, will apply the luigi event handler
    """
    @luigi.Task.event_handler(luigi.Event.PROCESSING_TIME)
    def print_execution_time(self, processing_time):
        print('### PROCESSING TIME ###: ' + str(processing_time))

    @luigi.Task.event_handler(luigi.Event.SUCCESS)
    def celebrate_success(self):
        print ('the task succeeded. Hooray!!!')

    @luigi.Task.event_handler(luigi.Event.FAILURE)
    def mourn_failure(self, exception):
        print (exception.message)


