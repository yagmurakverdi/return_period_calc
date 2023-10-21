import xarray as xr


def open_data_file():
    file_path = "./data/yagmur_Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc"
    nc_data = xr.open_dataset(file_path)
    return nc_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nc_data = open_data_file()
    # print('nc_data >>>')
    print(nc_data)
    # print('===========')
