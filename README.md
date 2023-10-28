Yagmur's Thesis Code Steps
==========================

This is to setup, run and trace steps for Yagmur.

Data Sets
---------
* 1970-2000 reference period precipitation data (will come)
* 2026-2050 3 hrs and daily precipitation data for RCP 8.5 scenario
* 2026-2050 daily precipitation for RCP 4.5 scenario (will come)
* 2050-2075 daily precipitation for RCP 4.5 and RCP 8.5 scenarios (will come)
* 2075-2100 daily precipitation for RCP 4.5 and RCP 8.5 scenarios (will come)

Methods
-------
* MEV (Meta Statistical Extreme Value)
* GEV (Generalized Extreme Value)
* Quantile 
* Statistical Calculation  
methods will be applied and calculations will be checked

Steps so far
------------
* opened the Data file for 2026-2050 RCP 8.5 RFE data


Data Set
--------
1. `Turkey_MPI_85_dn_SRF.2026-2050_pr_3hour.nc` - 25yr modeled 3hrs precipitation est. data
2. `pr_2023_daily.nc` - daily modeled precipitation for 2023 - as sample


Installing
----------
Run to install environment
```shell
pip install -r requirements.txt
```

Running
-------
To run the project run below command
```shell
python3 main.py
```

TODOs
-----

