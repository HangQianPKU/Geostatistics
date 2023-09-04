#!/bin/bash
#SBATCH --job-name=FM-6-16
#SBATCH --output=/lustre/home/hangqian/projects/FixedMulti/FM-6-16/output.log
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --time=1-00:00:00

# 加载 Anaconda 模块
#source ~/miniconda3/condabin/conda

# 激活虚拟环境
#conda activate pymc_env5

start_time=$(date +%s)

# 调用 Python 脚本并传递参数
python /lustre/home/hangqian/projects/FixedMulti/FM-6-16/FixedMulti.py

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
