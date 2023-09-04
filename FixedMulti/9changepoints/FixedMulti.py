#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

# 将所有输出重定向到文件
sys.stdout = open('all_output.txt', 'w')

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

# 保存直方图到本地
plt.savefig('histogram.png')

# 绘制散点图
plt.plot(ages, zircons_data, "o", markersize=3, alpha=1)
plt.ylabel("Zircons count")
plt.xlabel("Ages")

# 保存散点图到本地
plt.savefig('scatter_plot.png')

#定义变换方法
tr =pm.distributions.transforms

Order = tr.Ordered()

#使用PyMC建立模型
with pm.Model() as model:
    k = 9
    rates = pm.Exponential("rates", 1.0, shape=k + 1)
    switchpoints = pm.Uniform("switchpoints", lower=0, upper=max(ages), shape=k, transform=Order, initval=np.linspace(0, max(ages), k))
    rate = rates[0]
    for i in range(k):
        rate = pm.math.switch(switchpoints[i] >= ages, rate, rates[i + 1])
    disasters = pm.Poisson("counts", rate, observed=zircons_data)
    trace = pm.sample(tune=1000, cores=1)
# 输出 trace 绘图到文件
az.plot_trace(trace)
plt.savefig('trace_plot.png')

# 输出 summary 结果到文件
summary = pm.summary(trace)
with open('summary.txt', 'w') as f:
    f.write(str(summary))

# 关闭重定向，恢复标准输出
sys.stdout.close()
sys.stdout = sys.__stdout__

