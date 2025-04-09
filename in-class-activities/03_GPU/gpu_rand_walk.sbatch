#!/bin/bash
#SBATCH --job-name=gpu      # job name
#SBATCH --output=gpu.out    # output log file
#SBATCH --error=gpu.err     # error file
#SBATCH --partition=gpu     # GPU partition
#SBATCH --time=00:05:00     # 5 minutes of wall time
#SBATCH --nodes=1           # 1 GPU node
#SBATCH --ntasks=1          # 1 CPU core to drive GPU
#SBATCH --gres=gpu:1        # Request 1 GPU
#SBATCH --account=macs30123

module load python/anaconda-2022.05 cuda/11.7 gcc/10.2.0

python gpu_rand_walk-cuda.py
# python gpu_rand_walk-opencl.py