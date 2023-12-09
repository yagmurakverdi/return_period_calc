import numpy as np
import scipy.stats as stats
from xarray import apply_ufunc


def wrapper_lognorm_fit(sample):
    # clear NaN data and only use the positive values
    data = np.array(sample)
    data = data[np.logical_and(data > 0, ~np.isnan(data))]

    # If the data is enough start the fitting
    if len(data) > 0:
        # with floc=0 we fix the location value
        shape, loc, scale = stats.lognorm.fit(data, floc=0)
    else:
        shape, loc, scale = np.nan, np.nan, np.nan

    return np.array([shape, scale])


def calculate_lognorm_fit(d):
    print('calculating lognorm fit')
    lf = apply_ufunc(
        wrapper_lognorm_fit,
        d['pr'],
        input_core_dims=[['time']],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        output_core_dims=[["parameter"]]
    )
    lf = lf.assign_coords(parameter=["shape", "scale"])
    print('done...')
    return lf


def wrapper_lognorm_icdf(shape_in, scale_in, return_periods_in):
    # calculate ICDF for the return periods
    return_periods_in = np.array(return_periods_in)
    quantiles = 1 - 1 / return_periods_in
    return stats.lognorm.ppf(quantiles, shape_in, scale=scale_in)


def calculate_lognorm_icdf(d, rp):
    print('calculating lognorm icdf')
    rp_pr = apply_ufunc(
        wrapper_lognorm_icdf,
        d.sel(parameter="shape"),
        d.sel(parameter="scale"),
        input_core_dims=[[], []],
        output_core_dims=[["return_periods"]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[float],
        kwargs={"return_periods_in": rp}
    )
    rp_pr = rp_pr.assign_coords(return_periods=rp)
    print('done...')
    return rp_pr
