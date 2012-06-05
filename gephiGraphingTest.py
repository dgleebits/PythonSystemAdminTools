#some import
import org.gephi.graph.api as graph_api
 
#we do not need to init a project
 
#Get a graph model - it exists because gephi has created the workspace
graphModel = gephi.getLookup().lookup(graph_api.GraphController).getModel()
 
#Create three nodes
n0 = graphModel.factory().newNode("n0") #we just remove the type Node and the ;
n0.getNodeData().setLabel("Node 0")
n1 = graphModel.factory().newNode("n1")
n1.getNodeData().setLabel("Node 1")
n2 = graphModel.factory().newNode("n2")
n2.getNodeData().setLabel("Node 2")
 
#Create three edges
e1 = graphModel.factory().newEdge(n1, n2, 1., True)#we remove Edge, true->True and 1f -> 1.
#it was in java : Edge e1 = graphModel.factory().newEdge(n1, n2, 1f, true);
e2 = graphModel.factory().newEdge(n0, n2, 2., True)
e3 = graphModel.factory().newEdge(n2, n0, 2., True)   #This is e2's mutual edge
 
#Append as a Directed Graph
directedGraph = graphModel.getDirectedGraph()
directedGraph.addNode(n0)
directedGraph.addNode(n1)
directedGraph.addNode(n2)
directedGraph.addEdge(e1)
directedGraph.addEdge(e2)
directedGraph.addEdge(e3)
 
#Count nodes and edges
print "Nodes: ", directedGraph.getNodeCount(), " Edges: ",directedGraph.getEdgeCount() #python does not transform objects into str. We use a more pythonic way to present output
 
#Get a UndirectedGraph now and count edges
undirectedGraph = graphModel.getUndirectedGraph()
print "Edges: ", undirectedGraph.getEdgeCount()   #The mutual edge is automatically merged
 
#Iterate over nodes
for n in directedGraph.getNodes() : 
    neighbors = directedGraph.getNeighbors(n).toArray()
    print n.getNodeData().getLabel(), "has", len(neighbors), "neighbors"
 
 
#Iterate over edges
for e in directedGraph.getEdges() :
    print e.getSource().getNodeData().getId(), " -> ", e.getTarget().getNodeData().getId()
 
 
#Find node by id
node2 = directedGraph.getNode("n2")
 
#Get degree
print "Node2 degree: ", directedGraph.getDegree(node2)