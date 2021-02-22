import collections
import csv


class StandardGraph:
    adjacency_list = {}
    nodes_data = {}
    ''' Create graph from csv'''
    def __init__(self, nodes_csv, edges_csv):
        with open(edges_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                self.addEdge((row[0], row[1]))
        with open(nodes_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                id = row[-1]
                data = {'id': id, 'days': row[1], 'mature': row[2], 'views': row[3], 'partner': row[4],
                        'long_id': row[0]}
                self.addNodeData(id, data)

    def nodes(self):
        """ returns the nodes of the graph """
        return list(self.adjacency_list.keys())
    def noOfNodes(self):
        """ returns the number of nodes in the graph"""
        return len(self.adjacency_list.keys())
    def edges(self):
        """ returns the edges of the graph """
        return self.generateEdges()

    def addNodeData(self, node, data):
        """ add the node attributes associate to him in the hashmap"""
        if node not in self.nodes_data:
            self.nodes_data[node] = data

    def addEdge(self, edge):
        """ edge is a tuple of two nodes source and destination
            insert the nodes in the adjacency list key if they are not present and
            add the edge to the adjacency list
        """
        (vertex1, vertex2) = edge
        if vertex2 not in self.adjacency_list:
            self.adjacency_list[vertex2] = []

        if vertex1 in self.adjacency_list:
            self.adjacency_list[vertex1].append(vertex2)
        else:
            self.adjacency_list[vertex1] = [vertex2]

    def generateEdges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.adjacency_list:
            for neighbour in self.adjacency_list[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    """ Classic implementation of BFS using queque
        root: id of the node from where the traversal start
        attribute_name: the name of the attribute you want to query
        operator: mathematical operator for the query > < <= >= == !=
        attribute_value: value that you want the attribute to be
        query -> attribute_name operator attribute_value -> e.g. views > 2000
    """
    def BFSQuery(self, root, attribute_name, operator, attribute_value):
        candidateNodes = []
        visited, queue = set(), collections.deque([root])
        visited.add(root)

        while queue:

            # Dequeue a node from queue
            node = queue.popleft()
            node = str(node)
            try:
                if operator == '=':
                    if self.nodes_data[node][attribute_name] == attribute_value:
                        candidateNodes.append(node)
                elif operator == '<':
                    if self.nodes_data[node][attribute_name] < attribute_value:
                        candidateNodes.append(node)
                elif operator == '>':
                    if self.nodes_data[node][attribute_name] > attribute_value:
                        candidateNodes.append(node)
                elif operator == '<>':
                    if self.nodes_data[node][attribute_name] != attribute_value:
                        candidateNodes.append(node)
                elif operator == '>=':
                    if self.nodes_data[node][attribute_name] >= attribute_value:
                        candidateNodes.append(node)
                elif operator == '<=':
                    if self.nodes_data[node][attribute_name] <= attribute_value:
                        candidateNodes.append(node)
            except:
                print("Node key error")
            # If not visited, mark it as visited, and
            # enqueue it
            for neighbour in self.adjacency_list[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return candidateNodes

    ''' Works only for numeric values, get the node with the max value of a given attribute
        root: id of the node from where the traversal start
        attribute: attribute of the node of whom you want to find the max
    '''
    def nodeWithMaxValueOfAttribute(self, root, attribute):
        if attribute == 'partner' or attribute == 'mature':
            print("This function works only with numeric values, try to pass a attribute which is a integer or float")
            return
        visited, queue = set(), collections.deque([root])
        visited.add(root)
        maxValueOfAttribute = float('-inf')
        while queue:
            # Dequeue a node from queue
            node = queue.popleft()
            # print(str(node) + " -> ", end="")
            maxValueOfAttribute = max(maxValueOfAttribute, (float)(self.nodes_data[node][attribute]))

            # If not visited, mark it as visited, and
            # enqueue it
            for neighbour in self.adjacency_list[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return maxValueOfAttribute

    """ Depth first search helper for retriving connecting components
        acc: stores the nodes explored in a list
        visited: list of nodes already visit for avoid double couting
    """
    def DFSHelper(self, node, acc, visited={}):
        # Mark the current vertex as visited
        visited[node] = True

        # Store the vertex to list
        acc.append(node)

        # Repeat for all vertices adjacent
        # to this vertex v
        for neighbour in self.adjacency_list[node]:
            if visited[neighbour] == False:
                # Update the list
                acc = self.DFSHelper(neighbour, acc, visited)
        return acc

    """
    Get connected components of the graph and return them in a list
    """
    def connectedComponents(self):
        visited = {}
        cc = []
        for node in self.adjacency_list.keys():
            visited[node] = False
        for node in self.adjacency_list.keys():
            if visited[node] == False:
                acc = []
                cc.append(self.DFSHelper(node, acc, visited))
        return cc
    '''
    Get number of triangles in the graph
    isDirected: boolean that state if the graph is directed or not
    '''
    def countTriangle(self, isDirected):
        count_triangle = 0
        nodes = self.nodes()
        # Consider every possible
        # triplet of edges in graph
        already_checked_nodes = set()

        for i in nodes:
            for j in nodes:
                for k in nodes:
                    # check the triplet
                    # if it satisfies the condition
                    if (i != j and i != k and j != k and
                        j in self.adjacency_list[i] and
                        k in self.adjacency_list[j] and
                        i in self.adjacency_list[k]):
                        count_triangle += 1

        if isDirected:
            return count_triangle / 3
        else:
            return count_triangle / 6

    '''A recursive function that find finds and add them to a list strongly connected 
        components using DFSHelper traversal 
        u: The vertex to be visited next 
        disc: Stores discovery times of visited vertices 
        low: earliest visited vertex (the vertex with minimum 
                    discovery time) that can be reached from subtree 
                    rooted with current vertex 
         st: To store all the connected ancestors 
         stackMember: index array for faster check whether 
                      a node is in stack 
        '''

    def SCCHelper(self, node, low, disc, stackMember, st, time=0):
        # Initialize discovery time and low value
        disc[node] = time
        low[node] = time
        time += 1
        stackMember[node] = True
        st.append(node)

        # Go through all vertices adjacent to this
        for neighbor in self.adjacency_list[node]:

            # If v is not visited yet, then recur for it
            if disc[neighbor] == -1:

                self.SCCHelper(neighbor, low, disc, stackMember, st, time)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 (per above discussion on Disc and Low value)

                low[node] = min(low[node], low[neighbor])

            elif stackMember[neighbor] == True:

                '''Update low value of 'u' only if 'v' is still in stack 
                (i.e. it's a back edge, not cross edge). 
                Case 2 (per above discussion on Disc and Low value) '''
                low[node] = min(low[node], disc[neighbor])

                # head node found, pop the stack and print an SCC
        w = "-1"  # To store stack extracted vertices
        if low[node] == disc[node]:
            temp = []
            while w != node:
                w = st.pop()
                temp.append(w)
                stackMember[w] = False

        return temp
    '''
    Implementation of Tarjan's strongly connected components algorithm
    '''
    def stronglyConnectedComponents(self):

        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        disc = {}
        low = {}
        stackMember = {}
        for idx, node in enumerate(self.nodes()):
            disc[node] = -1
            low[node] = -1
            stackMember[node] = False
        st = []

        # Call the recursive helper function
        # to find articulation points
        # in DFSHelper tree rooted with vertex 'i'
        acc = []
        for node in self.nodes():
            if disc[node] == -1:
                acc.append(self.SCCHelper(node, low, disc, stackMember, st, 0))

        return acc


    def ShortestPath(self, start, goal):
        visited = []

        # Queue for traversing the graph with bfs fashion
        queue = [[start]]

        # If the desired node is
        # reached
        if start == goal:
            print("Same Node")
            return []

        # Loop to traverse the graph
        while queue:
            path = queue.pop(0)
            node = path[-1]

            # Condition to check if the current node is not visited
            if node not in visited:
                neighbours = self.adjacency_list[node]

                # Iterate over the neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    # Condition to check if the neighbour node is the goal
                    if neighbour == goal:
                        print("Shortest path = ", *new_path)
                        return new_path
                visited.append(node)

        #Doens't exists a path between start and goal
        print("A path between this two nodes doesn't exist")
        return []

    def calculateInDegrees(self):
        indegree = {}
        for node, neighbors in self.adjacency_list.keys():
            for neighbor in neighbors:
                indegree[neighbor] = indegree[neighbor] + 1

        return indegree