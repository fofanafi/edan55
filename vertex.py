class Vertex(object):
  self.num = None
  self.neighbors = []

  def __init__(self, num, neighbors = []):
    self.num = num
    self.neighbors = neighbors
  
  def addNeighbor(self, vertex):
    if vertex not in self.neighbors:
      self.neighbors.append(vertex)

  def numEdges(self, vertexList):
    count = 0
    for vertex in self.neighbors:
      if vertex in vertexList:
        count += 1
    return count

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
  Returns (setSize, recursiveCount)
  """
  if not graph:
    return (0, 1)

  i = findVertexOfDegree(0, graph)
  if i:
    g = graph.copy()
    g.pop(i)
    (setSize, count) = r0(g)
    return (setSize + 1, count + 1) 

  i = findVertexOfMaxDegree(graph)
  g1 = graph.copy()
  v = g1.pop(i)
  for j in v.neighbors:
    g1.pop(j, None) # remove vertex j without throwing an error
  (setSize1, count1) = r0(g1)
  
  g2 = graph.copy()
  g2.pop(i)
  (setSize2, count2) = r0(g2)

  if setSize1 > setSize2:
    return (setSize1 + 1, count1 + count2 + 1)
  else:
    return (setSize2, count1 + count2 + 1)
