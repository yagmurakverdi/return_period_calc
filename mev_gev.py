"""
Mev and Gev calculations using MevPy library
"""
import numpy as np
from xarray import apply_ufunc

import mevpy as mev
from constants import threshold, min_n_excesses


def wrapper_wei_fit_pwm(sample):
    # print('> ', end='')
    data0 = np.array(sample)
    enough_data_mask = np.logical_and(data0 >= 0, ~np.isnan(data0))
    data = data0[enough_data_mask]
    excesses = data[data > threshold] - threshold
    if len(excesses) > min_n_excesses:
        # print(len(excesses))
        n, c, w = mev.wei_fit_pwm(sample)
    else:
        # print('nan')
        n, c, w = np.NAN, np.NAN, np.NAN

    return np.array([n, c, w])


def wrapper_gev_fit_lmom(sample):
    csi, psi, mu = mev.gev_fit_lmom(sample)
    return np.array([csi, psi, mu])


def wrapper_mev_quant(n, c, w, rp):
    hmev = np.zeros(len(rp))
    x0 = np.median(c)

    for index, period in enumerate(rp):
        # x0 = 2 * period / 10 * np.mean(c)
        # x0 = 50
        fi = 1 - 1 / period
        hmev[index] = mev.mev_quant(fi, x0, n, c, w, potmode=True, thresh=1)[0]

    return hmev


def wrapper_gev_quant(csi, psi, mu, rp):
    hgev = np.zeros(len(rp))

    for index, period in enumerate(rp):
        fi = 1 - 1 / period
        hgev[index] = mev.gev_quant(fi, csi, psi, mu)

    return hgev


def calculate_max_rainfall(d):
    # calculate max rainfall for each year
    print('calculating max_rainfall...')
    max_rainfall = d['pr'].groupby('year').max(dim='time')
    max_rainfall.attrs['standard_name'] = 'max_precipitation_flux'
    max_rainfall.attrs['long_name'] = 'Max precipitation flux'
    max_rainfall.attrs['cell_methods'] = 'time: max'
    # debug_me('max_rainfall', max_rainfall)
    print('done...')

    return max_rainfall


def calculate_ncw(d):
    # Begin Calculating N, C, W values
    # Applying the function to each lon, lat, and year
    print('calculating n, c, w')
    ncw_fit = apply_ufunc(
        wrapper_wei_fit_pwm,
        d['pr'].groupby('year'),
        input_core_dims=[['time']],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        output_core_dims=[["parameter"]]
    )
    ncw_fit = ncw_fit.assign_coords(parameter=["n", "c", "w"])
    # TODO write summary, description and units etc to data set
    print('done...')
    return ncw_fit


def calculate_gev_max(d):
    # Calculating csi, psi and mu
    # Applying the function to each lon and lat for all years
    print('calculating gev_fit (csi, psi, mu) from max rainfall')
    gev_m = apply_ufunc(
        wrapper_gev_fit_lmom,
        d,
        input_core_dims=[['year']],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        output_core_dims=[["parameter"]]
    )

    gev_m = gev_m.assign_coords(parameter=["csi", "psi", "mu"])
    # TODO write summary, description and units etc to data set
    print('done...')
    # debug_me('gev_max', gev_max)
    return gev_m


def calculate_hmev(d, rp):
    # Calculating mev quant (hmev)
    print('calculating mev_quant (hmev) over return periods')
    hm = apply_ufunc(
        wrapper_mev_quant,
        d.sel(parameter='n'),
        d.sel(parameter='c'),
        d.sel(parameter='w'),
        rp,
        input_core_dims=[[], [], [], ['return_period']],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        # output_dtypes=[np.float64]  # Ensure this is a list of dtypes, not an array
        output_core_dims=[["return_period"]]
    )
    hm = hm.assign_coords(return_period=rp)
    # TODO write summary, description and units etc to data set
    return hm


def calculate_hgev(d, rp):
    # Calculating gev quant (hgev)
    print('calculating gev_quant (hgev) over return periods')
    hg = apply_ufunc(
        wrapper_gev_quant,
        d.sel(parameter='csi'),
        d.sel(parameter='psi'),
        d.sel(parameter='mu'),
        rp,
        input_core_dims=[[], [], [], ['return_period']],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        # output_dtypes=[np.float64]  # Ensure this is a list of dtypes, not an array
        output_core_dims=[["return_period"]]
    )
    hg = hg.assign_coords(return_period=rp)
    # TODO write summary, description and units etc to data set
    return hg
