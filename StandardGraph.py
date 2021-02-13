import collections
import csv


class StandardGraph:
    adjacency_list = {}
    nodes_data = {}

    def __init__(self, adjacency_list=None, nodes_data=None):
        """ initializes a graph object
            If no dictionary or None is given for the parameter,
            an empty dictionary will be instead used
        """
        if (adjacency_list == None):
            self.adjacency_list = {}
        else:
            self.adjacency_list = adjacency_list

        if (nodes_data == None):
            self.nodes_data = {}
        else:
            self.nodes_data = nodes_data

    def __init__(self, nodes_csv, edges_csv):
        with open(edges_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                self.add_edge((row[0], row[1]))
        with open(nodes_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                id = row[-1]
                data = {'id': id, 'days': row[1], 'mature': row[2], 'views': row[3], 'partner': row[4],
                        'long_id': row[0]}
                self.add_node_data(id, data)

    def nodes(self):
        """ returns the vertices of the graph """
        return list(self.adjacency_list.keys())

    def edges(self):
        """ returns the edges of the graph """
        return self.generate_edges()

    def add_node_data(self, node, data):
        if node not in self.nodes_data:
            self.nodes_data[node] = data

    def add_edge(self, edge):
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

    def generate_edges(self):
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

    def bfs(self, root, targetNode):
        matchingCriteriaNodes = []
        visited, queue = set(), collections.deque([root])
        visited.add(root)

        while queue:

            # Dequeue a node from queue
            node = queue.popleft()
            print(str(node) + " -> ", end="")
            if (node == targetNode):
                print("\nNode " + str(node) + " found!")
                return
            # If not visited, mark it as visited, and
            # enqueue it
            for neighbour in self.adjacency_list[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

    def max_views_node(self, root):
        visited, queue = set(), collections.deque([root])
        visited.add(root)
        maxViewsSoFar = float('-inf')
        while queue:
            # Dequeue a node from queue
            node = queue.popleft()
            # print(str(node) + " -> ", end="")
            maxViewsSoFar = max(maxViewsSoFar, (float)(self.nodes_data[node]['views']))

            # If not visited, mark it as visited, and
            # enqueue it
            for neighbour in self.adjacency_list[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return maxViewsSoFar

    def dfs(self, node, acc, visited={}):
        # Mark the current vertex as visited
        visited[node] = True

        # Store the vertex to list
        acc.append(node)

        # Repeat for all vertices adjacent
        # to this vertex v
        for neighbour in self.adjacency_list[node]:
            if visited[neighbour] == False:
                # Update the list
                acc = self.dfs(neighbour, acc, visited)
        return acc

    def connectedComponents(self):
        visited = {}
        cc = []
        for node in self.adjacency_list.keys():
            visited[node] = False
        for node in self.adjacency_list.keys():
            if visited[node] == False:
                acc = []
                cc.append(self.dfs(node, acc, visited))
        return cc