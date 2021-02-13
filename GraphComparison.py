import utils

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
    def compareTimesBFSQuery(selfs, query):
        pass