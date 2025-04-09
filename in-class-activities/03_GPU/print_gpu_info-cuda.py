import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np

def print_device_info():

    # Platform-level info
    print('\n' + '=' * 60 + '\nPlatform Info')
    print('' + '=' * 60 + '')
    print(f'CUDA Driver Version: {cuda.get_driver_version() // 1000}.{(cuda.get_driver_version() % 1000) // 10}')
    runtime_version = cuda.get_version()
    print(f'CUDA Runtime Version: {runtime_version[0]}.{runtime_version[1]}')

    # Get the number of CUDA devices available
    num_devices = cuda.Device.count()
    
    if num_devices == 0:
        print("No CUDA devices found.")
        return

    print('\n' + '=' * 60 + '\nCUDA Devices')
    
    for i in range(num_devices):
        device = cuda.Device(i)
        
        print('=' * 60)
        print(f'Device {i} - Name: {device.name()}')
        print(f'Device {i} - Compute Capability: {device.compute_capability()}')
        print(f'Device {i} - Total Memory: {device.total_memory() / 1024**2:.0f} MB')
        print(f'Device {i} - Multiprocessors: {device.get_attribute(cuda.device_attribute.MULTIPROCESSOR_COUNT)}')
        print(f'Device {i} - Clock Rate: {device.clock_rate / 1000} MHz')

        # Replace MAX_THREADS_DIM with separate attributes for each dimension
        max_threads_dim_x = device.get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_X)
        max_threads_dim_y = device.get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_Y)
        max_threads_dim_z = device.get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_Z)
        print(f'Device {i} - Max Threads per Block: X={max_threads_dim_x}, Y={max_threads_dim_y}, Z={max_threads_dim_z}')

        # Access the max grid dimensions directly via get_attribute
        max_grid_dim_x = device.get_attribute(cuda.device_attribute.MAX_GRID_DIM_X)
        max_grid_dim_y = device.get_attribute(cuda.device_attribute.MAX_GRID_DIM_Y)
        max_grid_dim_z = device.get_attribute(cuda.device_attribute.MAX_GRID_DIM_Z)
        print(f'Device {i} - Max Grid Dimensions: X={max_grid_dim_x}, Y={max_grid_dim_y}, Z={max_grid_dim_z}')

        print(f'Device {i} - Global Memory Size: {device.total_memory() / 1024**3:.2f} GB')
        print(f'Device {i} - Warp Size: {device.get_attribute(cuda.device_attribute.WARP_SIZE)}')
        print(f'Device {i} - Max Register per Block: {device.get_attribute(cuda.device_attribute.MAX_REGISTERS_PER_BLOCK)}')
        print(f'Device {i} - Max Shared Memory per Block: {device.get_attribute(cuda.device_attribute.MAX_SHARED_MEMORY_PER_BLOCK) / 1024.0:.2f} KB')
        print('\n')

if __name__ == '__main__':
    print_device_info()

