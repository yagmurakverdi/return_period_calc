import sys

import xarray as xr
import numpy as np
import pandas as pd

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
    """This is the beginning of the process"""
    data_type = data_files[key]['data_type']

    # with nc_data as fr:
    print(list(d.keys()))
    # print(list(d.keys()))  # ['time_bnds', 'crs', 'pr']

    # Lat - Lon Process
    lat = d['xlat'][:]  # Latitude on Cross Points
    lon = d['xlon'][:]  # Longitude on Cross Points
    nlon = np.size(lon)
    nlat = np.size(lat)
    lat_min_value = lat["xlat"].values.min()
    lat_max_value = lat["xlat"].values.max()
    lon_min_value = lon["xlon"].values.min()
    lon_max_value = lon["xlon"].values.max()

    # Time Process

    # Date Process
    # TODO check if we can use time_bnds
    dates_all = d['time'][:]  # get times - type is datetime64
    dates_all_size = np.size(dates_all)  # get size of times

    debug_me('dates_all', dates_all)

    if data_type == '3hrs':
        # converts format to daily
        # TODO check here
        dates_all = pd.to_datetime(dates_all, format='%Y-%m-%dT%H:%M:%S.%f')
        dates_all = [dt.strftime('%Y%m%d') for dt in dates_all]

    unique_dates = np.unique(dates_all)  # get unique dates - when it is daily all are unique
    debug_me('unique_dates', unique_dates)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data_file = '26-50-8.5-daily'
    # data_file = '26-50-8.5-3hrs'
    # data_file = '22-23-daily'
    print('opening file >', data_file)
    nc_data = open_data_file(data_file)
    if not nc_data:
        print('error')
        sys.exit(1)
    print('start processing >', data_file)
    process_data(nc_data, data_file)
    # print(nc_data)
