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
        pass
    def compareTimesStronglyConnectedCompontents(self):
        pass
    def compareTimesMaxAttribute(self):
        pass

    '''
    query: tuple of three element (parameter_name, operator, value_to_search)
    '''
    def compareTimesBFSQuery(self, query):
        (parameter_name, operator, value_to_search) = query.split(" ")
        csvpathname = 'Results/BFSQuery' + parameter_name + operator + value_to_search + '.csv'
        if not os.path.isfile(csvpathname):
            with open(csvpathname, mode='w') as results:
                writer = csv.writer(results)
                writer.writerow(['NoOfWorkers', 'GraphClass time (s)', 'GraphFrame time (s)'])
            results.close()

        startingNode = 1000

        print("StandardGraph calculating list of nodes from " + str(startingNode) + "that have " + query)
        #get time for query in standard graph
        start = time.time()
        self._standard_graph.bfs(startingNode, parameter_name, operator, value_to_search)
        end = time.time()
        standardGraphTime = end - start
        print("StandardGraph time elapsed to retrive connected components:" + str(standardGraphTime))

        #get noofworkers from spark context
        print("Retriving number of workers")
        noOfWorkers = self._spark_context._jsc.sc().getExecutorMemoryStatus().size()
        print("Number of workers deployed: " + str(noOfWorkers))

        #get time for query in spark graph
        print("GraphFrame calculating list of nodes from " + str(startingNode) + "that have " + query)
        start = time.time()
        self._spark_graph._spark_graph.bfs("id = " + str(startingNode), query)
        end = time.time()
        sparkGraphTime = end - start
        print("StandardGraph time elapsed to retrive connected components:" + str(sparkGraphTime))
        with open(csvpathname, mode='a') as results:
            writer = csv.writer(results)
            writer.writerow([noOfWorkers, standardGraphTime, sparkGraphTime])

        results.close()
