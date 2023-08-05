#ifndef _STAT_OPS_CU_H_
#define _STAT_OPS_CU_H_

#include "util_type.h"
#include "util_export.h"

DllExport double state_norm_squared_cublas_host(void *state, ITYPE dim);
DllExport double state_norm_squared_host(void *state, ITYPE dim);
DllExport double measurement_distribution_entropy_host(void* state, ITYPE dim);
DllExport void state_add_host(void *state_added, void *state, ITYPE dim);
DllExport void state_multiply_host(CPPCTYPE coef, void *state, ITYPE dim);
DllExport CPPCTYPE inner_product_host(const void *bra_state, const void *ket_state, ITYPE dim);
DllExport double expectation_value_single_qubit_Pauli_operator_host(unsigned int operator_index, unsigned int target_qubit_index, void* state, ITYPE dim);
DllExport void multi_Z_gate_host(int* gates, void* state, ITYPE dim, int n_qubits);
DllExport double multipauli_get_expectation_value_host(unsigned int* gates, void* state, ITYPE dim, int n_qubits);
DllExport double M0_prob_host(UINT target_qubit_index, void* state, ITYPE dim);
DllExport double M1_prob_host(UINT target_qubit_index, void* state, ITYPE dim);
DllExport double marginal_prob_host(UINT* sorted_target_qubit_index_list, UINT* measured_value_list, UINT target_qubit_index_count, void* state, ITYPE dim);
DllExport double expectation_value_multi_qubit_Pauli_operator_XZ_mask_host(ITYPE bit_flip_mask, ITYPE phase_flip_mask, UINT global_phase_90rot_count,UINT pivot_qubit_index, void* state, ITYPE dim);
DllExport double expectation_value_multi_qubit_Pauli_operator_Z_mask_host(ITYPE phase_flip_mask, void* state, ITYPE dim);
DllExport double expectation_value_multi_qubit_Pauli_operator_partial_list_host(const UINT* target_qubit_index_list, const UINT* Pauli_operator_type_list, UINT target_qubit_index_count, void* state, ITYPE dim);
DllExport double expectation_value_multi_qubit_Pauli_operator_whole_list_host(const UINT* Pauli_operator_type_list, UINT qubit_count, void* state, ITYPE dim);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_XZ_mask_host(ITYPE bit_flip_mask, ITYPE phase_flip_mask, UINT global_phase_90rot_count, UINT pivot_qubit_index, void* state_bra, void* state_ket, ITYPE dim);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_Z_mask_host(ITYPE phase_flip_mask, void* state_bra, void* state_ket, ITYPE dim);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_partial_list_host(const UINT* target_qubit_index_list, const UINT* Pauli_operator_type_list, UINT target_qubit_index_count, void* state_bra, void* state_ket, ITYPE dim);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_whole_list_host(const UINT* Pauli_operator_type_list, UINT qubit_count, void* state_bra, void* state_ket, ITYPE dim);

// using cuda_stream to launch kernel simultaneously
DllExport double state_norm_squared_host(void *state, ITYPE dim, void* stream);
DllExport double measurement_distribution_entropy_host(void* state, ITYPE dim, void* stream);
DllExport void state_add_host(void *state_added, void *state, ITYPE dim, void* stream);
DllExport void state_multiply_host(CPPCTYPE coef, void *state, ITYPE dim, void* stream);
DllExport CPPCTYPE inner_product_host(const void *bra_state, const void *ket_state, ITYPE dim, void* stream);
DllExport double expectation_value_single_qubit_Pauli_operator_host(unsigned int operator_index, unsigned int target_qubit_index, void *state, ITYPE dim, void* stream);
DllExport void multi_Z_gate_host(int* gates, void *state, ITYPE dim, int n_qubits, void* stream);
DllExport double multipauli_get_expectation_value_host(unsigned int* gates, void *state, ITYPE dim, int n_qubits, void* stream);
DllExport double M0_prob_host(UINT target_qubit_index, void* state, ITYPE dim, void* stream);
DllExport double M1_prob_host(UINT target_qubit_index, void* state, ITYPE dim, void* stream);
DllExport double marginal_prob_host(UINT* sorted_target_qubit_index_list, UINT* measured_value_list, UINT target_qubit_index_count, void* state, ITYPE dim, void* stream);
DllExport double expectation_value_multi_qubit_Pauli_operator_XZ_mask_host(ITYPE bit_flip_mask, ITYPE phase_flip_mask, UINT global_phase_90rot_count, UINT pivot_qubit_index, void* state, ITYPE dim, void* stream);
DllExport double expectation_value_multi_qubit_Pauli_operator_Z_mask_host(ITYPE phase_flip_mask, void* state, ITYPE dim, void* stream);
DllExport double expectation_value_multi_qubit_Pauli_operator_partial_list_host(const UINT* target_qubit_index_list, const UINT* Pauli_operator_type_list, UINT target_qubit_index_count, void* state, ITYPE dim, void* stream);
DllExport double expectation_value_multi_qubit_Pauli_operator_whole_list_host(const UINT* Pauli_operator_type_list, UINT qubit_count, void* state, ITYPE dim, void* stream);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_XZ_mask_host(ITYPE bit_flip_mask, ITYPE phase_flip_mask, UINT global_phase_90rot_count, UINT pivot_qubit_index, void* state_bra, void* state_ket, ITYPE dim, void* stream);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_Z_mask_host(ITYPE phase_flip_mask, void* state_bra, void* state_ket, ITYPE dim, void* stream);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_partial_list_host(const UINT* target_qubit_index_list, const UINT* Pauli_operator_type_list, UINT target_qubit_index_count, void* state_bra, void* state_ket, ITYPE dim, void* stream);
DllExport CPPCTYPE transition_amplitude_multi_qubit_Pauli_operator_whole_list_host(const UINT* Pauli_operator_type_list, UINT qubit_count, void* state_bra, void* state_ket, ITYPE dim, void* stream);

#endif // _STAT_OPS_CU_H_
