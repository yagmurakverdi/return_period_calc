import os
import sys

import numpy as np
import json
import xarray as xr

from json import JSONEncoder

from constants import data_files, data_path, out_path

debug_mode = True


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def save_file(fname, var):
    with open(f'./out/{fname}.json', 'w') as f:
        json.dump(var, f, cls=NumpyArrayEncoder)


def debug_me(key, val, force=False):
    if debug_mode or force:
        print(f'{key}\n=========')
        print(val)
        print('\n=========\n')


def save_nc(fname, nc):
    file_path = f'{out_path}{fname}.nc'
    if os.path.exists(file_path):
        os.remove(file_path)
    nc.to_netcdf(file_path)
    print(f'{fname} written to file')


def open_data_file(f):
    """This opens the nc file"""
    if f in data_files:
        file_path = f"{data_path}{data_files[f]['name']}"
    else:
        print('choose a proper file', str(data_files))
        return False
    nc_data = xr.open_dataset(file_path)
    return nc_data


def open_calculated_file(fname):
    file_path = f'{out_path}{fname}.nc'
    if os.path.exists(file_path):
        try:
            nc = xr.open_dataset(file_path)
        except Exception as e:
            print('File open error', str(e))
            sys.exit(1)
        return nc
    print(f'File {file_path} does not exists')
    sys.exit(1)
