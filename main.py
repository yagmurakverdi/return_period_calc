import sys

import xarray as xr

data_files = {
    '26-50-8.5': 'Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc',
    '22-23': 'pr_2023_daily.nc',
}

data_path = './data/'


def open_data_file(f):
    """This opens the nc file"""
    if f in data_files:
        file_path = data_path + data_files[f]
    else:
        print('choose a proper file', str(data_files))
        return False
    nc_data = xr.open_dataset(file_path)
    return nc_data


def process_data(d):
    """This is the beginning of the process"""
    # with nc_data as fr:
    print(list(d.keys()))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fkey = '26-50-8.5'
    print('opening file >', fkey)
    nc_data = open_data_file(fkey)
    if not nc_data:
        print('error')
        sys.exit(1)
    print('start processing >', fkey)
    process_data(nc_data)
    # print(nc_data)
