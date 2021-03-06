# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema


#####################################################
# Graph db basic elements to access the db directly #
#####################################################


class IElement(Interface):
    """
    Graph element object.
    """

    def get_property(key, default=None):
        """Gets the value of the property for the given key"""

    def get_properties():
        """Returns a dictionary with all properties (key/value)"""

    def set_property(key, value):
        """Sets the property of the element to the given value"""

    def set_properties(property_dictionary):
        """Add properties. Existing properties are replaced."""

    def remove_property(key):
        """Removes the value of the property for the given key"""

    def get_dbId():
        """Returns the unique identifier of the element"""

    def get_main_interface():
        """Returns the main interface property (string)"""


class IVertex(IElement):
    """
    Graph vertex object.
    """

    def out_edges(label=None):
        """Returns a generator with  all outgoing edges of the vertex.
           label: Optional string parameter to filter the edges
        """

    def in_edges(label=None):
        """Returns a generator with all incoming edges of the vertex.
           label: Optional string parameter to filter the edges
        """


class IEdge(IElement):
    """
    Graph edge object.
    """

    def start_vertex():
        """Returns the origin vertex of the edge"""

    def end_vertex():
        """Returns the target vertex of the edge"""

    def get_label():
        """Returns the label of the edge"""


class IGraph(Interface):
    """
    The graph connection object.
    """

    def __init__(graphdb_connection_string):
        """Creates a new GraphConnection"""

    def shutdown():
        """Closes graph connection"""

    def add_vertex(main_interface=IVertex):
        """Adds a new vertex to the graph with the given
           Interface.
        """

    def get_vertex(dbid):
        """Retrieves an existing vertex from the graph
           with the given dbid or None.
        """

    def get_vertices():
        """Returns an iterator with all the vertices"""

    def remove_vertex(vertex):
        """Removes the given vertex.
        May raise DontRemoveRootException
        """

    def get_root_vertex():
        """Returns the root vertex (with db_id == 0)"""

    def add_edge(startVertex, endVertex, label, main_interface=IEdge):
        """Creates a new edge with label(String)"""

    def get_edge(dbid):
        """Retrieves an existing edge from the graph
           with the given dbid or None.
        """

    def get_edges():
        """Returns an iterator with all the vertices"""

    def remove_edge(edge):
        """Removes the given edge"""

    def clear():
        """Dooms day machine"""

    def start_transaction():
        """Start Transaction to add new or create Elements.
           Returns the transaction."""

    def stop_transaction(transaction):
        """Stop a transaction. You have to make
        sure, this function gets called
        on every created transaction in any case."""

    def fail_transaction(transaction):
        """Marks the current transaction for rollback."""

    def transaction_context():
        """Returns a context for a given transaction.
        Can be used in with-statements."""


class DontRemoveRootException(Exception):
    pass


####################################
# Pyramid location aware, security #
####################################


#class ILocationAware(Interface):
    #"""Attributes needed to make the object hierachy / local permissions work
        #http://readthedocs.org/docs/pyramid/en/1.3-branch/narr/resources.html
    #"""

    ##__parent__ = schema.Object(required=True,)

    #__name__ = schema.TextLine(title=u"Identifier (url slug)",\
                               #required=True,)

    #__acl__ = schema.List(title=u"ACL Control list",\
                          #required=True,
                          #readonly=True)


##############################
# Supergraph basic elements #
#############################


class INode(IVertex):
    """
    Supergraph Node object.
    """

    #TODO
    #def outReferences():
        #""" """

    #def inReferences():
        #""" """


class IReference(IEdge):
    """
    Supergraph Reference object.
    """
    #TODO
