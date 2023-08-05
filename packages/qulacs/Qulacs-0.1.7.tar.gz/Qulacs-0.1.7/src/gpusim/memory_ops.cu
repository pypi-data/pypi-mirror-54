#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <cuda_runtime.h>
//#include <cuda.h>
#include <curand.h>
#include <curand_kernel.h>

#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <complex>
#include <assert.h>
#include <algorithm>
#include <cuComplex.h>
#include "util_type.h"
#include "util_type_internal.h"
#include "util.cuh"
#include "memory_ops.h"
#include "memory_ops_device_functions.h"
#include "stat_ops.h"
#include "update_ops_cuda.h"

__host__ void* allocate_cuda_stream_host(unsigned int max_cuda_stream) {
	cudaStream_t* stream = (cudaStream_t*)malloc(max_cuda_stream * sizeof(cudaStream_t));
	for (unsigned int i = 0; i < max_cuda_stream; ++i) cudaStreamCreate(&stream[i]);
	void* cuda_stream = reinterpret_cast<void*>(stream);
	return cuda_stream;
}

__host__ void release_cuda_stream_host(void* cuda_stream, unsigned int max_cuda_stream) {
	cudaStream_t* stream = reinterpret_cast<cudaStream_t*>(cuda_stream);
	for (unsigned int i = 0; i < max_cuda_stream; ++i) cudaStreamDestroy(stream[i]);
	free(stream);
}

__global__ void init_qstate(GTYPE* state_gpu, ITYPE dim){
	ITYPE idx = blockIdx.x * blockDim.x + threadIdx.x;
	if (idx < dim) {
		state_gpu[idx] = make_cuDoubleComplex(0.0, 0.0);
	}
	if (idx == 0) state_gpu[idx] = make_cuDoubleComplex(1.0, 0.0);
}

// void* (GTYPE*)
__host__ void* allocate_quantum_state_host(ITYPE dim){
	GTYPE *state_gpu;
	checkCudaErrors(cudaSetDevice(0));
	checkCudaErrors(cudaMalloc((void**)&state_gpu, dim * sizeof(GTYPE)));
	void* psi_gpu = reinterpret_cast<void*>(state_gpu);
    return psi_gpu;
}

__host__ void initialize_quantum_state_host(void* state, ITYPE dim, void* stream) {
	GTYPE* state_gpu = reinterpret_cast<GTYPE*>(state);
	cudaStream_t* cuda_stream = reinterpret_cast<cudaStream_t*>(stream);
	cudaError cudaStatus;
	unsigned int block = dim <= 1024 ? dim : 1024;
	unsigned int grid = dim / block;
	init_qstate << <grid, block, 0, *cuda_stream >> > (state_gpu, dim);

	checkCudaErrors(cudaStreamSynchronize(*cuda_stream), __FILE__, __LINE__);
	cudaStatus = cudaGetLastError();
	checkCudaErrors(cudaStatus, __FILE__, __LINE__);
	state = reinterpret_cast<void*>(state_gpu);
	stream = reinterpret_cast<void*>(cuda_stream);
}

__host__ void initialize_quantum_state_host(void* state, ITYPE dim) {
	cudaStream_t cuda_stream = (cudaStream_t)0;
	initialize_quantum_state_host(state, dim, &cuda_stream);
}

__host__ void release_quantum_state_host(void* state){
	GTYPE* state_gpu = reinterpret_cast<GTYPE*>(state);
	checkCudaErrors(cudaFree(state_gpu), __FILE__, __LINE__);
}

__host__ void initialize_Haar_random_state_host(void *state, ITYPE dim, void* stream) {
	initialize_Haar_random_state_with_seed_host(state, dim, (unsigned)time(NULL), stream);
}

__host__ void initialize_Haar_random_state_host(void *state, ITYPE dim) {
	initialize_Haar_random_state_with_seed_host(state, dim, (unsigned)time(NULL));
}

__global__ void init_rnd(curandState *const rnd_state, const unsigned int seed)
{
    unsigned int tid = blockIdx.x * blockDim.x + threadIdx.x;
    curand_init(seed, tid, 0, &rnd_state[tid]);
}

/*
__global__ void rand_normal_mtgp32(curandState* rnd_state, GTYPE* state, ITYPE dim){
	ITYPE idx = blockIdx.x * blockDim.x + threadIdx.x;
    double2 rnd;
    curandStateMtgp32 localState = rnd_state[idx];
	if (idx < dim) {
        rnd = curand_normal2_double(&localState);
        state[idx] = make_cuDoubleComplex(rnd.x, rnd.y);
        rnd_state[idx] = localState;
    }
}
*/

__global__ void rand_normal_xorwow(curandState* rnd_state, GTYPE* state, ITYPE dim){
	ITYPE idx = blockIdx.x * blockDim.x + threadIdx.x;
    // double2 rnd;
    double tmp1, tmp2;
    double real, imag;
    curandStateXORWOW localState = rnd_state[idx];
	if (idx < dim) {
        // rnd = curand_normal2_double(&localState);
        tmp1 = curand_uniform_double(&localState);
        tmp2 = curand_uniform_double(&localState);
	    real = sqrt(-1.0*log(tmp1)) * sinpi(2.0*tmp2);
        tmp1 = curand_uniform_double(&localState);
        tmp2 = curand_uniform_double(&localState);
	    imag = sqrt(-1.0*log(tmp1)) * sinpi(2.0*tmp2);
        state[idx] = make_cuDoubleComplex(real, imag);
        rnd_state[idx] = localState;
    }
}

__host__ void initialize_Haar_random_state_with_seed_host(void *state, ITYPE dim, UINT seed, void* stream) {
	GTYPE* state_gpu = reinterpret_cast<GTYPE*>(state);
	cudaStream_t* cuda_stream = reinterpret_cast<cudaStream_t*>(stream);
	//const ITYPE ignore_first = 40;
	double norm = 0.;

	curandState* rnd_state;
	checkCudaErrors(cudaMalloc((void**)&rnd_state, dim * sizeof(curandState)), __FILE__, __LINE__);

	// CURAND_RNG_PSEUDO_XORWOW
	// CURAND_RNG_PSEUDO_MT19937 offset cannot be used and need sm_35 or higher.

	unsigned int block = dim <= 512 ? dim : 512;
	unsigned int grid = min((int)(dim / block), 512);

	init_rnd << < grid, block, 0, *cuda_stream >> > (rnd_state, seed);
	checkCudaErrors(cudaGetLastError(), __FILE__, __LINE__);

	rand_normal_xorwow << < grid, block, 0, *cuda_stream >> > (rnd_state, state_gpu, dim);
	checkCudaErrors(cudaGetLastError(), __FILE__, __LINE__);

	checkCudaErrors(cudaStreamSynchronize(*cuda_stream), __FILE__, __LINE__);
	checkCudaErrors(cudaFree(rnd_state), __FILE__, __LINE__);
	state = reinterpret_cast<void*>(state_gpu);

	norm = state_norm_host(state, dim, cuda_stream);
	normalize_host(norm, state, dim, cuda_stream);
}

__host__ void initialize_Haar_random_state_with_seed_host(void *state, ITYPE dim, UINT seed) {
	cudaStream_t cuda_stream = (cudaStream_t)0;
	initialize_Haar_random_state_with_seed_host(state, dim, seed, &cuda_stream);
}
