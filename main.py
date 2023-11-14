import sys
import time

import numpy as np
import mevpy as mev
from xarray import apply_ufunc

from constants import threshold, min_n_excesses, use_existing, return_period
from utility import debug_me, save_nc, open_data_file, open_calculated_file


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


def assign_year_coord(d):
    """This is the main process where we prepare and run the data

    Data Files General Info
    'time_bnds' - daily times
    'crs' - coordinates w/ GeoX GeoY
    'pr'
        standard_name:  precipitation_flux
        long_name:      Mean total precipitation flux
        units:          kg m-2 s-1
        grid_mapping:   crs
        cell_methods:   time: mean
    'xlon'
        standard_name:        longitude
        long_name:            Longitude on Cross Points
        units:                degrees_east
    'xlat'
        standard_name:        latitude
        long_name:            Latitude on Cross Points
        units:                degrees_north
    """
    # creates another year coordinate in relation with time
    d = d.assign_coords(year=d['time'].dt.year)
    # converts timestamp to string YYYY-MM-DD
    d['time'] = d['time'].dt.strftime('%Y-%m-%d')
    return d


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


if __name__ == '__main__':
    # data_file = '26-50-8.5-3hrs'  # currently we don't need this
    data_file = '26-50-8.5-daily'
    # data_file = '22-23-daily'
    time_start = time.time()
    print('opening file >', data_file)
    nc_data = open_data_file(data_file)
    if not nc_data:
        print('error')
        sys.exit(1)
    print('start processing >', data_file)

    # TODO make the below to work with all years
    if not use_existing:
        # If we don't already have the calculated files
        print('start calculating data...')
        ds = assign_year_coord(nc_data)
        max_rainfall = calculate_max_rainfall(ds)
        save_nc('max_rainfall_2026-2050-4', max_rainfall)
        ncw = calculate_ncw(ds)
        save_nc('NCW_2026-2050-4', ncw)
        gev_max = calculate_gev_max(max_rainfall)
        save_nc('GEV_MAX_2026-2050-4', gev_max)
        hmev = calculate_hmev(ncw, return_period)
        save_nc('HMEV_2026-2050-4', hmev)
    else:
        print('gather existing data...')
        # TODO check if we need below line
        ds = assign_year_coord(nc_data)
        max_rainfall = open_calculated_file('max_rainfall_2026-2050-4')
        ncw = open_calculated_file('NCW_2026-2050-4')
        gev_max = open_calculated_file('GEV_MAX_2026-2050-4')
        hmev = open_calculated_file('HMEV_2026-2050-4')

    time_end = time.time()
    print(f'completed in {(time_end - time_start) / 60} mins')
    # print(nc_data)
