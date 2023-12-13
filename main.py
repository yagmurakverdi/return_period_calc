import sys
import time

import matplotlib.colors as mcolors
from matplotlib import pyplot as plt
import numpy as np

from common import filter_by_threshold, crop_data_by_degree
from lognorm import calculate_lognorm_fit, calculate_lognorm_icdf
from plotter import plot_data
from utility import open_data_file, save_nc
from constants import threshold, return_periods_day

if __name__ == '__main__':
    print('Return Period Calculator')
    print('========================')
    time_start = time.time()

    # data_file = '26-50-8.5-daily'
    data_file = '76-00-daily'
    print('opening file >', data_file)
    nc_data = open_data_file(data_file)

    if not nc_data:
        print('error')
        sys.exit(1)
    print('start processing >', data_file)

    # filter by threshold
    filtered_data = filter_by_threshold(nc_data, threshold)

    cropped_data = crop_data_by_degree(filtered_data)

    lognorm_f_data = calculate_lognorm_fit(cropped_data)
    save_nc(f'{data_file}-lognorm_fit-cropped', lognorm_f_data)

    icdf_rp_data = calculate_lognorm_icdf(lognorm_f_data, return_periods_day)
    save_nc(f'{data_file}-lognorm_fit-cropped-icdf-rp', icdf_rp_data)

    # Define a custom modification of the YlGnBu colormap
    # custom_cmap = 'YlGnBu'
    original_cmap = plt.cm.YlGnBu
    custom_cmap = mcolors.LinearSegmentedColormap.from_list(
        'truncated_YlGnBu',
        original_cmap(np.linspace(0, 0.80, 256))
    )

    for rp in range(len(return_periods_day)):
        period = return_periods_day[rp]
        years = int(period / 365)
        period_data = icdf_rp_data[:, :, rp]
        label = f'{years} year rainfall accumulation [mm]'
        title = f'{years} year Return Period Map'
        fname = f'./out/{data_file}-cropped-{years}_yr_rp.jpg'

        plot_data(period_data, label, title, fname, custom_cmap)

    time_end = time.time()
    print(f'completed in {round((time_end - time_start) / 60, 2)} mins')
    # sys.exit(0)
