from pyramid.threadlocal import get_current_registry
# collection of general convenience functions


#Database helpers

#def run_gremlin_script(name, params={}):
    #"""
       #Queries the database with a gremlin script.

       #name: script name
       #params: optional script parameter dict

       #returns: the raw result dict
       #raises: GremlinError
    #"""
    #graph = get_graph()
    #resp = {}
    #script = graph.scripts.get(name)
    #try:
        #resp = graph.client.gremlin(script, params)
    #except SystemError as e:
        #import json
        #raise GremlinError("\n" + json.loads(e.message[1])["error"])

    #return resp


#class GremlinError(Exception):
    #pass
