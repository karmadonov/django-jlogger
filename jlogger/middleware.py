import sys
import inspect

from django.http import HttpResponseRedirect

from loggers import logger


class ProcessExceptionMiddleware(object):
    def process_exception(self, request, exception):
        message = getattr(exception, "message", "Some exception")
        exec_frame = sys._getframe(2)
        code_info = inspect.getframeinfo(exec_frame, context=0)
        print code_info
        logger.warning(message)
        return HttpResponseRedirect('/')
