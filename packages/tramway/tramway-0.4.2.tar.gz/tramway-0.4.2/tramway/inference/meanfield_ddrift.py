# -*- coding: utf-8 -*-

# Copyright © 2019, Institut Pasteur
#   Contributor: François Laurent

# This file is part of the TRamWAy software available at
# "https://github.com/DecBayComp/TRamWAy" and is distributed under
# the terms of the CeCILL license as circulated at the following URL
# "http://www.cecill.info/licenses.en.html".

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.


from .base import *
from .gradient import get_grad_kwargs, setup_with_grad_arguments
from math import *
import numpy as np
import pandas as pd
from collections import OrderedDict


setup = {'name': ('meanfield.dd', 'meanfield.ddrift'),
        'provides': ('dd', 'ddrift'),
        'arguments': OrderedDict((
            #('localization_error',  ('-e', dict(type=float, help='localization precision (see also sigma; default is 0.03)'))),
            ('diffusivity_prior',   ('-d', dict(type=float, help='prior on the diffusivity'))),
            ('drift_prior',         dict(type=float, help='prior on the amplitude of the drift')),
            ('diffusivity_time_prior',  ('--time-d', dict(type=float, help='prior on the temporal variations of the diffusivity'))),
            ('drift_time_prior',        dict(type=float, help='prior on the temporal variations of drift amplitude')),
            ('verbose',         ()))),
        'default_rgrad':    'delta0'}
#setup_with_grad_arguments(setup)


def infer_meanfield_DD(cells, diffusivity_spatial_prior=None, drift_spatial_prior=None,
        diffusivity_time_prior=None, drift_time_prior=None,
        diffusivity_prior=None, drift_prior=None,
        diffusion_prior=None, diffusion_spatial_prior=None, diffusion_time_prior=None,
        dt=None, tol=1e-6, verbose=True, **kwargs):
    """
    """
    grad_kwargs = get_grad_kwargs(kwargs)
    #localization_error = cells.get_localization_error(kwargs, 0.03, True)
    index, reverse_index, n, dt_mean, _, _, _, _ = \
        smooth_infer_init(cells, sigma2=0)#localization_error)
    if dt is None:
        dt = dt_mean
    elif np.isscalar(dt):
        dt = np.full_like(dt_mean, dt)

    if diffusivity_prior is None:
        diffusivity_prior = diffusion_prior
    if diffusivity_spatial_prior is None:
        if diffusion_spatial_prior is None:
            diffusivity_spatial_prior = diffusivity_prior
        else:
            diffusivity_spatial_prior = diffusion_spatial_prior
    if diffusivity_time_prior is None:
        diffusivity_time_prior = diffusion_time_prior

    if drift_spatial_prior is None:
        drift_spatial_prior = drift_prior
    if drift_time_prior is None:
        drift_time_prior = drift_prior
    mu_spatial_prior, mu_time_prior = drift_spatial_prior, drift_time_prior

    spatial_reg = diffusivity_spatial_prior or drift_spatial_prior
    time_reg = diffusivity_time_prior or drift_time_prior
    reg = spatial_reg or time_reg

    index = np.array(index)
    ok = 1<n
    #print(ok.size, np.sum(ok))
    if not np.all(ok):
        reverse_index[index] -= np.cumsum(~ok)
        reverse_index[index[~ok]] = -1
        index, n, dt = index[ok], n[ok], dt[ok]

    dr, chi2 = [], []
    if reg:
        reg_Z = []
        time_reg_Z = []
        ones = np.ones(n.size, dtype=dt.dtype)
    for _i, i in enumerate(index):
        # local variables
        dr_mean = np.mean(cells[i].dr, axis=0, keepdims=True)
        dr_centered = cells[i].dr - dr_mean
        dr2 = np.sum(dr_centered * dr_centered, axis=1)
        dr.append(dr_mean)
        chi2.append(np.sum(dr2))
        # regularization constants
        if reg:
            ones[_i] = 0.
            if spatial_reg:
                _grad = cells.rgrad(i, ones, reverse_index)#, **grad_kwargs)
                reg_Z.append( 0. if _grad is None else np.nansum(_grad) )
            if time_reg:
                _ddt = cells.temporal_variation(i, ones, reverse_index)
                time_reg_Z.append( 0. if _ddt is None else np.mean(_ddt * _ddt) )
            ones[_i] = 1.
    dr = np.vstack(dr)
    chi2 = np.array(chi2)
    if reg:
        reg_Z = np.array(reg_Z)
        time_reg_Z = np.array(time_reg_Z)

    aD = chi2 / (4. * n * dt)
    a_mu = dr
    bD = n / (aD * aD)
    b_mu = n / (2. * dt * aD)

    # priors
    #sumC = np.array([ np.sum(_C) for _C in C ])
    if diffusivity_spatial_prior or diffusivity_time_prior:
        AD = aD / (2. * bD)
        BD = bD # no need for copying
        # do not scale time;
        # assume constant window shift and let time_prior hyperparameters bear all the responsibility
        D_spatial_penalty = []
        D_time_penalty = []
        for _i, i in enumerate(index):
            aD_i, aD[_i] = aD[_i], 0.
            if diffusivity_spatial_prior is not None:
                delta_aD = cells.rgrad(i, aD, reverse_index)
                delta_aD = 0. if delta_aD is None else -np.nansum(delta_aD)
                D_spatial_penalty.append(delta_aD)
            if diffusivity_time_prior is not None:
                ddt_aD = cells.temporal_variation(i, aD, reverse_index)
                ddt_aD = 0. if ddt_aD is None else -np.nansum(ddt_aD)
                D_time_penalty.append(ddt_aD)
            aD[_i] = aD_i
        if diffusivity_spatial_prior is not None:
            AD -= diffusivity_spatial_prior * np.array(D_spatial_penalty)
            BD -= 2. * diffusivity_spatial_prior * reg_Z
        if diffusivity_time_prior is not None:
            AD -= diffusivity_time_prior * np.array(D_time_penalty)
            BD -= 2. * diffusivity_time_prior * time_reg_Z
        AD /= BD / 2.
        aD, bD = AD, BD
    if mu_spatial_prior or mu_time_prior:
        A_mu = a_mu / (2. * b_mu)[:,np.newaxis]
        B_mu = b_mu # no need for copying
        mu_spatial_penalty = []
        mu_time_penalty = []
        for _i, i in enumerate(index):
            a_i, a_mu[_i] = a_mu[_i], 0.
            if mu_spatial_prior is not None:
                delta_a_mu = []
                for d in range(cells.dim):
                    delta_d = cells.rgrad(i, a_mu[:,d], reverse_index)
                    delta_d = 0. if delta_d is None else -np.nansum(delta_d)
                    delta_a_mu.append(delta_d)
                mu_spatial_penalty.append(delta_a_mu)
            if mu_time_prior is not None:
                ddt_a_mu = []
                for d in range(cells.dim):
                    ddt_d = cells.temporal_variation(i, a_mu[:,d], reverse_index)
                    ddt_d = 0. if ddt_d is None else -np.nansum(ddt_d)
                    ddt_a_mu.append(ddt_d)
                mu_time_penalty.append(ddt_a_mu)
            a_mu[_i] = a_i
        if mu_spatial_prior is not None:
            A_mu -= mu_spatial_prior * np.array(mu_spatial_penalty)
            B_mu -= 2. * mu_spatial_prior * reg_Z
        if mu_time_prior is not None:
            A_mu -= mu_time_prior * np.array(mu_time_penalty)
            B_mu -= 2. * mu_time_prior * time_reg_Z
        A_mu /= (B_mu / 2.)[:,np.newaxis]
        a_mu, b_mu = A_mu, B_mu

    D, drift = aD, a_mu / dt[:,np.newaxis]

    DD = pd.DataFrame(np.hstack((D[:,np.newaxis], drift)), index=index, \
        columns=[ 'diffusivity' ] + \
            [ 'drift ' + col for col in cells.space_cols ])

    return DD


__all__ = ['setup', 'infer_meanfield_DD']

