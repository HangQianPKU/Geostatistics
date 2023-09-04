#!/bin/bash
#SBATCH --job-name=9points
#SBATCH --output=/lustre/home/hangqian/projects/FixedMulti/9changepoints/output.log
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --time=1-00:00:00

# 加载 Anaconda 模块
source ~/miniconda3/condabin/conda

# 激活虚拟环境
conda activate pymc_env5

# 调用 Python 脚本并传递参数
python /lustre/home/hangqian/projects/FixedMulti/9changepoints/FixedMulti.py

# 关闭虚拟环境
conda deactivate
