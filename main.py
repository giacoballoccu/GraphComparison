import time

import pyspark
from pyspark.sql import SparkSession

import StandardGraph
import SparkGraph
import GraphComparison
def main():
    conf = pyspark.SparkConf()
    sc = pyspark.SparkContext(conf=conf)
    ss = SparkSession(sc)
    print(sc._conf.getAll())

    standardGraph = StandardGraph("Dataset/twitch/ENGB/musae_ENGB_target.csv", "Dataset/twitch/ENGB/musae_ENGB_edges.csv")
    sparkGraph =  SparkGraph("Dataset/twitch/ENGB/musae_ENGB_target.csv", "Dataset/twitch/ENGB/musae_ENGB_edges.csv")
    compator = GraphComparison(sc, standardGraph, sparkGraph)

if __name__ == "__main__":
    main()
