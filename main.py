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
    findspark.init()
    SUBMIT_ARGS = "--packages graphframes:graphframes:0.8.1-spark3.0-s_2.12 pyspark-shell"
    os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
    conf = pyspark.SparkConf()
    sc = pyspark.SparkContext(conf=conf)
    ss = SparkSession(sc)
    ss._jsc.addJar("Jars/graphframes-0.8.1-spark3.0-s_2.12.jar")
    print(sc._conf.getAll())

    standardGraph = StandardGraph("Dataset/twitch/ENGB/musae_ENGB_target.csv", "Dataset/twitch/ENGB/musae_ENGB_edges.csv")
    sparkGraph =  SparkGraph(ss, "Dataset/twitch/ENGB/musae_ENGB_target.csv", "Dataset/twitch/ENGB/musae_ENGB_edges.csv")
    comparator = GraphComparison(ss, standardGraph, sparkGraph)
    query = "views < 1000"
    comparator.compareTimesBFSQuery(query)

if __name__ == "__main__":
    main()
