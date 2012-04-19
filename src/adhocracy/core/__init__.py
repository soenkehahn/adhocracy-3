from pyramid.config import Configurator

from adhocracy.core.models.adhocracyroot import appmaker


def root_factory(request):
    """Return application root
    """
    return appmaker()


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    #load application settings (rootfactory == try to use object traversal)
    config = Configurator(root_factory=root_factory, settings=settings)
    #hook zope global component registry into the pyramid application registry
    #http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/zca.html?highlight=utility#using-the-zca-global-registry
    #config.hook_zca()
    #add views (TODO: use zcml or imperative?)
    config.add_static_view('static', 'static', cache_max_age=3600)
    #scan modules for configuration decorators
    config.scan()
    #load zcml configuration files
    #http://readthedocs.org/docs/pyramid_zcml/en/latest/narr.html
    config.include('pyramid_zcml') #imperative configuration: run pyramid_zcml.includeme()
    config.load_zcml('configure.zcml') #declerative configuration: load central zcml file

    return config.make_wsgi_app()
