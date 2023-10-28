import sys

import xarray as xr
import numpy as np
import pandas as pd
import mevpy as mev

from utility import save_file, debug_me

data_path = './data/'
data_files = {
    '26-50-8.5-daily': {'name': 'Turkey_MPI_85_dn_STS.2026-2050_pr_daily.nc', 'data_type': 'daily'},
    '26-50-8.5-3hrs': {'name': 'Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc', 'data_type': '3hrs'},
    '22-23-daily': {'name': 'pr_2023_daily.nc', 'data_type': 'daily'},
}


def open_data_file(f):
    """This opens the nc file"""
    if f in data_files:
        file_path = data_path + data_files[f]['name']
    else:
        print('choose a proper file', str(data_files))
        return False
    nc_data = xr.open_dataset(file_path)
    return nc_data


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

    # data_type = data_files[key]['data_type']

    # Lat & Lon
    lat = d['xlat'][:]  # Latitude on Cross Points
    lon = d['xlon'][:]  # Longitude on Cross Points

    # Time and Year
    time_series = pd.Series(d['time'])
    unique_days = time_series.dt.date.astype(str).tolist()
    unique_days = list(set(unique_days))
    unique_days.sort()

    # if data_type == '3hrs':
    #     hours = d['time'][:]  # time
    #     debug_me('hours', hours)
    #     # TODO convert 3hrs to daily

    # Precipitation Data
    prcp_mat = d['pr']  # Total precipitation flux

    # Variables
    threshold = 1  # threshold for computing excesses over threshold = ordinary events
    # min_yearly_dates = 300  # do not compute parameters for years with less than 330 files
    # min_n_excesses = 3  # min yearly number of ordinary events
    # min_n_obs = 300  # min number of non-missing daily totals in any year

    print('starting the calculations')
    lon_size = lon.size
    lat_size = lat.size
    for ix in range(lon_size):
        for iy in range(lat_size):
            prcp = prcp_mat[:, ix, iy]  # total precip for the given lon and lat

            debug_me('len prcp', len(prcp))
            debug_me('len year', len(unique_days))
            df = pd.DataFrame({'PRCP': prcp, 'YEAR': unique_days})

            XI, Fi, TR, NCW = mev.table_rainfall_maxima(df, how='pwm', thresh=threshold)

            debug_me('XI', XI)
            debug_me('Fi', Fi)
            debug_me('TR', TR)
            debug_me('NCW', NCW)

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
    # print(nc_data)
