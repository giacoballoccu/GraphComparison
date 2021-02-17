# Graph Comparison

1. [Introduction](#Introduction)
2. [Project structure](#Project-structure)
3. [Implementation](#Implementation)
4. [Initialize project in your machine](#Initialize-project-in-your-machine)
6. [Table of results](#Table-of-results)
8. [References](#References)

## Introduction
The purpose of this project is to compare a graph class and its method against the state of art Pyspark class for graph operations (GraphFrame). Compare the results, in time of execution and show the superiority of parallel computing against not parallelized data structures when dealing with high dimensional data. Also, the project has the purpose of showing the relationship between the number of workers nodes and computation times for graph related problems. The dataset used is the Twitch-Social-Network dataset [1] of Standard university which is composed of 7,126 nodes and 35,324 edges. 

## Project structure


## Implementation
Graph algorithm that you can test with this project:
- Retriving of the node with the max value of a numeric attribute
- Retriving of the list of connected component
- Retriving a list of node that satify a particular query
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
**Note:** without setting the other variables (you can find it on variables.tf), terraform will create a cluster on region "us-east-1", with 1 namenode, 3 datanode and with an instance type of t2.medium.

3. Download the files from this repository
4. Put the files of this repository into the "app" terraform project folder (e.g. example.py should be in spark-terraform-master/app/example.py and so on for all the other files)
5. Create a zip archive of the TransEmodule folder and put it on spark-terraform-master/app/TransEmodule.zip
6. Open a terminal and generate a new ssh-key
```
ssh-keygen -f <PATH_TO_SPARK_TERRAFORM>/spark-terraform-master/localkey
```
Where `<PATH_TO_SPARK_TERRAFORM>` is the path to the /spark-terraform-master/ folder (e.g. /home/user/)

7. Login to AWS and create a key pairs named **GraphComparison** in **PEM** file format. Follow the guide on [AWS DOCS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair). Download the key and put it in the spark-terraform-master/ folder.

8. Open a terminal and go to the spark-terraform-master/ folder, execute the command
 ```
 terraform init
 terraform apply
 ```
 After a while (wait!) it should print some public DNS in a green color, these are the public dns of your instances.
 It can happen that the command doesn't work (with an error like "Connection timeout"), usually it can be solved by doing a `terraform destroy` and re-do the `terraform apply`.

9. Connect via ssh to all your instances via
 ```
ssh -i <PATH_TO_SPARK_TERRAFORM>/spark-terraform-master/GraphComparison.pem ubuntu@<PUBLIC DNS>
 ```
If Terraform for some reason didn't print the DNS of the nodes you can find the public dns of the master as the node s01 in your aws console.
10. Execute on the master (one by one):
 ```
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver
$SPARK_HOME/sbin/start-master.sh
hdfs dfs -put /home/ubuntu/dataset/train2.tsv /train2.tsv
hdfs dfs -put /home/ubuntu/dataset/test2.tsv /test2.tsv
$SPARK_HOME/sbin/start-slaves.sh spark://s01:7077

 ```

11. You are ready to execute GraphComparison! Execute this command on the master
```
/opt/spark-3.0.1-bin-hadoop2.7/bin/spark-submit --master spark://s01:7077  --executor-cores 2 --executor-memory 2g main.py
```
Based on what machine you chose you will be able to change the number of cores used and the amount of ram memory allocated for the tasks. If you would like to use a dataset different from the ENGB pay attention from the output of this command; if you get this warn message:
```
WARN scheduler.TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources
```
That means that you have allocated an insufficient amount of resources or others task have a lock on them. You can check the jobs being executed with the spark UI at the following link:
```
<PUBLIC DNS OF YOUR MASTER NODE>:8080
```
Sometimes it happen that some iteration takes much more time than the others. The causes could be 1) in the install-all.sh there are more workers defined than the real number of workers (e.g. if we are using 2 workers, we need to delete s04, s05 and s06 from lines 166 and 204 of install-all.sh) 2) aws is throttling the resources of the instances. We usually resolve these problems by destroying the instances and waiting some time before re-running them.

12. Remember to do `terraform destroy` to delete your EC2 instances

**Note:** The steps from 0 to 7 (included) are needed only on the first execution ever
## Table of results

## References
\[1\] https://snap.stanford.edu/data/twitch-social-networks.html
\[2\] https://github.com/conema/spark-terraform
