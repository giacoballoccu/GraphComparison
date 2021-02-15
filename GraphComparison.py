import csv
import time
import utils
import os.path
class GraphComparison:
    """
      GraphComparison for showing the difference in computation methods between standard graphs and GraphFrame
      spark_context: the spark context to distribute the computation

    """
    def __init__(self, spark_context, standard_graph, spark_graph):
        self._spark_context = spark_context
        self._standard_graph = standard_graph
        self._spark_graph = spark_graph

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

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time])

    def compareTimesStronglyConnectedCompontents(self):
        pass
    def compareTimesMaxAttribute(self, attribute):
        csv_path_name = 'Results/Max' + attribute + '.csv'
        if not os.path.isfile(csv_path_name):
            row = ['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)']
            utils.write_results_csv(csv_path_name, row)

        startingNode = "1000"

        print("StandardGraph calculating max value of nodes attribute " + attribute + "...\n")
        start = time.time()
        sg_value = self._standard_graph.node_with_max_value_of_attribute(startingNode, attribute)
        end = time.time()
        standard_graph_time = end - start
        print("\n StandardGraph time elapsed to max value of nodes attribute " + attribute + ":" + str(standard_graph_time))

        # get noofworkers from spark context
        noOfWorkers = utils.number_of_workers(self._spark_context)

        print("GraphFrame calculating max value of nodes attribute " + attribute + "...\n")
        start = time.time()
        gf_value = mostPopular = self._spark_graph._spark_graph.vertices.groupBy().max(attribute)
        end = time.time()
        graph_frame_time = end - start
        print("\n GraphFrame time elapsed to max value of nodes attribute " + attribute + ":" + str(graph_frame_time))

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time])

    '''
    query: tuple of three element (parameter_name, operator, value_to_search)
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
        self._standard_graph.bfs(startingNode, parameter_name, operator, value_to_search)
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

        utils.write_results_csv(csv_path_name, [noOfWorkers, standard_graph_time, graph_frame_time])

