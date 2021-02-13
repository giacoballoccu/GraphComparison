import csv

def write_results_csv(path, row):
    with open(path, mode='a') as results:
        writer = csv.writer(results)
        writer.writerow(row)
    results.close()

def number_of_workers(self, sc):
    return sc._jsc.sc().getExecutorMemoryStatus().size()
