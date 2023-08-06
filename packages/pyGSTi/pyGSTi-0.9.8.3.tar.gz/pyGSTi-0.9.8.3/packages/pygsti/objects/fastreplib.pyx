# encoding: utf-8
# cython: profile=False
# cython: linetrace=False
# filename: fastactonlib.pyx

#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************


import sys
import time as pytime
import numpy as np
from libc.stdlib cimport malloc, free
from libc.math cimport log10, sqrt, log
from libc cimport time
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.algorithm cimport sort as stdsort
from libcpp.unordered_map cimport unordered_map
from cython.operator cimport dereference as deref, preincrement as inc
cimport numpy as np
cimport cython

import itertools as _itertools
from ..tools import mpitools as _mpit
from ..tools import slicetools as _slct
from ..tools import optools as _gt
from scipy.sparse.linalg import LinearOperator


#Use 64-bit integers
ctypedef long long INT
ctypedef unsigned long long UINT

cdef extern from "fastreps.h" namespace "CReps":

    # Density Matrix (DM) propagation classes
    cdef cppclass DMStateCRep:
        DMStateCRep() except +
        DMStateCRep(INT) except +
        DMStateCRep(double*,INT,bool) except +
        void copy_from(DMStateCRep*)
        INT _dim
        double* _dataptr

    cdef cppclass DMEffectCRep:
        DMEffectCRep() except +
        DMEffectCRep(INT) except +
        double probability(DMStateCRep* state)
        INT _dim

    cdef cppclass DMEffectCRep_Dense(DMEffectCRep):
        DMEffectCRep_Dense() except +
        DMEffectCRep_Dense(double*,INT) except +
        double probability(DMStateCRep* state)
        INT _dim
        double* _dataptr

    cdef cppclass DMEffectCRep_TensorProd(DMEffectCRep):
        DMEffectCRep_TensorProd() except +
        DMEffectCRep_TensorProd(double*, INT*, INT, INT, INT) except +
        double probability(DMStateCRep* state)
        INT _dim

    cdef cppclass DMEffectCRep_Computational(DMEffectCRep):
        DMEffectCRep_Computational() except +
        DMEffectCRep_Computational(INT, INT, double, INT) except +
        double probability(DMStateCRep* state)
        INT _dim

    cdef cppclass DMEffectCRep_Errgen(DMEffectCRep):
        DMEffectCRep_Errgen() except +
        DMEffectCRep_Errgen(DMOpCRep*, DMEffectCRep*, INT, INT) except +
        double probability(DMStateCRep* state)
        INT _dim

    cdef cppclass DMOpCRep:
        DMOpCRep(INT) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)
        INT _dim

    cdef cppclass DMOpCRep_Dense(DMOpCRep):
        DMOpCRep_Dense(double*,INT) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)
        double* _dataptr
        INT _dim

    cdef cppclass DMOpCRep_Embedded(DMOpCRep):
        DMOpCRep_Embedded(DMOpCRep*, INT*, INT*, INT*, INT*, INT, INT, INT, INT, INT) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)

    cdef cppclass DMOpCRep_Composed(DMOpCRep):
        DMOpCRep_Composed(vector[DMOpCRep*], INT) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)

    cdef cppclass DMOpCRep_Sum(DMOpCRep):
        DMOpCRep_Sum(vector[DMOpCRep*], INT) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)

    cdef cppclass DMOpCRep_Exponentiated(DMOpCRep):
        DMOpCRep_Exponentiated(DMOpCRep*, INT, INT) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)

    cdef cppclass DMOpCRep_Lindblad(DMOpCRep):
        DMOpCRep_Lindblad(DMOpCRep* errgen_rep,
			    double mu, double eta, INT m_star, INT s, INT dim,
			    double* unitarypost_data, INT* unitarypost_indices,
                            INT* unitarypost_indptr, INT unitarypost_nnz) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)

    cdef cppclass DMOpCRep_Sparse(DMOpCRep):
        DMOpCRep_Sparse(double* A_data, INT* A_indices, INT* A_indptr,
                          INT nnz, INT dim) except +
        DMStateCRep* acton(DMStateCRep*, DMStateCRep*)
        DMStateCRep* adjoint_acton(DMStateCRep*, DMStateCRep*)


    # State vector (SV) propagation classes
    cdef cppclass SVStateCRep:
        SVStateCRep() except +
        SVStateCRep(INT) except +
        SVStateCRep(double complex*,INT,bool) except +
        void copy_from(SVStateCRep*)
        INT _dim
        double complex* _dataptr

    cdef cppclass SVEffectCRep:
        SVEffectCRep() except +
        SVEffectCRep(INT) except +
        double probability(SVStateCRep* state)
        double complex amplitude(SVStateCRep* state)
        INT _dim

    cdef cppclass SVEffectCRep_Dense(SVEffectCRep):
        SVEffectCRep_Dense() except +
        SVEffectCRep_Dense(double complex*,INT) except +
        double probability(SVStateCRep* state)
        double complex amplitude(SVStateCRep* state)
        INT _dim
        double complex* _dataptr

    cdef cppclass SVEffectCRep_TensorProd(SVEffectCRep):
        SVEffectCRep_TensorProd() except +
        SVEffectCRep_TensorProd(double complex*, INT*, INT, INT, INT) except +
        double probability(SVStateCRep* state)
        double complex amplitude(SVStateCRep* state)
        INT _dim

    cdef cppclass SVEffectCRep_Computational(SVEffectCRep):
        SVEffectCRep_Computational() except +
        SVEffectCRep_Computational(INT, INT, INT) except +
        double probability(SVStateCRep* state)
        double complex amplitude(SVStateCRep* state)
        INT _dim

    cdef cppclass SVOpCRep:
        SVOpCRep(INT) except +
        SVStateCRep* acton(SVStateCRep*, SVStateCRep*)
        SVStateCRep* adjoint_acton(SVStateCRep*, SVStateCRep*)
        INT _dim

    cdef cppclass SVOpCRep_Dense(SVOpCRep):
        SVOpCRep_Dense(double complex*,INT) except +
        SVStateCRep* acton(SVStateCRep*, SVStateCRep*)
        SVStateCRep* adjoint_acton(SVStateCRep*, SVStateCRep*)
        double complex* _dataptr
        INT _dim

    cdef cppclass SVOpCRep_Embedded(SVOpCRep):
        SVOpCRep_Embedded(SVOpCRep*, INT*, INT*, INT*, INT*, INT, INT, INT, INT, INT) except +
        SVStateCRep* acton(SVStateCRep*, SVStateCRep*)
        SVStateCRep* adjoint_acton(SVStateCRep*, SVStateCRep*)

    cdef cppclass SVOpCRep_Composed(SVOpCRep):
        SVOpCRep_Composed(vector[SVOpCRep*], INT) except +
        SVStateCRep* acton(SVStateCRep*, SVStateCRep*)
        SVStateCRep* adjoint_acton(SVStateCRep*, SVStateCRep*)

    cdef cppclass SVOpCRep_Sum(SVOpCRep):
        SVOpCRep_Sum(vector[SVOpCRep*], INT) except +
        SVStateCRep* acton(SVStateCRep*, SVStateCRep*)
        SVStateCRep* adjoint_acton(SVStateCRep*, SVStateCRep*)

    cdef cppclass SVOpCRep_Exponentiated(SVOpCRep):
        SVOpCRep_Exponentiated(SVOpCRep*, INT, INT) except +
        SVStateCRep* acton(SVStateCRep*, SVStateCRep*)
        SVStateCRep* adjoint_acton(SVStateCRep*, SVStateCRep*)



    # Stabilizer state (SB) propagation classes
    cdef cppclass SBStateCRep:
        SBStateCRep(INT*, INT*, double complex*, INT, INT) except +
        SBStateCRep(INT, INT) except +
        SBStateCRep(double*,INT,bool) except +
        void copy_from(SBStateCRep*)
        INT _n
        INT _namps
        # for DEBUG
        INT* _smatrix
        INT* _pvectors
        INT _zblock_start
        double complex* _amps


    cdef cppclass SBEffectCRep:
        SBEffectCRep(INT*, INT) except +
        double probability(SBStateCRep* state)
        double complex amplitude(SBStateCRep* state)
        INT _n

    cdef cppclass SBOpCRep:
        SBOpCRep(INT) except +
        SBStateCRep* acton(SBStateCRep*, SBStateCRep*)
        SBStateCRep* adjoint_acton(SBStateCRep*, SBStateCRep*)
        INT _n

    cdef cppclass SBOpCRep_Embedded(SBOpCRep):
        SBOpCRep_Embedded(SBOpCRep*, INT, INT*, INT) except +
        SBStateCRep* acton(SBStateCRep*, SBStateCRep*)
        SBStateCRep* adjoint_acton(SBStateCRep*, SBStateCRep*)

    cdef cppclass SBOpCRep_Composed(SBOpCRep):
        SBOpCRep_Composed(vector[SBOpCRep*], INT) except +
        SBStateCRep* acton(SBStateCRep*, SBStateCRep*)
        SBStateCRep* adjoint_acton(SBStateCRep*, SBStateCRep*)

    cdef cppclass SBOpCRep_Sum(SBOpCRep):
        SBOpCRep_Sum(vector[SBOpCRep*], INT) except +
        SBStateCRep* acton(SBStateCRep*, SBStateCRep*)
        SBStateCRep* adjoint_acton(SBStateCRep*, SBStateCRep*)

    cdef cppclass SBOpCRep_Exponentiated(SBOpCRep):
        SBOpCRep_Exponentiated(SBOpCRep*, INT, INT) except +
        SBStateCRep* acton(SBStateCRep*, SBStateCRep*)
        SBStateCRep* adjoint_acton(SBStateCRep*, SBStateCRep*)

    cdef cppclass SBOpCRep_Clifford(SBOpCRep):
        SBOpCRep_Clifford(INT*, INT*, double complex*, INT*, INT*, double complex*, INT) except +
        SBStateCRep* acton(SBStateCRep*, SBStateCRep*)
        SBStateCRep* adjoint_acton(SBStateCRep*, SBStateCRep*)
        #for DEBUG:
        INT *_smatrix
        INT *_svector
        INT *_smatrix_inv
        INT *_svector_inv
        double complex *_unitary
        double complex *_unitary_adj


    #Other classes
    cdef cppclass PolyVarsIndex:
        PolyVarsIndex() except +
        PolyVarsIndex(INT) except +
        bool operator<(PolyVarsIndex i)
        vector[INT] _parts

    cdef cppclass PolyCRep:
        PolyCRep() except +
        PolyCRep(unordered_map[PolyVarsIndex, complex], INT, INT, INT) except +
        PolyCRep mult(PolyCRep&)
        void add_inplace(PolyCRep&)
        void scale(double complex scale)
        vector[INT] int_to_vinds(PolyVarsIndex indx_tup)
        unordered_map[PolyVarsIndex, complex] _coeffs
        INT _max_order
        INT _max_num_vars


    cdef cppclass SVTermCRep:
        SVTermCRep(PolyCRep*, double, double, SVStateCRep*, SVStateCRep*, vector[SVOpCRep*], vector[SVOpCRep*]) except +
        SVTermCRep(PolyCRep*, double, double, SVEffectCRep*, SVEffectCRep*, vector[SVOpCRep*], vector[SVOpCRep*]) except +
        SVTermCRep(PolyCRep*, double, double, vector[SVOpCRep*], vector[SVOpCRep*]) except +
        PolyCRep* _coeff
        double _magnitude
        double _logmagnitude
        SVStateCRep* _pre_state
        SVEffectCRep* _pre_effect
        vector[SVOpCRep*] _pre_ops
        SVStateCRep* _post_state
        SVEffectCRep* _post_effect
        vector[SVOpCRep*] _post_ops

    cdef cppclass SVTermDirectCRep:
        SVTermDirectCRep(double complex, double, double, SVStateCRep*, SVStateCRep*, vector[SVOpCRep*], vector[SVOpCRep*]) except +
        SVTermDirectCRep(double complex, double, double, SVEffectCRep*, SVEffectCRep*, vector[SVOpCRep*], vector[SVOpCRep*]) except +
        SVTermDirectCRep(double complex, double, double, vector[SVOpCRep*], vector[SVOpCRep*]) except +
        double complex _coeff
        double _magnitude
        double _logmagnitude
        SVStateCRep* _pre_state
        SVEffectCRep* _pre_effect
        vector[SVOpCRep*] _pre_ops
        SVStateCRep* _post_state
        SVEffectCRep* _post_effect
        vector[SVOpCRep*] _post_ops

    cdef cppclass SBTermCRep:
        SBTermCRep(PolyCRep*, double, double, SBStateCRep*, SBStateCRep*, vector[SBOpCRep*], vector[SBOpCRep*]) except +
        SBTermCRep(PolyCRep*, double, double, SBEffectCRep*, SBEffectCRep*, vector[SBOpCRep*], vector[SBOpCRep*]) except +
        SBTermCRep(PolyCRep*, double, double, vector[SBOpCRep*], vector[SBOpCRep*]) except +
        PolyCRep* _coeff
        double _magnitude
        double _logmagnitude
        SBStateCRep* _pre_state
        SBEffectCRep* _pre_effect
        vector[SBOpCRep*] _pre_ops
        SBStateCRep* _post_state
        SBEffectCRep* _post_effect
        vector[SBOpCRep*] _post_ops



ctypedef double complex DCOMPLEX
ctypedef DMOpCRep* DMGateCRep_ptr
ctypedef DMStateCRep* DMStateCRep_ptr
ctypedef DMEffectCRep* DMEffectCRep_ptr
ctypedef SVOpCRep* SVGateCRep_ptr
ctypedef SVStateCRep* SVStateCRep_ptr
ctypedef SVEffectCRep* SVEffectCRep_ptr
ctypedef SVTermCRep* SVTermCRep_ptr
ctypedef SVTermDirectCRep* SVTermDirectCRep_ptr
ctypedef SBOpCRep* SBGateCRep_ptr
ctypedef SBStateCRep* SBStateCRep_ptr
ctypedef SBEffectCRep* SBEffectCRep_ptr
ctypedef SBTermCRep* SBTermCRep_ptr
ctypedef PolyCRep* PolyCRep_ptr
ctypedef vector[SVTermCRep_ptr]* vector_SVTermCRep_ptr_ptr
ctypedef vector[SBTermCRep_ptr]* vector_SBTermCRep_ptr_ptr
ctypedef vector[SVTermDirectCRep_ptr]* vector_SVTermDirectCRep_ptr_ptr
ctypedef vector[INT]* vector_INT_ptr

#Create a function pointer type for term-based calc inner loop
ctypedef void (*sv_innerloopfn_ptr)(vector[vector_SVTermCRep_ptr_ptr],
                                    vector[INT]*, vector[PolyCRep*]*, INT)
ctypedef INT (*sv_innerloopfn_direct_ptr)(vector[vector_SVTermDirectCRep_ptr_ptr],
                                           vector[INT]*, vector[DCOMPLEX]*, INT, vector[double]*, double)
ctypedef void (*sb_innerloopfn_ptr)(vector[vector_SBTermCRep_ptr_ptr],
                                    vector[INT]*, vector[PolyCRep*]*, INT)
ctypedef void (*sv_addpathfn_ptr)(vector[PolyCRep*]*, vector[INT]&, INT, vector[vector_SVTermCRep_ptr_ptr]&,
                                  SVStateCRep**, SVStateCRep**, vector[INT]*,
                                  vector[SVStateCRep*]*, vector[SVStateCRep*]*, vector[PolyCRep]*)

ctypedef double (*TD_obj_fn)(double, double, double, double, double, double, double)


#cdef class StateRep:
#    pass

# Density matrix (DM) propagation wrapper classes
cdef class DMStateRep: #(StateRep):
    cdef DMStateCRep* c_state
    cdef np.ndarray data_ref
    #cdef double [:] data_view # alt way to hold a reference

    def __cinit__(self, np.ndarray[double, ndim=1, mode='c'] data):
        #print("PYX state constructed w/dim ",data.shape[0])
        #cdef np.ndarray[double, ndim=1, mode='c'] np_cbuf = np.ascontiguousarray(data, dtype='d') # would allow non-contig arrays
        #cdef double [:] view = data;  self.data_view = view # ALT: holds reference...
        self.data_ref = data # holds reference to data so it doesn't get garbage collected - or could copy=true
        #self.c_state = new DMStateCRep(<double*>np_cbuf.data,<INT>np_cbuf.shape[0],<bool>0)
        self.c_state = new DMStateCRep(<double*>data.data,<INT>data.shape[0],<bool>0)

    def todense(self):
        return self.data_ref

    @property
    def dim(self):
        return self.c_state._dim

    def __dealloc__(self):
        del self.c_state

    def __str__(self):
        return str([self.c_state._dataptr[i] for i in range(self.c_state._dim)])



cdef class DMEffectRep:
    cdef DMEffectCRep* c_effect

    def __cinit__(self):
        pass # no init; could set self.c_effect = NULL? could assert(False)?
    def __dealloc__(self):
        del self.c_effect # check for NULL?
    @property
    def dim(self):
        return self.c_effect._dim

    def probability(self, DMStateRep state not None):
        #unnecessary (just put in signature): cdef DMStateRep st = <DMStateRep?>state
        return self.c_effect.probability(state.c_state)


cdef class DMEffectRep_Dense(DMEffectRep):
    cdef np.ndarray data_ref

    def __cinit__(self, np.ndarray[double, ndim=1, mode='c'] data):
        self.data_ref = data # holds reference to data
        self.c_effect = new DMEffectCRep_Dense(<double*>data.data,
                                               <INT>data.shape[0])

cdef class DMEffectRep_TensorProd(DMEffectRep):
    cdef np.ndarray data_ref1
    cdef np.ndarray data_ref2

    def __cinit__(self, np.ndarray[double, ndim=2, mode='c'] kron_array,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] factor_dims, INT nfactors, INT max_factor_dim, INT dim):
        # cdef INT dim = np.product(factor_dims) -- just send as argument
        self.data_ref1 = kron_array
        self.data_ref2 = factor_dims
        self.c_effect = new DMEffectCRep_TensorProd(<double*>kron_array.data,
                                                    <INT*>factor_dims.data,
                                                    nfactors, max_factor_dim, dim)


cdef class DMEffectRep_Computational(DMEffectRep):

    def __cinit__(self, np.ndarray[np.int64_t, ndim=1, mode='c'] zvals, INT dim):
        # cdef INT dim = 4**zvals.shape[0] -- just send as argument
        cdef INT nfactors = zvals.shape[0]
        cdef double abs_elval = 1/(np.sqrt(2)**nfactors)
        cdef INT base = 1
        cdef INT zvals_int = 0
        for i in range(nfactors):
            zvals_int += base * zvals[i]
            base = base << 1 # *= 2
        self.c_effect = new DMEffectCRep_Computational(nfactors, zvals_int, abs_elval, dim)


cdef class DMEffectRep_Errgen(DMEffectRep):  #TODO!! Need to make SV version
    cdef DMOpRep errgen
    cdef DMEffectRep effect

    def __cinit__(self, DMOpRep errgen_oprep not None, DMEffectRep effect_rep not None, errgen_id):
        cdef INT dim = effect_rep.c_effect._dim
        self.errgen = errgen_oprep
        self.effect = effect_rep
        self.c_effect = new DMEffectCRep_Errgen(errgen_oprep.c_gate,
                                                effect_rep.c_effect,
                                                <INT>errgen_id, dim)

cdef class DMOpRep:
    cdef DMOpCRep* c_gate

    def __cinit__(self):
        pass # self.c_gate = NULL ?

    def __dealloc__(self):
        del self.c_gate

    @property
    def dim(self):
        return self.c_gate._dim

    def acton(self, DMStateRep state not None):
        cdef DMStateRep out_state = DMStateRep(np.empty(self.c_gate._dim, dtype='d'))
        #print("PYX acton called w/dim ", self.c_gate._dim, out_state.c_state._dim)
        # assert(state.c_state._dataptr != out_state.c_state._dataptr) # DEBUG
        self.c_gate.acton(state.c_state, out_state.c_state)
        return out_state

    def adjoint_acton(self, DMStateRep state not None):
        cdef DMStateRep out_state = DMStateRep(np.empty(self.c_gate._dim, dtype='d'))
        #print("PYX acton called w/dim ", self.c_gate._dim, out_state.c_state._dim)
        # assert(state.c_state._dataptr != out_state.c_state._dataptr) # DEBUG
        self.c_gate.adjoint_acton(state.c_state, out_state.c_state)
        return out_state

    def aslinearoperator(self):
        def mv(v):
            if v.ndim == 2 and v.shape[1] == 1: v = v[:,0]
            in_state = DMStateRep(np.ascontiguousarray(v,'d'))
            return self.acton(in_state).todense()
        def rmv(v):
            if v.ndim == 2 and v.shape[1] == 1: v = v[:,0]
            in_state = DMStateRep(np.ascontiguousarray(v,'d'))
            return self.adjoint_acton(in_state).todense()
        dim = self.c_gate._dim
        return LinearOperator((dim,dim), matvec=mv, rmatvec=rmv) # transpose, adjoint, dot, matmat?



cdef class DMOpRep_Dense(DMOpRep):
    cdef np.ndarray data_ref

    def __cinit__(self, np.ndarray[double, ndim=2, mode='c'] data):
        self.data_ref = data
        #print("PYX dense gate constructed w/dim ",data.shape[0])
        self.c_gate = new DMOpCRep_Dense(<double*>data.data,
                                           <INT>data.shape[0])
    def __str__(self):
        s = ""
        cdef DMOpCRep_Dense* my_cgate = <DMOpCRep_Dense*>self.c_gate # b/c we know it's a _Dense gate...
        cdef INT i,j,k
        for i in range(my_cgate._dim):
            k = i*my_cgate._dim
            for j in range(my_cgate._dim):
                s += str(my_cgate._dataptr[k+j]) + " "
            s += "\n"
        return s


cdef class DMOpRep_Embedded(DMOpRep):
    cdef np.ndarray data_ref1
    cdef np.ndarray data_ref2
    cdef np.ndarray data_ref3
    cdef np.ndarray data_ref4
    cdef DMOpRep embedded

    def __cinit__(self, DMOpRep embedded_op,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] numBasisEls,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] actionInds,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] blocksizes,
		  INT embedded_dim, INT nComponentsInActiveBlock,
                  INT iActiveBlock, INT nBlocks, INT dim):

        cdef INT i, j

        # numBasisEls_noop_blankaction is just numBasisEls with actionInds == 1
        cdef np.ndarray[np.int64_t, ndim=1, mode='c'] numBasisEls_noop_blankaction = numBasisEls.copy()
        for i in actionInds:
            numBasisEls_noop_blankaction[i] = 1 # for indexing the identity space

        # multipliers to go from per-label indices to tensor-product-block index
        # e.g. if map(len,basisInds) == [1,4,4] then multipliers == [ 16 4 1 ]
        cdef np.ndarray tmp = np.empty(nComponentsInActiveBlock,np.int64)
        tmp[0] = 1
        for i in range(1,nComponentsInActiveBlock):
            tmp[i] = numBasisEls[nComponentsInActiveBlock-i]
        multipliers = np.array( np.flipud( np.cumprod(tmp) ), np.int64)

        # noop_incrementers[i] specifies how much the overall vector index
        #  is incremented when the i-th "component" digit is advanced
        cdef INT dec = 0
        cdef np.ndarray[np.int64_t, ndim=1, mode='c'] noop_incrementers = np.empty(nComponentsInActiveBlock,np.int64)
        for i in range(nComponentsInActiveBlock-1,-1,-1):
            noop_incrementers[i] = multipliers[i] - dec
            dec += (numBasisEls_noop_blankaction[i]-1)*multipliers[i]

        cdef INT vec_index
        cdef INT offset = 0 #number of basis elements preceding our block's elements
        for i in range(iActiveBlock):
            offset += blocksizes[i]

        # self.baseinds specifies the contribution from the "active
        #  component" digits to the overall vector index.
        cdef np.ndarray[np.int64_t, ndim=1, mode='c'] baseinds = np.empty(embedded_dim,np.int64)
        basisInds_action = [ list(range(numBasisEls[i])) for i in actionInds ]
        for ii,op_b in enumerate(_itertools.product(*basisInds_action)):
            vec_index = offset
            for j,bInd in zip(actionInds,op_b):
                vec_index += multipliers[j]*bInd
            baseinds[ii] = vec_index

        self.data_ref1 = noop_incrementers
        self.data_ref2 = numBasisEls_noop_blankaction
        self.data_ref3 = baseinds
        self.data_ref4 = blocksizes
        self.embedded = embedded_op # needed to prevent garbage collection?
        self.c_gate = new DMOpCRep_Embedded(embedded_op.c_gate,
                                              <INT*>noop_incrementers.data, <INT*>numBasisEls_noop_blankaction.data,
                                              <INT*>baseinds.data, <INT*>blocksizes.data,
                                              embedded_dim, nComponentsInActiveBlock,
                                              iActiveBlock, nBlocks, dim)


cdef class DMOpRep_Composed(DMOpRep):
    cdef object list_of_factors # list of DMOpRep objs?

    def __cinit__(self, factor_op_reps, INT dim):
        self.list_of_factors = factor_op_reps
        cdef INT i
        cdef INT nfactors = len(factor_op_reps)
        cdef vector[DMOpCRep*] gate_creps = vector[DMGateCRep_ptr](nfactors)
        for i in range(nfactors):
            gate_creps[i] = (<DMOpRep?>factor_op_reps[i]).c_gate
        self.c_gate = new DMOpCRep_Composed(gate_creps, dim)


cdef class DMOpRep_Sum(DMOpRep):
    cdef object list_of_factors # list of DMOpRep objs?

    def __cinit__(self, factor_reps, INT dim):
        self.list_of_factors = factor_reps
        cdef INT i
        cdef INT nfactors = len(factor_reps)
        cdef vector[DMOpCRep*] factor_creps = vector[DMGateCRep_ptr](nfactors)
        for i in range(nfactors):
            factor_creps[i] = (<DMOpRep?>factor_reps[i]).c_gate
        self.c_gate = new DMOpCRep_Sum(factor_creps, dim)


cdef class DMOpRep_Exponentiated(DMOpRep):
    cdef DMOpRep exponentiated_op
    cdef INT power

    def __cinit__(self, DMOpRep exponentiated_op_rep, INT power, INT dim):
        self.exponentiated_op = exponentiated_op_rep
        self.power = power
        self.c_gate = new DMOpCRep_Exponentiated(exponentiated_op_rep.c_gate, power, dim)


cdef class DMOpRep_Lindblad(DMOpRep):
    cdef object data_ref1
    cdef np.ndarray data_ref2
    cdef np.ndarray data_ref3
    cdef np.ndarray data_ref4

    def __cinit__(self, errgen_rep,
                  double mu, double eta, INT m_star, INT s,
                  np.ndarray[double, ndim=1, mode='c'] unitarypost_data,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] unitarypost_indices,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] unitarypost_indptr):
        self.data_ref1 = errgen_rep
        self.data_ref2 = unitarypost_data
        self.data_ref3 = unitarypost_indices
        self.data_ref4 = unitarypost_indptr
        cdef INT dim = errgen_rep.dim
        cdef INT upost_nnz = unitarypost_data.shape[0]
        self.c_gate = new DMOpCRep_Lindblad((<DMOpRep?>errgen_rep).c_gate,
                                              mu, eta, m_star, s, dim,
                                              <double*>unitarypost_data.data,
                                              <INT*>unitarypost_indices.data,
                                              <INT*>unitarypost_indptr.data, upost_nnz)

cdef class DMOpRep_Sparse(DMOpRep):
    cdef np.ndarray data_ref1
    cdef np.ndarray data_ref2
    cdef np.ndarray data_ref3

    def __cinit__(self, np.ndarray[double, ndim=1, mode='c'] A_data,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] A_indices,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] A_indptr):
        self.data_ref1 = A_data
        self.data_ref2 = A_indices
        self.data_ref3 = A_indptr
        cdef INT nnz = A_data.shape[0]
        cdef INT dim = A_indptr.shape[0]-1
        self.c_gate = new DMOpCRep_Sparse(<double*>A_data.data, <INT*>A_indices.data,
                                             <INT*>A_indptr.data, nnz, dim);


# State vector (SV) propagation wrapper classes
cdef class SVStateRep: #(StateRep):
    cdef SVStateCRep* c_state
    cdef np.ndarray data_ref

    def __cinit__(self, np.ndarray[np.complex128_t, ndim=1, mode='c'] data):
        self.data_ref = data # holds reference to data so it doesn't get garbage collected - or could copy=true
        self.c_state = new SVStateCRep(<double complex*>data.data,<INT>data.shape[0],<bool>0)

    @property
    def dim(self):
        return self.c_state._dim

    def __dealloc__(self):
        del self.c_state

    def __str__(self):
        return str([self.c_state._dataptr[i] for i in range(self.c_state._dim)])


cdef class SVEffectRep:
    cdef SVEffectCRep* c_effect

    def __cinit__(self):
        pass # no init; could set self.c_effect = NULL? could assert(False)?
    def __dealloc__(self):
        del self.c_effect # check for NULL?

    def probability(self, SVStateRep state not None):
        #unnecessary (just put in signature): cdef SVStateRep st = <SVStateRep?>state
        return self.c_effect.probability(state.c_state)

    @property
    def dim(self):
        return self.c_effect._dim


cdef class SVEffectRep_Dense(SVEffectRep):
    cdef np.ndarray data_ref

    def __cinit__(self, np.ndarray[np.complex128_t, ndim=1, mode='c'] data):
        self.data_ref = data # holds reference to data
        self.c_effect = new SVEffectCRep_Dense(<double complex*>data.data,
                                               <INT>data.shape[0])

cdef class SVEffectRep_TensorProd(SVEffectRep):
    cdef np.ndarray data_ref1
    cdef np.ndarray data_ref2

    def __cinit__(self, np.ndarray[np.complex128_t, ndim=2, mode='c'] kron_array,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] factor_dims, INT nfactors, INT max_factor_dim, INT dim):
        # cdef INT dim = np.product(factor_dims) -- just send as argument
        self.data_ref1 = kron_array
        self.data_ref2 = factor_dims
        self.c_effect = new SVEffectCRep_TensorProd(<double complex*>kron_array.data,
                                                    <INT*>factor_dims.data,
                                                    nfactors, max_factor_dim, dim)


cdef class SVEffectRep_Computational(SVEffectRep):

    def __cinit__(self, np.ndarray[np.int64_t, ndim=1, mode='c'] zvals, INT dim):
        # cdef INT dim = 2**zvals.shape[0] -- just send as argument
        cdef INT nfactors = zvals.shape[0]
        cdef double abs_elval = 1/(np.sqrt(2)**nfactors)
        cdef INT base = 1
        cdef INT zvals_int = 0
        for i in range(nfactors):
            zvals_int += base * zvals[i]
            base = base << 1 # *= 2
        self.c_effect = new SVEffectCRep_Computational(nfactors, zvals_int, dim)



cdef class SVOpRep:
    cdef SVOpCRep* c_gate

    def __cinit__(self):
        pass # self.c_gate = NULL ?

    def __dealloc__(self):
        del self.c_gate

    def acton(self, SVStateRep state not None):
        cdef SVStateRep out_state = SVStateRep(np.empty(self.c_gate._dim, dtype=np.complex128))
        #print("PYX acton called w/dim ", self.c_gate._dim, out_state.c_state._dim)
        # assert(state.c_state._dataptr != out_state.c_state._dataptr) # DEBUG
        self.c_gate.acton(state.c_state, out_state.c_state)
        return out_state

    #FUTURE: adjoint acton

    @property
    def dim(self):
        return self.c_gate._dim


cdef class SVOpRep_Dense(SVOpRep):
    cdef np.ndarray data_ref

    def __cinit__(self, np.ndarray[np.complex128_t, ndim=2, mode='c'] data):
        self.data_ref = data
        #print("PYX dense gate constructed w/dim ",data.shape[0])
        self.c_gate = new SVOpCRep_Dense(<double complex*>data.data,
                                           <INT>data.shape[0])

    def __str__(self):
        s = ""
        cdef SVOpCRep_Dense* my_cgate = <SVOpCRep_Dense*>self.c_gate # b/c we know it's a _Dense gate...
        cdef INT i,j,k
        for i in range(my_cgate._dim):
            k = i*my_cgate._dim
            for j in range(my_cgate._dim):
                s += str(my_cgate._dataptr[k+j]) + " "
            s += "\n"
        return s


cdef class SVOpRep_Embedded(SVOpRep):
    cdef np.ndarray data_ref1
    cdef np.ndarray data_ref2
    cdef np.ndarray data_ref3
    cdef np.ndarray data_ref4
    cdef SVOpRep embedded


    def __cinit__(self, SVOpRep embedded_op,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] numBasisEls,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] actionInds,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] blocksizes,
		  INT embedded_dim, INT nComponentsInActiveBlock,
                  INT iActiveBlock, INT nBlocks, INT dim):

        cdef INT i, j

        # numBasisEls_noop_blankaction is just numBasisEls with actionInds == 1
        cdef np.ndarray[np.int64_t, ndim=1, mode='c'] numBasisEls_noop_blankaction = numBasisEls.copy()
        for i in actionInds:
            numBasisEls_noop_blankaction[i] = 1 # for indexing the identity space

        # multipliers to go from per-label indices to tensor-product-block index
        # e.g. if map(len,basisInds) == [1,4,4] then multipliers == [ 16 4 1 ]
        cdef np.ndarray tmp = np.empty(nComponentsInActiveBlock,np.int64)
        tmp[0] = 1
        for i in range(1,nComponentsInActiveBlock):
            tmp[i] = numBasisEls[nComponentsInActiveBlock-i]
        multipliers = np.array( np.flipud( np.cumprod(tmp) ), np.int64)

        # noop_incrementers[i] specifies how much the overall vector index
        #  is incremented when the i-th "component" digit is advanced
        cdef INT dec = 0
        cdef np.ndarray[np.int64_t, ndim=1, mode='c'] noop_incrementers = np.empty(nComponentsInActiveBlock,np.int64)
        for i in range(nComponentsInActiveBlock-1,-1,-1):
            noop_incrementers[i] = multipliers[i] - dec
            dec += (numBasisEls_noop_blankaction[i]-1)*multipliers[i]

        cdef INT vec_index
        cdef INT offset = 0 #number of basis elements preceding our block's elements
        for i in range(iActiveBlock):
            offset += blocksizes[i]

        # self.baseinds specifies the contribution from the "active
        #  component" digits to the overall vector index.
        cdef np.ndarray[np.int64_t, ndim=1, mode='c'] baseinds = np.empty(embedded_dim,np.int64)
        basisInds_action = [ list(range(numBasisEls[i])) for i in actionInds ]
        for ii,op_b in enumerate(_itertools.product(*basisInds_action)):
            vec_index = offset
            for j,bInd in zip(actionInds,op_b):
                vec_index += multipliers[j]*bInd
            baseinds[ii] = vec_index

        self.data_ref1 = noop_incrementers
        self.data_ref2 = numBasisEls_noop_blankaction
        self.data_ref3 = baseinds
        self.data_ref4 = blocksizes
        self.embedded = embedded_op # needed to prevent garbage collection?
        self.c_gate = new SVOpCRep_Embedded(embedded_op.c_gate,
                                              <INT*>noop_incrementers.data, <INT*>numBasisEls_noop_blankaction.data,
                                              <INT*>baseinds.data, <INT*>blocksizes.data,
                                              embedded_dim, nComponentsInActiveBlock,
                                              iActiveBlock, nBlocks, dim)


cdef class SVOpRep_Composed(SVOpRep):
    cdef object list_of_factors # list of SVOpRep objs?

    def __cinit__(self, factor_op_reps, INT dim):
        self.list_of_factors = factor_op_reps
        cdef INT i
        cdef INT nfactors = len(factor_op_reps)
        cdef vector[SVOpCRep*] gate_creps = vector[SVGateCRep_ptr](nfactors)
        for i in range(nfactors):
            gate_creps[i] = (<SVOpRep?>factor_op_reps[i]).c_gate
        self.c_gate = new SVOpCRep_Composed(gate_creps, dim)


cdef class SVOpRep_Sum(SVOpRep):
    cdef object list_of_factors # list of SVOpRep objs?

    def __cinit__(self, factor_reps, INT dim):
        self.list_of_factors = factor_reps
        cdef INT i
        cdef INT nfactors = len(factor_reps)
        cdef vector[SVOpCRep*] factor_creps = vector[SVGateCRep_ptr](nfactors)
        for i in range(nfactors):
            factor_creps[i] = (<SVOpRep?>factor_reps[i]).c_gate
        self.c_gate = new SVOpCRep_Sum(factor_creps, dim)

cdef class SVOpRep_Exponentiated(SVOpRep):
    cdef SVOpRep exponentiated_op
    cdef INT power

    def __cinit__(self, SVOpRep exponentiated_op_rep, INT power, INT dim):
        self.exponentiated_op = exponentiated_op_rep
        self.power = power
        self.c_gate = new SVOpCRep_Exponentiated(exponentiated_op_rep.c_gate, power, dim)



# Stabilizer state (SB) propagation wrapper classes
cdef class SBStateRep: #(StateRep):
    cdef SBStateCRep* c_state
    cdef np.ndarray data_ref1
    cdef np.ndarray data_ref2
    cdef np.ndarray data_ref3

    def __cinit__(self, np.ndarray[np.int64_t, ndim=2, mode='c'] smatrix,
                  np.ndarray[np.int64_t, ndim=2, mode='c'] pvectors,
                  np.ndarray[np.complex128_t, ndim=1, mode='c'] amps):
        self.data_ref1 = smatrix
        self.data_ref2 = pvectors
        self.data_ref3 = amps
        cdef INT namps = amps.shape[0]
        cdef INT n = smatrix.shape[0] // 2
        self.c_state = new SBStateCRep(<INT*>smatrix.data,<INT*>pvectors.data,
                                       <double complex*>amps.data, namps, n)

    @property
    def nqubits(self):
        return self.c_state._n

    def __dealloc__(self):
        del self.c_state

    def __str__(self):
        #DEBUG
        cdef INT n = self.c_state._n
        cdef INT namps = self.c_state._namps
        s = "SBStateRep\n"
        s +=" smx = " + str([ self.c_state._smatrix[ii] for ii in range(2*n*2*n) ])
        s +=" pvecs = " + str([ self.c_state._pvectors[ii] for ii in range(2*n) ])
        s +=" amps = " + str([ self.c_state._amps[ii] for ii in range(namps) ])
        s +=" zstart = " + str(self.c_state._zblock_start)
        return s


cdef class SBEffectRep:
    cdef SBEffectCRep* c_effect
    cdef np.ndarray data_ref

    def __cinit__(self, np.ndarray[np.int64_t, ndim=1, mode='c'] zvals):
        self.data_ref = zvals
        self.c_effect = new SBEffectCRep(<INT*>zvals.data,
                                         <INT>zvals.shape[0])

    def __dealloc__(self):
        del self.c_effect # check for NULL?

    @property
    def nqubits(self):
        return self.c_effect._n

    def probability(self, SBStateRep state not None):
        #unnecessary (just put in signature): cdef SBStateRep st = <SBStateRep?>state
        return self.c_effect.probability(state.c_state)

    def amplitude(self, SBStateRep state not None):
        return self.c_effect.amplitude(state.c_state)



cdef class SBOpRep:
    cdef SBOpCRep* c_gate

    def __cinit__(self):
        pass # self.c_gate = NULL ?

    def __dealloc__(self):
        del self.c_gate

    @property
    def nqubits(self):
        return self.c_gate._n

    def acton(self, SBStateRep state not None):
        cdef INT n = self.c_gate._n
        cdef INT namps = state.c_state._namps
        cdef SBStateRep out_state = SBStateRep(np.empty((2*n,2*n), dtype=np.int64),
                                               np.empty((namps,2*n), dtype=np.int64),
                                               np.empty(namps, dtype=np.complex128))
        self.c_gate.acton(state.c_state, out_state.c_state)
        return out_state

    def adjoint_acton(self, SBStateRep state not None):
        cdef INT n = self.c_gate._n
        cdef INT namps = state.c_state._namps
        cdef SBStateRep out_state = SBStateRep(np.empty((2*n,2*n), dtype=np.int64),
                                               np.empty((namps,2*n), dtype=np.int64),
                                               np.empty(namps, dtype=np.complex128))
        self.c_gate.adjoint_acton(state.c_state, out_state.c_state)
        return out_state


cdef class SBOpRep_Embedded(SBOpRep):
    cdef np.ndarray data_ref
    cdef SBOpRep embedded

    def __cinit__(self, SBOpRep embedded_op, INT n,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] qubits):
        self.data_ref = qubits
        self.embedded = embedded_op # needed to prevent garbage collection?
        self.c_gate = new SBOpCRep_Embedded(embedded_op.c_gate, n,
                                              <INT*>qubits.data, <INT>qubits.shape[0])


cdef class SBOpRep_Composed(SBOpRep):
    cdef object list_of_factors # list of SBOpRep objs?

    def __cinit__(self, factor_op_reps, INT n):
        self.list_of_factors = factor_op_reps
        cdef INT i
        cdef INT nfactors = len(factor_op_reps)
        cdef vector[SBOpCRep*] gate_creps = vector[SBGateCRep_ptr](nfactors)
        for i in range(nfactors):
            gate_creps[i] = (<SBOpRep?>factor_op_reps[i]).c_gate
        self.c_gate = new SBOpCRep_Composed(gate_creps, n)


cdef class SBOpRep_Sum(SBOpRep):
    cdef object list_of_factors # list of SBOpRep objs?

    def __cinit__(self, factor_reps, INT n):
        self.list_of_factors = factor_reps
        cdef INT i
        cdef INT nfactors = len(factor_reps)
        cdef vector[SBOpCRep*] factor_creps = vector[SBGateCRep_ptr](nfactors)
        for i in range(nfactors):
            factor_creps[i] = (<SBOpRep?>factor_reps[i]).c_gate
        self.c_gate = new SBOpCRep_Sum(factor_creps, n)

cdef class SBOpRep_Exponentiated(SBOpRep):
    cdef SBOpRep exponentiated_op
    cdef INT power

    def __cinit__(self, SBOpRep exponentiated_op_rep, INT power, INT n):
        self.exponentiated_op = exponentiated_op_rep
        self.power = power
        self.c_gate = new SBOpCRep_Exponentiated(exponentiated_op_rep.c_gate, power, n)



cdef class SBOpRep_Clifford(SBOpRep):
    cdef np.ndarray data_ref1
    cdef np.ndarray data_ref2
    cdef np.ndarray data_ref3
    cdef np.ndarray data_ref4
    cdef np.ndarray data_ref5
    cdef np.ndarray data_ref6

    def __cinit__(self, np.ndarray[np.int64_t, ndim=2, mode='c'] smatrix,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] svector,
                  np.ndarray[np.int64_t, ndim=2, mode='c'] smatrix_inv,
                  np.ndarray[np.int64_t, ndim=1, mode='c'] svector_inv,
                  np.ndarray[np.complex128_t, ndim=2, mode='c'] unitary):

        self.data_ref1 = smatrix
        self.data_ref2 = svector
        self.data_ref3 = unitary
        self.data_ref4 = smatrix_inv
        self.data_ref5 = svector_inv
        self.data_ref6 = np.ascontiguousarray(np.conjugate(np.transpose(unitary)))
           # the "ascontiguousarray" is crucial, since we just use the .data below
        cdef INT n = smatrix.shape[0] // 2
        self.c_gate = new SBOpCRep_Clifford(<INT*>smatrix.data, <INT*>svector.data, <double complex*>unitary.data,
                                              <INT*>smatrix_inv.data, <INT*>svector_inv.data,
                                              <double complex*>self.data_ref6.data, n)

# Other classes
cdef class PolyRep:
    cdef PolyCRep* c_poly

    #Use normal init here so can bypass to create from an already alloc'd c_poly
    def __init__(self, coeff_dict, INT max_order, INT max_num_vars, INT vindices_per_int):
        cdef unordered_map[PolyVarsIndex, complex] coeffs
        cdef PolyVarsIndex indx
        for i_tup,c in coeff_dict.items():
            indx = PolyVarsIndex(len(i_tup))
            for ii,i in enumerate(i_tup):
                indx._parts[ii] = i
            coeffs[indx] = <double complex>c
        self.c_poly = new PolyCRep(coeffs, max_order, max_num_vars, vindices_per_int)

    def __dealloc__(self):
        del self.c_poly

    @property
    def max_order(self): # so we can convert back to python Polys
        return self.c_poly._max_order

    @property
    def max_num_vars(self): # so we can convert back to python Polys
        return self.c_poly._max_num_vars

    @property
    def coeffs(self): # so we can convert back to python Polys
        # need to convert _coeffs keys (PolyVarsIndex objs) to tuples of Python ints
        cdef INT i;
        ret = {}
        cdef vector[INT].iterator vit
        cdef unordered_map[PolyVarsIndex, complex].iterator it = self.c_poly._coeffs.begin()
        while(it != self.c_poly._coeffs.end()):
            i_tup = []
            i_vec = deref(it).first._parts
            vit = i_vec.begin()
            while(vit != i_vec.end()):
                i_tup.append( deref(vit) )
                inc(vit)
            ret[tuple(i_tup)] = deref(it).second
            inc(it)
        return ret

    def compact_complex(self):
        cdef INT i,l, iTerm, nVarIndices=0;
        cdef PolyVarsIndex k;
        cdef vector[INT] v;
        cdef vector[INT].iterator vit
        cdef unordered_map[PolyVarsIndex, complex].iterator it = self.c_poly._coeffs.begin()
        cdef vector[ pair[PolyVarsIndex, vector[INT]] ] vinds;
        cdef INT nTerms = self.c_poly._coeffs.size()

        while(it != self.c_poly._coeffs.end()):
            vs = self.c_poly.int_to_vinds( deref(it).first )
            nVarIndices += vs.size()
            vinds.push_back( pair[PolyVarsIndex, vector[INT]](deref(it).first, vs) )
            inc(it)

        vtape = np.empty(1 + nTerms + nVarIndices, np.int64) # "variable" tape
        ctape = np.empty(nTerms, np.complex128) # "coefficient tape"

        i = 0
        vtape[i] = nTerms; i+=1
        stdsort(vinds.begin(), vinds.end(), &compare_pair) # sorts in place
        for iTerm in range(vinds.size()):
            k = vinds[iTerm].first
            v = vinds[iTerm].second
            l = v.size()
            ctape[iTerm] = self.c_poly._coeffs[k]
            vtape[i] = l; i += 1
            vtape[i:i+l] = v; i += l

        return vtape, ctape

cdef bool compare_pair(const pair[PolyVarsIndex, vector[INT]]& a, const pair[PolyVarsIndex, vector[INT]]& b):
    return a.first < b.first

cdef class SVTermRep:
    cdef SVTermCRep* c_term

    #Hold references to other reps so we don't GC them
    cdef PolyRep coeff_ref
    cdef SVStateRep state_ref1
    cdef SVStateRep state_ref2
    cdef SVEffectRep effect_ref1
    cdef SVEffectRep effect_ref2
    cdef object list_of_preops_ref
    cdef object list_of_postops_ref

    def __cinit__(self, PolyRep coeff, double mag, double logmag,
                  SVStateRep pre_state, SVStateRep post_state,
                  SVEffectRep pre_effect, SVEffectRep post_effect, pre_ops, post_ops):
        self.coeff_ref = coeff
        self.list_of_preops_ref = pre_ops
        self.list_of_postops_ref = post_ops

        cdef INT i
        cdef INT npre = len(pre_ops)
        cdef INT npost = len(post_ops)
        cdef vector[SVOpCRep*] c_pre_ops = vector[SVGateCRep_ptr](npre)
        cdef vector[SVOpCRep*] c_post_ops = vector[SVGateCRep_ptr](<INT>len(post_ops))
        for i in range(npre):
            c_pre_ops[i] = (<SVOpRep?>pre_ops[i]).c_gate
        for i in range(npost):
            c_post_ops[i] = (<SVOpRep?>post_ops[i]).c_gate

        if pre_state is not None or post_state is not None:
            assert(pre_state is not None and post_state is not None)
            self.state_ref1 = pre_state
            self.state_ref2 = post_state
            self.c_term = new SVTermCRep(coeff.c_poly, mag, logmag, pre_state.c_state, post_state.c_state,
                                         c_pre_ops, c_post_ops);
        elif pre_effect is not None or post_effect is not None:
            assert(pre_effect is not None and post_effect is not None)
            self.effect_ref1 = pre_effect
            self.effect_ref2 = post_effect
            self.c_term = new SVTermCRep(coeff.c_poly, mag, logmag, pre_effect.c_effect, post_effect.c_effect,
                                         c_pre_ops, c_post_ops);
        else:
            self.c_term = new SVTermCRep(coeff.c_poly, mag, logmag, c_pre_ops, c_post_ops);

    def __dealloc__(self):
        del self.c_term


cdef class SVTermDirectRep:
    cdef SVTermDirectCRep* c_term

    #Hold references to other reps so we don't GC them
    cdef SVStateRep state_ref1
    cdef SVStateRep state_ref2
    cdef SVEffectRep effect_ref1
    cdef SVEffectRep effect_ref2
    cdef object list_of_preops_ref
    cdef object list_of_postops_ref

    def __cinit__(self, double complex coeff, double mag, double logmag,
                  SVStateRep pre_state, SVStateRep post_state,
                  SVEffectRep pre_effect, SVEffectRep post_effect, pre_ops, post_ops):
        self.list_of_preops_ref = pre_ops
        self.list_of_postops_ref = post_ops

        cdef INT i
        cdef INT npre = len(pre_ops)
        cdef INT npost = len(post_ops)
        cdef vector[SVOpCRep*] c_pre_ops = vector[SVGateCRep_ptr](npre)
        cdef vector[SVOpCRep*] c_post_ops = vector[SVGateCRep_ptr](<INT>len(post_ops))
        for i in range(npre):
            c_pre_ops[i] = (<SVOpRep?>pre_ops[i]).c_gate
        for i in range(npost):
            c_post_ops[i] = (<SVOpRep?>post_ops[i]).c_gate

        if pre_state is not None or post_state is not None:
            assert(pre_state is not None and post_state is not None)
            self.state_ref1 = pre_state
            self.state_ref2 = post_state
            self.c_term = new SVTermDirectCRep(coeff, mag, logmag, pre_state.c_state, post_state.c_state,
                                               c_pre_ops, c_post_ops);
        elif pre_effect is not None or post_effect is not None:
            assert(pre_effect is not None and post_effect is not None)
            self.effect_ref1 = pre_effect
            self.effect_ref2 = post_effect
            self.c_term = new SVTermDirectCRep(coeff, mag, logmag, pre_effect.c_effect, post_effect.c_effect,
                                               c_pre_ops, c_post_ops);
        else:
            self.c_term = new SVTermDirectCRep(coeff, mag, logmag, c_pre_ops, c_post_ops);

    def set_coeff(self, coeff):
        self.c_term._coeff = coeff

    def __dealloc__(self):
        del self.c_term


cdef class SBTermRep:
    cdef SBTermCRep* c_term

    #Hold references to other reps so we don't GC them
    cdef PolyRep coeff_ref
    cdef SBStateRep state_ref1
    cdef SBStateRep state_ref2
    cdef SBEffectRep effect_ref1
    cdef SBEffectRep effect_ref2
    cdef object list_of_preops_ref
    cdef object list_of_postops_ref

    def __cinit__(self, PolyRep coeff, double mag, double logmag,
                  SBStateRep pre_state, SBStateRep post_state,
                  SBEffectRep pre_effect, SBEffectRep post_effect, pre_ops, post_ops):
        self.coeff_ref = coeff
        self.list_of_preops_ref = pre_ops
        self.list_of_postops_ref = post_ops

        cdef INT i
        cdef INT npre = len(pre_ops)
        cdef INT npost = len(post_ops)
        cdef vector[SBOpCRep*] c_pre_ops = vector[SBGateCRep_ptr](npre)
        cdef vector[SBOpCRep*] c_post_ops = vector[SBGateCRep_ptr](<INT>len(post_ops))
        for i in range(npre):
            c_pre_ops[i] = (<SBOpRep?>pre_ops[i]).c_gate
        for i in range(npost):
            c_post_ops[i] = (<SBOpRep?>post_ops[i]).c_gate

        if pre_state is not None or post_state is not None:
            assert(pre_state is not None and post_state is not None)
            self.state_ref1 = pre_state
            self.state_ref2 = post_state
            self.c_term = new SBTermCRep(coeff.c_poly, mag, logmag,
                                         pre_state.c_state, post_state.c_state,
                                         c_pre_ops, c_post_ops);
        elif pre_effect is not None or post_effect is not None:
            assert(pre_effect is not None and post_effect is not None)
            self.effect_ref1 = pre_effect
            self.effect_ref2 = post_effect
            self.c_term = new SBTermCRep(coeff.c_poly, mag, logmag,
                                         pre_effect.c_effect, post_effect.c_effect,
                                         c_pre_ops, c_post_ops);
        else:
            self.c_term = new SBTermCRep(coeff.c_poly, mag, logmag, c_pre_ops, c_post_ops);

    def __dealloc__(self):
        del self.c_term


cdef class RepCacheEl:
    cdef vector[SVTermCRep_ptr] reps
    cdef vector[INT] foat_indices
    cdef vector[INT] E_indices
    cdef object pyterm_references

    def __cinit__(self):
        self.reps = vector[SVTermCRep_ptr](0)
        self.foat_indices = vector[INT](0)
        self.E_indices = vector[INT](0)
        self.pyterm_references = []


## END CLASSES -- BEGIN CALC METHODS


def propagate_staterep(staterep, operationreps):
    # FUTURE: could use inner C-reps to do propagation
    # instead of using extension type wrappers as this does now
    ret = staterep
    for oprep in operationreps:
        ret = oprep.acton(ret)
        # DEBUG print("post-action rhorep = ",str(ret))
    return ret


cdef vector[vector[INT]] convert_evaltree(evalTree, operation_lookup):
    # c_evalTree :
    # an array of INT-arrays; each INT-array is [i,iStart,iCache,<remainder gate indices>]
    cdef vector[INT] intarray
    cdef vector[vector[INT]] c_evalTree = vector[vector[INT]](len(evalTree))
    for kk,ii in enumerate(evalTree.get_evaluation_order()):
        iStart,remainder,iCache = evalTree[ii]
        if iStart is None: iStart = -1 # so always an int
        if iCache is None: iCache = -1 # so always an int
        intarray = vector[INT](3 + len(remainder))
        intarray[0] = ii
        intarray[1] = iStart
        intarray[2] = iCache
        for jj,gl in enumerate(remainder,start=3):
            intarray[jj] = operation_lookup[gl]
        c_evalTree[kk] = intarray

    return c_evalTree

cdef vector[DMStateCRep*] create_rhocache(INT cacheSize, INT state_dim):
    cdef INT i
    cdef vector[DMStateCRep*] rho_cache = vector[DMStateCRep_ptr](cacheSize)
    for i in range(cacheSize): # fill cache with empty but alloc'd states
        rho_cache[i] = new DMStateCRep(state_dim)
    return rho_cache

cdef void free_rhocache(vector[DMStateCRep*] rho_cache):
    cdef UINT i
    for i in range(rho_cache.size()): # fill cache with empty but alloc'd states
        del rho_cache[i]


cdef vector[DMOpCRep*] convert_gatereps(operationreps):
    # c_gatereps : an array of DMGateCReps
    cdef vector[DMOpCRep*] c_gatereps = vector[DMGateCRep_ptr](len(operationreps))
    for ii,grep in operationreps.items(): # (ii = python variable)
        c_gatereps[ii] = (<DMOpRep?>grep).c_gate
    return c_gatereps

cdef DMStateCRep* convert_rhorep(rhorep):
    # extract c-reps from rhorep and ereps => c_rho and c_ereps
    return (<DMStateRep?>rhorep).c_state

cdef vector[DMEffectCRep*] convert_ereps(ereps):
    cdef vector[DMEffectCRep*] c_ereps = vector[DMEffectCRep_ptr](len(ereps))
    for i in range(len(ereps)):
        c_ereps[i] = (<DMEffectRep>ereps[i]).c_effect
    return c_ereps


def DM_compute_pr_cache(calc, rholabel, elabels, evalTree, comm):

    rhoVec,EVecs = calc._rhoEs_from_labels(rholabel, elabels)
    pCache = np.empty((len(evalTree),len(EVecs)),'d')

    #Get (extension-type) representation objects
    rhorep = rhoVec.torep('prep')
    ereps = [ E.torep('effect') for E in EVecs]  # could cache these? then have torep keep a non-dense rep that can be quickly kron'd for a tensorprod spamvec
    operation_lookup = { lbl:i for i,lbl in enumerate(evalTree.opLabels) } # operation labels -> ints for faster lookup
    operationreps = { i:calc.sos.get_operation(lbl).torep() for lbl,i in operation_lookup.items() }

    # convert to C-mode:  evaltree, operation_lookup, operationreps
    cdef c_evalTree = convert_evaltree(evalTree, operation_lookup)
    cdef DMStateCRep *c_rho = convert_rhorep(rhorep)
    cdef vector[DMOpCRep*] c_gatereps = convert_gatereps(operationreps)
    cdef vector[DMEffectCRep*] c_ereps = convert_ereps(ereps)

    # create rho_cache = vector of DMStateCReps
    #print "DB: creating rho_cache of size %d * %g GB => %g GB" % \
    #   (evalTree.cache_size(), 8.0 * c_rho._dim / 1024.0**3, evalTree.cache_size() * 8.0 * c_rho._dim / 1024.0**3)
    cdef vector[DMStateCRep*] rho_cache = create_rhocache(evalTree.cache_size(), c_rho._dim)

    dm_compute_pr_cache(pCache, c_evalTree, c_gatereps, c_rho, c_ereps, &rho_cache, comm)

    free_rhocache(rho_cache)  #delete cache entries
    return pCache



cdef dm_compute_pr_cache(double[:,:] ret,
                         vector[vector[INT]] c_evalTree,
                         vector[DMOpCRep*] c_gatereps,
                         DMStateCRep *c_rho, vector[DMEffectCRep*] c_ereps,
                         vector[DMStateCRep*]* prho_cache, comm): # any way to transmit comm?
    #Note: we need to take in rho_cache as a pointer b/c we may alter the values its
    # elements point to (instead of copying the states) - we just guarantee that in the end
    # all of the cache entries are filled with allocated (by 'new') states that the caller
    # can deallocate at will.
    cdef INT k,l,i,istart, icache
    cdef double p
    cdef INT dim = c_rho._dim
    cdef DMStateCRep *init_state
    cdef DMStateCRep *prop1
    cdef DMStateCRep *tprop
    cdef DMStateCRep *final_state
    cdef DMStateCRep *prop2 = new DMStateCRep(dim)
    cdef DMStateCRep *shelved = new DMStateCRep(dim)

    #print "BEGIN"

    #Invariants required for proper memory management:
    # - upon loop entry, prop2 is allocated and prop1 is not (it doesn't "own" any memory)
    # - all rho_cache entries have been allocated via "new"
    for k in range(<INT>c_evalTree.size()):
        #t0 = pytime.time() # DEBUG
        intarray = c_evalTree[k]
        i = intarray[0]
        istart = intarray[1]
        icache = intarray[2]

        if istart == -1:  init_state = c_rho
        else:             init_state = deref(prho_cache)[istart]

        #DEBUG
        #print "LOOP i=",i," istart=",istart," icache=",icache," remcnt=",(intarray.size()-3)
        #print [ init_state._dataptr[t] for t in range(4) ]

        #Propagate state rep
        # prop2 should already be alloc'd; need to "allocate" prop1 - either take from cache or from "shelf"
        prop1 = shelved if icache == -1 else deref(prho_cache)[icache]
        prop1.copy_from(init_state) # copy init_state -> prop1
        #print " prop1:";  print [ prop1._dataptr[t] for t in range(4) ]
        #t1 = pytime.time() # DEBUG
        for l in range(3,<INT>intarray.size()): #during loop, both prop1 & prop2 are alloc'd
            #print "begin acton %d: %.2fs since last, %.2fs elapsed" % (l-2,pytime.time()-t1,pytime.time()-t0) # DEBUG
            #t1 = pytime.time() #DEBUG
            c_gatereps[intarray[l]].acton(prop1,prop2)
            #print " post-act prop2:"; print [ prop2._dataptr[t] for t in range(4) ]
            tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
        final_state = prop1 # output = prop1 (after swap from loop above)
        # Note: prop2 is the other alloc'd state and this maintains invariant
        #print " final:"; print [ final_state._dataptr[t] for t in range(4) ]

        #print "begin prob comps: %.2fs since last, %.2fs elapsed" % (pytime.time()-t1, pytime.time()-t0) # DEBUG
        for j in range(<INT>c_ereps.size()):
            p = c_ereps[j].probability(final_state) #outcome probability
            #print("processing ",i,j,p)
            ret[i,j] = p

        if icache != -1:
            deref(prho_cache)[icache] = final_state # store this state in the cache
        else: # our 2nd state was pulled from the shelf before; return it
            shelved = final_state
            final_state = NULL
        #print "%d of %d (i=%d,istart=%d,remlen=%d): %.1fs" % (k, c_evalTree.size(), i, istart,
        #                                                      intarray.size()-3, pytime.time()-t0)

    #delete our temp states
    del prop2
    del shelved



def DM_compute_dpr_cache(calc, rholabel, elabels, evalTree, wrtSlice, comm, scratch=None):
    # can remove unused 'scratch' arg once we move hpr_cache to replibs
    cdef double eps = 1e-7 #hardcoded?

    #Compute finite difference derivatives, one parameter at a time.
    param_indices = range(calc.Np) if (wrtSlice is None) else _slct.indices(wrtSlice)
    nDerivCols = len(param_indices) # *all*, not just locally computed ones

    rhoVec,EVecs = calc._rhoEs_from_labels(rholabel, elabels)
    pCache = np.empty((len(evalTree),len(elabels)),'d')
    dpr_cache  = np.zeros((len(evalTree), len(elabels), nDerivCols),'d')
    #print("BEGIN dpr_cache")

    #Get (extension-type) representation objects
    rhorep = calc.sos.get_prep(rholabel).torep('prep')
    ereps = [ calc.sos.get_effect(el).torep('effect') for el in elabels]
    operation_lookup = { lbl:i for i,lbl in enumerate(evalTree.opLabels) } # operation labels -> ints for faster lookup
    operations = { i:calc.sos.get_operation(lbl) for lbl,i in operation_lookup.items() } # it should be safe to do this *once*
    operationreps = { i:op.torep() for i,op in operations.items() }
    #OLD: operationreps = { i:calc.sos.get_operation(lbl).torep() for lbl,i in operation_lookup.items() }
    #print("compute_dpr_cache has %d operations" % len(operation_lookup))

    # convert to C-mode:  evaltree, operation_lookup, operationreps
    cdef c_evalTree = convert_evaltree(evalTree, operation_lookup)
    cdef DMStateCRep *c_rho = convert_rhorep(rhorep)
    cdef vector[DMOpCRep*] c_gatereps = convert_gatereps(operationreps)
    cdef vector[DMEffectCRep*] c_ereps = convert_ereps(ereps)

    # create rho_cache = vector of DMStateCReps
    cdef vector[DMStateCRep*] rho_cache = create_rhocache(evalTree.cache_size(), c_rho._dim)

    #print("DB: params = ", calc.paramvec)
    dm_compute_pr_cache(pCache, c_evalTree, c_gatereps, c_rho, c_ereps, &rho_cache, comm)
    pCache_delta = pCache.copy() # for taking finite differences
    #print("DB: Initial = ", np.linalg.norm(pCache), np.linalg.norm(pCache_delta))
    #print("p = ",pCache)

    all_slices, my_slice, owners, subComm = \
            _mpit.distribute_slice(slice(0,len(param_indices)), comm)

    my_param_indices = param_indices[my_slice]
    st = my_slice.start #beginning of where my_param_indices results
                        # get placed into dpr_cache

    #Get a map from global parameter indices to the desired
    # final index within dpr_cache
    iParamToFinal = { i: st+ii for ii,i in enumerate(my_param_indices) }

    #tStart = pytime.time(); #REMOVE
    #t_pr = 0; t_reps = 0; t_conv=0; t_copy=0; t_fromvec=0; t_gather=0;   #REMOVE
    #time_dict = {'expon':0.0, 'composed': 0.0, 'dense':0.0, 'lind': 0.0} #REMOVE
    orig_vec = calc.to_vector().copy()
    for i in range(calc.Np):
        #print("dprobs cache %d of %d" % (i,calc.Np))
        if i in iParamToFinal:
            iFinal = iParamToFinal[i]
            #t1 = pytime.time() # REMOVE
            vec = orig_vec.copy(); vec[i] += eps
            #t_copy += pytime.time()-t1; t1 = pytime.time() # REMOVE
            calc.from_vector(vec)
            #t_fromvec += pytime.time()-t1; t1 = pytime.time() # REMOVE

            #rebuild reps (not evaltree or operation_lookup)
            rhorep = calc.sos.get_prep(rholabel).torep('prep')
            ereps = [ calc.sos.get_effect(el).torep('effect') for el in elabels]
            operations = { i:calc.sos.get_operation(lbl) for lbl,i in operation_lookup.items() } # NEEDED! (at least for multiQ GST)
            operationreps = { k:op.torep() for k,op in operations.items() }

            #REMOVE: note - used torep(time_dict) in profiling, when torep calls could all their timing info
            #OLD: operationreps = { i:calc.sos.get_operation(lbl).torep() for lbl,i in operation_lookup.items() }
            #t_reps += pytime.time()-t1; t1 = pytime.time() #REMOVE
            c_rho = convert_rhorep(rhorep)
            c_ereps = convert_ereps(ereps)
            c_gatereps = convert_gatereps(operationreps)
            #t_conv += pytime.time()-t1; t1 = pytime.time() #REMOVE

            dm_compute_pr_cache(pCache_delta, c_evalTree, c_gatereps, c_rho, c_ereps, &rho_cache, comm)
            dpr_cache[:,:,iFinal] = (pCache_delta - pCache)/eps
            #t_pr += pytime.time()-t1 #REMOVE

    calc.from_vector(orig_vec)
    free_rhocache(rho_cache)

    #Now each processor has filled the relavant parts of dpr_cache,
    # so gather together:
    #t3 = pytime.time() #REMOVE
    _mpit.gather_slices(all_slices, owners, dpr_cache,[], axes=2, comm=comm)
    #t_gather = pytime.time()-t3 #REMOVE

    # DEBUG LINE USED FOR MONITORING N-QUBIT GST TESTS
    #print("DEBUG TIME: dpr_cache(Np=%d, dim=%d, cachesize=%d, treesize=%d, napplies=%d) in %gs" %
    #      (self.Np, self.dim, cacheSize, len(evalTree), evalTree.get_num_applies(), pytime.time()-tStart)) #DEBUG

    # DEBUG FOR PROFILING THIS FUNCTION
    #print("dpr_cache tot=%.3fs, reps=%.3fs, conv=%.3fs, pr_cache=%.3fs, copy=%.3fs, fromvec=%.3fs, gather=%.3fs" % (pytime.time()-tStart, t_reps, t_conv, t_pr, t_copy, t_fromvec, t_gather))
#, rep_expon=%.3fs rep_comp=%.3fs rep_dense=%.3fs rep_lind=%.3fs"
#, time_dict['expon'], time_dict['composed'],time_dict['dense'],time_dict['lind']))

    return dpr_cache

#HERE
cdef double TDchi2_obj_fn(double p, double f, double Ni, double N, double omitted_p, double minProbClipForWeighting, double extra):
    cdef double cp, v, omitted_cp
    cp = p if p > minProbClipForWeighting else minProbClipForWeighting
    cp = cp if cp < 1 - minProbClipForWeighting else 1 - minProbClipForWeighting
    v = (p - f) * sqrt(N / cp)

    if omitted_p != 0.0:
        # if this is the *last* outcome at this time then account for any omitted probability
        if omitted_p < minProbClipForWeighting:        omitted_cp = minProbClipForWeighting
        elif omitted_p > 1 - minProbClipForWeighting:  omitted_cp = 1 - minProbClipForWeighting
        else:                                          omitted_cp = omitted_p
        v = sqrt(v*v + N * omitted_p*omitted_p / omitted_cp)
    return v  # sqrt(the objective function term)  (the qty stored in cache)

def DM_compute_TDchi2_cache(calc, rholabel, elabels, num_outcomes, evalTree, dataset_rows,
                            minProbClipForWeighting, probClipInterval, comm):
    return DM_compute_TDcache(calc, "chi2", rholabel, elabels, num_outcomes, evalTree,
                              dataset_rows, comm, minProbClipForWeighting, 0.0)


cdef double TDloglpp_obj_fn(double p, double f, double Ni, double N, double omitted_p, double min_p, double a):
    cdef double freq_term, S, S2, v, tmp
    cdef double pos_p = max(p, min_p)

    if Ni != 0.0:
        freq_term = Ni * (log(f) - 1.0)
    else:
        freq_term = 0.0

    S = -Ni / min_p + N
    S2 = 0.5 * Ni / (min_p*min_p)
    v = freq_term + -Ni * log(pos_p) + N * pos_p  # dims K x M (K = nSpamLabels, M = nCircuits)

    # remove small negative elements due to roundoff error (above expression *cannot* really be negative)
    v = max(v, 0)

    # quadratic extrapolation of logl at min_p for probabilities < min_p
    if p < min_p:
        tmp = (p - min_p)
        v = v + S * tmp + S2 * tmp * tmp

    if Ni == 0.0:
        if p >= a:
            v = N * p
        else:
            v = N * ((-1.0 / (3 * a*a)) * p*p*p + p*p / a + a / 3.0)
    # special handling for f == 0 terms
    # using quadratic rounding of function with minimum: max(0,(a-p)^2)/(2a) + p

    if omitted_p != 0.0:
        # if this is the *last* outcome at this time then account for any omitted probability
        v += N * omitted_p if omitted_p >= a else \
            N * ((-1.0 / (3 * a*a)) * omitted_p*omitted_p*omitted_p + omitted_p*omitted_p / a + a / 3.0)

    return v  # objective function term (the qty stored in cache)


def DM_compute_TDloglpp_cache(calc, rholabel, elabels, num_outcomes, evalTree, dataset_rows,
                              minProbClip, radius, probClipInterval, comm):
    return DM_compute_TDcache(calc, "logl", rholabel, elabels, num_outcomes, evalTree,
                              dataset_rows, comm, minProbClip, radius)


def DM_compute_TDcache(calc, objective, rholabel, elabels, num_outcomes, evalTree, dataset_rows, comm, double fnarg1, double fnarg2):

    cdef INT i, j, k, l, n, kinit, nTotOutcomes, N, Ni
    cdef double cur_probtotal, t, t0
    cdef TD_obj_fn objfn
    if objective == "chi2":
        objfn = TDchi2_obj_fn
    else:
        objfn = TDloglpp_obj_fn

    cdef INT cacheSize = evalTree.cache_size()
    cdef np.ndarray ret = np.zeros((len(evalTree), len(elabels)), 'd')  # zeros so we can just add contributions below
    rhoVec, EVecs = calc._rhoEs_from_labels(rholabel, elabels)

    elabels_as_outcomes = [_gt.spamTupleToOutcome((rholabel, e)) for e in elabels]
    outcome_to_elabel_index = {outcome: i for i, outcome in enumerate(elabels_as_outcomes)}
    dataset_rows = {i: row for i,row in enumerate(dataset_rows) } # change to dict for indexing speed - maybe pass this in? FUTURE
    num_outcomes = {i: N for i,N in enumerate(num_outcomes) } # change to dict for indexing speed

    #comm is currently ignored
    #TODO: if evalTree is split, distribute among processors
    for i in evalTree.get_evaluation_order():
        iStart, remainder, iCache = evalTree[i]
        datarow = dataset_rows[i]
        nTotOutcomes = num_outcomes[i]
        N = 0; nOutcomes = 0

        n = len(datarow.reps) # == len(datarow.time)
        kinit = 0
        while kinit < n:
            #Process all outcomes of this datarow occuring at a single time, t0
            t0 = datarow.time[kinit]

            #Compute N, nOutcomes for t0
            N = 0; k = kinit
            while k < n and datarow.time[k] == t0:
                N += datarow.reps[k]
                k += 1
            nOutcomes = k - kinit

            #Compute each outcome's contribution
            cur_probtotal = 0.0
            for l in range(kinit,k):
                t = t0
                rhoVec.set_time(t)
                rho = rhoVec.torep('prep')
                t += rholabel.time

                Ni = datarow.reps[l]
                outcome = datarow.outcomes[l]

                for gl in remainder:
                    op = calc.sos.get_operation(gl)
                    op.set_time(t); t += gl.time  # time in gate label == gate duration?
                    rho = op.torep().acton(rho)

                j = outcome_to_elabel_index[outcome]
                E = EVecs[j]; E.set_time(t)
                p = E.torep('effect').probability(rho)  # outcome probability
                f = float(Ni) / float(N)
                cur_probtotal += p

                omitted_p = 1.0 - cur_probtotal if (l == k-1 and nOutcomes < nTotOutcomes) else 0.0
                # and cur_probtotal < 1.0?

                ret[i, j] += objfn(p, f, Ni, N, omitted_p, fnarg1, fnarg2)
            kinit = k
    return ret


def DM_compute_TDdchi2_cache(calc, rholabel, elabels, num_outcomes, evalTree, dataset_rows,
                             minProbClipForWeighting, probClipInterval, wrtSlice, comm):

    def cachefn(rholabel, elabels, n_outcomes, evTree, dataset_rows, fillComm):
        return DM_compute_TDchi2_cache(calc, rholabel, elabels, n_outcomes, evTree, dataset_rows,
                                       minProbClipForWeighting, probClipInterval, fillComm)

    return DM_compute_timedep_dcache(calc, rholabel, elabels, num_outcomes, evalTree, dataset_rows,
                                     cachefn, wrtSlice, comm)


def DM_compute_TDdloglpp_cache(calc, rholabel, elabels, num_outcomes, evalTree, dataset_rows,
                               minProbClip, radius, probClipInterval, wrtSlice, comm):

    def cachefn(rholabel, elabels, n_outcomes, evTree, dataset_rows, fillComm):
        return DM_compute_TDloglpp_cache(calc, rholabel, elabels, n_outcomes, evTree, dataset_rows,
                                         minProbClip, radius, probClipInterval, fillComm)

    return DM_compute_timedep_dcache(calc, rholabel, elabels, num_outcomes, evalTree, dataset_rows,
                                     cachefn, wrtSlice, comm)


def DM_compute_timedep_dcache(calc, rholabel, elabels, num_outcomes, evalTree, dataset_rows,
                              cachefn, wrtSlice, comm):

    cdef INT i, ii
    cdef double eps = 1e-7  # hardcoded?

    #Compute finite difference derivatives, one parameter at a time.
    param_indices = range(calc.Np) if (wrtSlice is None) else _slct.indices(wrtSlice)
    cdef INT nDerivCols = len(param_indices)  # *all*, not just locally computed ones

    rhoVec, EVecs = calc._rhoEs_from_labels(rholabel, elabels)
    cdef np.ndarray cache = np.empty((len(evalTree), len(elabels)), 'd')
    cdef np.ndarray dcache = np.zeros((len(evalTree), len(elabels), nDerivCols), 'd')

    cdef INT cacheSize = evalTree.cache_size()
    #assert(cacheSize == 0)

    cache = cachefn(rholabel, elabels, num_outcomes, evalTree, dataset_rows, comm)

    all_slices, my_slice, owners, subComm = \
        _mpit.distribute_slice(slice(0, len(param_indices)), comm)

    my_param_indices = param_indices[my_slice]
    cdef INT st = my_slice.start  # beginning of where my_param_indices results
    # get placed into dpr_cache

    #Get a map from global parameter indices to the desired
    # final index within dpr_cache
    iParamToFinal = {i: st + ii for ii, i in enumerate(my_param_indices)}

    orig_vec = calc.to_vector().copy()
    for i in range(calc.Np):
        #print("dprobs cache %d of %d" % (i,calc.Np))
        if i in iParamToFinal:
            iFinal = iParamToFinal[i]
            vec = orig_vec.copy(); vec[i] += eps
            calc.from_vector(vec)
            dcache[:, :, iFinal] = (cachefn(rholabel, elabels, num_outcomes, evalTree, dataset_rows, subComm)
                                    - cache) / eps
    calc.from_vector(orig_vec)

    #Now each processor has filled the relavant parts of dpr_cache,
    # so gather together:
    _mpit.gather_slices(all_slices, owners, dcache, [], axes=2, comm=comm)

    #REMOVE
    # DEBUG LINE USED FOR MONITORION N-QUBIT GST TESTS
    #print("DEBUG TIME: dpr_cache(Np=%d, dim=%d, cachesize=%d, treesize=%d, napplies=%d) in %gs" %
    #      (calc.Np, calc.dim, cacheSize, len(evalTree), evalTree.get_num_applies(), _time.time()-tStart)) #DEBUG

    return dcache
#HERE2


# Helper functions
cdef PolyRep_from_allocd_PolyCRep(PolyCRep* crep):
    cdef PolyRep ret = PolyRep.__new__(PolyRep) # doesn't call __init__
    ret.c_poly = crep
    return ret

cdef vector[vector[SVTermCRep_ptr]] sv_extract_cterms(python_termrep_lists, INT max_order):
    cdef vector[vector[SVTermCRep_ptr]] ret = vector[vector[SVTermCRep_ptr]](max_order+1)
    cdef vector[SVTermCRep*] vec_of_terms
    for order,termreps in enumerate(python_termrep_lists): # maxorder+1 lists
        vec_of_terms = vector[SVTermCRep_ptr](len(termreps))
        for i,termrep in enumerate(termreps):
            vec_of_terms[i] = (<SVTermRep?>termrep).c_term
        ret[order] = vec_of_terms
    return ret


def SV_prs_as_polys(calc, rholabel, elabels, circuit, comm=None, memLimit=None, fastmode=True):

    # Create gatelable -> int mapping to be used throughout
    distinct_gateLabels = sorted(set(circuit))
    glmap = { gl: i for i,gl in enumerate(distinct_gateLabels) }

    # Convert circuit to a vector of ints
    cdef INT i
    cdef vector[INT] cgatestring
    for gl in circuit:
        cgatestring.push_back(<INT>glmap[gl])

    cdef INT mpv = calc.Np # max_poly_vars
    cdef INT mpo = calc.max_order*2 #max_poly_order
    cdef INT vpi = calc.poly_vindices_per_int
    cdef INT order;
    cdef INT numEs = len(elabels)

    # Construct dict of gate term reps, then *convert* to c-reps, as this
    #  keeps alive the non-c-reps which keep the c-reps from being deallocated...
    op_term_reps = { glmap[glbl]: [ [t.torep(mpo,mpv,"gate") for t in calc.sos.get_operation(glbl).get_taylor_order_terms(order)]
                                      for order in range(calc.max_order+1) ]
                       for glbl in distinct_gateLabels }

    #Similar with rho_terms and E_terms
    rho_term_reps = [ [t.torep(mpo,mpv,"prep") for t in calc.sos.get_prep(rholabel).get_taylor_order_terms(order)]
                      for order in range(calc.max_order+1) ]

    E_term_reps = []
    E_indices = []
    for order in range(calc.max_order+1):
        cur_term_reps = [] # the term reps for *all* the effect vectors
        cur_indices = [] # the Evec-index corresponding to each term rep
        for i,elbl in enumerate(elabels):
            term_reps = [t.torep(mpo,mpv,"effect") for t in calc.sos.get_effect(elbl).get_taylor_order_terms(order) ]
            cur_term_reps.extend( term_reps )
            cur_indices.extend( [i]*len(term_reps) )
        E_term_reps.append( cur_term_reps )
        E_indices.append( cur_indices )


    #convert to c-reps
    cdef INT gi
    cdef vector[vector[SVTermCRep_ptr]] rho_term_creps = sv_extract_cterms(rho_term_reps,calc.max_order)
    cdef vector[vector[SVTermCRep_ptr]] E_term_creps = sv_extract_cterms(E_term_reps,calc.max_order)
    cdef unordered_map[INT, vector[vector[SVTermCRep_ptr]]] gate_term_creps
    for gi,termrep_lists in op_term_reps.items():
        gate_term_creps[gi] = sv_extract_cterms(termrep_lists,calc.max_order)

    E_cindices = vector[vector[INT]](<INT>len(E_indices))
    for ii,inds in enumerate(E_indices):
        E_cindices[ii] = vector[INT](<INT>len(inds))
        for jj,indx in enumerate(inds):
            E_cindices[ii][jj] = <INT>indx

    #Note: term calculator "dim" is the full density matrix dim
    stateDim = int(round(np.sqrt(calc.dim)))

    #Call C-only function (which operates with C-representations only)
    cdef vector[PolyCRep*] polys = sv_prs_as_polys(
        cgatestring, rho_term_creps, gate_term_creps, E_term_creps,
        E_cindices, numEs, calc.max_order, mpo, mpv, vpi, stateDim, <bool>fastmode)

    return [ PolyRep_from_allocd_PolyCRep(polys[i]) for i in range(<INT>polys.size()) ]


cdef vector[PolyCRep*] sv_prs_as_polys(
    vector[INT]& circuit, vector[vector[SVTermCRep_ptr]] rho_term_reps,
    unordered_map[INT, vector[vector[SVTermCRep_ptr]]] op_term_reps,
    vector[vector[SVTermCRep_ptr]] E_term_reps, vector[vector[INT]] E_term_indices,
    INT numEs, INT max_order, INT max_poly_order, INT max_poly_vars, INT vindices_per_int, INT dim, bool fastmode):

    #NOTE: circuit and gate_terms use *integers* as operation labels, not Label objects, to speed
    # lookups and avoid weird string conversion stuff with Cython

    cdef INT N = len(circuit)
    cdef INT* p = <INT*>malloc((N+2) * sizeof(INT))
    cdef INT i,j,k,order,nTerms
    cdef INT gn

    cdef sv_innerloopfn_ptr innerloop_fn;
    if fastmode:
        innerloop_fn = sv_pr_as_poly_innerloop_savepartials
    else:
        innerloop_fn = sv_pr_as_poly_innerloop

    #extract raw data from gate_terms dictionary-of-lists for faster lookup
    #gate_term_prefactors = np.empty( (nOperations,max_order+1,dim,dim)
    #cdef unordered_map[INT, vector[vector[unordered_map[INT, complex]]]] gate_term_coeffs
    #cdef vector[vector[unordered_map[INT, complex]]] rho_term_coeffs
    #cdef vector[vector[unordered_map[INT, complex]]] E_term_coeffs
    #cdef vector[vector[INT]] E_indices

    cdef vector[INT]* Einds
    cdef vector[vector_SVTermCRep_ptr_ptr] factor_lists

    assert(max_order <= 2) # only support this partitioning below (so far)

    cdef vector[PolyCRep_ptr] prps = vector[PolyCRep_ptr](numEs)
    for i in range(numEs):
        prps[i] = new PolyCRep(unordered_map[PolyVarsIndex,complex](),max_poly_order, max_poly_vars, vindices_per_int)
        # create empty polys - maybe overload constructor for this?
        # these PolyCReps are alloc'd here and returned - it is the job of the caller to
        #  free them (or assign them to new PolyRep wrapper objs)

    for order in range(max_order+1):
        #print("DB: pr_as_poly order=",order)

        #for p in partition_into(order, N):
        for i in range(N+2): p[i] = 0 # clear p
        factor_lists = vector[vector_SVTermCRep_ptr_ptr](N+2)

        if order == 0:
            #inner loop(p)
            #factor_lists = [ gate_terms[glbl][pi] for glbl,pi in zip(circuit,p) ]
            factor_lists[0] = &rho_term_reps[p[0]]
            for k in range(N):
                gn = circuit[k]
                factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
                #if factor_lists[k+1].size() == 0: continue # WHAT???
            factor_lists[N+1] = &E_term_reps[p[N+1]]
            Einds = &E_term_indices[p[N+1]]

            #print("Part0 ",p)
            innerloop_fn(factor_lists,Einds,&prps,dim) #, prps_chk)


        elif order == 1:
            for i in range(N+2):
                p[i] = 1
                #inner loop(p)
                factor_lists[0] = &rho_term_reps[p[0]]
                for k in range(N):
                    gn = circuit[k]
                    factor_lists[k+1] = &op_term_reps[gn][p[k+1]]
                    #if len(factor_lists[k+1]) == 0: continue #WHAT???
                factor_lists[N+1] = &E_term_reps[p[N+1]]
                Einds = &E_term_indices[p[N+1]]

                #print "DB: Order1 "
                innerloop_fn(factor_lists,Einds,&prps,dim) #, prps_chk)
                p[i] = 0

        elif order == 2:
            for i in range(N+2):
                p[i] = 2
                #inner loop(p)
                factor_lists[0] = &rho_term_reps[p[0]]
                for k in range(N):
                    gn = circuit[k]
                    factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
                    #if len(factor_lists[k+1]) == 0: continue # WHAT???
                factor_lists[N+1] = &E_term_reps[p[N+1]]
                Einds = &E_term_indices[p[N+1]]

                innerloop_fn(factor_lists,Einds,&prps,dim) #, prps_chk)
                p[i] = 0

            for i in range(N+2):
                p[i] = 1
                for j in range(i+1,N+2):
                    p[j] = 1
                    #inner loop(p)
                    factor_lists[0] = &rho_term_reps[p[0]]
                    for k in range(N):
                        gn = circuit[k]
                        factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
                        #if len(factor_lists[k+1]) == 0: continue #WHAT???
                    factor_lists[N+1] = &E_term_reps[p[N+1]]
                    Einds = &E_term_indices[p[N+1]]

                    innerloop_fn(factor_lists,Einds,&prps,dim) #, prps_chk)
                    p[j] = 0
                p[i] = 0
        else:
            assert(False) # order > 2 not implemented yet...

    free(p)
    return prps



cdef void sv_pr_as_poly_innerloop(vector[vector_SVTermCRep_ptr_ptr] factor_lists, vector[INT]* Einds,
                                  vector[PolyCRep*]* prps, INT dim): #, prps_chk):
    #print("DB partition = ","listlens = ",[len(fl) for fl in factor_lists])

    cdef INT i,j,Ei
    cdef double complex scale, val, newval, pLeft, pRight, p

    cdef SVTermCRep* factor

    cdef INT nFactorLists = factor_lists.size() # may need to recompute this after fast-mode
    cdef INT* factorListLens = <INT*>malloc(nFactorLists * sizeof(INT))
    cdef INT last_index = nFactorLists-1

    for i in range(nFactorLists):
        factorListLens[i] = factor_lists[i].size()
        if factorListLens[i] == 0:
            free(factorListLens)
            return # nothing to loop over! - (exit before we allocate more)

    cdef PolyCRep coeff
    cdef PolyCRep result

    cdef SVStateCRep *prop1 = new SVStateCRep(dim)
    cdef SVStateCRep *prop2 = new SVStateCRep(dim)
    cdef SVStateCRep *tprop
    cdef SVEffectCRep* EVec

    cdef INT* b = <INT*>malloc(nFactorLists * sizeof(INT))
    for i in range(nFactorLists): b[i] = 0

    assert(nFactorLists > 0), "Number of factor lists must be > 0!"

    #for factors in _itertools.product(*factor_lists):
    while(True):
        # In this loop, b holds "current" indices into factor_lists
        factor = deref(factor_lists[0])[b[0]] # the last factor (an Evec)
        coeff = deref(factor._coeff) # an unordered_map (copies to new "coeff" variable)

        for i in range(1,nFactorLists):
            coeff = coeff.mult( deref(deref(factor_lists[i])[b[i]]._coeff) )

        #pLeft / "pre" sim
        factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
        prop1.copy_from(factor._pre_state)
        for j in range(<INT>factor._pre_ops.size()):
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop
        for i in range(1,last_index):
            factor = deref(factor_lists[i])[b[i]]
            for j in range(<INT>factor._pre_ops.size()):
                factor._pre_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)

	# can't propagate effects, so effect's post_ops are constructed to act on *state*
        EVec = factor._post_effect
        for j in range(<INT>factor._post_ops.size()):
            rhoVec = factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        pLeft = EVec.amplitude(prop1)

        #pRight / "post" sim
        factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
        prop1.copy_from(factor._post_state)
        for j in range(<INT>factor._post_ops.size()):
            factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        for i in range(1,last_index):
            factor = deref(factor_lists[i])[b[i]]
            for j in range(<INT>factor._post_ops.size()):
                factor._post_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)

        EVec = factor._pre_effect
        for j in range(<INT>factor._pre_ops.size()):
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        pRight = EVec.amplitude(prop1).conjugate()


        #Add result to appropriate poly
        result = coeff  # use a reference?
        result.scale(pLeft * pRight)
        final_factor_indx = b[last_index]
        Ei = deref(Einds)[final_factor_indx] #final "factor" index == E-vector index
        deref(prps)[Ei].add_inplace(result)

        #increment b ~ itertools.product & update vec_index_noop = np.dot(self.multipliers, b)
        for i in range(nFactorLists-1,-1,-1):
            if b[i]+1 < factorListLens[i]:
                b[i] += 1
                break
            else:
                b[i] = 0
        else:
            break # can't increment anything - break while(True) loop

    #Clenaup: free allocated memory
    del prop1
    del prop2
    free(factorListLens)
    free(b)
    return


cdef void sv_pr_as_poly_innerloop_savepartials(vector[vector_SVTermCRep_ptr_ptr] factor_lists,
                                               vector[INT]* Einds, vector[PolyCRep*]* prps, INT dim): #, prps_chk):
    #print("DB partition = ","listlens = ",[len(fl) for fl in factor_lists])

    cdef INT i,j,Ei
    cdef double complex scale, val, newval, pLeft, pRight, p

    cdef INT incd
    cdef SVTermCRep* factor

    cdef INT nFactorLists = factor_lists.size() # may need to recompute this after fast-mode
    cdef INT* factorListLens = <INT*>malloc(nFactorLists * sizeof(INT))
    cdef INT last_index = nFactorLists-1

    for i in range(nFactorLists):
        factorListLens[i] = factor_lists[i].size()
        if factorListLens[i] == 0:
            free(factorListLens)
            return # nothing to loop over! (exit before we allocate anything else)

    cdef PolyCRep coeff
    cdef PolyCRep result

    #fast mode
    cdef vector[SVStateCRep*] leftSaved = vector[SVStateCRep_ptr](nFactorLists-1)  # saved[i] is state after i-th
    cdef vector[SVStateCRep*] rightSaved = vector[SVStateCRep_ptr](nFactorLists-1) # factor has been applied
    cdef vector[PolyCRep] coeffSaved = vector[PolyCRep](nFactorLists-1)
    cdef SVStateCRep *shelved = new SVStateCRep(dim)
    cdef SVStateCRep *prop2 = new SVStateCRep(dim) # prop2 is always a temporary allocated state not owned by anything else
    cdef SVStateCRep *prop1
    cdef SVStateCRep *tprop
    cdef SVEffectCRep* EVec

    cdef INT* b = <INT*>malloc(nFactorLists * sizeof(INT))
    for i in range(nFactorLists): b[i] = 0
    assert(nFactorLists > 0), "Number of factor lists must be > 0!"

    incd = 0

    #Fill saved arrays with allocated states
    for i in range(nFactorLists-1):
        leftSaved[i] = new SVStateCRep(dim)
        rightSaved[i] = new SVStateCRep(dim)

    #for factors in _itertools.product(*factor_lists):
    #for incd,fi in incd_product(*[range(len(l)) for l in factor_lists]):
    while(True):
        # In this loop, b holds "current" indices into factor_lists
        #print "DB: iter-product BEGIN"

        if incd == 0: # need to re-evaluate rho vector
            #print "DB: re-eval at incd=0"
            factor = deref(factor_lists[0])[b[0]]

            #print "DB: re-eval left"
            prop1 = leftSaved[0] # the final destination (prop2 is already alloc'd)
            prop1.copy_from(factor._pre_state)
            for j in range(<INT>factor._pre_ops.size()):
                #print "DB: re-eval left item"
                factor._pre_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
            rhoVecL = prop1
            leftSaved[0] = prop1 # final state -> saved
            # (prop2 == the other allocated state)

            #print "DB: re-eval right"
            prop1 = rightSaved[0] # the final destination (prop2 is already alloc'd)
            prop1.copy_from(factor._post_state)
            for j in range(<INT>factor._post_ops.size()):
                #print "DB: re-eval right item"
                factor._post_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
            rhoVecR = prop1
            rightSaved[0] = prop1 # final state -> saved
            # (prop2 == the other allocated state)

            #print "DB: re-eval coeff"
            coeff = deref(factor._coeff)
            coeffSaved[0] = coeff
            incd += 1
        else:
            #print "DB: init from incd"
            rhoVecL = leftSaved[incd-1]
            rhoVecR = rightSaved[incd-1]
            coeff = coeffSaved[incd-1]

        # propagate left and right states, saving as we go
        for i in range(incd,last_index):
            #print "DB: propagate left begin"
            factor = deref(factor_lists[i])[b[i]]
            prop1 = leftSaved[i] # destination
            prop1.copy_from(rhoVecL) #starting state
            for j in range(<INT>factor._pre_ops.size()):
                #print "DB: propagate left item"
                factor._pre_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop
            rhoVecL = prop1
            leftSaved[i] = prop1
            # (prop2 == the other allocated state)

            #print "DB: propagate right begin"
            prop1 = rightSaved[i] # destination
            prop1.copy_from(rhoVecR) #starting state
            for j in range(<INT>factor._post_ops.size()):
                #print "DB: propagate right item"
                factor._post_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop
            rhoVecR = prop1
            rightSaved[i] = prop1
            # (prop2 == the other allocated state)

            #print "DB: propagate coeff mult"
            coeff = coeff.mult(deref(factor._coeff)) # copy a PolyCRep
            coeffSaved[i] = coeff

        # for the last index, no need to save, and need to construct
        # and apply effect vector
        prop1 = shelved # so now prop1 (and prop2) are alloc'd states

        #print "DB: left ampl"
        factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)
        EVec = factor._post_effect
        prop1.copy_from(rhoVecL) # initial state (prop2 already alloc'd)
        for j in range(<INT>factor._post_ops.size()):
            factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop
        pLeft = EVec.amplitude(prop1) # output in prop1, so this is final amplitude

        #print "DB: right ampl"
        EVec = factor._pre_effect
        prop1.copy_from(rhoVecR)
        for j in range(<INT>factor._pre_ops.size()):
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop
        pRight = EVec.amplitude(prop1).conjugate()

        shelved = prop1 # return prop1 to the "shelf" since we'll use prop1 for other things next

        #print "DB: final block"
        #print "DB running coeff = ",dict(coeff._coeffs)
        #print "DB factor coeff = ",dict(factor._coeff._coeffs)
        result = coeff.mult(deref(factor._coeff))
        #print "DB result = ",dict(result._coeffs)
        result.scale(pLeft * pRight)
        final_factor_indx = b[last_index]
        Ei = deref(Einds)[final_factor_indx] #final "factor" index == E-vector index
        deref(prps)[Ei].add_inplace(result)
        #print "DB prps[",INT(Ei),"] = ",dict(deref(prps)[Ei]._coeffs)

        #assert(debug < 100) #DEBUG
        #print "DB: end product loop"

        #increment b ~ itertools.product & update vec_index_noop = np.dot(self.multipliers, b)
        for i in range(nFactorLists-1,-1,-1):
            if b[i]+1 < factorListLens[i]:
                b[i] += 1; incd = i
                break
            else:
                b[i] = 0
        else:
            break # can't increment anything - break while(True) loop

    #Cleanup: free allocated memory
    for i in range(nFactorLists-1):
        del leftSaved[i]
        del rightSaved[i]
    del prop2
    del shelved
    free(factorListLens)
    free(b)
    return


# State-vector pruned-poly-term calcs -------------------------

def SV_prs_as_pruned_polys(calc, rholabel, elabels, circuit, repcache, opcache, comm=None, memLimit=None, fastmode=True, pathmagnitude_gap=0.0, min_term_mag=0.01,
                           current_threshold=None):

    #t0 = pytime.time()
    #if debug is not None:
    #    debug['tstartup'] += pytime.time()-t0
    #    t0 = pytime.time()

    # Create gatelable -> int mapping to be used throughout
    distinct_gateLabels = sorted(set(circuit))
    glmap = { gl: i for i,gl in enumerate(distinct_gateLabels) }
    t0 = pytime.time()

    # Convert circuit to a vector of ints
    cdef INT i, j
    cdef INT mpv = calc.Np # max_poly_vars
    cdef INT mpo = calc.max_order*2 #max_poly_order
    cdef INT vpi = calc.poly_vindices_per_int
    cdef vector[INT] cgatestring
    for gl in circuit:
        cgatestring.push_back(<INT>glmap[gl])

    cdef double order_base = 0.1 # default for now - TODO: make this a calc param like max_order?
    cdef INT order
    cdef INT numEs = len(elabels)

    cdef RepCacheEl repcel;
    cdef vector[SVTermCRep_ptr] treps;
    #cdef DCOMPLEX* coeffs;
    #cdef np.ndarray coeffs_array;
    cdef SVTermRep rep;

    # Construct dict of gate term reps, then *convert* to c-reps, as this
    #  keeps alive the non-c-reps which keep the c-reps from being deallocated...
    cdef unordered_map[INT, vector[SVTermCRep_ptr] ] op_term_reps = unordered_map[INT, vector[SVTermCRep_ptr] ]();
    cdef unordered_map[INT, vector[INT] ] op_foat_indices = unordered_map[INT, vector[INT] ]();
    for glbl in distinct_gateLabels:
        if glbl in repcache:
            repcel = <RepCacheEl?>repcache[glbl]
            op_term_reps[ glmap[glbl] ] = repcel.reps
            op_foat_indices[ glmap[glbl] ] = repcel.foat_indices
        else:
            repcel = RepCacheEl()
            if glbl in opcache:
                op = opcache[glbl]
                db_made_op = False
            else:
                op = calc.sos.get_operation(glbl)
                opcache[glbl] = op
                db_made_op = True

            hmterms, foat_indices = op.get_highmagnitude_terms(
                min_term_mag, max_taylor_order=calc.max_order)

            #DEBUG CHECK TERM MAGNITUDES make sense
            #chk_tot_mag = sum([t.magnitude for t in hmterms])
            #chk_tot_mag2 = op.get_total_term_magnitude()
            #if chk_tot_mag > chk_tot_mag2+1e-5: # give a tolerance here
            #    print "Warning: highmag terms for ",str(glbl),": ",len(hmterms)," have total mag = ",chk_tot_mag," but max should be ",chk_tot_mag2,"!!"
            #else:
            #    print "Highmag terms recomputed (OK) - made op = ", db_made_op

            for t in hmterms:
                rep = (<SVTermRep?>t.torep(mpo,mpv,"gate"))
                repcel.pyterm_references.append(rep)
                repcel.reps.push_back( rep.c_term )

            for i in foat_indices:
                repcel.foat_indices.push_back(<INT?>i)

            op_term_reps[ glmap[glbl] ] = repcel.reps
            op_foat_indices[ glmap[glbl] ] = repcel.foat_indices
            repcache[glbl] = repcel

    #Similar with rho_terms and E_terms
    cdef vector[SVTermCRep_ptr] rho_term_reps;
    cdef vector[INT] rho_foat_indices;
    if rholabel in repcache:
        repcel = repcache[rholabel]
        rho_term_reps = repcel.reps
        rho_foat_indices = repcel.foat_indices
    else:
        repcel = RepCacheEl()
        hmterms, foat_indices = calc.sos.get_prep(rholabel).get_highmagnitude_terms(
            min_term_mag, max_taylor_order=calc.max_order)

        for t in hmterms:
            rep = (<SVTermRep?>t.torep(mpo,mpv,"prep"))
            repcel.pyterm_references.append(rep)
            repcel.reps.push_back( rep.c_term )

        for i in foat_indices:
            repcel.foat_indices.push_back(<INT?>i)

        rho_term_reps = repcel.reps
        rho_foat_indices = repcel.foat_indices
        repcache[rholabel] = repcel


    cdef vector[SVTermCRep_ptr] E_term_reps = vector[SVTermCRep_ptr](0);
    cdef vector[INT] E_foat_indices = vector[INT](0);
    cdef vector[INT] E_indices = vector[INT](0);
    cdef SVTermCRep_ptr cterm;

    elabels = tuple(elabels) # so hashable
    if elabels in repcache:
        repcel = <RepCacheEl?>repcache[elabels]
        E_term_reps = repcel.reps
        E_indices = repcel.E_indices
        E_foat_indices = repcel.foat_indices
    else:
        repcel = RepCacheEl()
        E_term_indices_and_reps = []
        for i,elbl in enumerate(elabels):
            hmterms, foat_indices = calc.sos.get_effect(elbl).get_highmagnitude_terms(
                min_term_mag, max_taylor_order=calc.max_order)
            E_term_indices_and_reps.extend(
                [ (i,t,t.magnitude,1 if (j in foat_indices) else 0) for j,t in enumerate(hmterms) ] )

        #Sort all terms by magnitude
        E_term_indices_and_reps.sort(key=lambda x: x[2], reverse=True)
        for j,(i,t,_,is_foat) in enumerate(E_term_indices_and_reps):
            rep = (<SVTermRep?>t.torep(mpo,mpv,"effect"))
            repcel.pyterm_references.append(rep)
            repcel.reps.push_back( rep.c_term )
            repcel.E_indices.push_back(<INT?>i)
            if(is_foat): repcel.foat_indices.push_back(<INT>j)

        E_term_reps = repcel.reps
        E_indices = repcel.E_indices
        E_foat_indices = repcel.foat_indices
        repcache[elabels] = repcel

    cdef double max_partial_sopm = calc.sos.get_prep(rholabel).get_total_term_magnitude()
    cdef vector[double] target_sum_of_pathmags = vector[double](numEs)
    for glbl in circuit:
        op = opcache.get(glbl, calc.sos.get_operation(glbl))
        max_partial_sopm *= op.get_total_term_magnitude()
    for i,elbl in enumerate(elabels):
        target_sum_of_pathmags[i] = max_partial_sopm * calc.sos.get_effect(elbl).get_total_term_magnitude() - pathmagnitude_gap

    #Note: term calculator "dim" is the full density matrix dim
    stateDim = int(round(np.sqrt(calc.dim)))

    #Call C-only function (which operates with C-representations only)
    cdef vector[float] returnvec = vector[float](4)
    cdef vector[PolyCRep*] polys = sv_prs_pruned(
        cgatestring, rho_term_reps, op_term_reps, E_term_reps,
        rho_foat_indices, op_foat_indices, E_foat_indices, E_indices,
        numEs, calc.max_order, stateDim, <bool>fastmode, pathmagnitude_gap, min_term_mag,
        current_threshold, target_sum_of_pathmags, mpo, mpv, vpi, returnvec)

    if returnvec[2]+pathmagnitude_gap+1e-5 < returnvec[3]: # index 2 = Target, index 3 = Achieved
        print "Warning: Achieved sum(path mags) exceeds max by ", returnvec[3]-(returnvec[2]+pathmagnitude_gap),"!!!"

    return [ PolyRep_from_allocd_PolyCRep(polys[i]) for i in range(<INT>polys.size()) ], int(returnvec[0]), returnvec[1], returnvec[2], returnvec[3]


cdef vector[PolyCRep*] sv_prs_pruned(
    vector[INT]& circuit,
    vector[SVTermCRep_ptr] rho_term_reps, unordered_map[INT, vector[SVTermCRep_ptr]] op_term_reps, vector[SVTermCRep_ptr] E_term_reps,
    vector[INT] rho_foat_indices, unordered_map[INT,vector[INT]] op_foat_indices, vector[INT] E_foat_indices, vector[INT] E_indices,
    INT numEs, INT max_order, INT dim, bool fastmode, double pathmagnitude_gap, double min_term_mag, double current_threshold,
    vector[double]& target_sum_of_pathmags, INT max_poly_order, INT max_poly_vars, INT vindices_per_int, vector[float]& returnvec):

    #NOTE: circuit and gate_terms use *integers* as operation labels, not Label objects, to speed
    # lookups and avoid weird string conversion stuff with Cython

    cdef INT N = circuit.size()
    cdef INT nFactorLists = N+2
    #cdef INT n = N+2 # number of factor lists
    #cdef INT* p = <INT*>malloc((N+2) * sizeof(INT))
    cdef INT i #,j,k #,order,nTerms
    #cdef INT gn

    cdef INT t0 = time.clock()
    #cdef INT t, nPaths; #for below

    cdef vector[vector_SVTermCRep_ptr_ptr] factor_lists = vector[vector_SVTermCRep_ptr_ptr](nFactorLists)
    cdef vector[vector_INT_ptr] foat_indices_per_op = vector[vector_INT_ptr](nFactorLists)
    cdef vector[INT] nops = vector[INT](nFactorLists)
    cdef vector[INT] b = vector[INT](nFactorLists)

    factor_lists[0] = &rho_term_reps
    foat_indices_per_op[0] = &rho_foat_indices
    for i in range(N):
        factor_lists[i+1] = &op_term_reps[circuit[i]]
        foat_indices_per_op[i+1] = &op_foat_indices[circuit[i]]
    factor_lists[N+1] = &E_term_reps
    foat_indices_per_op[N+1] = &E_foat_indices

    #print "CHECK: ",N+2, " op lists"
    #running=1.0
    #for i in range(N+1):
    #    nTerms = deref(factor_lists[i]).size()
    #    mags = [ deref(factor_lists[i])[j]._magnitude for j in range(nTerms) ]
    #    running *= sum(mags)
    #    print i,": ",nTerms,"terms: "," sum=",sum(mags)," running=",running
    #nETerms = deref(factor_lists[N+1]).size()
    #mags0 = [ deref(factor_lists[N+1])[j]._magnitude for j in range(nETerms) if E_indices[j] == 0]
    #mags1 = [ deref(factor_lists[N+1])[j]._magnitude for j in range(nETerms) if E_indices[j] == 1]
    #print "Final check E0: * ",sum(mags0)," = ",running*sum(mags0)
    #print "Final check E1: * ",sum(mags1)," = ",running*sum(mags1)


    cdef vector[double] achieved_sum_of_pathmags = vector[double](numEs)
    cdef vector[INT] npaths = vector[INT](numEs)
    cdef vector[PolyCRep_ptr] empty_prps = vector[PolyCRep_ptr](0)

    threshold = pathmagnitude_threshold(factor_lists, E_indices, numEs, target_sum_of_pathmags, foat_indices_per_op,
                                        current_threshold, pathmagnitude_gap/100.0, achieved_sum_of_pathmags, npaths)
    #DEBUG
    #print("FOAT: ")
    #for i in range(nFactorLists):
    #    print(deref(foat_indices_per_op[i]))
    #print("Threshold = ",threshold," Paths=",npaths)

    #Construct all our return values (HACK - return these as a vector of floats)
    returnvec[0] = 0.0
    returnvec[1] = threshold
    returnvec[2] = 0.0
    returnvec[3] = 0.0
    for i in range(numEs):
        returnvec[0] += npaths[i]
        returnvec[2] += target_sum_of_pathmags[i]
        returnvec[3] += achieved_sum_of_pathmags[i]

    #print("Threshold = ",threshold, "(current = ",current_threshold,")")
    if current_threshold >= 0 and threshold >= current_threshold: # then just keep existing (cached) polys
        return empty_prps #(empty)

    #Traverse paths up to threshold, running "innerloop" as we go (~add_path)
    cdef vector[PolyCRep_ptr] prps = vector[PolyCRep_ptr](numEs)
    for i in range(numEs):
        prps[i] = new PolyCRep(unordered_map[PolyVarsIndex,complex](),max_poly_order, max_poly_vars, vindices_per_int)
        # create empty polys - maybe overload constructor for this?
        # these PolyCReps are alloc'd here and returned - it is the job of the caller to
        #  free them (or assign them to new PolyRep wrapper objs)

    cdef double log_thres = log10(threshold)
    cdef double current_mag = 1.0
    cdef double current_logmag = 0.0
    for i in range(nFactorLists):
        nops[i] = factor_lists[i].size()
        b[i] = 0

    ## fn_visitpath(b, current_mag, 0) # visit root (all 0s) path
    cdef sv_addpathfn_ptr addpath_fn;
    cdef vector[SVStateCRep*] leftSaved = vector[SVStateCRep_ptr](nFactorLists-1)  # saved[i] is state after i-th
    cdef vector[SVStateCRep*] rightSaved = vector[SVStateCRep_ptr](nFactorLists-1) # factor has been applied
    cdef vector[PolyCRep] coeffSaved = vector[PolyCRep](nFactorLists-1)

    #Fill saved arrays with allocated states
    if fastmode:
        #fast mode
        addpath_fn = add_path_savepartials
        for i in range(nFactorLists-1):
            leftSaved[i] = new SVStateCRep(dim)
            rightSaved[i] = new SVStateCRep(dim)
    else:
        addpath_fn = add_path
        for i in range(nFactorLists-1):
            leftSaved[i] = NULL
            rightSaved[i] = NULL

    cdef SVStateCRep *prop1 = new SVStateCRep(dim)
    cdef SVStateCRep *prop2 = new SVStateCRep(dim)
    addpath_fn(&prps, b, 0, factor_lists, &prop1, &prop2, &E_indices, &leftSaved, &rightSaved, &coeffSaved)
    ## -------------------------------
    add_paths(addpath_fn, b, factor_lists, foat_indices_per_op, numEs, nops, E_indices, 0, log_thres, current_mag, current_logmag, 0,
              &prps, &prop1, &prop2, &leftSaved, &rightSaved, &coeffSaved)

    del prop1
    del prop2
    return prps


cdef void add_path(vector[PolyCRep*]* prps, vector[INT]& b, INT incd, vector[vector_SVTermCRep_ptr_ptr]& factor_lists,
                   SVStateCRep **pprop1, SVStateCRep **pprop2, vector[INT]* Einds,
                   vector[SVStateCRep*]* pleftSaved, vector[SVStateCRep*]* prightSaved, vector[PolyCRep]* pcoeffSaved):

    cdef PolyCRep coeff
    cdef PolyCRep result
    cdef double complex pLeft, pRight

    cdef INT i,j, Ei
    cdef SVTermCRep* factor
    cdef SVStateCRep *prop1 = deref(pprop1)
    cdef SVStateCRep *prop2 = deref(pprop2)
    cdef SVStateCRep *tprop
    cdef SVEffectCRep* EVec
    cdef SVStateCRep *rhoVec
    cdef INT nFactorLists = b.size()
    cdef INT last_index = nFactorLists-1
    # ** Assume prop1 and prop2 begin as allocated **

    # In this loop, b holds "current" indices into factor_lists
    factor = deref(factor_lists[0])[b[0]]
    coeff = deref(factor._coeff) # an unordered_map (copies to new "coeff" variable)

    for i in range(1,nFactorLists):
        coeff = coeff.mult( deref(deref(factor_lists[i])[b[i]]._coeff) )

    #pLeft / "pre" sim
    factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
    prop1.copy_from(factor._pre_state)
    for j in range(<INT>factor._pre_ops.size()):
        factor._pre_ops[j].acton(prop1,prop2)
        tprop = prop1; prop1 = prop2; prop2 = tprop
    for i in range(1,last_index):
        factor = deref(factor_lists[i])[b[i]]
        for j in range(<INT>factor._pre_ops.size()):
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
    factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)

	# can't propagate effects, so effect's post_ops are constructed to act on *state*
    EVec = factor._post_effect
    for j in range(<INT>factor._post_ops.size()):
        rhoVec = factor._post_ops[j].acton(prop1,prop2)
        tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
    pLeft = EVec.amplitude(prop1)

    #pRight / "post" sim
    factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
    prop1.copy_from(factor._post_state)
    for j in range(<INT>factor._post_ops.size()):
        factor._post_ops[j].acton(prop1,prop2)
        tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
    for i in range(1,last_index):
        factor = deref(factor_lists[i])[b[i]]
        for j in range(<INT>factor._post_ops.size()):
            factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
    factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)

    EVec = factor._pre_effect
    for j in range(<INT>factor._pre_ops.size()):
        factor._pre_ops[j].acton(prop1,prop2)
        tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
    pRight = EVec.amplitude(prop1).conjugate()


    #Add result to appropriate poly
    result = coeff  # use a reference?
    result.scale(pLeft * pRight)
    Ei = deref(Einds)[ b[last_index] ] #final "factor" index == E-vector index
    #print("Ei = ",Ei," size = ",deref(prps).size())
    #print("result = ")
    #for x in result._coeffs:
    #    print x.first._parts, x.second
    #print("prps = ")
    #for x in deref(prps)[Ei]._coeffs:
    #    print x.first._parts, x.second
    deref(prps)[Ei].add_inplace(result)

    #Update the slots held by prop1 and prop2, which still have allocated states (though really no need?)
    pprop1[0] = prop1
    pprop2[0] = prop2


cdef void add_path_savepartials(vector[PolyCRep*]* prps, vector[INT]& b, INT incd, vector[vector_SVTermCRep_ptr_ptr]& factor_lists,
                                SVStateCRep** pprop1, SVStateCRep** pprop2, vector[INT]* Einds,
                                vector[SVStateCRep*]* pleftSaved, vector[SVStateCRep*]* prightSaved, vector[PolyCRep]* pcoeffSaved):

    cdef PolyCRep coeff
    cdef PolyCRep result
    cdef double complex pLeft, pRight

    cdef INT i,j, Ei
    cdef SVTermCRep* factor
    cdef SVStateCRep *prop1 = deref(pprop1)
    cdef SVStateCRep *prop2 = deref(pprop2)
    cdef SVStateCRep *tprop
    cdef SVStateCRep *shelved = prop1
    cdef SVEffectCRep* EVec
    cdef SVStateCRep *rhoVec
    cdef INT nFactorLists = b.size()
    cdef INT last_index = nFactorLists-1
    # ** Assume shelved and prop2 begin as allocated **

    if incd == 0: # need to re-evaluate rho vector
        #print "DB: re-eval at incd=0"
        factor = deref(factor_lists[0])[b[0]]

        #print "DB: re-eval left"
        prop1 = deref(pleftSaved)[0] # the final destination (prop2 is already alloc'd)
        prop1.copy_from(factor._pre_state)
        for j in range(<INT>factor._pre_ops.size()):
            #print "DB: re-eval left item"
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
        rhoVecL = prop1
        deref(pleftSaved)[0] = prop1 # final state -> saved
        # (prop2 == the other allocated state)

        #print "DB: re-eval right"
        prop1 = deref(prightSaved)[0] # the final destination (prop2 is already alloc'd)
        prop1.copy_from(factor._post_state)
        for j in range(<INT>factor._post_ops.size()):
            #print "DB: re-eval right item"
            factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
        rhoVecR = prop1
        deref(prightSaved)[0] = prop1 # final state -> saved
        # (prop2 == the other allocated state)

        #print "DB: re-eval coeff"
        coeff = deref(factor._coeff)
        deref(pcoeffSaved)[0] = coeff
        incd += 1
    else:
        #print "DB: init from incd"
        rhoVecL = deref(pleftSaved)[incd-1]
        rhoVecR = deref(prightSaved)[incd-1]
        coeff = deref(pcoeffSaved)[incd-1]

    # propagate left and right states, saving as we go
    for i in range(incd,last_index):
        #print "DB: propagate left begin"
        factor = deref(factor_lists[i])[b[i]]
        prop1 = deref(pleftSaved)[i] # destination
        prop1.copy_from(rhoVecL) #starting state
        for j in range(<INT>factor._pre_ops.size()):
            #print "DB: propagate left item"
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop
        rhoVecL = prop1
        deref(pleftSaved)[i] = prop1
        # (prop2 == the other allocated state)

        #print "DB: propagate right begin"
        prop1 = deref(prightSaved)[i] # destination
        prop1.copy_from(rhoVecR) #starting state
        for j in range(<INT>factor._post_ops.size()):
            #print "DB: propagate right item"
            factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop
        rhoVecR = prop1
        deref(prightSaved)[i] = prop1
        # (prop2 == the other allocated state)

        #print "DB: propagate coeff mult"
        coeff = coeff.mult(deref(factor._coeff)) # copy a PolyCRep
        deref(pcoeffSaved)[i] = coeff

    # for the last index, no need to save, and need to construct
    # and apply effect vector
    prop1 = shelved # so now prop1 (and prop2) are alloc'd states

    #print "DB: left ampl"
    factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)
    EVec = factor._post_effect
    prop1.copy_from(rhoVecL) # initial state (prop2 already alloc'd)
    for j in range(<INT>factor._post_ops.size()):
        factor._post_ops[j].acton(prop1,prop2)
        tprop = prop1; prop1 = prop2; prop2 = tprop
    pLeft = EVec.amplitude(prop1) # output in prop1, so this is final amplitude

    #print "DB: right ampl"
    EVec = factor._pre_effect
    prop1.copy_from(rhoVecR)
    for j in range(<INT>factor._pre_ops.size()):
        factor._pre_ops[j].acton(prop1,prop2)
        tprop = prop1; prop1 = prop2; prop2 = tprop
    pRight = EVec.amplitude(prop1).conjugate()

    shelved = prop1 # return prop1 to the "shelf" since we'll use prop1 for other things next

    #print "DB: final block"
    #print "DB running coeff = ",dict(coeff._coeffs)
    #print "DB factor coeff = ",dict(factor._coeff._coeffs)
    result = coeff.mult(deref(factor._coeff))
    #print "DB result = ",dict(result._coeffs)
    result.scale(pLeft * pRight)
    Ei = deref(Einds)[b[last_index]] #final "factor" index == E-vector index
    deref(prps)[Ei].add_inplace(result)

    #Update the slots held by prop1 and prop2, which still have allocated states
    pprop1[0] = prop1 # b/c can't deref(pprop1) = prop1 isn't allowed (?)
    pprop2[0] = prop2 # b/c can't deref(pprop2) = prop1 isn't allowed (?)
    #print "DB prps[",INT(Ei),"] = ",dict(deref(prps)[Ei]._coeffs)


cdef void add_paths(sv_addpathfn_ptr addpath_fn, vector[INT]& b, vector[vector_SVTermCRep_ptr_ptr] oprep_lists,
                    vector[vector_INT_ptr] foat_indices_per_op, INT num_elabels,
                    vector[INT]& nops, vector[INT]& E_indices, INT incd, double log_thres,
                    double current_mag, double current_logmag, INT order,
                    vector[PolyCRep*]* prps, SVStateCRep **pprop1, SVStateCRep **pprop2,
                    vector[SVStateCRep*]* pleftSaved, vector[SVStateCRep*]* prightSaved, vector[PolyCRep]* pcoeffSaved):
    """ first_order means only one b[i] is incremented, e.g. b == [0 1 0] or [4 0 0] """
    cdef INT i, j, k, orig_bi, orig_bn
    cdef INT n = b.size()
    cdef INT sub_order
    cdef double mag, mag2

    for i in range(n-1, incd-1, -1):
        if b[i]+1 == nops[i]: continue
        b[i] += 1

        if order == 0: # then incd doesn't matter b/c can inc anything to become 1st order
            sub_order = 1 if (i != n-1 or b[i] >= num_elabels) else 0
        elif order == 1:
            # we started with a first order term where incd was incremented, and now
            # we're incrementing something else
            sub_order = 1 if i == incd else 2 # signifies anything over 1st order where >1 column has be inc'd
        else:
            sub_order = order

        logmag = current_logmag + (deref(oprep_lists[i])[b[i]]._logmagnitude - deref(oprep_lists[i])[b[i]-1]._logmagnitude)
        if logmag >= log_thres:
            if deref(oprep_lists[i])[b[i]-1]._magnitude == 0:
                mag = 0
            else:
                mag = current_mag * (deref(oprep_lists[i])[b[i]]._magnitude / deref(oprep_lists[i])[b[i]-1]._magnitude)

            ## fn_visitpath(b, mag, i) ##
            addpath_fn(prps, b, i, oprep_lists, pprop1, pprop2, &E_indices, pleftSaved, prightSaved, pcoeffSaved)
            ## --------------------------

            add_paths(addpath_fn, b, oprep_lists, foat_indices_per_op, num_elabels, nops, E_indices,
                      i, log_thres, mag, logmag, sub_order, prps, pprop1, pprop2, pleftSaved, prightSaved, pcoeffSaved)
                #add any allowed paths beneath this one

        elif sub_order <= 1:
            #We've rejected term-index b[i] (in column i) because it's too small - the only reason
            # to accept b[i] or term indices higher than it is to include "foat" terms, so we now
            # iterate through any remaining foat indices for this column (we've accepted all lower
            # values of b[i], or we wouldn't be here).  Note that we just need to visit the path,
            # we don't need to traverse down, since we know the path magnitude is already too low.
            orig_bi = b[i]
            for j in deref(foat_indices_per_op[i]):
                if j >= orig_bi:
                    b[i] = j
                    mag = 0 if deref(oprep_lists[i])[orig_bi-1]._magnitude == 0 else \
                        current_mag * (deref(oprep_lists[i])[b[i]]._magnitude / deref(oprep_lists[i])[orig_bi-1]._magnitude)

                    ## fn_visitpath(b, mag, i) ##
                    addpath_fn(prps, b, i, oprep_lists, pprop1, pprop2, &E_indices, pleftSaved, prightSaved, pcoeffSaved)
                    ## --------------------------

                    if i != n-1:
                        # if we're not incrementing (from a zero-order term) the final index, then we
                        # need to to increment it until we hit num_elabels (*all* zero-th order paths)
                        orig_bn = b[n-1]
                        for k in range(1,num_elabels):
                            b[n-1] = k
                            mag2 = mag * (deref(oprep_lists[n-1])[b[n-1]]._magnitude / deref(oprep_lists[i])[orig_bn]._magnitude)

                            ## fn_visitpath(b, mag2, n-1) ##
                            addpath_fn(prps, b, n-1, oprep_lists, pprop1, pprop2, &E_indices, pleftSaved, prightSaved, pcoeffSaved)
                            ## --------------------------
                        b[n-1] = orig_bn
            b[i] = orig_bi
        b[i] -= 1 # so we don't have to copy b



cdef void count_paths(vector[INT]& b, vector[vector_SVTermCRep_ptr_ptr]& oprep_lists,
                      vector[vector_INT_ptr]& foat_indices_per_op, INT num_elabels,
                      vector[INT]& nops, vector[INT]& E_indices, vector[double]& pathmags, vector[INT]& nPaths,
                      INT incd, double log_thres, double current_mag, double current_logmag, INT order):
    """ first_order means only one b[i] is incremented, e.g. b == [0 1 0] or [4 0 0] """
    cdef INT i, j, k, orig_bi, orig_bn
    cdef INT n = b.size()
    cdef INT sub_order
    cdef double mag, mag2

    for i in range(n-1, incd-1, -1):
        if b[i]+1 == nops[i]: continue
        b[i] += 1

        if order == 0: # then incd doesn't matter b/c can inc anything to become 1st order
            sub_order = 1 if (i != n-1 or b[i] >= num_elabels) else 0
        elif order == 1:
            # we started with a first order term where incd was incremented, and now
            # we're incrementing something else
            sub_order = 1 if i == incd else 2 # signifies anything over 1st order where >1 column has be inc'd
        else:
            sub_order = order

        logmag = current_logmag + (deref(oprep_lists[i])[b[i]]._logmagnitude - deref(oprep_lists[i])[b[i]-1]._logmagnitude)
        if logmag >= log_thres:
            if deref(oprep_lists[i])[b[i]-1]._magnitude == 0:
                mag = 0
            else:
                mag = current_mag * (deref(oprep_lists[i])[b[i]]._magnitude / deref(oprep_lists[i])[b[i]-1]._magnitude)

            ## fn_visitpath(b, mag, i) ##
            pathmags[E_indices[b[n-1]]] += mag
            nPaths[E_indices[b[n-1]]] += 1
            #print("Adding ",b)
            ## --------------------------

            count_paths(b, oprep_lists, foat_indices_per_op, num_elabels, nops,
                        E_indices, pathmags, nPaths, i, log_thres, mag, logmag, sub_order) #add any allowed paths beneath this one

        elif sub_order <= 1:
            #We've rejected term-index b[i] (in column i) because it's too small - the only reason
            # to accept b[i] or term indices higher than it is to include "foat" terms, so we now
            # iterate through any remaining foat indices for this column (we've accepted all lower
            # values of b[i], or we wouldn't be here).  Note that we just need to visit the path,
            # we don't need to traverse down, since we know the path magnitude is already too low.
            orig_bi = b[i]
            for j in deref(foat_indices_per_op[i]):
                if j >= orig_bi:
                    b[i] = j
                    mag = 0 if deref(oprep_lists[i])[orig_bi-1]._magnitude == 0 else \
                        current_mag * (deref(oprep_lists[i])[b[i]]._magnitude / deref(oprep_lists[i])[orig_bi-1]._magnitude)

                    ## fn_visitpath(b, mag, i) ##
                    pathmags[E_indices[b[n-1]]] += mag
                    nPaths[E_indices[b[n-1]]] += 1
                    #print("FOAT Adding ",b)
                    ## --------------------------

                    if i != n-1:
                        # if we're not incrementing (from a zero-order term) the final index, then we
                        # need to to increment it until we hit num_elabels (*all* zero-th order paths)
                        orig_bn = b[n-1]
                        for k in range(1,num_elabels):
                            b[n-1] = k
                            mag2 = mag * (deref(oprep_lists[n-1])[b[n-1]]._magnitude / deref(oprep_lists[i])[orig_bn]._magnitude)

                            ## fn_visitpath(b, mag2, n-1) ##
                            pathmags[E_indices[b[n-1]]] += mag2
                            nPaths[E_indices[b[n-1]]] += 1
                            #print("FOAT Adding ",b)
                            ## --------------------------
                        b[n-1] = orig_bn
            b[i] = orig_bi
        b[i] -= 1 # so we don't have to copy b


cdef void count_paths_upto_threshold(vector[vector_SVTermCRep_ptr_ptr] oprep_lists, double pathmag_threshold, INT num_elabels,
                                vector[vector_INT_ptr] foat_indices_per_op, vector[INT]& E_indices, vector[double]& pathmags, vector[INT]& nPaths):
    """ TODO: docstring """
    cdef INT i
    cdef INT n = oprep_lists.size()
    cdef vector[INT] nops = vector[INT](n)
    cdef vector[INT] b = vector[INT](n)
    cdef double log_thres = log10(pathmag_threshold)
    cdef double current_mag = 1.0
    cdef double current_logmag = 0.0

    for i in range(n):
        nops[i] = oprep_lists[i].size()
        b[i] = 0

    ## fn_visitpath(b, current_mag, 0) # visit root (all 0s) path
    pathmags[E_indices[0]] += current_mag
    nPaths[E_indices[0]] += 1
    #print("Adding ",b)
    ## -------------------------------
    count_paths(b, oprep_lists, foat_indices_per_op, num_elabels, nops, E_indices, pathmags, nPaths, 0, log_thres, current_mag, current_logmag, 0)
    return


cdef double pathmagnitude_threshold(vector[vector_SVTermCRep_ptr_ptr] oprep_lists, vector[INT]& E_indices,
        INT nEffects, vector[double] target_sum_of_pathmags, vector[vector_INT_ptr] foat_indices_per_op,
        double initial_threshold, double min_threshold, vector[double]& mags, vector[INT]& nPaths):
    """
    TODO: docstring - note: target_sum_of_pathmags is a *vector* that holds a separate value for each E-index
    """
    cdef INT nIters = 0
    cdef double threshold = initial_threshold if (initial_threshold >= 0) else 0.1 # default value
    #target_mag = target_sum_of_pathmags
    cdef double threshold_upper_bound = 1.0
    cdef double threshold_lower_bound = -1.0
    cdef INT i
    cdef INT try_larger_threshold

    while nIters < 100: # TODO: allow setting max_nIters as an arg?
        for i in range(nEffects):
            mags[i] = 0.0; nPaths[i] = 0
        count_paths_upto_threshold(oprep_lists, threshold, nEffects,
                                   foat_indices_per_op, E_indices, mags, nPaths)

        try_larger_threshold = 1 # True
        for i in range(nEffects):
            #if(mags[i] > target_sum_of_pathmags[i]): #DEBUG TODO REMOVE
            #    print "MAGS TOO LARGE!!! mags=",mags[i]," target_sum=",target_sum_of_pathmags[i]

            if(mags[i] < target_sum_of_pathmags[i]):
                try_larger_threshold = 0 # False
                break

        if try_larger_threshold:
            threshold_lower_bound = threshold
            if threshold_upper_bound >= 0: # ~(is not None)
                threshold = (threshold_upper_bound + threshold_lower_bound)/2
            else: threshold *= 2
        else: # try smaller threshold
            threshold_upper_bound = threshold
            if threshold_lower_bound >= 0: # ~(is not None)
                threshold = (threshold_upper_bound + threshold_lower_bound)/2
            else: threshold /= 2

        #print("  Interval: threshold in [%s,%s]: %s %s" % (str(threshold_upper_bound),str(threshold_lower_bound),mag,nPaths))
        if threshold_upper_bound >= 0 and threshold_lower_bound >= 0 and \
           (threshold_upper_bound - threshold_lower_bound)/threshold_upper_bound < 1e-3:
            #print("Converged after %d iters!" % nIters)
            break
        if threshold_upper_bound < min_threshold: # could also just set min_threshold to be the lower bound initially?
            threshold_upper_bound = threshold_lower_bound = min_threshold
            #print("Hit min threshold after %d iters!" % nIters)
            break

        nIters += 1

    #Run path traversal once more to count final number of paths
    for i in range(nEffects):
        mags[i] = 0.0; nPaths[i] = 0
    count_paths_upto_threshold(oprep_lists, threshold_lower_bound, nEffects,
                               foat_indices_per_op, E_indices, mags, nPaths) # sets mags and nPaths

    return threshold_lower_bound



# State-vector direct-term calcs -------------------------

#cdef vector[vector[SVTermDirectCRep_ptr]] sv_extract_cterms_direct(python_termrep_lists, INT max_order):
#    cdef vector[vector[SVTermDirectCRep_ptr]] ret = vector[vector[SVTermDirectCRep_ptr]](max_order+1)
#    cdef vector[SVTermDirectCRep*] vec_of_terms
#    for order,termreps in enumerate(python_termrep_lists): # maxorder+1 lists
#        vec_of_terms = vector[SVTermDirectCRep_ptr](len(termreps))
#        for i,termrep in enumerate(termreps):
#            vec_of_terms[i] = (<SVTermDirectRep?>termrep).c_term
#        ret[order] = vec_of_terms
#    return ret

#def SV_prs_directly(calc, rholabel, elabels, circuit, repcache, comm=None, memLimit=None, fastmode=True, wtTol=0.0, resetTermWeights=True, debug=None):
#
#    # Create gatelable -> int mapping to be used throughout
#    distinct_gateLabels = sorted(set(circuit))
#    glmap = { gl: i for i,gl in enumerate(distinct_gateLabels) }
#    t0 = pytime.time()
#
#    # Convert circuit to a vector of ints
#    cdef INT i, j
#    cdef vector[INT] cgatestring
#    for gl in circuit:
#        cgatestring.push_back(<INT>glmap[gl])
#
#    #TODO: maybe compute these weights elsewhere and pass in?
#    cdef double circuitWeight
#    cdef double remaingingWeightTol = <double?>wtTol
#    cdef vector[double] remainingWeight = vector[double](<INT>len(elabels))
#    if 'circuitWeights' not in repcache:
#        repcache['circuitWeights'] = {}
#    if resetTermWeights or circuit not in repcache['circuitWeights']:
#        circuitWeight = calc.sos.get_prep(rholabel).get_total_term_weight()
#        for gl in circuit:
#            circuitWeight *= calc.sos.get_operation(gl).get_total_term_weight()
#        for i,elbl in enumerate(elabels):
#            remainingWeight[i] = circuitWeight * calc.sos.get_effect(elbl).get_total_term_weight()
#        repcache['circuitWeights'][circuit] = [ remainingWeight[i] for i in range(remainingWeight.size()) ]
#    else:
#        for i,wt in enumerate(repcache['circuitWeights'][circuit]):
#            assert(wt > 1.0)
#            remainingWeight[i] = wt
#
#    #if resetTermWeights:
#    #    print "Remaining weights: "
#    #    for i in range(remainingWeight.size()):
#    #        print remainingWeight[i]
#
#    cdef double order_base = 0.1 # default for now - TODO: make this a calc param like max_order?
#    cdef INT order
#    cdef INT numEs = len(elabels)
#
#    cdef RepCacheEl repcel;
#    cdef vector[SVTermDirectCRep_ptr] treps;
#    cdef DCOMPLEX* coeffs;
#    cdef vector[SVTermDirectCRep*] reps_at_order;
#    cdef np.ndarray coeffs_array;
#    cdef SVTermDirectRep rep;
#
#    # Construct dict of gate term reps, then *convert* to c-reps, as this
#    #  keeps alive the non-c-reps which keep the c-reps from being deallocated...
#    cdef unordered_map[INT, vector[vector[SVTermDirectCRep_ptr]] ] op_term_reps = unordered_map[INT, vector[vector[SVTermDirectCRep_ptr]] ](); # OLD = {}
#    for glbl in distinct_gateLabels:
#        if glbl in repcache:
#            repcel = <RepCacheEl?>repcache[glbl]
#            op_term_reps[ glmap[glbl] ] = repcel.reps
#            for order in range(calc.max_order+1):
#                treps = repcel.reps[order]
#                coeffs_array = calc.sos.get_operation(glbl).get_direct_order_coeffs(order,order_base)
#                coeffs = <DCOMPLEX*?>(coeffs_array.data)
#                for i in range(treps.size()):
#                    treps[i]._coeff = coeffs[i]
#                    if resetTermWeights: treps[i]._magnitude = abs(coeffs[i])
#            #for order,treps in enumerate(op_term_reps[ glmap[glbl] ]):
#            #    for coeff,trep in zip(calc.sos.get_operation(glbl).get_direct_order_coeffs(order,order_base), treps):
#            #        trep.set_coeff(coeff)
#        else:
#            repcel = RepCacheEl(calc.max_order)
#            for order in range(calc.max_order+1):
#                reps_at_order = vector[SVTermDirectCRep_ptr](0)
#                for t in calc.sos.get_operation(glbl).get_direct_order_terms(order,order_base):
#                    rep = (<SVTermDirectRep?>t.torep(None,None,"gate"))
#                    repcel.pyterm_references.append(rep)
#                    reps_at_order.push_back( rep.c_term )
#                repcel.reps[order] = reps_at_order
#            #OLD
#            #reps = [ [t.torep(None,None,"gate") for t in calc.sos.get_operation(glbl).get_direct_order_terms(order,order_base)]
#            #                                for order in range(calc.max_order+1) ]
#            op_term_reps[ glmap[glbl] ] = repcel.reps
#            repcache[glbl] = repcel
#
#    #OLD
#    #op_term_reps = { glmap[glbl]: [ [t.torep(None,None,"gate") for t in calc.sos.get_operation(glbl).get_direct_order_terms(order,order_base)]
#    #                                  for order in range(calc.max_order+1) ]
#    #                   for glbl in distinct_gateLabels }
#
#    #Similar with rho_terms and E_terms
#    cdef vector[vector[SVTermDirectCRep_ptr]] rho_term_reps;
#    if rholabel in repcache:
#        repcel = repcache[rholabel]
#        rho_term_reps = repcel.reps
#        for order in range(calc.max_order+1):
#            treps = rho_term_reps[order]
#            coeffs_array = calc.sos.get_prep(rholabel).get_direct_order_coeffs(order,order_base)
#            coeffs = <DCOMPLEX*?>(coeffs_array.data)
#            for i in range(treps.size()):
#                treps[i]._coeff = coeffs[i]
#                if resetTermWeights: treps[i]._magnitude = abs(coeffs[i])
#
#        #for order,treps in enumerate(rho_term_reps):
#        #    for coeff,trep in zip(calc.sos.get_prep(rholabel).get_direct_order_coeffs(order,order_base), treps):
#        #        trep.set_coeff(coeff)
#    else:
#        repcel = RepCacheEl(calc.max_order)
#        for order in range(calc.max_order+1):
#            reps_at_order = vector[SVTermDirectCRep_ptr](0)
#            for t in calc.sos.get_prep(rholabel).get_direct_order_terms(order,order_base):
#                rep = (<SVTermDirectRep?>t.torep(None,None,"prep"))
#                repcel.pyterm_references.append(rep)
#                reps_at_order.push_back( rep.c_term )
#            repcel.reps[order] = reps_at_order
#        rho_term_reps = repcel.reps
#        repcache[rholabel] = repcel
#
#        #OLD
#        #rho_term_reps = [ [t.torep(None,None,"prep") for t in calc.sos.get_prep(rholabel).get_direct_order_terms(order,order_base)]
#        #              for order in range(calc.max_order+1) ]
#        #repcache[rholabel] = rho_term_reps
#
#    #E_term_reps = []
#    cdef vector[vector[SVTermDirectCRep_ptr]] E_term_reps = vector[vector[SVTermDirectCRep_ptr]](0);
#    cdef SVTermDirectCRep_ptr cterm;
#    E_indices = [] # TODO: upgrade to C-type?
#    if all([ elbl in repcache for elbl in elabels]):
#        for order in range(calc.max_order+1):
#            reps_at_order = vector[SVTermDirectCRep_ptr](0) # the term reps for *all* the effect vectors
#            cur_indices = [] # the Evec-index corresponding to each term rep
#            for j,elbl in enumerate(elabels):
#                repcel = <RepCacheEl?>repcache[elbl]
#                #term_reps = [t.torep(None,None,"effect") for t in calc.sos.get_effect(elbl).get_direct_order_terms(order,order_base) ]
#
#                treps = repcel.reps[order]
#                coeffs_array = calc.sos.get_effect(elbl).get_direct_order_coeffs(order,order_base)
#                coeffs = <DCOMPLEX*?>(coeffs_array.data)
#                for i in range(treps.size()):
#                    treps[i]._coeff = coeffs[i]
#                    if resetTermWeights: treps[i]._magnitude = abs(coeffs[i])
#                    reps_at_order.push_back(treps[i])
#                cur_indices.extend( [j]*reps_at_order.size() )
#
#                #OLD
#                #term_reps = repcache[elbl][order]
#                #for coeff,trep in zip(calc.sos.get_effect(elbl).get_direct_order_coeffs(order,order_base), term_reps):
#                #    trep.set_coeff(coeff)
#                #cur_term_reps.extend( term_reps )
#                # cur_indices.extend( [j]*len(term_reps) )
#
#            E_term_reps.push_back(reps_at_order)
#            E_indices.append( cur_indices )
#            # E_term_reps.append( cur_term_reps )
#
#    else:
#        for elbl in elabels:
#            if elbl not in repcache: repcache[elbl] = RepCacheEl(calc.max_order) #[None]*(calc.max_order+1) # make sure there's room
#        for order in range(calc.max_order+1):
#            reps_at_order = vector[SVTermDirectCRep_ptr](0) # the term reps for *all* the effect vectors
#            cur_indices = [] # the Evec-index corresponding to each term rep
#            for j,elbl in enumerate(elabels):
#                repcel = <RepCacheEl?>repcache[elbl]
#                treps = vector[SVTermDirectCRep_ptr](0) # the term reps for *all* the effect vectors
#                for t in calc.sos.get_effect(elbl).get_direct_order_terms(order,order_base):
#                    rep = (<SVTermDirectRep?>t.torep(None,None,"effect"))
#                    repcel.pyterm_references.append(rep)
#                    treps.push_back( rep.c_term )
#                    reps_at_order.push_back( rep.c_term )
#                repcel.reps[order] = treps
#                cur_indices.extend( [j]*treps.size() )
#                #term_reps = [t.torep(None,None,"effect") for t in calc.sos.get_effect(elbl).get_direct_order_terms(order,order_base) ]
#                #repcache[elbl][order] = term_reps
#                #cur_term_reps.extend( term_reps )
#                #cur_indices.extend( [j]*len(term_reps) )
#            E_term_reps.push_back(reps_at_order)
#            E_indices.append( cur_indices )
#            #E_term_reps.append( cur_term_reps )
#
#    #convert to c-reps
#    cdef INT gi
#    #cdef vector[vector[SVTermDirectCRep_ptr]] rho_term_creps = rho_term_reps # already c-reps...
#    #cdef vector[vector[SVTermDirectCRep_ptr]] E_term_creps = E_term_reps # already c-reps...
#    #cdef unordered_map[INT, vector[vector[SVTermDirectCRep_ptr]]] gate_term_creps = op_term_reps # already c-reps...
#    #cdef vector[vector[SVTermDirectCRep_ptr]] rho_term_creps = sv_extract_cterms_direct(rho_term_reps,calc.max_order)
#    #cdef vector[vector[SVTermDirectCRep_ptr]] E_term_creps = sv_extract_cterms_direct(E_term_reps,calc.max_order)
#    #for gi,termrep_lists in op_term_reps.items():
#    #    gate_term_creps[gi] = sv_extract_cterms_direct(termrep_lists,calc.max_order)
#
#    E_cindices = vector[vector[INT]](<INT>len(E_indices))
#    for ii,inds in enumerate(E_indices):
#        E_cindices[ii] = vector[INT](<INT>len(inds))
#        for jj,indx in enumerate(inds):
#            E_cindices[ii][jj] = <INT>indx
#
#    #Note: term calculator "dim" is the full density matrix dim
#    stateDim = int(round(np.sqrt(calc.dim)))
#    if debug is not None:
#        debug['tstartup'] += pytime.time()-t0
#        t0 = pytime.time()
#
#    #Call C-only function (which operates with C-representations only)
#    cdef vector[float] debugvec = vector[float](10)
#    debugvec[0] = 0.0
#    cdef vector[DCOMPLEX] prs = sv_prs_directly(
#        cgatestring, rho_term_reps, op_term_reps, E_term_reps,
#        #cgatestring, rho_term_creps, gate_term_creps, E_term_creps,
#        E_cindices, numEs, calc.max_order, stateDim, <bool>fastmode, &remainingWeight, remaingingWeightTol, debugvec)
#
#    debug['total'] += debugvec[0]
#    debug['t1'] += debugvec[1]
#    debug['t2'] += debugvec[2]
#    debug['t3'] += debugvec[3]
#    debug['n1'] += debugvec[4]
#    debug['n2'] += debugvec[5]
#    debug['n3'] += debugvec[6]
#    debug['t4'] += debugvec[7]
#    debug['n4'] += debugvec[8]
#    #if not all([ abs(prs[i].imag) < 1e-4 for i in range(<INT>prs.size()) ]):
#    #    print("ERROR: prs = ",[ prs[i] for i in range(<INT>prs.size()) ])
#    #assert(all([ abs(prs[i].imag) < 1e-6 for i in range(<INT>prs.size()) ]))
#    return [ prs[i].real for i in range(<INT>prs.size()) ] # TODO: make this into a numpy array? - maybe pass array to fill to sv_prs_directy above?
#
#
#cdef vector[DCOMPLEX] sv_prs_directly(
#    vector[INT]& circuit, vector[vector[SVTermDirectCRep_ptr]] rho_term_reps,
#    unordered_map[INT, vector[vector[SVTermDirectCRep_ptr]]] op_term_reps,
#    vector[vector[SVTermDirectCRep_ptr]] E_term_reps, vector[vector[INT]] E_term_indices,
#    INT numEs, INT max_order, INT dim, bool fastmode, vector[double]* remainingWeight, double remTol, vector[float]& debugvec):
#
#    #NOTE: circuit and gate_terms use *integers* as operation labels, not Label objects, to speed
#    # lookups and avoid weird string conversion stuff with Cython
#
#    cdef INT N = len(circuit)
#    cdef INT* p = <INT*>malloc((N+2) * sizeof(INT))
#    cdef INT i,j,k,order,nTerms
#    cdef INT gn
#
#    cdef INT t0 = time.clock()
#    cdef INT t, n, nPaths; #for below
#
#    cdef sv_innerloopfn_direct_ptr innerloop_fn;
#    if fastmode:
#        innerloop_fn = sv_pr_directly_innerloop_savepartials
#    else:
#        innerloop_fn = sv_pr_directly_innerloop
#
#    #extract raw data from gate_terms dictionary-of-lists for faster lookup
#    #gate_term_prefactors = np.empty( (nOperations,max_order+1,dim,dim)
#    #cdef unordered_map[INT, vector[vector[unordered_map[INT, complex]]]] gate_term_coeffs
#    #cdef vector[vector[unordered_map[INT, complex]]] rho_term_coeffs
#    #cdef vector[vector[unordered_map[INT, complex]]] E_term_coeffs
#    #cdef vector[vector[INT]] E_indices
#
#    cdef vector[INT]* Einds
#    cdef vector[vector_SVTermDirectCRep_ptr_ptr] factor_lists
#
#    assert(max_order <= 2) # only support this partitioning below (so far)
#
#    cdef vector[DCOMPLEX] prs = vector[DCOMPLEX](numEs)
#
#    for order in range(max_order+1):
#        #print("DB: pr_as_poly order=",order)
#
#        #for p in partition_into(order, N):
#        for i in range(N+2): p[i] = 0 # clear p
#        factor_lists = vector[vector_SVTermDirectCRep_ptr_ptr](N+2)
#
#        if order == 0:
#            #inner loop(p)
#            #factor_lists = [ gate_terms[glbl][pi] for glbl,pi in zip(circuit,p) ]
#            t = time.clock()
#            factor_lists[0] = &rho_term_reps[p[0]]
#            for k in range(N):
#                gn = circuit[k]
#                factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
#                #if factor_lists[k+1].size() == 0: continue # WHAT???
#            factor_lists[N+1] = &E_term_reps[p[N+1]]
#            Einds = &E_term_indices[p[N+1]]
#
#            #print("Part0 ",p)
#            nPaths = innerloop_fn(factor_lists,Einds,&prs,dim,remainingWeight,0.0) #remTol) # force 0-order
#            debugvec[1] += float(time.clock() - t)/time.CLOCKS_PER_SEC
#            debugvec[4] += nPaths
#
#        elif order == 1:
#            t = time.clock(); n=0
#            for i in range(N+2):
#                p[i] = 1
#                #inner loop(p)
#                factor_lists[0] = &rho_term_reps[p[0]]
#                for k in range(N):
#                    gn = circuit[k]
#                    factor_lists[k+1] = &op_term_reps[gn][p[k+1]]
#                    #if len(factor_lists[k+1]) == 0: continue #WHAT???
#                factor_lists[N+1] = &E_term_reps[p[N+1]]
#                Einds = &E_term_indices[p[N+1]]
#
#                #print "DB: Order1 "
#                nPaths = innerloop_fn(factor_lists,Einds,&prs,dim,remainingWeight,0.0) #remTol) # force 1st-order
#                p[i] = 0
#                n += nPaths
#            debugvec[2] += float(time.clock() - t)/time.CLOCKS_PER_SEC
#            debugvec[5] += n
#
#        elif order == 2:
#            t = time.clock(); n=0
#            for i in range(N+2):
#                p[i] = 2
#                #inner loop(p)
#                factor_lists[0] = &rho_term_reps[p[0]]
#                for k in range(N):
#                    gn = circuit[k]
#                    factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
#                    #if len(factor_lists[k+1]) == 0: continue # WHAT???
#                factor_lists[N+1] = &E_term_reps[p[N+1]]
#                Einds = &E_term_indices[p[N+1]]
#
#                nPaths = innerloop_fn(factor_lists,Einds,&prs,dim,remainingWeight,remTol)
#                p[i] = 0
#                n += nPaths
#
#            debugvec[3] += float(time.clock() - t)/time.CLOCKS_PER_SEC
#            debugvec[6] += n
#            t = time.clock(); n=0
#
#            for i in range(N+2):
#                p[i] = 1
#                for j in range(i+1,N+2):
#                    p[j] = 1
#                    #inner loop(p)
#                    factor_lists[0] = &rho_term_reps[p[0]]
#                    for k in range(N):
#                        gn = circuit[k]
#                        factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
#                        #if len(factor_lists[k+1]) == 0: continue #WHAT???
#                    factor_lists[N+1] = &E_term_reps[p[N+1]]
#                    Einds = &E_term_indices[p[N+1]]
#
#                    nPaths = innerloop_fn(factor_lists,Einds,&prs,dim,remainingWeight,remTol)
#                    p[j] = 0
#                    n += nPaths
#                p[i] = 0
#            debugvec[7] += float(time.clock() - t)/time.CLOCKS_PER_SEC
#            debugvec[8] += n
#
#        else:
#            assert(False) # order > 2 not implemented yet...
#
#    free(p)
#
#    debugvec[0] += float(time.clock() - t0)/time.CLOCKS_PER_SEC
#    return prs
#
#
#
#cdef INT sv_pr_directly_innerloop(vector[vector_SVTermDirectCRep_ptr_ptr] factor_lists, vector[INT]* Einds,
#                                   vector[DCOMPLEX]* prs, INT dim, vector[double]* remainingWeight, double remainingWeightTol):
#    #print("DB partition = ","listlens = ",[len(fl) for fl in factor_lists])
#
#    cdef INT i,j,Ei
#    cdef double complex scale, val, newval, pLeft, pRight, p
#    cdef double wt, cwt
#    cdef int nPaths = 0
#
#    cdef SVTermDirectCRep* factor
#
#    cdef INT nFactorLists = factor_lists.size() # may need to recompute this after fast-mode
#    cdef INT* factorListLens = <INT*>malloc(nFactorLists * sizeof(INT))
#    cdef INT last_index = nFactorLists-1
#
#    for i in range(nFactorLists):
#        factorListLens[i] = factor_lists[i].size()
#        if factorListLens[i] == 0:
#            free(factorListLens)
#            return 0 # nothing to loop over! - (exit before we allocate more)
#
#    cdef double complex coeff   # THESE are only real changes from "as_poly"
#    cdef double complex result  # version of this function (where they are PolyCRep type)
#
#    cdef SVStateCRep *prop1 = new SVStateCRep(dim)
#    cdef SVStateCRep *prop2 = new SVStateCRep(dim)
#    cdef SVStateCRep *tprop
#    cdef SVEffectCRep* EVec
#
#    cdef INT* b = <INT*>malloc(nFactorLists * sizeof(INT))
#    for i in range(nFactorLists): b[i] = 0
#
#    assert(nFactorLists > 0), "Number of factor lists must be > 0!"
#
#    #for factors in _itertools.product(*factor_lists):
#    while(True):
#        final_factor_indx = b[last_index]
#        Ei = deref(Einds)[final_factor_indx] #final "factor" index == E-vector index
#        wt = deref(remainingWeight)[Ei]
#        if remainingWeightTol == 0.0 or wt > remainingWeightTol: #if we need this "path"
#            # In this loop, b holds "current" indices into factor_lists
#            factor = deref(factor_lists[0])[b[0]] # the last factor (an Evec)
#            coeff = factor._coeff
#            cwt = factor._magnitude
#
#            for i in range(1,nFactorLists):
#                coeff *= deref(factor_lists[i])[b[i]]._coeff
#                cwt *= deref(factor_lists[i])[b[i]]._magnitude
#
#            #pLeft / "pre" sim
#            factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
#            prop1.copy_from(factor._pre_state)
#            for j in range(<INT>factor._pre_ops.size()):
#                factor._pre_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop
#            for i in range(1,last_index):
#                factor = deref(factor_lists[i])[b[i]]
#                for j in range(<INT>factor._pre_ops.size()):
#                    factor._pre_ops[j].acton(prop1,prop2)
#                    tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
#            factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)
#
#        	# can't propagate effects, so effect's post_ops are constructed to act on *state*
#            EVec = factor._post_effect
#            for j in range(<INT>factor._post_ops.size()):
#                rhoVec = factor._post_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
#            pLeft = EVec.amplitude(prop1)
#
#            #pRight / "post" sim
#            factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
#            prop1.copy_from(factor._post_state)
#            for j in range(<INT>factor._post_ops.size()):
#                factor._post_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
#            for i in range(1,last_index):
#                factor = deref(factor_lists[i])[b[i]]
#                for j in range(<INT>factor._post_ops.size()):
#                    factor._post_ops[j].acton(prop1,prop2)
#                    tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
#            factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)
#
#            EVec = factor._pre_effect
#            for j in range(<INT>factor._pre_ops.size()):
#                factor._pre_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
#            pRight = EVec.amplitude(prop1).conjugate()
#
#            #Add result to appropriate poly
#            result = coeff * pLeft * pRight
#            deref(prs)[Ei] = deref(prs)[Ei] + result #TODO - see why += doesn't work here
#            deref(remainingWeight)[Ei] = wt - cwt # "weight" of this path
#            nPaths += 1 # just for debuggins
#
#        #increment b ~ itertools.product & update vec_index_noop = np.dot(self.multipliers, b)
#        for i in range(nFactorLists-1,-1,-1):
#            if b[i]+1 < factorListLens[i]:
#                b[i] += 1
#                break
#            else:
#                b[i] = 0
#        else:
#            break # can't increment anything - break while(True) loop
#
#    #Clenaup: free allocated memory
#    del prop1
#    del prop2
#    free(factorListLens)
#    free(b)
#    return nPaths
#
#
#cdef INT sv_pr_directly_innerloop_savepartials(vector[vector_SVTermDirectCRep_ptr_ptr] factor_lists,
#                                                vector[INT]* Einds, vector[DCOMPLEX]* prs, INT dim,
#                                                vector[double]* remainingWeight, double remainingWeightTol):
#    #print("DB partition = ","listlens = ",[len(fl) for fl in factor_lists])
#
#    cdef INT i,j,Ei
#    cdef double complex scale, val, newval, pLeft, pRight, p
#
#    cdef INT incd
#    cdef SVTermDirectCRep* factor
#
#    cdef INT nFactorLists = factor_lists.size() # may need to recompute this after fast-mode
#    cdef INT* factorListLens = <INT*>malloc(nFactorLists * sizeof(INT))
#    cdef INT last_index = nFactorLists-1
#
#    for i in range(nFactorLists):
#        factorListLens[i] = factor_lists[i].size()
#        if factorListLens[i] == 0:
#            free(factorListLens)
#            return 0 # nothing to loop over! (exit before we allocate anything else)
#
#    cdef double complex coeff
#    cdef double complex result
#
#    #fast mode
#    cdef vector[SVStateCRep*] leftSaved = vector[SVStateCRep_ptr](nFactorLists-1)  # saved[i] is state after i-th
#    cdef vector[SVStateCRep*] rightSaved = vector[SVStateCRep_ptr](nFactorLists-1) # factor has been applied
#    cdef vector[DCOMPLEX] coeffSaved = vector[DCOMPLEX](nFactorLists-1)
#    cdef SVStateCRep *shelved = new SVStateCRep(dim)
#    cdef SVStateCRep *prop2 = new SVStateCRep(dim) # prop2 is always a temporary allocated state not owned by anything else
#    cdef SVStateCRep *prop1
#    cdef SVStateCRep *tprop
#    cdef SVEffectCRep* EVec
#
#    cdef INT* b = <INT*>malloc(nFactorLists * sizeof(INT))
#    for i in range(nFactorLists): b[i] = 0
#    assert(nFactorLists > 0), "Number of factor lists must be > 0!"
#
#    incd = 0
#
#    #Fill saved arrays with allocated states
#    for i in range(nFactorLists-1):
#        leftSaved[i] = new SVStateCRep(dim)
#        rightSaved[i] = new SVStateCRep(dim)
#
#    #for factors in _itertools.product(*factor_lists):
#    #for incd,fi in incd_product(*[range(len(l)) for l in factor_lists]):
#    while(True):
#        # In this loop, b holds "current" indices into factor_lists
#        #print "DB: iter-product BEGIN"
#
#        if incd == 0: # need to re-evaluate rho vector
#            #print "DB: re-eval at incd=0"
#            factor = deref(factor_lists[0])[b[0]]
#
#            #print "DB: re-eval left"
#            prop1 = leftSaved[0] # the final destination (prop2 is already alloc'd)
#            prop1.copy_from(factor._pre_state)
#            for j in range(<INT>factor._pre_ops.size()):
#                #print "DB: re-eval left item"
#                factor._pre_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
#            rhoVecL = prop1
#            leftSaved[0] = prop1 # final state -> saved
#            # (prop2 == the other allocated state)
#
#            #print "DB: re-eval right"
#            prop1 = rightSaved[0] # the final destination (prop2 is already alloc'd)
#            prop1.copy_from(factor._post_state)
#            for j in range(<INT>factor._post_ops.size()):
#                #print "DB: re-eval right item"
#                factor._post_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
#            rhoVecR = prop1
#            rightSaved[0] = prop1 # final state -> saved
#            # (prop2 == the other allocated state)
#
#            #print "DB: re-eval coeff"
#            coeff = factor._coeff
#            coeffSaved[0] = coeff
#            incd += 1
#        else:
#            #print "DB: init from incd"
#            rhoVecL = leftSaved[incd-1]
#            rhoVecR = rightSaved[incd-1]
#            coeff = coeffSaved[incd-1]
#
#        # propagate left and right states, saving as we go
#        for i in range(incd,last_index):
#            #print "DB: propagate left begin"
#            factor = deref(factor_lists[i])[b[i]]
#            prop1 = leftSaved[i] # destination
#            prop1.copy_from(rhoVecL) #starting state
#            for j in range(<INT>factor._pre_ops.size()):
#                #print "DB: propagate left item"
#                factor._pre_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop
#            rhoVecL = prop1
#            leftSaved[i] = prop1
#            # (prop2 == the other allocated state)
#
#            #print "DB: propagate right begin"
#            prop1 = rightSaved[i] # destination
#            prop1.copy_from(rhoVecR) #starting state
#            for j in range(<INT>factor._post_ops.size()):
#                #print "DB: propagate right item"
#                factor._post_ops[j].acton(prop1,prop2)
#                tprop = prop1; prop1 = prop2; prop2 = tprop
#            rhoVecR = prop1
#            rightSaved[i] = prop1
#            # (prop2 == the other allocated state)
#
#            #print "DB: propagate coeff mult"
#            coeff *= factor._coeff
#            coeffSaved[i] = coeff
#
#        # for the last index, no need to save, and need to construct
#        # and apply effect vector
#        prop1 = shelved # so now prop1 (and prop2) are alloc'd states
#
#        #print "DB: left ampl"
#        factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)
#        EVec = factor._post_effect
#        prop1.copy_from(rhoVecL) # initial state (prop2 already alloc'd)
#        for j in range(<INT>factor._post_ops.size()):
#            factor._post_ops[j].acton(prop1,prop2)
#            tprop = prop1; prop1 = prop2; prop2 = tprop
#        pLeft = EVec.amplitude(prop1) # output in prop1, so this is final amplitude
#
#        #print "DB: right ampl"
#        EVec = factor._pre_effect
#        prop1.copy_from(rhoVecR)
#        for j in range(<INT>factor._pre_ops.size()):
#            factor._pre_ops[j].acton(prop1,prop2)
#            tprop = prop1; prop1 = prop2; prop2 = tprop
#        pRight = EVec.amplitude(prop1).conjugate()
#
#        shelved = prop1 # return prop1 to the "shelf" since we'll use prop1 for other things next
#
#        #print "DB: final block"
#        #print "DB running coeff = ",dict(coeff._coeffs)
#        #print "DB factor coeff = ",dict(factor._coeff._coeffs)
#        result = coeff * factor._coeff
#        #print "DB result = ",dict(result._coeffs)
#        result *= pLeft * pRight
#        final_factor_indx = b[last_index]
#        Ei = deref(Einds)[final_factor_indx] #final "factor" index == E-vector index
#        deref(prs)[Ei] += result
#        #print "DB prs[",INT(Ei),"] = ",dict(deref(prs)[Ei]._coeffs)
#
#        #assert(debug < 100) #DEBUG
#        #print "DB: end product loop"
#
#        #increment b ~ itertools.product & update vec_index_noop = np.dot(self.multipliers, b)
#        for i in range(nFactorLists-1,-1,-1):
#            if b[i]+1 < factorListLens[i]:
#                b[i] += 1; incd = i
#                break
#            else:
#                b[i] = 0
#        else:
#            break # can't increment anything - break while(True) loop
#
#    #Cleanup: free allocated memory
#    for i in range(nFactorLists-1):
#        del leftSaved[i]
#        del rightSaved[i]
#    del prop2
#    del shelved
#    free(factorListLens)
#    free(b)
#    return 0 #TODO: fix nPaths


# Stabilizer-evolution version of poly term calcs -----------------------

cdef vector[vector[SBTermCRep_ptr]] sb_extract_cterms(python_termrep_lists, INT max_order):
    cdef vector[vector[SBTermCRep_ptr]] ret = vector[vector[SBTermCRep_ptr]](max_order+1)
    cdef vector[SBTermCRep*] vec_of_terms
    for order,termreps in enumerate(python_termrep_lists): # maxorder+1 lists
        vec_of_terms = vector[SBTermCRep_ptr](len(termreps))
        for i,termrep in enumerate(termreps):
            vec_of_terms[i] = (<SBTermRep?>termrep).c_term
        ret[order] = vec_of_terms
    return ret


def SB_prs_as_polys(calc, rholabel, elabels, circuit, comm=None, memLimit=None, fastmode=True):

    # Create gatelable -> int mapping to be used throughout
    distinct_gateLabels = sorted(set(circuit))
    glmap = { gl: i for i,gl in enumerate(distinct_gateLabels) }

    # Convert circuit to a vector of ints
    cdef INT i
    cdef vector[INT] cgatestring
    for gl in circuit:
        cgatestring.push_back(<INT>glmap[gl])

    cdef INT mpv = calc.Np # max_poly_vars
    cdef INT mpo = calc.max_order*2 #max_poly_order
    cdef INT vpi = calc.poly_vindices_per_int
    cdef INT order;
    cdef INT numEs = len(elabels)

    # Construct dict of gate term reps, then *convert* to c-reps, as this
    #  keeps alive the non-c-reps which keep the c-reps from being deallocated...
    op_term_reps = { glmap[glbl]: [ [t.torep(mpo,mpv,"gate") for t in calc.sos.get_operation(glbl).get_taylor_order_terms(order)]
                                      for order in range(calc.max_order+1) ]
                       for glbl in distinct_gateLabels }

    #Similar with rho_terms and E_terms
    rho_term_reps = [ [t.torep(mpo,mpv,"prep") for t in calc.sos.get_prep(rholabel).get_taylor_order_terms(order)]
                      for order in range(calc.max_order+1) ]

    E_term_reps = []
    E_indices = []
    for order in range(calc.max_order+1):
        cur_term_reps = [] # the term reps for *all* the effect vectors
        cur_indices = [] # the Evec-index corresponding to each term rep
        for i,elbl in enumerate(elabels):
            term_reps = [t.torep(mpo,mpv,"effect") for t in calc.sos.get_effect(elbl).get_taylor_order_terms(order) ]
            cur_term_reps.extend( term_reps )
            cur_indices.extend( [i]*len(term_reps) )
        E_term_reps.append( cur_term_reps )
        E_indices.append( cur_indices )


    #convert to c-reps
    cdef INT gi
    cdef vector[vector[SBTermCRep_ptr]] rho_term_creps = sb_extract_cterms(rho_term_reps,calc.max_order)
    cdef vector[vector[SBTermCRep_ptr]] E_term_creps = sb_extract_cterms(E_term_reps,calc.max_order)
    cdef unordered_map[INT, vector[vector[SBTermCRep_ptr]]] gate_term_creps
    for gi,termrep_lists in op_term_reps.items():
        gate_term_creps[gi] = sb_extract_cterms(termrep_lists,calc.max_order)

    E_cindices = vector[vector[INT]](<INT>len(E_indices))
    for ii,inds in enumerate(E_indices):
        E_cindices[ii] = vector[INT](<INT>len(inds))
        for jj,indx in enumerate(inds):
            E_cindices[ii][jj] = <INT>indx

    # Assume when we calculate terms, that "dimension" of Model is
    # a full vectorized-density-matrix dimension, so nqubits is:
    cdef INT nqubits = <INT>(np.log2(calc.dim)//2)

    #Call C-only function (which operates with C-representations only)
    cdef vector[PolyCRep*] polys = sb_prs_as_polys(
        cgatestring, rho_term_creps, gate_term_creps, E_term_creps,
        E_cindices, numEs, calc.max_order, mpo, mpv, vpi, nqubits, <bool>fastmode)

    return [ PolyRep_from_allocd_PolyCRep(polys[i]) for i in range(<INT>polys.size()) ]


cdef vector[PolyCRep*] sb_prs_as_polys(
    vector[INT]& circuit, vector[vector[SBTermCRep_ptr]] rho_term_reps,
    unordered_map[INT, vector[vector[SBTermCRep_ptr]]] op_term_reps,
    vector[vector[SBTermCRep_ptr]] E_term_reps, vector[vector[INT]] E_term_indices,
    INT numEs, INT max_order, INT max_poly_order, INT max_poly_vars, INT vindices_per_int, INT nqubits, bool fastmode):

    #NOTE: circuit and gate_terms use *integers* as operation labels, not Label objects, to speed
    # lookups and avoid weird string conversion stuff with Cython

    cdef INT N = len(circuit)
    cdef INT* p = <INT*>malloc((N+2) * sizeof(INT))
    cdef INT i,j,k,order,nTerms
    cdef INT gn

    cdef sb_innerloopfn_ptr innerloop_fn;
    if fastmode:
        innerloop_fn = sb_pr_as_poly_innerloop_savepartials
    else:
        innerloop_fn = sb_pr_as_poly_innerloop

    #extract raw data from gate_terms dictionary-of-lists for faster lookup
    #gate_term_prefactors = np.empty( (nOperations,max_order+1,dim,dim)
    #cdef unordered_map[INT, vector[vector[unordered_map[INT, complex]]]] gate_term_coeffs
    #cdef vector[vector[unordered_map[INT, complex]]] rho_term_coeffs
    #cdef vector[vector[unordered_map[INT, complex]]] E_term_coeffs
    #cdef vector[vector[INT]] E_indices

    cdef vector[INT]* Einds
    cdef vector[vector_SBTermCRep_ptr_ptr] factor_lists

    assert(max_order <= 2) # only support this partitioning below (so far)

    cdef vector[PolyCRep_ptr] prps = vector[PolyCRep_ptr](numEs)
    for i in range(numEs):
        prps[i] = new PolyCRep(unordered_map[PolyVarsIndex,complex](),max_poly_order, max_poly_vars, vindices_per_int)
        # create empty polys - maybe overload constructor for this?
        # these PolyCReps are alloc'd here and returned - it is the job of the caller to
        #  free them (or assign them to new PolyRep wrapper objs)

    for order in range(max_order+1):
        #print "DB CYTHON: pr_as_poly order=",INT(order)

        #for p in partition_into(order, N):
        for i in range(N+2): p[i] = 0 # clear p
        factor_lists = vector[vector_SBTermCRep_ptr_ptr](N+2)

        if order == 0:
            #inner loop(p)
            #factor_lists = [ gate_terms[glbl][pi] for glbl,pi in zip(circuit,p) ]
            factor_lists[0] = &rho_term_reps[p[0]]
            for k in range(N):
                gn = circuit[k]
                factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
                #if factor_lists[k+1].size() == 0: continue # WHAT???
            factor_lists[N+1] = &E_term_reps[p[N+1]]
            Einds = &E_term_indices[p[N+1]]

            #print "DB CYTHON: Order0"
            innerloop_fn(factor_lists,Einds,&prps,nqubits) #, prps_chk)


        elif order == 1:
            for i in range(N+2):
                p[i] = 1
                #inner loop(p)
                factor_lists[0] = &rho_term_reps[p[0]]
                for k in range(N):
                    gn = circuit[k]
                    factor_lists[k+1] = &op_term_reps[gn][p[k+1]]
                    #if len(factor_lists[k+1]) == 0: continue #WHAT???
                factor_lists[N+1] = &E_term_reps[p[N+1]]
                Einds = &E_term_indices[p[N+1]]

                #print "DB CYTHON: Order1 "
                innerloop_fn(factor_lists,Einds,&prps,nqubits) #, prps_chk)
                p[i] = 0

        elif order == 2:
            for i in range(N+2):
                p[i] = 2
                #inner loop(p)
                factor_lists[0] = &rho_term_reps[p[0]]
                for k in range(N):
                    gn = circuit[k]
                    factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
                    #if len(factor_lists[k+1]) == 0: continue # WHAT???
                factor_lists[N+1] = &E_term_reps[p[N+1]]
                Einds = &E_term_indices[p[N+1]]

                innerloop_fn(factor_lists,Einds,&prps,nqubits) #, prps_chk)
                p[i] = 0

            for i in range(N+2):
                p[i] = 1
                for j in range(i+1,N+2):
                    p[j] = 1
                    #inner loop(p)
                    factor_lists[0] = &rho_term_reps[p[0]]
                    for k in range(N):
                        gn = circuit[k]
                        factor_lists[k+1] = &op_term_reps[circuit[k]][p[k+1]]
                        #if len(factor_lists[k+1]) == 0: continue #WHAT???
                    factor_lists[N+1] = &E_term_reps[p[N+1]]
                    Einds = &E_term_indices[p[N+1]]

                    innerloop_fn(factor_lists,Einds,&prps,nqubits) #, prps_chk)
                    p[j] = 0
                p[i] = 0
        else:
            assert(False) # order > 2 not implemented yet...

    free(p)
    return prps



cdef void sb_pr_as_poly_innerloop(vector[vector_SBTermCRep_ptr_ptr] factor_lists, vector[INT]* Einds,
                                  vector[PolyCRep*]* prps, INT n): #, prps_chk):
    #print("DB partition = ","listlens = ",[len(fl) for fl in factor_lists])

    cdef INT i,j,Ei
    cdef double complex scale, val, newval, pLeft, pRight, p

    cdef INT incd
    cdef SBTermCRep* factor

    cdef INT nFactorLists = factor_lists.size() # may need to recompute this after fast-mode
    cdef INT* factorListLens = <INT*>malloc(nFactorLists * sizeof(INT))
    cdef INT last_index = nFactorLists-1

    for i in range(nFactorLists):
        factorListLens[i] = factor_lists[i].size()
        if factorListLens[i] == 0:
            free(factorListLens)
            return # nothing to loop over! - (exit before we allocate more)

    cdef PolyCRep coeff
    cdef PolyCRep result

    cdef INT namps = 1 # HARDCODED namps for SB states - in future this may be just the *initial* number
    cdef SBStateCRep *prop1 = new SBStateCRep(namps, n)
    cdef SBStateCRep *prop2 = new SBStateCRep(namps, n)
    cdef SBStateCRep *tprop
    cdef SBEffectCRep* EVec

    cdef INT* b = <INT*>malloc(nFactorLists * sizeof(INT))
    for i in range(nFactorLists): b[i] = 0

    assert(nFactorLists > 0), "Number of factor lists must be > 0!"

    #for factors in _itertools.product(*factor_lists):
    while(True):
        # In this loop, b holds "current" indices into factor_lists
        factor = deref(factor_lists[0])[b[0]] # the last factor (an Evec)
        coeff = deref(factor._coeff) # an unordered_map (copies to new "coeff" variable)

        for i in range(1,nFactorLists):
            coeff = coeff.mult( deref(deref(factor_lists[i])[b[i]]._coeff) )

        #pLeft / "pre" sim
        factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
        prop1.copy_from(factor._pre_state)
        for j in range(<INT>factor._pre_ops.size()):
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop
        for i in range(1,last_index):
            factor = deref(factor_lists[i])[b[i]]
            for j in range(<INT>factor._pre_ops.size()):
                factor._pre_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)

        # can't propagate effects, so effect's post_ops are constructed to act on *state*
        EVec = factor._post_effect
        for j in range(<INT>factor._post_ops.size()):
            rhoVec = factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        pLeft = EVec.amplitude(prop1)

        #pRight / "post" sim
        factor = deref(factor_lists[0])[b[0]] # 0th-factor = rhoVec
        prop1.copy_from(factor._post_state)
        for j in range(<INT>factor._post_ops.size()):
            factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        for i in range(1,last_index):
            factor = deref(factor_lists[i])[b[i]]
            for j in range(<INT>factor._post_ops.size()):
                factor._post_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)

        EVec = factor._pre_effect
        for j in range(<INT>factor._pre_ops.size()):
            factor._pre_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop # final state in prop1
        pRight = EVec.amplitude(prop1).conjugate()


        #Add result to appropriate poly
        result = coeff  # use a reference?
        result.scale(pLeft * pRight)
        final_factor_indx = b[last_index]
        Ei = deref(Einds)[final_factor_indx] #final "factor" index == E-vector index
        deref(prps)[Ei].add_inplace(result)

        #increment b ~ itertools.product & update vec_index_noop = np.dot(self.multipliers, b)
        for i in range(nFactorLists-1,-1,-1):
            if b[i]+1 < factorListLens[i]:
                b[i] += 1
                break
            else:
                b[i] = 0
        else:
            break # can't increment anything - break while(True) loop

    #Clenaup: free allocated memory
    del prop1
    del prop2
    free(factorListLens)
    free(b)
    return


cdef void sb_pr_as_poly_innerloop_savepartials(vector[vector_SBTermCRep_ptr_ptr] factor_lists,
                                               vector[INT]* Einds, vector[PolyCRep*]* prps, INT n): #, prps_chk):
    #print("DB partition = ","listlens = ",[len(fl) for fl in factor_lists])

    cdef INT i,j,Ei
    cdef double complex scale, val, newval, pLeft, pRight, p

    cdef INT incd
    cdef SBTermCRep* factor

    cdef INT nFactorLists = factor_lists.size() # may need to recompute this after fast-mode
    cdef INT* factorListLens = <INT*>malloc(nFactorLists * sizeof(INT))
    cdef INT last_index = nFactorLists-1

    for i in range(nFactorLists):
        factorListLens[i] = factor_lists[i].size()
        if factorListLens[i] == 0:
            free(factorListLens)
            return # nothing to loop over! (exit before we allocate anything else)

    cdef PolyCRep coeff
    cdef PolyCRep result

    cdef INT namps = 1 # HARDCODED namps for SB states - in future this may be just the *initial* number
    cdef vector[SBStateCRep*] leftSaved = vector[SBStateCRep_ptr](nFactorLists-1)  # saved[i] is state after i-th
    cdef vector[SBStateCRep*] rightSaved = vector[SBStateCRep_ptr](nFactorLists-1) # factor has been applied
    cdef vector[PolyCRep] coeffSaved = vector[PolyCRep](nFactorLists-1)
    cdef SBStateCRep *shelved = new SBStateCRep(namps, n)
    cdef SBStateCRep *prop2 = new SBStateCRep(namps, n) # prop2 is always a temporary allocated state not owned by anything else
    cdef SBStateCRep *prop1
    cdef SBStateCRep *tprop
    cdef SBEffectCRep* EVec

    cdef INT* b = <INT*>malloc(nFactorLists * sizeof(INT))
    for i in range(nFactorLists): b[i] = 0
    assert(nFactorLists > 0), "Number of factor lists must be > 0!"

    incd = 0

    #Fill saved arrays with allocated states
    for i in range(nFactorLists-1):
        leftSaved[i] = new SBStateCRep(namps, n)
        rightSaved[i] = new SBStateCRep(namps, n)

    #for factors in _itertools.product(*factor_lists):
    #for incd,fi in incd_product(*[range(len(l)) for l in factor_lists]):
    while(True):
        # In this loop, b holds "current" indices into factor_lists
        #print "DB: iter-product BEGIN"

        if incd == 0: # need to re-evaluate rho vector
            #print "DB: re-eval at incd=0"
            factor = deref(factor_lists[0])[b[0]]

            #print "DB: re-eval left"
            prop1 = leftSaved[0] # the final destination (prop2 is already alloc'd)
            prop1.copy_from(factor._pre_state)
            for j in range(<INT>factor._pre_ops.size()):
                #print "DB: re-eval left item"
                factor._pre_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
            rhoVecL = prop1
            leftSaved[0] = prop1 # final state -> saved
            # (prop2 == the other allocated state)

            #print "DB: re-eval right"
            prop1 = rightSaved[0] # the final destination (prop2 is already alloc'd)
            prop1.copy_from(factor._post_state)
            for j in range(<INT>factor._post_ops.size()):
                #print "DB: re-eval right item"
                factor._post_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop # swap prop1 <-> prop2
            rhoVecR = prop1
            rightSaved[0] = prop1 # final state -> saved
            # (prop2 == the other allocated state)

            #print "DB: re-eval coeff"
            coeff = deref(factor._coeff)
            coeffSaved[0] = coeff
            incd += 1
        else:
            #print "DB: init from incd"
            rhoVecL = leftSaved[incd-1]
            rhoVecR = rightSaved[incd-1]
            coeff = coeffSaved[incd-1]

        # propagate left and right states, saving as we go
        for i in range(incd,last_index):
            #print "DB: propagate left begin"
            factor = deref(factor_lists[i])[b[i]]
            prop1 = leftSaved[i] # destination
            prop1.copy_from(rhoVecL) #starting state
            for j in range(<INT>factor._pre_ops.size()):
                #print "DB: propagate left item"
                factor._pre_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop
            rhoVecL = prop1
            leftSaved[i] = prop1
            # (prop2 == the other allocated state)

            #print "DB: propagate right begin"
            prop1 = rightSaved[i] # destination
            prop1.copy_from(rhoVecR) #starting state
            for j in range(<INT>factor._post_ops.size()):
                #print "DB: propagate right item"
                factor._post_ops[j].acton(prop1,prop2)
                tprop = prop1; prop1 = prop2; prop2 = tprop
            rhoVecR = prop1
            rightSaved[i] = prop1
            # (prop2 == the other allocated state)

            #print "DB: propagate coeff mult"
            coeff = coeff.mult(deref(factor._coeff)) # copy a PolyCRep
            coeffSaved[i] = coeff

        # for the last index, no need to save, and need to construct
        # and apply effect vector
        prop1 = shelved # so now prop1 (and prop2) are alloc'd states

        #print "DB: left ampl"
        factor = deref(factor_lists[last_index])[b[last_index]] # the last factor (an Evec)
        EVec = factor._post_effect
        prop1.copy_from(rhoVecL) # initial state (prop2 already alloc'd)
        for j in range(<INT>factor._post_ops.size()):
            factor._post_ops[j].acton(prop1,prop2)
            tprop = prop1; prop1 = prop2; prop2 = tprop
        pLeft = EVec.amplitude(prop1) # output in prop1, so this is final amplitude

        #print "DB: right ampl"
        EVec = factor._pre_effect
        prop1.copy_from(rhoVecR)
        pRight = EVec.amplitude(prop1)
        #DEBUG print "  - begin: ",complex(pRight)
        for j in range(<INT>factor._pre_ops.size()):
            #DEBUG print " - state = ", [ prop1._smatrix[ii] for ii in range(2*2)]
            #DEBUG print "         = ", [ prop1._pvectors[ii] for ii in range(2)]
            #DEBUG print "         = ", [ prop1._amps[ii] for ii in range(1)]
            factor._pre_ops[j].acton(prop1,prop2)
            #DEBUG print " - action with ", [ (<SBOpCRep_Clifford*>factor._pre_ops[j])._smatrix_inv[ii] for ii in range(2*2)]
            #DEBUG print " - action with ", [ (<SBOpCRep_Clifford*>factor._pre_ops[j])._svector_inv[ii] for ii in range(2)]
            #DEBUG print " - action with ", [ (<SBOpCRep_Clifford*>factor._pre_ops[j])._unitary_adj[ii] for ii in range(2*2)]
            tprop = prop1; prop1 = prop2; prop2 = tprop
            pRight = EVec.amplitude(prop1)
            #DEBUG print "  - prop ",INT(j)," = ",complex(pRight)
            #DEBUG print " - post state = ", [ prop1._smatrix[ii] for ii in range(2*2)]
            #DEBUG print "              = ", [ prop1._pvectors[ii] for ii in range(2)]
            #DEBUG print "              = ", [ prop1._amps[ii] for ii in range(1)]

        pRight = EVec.amplitude(prop1).conjugate()

        shelved = prop1 # return prop1 to the "shelf" since we'll use prop1 for other things next

        #print "DB: final block: pLeft=",complex(pLeft)," pRight=",complex(pRight)
        #print "DB running coeff = ",dict(coeff._coeffs)
        #print "DB factor coeff = ",dict(factor._coeff._coeffs)
        result = coeff.mult(deref(factor._coeff))
        #print "DB result = ",dict(result._coeffs)
        result.scale(pLeft * pRight)
        final_factor_indx = b[last_index]
        Ei = deref(Einds)[final_factor_indx] #final "factor" index == E-vector index
        deref(prps)[Ei].add_inplace(result)
        #print "DB prps[",INT(Ei),"] = ",dict(deref(prps)[Ei]._coeffs)

        #assert(debug < 100) #DEBUG
        #print "DB: end product loop"

        #increment b ~ itertools.product & update vec_index_noop = np.dot(self.multipliers, b)
        for i in range(nFactorLists-1,-1,-1):
            if b[i]+1 < factorListLens[i]:
                b[i] += 1; incd = i
                break
            else:
                b[i] = 0
        else:
            break # can't increment anything - break while(True) loop

    #Cleanup: free allocated memory
    for i in range(nFactorLists-1):
        del leftSaved[i]
        del rightSaved[i]
    del prop2
    del shelved
    free(factorListLens)
    free(b)
    return


## You can also typedef pointers too
#
#ctypedef INT * int_ptr
#
#
#ctypedef int (* no_arg_c_func)(BaseThing)
#cdef no_arg_c_func funcs[1000]
#
#ctypedef void (*cfptr)(int)
#
## then we use the function pointer:
#cdef cfptr myfunctionptr = &myfunc

def dot(np.ndarray[double, ndim=1] f, np.ndarray[double, ndim=1] g):
    cdef INT N = f.shape[0]
    cdef float ret = 0.0
    cdef INT i
    for i in range(N):
        ret += f[i]*g[i]
    return ret
