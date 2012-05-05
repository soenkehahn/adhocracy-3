from bulbs.property import String
from bulbs.property import List
from zope.interface import implements
from zope.dottedname.resolve import resolve

from pyramid.threadlocal import get_current_registry
from repoze.lemonade.content import create_content

from adhocracy.core.models.interfaces import IAdhocracyRoot
from adhocracy.core.models.interfaces import IGraphConnection
from adhocracy.core.models.node import NodeAdhocracy
from adhocracy.core.security import SITE_ACL


class AdhocracyRoot(NodeAdhocracy):
    """no parent == this is the application root object"""

    implements(IAdhocracyRoot)

    element_type = "adhocracyroot"

    __parent__ = None
    __name__ = ''

    __acl__ = List()
    name = String(nullable=False)


def appmaker():
    root = create_content(IAdhocracyRoot)
    if not root.__acl__:
        root.__acl__ = SITE_ACL
        root.save()
    return root


def adhocracyroot_factory():
    interface = IAdhocracyRoot
    registry = get_current_registry()
    graph = registry.getUtility(IGraphConnection)
    root = graph.getVertex(0)
    if not root:
        root = graph.addVertex(0)
        root.initialize()
    return
