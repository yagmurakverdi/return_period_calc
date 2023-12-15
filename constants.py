"""
Constants
"""
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

# script variables
# use_existing = True

# data file variables
data_path = './data/'
out_data_path = './out/data/'
out_plot_path = './out/plot/'

data_files = {
    # '8.5-26-50-3hrs': {'name': 'Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc', 'data_type': 'model-85-3hrs'},
    # 'hist-22-23': {'name': 'pr_2023_daily.nc', 'data_type': 'historic'},
    'hist-76-00': {'name': 'Turkey_MPI_dn_STS.1976-2000_pr.nc', 'data_type': 'historic'},
    '8.5-26-50': {'name': 'Turkey_MPI_85_dn_STS.2026-2050_pr.nc', 'data_type': 'model-85'},
    '8.5-51-75': {'name': 'Turkey_MPI_85_dn_STS.2051-2075_pr.nc', 'data_type': 'model-85'},
    '8.5-76-99': {'name': 'Turkey_MPI_85_dn_STS.2076-2099_pr.nc', 'data_type': 'model-85'},
    # '4.5-26-50': {'name': 'Turkey_MPI_45_dn_STS.2026-2050_pr.nc', 'data_type': 'model-45'},
    # '4.5-51-75': {'name': 'Turkey_MPI_45_dn_STS.2051-2075_pr.nc', 'data_type': 'model-45'},
    # '4.5-76-99': {'name': 'Turkey_MPI_45_dn_STS.2076-2099_pr.nc', 'data_type': 'model-45'},
}

# calculation variables
threshold = 1
crop_degrees = 5
# min_n_excesses = 3
# return_periods_year = np.array([1, 10, 100])
return_periods_day = np.array([365, 3650, 36500, 365000, 3650000])


# Define a custom modification of the YlGnBu colormap
# custom_cmap = 'YlGnBu'
original_cmap = plt.cm.YlGnBu
custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    'truncated_YlGnBu',
    original_cmap(np.linspace(0, 0.80, 256))
)