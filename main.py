import sys
import time

from common import filter_by_threshold, crop_data_by_degree
from lognorm import calculate_lognorm_fit, calculate_lognorm_icdf
from plotter import plot_data
from utility import open_data_file, save_nc, open_calculated_file
from constants import threshold, return_periods_day, data_files, crop_degrees, custom_cmap

if __name__ == '__main__':
    print('Return Period Calculator')
    print('========================')
    time_start = time.time()

    ans = input('Do you want to run all the data? (y/n) ')
    if ans not in ['y', 'n']:
        print('wrong answer, it must be either y or n exiting...')
        sys.exit(1)
    if ans == 'y':
        print('the plots will be redrawn...')
        use_existing = False
        use_existing_plot = False
    else:
        use_existing = True
        ans = input('Do you want to plot all the return periods? (y/n) ')
        if ans not in ['y', 'n']:
            print('wrong answer, it must be either y or n exiting...')
            sys.exit(1)
        if ans == 'y':
            use_existing_plot = False
        else:
            use_existing_plot = True

    if not use_existing:
        print('calculating all the data')
        for data_file in data_files:
            print('\nprocessing file >', data_file, '>', data_files[data_file]['name'], '>>>')
            nc_data = open_data_file(data_file)
            print('> start processing >', data_file)

            # prepare the data
            print('> filtering by threshold:', threshold)
            filtered_data = filter_by_threshold(nc_data, threshold)
            print('> cropping edge data by:', crop_degrees, 'degrees')
            cropped_data = crop_data_by_degree(filtered_data, crop_degrees)

            # log fit and save
            lognorm_f_data = calculate_lognorm_fit(cropped_data)
            data_files[data_file]['log-fit'] = lognorm_f_data
            save_nc(f'{data_file}-lognorm_fit', lognorm_f_data)

            icdf_rp_data = calculate_lognorm_icdf(lognorm_f_data, return_periods_day)
            data_files[data_file]['icdf-rp'] = icdf_rp_data
            save_nc(f'{data_file}-lognorm_fit-icdf_rp', icdf_rp_data)

            print('> plotting all the return periods')
            for rp in range(len(return_periods_day)):
                period = return_periods_day[rp]
                years = int(period / 365)
                print('> return period >', years)
                period_data = icdf_rp_data[:, :, rp]
                label = f'{years} year precipitation accumulation [mm]'
                title = f'{years} year Return Period Map'
                fname = f'{data_file}-{years}_yr-rp'
                plot_data(period_data, label, title, fname, custom_cmap)
    else:
        print('using existing data in ./out/data')
        for data_file in data_files:
            print('\nretrieving file >', data_file, 'lognorm_fit >>>')
            log_fit_data = open_calculated_file(f'{data_file}-lognorm_fit')
            data_files[data_file]['log-fit'] = log_fit_data
            print('retrieving file >', data_file, 'icdf_rp >>>')
            icdf_data = open_calculated_file(f'{data_file}-lognorm_fit-icdf_rp')
            data_files[data_file]['icdf-rp'] = icdf_data

            if use_existing_plot:
                print('> you can find the pre-drawn plots in ./out/plot')
            else:
                print('> plotting all the return periods')
                for rp in range(len(return_periods_day)):
                    period = return_periods_day[rp]
                    years = int(period / 365)
                    print('> return period >', years)
                    if use_existing:
                        period_data = icdf_data['pr'][:, :, rp]
                    else:
                        period_data = icdf_data[:, :, rp]
                    label = f'{years} year precipitation accumulation [mm]'
                    title = f'{years} year Return Period Map'
                    fname = f'{data_file}-{years}_yr-rp'
                    plot_data(period_data, label, title, fname, custom_cmap)

    if not use_existing:
        hist_icdf_data = None
        for data_file in data_files:
            if data_files[data_file]['data_type'] == 'historic':
                hist_icdf_data = data_files[data_file]['icdf-rp']
                break
        if hist_icdf_data is None:
            print('there is something wrong with reading historic data')
            sys.exit(1)
        for data_file in data_files:
            if data_files[data_file]['data_type'] == 'historic':
                continue
            print(f'\nstart calculating change for {data_file} >>>')
            cur_icdf_data = data_files[data_file]['icdf-rp']
            for rp in range(len(return_periods_day)):
                period = return_periods_day[rp]
                years = int(period / 365)
                print(f'> calculating change for {data_file} @ {years} rp')
                if use_existing:
                    hist_period_data = hist_icdf_data['pr'][:, :, rp]
                    cur_period_data = cur_icdf_data['pr'][:, :, rp]
                else:
                    hist_period_data = hist_icdf_data[:, :, rp]
                    cur_period_data = cur_icdf_data[:, :, rp]
                change_period_data = ((cur_period_data - hist_period_data) / hist_period_data)*100
                data_files[data_file][f'{years}-rp-ch'] = change_period_data
                save_nc(f'{data_file}-{years}_yr-rp_change', change_period_data)
                print(f'> plotting change for {data_file} @ {years} rp')
                label = f'Percentage Change in Precipitation over {years} Years'
                title = f'{years} year Changing Return Period Map'
                fname = f'{data_file}-change-{years}_yr-rp'
                plot_data(change_period_data, label, title, fname, 'BrBG', 'change')
    else:
        for data_file in data_files:
            if data_files[data_file]['data_type'] == 'historic':
                continue

            print(f'\n> retrieving {data_file} return periods')
            for rp in range(len(return_periods_day)):
                period = return_periods_day[rp]
                years = int(period / 365)
                print(f'> retrieving {data_file} @ {years} rp')
                change_data = open_calculated_file(f'{data_file}-{years}_yr-rp_change')
                data_files[data_file][f'{years}-rp-ch'] = change_data

                if use_existing_plot:
                    print('> you can find the pre-drawn plots in ./out/plot')
                else:
                    print(f'> plotting change for {data_file} @ {years} rp')
                    label = f'{years} year changing precipitation accumulation [mm]'
                    title = f'{years} year Changing Return Period Map'
                    fname = f'{data_file}-change-{years}_yr-rp'
                    if use_existing:
                        change_data = change_data['pr']
                    plot_data(change_data, label, title, fname, 'BrBG', 'change')

    time_end = time.time()
    print(f'completed in {round((time_end - time_start) / 60, 2)} mins')
    # sys.exit(0)
