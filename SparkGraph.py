import pandas as pd
from graphframes import *


class SparkGraph:
    def __init__(self, spark_session, nodes_csv, edges_csv):
        cols_names_edges = ['src', 'dst']
        cols_names_nodes = ['long_id', 'days', 'mature', 'views', 'partner', 'id']
        edges_df = pd.read_csv(edges_csv, names=cols_names_edges, header=1)
        nodes_df = pd.read_csv(nodes_csv, names=cols_names_nodes, header=1)
        edgesSparkDf = spark_session.createDataFrame(edges_df)
        nodesSparkDf = spark_session.createDataFrame(nodes_df)
        self._spark_graph = GraphFrame(nodesSparkDf, edgesSparkDf)