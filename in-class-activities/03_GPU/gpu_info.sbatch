#!/bin/bash
#SBATCH --job-name=gpu      # job name
#SBATCH --output=info.out   # output log file
#SBATCH --error=info.err    # error file
#SBATCH --partition=gpu     # GPU partition
#SBATCH --time=00:05:00     # 5 minutes of wall time
#SBATCH --nodes=1           # 1 GPU node
#SBATCH --ntasks=1          # 1 CPU core to drive GPU
#SBATCH --gres=gpu:1        # Request 1 GPU
#SBATCH --account=macs30123

module load python/anaconda-2022.05 cuda/11.7 gcc/10.2.0

python print_gpu_info-cuda.py
# python print_gpu_info-opencl.py