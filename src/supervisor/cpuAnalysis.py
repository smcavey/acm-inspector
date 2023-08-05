from prometheus_api_client import *
import datetime
import sys
import numpy as np
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

def checkCPUUsage(startTime, endTime, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking CPU Usage across the cluster")
    pc=promConnect()
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True

    status=clusterCPUCoreCapacity(pc,startTime, endTime, step)
    status=clusterCPUCoreUsed(pc,startTime, endTime, step)
    status=clusterCPUPctUsed(pc,startTime, endTime, step)
    status=clusterCPUUsage(pc,startTime, endTime, step)
    status=nodeCPUUsage(pc,startTime, endTime, step)
    status=kubeAPICPUUsage(pc,startTime, endTime, step)
    status=ACMCPUUsage(pc,startTime, endTime, step)
    status=ACMDetailCPUUsage(pc,startTime, endTime, step)
    status=OtherCPUUsage(pc,startTime, endTime, step)
    

    
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("CPU Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    return status
     
def clusterCPUCoreCapacity(pc,startTime, endTime, step):

    print("Total Cluster CPU Core Capacity")

    try:
        node_cpu = pc.custom_query('sum(instance:node_num_cpu:sum{job="node-exporter", cluster=""})')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "ClusterCPUCoreCap"}, inplace = True)
        print(node_cpu_df[['ClusterCPUCoreCap']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(instance:node_num_cpu:sum{job="node-exporter", cluster=""})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "ClusterCPUCoreCap"}, inplace = True)
        node_cpu_trend_df.plot(title="Cluster CPU Core Capacity",figsize=(30, 15))
        plt.savefig('../../output/cluster-cpu-core-cap.png')
        saveCSV(node_cpu_trend_df,"cluster-cpu-core-cap",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu core Capacity for cluster: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

def clusterCPUCoreUsed(pc,startTime, endTime, step):

    print("Total Cluster CPU Core usage")

    try:
        node_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster=""})')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "ClusterCPUCoreUsage"}, inplace = True)
        print(node_cpu_df[['ClusterCPUCoreUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster=""})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "ClusterCPUCoreUsage"}, inplace = True)
        node_cpu_trend_df.plot(title="Cluster CPU Core usage",figsize=(30, 15))
        plt.savefig('../../output/cluster-cpu-core-usage.png')
        saveCSV(node_cpu_trend_df,"cluster-cpu-core-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu core for cluster: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

def clusterCPUPctUsed(pc,startTime, endTime, step):

    print("Total Cluster CPU Pct usage")

    try:
        node_cpu = pc.custom_query('(1 - sum(avg by (mode) (rate(node_cpu_seconds_total{job="node-exporter", mode=~"idle|iowait|steal", cluster=""}[5m]))))*100')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "ClusterCPUPctUsage"}, inplace = True)
        print(node_cpu_df[['ClusterCPUPctUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='(1 - sum(avg by (mode) (rate(node_cpu_seconds_total{job="node-exporter", mode=~"idle|iowait|steal", cluster=""}[5m]))))*100',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "ClusterCPUPctUsage"}, inplace = True)
        node_cpu_trend_df.plot(title="Cluster CPU Pct usage",figsize=(30, 15))
        plt.savefig('../../output/cluster-cpu-pct-usage.png')
        saveCSV(node_cpu_trend_df,"cluster-cpu-pct-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu pct for cluster: ",e) 
        print(Style.RESET_ALL)   
    print("=============================================")
   
    status=True
    return status


def clusterCPUUsage(pc,startTime, endTime, step):

    print("Total Cluster CPU usage")

    try:
        node_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate)')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "ClusterCPUUsage"}, inplace = True)
        print(node_cpu_df[['ClusterCPUUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "ClusterCPUUsage"}, inplace = True)
        node_cpu_trend_df.plot(title="Cluster CPU usage",figsize=(30, 15))
        plt.savefig('../../output/cluster-cpu-usage.png')
        saveCSV(node_cpu_trend_df,"cluster-cpu-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu for cluster: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status  

def nodeCPUUsage(pc,startTime, endTime, step):

    print("CPU Usage across Nodes")

    try:
        node_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate) by (node)')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "NodeCPUCoreUsage"}, inplace = True)
        print(node_cpu_df[['node','NodeCPUCoreUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate) by (node)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "NodeCPUCoreUsage"}, inplace = True)
        node_cpu_trend_df.plot(title="CPU Core Usage across Nodes",figsize=(30, 15))
        plt.savefig('../../output/breakdown/node-cpu-usage.png')
        saveCSV(node_cpu_trend_df,"node-cpu-usage")
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu usage across Nodes: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status   

def kubeAPICPUUsage(pc,startTime, endTime, step):

    print("Total Kube API Server CPU Core usage")

    try:
        kubeapi_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"openshift-kube-apiserver|openshift-etcd"})')

        kubeapi_cpu_df = MetricSnapshotDataFrame(kubeapi_cpu)
        kubeapi_cpu_df["value"]=kubeapi_cpu_df["value"].astype(float)
        kubeapi_cpu_df.rename(columns={"value": "KubeAPICPUCoreUsage"}, inplace = True)
        print(kubeapi_cpu_df[['KubeAPICPUCoreUsage']].to_markdown())

        kubeapi_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"openshift-kube-apiserver|openshift-etcd"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        kubeapi_cpu_trend_df = MetricRangeDataFrame(kubeapi_cpu_trend)
        kubeapi_cpu_trend_df["value"]=kubeapi_cpu_trend_df["value"].astype(float)
        kubeapi_cpu_trend_df.index= pandas.to_datetime(kubeapi_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        kubeapi_cpu_trend_df.rename(columns={"value": "KubeAPICPUCoreUsage"}, inplace = True)
        kubeapi_cpu_trend_df.plot(title="Kube API Server CPU Core usage",figsize=(30, 15))
        plt.savefig('../../output/kubeapi-cpu-usage.png')
        saveCSV(kubeapi_cpu_trend_df,"kubeapi-cpu-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu for Kube API Server: ",e) 
        print(Style.RESET_ALL)   
    print("=============================================")
   
    status=True
    return status  

def ACMCPUUsage(pc,startTime, endTime, step):

    print("Total ACM CPU Core usage")

    try:
        acm_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"})')

        acm_cpu_df = MetricSnapshotDataFrame(acm_cpu)
        acm_cpu_df["value"]=acm_cpu_df["value"].astype(float)
        acm_cpu_df.rename(columns={"value": "ACMCPUCoreUsage"}, inplace = True)
        print(acm_cpu_df[['ACMCPUCoreUsage']].to_markdown())

        acm_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_cpu_trend_df = MetricRangeDataFrame(acm_cpu_trend)
        acm_cpu_trend_df["value"]=acm_cpu_trend_df["value"].astype(float)
        acm_cpu_trend_df.index= pandas.to_datetime(acm_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        acm_cpu_trend_df.rename(columns={"value": "ACMCPUCoreUsage"}, inplace = True)
        acm_cpu_trend_df.plot(title="ACM CPU Core usage",figsize=(30, 15))
        plt.savefig('../../output/acm-cpu-usage.png')
        saveCSV(acm_cpu_trend_df,"acm-cpu-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu for ACM: ",e)  
        print(Style.RESET_ALL)  
    print("=============================================")
   
    status=True
    return status

def ACMDetailCPUUsage(pc,startTime, endTime, step):

    print("Detailed ACM CPU Core usage")

    try:
        acm_detail_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"}) by (namespace)')

        acm_detail_cpu_df = MetricSnapshotDataFrame(acm_detail_cpu)
        acm_detail_cpu_df["value"]=acm_detail_cpu_df["value"].astype(float)
        acm_detail_cpu_df.rename(columns={"value": "CPUCoreUsage"}, inplace = True)
        print(acm_detail_cpu_df[['namespace','CPUCoreUsage']].to_markdown())

        acm_detail_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"}) by (namespace)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_detail_cpu_trend_df = MetricRangeDataFrame(acm_detail_cpu_trend)
        acm_detail_cpu_trend_df["value"]=acm_detail_cpu_trend_df["value"].astype(float)
        acm_detail_cpu_trend_df.index= pandas.to_datetime(acm_detail_cpu_trend_df.index, unit="s")
        acm_detail_cpu_trend_df =  acm_detail_cpu_trend_df.pivot( columns='namespace',values='value')
        acm_detail_cpu_trend_df.rename(columns={"value": "CPUCoreUsage"}, inplace = True)
        acm_detail_cpu_trend_df.plot(title="ACM Detailed CPU Core usage",figsize=(30, 15))
        plt.savefig('../../output/breakdown/acm-detail-cpu-usage.png')
        saveCSV(acm_detail_cpu_trend_df,"acm-detail-cpu-usage")
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu details for ACM: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status
def OtherCPUUsage(pc,startTime, endTime, step):

    print("Total CPU Core usage - Other")

    try:
        acm_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace!~"multicluster-engine|open-cluster-.+|openshift-kube-apiserver|openshift-etcd"})')

        acm_cpu_df = MetricSnapshotDataFrame(acm_cpu)
        acm_cpu_df["value"]=acm_cpu_df["value"].astype(float)
        acm_cpu_df.rename(columns={"value": "OtherCPUCoreUsage"}, inplace = True)
        print(acm_cpu_df[['OtherCPUCoreUsage']].to_markdown())

        acm_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace!~"multicluster-engine|open-cluster-.+|openshift-kube-apiserver|openshift-etcd"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_cpu_trend_df = MetricRangeDataFrame(acm_cpu_trend)
        acm_cpu_trend_df["value"]=acm_cpu_trend_df["value"].astype(float)
        acm_cpu_trend_df.index= pandas.to_datetime(acm_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        acm_cpu_trend_df.rename(columns={"value": "OtherCPUCoreUsage"}, inplace = True)
        acm_cpu_trend_df.plot(title="Other CPU Core usage",figsize=(30, 15))
        plt.savefig('../../output/other-cpu-usage.png')
        saveCSV(acm_cpu_trend_df,"other-cpu-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu for Others: ",e)  
        print(Style.RESET_ALL)  
    print("=============================================")
   
    status=True
    return status
