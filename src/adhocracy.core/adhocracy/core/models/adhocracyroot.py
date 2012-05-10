from zope.interface import implements
from zope.interface import Interface
from zope.interface import directlyProvides
from zope import component

from repoze.lemonade.content import create_content

from adhocracy.dbgraph.embeddedgraph import get_graph
from adhocracy.core.models.interfaces import ILocationAware
from adhocracy.core.security import SITE_ACL


class IAdhocracyRootMarker(Interface):
    """
    Adhocracy root object Marker.
    """


class AdhocracyRootLocationAware(object):
     implements(ILocationAware)
     component.adapts(IAdhocracyRootMarker)

     def __init__(self, context):
         self.context = context

     __parent__ = None
     __name__ = ''
     __acl__ = SITE_ACL


def adhocracyroot_factory():
    graph = get_graph()
    root = graph.get_vertex(0)
    if not IAdhocracyRootMarker.providedBy(root):
        root.set_property("main_interface", IAdhocracyRootMarker)
        directlyProvides(IAdhocracyRootMarker, root)
    return


def appmaker():
    root = create_content(IAdhocracyRootMarker)
    return root

