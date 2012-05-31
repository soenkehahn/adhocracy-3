# -*- coding: utf-8 -*-
import atexit
from zope.interface import implements
from zope.interface import implementer
from zope import component
from pyramid.threadlocal import get_current_registry

from adhocracy.dbgraph.interfaces import IGraph
from adhocracy.dbgraph.interfaces import DontRemoveRootException

from adhocracy.dbgraph.elements import _is_deleted_element
from adhocracy.dbgraph.elements import element_factory


class EmbeddedGraph():
    implements(IGraph)

    def __init__(self, dbgraph_database):
        self.db = dbgraph_database

    def shutdown(self):
        self.db.shutdown()

    def add_vertex(self, main_interface=None):
        db_vertex = self.db.node()
        if main_interface:
            db_vertex['main_interface'] = main_interface.__identifier__
        return element_factory(db_vertex)

    def get_vertex(self, dbid):
        try:
            db_vertex = self.db.node[dbid]
        except KeyError:
            return None
        else:
            return element_factory(db_vertex)

    def get_vertices(self):
        nodes = self.db.nodes
        return [element_factory(node) for node in nodes
                if not _is_deleted_element(node)]

    def remove_vertex(self, vertex):
        if vertex.get_dbId() == 0:
            raise DontRemoveRootException()
        else:
            vertex.db_element.delete()

    def get_root_vertex(self):
        return self.get_vertex(0)

    def add_edge(self, start_vertex, end_vertex, label, main_interface=None):
        db_edge = start_vertex.db_element.relationships.create(label,
                    end_vertex.db_element)
        if main_interface:
            db_edge['main_interface'] = main_interface.__identifier__
        return element_factory(db_edge)

    def get_edge(self, dbid):
        return element_factory(self.db.relationships[dbid])

    def get_edges(self):
        return [element_factory(edge) for edge in self.db.relationships
                if not _is_deleted_element(edge)]

    def remove_edge(self, edge):
        """Removes the given edge"""
        edge.db_element.delete()

    def clear(self):
        for e in self.get_edges():
            self.remove_edge(e)
        for v in self.get_vertices():
            if v.get_dbId() == 0:
                # this is the root node
                # don't remove it, but remove all its properties
                for k in v.db_element.keys():
                    del v.db_element[k]
            else:
                self.remove_vertex(v)

    def start_transaction(self):
        return self.db.beginTx()

    def stop_transaction(self, tx):
        tx.success()
        tx.finish()

    def fail_transaction(self, tx):
        tx.failure()
        tx.finish()


def get_graph():
    """ returns the graph database connection object
    """
    global_registry = component.getGlobalSiteManager()
    graph = global_registry.queryUtility(IGraph)
    if not graph:
        global_registry = component.getGlobalSiteManager()
        graph = graph_factory()
        global_registry.registerUtility(graph)
    return graph


def del_graph():
    """manually shuts the graph down, that got created using get_graph.
    Normally, you don't have to call this function, the global graph db
    connection will be shut down when the process exits. This is needed,
    if you manually want to fire up your own neo4j kernel for the same db."""
    graph = get_graph()
    graph.shutdown()
    global_registry = component.getGlobalSiteManager()
    global_registry.unregisterUtility(graph)


@implementer(IGraph)
def graph_factory():
    """Utility to store the db graph conneciton object
    """
    settings = get_current_registry().settings
    connection_string = settings and settings['graphdb_connection_string'] \
                        or "testdb"
    import os
    os.environ['NEO4J_PYTHON_JVMARGS'] = '-Xms128M -Xmx512M'
    from neo4j import GraphDatabase
    db = GraphDatabase(connection_string)

    def close_db():
        """Make sure to always close the database
        """
        try:
            db.shutdown()
            print("db shut down")
        except NameError:
            print 'Could not shutdown Neo4j database.'

    atexit.register(close_db)

    return EmbeddedGraph(db)
