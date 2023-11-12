import numpy as np

# script variables
use_existing = True

# data file variables
data_path = './data/'
out_path = './out/'
data_files = {
    '26-50-8.5-daily': {'name': 'Turkey_MPI_85_dn_STS.2026-2050_pr_daily.nc', 'data_type': 'daily'},
    '26-50-8.5-3hrs': {'name': 'Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc', 'data_type': '3hrs'},
    '22-23-daily': {'name': 'pr_2023_daily.nc', 'data_type': 'daily'},
}

# calculation variables
threshold = 1
min_n_excesses = 3  # TODO 20?
return_period = np.array([1, 10, 100])
