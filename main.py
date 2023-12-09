import sys
import time

from common import filter_by_threshold
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
    f_data = filter_by_threshold(nc_data, threshold)

    lognorm_f_data = calculate_lognorm_fit(f_data)
    save_nc(f'{data_file}-lognorm_fit', lognorm_f_data)

    icdf_rp_data = calculate_lognorm_icdf(lognorm_f_data, return_periods_day)
    save_nc(f'{data_file}-lognorm_fit-icdf-rp', icdf_rp_data)

    for rp in range(len(return_periods_day)):
        period = return_periods_day[rp]
        years = int(period / 365)
        period_data = icdf_rp_data[:, :, rp]
        label = f'{years} year rainfall accumulation [mm]'
        title = f'{years} year Return Period Map'
        fname = f'./out/{data_file}-{years}_yr_rp.jpg'

        plot_data(period_data, label, title, fname, 'YlGnBu')

    time_end = time.time()
    print(f'completed in {round((time_end - time_start) / 60, 2)} mins')
    # sys.exit(0)
