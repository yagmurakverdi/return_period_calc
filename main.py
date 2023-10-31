import sys

import xarray as xr
import numpy as np
import pandas as pd
import mevpy as mev
from xarray import apply_ufunc

from utility import save_file, debug_me

data_path = './data/'
data_files = {
    '26-50-8.5-daily': {'name': 'Turkey_MPI_85_dn_STS.2026-2050_pr_daily.nc', 'data_type': 'daily'},
    '26-50-8.5-3hrs': {'name': 'Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc', 'data_type': '3hrs'},
    '22-23-daily': {'name': 'pr_2023_daily.nc', 'data_type': 'daily'},
}

threshold = 1
min_n_excesses = 3


def open_data_file(f):
    """This opens the nc file"""
    if f in data_files:
        file_path = data_path + data_files[f]['name']
    else:
        print('choose a proper file', str(data_files))
        return False
    nc_data = xr.open_dataset(file_path)
    return nc_data


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


def process_data(d, key):
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

    # calculate max rainfall for each year
    print('calculating max_rainfall...')
    max_rainfall = d['pr'].groupby('year').max(dim='time')
    max_rainfall.attrs['standard_name'] = 'max_precipitation_flux'
    max_rainfall.attrs['long_name'] = 'Max precipitation flux'
    max_rainfall.attrs['cell_methods'] = 'time: max'
    # debug_me('max_rainfall', max_rainfall)
    print('done...')

    # Save to a netCDF file
    max_rainfall.to_netcdf('./out/max_rainfall_2026-2050-4.nc')
    print('max rainfall written to file')

    # Begin Calculating N, C, W values
    # Applying the function to each lon, lat, and year
    print('calculating n, c, w')
    ncw = apply_ufunc(
        wrapper_wei_fit_pwm,
        d['pr'].groupby('year'),
        input_core_dims=[['time']],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        output_core_dims=[["parameter"]]
    )
    ncw = ncw.assign_coords(parameter=["n", "c", "w"])
    print('done...')
    # debug_me('result', result)

    # Write to NetCDF file
    # TODO write summary, description and units etc to ncw data set
    ncw.to_netcdf('./out/NCW_2026-2050-4.nc')
    print('n, c, w written to file')

    # Calculating csi, psi and mu
    # Applying the function to each lon and lat for all years
    print('calculating gev_fit (csi, psi, mu) from max rainfall')
    gev_max = apply_ufunc(
        wrapper_gev_fit_lmom,
        max_rainfall,
        input_core_dims=[['year']],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        output_core_dims=[["parameter"]]
    )

    gev_max = gev_max.assign_coords(parameter=["csi", "psi", "mu"])
    print('done...')
    # debug_me('gev_max', gev_max)

    # Write to NetCDF file
    # TODO write summary, description and units etc to ncw data set
    gev_max.to_netcdf('./out/GEV_MAX_2026-2050-4.nc')
    print('gev fit (csi, psi, mu) written to file...')


if __name__ == '__main__':
    # data_file = '26-50-8.5-3hrs'  # currently we don't need this
    data_file = '26-50-8.5-daily'
    # data_file = '22-23-daily'
    print('opening file >', data_file)
    nc_data = open_data_file(data_file)
    if not nc_data:
        print('error')
        sys.exit(1)
    print('start processing >', data_file)
    process_data(nc_data, data_file)
    print('completed...')
    # print(nc_data)
