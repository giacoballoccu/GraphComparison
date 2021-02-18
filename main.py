import time

import pyspark
import findspark
from pyspark.sql import SparkSession
from StandardGraph import *
from SparkGraph import *
from GraphComparison import *

def main():
    os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/openjdk-13.0.2.jdk/Contents/Home"
    os.environ["SPARK_HOME"] = "spark-3.0.1-bin-hadoop3.2"
    edge_path = "Dataset/twitch/DE/musae_DE_edges.csv"
    nodes_path = "Dataset/twitch/DE/musae_DE_target.csv"
    dataset_name = edge_path.split("/")[2]
    findspark.init()
    SUBMIT_ARGS = "--packages graphframes:graphframes:0.8.1-spark3.0-s_2.12 pyspark-shell"
    os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
    conf = pyspark.SparkConf()
    sc = pyspark.SparkContext(conf=conf)
    ss = SparkSession(sc)
    ss._jsc.addJar("Jars/graphframes-0.8.1-spark3.0-s_2.12.jar")
    sc.setCheckpointDir('checkpoints')
    print(sc._conf.getAll())

    #Initalize the two graphs and the compator
    standardGraph = StandardGraph(nodes_path, edge_path)
    sparkGraph =  SparkGraph(ss, nodes_path, edge_path)
    comparator = GraphComparison(ss, standardGraph, sparkGraph, dataset_name)
    query = "id = 6780"

    comparator.compareTimesBFSQuery(query)
    comparator.compareTimesConnectedComponents()
    comparator.compareTimesMaxAttribute("views")
    comparator.compareTimesStronglyConnectedCompontents()
    comparator.compareTimesCountTriangle()
if __name__ == "__main__":
    main()
