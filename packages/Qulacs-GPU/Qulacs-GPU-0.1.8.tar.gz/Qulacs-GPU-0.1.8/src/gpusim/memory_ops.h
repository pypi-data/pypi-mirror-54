#ifndef _MEMORY_OPS_CU_H_
#define _MEMORY_OPS_CU_H_

#include "util_export.h"
#include "util_type.h"

DllExport void* allocate_quantum_state_host(ITYPE dim);
DllExport void initialize_quantum_state_host(void* state, ITYPE dim);
DllExport void release_quantum_state_host(void* state);
DllExport void initialize_Haar_random_state_host(void *state, ITYPE dim);
DllExport void initialize_Haar_random_state_with_seed_host(void *state, ITYPE dim, UINT seed);

// using cuda_stream to launch kernel simultaneously
DllExport void initialize_quantum_state_host(void* state, ITYPE dim, void* stream);
DllExport void initialize_Haar_random_state_host(void *state, ITYPE dim, void* stream);
DllExport void initialize_Haar_random_state_with_seed_host(void *state, ITYPE dim, UINT seed, void* stream);
DllExport void* allocate_cuda_stream_host(unsigned int max_cuda_stream);
DllExport void release_cuda_stream_host(void* cuda_stream, unsigned int max_cuda_stream);

#endif // _MEMORY_OPS_CU_H_

