import argparse


class HendrixParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(HendrixParser, self).__init__(*args, **kwargs)
        if not self.description:
            self.description="The Hendrix Development Server"

    def base_args(self):
        self.add_argument('settings', help='Location of the settings object e.g. myproject.app.settings')
        self.add_argument('wsgi', help='Location of the wsgi object e.g. ./wsgi.py')
        self.add_argument('port', type=int, help='Enter a port number for the server to serve content.')
        return self

    def all_args(self):
        self.add_argument('action', help='Use start, stop, or restart')
        self.base_args()
        self.add_argument('workers', type=int, nargs='?', default=0, help='Number of processes to run')
        self.add_argument('fd', type=int, nargs='?', default=None, help='DO NOT SET THIS')
        return self