import os
import imp
import importlib
from path import path

from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

from hendrix.services import HendrixService, get_additional_services
from hendrix import import_wsgi
from hendrix.resources import get_additional_resources


class Options(usage.Options):
    optParameters = [
        ["wsgi", "w", None, "The path to a python module that contains a WSGIHandler instance."],
        ["port", "p", None, "The port number to listen on."],
        ["settings", "s", None, "The settings to use for launch."],
    ]


class HendrixServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "hendrix"
    description = "A twisted deployment module for django."
    options = Options

    def makeService(self, options):
        wsgi_module = import_wsgi(options['wsgi'])
        settings = options['settings']
        os.environ['DJANGO_SETTINGS_MODULE'] = settings

        # Use the logger defined in the settings file.
        try:
            settings_module = importlib.import_module(settings)
        except ImportError:
            raise RuntimeError("Could not find '%s'." % settings)

        server = HendrixService(
            application=wsgi_module.application,
            port=int(options['port']),
            resources=get_additional_resources(settings_module),
            services=get_additional_services(settings_module)
        )
        return server


serviceMaker = HendrixServiceMaker()
