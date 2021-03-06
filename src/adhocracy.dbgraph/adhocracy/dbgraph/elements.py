# -*- coding: utf-8 -*-
from zope.dottedname.resolve import resolve
from zope.interface import implements
from zope.interface import directlyProvides

from adhocracy.dbgraph.interfaces import IElement
from adhocracy.dbgraph.interfaces import IVertex
from adhocracy.dbgraph.interfaces import IEdge
from adhocracy.dbgraph.interfaces import INode
from adhocracy.dbgraph.interfaces import IReference


def _is_existing_element(element):
    """
    Determines whether a db element is supposed to be visible in this scope.
    This is related to the following issues:
    # https://github.com/neo4j/community/issues/520
    # https://github.com/neo4j/community/issues/457
    """
    from neo4j._backend import NodeProxy
    from neo4j._backend import RelationshipProxy
    assert (type(element) == NodeProxy) or (type(element) == RelationshipProxy)
    #TODO: implement using TransactionData?
    r = True
    try:
        r = bool(element.hasProperty('_exists'))
        list(element.keys())
        'foo' in element.keys()
    except Exception:
        r = False
    return r


class EmbeddedElement(object):
    implements(IElement)
    """implementation for EmbeddedGraph"""

    def __init__(self, db_element):
        self.db_element = db_element

    def __eq__(self, other):
        both_elements = hasattr(self, 'get_dbId') \
            and hasattr(other, 'get_dbId')
        if both_elements:
            return self.get_dbId() == other.get_dbId()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_main_interface(self):
        if 'main_interface' in self.db_element.keys():
            return resolve(self.db_element['main_interface'])
        else:
            return None

    def get_dbId(self):
        return self.db_element.id

    def get_property(self, key, default=None):
        try:
            return self.db_element[key]
        except KeyError:
            return default

    def get_properties(self):
        return dict((k, v)
                for k, v in self.db_element.items() if k != '_exists')

    def set_property(self, key, value):
        self.db_element[key] = value

    def set_properties(self, property_dictionary):
        for k in property_dictionary.keys():
            self.set_property(k, property_dictionary[k])

    def remove_property(self, key):
        del self.db_element[key]


class Vertex(EmbeddedElement):
    implements(IVertex)

    def __repr__(self):
        return "<Vertex %i>" % self.get_dbId()

    def out_edges(self, label=None):
        return [element_factory(edge) for edge \
                in self.db_element.relationships.outgoing
                if _is_existing_element(edge)]

    def in_edges(self, label=None):
        return [element_factory(edge) for edge \
                in self.db_element.relationships.incoming
                if _is_existing_element(edge)]


class Edge(EmbeddedElement):
    implements(IEdge)

    def __repr__(self):
        return "<Edge %i>" % self.get_dbId()

    def start_vertex(self):
        return element_factory(self.db_element.start)

    def end_vertex(self):
        return element_factory(self.db_element.end)

    def get_label(self):
        return self.db_element.type.name()


class Node(Vertex):
    """TODO """

    implements(INode)


class Reference(Edge):
    """TODO """

    implements(IReference)


def element_factory(db_element):
    """Make a proper element according to the main_interface"""

    interface = IElement
    if 'main_interface' in db_element.keys():
        interface = resolve(db_element['main_interface'])
    # import here, we do not want to wake the jvm earlier...
    from neo4j._backend import RelationshipProxy
    from neo4j._backend import NodeProxy
    element = None
    if issubclass(interface, INode):
        element = Node(db_element)
    elif issubclass(interface, IReference):
        element = Reference(db_element)
    elif isinstance(db_element, NodeProxy):
        element = Vertex(db_element)
    elif isinstance(db_element, RelationshipProxy):
        element = Edge(db_element)
    element and directlyProvides(element, interface)
    return element
