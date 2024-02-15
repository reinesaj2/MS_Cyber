class Graph(object):
   def degree(self, n):
      """
      Get degree of vertex as (in, out) pair
      """
      self.validIndex(n)
      inb, outb = 0, 0
      for j in self.vertices():  # Loop over all vertices
         if j != n:  # Exclude target vertex
            if self.hasEdge(j, n):  # If other vertex precedes
               inb += 1  # Increase inbound degree
            if self.hasEdge(n, j):  # If other vertex succeeds n
               outb += 1  # Increase outbound degree
      return (inb, outb)  # Return inbound and outbound degree

   def sortVertsTopologically(self):
      """
      Return sequence of all vertex indices sorted topologically more efficiently
      """
      vertsByDegree = [{} for _ in range(min(self.nVertices(), self.nEdges() + 1))]  # Hash table for every possible degree
      inDegree = [0] * self.nVertices()  # Allocate indegree array

      for vertex in self.vertices():  # Loop over all vertices, record inbound degree
         inDegree[vertex] = self.degree(vertex)[0]  # Inbound degree
         vertsByDegree[inDegree[vertex]][vertex] = 1  # Insert vertex in hash table for this inbound degree

      result = []  # Result list is initially empty
      while len(vertsByDegree[0]) > 0:  # While there are vertices with inbound degree of 0
         vertex, _ = vertsByDegree[0].popitem()  # Take vertex out of hash table
         result.append(vertex)  # Add it to end of result
         for s in self.adjacentVertices(vertex):  # Loop over vertex’s successors; move them to lower degree
            vertsByDegree[inDegree[s]].pop(s)  # Delete the successor
            inDegree[s] -= 1  # Decrease inbound degree of successor
            vertsByDegree[inDegree[s]][s] = 1  # Insert modified successor in hash table for lowered inbound degree

      if len(result) == self.nVertices():  # All vertices in result?
         return result  # Yes, then return it, otherwise cycle
      raise Exception('Cycle in graph, cannot sort')