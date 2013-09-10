import os

from django.core import management
from django.core.servers.basehttp import get_internal_wsgi_application


def main(settings_file, logfile=None):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)

    # Setup settings

    if logfile:
        redirect_streams(logfile)

    return get_internal_wsgi_application()


def redirect_streams(logfile):
    import datetime
    import sys

    class logger(object):
        def __init__(self, logfile):
            self.logfile = logfile

        def write(self, data):
            self.log(data)

        def writeline(self, data):
            self.log(data)

        def log(self, msg):
            line = '%s - %s\n' % (
                datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'), msg)
            fp = open(self.logfile, 'a')
            try:
                fp.write(line)
            finally:
                fp.close()
    sys.stdout = sys.stderr = logger(logfile)