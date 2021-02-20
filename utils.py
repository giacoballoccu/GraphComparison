import csv

""" write row in the csv file of results"""
def write_results_csv(path, row):
    with open(path, mode='a') as results:
        writer = csv.writer(results)
        writer.writerow(row)
    results.close()

"""return the number of workers used from the spark context"""
def number_of_workers(sc):
    print("Retriving number of workers")
    noOfWorkers = sc._jsc.sc().getExecutorMemoryStatus().size()
    print("Number of workers deployed: " + str(noOfWorkers))
    return  noOfWorkers