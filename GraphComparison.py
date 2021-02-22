import csv
import time
import utils
import os.path
class GraphComparison:
    """
      GraphComparison for showing the difference in computation methods between standard graphs and GraphFrame
      spark_context: the spark context to distribute the computation
      standard_graph: normal graph implemented with adjacency lists
      spark_graph: graph created using graphframe
    """
    def __init__(self, spark_context, standard_graph, spark_graph, dataset_name):
        self._spark_context = spark_context
        self._standard_graph = standard_graph
        self._spark_graph = spark_graph
        self._dataset_name = dataset_name

    '''
    Compares the computational times for calculating connected component of a graph
    between the standard graph and the graphframe and write the results in a csv files
    '''
    def compareTimesConnectedComponents(self):
        csv_path_name = 'Results/ConnectedComponents.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)']
            utils.write_results_csv(csv_path_name, row)

        print("StandardGraph calculating list of connected components")
        start = time.time()
        SGcc = self._standard_graph.connectedComponents()
        end = time.time()
        standard_graph_time = end - start
        print("\n StandardGraph time elapsed to retrive connected components:" + str(standard_graph_time))

        #get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        print("GraphFrame calculating list of connected components")
        start = time.time()
        GFcc = self._spark_graph._spark_graph.connectedComponents(algorithm='graphframes')
        end = time.time()
        graph_frame_time = end - start
        print("\n GraphFrame time elapsed to retrive connected components:" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time, self._dataset_name])

    '''
    This method compare the computational times for calculating strongly connected component of a graph between
    the standard graph and the graphframe and write the results in a csv files
    '''
    def compareTimesStronglyConnectedCompontents(self):
        csv_path_name = 'Results/StronglyConnectedComponents.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)']
            utils.write_results_csv(csv_path_name, row)

        print("StandardGraph calculating list of strongly connected components")
        start = time.time()
        SGscc = self._standard_graph.stronglyConnectedComponents()
        end = time.time()
        standard_graph_time = end - start
        print("\n StandardGraph time elapsed to retrive strongly connected components:" + str(standard_graph_time))

        # get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        print("GraphFrame calculating list of connected components")
        start = time.time()
        GFscc = self._spark_graph._spark_graph.stronglyConnectedComponents(1)
        end = time.time()
        graph_frame_time = end - start
        print("\n GraphFrame time elapsed to retrive strongly connected components:" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time, self._dataset_name])

    '''
    Compares the computational times for calculating the node with the max value of a given attribute
    attribute: attribute of the node that you want to query and write the results in a csv files
    '''
    def compareTimesMaxAttribute(self, attribute):
        csv_path_name = 'Results/Max' + attribute + '.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)']
            utils.write_results_csv(csv_path_name, row)

        startingNode = "1000"

        print("StandardGraph calculating max value of nodes attribute " + attribute + "...\n")
        start = time.time()
        sg_value = self._standard_graph.nodeWithMaxValueOfAttribute(startingNode, attribute)
        end = time.time()
        standard_graph_time = end - start
        print("\n StandardGraph time elapsed to max value of nodes attribute " + attribute + ":" + str(standard_graph_time))

        # get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        print("GraphFrame calculating max value of nodes attribute " + attribute + "...\n")
        start = time.time()
        gf_value = self._spark_graph._spark_graph.vertices.groupBy().max(attribute)
        end = time.time()
        graph_frame_time = end - start
        print("\n GraphFrame time elapsed to max value of nodes attribute " + attribute + ":" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time, self._dataset_name])

    '''
    Compares the computational times for retriving a list of nodes that satisfy a particular query and write the results in a csv files
    query: tuple of three element (parameter_name, operator, value_to_search) e.g ("views", "<", 2000)
    '''
    def compareTimesBFSQuery(self, query):
        (parameter_name, operator, value_to_search) = query.split(" ")
        csv_path_name = 'Results/BFSQuery' + parameter_name + operator + value_to_search + '.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)']
            utils.write_results_csv(csv_path_name, row)

        startingNode = 1000

        print("StandardGraph calculating list of nodes from " + str(startingNode) + " that have " + query + "...\n")
        #get time for query in standard graph
        start = time.time()
        self._standard_graph.BFSQuery(startingNode, parameter_name, operator, value_to_search)
        end = time.time()
        standard_graph_time = end - start
        print("StandardGraph time elapsed to retrive list of nodes:" + str(standard_graph_time))

        #get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        #get time for query in spark graph
        print("GraphFrame calculating list of nodes from " + str(startingNode) + " that have " + query + "...\n")
        start = time.time()
        self._spark_graph._spark_graph.bfs("id = " + str(startingNode), query)
        end = time.time()
        graph_frame_time = end - start
        print("StandardGraph time elapsed to retrive list of nodes:" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time, self._dataset_name])

    '''
    Compares the computational times for calculating the number of triangles in the graph and write the results in a csv files 
    '''
    def compareTimesCountTriangle(self):
        csv_path_name = 'Results/CountTriangles.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)']
            utils.write_results_csv(csv_path_name, row)

        print("StandardGraph calculating number of triangles in the graph")
        start = time.time()
        #SG_no_of_triangles = self._standard_graph.countTriangle(True)
        end = time.time()
        standard_graph_time = end - start
        print("\n StandardGraph time elapsed to retrive the number of triangles in the graph:" + str(standard_graph_time))

        # get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        print("GraphFrame calculating number of triangles in the graph")
        start = time.time()
        GF_no_of_triangles = self._spark_graph._spark_graph.triangleCount().count()
        end = time.time()
        graph_frame_time = end - start
        print("\n GraphFrame time elapsed to retrive the number of triangles in the graph" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time, self._dataset_name])

    '''
     Compares the computational times for calculating the indegree of every node in the graph
     '''
    def compareTimesIndegreeOfGraph(self):
        csv_path_name = 'Results/Indegree.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)', 'Dataset']
            utils.write_results_csv(csv_path_name, row)

        print("StandardGraph calculating indegree for every node in the graph")
        start = time.time()
        dict_indegree = self._standard_graph.calculateInDegrees()
        end = time.time()
        standard_graph_time = end - start
        print("\n StandardGraph time elapsed to retrive the indegree for every node in the graph:" + str(standard_graph_time))

        # get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        print("GraphFrame calculating indegree for every node in the graph")
        start = time.time()
        df_with_indegree = self._spark_graph.inDegree()
        end = time.time()
        graph_frame_time = end - start
        print("\n GraphFrame time elapsed to retrive the indegree for every node in the graph:" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time, self._dataset_name])

        '''
        Compares the computational times for calculating the shortest path between a source node and a sink node
        '''

    def compareTimesShortestPath(self, source, sink):
        csv_path_name = 'Results/ShortestPath.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)', 'Dataset']
            utils.write_results_csv(csv_path_name, row)

        print("StandardGraph calculating shortest path between " + source + " and " + sink + ":")
        start = time.time()
        shortest_path = self._standard_graph.ShortestPath(source, sink)
        end = time.time()
        standard_graph_time = end - start
        print("\n StandardGraph time elapsed to retrive the shortest path:" + str(
            standard_graph_time))

        # get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        print("GraphFrame  calculating shortest path between " + source + " and " + sink + ":")
        start = time.time()
        shortest_path = self._spark_graph.shortestPath(source, sink)
        end = time.time()
        graph_frame_time = end - start
        print("\n GraphFrame time elapsed to retrive the shortest path:" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time, self._dataset_name])