"""
Common Data Operations
"""


def assign_year_coord(d):
    """This is the main process where we prepare and run the data

    Data Files General Info
    'time_bnds' - daily times
    'crs' - coordinates w/ GeoX GeoY
    'pr'
        standard_name:  precipitation_flux
        long_name:      Mean total precipitation flux
        units:          kg m-2 s-1
        grid_mapping:   crs
        cell_methods:   time: mean
    'xlon'
        standard_name:        longitude
        long_name:            Longitude on Cross Points
        units:                degrees_east
    'xlat'
        standard_name:        latitude
        long_name:            Latitude on Cross Points
        units:                degrees_north
    """
    # creates another year coordinate in relation with time
    d = d.assign_coords(year=d['time'].dt.year)
    # converts timestamp to string YYYY-MM-DD
    d['time'] = d['time'].dt.strftime('%Y-%m-%d')
    return d


def filter_by_threshold(d, th=0):
    d = d.where(d.pr > th, drop=True)
    return d
