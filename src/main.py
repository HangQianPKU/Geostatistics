#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import os
import math
import numpy as np
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel
from scipy.stats import poisson
from patsy import dmatrices
import statsmodels.graphics.tsaplots as tsa
from matplotlib import pyplot as plt
from statsmodels.tools.numdiff import approx_hess1, approx_hess2, approx_hess3
import pandas as pd
import pymc as pm
import sys
import arviz as az
import pickle

# 创建参数解析器
parser = argparse.ArgumentParser(description="Your Script Description")

# 添加需要的命令行参数
parser.add_argument('--k', type=int, help="An int parameter,the number of switchpoints")
parser.add_argument('--mantissa', type=float, help="A floating-point parameter, the mantissa of draws of MCMC,including tunes")
parser.add_argument('--exponent', type=int, help="An int parameter,the exponent of draws of MCMC, including tunes")
parser.add_argument('--job_name', type=str, help="A str parameter,the name of job(and name of PATH to the output data)")

# 解析命令行参数
args = parser.parse_args()

# 获取命令行传递的参数值
k = args.k
mantissa = args.mantissa
exponent = args.exponent
job_name = args.job_name

draws = int(mantissa * 10**exponent)
tune = draws//2

# 构建完整的输出目录路径
output_directory = os.path.join("../data", job_name)

# 确保输出目录存在，如果不存在则创建它
os.makedirs(output_directory, exist_ok=True)

# 将所有输出重定向到指定目录下的文件
sys.stdout = open(os.path.join(output_directory, "all_output.txt"), 'w')

# 加载数据,绘制直方图
df = pd.read_csv('/lustre/home/hangqian/projects/data/zircons/Roberts_Spencer_2015.csv')
years = df["U-Pb (Ma)"]
data = plt.hist(years, bins=200)
zircons_data = data[0]
ages = data[1][1:]


data = plt.hist(years, bins=200)
plt.xlabel('Ages (Ma)')
plt.ylabel('Frequency')
plt.title('Histogram of Zircon Ages')
plt.grid(True)

# 保存直方图到指定目录
plt.savefig(os.path.join(output_directory, 'histogram.png'))

# 绘制散点图
plt.plot(ages, zircons_data, "o", markersize=3, alpha=1)
plt.ylabel("Zircons count")
plt.xlabel("Ages")

# 保存散点图到指定目录
plt.savefig(os.path.join(output_directory, 'scatter_plot.png'))

#定义变换方法
tr =pm.distributions.transforms

Order = tr.Ordered()

#使用PyMC建立模型
with pm.Model() as model:
    rates = pm.Exponential("rates", 1.0, shape=k + 1)
    switchpoints = pm.Uniform("switchpoints", lower=0, upper=max(ages), shape=k, transform=Order, initval=np.linspace(0+5, max(ages)-5, k))
    rate = rates[0]
    for i in range(k):
        rate = pm.math.switch(switchpoints[i] >= ages, rate, rates[i + 1])
    disasters = pm.Poisson("counts", rate, observed=zircons_data)
    trace = pm.sample(tune=tune, draws=draws, cores=4)
# 输出 trace 绘图到文件
#az.plot_trace(trace)
#plt.savefig('trace_plot.png')

# 构建 trace 文件的完整路径
trace_output_path = os.path.join(output_directory, "trace")

# 将采样结果 trace 序列化后输出到指定路径
with open(trace_output_path, 'wb') as f:
    pickle.dump(trace, f)


# 将trace文件反序列化后加载：
#with open('trace', 'rb') as f:
#    loaded_data = pickle.load(f)

# 输出 summary 结果到文件
#summary = pm.summary(trace)
#with open('summary.txt', 'w') as f:
#    f.write(str(summary))



#pm.save_trace(trace, directory='path_to_save', overwrite=True, save_on_disk=True, format='csv')
#关闭重定向，恢复标准输出
sys.stdout.close()
sys.stdout = sys.__stdout__

