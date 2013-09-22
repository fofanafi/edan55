import sys

class Vertex(object):
  def __init__(self, num, neighbors = None):
    if neighbors is None:
      neighbors = []
    self.num = num
    self.neighbors = neighbors
  
  def addNeighbor(self, vertex):
    self.neighbors.append(vertex)

  def numEdges(self, vertexList):
    count = 0
    for vertex in self.neighbors:
      if vertex in vertexList:
        count += 1
    return count

  def getNeighbors(self, vertexList):
    neighbors = []
    for vertex in self.neighbors:
      if vertex in vertexList:
        neighbors.append(vertex)
    return neighbors

def createGraph(numVertices):
  """
  Creates an empty graph with numVertices vertices.
  """
  graph = {}
  for i in range(numVertices):
    vertex = Vertex(i)
    graph[i] = vertex
  return graph

def readGraph(numVertices):
  """
  Reads a graph from the file with the specified number of vertices.
  """
  filename = "g" + str(numVertices) + ".in"
  f = open('data/' + filename)
  f.readline() # throw out the first line, only contains numVertices 

  graph = createGraph(numVertices)
  for i in range(numVertices):
    edges = f.readline().split()
    for j in range(numVertices):
      if edges[j] == '1':
        graph[i].addNeighbor(j)
  return graph

def findVertexOfDegree(n, graph):
  for i, vertex in graph.iteritems():
    if vertex.numEdges(graph) == n:
      return i

def findVertexOfMaxDegree(graph):
  maximum = (0, None)
  for i, vertex in graph.iteritems():
    degree = vertex.numEdges(graph)
    if degree > maximum[0]:
      maximum = (degree, i)
  return maximum[1] 

def r0(graph):
  """
  Returns (setSize, numRecursiveCalls)
  """
  if not graph:
    return (0, 1)

  g = graph.copy()

  i = findVertexOfDegree(0, graph)
  if i is not None:
    g.pop(i)
    (setSize, count) = r0(g)
    return (setSize + 1, count + 1) 

  i = findVertexOfMaxDegree(graph)
  v = g.pop(i)
  (setSize2, count2) = r0(g)
  
  for j in v.neighbors:
    g.pop(j, None) # remove vertex j without throwing an error
  (setSize1, count1) = r0(g)
 
  return (max(setSize1 + 1, setSize2), count1 + count2 + 1)
  
def r1(graph):
  """
  Returns (setSize, numRecursiveCalls)
  """
  if not graph:
    return (0, 1)
  
  g = graph.copy()

  i = findVertexOfDegree(1, graph)
  if i is not None:
    v = g.pop(i) # remove vertex i, which has only 1 neighbor
    for j in v.neighbors:
      g.pop(j, None) # remove vertex j without throwing an error
    (setSize, count) = r1(g)
    return (setSize + 1, count + 1) 

  i = findVertexOfDegree(0, graph)
  if i is not None:
    g.pop(i)
    (setSize, count) = r1(g)
    return (setSize + 1, count + 1) 

  i = findVertexOfMaxDegree(graph)
  v = g.pop(i)
  (setSize2, count2) = r1(g)

  for j in v.neighbors:
    g.pop(j, None) # remove vertex j without throwing an error
  (setSize1, count1) = r1(g)
  
  return (max(setSize1 + 1, setSize2), count1 + count2 + 1)

def r2(graph):
  """
  Returns (setSize, numRecursiveCalls)
  """
  if not graph:
    return (0, 1)
  
  g = graph.copy()

  i = findVertexOfDegree(2, graph)
  if i is not None:
    v = g.pop(i)
    neighbors = v.getNeighbors(graph)
    u = neighbors[0]
    w = neighbors[1]
    if u not in graph[w].getNeighbors(g):
      global numVertices
      neighbors = g[u].getNeighbors(g)
      for neighbor in g[w].getNeighbors(g):
        if neighbor not in neighbors:
          neighbors.append(neighbor)
      z = Vertex(numVertices + 1, neighbors)
      numVertices += 1
      g[z.num] = z

    g.pop(u)
    g.pop(w)
    (setSize, count) = r2(g)
    return (setSize + 1, count + 1)

  i = findVertexOfDegree(1, graph)
  if i is not None:
    v = g.pop(i) # remove vertex i, which has only 1 neighbor
    for j in v.neighbors:
      g.pop(j, None) # remove vertex j without throwing an error
    (setSize, count) = r2(g)
    return (setSize + 1, count + 1) 

  i = findVertexOfDegree(0, graph)
  if i is not None:
    g.pop(i)
    (setSize, count) = r2(g)
    return (setSize + 1, count + 1) 

  i = findVertexOfMaxDegree(graph)
  v = g.pop(i)
  (setSize2, count2) = r2(g)

  for j in v.neighbors:
    g.pop(j, None) # remove vertex j without throwing an error
  (setSize1, count1) = r2(g)
  
  return (max(setSize1 + 1, setSize2), count1 + count2 + 1)

def main():
  global numVertices
  numVertices = int(sys.argv[1])
  graph = readGraph(numVertices)
  if sys.argv[2] == "r0":
    (setSize, numCalls) = r0(graph)
  elif sys.argv[2] == "r1":
    (setSize, numCalls) = r1(graph)
  else:
    (setSize, numCalls) = r2(graph)
  print "setSize: ", setSize, "numCalls: ", numCalls

if __name__ == "__main__":
  main()
