import sys

import xarray as xr

data_files = {
    '26-50-8.5': 'Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc',
    '22-23': 'pr_2023_daily.nc',
}

data_path = './data/'


def open_data_file(f):
    if f in data_files:
        file_path = data_path + data_files[f]
    else:
        print('choose a proper file', str(data_files))
        return False
    nc_data = xr.open_dataset(file_path)
    return nc_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nc_data = open_data_file('26-50-8.5')
    if not nc_data:
        print('error')
        sys.exit(1)
    print(nc_data)
