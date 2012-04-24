"""Helper classes for adhocracy.core test"""
from bulbs.model import Relationship
from bulbs.property import String
from bulbs.property import Integer

from pyramid.threadlocal import get_current_registry
from pyramid import testing

from adhocracy.core.models.interfaces import IGraphConnection
from adhocracy.core.models import utilities
from adhocracy.core.models.node import NodeAdhocracy

#Unit testing


def setUp(**kwargs):
    """
       setUp basic test environment with database connection
       proxy to pyramid.testing.setUp(**kwargs)
    """
    testing.tearDown()
    settings = {}
    settings['rexster_uri'] = "http://localhost:8182/graphs/testgraph"
    settings.update(kwargs.get('settings', {}))
    kwargs['settings'] = settings
    config = testing.setUp(**kwargs)

    config.registry.registerUtility(utilities.graph_object(), IGraphConnection)

    return config


def tearDown(**kwargs):
    """
       tearDown basic test environment with database
       proxy to paramid.testing.tearDown(**kwargs)
    """
    graph = get_graph()
    if graph:
        graph.clear()
    testing.tearDown(**kwargs)


def get_graph(config=None):
    """
        returns the graph database connection object
    """
    if config:
        return config.registry.queryUtility(IGraphConnection)
    else:
        registry = get_current_registry()
        return registry.queryUtility(IGraphConnection)


# Integration testing

def load_registry(config):
    """
       Load configuration like adhocracy.core.main()
       Returns the registry
    """
    config.include('pyramid_zcml')
    registry = config.load_zcml("adhocracy.core:configure.zcml")
    return registry


#Functional testing with zope.testbrowser

#class Browser(wsgi_intercept.zope_testbrowser.WSGI_Browser):
    #"""Simplify zope.testbrowser sessions"""

    #def dc(self, filename="/tmp/test-output.html"):
        #"""Write html output to file"""
        #open(filename, 'w').write(self.contents)


def setUpFunctional(global_config=None, **settings):
    from adhocracy.core import main
    import wsgi_intercept.zope_testbrowser
    from webtest import TestApp

    testing.tearDown()
    _settings = {}
    _settings['rexster_uri'] = "http://localhost:8182/graphs/testgraph"
    _settings.update(settings)

    host = "localhost"
    port = 6543
    app = main({}, **_settings)
    wsgi_intercept.add_wsgi_intercept(host, port, lambda: app)
    Browser = wsgi_intercept.zope_testbrowser.WSGI_Browser

    return dict(
        Browser=Browser,
        browser=Browser(),
        app=app,
        test_app=TestApp(app),
        )

#Various test helper stuff


class Dummy(dict):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Person(NodeAdhocracy):
    """Dummy node class"""

    element_type = "person"
    name = String(nullable=False)
    age = Integer()


class Knows(Relationship):
    """Dummy relation class"""

    label = "knows"
    place = String()
