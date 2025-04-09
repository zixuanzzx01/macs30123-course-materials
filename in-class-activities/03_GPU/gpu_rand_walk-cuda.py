import matplotlib.pyplot as plt
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
from pycuda import curandom
import time

def sim_rand_walks(n_runs, n_steps):
    # Set up context and queue
    t0 = time.time()

    # Generate random numbers using CURAND for normal distribution
    rand_gen = curandom.XORWOWRandomNumberGenerator()
    data_gpu = rand_gen.gen_normal((n_runs * n_steps), dtype=np.float32)

    # Establish boundaries for each simulated walk (i.e. start and end)
    # Necessary so that we perform scan only within rand walks and not between
    seg_boundaries = [1] + [0] * (n_steps - 1)
    seg_boundaries = np.array(seg_boundaries, dtype=np.int32)
    seg_ids = np.tile(seg_boundaries, int(n_runs))


    # CUDA Scan Kernel (simplified version of segmented scan)
    kernel_code = """
    __global__ void segmented_scan_kernel(float *data, uint *seg_ids,
                                          float *output, uint n_runs, uint n_steps)
    {
        uint n = n_runs * n_steps;
        extern __shared__ char shared[];
        float *s_data = (float *)shared;
        int *s_seg_ids = (int *)(shared + blockDim.x * sizeof(float));
        int tid = threadIdx.x;
        int gid = blockIdx.x * blockDim.x + threadIdx.x;

        if (gid < n) {
            s_data[tid] = data[gid];
            s_seg_ids[tid] = seg_ids[gid];
        } else {
            s_data[tid] = 0.0f;
            s_seg_ids[tid] = 0;
        }
        __syncthreads();

        if (gid < n) {
            float sum = 0.0f;
            int j = tid;
            while (j >= 0) {
                sum += s_data[j];
                if (s_seg_ids[j] == 1) {
                    break;
                }
                j--;
            }
            output[gid] = sum + n_steps;
        }
    }
    """

    # # Compile and get the kernel function
    mod = SourceModule(kernel_code)
    segmented_scan = mod.get_function("segmented_scan_kernel")

    # Allocate GPU memory
    seg_ids_gpu = cuda.mem_alloc(seg_ids.nbytes)
    output_gpu = cuda.mem_alloc(data_gpu.get().nbytes)

    # Transfer data to GPU
    cuda.memcpy_htod(seg_ids_gpu, seg_ids)

    # Set block and grid sizes
    block_size = 512 # Adjust based on needs, here n=6 < 32
    grid_size = (n_runs*n_steps + block_size - 1) // block_size
    # Shared memory: block_size floats + block_size ints
    shared_mem_size = (block_size * np.dtype(np.float32).itemsize)  \
                      + (block_size * np.dtype(np.uint32).itemsize)

    # Launch the kernel
    segmented_scan(
        data_gpu, seg_ids_gpu, output_gpu, np.uint32(n_runs), np.uint32(n_steps),
        block=(block_size, 1, 1),
        grid=(grid_size, 1),
        shared=shared_mem_size
    )

    # Get the result back on the CPU
    output = np.empty_like(data_gpu.get())
    cuda.memcpy_dtoh(output, output_gpu)
    r_walks_all = output.reshape(n_runs, n_steps).transpose()

    # Compute average and standard deviation of the final positions
    average_finish = np.mean(r_walks_all[-1])
    std_finish = np.std(r_walks_all[-1])
    final_time = time.time()
    time_elapsed = final_time - t0

    print("Simulated %d Random Walks in: %f seconds"
                % (n_runs, time_elapsed))
    print("Average final position: %f, Standard Deviation: %f"
                % (average_finish, std_finish))

    # plt.plot(r_walks_all)
    # plt.savefig("r_walk_nruns%d_gpu.png" % n_runs)

if __name__ == "__main__":
    sim_rand_walks(n_runs=10000, n_steps=100)


