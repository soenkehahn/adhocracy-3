// Gremlin scripts in Gremlin-Groovy v1.3
//
// See the Gremlin and Blueprints docs for the full Gremlin/Blueprints API. 
//
// Gremlin Wiki:     https://github.com/tinkerpop/gremlin/wiki
// Gremlin Steps:    https://github.com/tinkerpop/gremlin/wiki/Gremlin-Steps
// Gremlin Methods:  https://github.com/tinkerpop/gremlin/wiki/Gremlin-Methods 
// Blueprints Wiki:  https://github.com/tinkerpop/blueprints/wiki
//

// Vertices

// These edge-label conditionals are a messy hack until Gremin allows null labels. 
// See https://github.com/tinkerpop/gremlin/issues/267

// the || label == "null" is a hack until Rexster fixes its null label bug.
// See https://github.com/tinkerpop/rexster/issues/197


def outE(_id, label) {
  if (label == null)
    g.v(_id).outE()
  else
    g.v(_id).outE(label)
}

def inE(_id, label) {
  if (label == null)
    g.v(_id).inE()
  else
    g.v(_id).inE(label)
}

def bothE(_id, label) { 
  if (label == null)
    g.v(_id).bothE()
  else
    g.v(_id).bothE(label)
}

//extended outV to filter edge properties
def outV(_id, label, property_key, property_value) {
  if (label == null)
    return g.v(_id).outE().filter{
            if (property_key != null && property_value != null) it.getProperty(property_key) == property_value  
            else true 
            }.inV
  else 
    return g.v(_id).outE(label).filter{
            if (property_key != null && property_value != null) it.getProperty(property_key) == property_value  
            else true 
            }.inV
}

def inV(_id, label) {
  if (label == null)
    g.v(_id).in()
  else
    g.v(_id).in(label)
}

def bothV(_id, label) { 
  if (label == null)
    g.v(_id).both()
  else
    g.v(_id).both(label)
}
