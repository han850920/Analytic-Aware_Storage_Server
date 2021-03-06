import csv
import numpy as np
import yaml
import sys
with open('configuration_manager/config.yaml','r') as yamlfile:
    data = yaml.load(yamlfile,Loader=yaml.FullLoader)
from optimal_downsampling_manager.resource_predictor.estimate_table import get_context, get_month_and_day
from influxdb import InfluxDBClient
DBclient = InfluxDBClient(data['global']['database_ip'], data['global']['database_port'], 'root', 'root', "exp_storage")
# algo_list = ["FIFO", "opt", "heuristic", "EF", "EFR", "approx"]
algo_list = ["heuristic"]

for algo in algo_list:
#     ## Hour <--> IA
    result = DBclient.query("SELECT * FROM log_every_hour_"+algo)
    result_list = list(result.get_points(measurement = "log_every_hour_"+algo))
    count=0
    prev_amount = 0
    with open("experiments/P_"+algo+"_ia_hours.csv",'w') as csvfile:
        writer = csv.writer(csvfile)
        for r in result_list:
            while count != int(r['hour']):
                writer.writerow([prev_amount])
                count = (count+1)%24            

            writer.writerow([r['total_ia']])
            prev_amount = float(r['total_ia'])
            count = (count+1)%24

    ## Hour <--> clips
    result = DBclient.query("SELECT * FROM log_every_hour_"+algo)
    result_list = list(result.get_points(measurement = "log_every_hour_"+algo))
    count=0
    prev_amount = 0
    with open("experiments/P_"+algo+"_clips_hours.csv",'w') as csvfile:
        writer = csv.writer(csvfile)
        for r in result_list:
            while count != int(r['hour']):
                writer.writerow([prev_amount])
                count = (count+1)%24            

            writer.writerow([r['total_clips_number']])
            prev_amount = int(r['total_clips_number'])
            count = (count+1)%24

    ### Hour <--> space
    result = DBclient.query("SELECT * FROM log_every_hour_"+algo)
    result_list = list(result.get_points(measurement = "log_every_hour_"+algo))
    count=0
    prev_amount = 0
    with open("experiments/P_"+algo+"_space_hours.csv",'w') as csvfile:
        writer = csv.writer(csvfile)
        for r in result_list:
            while count != int(r['hour']):
                writer.writerow([prev_amount])
                count = (count+1)%24            

            writer.writerow([r['total_size']])
            prev_amount = int(r['total_size'])
            count = (count+1)%24

## Hour <--> Downsampling Time 
# for algo in algo_list[1:]:
#     result = DBclient.query("SELECT * FROM P_exp_result_"+algo)
#     result_list = list(result.get_points(measurement = "P_exp_result_"+algo))
#     ti=[]
#     for r in result_list:
#         ti.append(r['time_sum'])
#     ti = np.array(ti)
#     avg = np.mean(ti)
#     err = 1.96*(np.std(ti)/ti.shape[0])
#     with open("experiments/P_"+algo+"_downsampling_time_GB.csv",'w') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow([avg,err])



## Hour <--> Algo runnning Time 
# for algo in algo_list:
#     ### Hours <--> Information Amount 
#     result = DBclient.query("SELECT * FROM P_exp_result_"+algo)
#     result_list = list(result.get_points(measurement = "P_exp_result_"+algo))

#     ti=[]

#     for r in result_list:
#         ti.append(r['algo_exec_time'])
    
#     ti = np.array(ti)

#     avg = np.mean(ti)
#     err = 1.96*(np.std(ti)/ti.shape[0])

#     print(algo, avg, err)

# no_pca = []
# with open('query_ia_heuristic_unseen_no_pca_14.csv','r') as csvfile:
#     rows = csv.reader(csvfile)
#     for row in rows:
#         no_pca.append(float(row[0]))
# no_pca = np.array(no_pca)
# avg_no_pca = np.mean(no_pca)
# no_pca_err = 1.96*(np.std(no_pca)/no_pca.shape[0])
# print("avg_no_pca",avg_no_pca,"no_pca_err", no_pca_err)

# pca = []
# with open('query_ia_heuristic_unseen_with_pca_14.csv','r') as csvfile:
#     rows = csv.reader(csvfile)
#     for row in rows:
#         pca.append(float(row[0]))
# pca = np.array(pca)
# avg= np.mean(pca)
# pca_err = 1.96*(np.std(pca)/pca.shape[0])

# print("avg_pca",avg,"pca_err", pca_err)

