import os
import sys
import random
import string

colors = ["aliceblue", "antiquewhite1", "aquamarine1", "bisque", "blanchedalmond", "brown", "chartreuse", "crimson", "darkgoldenrod", "darkorange"]
def genName(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Node:
    def __init__ (self, f):
        self.name = genName()
        self.directedEdges = []
        #declare self with random attributes
        declaration = '"' + self.name + '" [sides=' + str(random.randint(0,10)) + ', distortion="' + str(random.uniform(-1,1)) + '", orientation=' + str(random.randint(10,60)) + ', skew="' + str(random.uniform(-1,1)) + '", color=' + colors[random.randint(0,len(colors)-1)] + ' ] \n'
        f.write(declaration)
    def setChild(self, child):
        self.directedEdges.append(child)
        f.write('"' + self.name + '" -> "' + child.name + '"')

def tree(f, numNodes):
    root = Node(f)
    openNodes = [root]
    nodesUsed = 1
    while (nodesUsed < numNodes):
        parent = openNodes[random.randint(0,len(openNodes)-1)]
        child = Node(f)
        nodesUsed+=1
        parent.setChild(child)
        openNodes.append(child)
        if (len(parent.directedEdges) == 2):
            openNodes.remove(parent)


def disconnected(f, numNodes, numEdges):
    nodesUsed = 0
    edgesUsed = 0
    openNodes = []
    while (nodesUsed < numNodes):
        child = Node(f)
        nodesUsed+=1
        openNodes.append(child)
    while (edgesUsed < numEdges):
        node = openNodes[random.randint(0,len(openNodes)-1)]
        node.setChild(openNodes[random.randint(0,len(openNodes)-1)])
        edgesUsed+=1

def clique(f, numNodes):
        nodesUsed = 0
        openNodes = []
        while (nodesUsed < numNodes):
            node = Node(f)
            for s in openNodes:
                node.setChild(s)
                s.setChild(node)
            nodesUsed+=1
            openNodes.append(node)

def bipartite(f,numNodes, numEdges):
    if (numNodes < 2):
        print "Are you really trying to create a bipartite graph with only one node? How does that even make sense?"
        numNodes = 15
    ACount = random.randint(1,numNodes/2)
    if (numEdges < ACount) :
        print "Not enough edges to split into random bipartite graph. Let me just reset numEdges for you\n"
        numEdges = numNodes
    BCount = numNodes - ACount
    nodesUsed = 0
    ANodes = []
    BNodes = []
    edgesUsed = 0
    fluffA = 'subgraph cluster_0 {\n style=filled;\n color=lightgrey;\n node [style=filled,color=white];\nlabel = "Set #1";\n'
    while (nodesUsed < ACount):
        child = Node(f)
        nodesUsed+=1
        ANodes.append(child)
        temp = '"' + child.name + '";\n'
        fluffA += temp
    nodesUsed = 0
    fluffB = 'subgraph cluster_2 {\n node [style=filled];\n color=blue;\nlabel = "Set #2";\n'
    while (nodesUsed < BCount):
        child = Node(f)
        nodesUsed+=1
        BNodes.append(child)
        temp = '"' + child.name + '";\n'
        fluffB += temp
    #print out fluff to sepparate nodes visually
    fluffA+='}\n'
    fluffB+='}\n'
    f.write(fluffA)
    f.write(fluffB)
    itr = 0
    for i in range(BCount-1):
        if itr == ACount:
            itr = 0
        f.write('"' + BNodes[i].name + '" -> "' + ANodes[itr].name + '"\n')
        edgesUsed+=1
        itr+=1
    while (edgesUsed < numEdges):
        node = ANodes[random.randint(0,ACount-1)]
        node.setChild(BNodes[random.randint(0,BCount-1)])
        edgesUsed+=1

if __name__ == '__main__':
    #creates file named temp.dot
    #argv[0] is the file
    #argv[1] is the number of nodes
    #argv[2] is the type of graph you are looking to generate. Options are tree, clique, bipartite, disconnected
    #argv[3] is the number of edges per node from 0 to 5, as a double. Only works with disconnected and bipartite
    if (len(sys.argv) > 2 and len(sys.argv) < 5 and int(sys.argv[1]) > 0):
        numNodes = sys.argv[1]
        graphType = sys.argv[2]
        f = open('temp.dot', 'w')
        opener = 'digraph G { \n node [	shape = polygon, sides = 4, distortion = "0.0", orientation = "0.0", skew = "0.0", color = white, style = filled, fontname = "Helvetica-Outline" ] \n'
        f.write(opener)
        if (sys.argv[2] == "tree"):
            tree(f, int(numNodes))
        elif(sys.argv[2] == "disconnected"):
            edgeDensity = numNodes
            if (len(sys.argv) == 4):
                edgeDensity = int(float(sys.argv[3]) * float(numNodes))
            disconnected(f,int(numNodes),int(edgeDensity))
        elif(sys.argv[2] == "clique"):
            clique(f, int(numNodes))
        elif(sys.argv[2] == "bipartite"):
            edgeDensity = numNodes
            if (len(sys.argv) == 4):
                edgeDensity = int(float(sys.argv[3]) * float(numNodes))
            bipartite(f, int(numNodes),int(edgeDensity))
        f.write("}")
        print "your graphviz compilable file is now at temp.dot. You can run dot -Tpng -O temp.dot to get an easy png :)"



    else:
        print "Usage: python autogenerate.py NumberOfNodes TypeOfGraph EdgeDensity \n" + "Types of Graphs: tree, clique, bipartite, disconnected \n" + "note EdgeDensity only works will full disconnected and bipartite and is a multiplier of numnodes"
