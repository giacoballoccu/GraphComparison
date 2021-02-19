# Graph Comparison

1. [Introduction](#Introduction)
2. [Project structure](#Project-structure)
3. [Implementation](#Implementation)
4. [Initialize project in your machine](#Initialize-project-in-your-machine)
6. [Table of results](#Table-of-results)
8. [References](#References)

## Introduction
The purpose of this project is to compare a graph class and its method against the state of art Pyspark class for graph operations (GraphFrame). Compare the results, in time of execution and show the superiority of parallel computing against not parallelized data structures when dealing with high dimensional data. Also, the project has the purpose of showing the relationship between the number of workers nodes and computation times for graph-related problems. The dataset used is the Twitch-Social-Network dataset [1] of Standard university. In particular, almost all the tests are run on the twitch/ENGB dataset which is composed of 7,126 nodes and 35,324 edges. In addition to these results, a stress-test has been done with the twitch/DE dataset which has 153,138 edges and 9498 nodes.

## Project structure
All the tests and experimented were performed on collaboratory with the GraphMethodsComparison.ipynb file before the landing on the AWS platform of the project. Starting from that file all the stuff has been divided into 3 main classes:
* StandardGraph.py: This class is a personal implementation of a graph in Python using nodes adjacency list and an additional hashmap to carry nodes attributes and values.
* SparkGraph.py: This class is the parallelized version of the graph. It has only one attribute which is a spark GraphFrame object. Thanks to the init it is possible to construct directly the graph from the target.csv and edges.csv (check their headers and composition to see if you can fit your dataset).
* GraphComparison.py: This class is the comparator for the two graphs. It needs an instance of StandardGraph, one of SparkGraph and the spark context to be initialized. Inside this function there are all the methods to run and compare the following graph methods:
  * Retrieve nodes that satisfy a particular query.
  * Retrieve the node that has the max value of a given parameter.
  * Retrieve connected components.
  * Retrieve strongly connected components.
  * Count the number of triangles.  

All of these methods are differently implemented for the StandardGraph (which doesn't need to exploit parallelization) and GraphFrame. The timing of every method execution is recorded in the Results/<Name of the task>.csv file in order to compare them and draw conclusions.

* Main.py is just a main, it does initializations and runs all the graphComparison methods.  

## Implementation
Every method used for the standardGraph is a well-known algorithm. 
* BFSQuery(): Just a breadth first search in the entire graph, if the nodes satisfy the query it gets added to the result time complexity: O(v)
* nodeWithMaxValueOfAttribute(): Same principle of BFSQuery() time complexity: O(v)
* connectedComponents(): Retrived using a DFS search helper, time complexity: O(v+e)
* stronglyConnectedComponents(): Tarjan’s Algorithm implementation, time complexity: O(v+e).
* countTriangles(): Without matrix trace approach time complexity: O(v^3).


Where v # of vertices and e # of edges.  


The methods of the SparkGraph are the ones present in the GraphFrame python library. You can have more information about the methods used in this project and many more in the GraphFrame documentation: https://graphframes.github.io/graphframes/docs/_site/user-guide.html

Regarding the AWS setup, it has been done using Terraform and using a good project from a friend and colleague that you can find at [2]. With some tweaks in the parameters and following the guideline is possible to land to terraform safely.

You can find more about the implementation, results, and conclusions in the GraphComparisonReport.pdf file.
## Initialize project in your machine
0. Download and install Terraform
1. Download the terraform project from [3] and unzip it
2. Open the terraform project folder "spark-terraform-master/"
3. Create a file named "terraform.tfvars" and paste this:
```
access_key="<YOUR AWS ACCESS KEY>"
secret_key="<YOUR AWS SECRET KEY>"
token="<YOUR AWS TOKEN>"
aws_key_name="GraphComparison"
amz_key_path="GraphComparison.pem"
```
**Note:** without setting the other variables (you can find it on variables.tf), terraform will create a cluster on the region "us-east-1", with 1 namenode, 3 datanode and with an instance type of t2.medium.

3. Download the files from this repository
4. Put the files of this repository into the "app" terraform project folder (e.g. example.py should be in spark-terraform-master/app/main.py and so on for all the other files)
5. Open a terminal and generate a new ssh-key
```
ssh-keygen -f <PATH_TO_SPARK_TERRAFORM>/spark-terraform-master/localkey
```
Where `<PATH_TO_SPARK_TERRAFORM>` is the path to the /spark-terraform-master/ folder (e.g. /home/user/)

6. Login to AWS and create a key pair named **GraphComparison** in **PEM** file format. Follow the guide on [AWS DOCS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair). Download the key and put it in the spark-terraform-master/ folder.

7. Open a terminal and go to the spark-terraform-master/ folder, execute the command
 ```
 terraform init
 terraform apply
 ```
 After a while (wait!) it should print some public DNS in a green color, these are the public dns of your instances.
 It can happen that the command doesn't work (with an error like "Connection timeout"), usually it can be solved by doing a `terraform destroy` and re-do the `terraform apply`.

8. Connect via ssh to all your instances via
 ```
ssh -i <PATH_TO_SPARK_TERRAFORM>/spark-terraform-master/GraphComparison.pem ubuntu@<PUBLIC DNS>
 ```
If Terraform for some reason didn't print the DNS of the nodes you can find the public dns of the master as the node s01 in your aws console.
9. Connect to the master and execute (one by one):
 ```
cp Jars/graphframes-0.8.1-spark3.0-s_2.12.jar /opt/spark-3.0.1-bin-hadoop2.7/jars/graphframes-0.8.1-spark3.0-s_2.12.jar
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slaves.sh spark://s01:7077
 ```

10. You are ready to execute GraphComparison! Execute this command on the master
```
/opt/spark-3.0.1-bin-hadoop2.7/bin/spark-submit --master spark://s01:7077  --executor-cores 2 --executor-memory 2g main.py
```
10a. Common error in this phase.  
Based on what machine you chose you will be able to change the number of cores used and the amount of RAM allocated for the tasks. If you would like to use a dataset different from the ENGB pay attention to the output of this command; if you get this warn message:
```
WARN scheduler.TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources
```
That means that you have allocated an insufficient amount of resources or other tasks have a lock on them. You can check the jobs being executed with the spark UI at the following link:
```
<PUBLIC DNS OF YOUR MASTER NODE>:8080
```
Sometimes it happens that some iteration takes much more time than the others. The causes could be 1) in the install-all.sh there are more workers defined than the real number of workers (e.g. if we are using 2 workers, we need to delete s04, s05 and s06 from lines 166 and 204 of install-all.sh) 2) aws is throttling the resources of the instances. We usually resolve these problems by destroying the instances and waiting some time before re-running them.

12. Remember to do `terraform destroy` to delete your EC2 instances

**Note:** The steps from 0 to 7 (included) are needed only on the first execution ever
## Table of results
Retrieve nodes that satisfy a particular query.
|NoOfWorkers|GraphClass time (s)|GraphFrame time (s)|Dataset|
|---|---|---|---|
|2|0.000423431396484375|37.88420820236206|ENGB|
|3|0.0003943443298339844|32.59935522079468|ENGB|
|5|0.0004055500030517578|36.94925403594971|ENGB|
|6|0.0004177093505859375|27.606682062149048|ENGB|
|4|0.015209436416625977|23.92878246307373|DE|

Retrieve the node that has the max value of a given parameter.
|NoOfWorkers|GraphClass time (s)|GraphFrame time (s)|Dataset|
|---|---|---|---|
|2|0.0006043910980224609|0.018646240234375|ENGB|
|3|0.0004267692565917969|0.009284496307373047|ENGB|
|5|0.00044655799865722656|0.010093927383422852|ENGB|
|6|0.00043702125549316406|0.011041641235351562|ENGB|
|4|0.039754629135131836|0.02134227752685547|DE|

Retrieve connected components.
|NoOfWorkers|GraphClass time (s)|GraphFrame time (s)|Dataset|
|---|---|---|---|
|2|0.01049494743347168|102.73485112190247|ENGB|   
|3|0.009637594223022461|74.6495943069458|ENGB|
|5|0.009996652603149414|81.32360482215881|ENGB|
|6|0.010695457458496094|82.51052212715149|ENGB|
|4|0.0259702205657959|73.20449471473694|DE|

Retrieve strongly connected components.

|NoOfWorkers|GraphClass time (s)|GraphFrame time (s)|Dataset|
|---|---|---|---|
|2|0.017906665802001953|15.816995620727539|ENGB|
|3|0.018994808197021484|18.190645933151245|ENGB|
|5|0.019264936447143555|19.353548049926758|ENGB|
|6|0.018758773803710938|21.704362869262695|ENGB|
|4|0.027454945792391022|out of time (over 10 minutes)|DE|

Count the number of triangles.

|NoOfWorkers|GraphClass time (s)|GraphFrame time (s)|Dataset|
|---|---|---|---|
|2|out of time (over 10 minutes)|29.846829891204834|ENGB
|3|out of time (over 10 minutes)|19.2566659450531|ENGB
|5|out of time (over 10 minutes)|19.41680598258972|ENGB
|6|out of time (over 10 minutes)|14.647715330123901|ENGB
|4|out of time (over 10 minutes)|86.29342651367188|DE

## References
\[1\] https://snap.stanford.edu/data/twitch-social-networks.html
\[2\] https://github.com/conema/spark-terraform
\[3\] https://github.com/giacoballoccu/spark-terraform
