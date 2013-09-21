class Vertex(object):
  self.num = None
  self.neighbors = None

  def __init__(self, num, neighbors = None):
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

