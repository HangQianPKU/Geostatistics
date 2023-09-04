#!/bin/bash

#SBATCH --job-name=FM-6-46
#SBATCH --output=FM-6-46.output
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --time=3-00:00:00

#定义参数
k=6
mantissa=4
exponent=6

#构建任务名称
job_name="FM-$k-$mantissa-$exponent"


# 加载 Anaconda 模块
#source ~/miniconda3/condabin/conda

# 激活虚拟环境
#conda activate pymc_env5

start_time=$(date +%s)

# 调用 Python 脚本并传递参数
python /lustre/home/hangqian/projects/src/main.py --k $k --mantissa $mantissa --exponent $exponent --job_name $job_name

end_time=$(date +%s)
runtime=$((end_time - start_time))

# 输出程序运行信息到输出文件
echo "-----------------------------"
echo "Program Start Time: $(date -d @$start_time)"
echo "Program End Time: $(date -d @$end_time)"
echo "Program Runtime: $runtime seconds"
echo "-----------------------------"


# 关闭虚拟环境
# conda deactivate
