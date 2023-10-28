import numpy as np
import json
from json import JSONEncoder

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
