import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature


def plot_data(d, label, title, fname, map_color='YlGnBu'):
    # Define the projection
    proj = ccrs.Mercator()

    # Create Map Figure
    fig, ax = plt.subplots(figsize=(16, 6.25), subplot_kw={'projection': proj})

    # Set Map Features
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle='-')
    ax.add_feature(cfeature.STATES, linestyle=':')

    # Set the Map Border Coordinates
    extent = [d['xlon'].min(), d['xlon'].max(), d['xlat'].min(), d['xlat'].max()]
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    # Add Precipitation Data as scatter on the map
    scatter = ax.scatter(d['xlon'], d['xlat'], c=d, cmap=map_color, vmin=0, vmax=500, transform=ccrs.PlateCarree())

    # Add a color bar and a label
    cbar = plt.colorbar(scatter, orientation='horizontal', pad=0.05, aspect=50)

    # Adjust color bar to match the width of the map
    posn = ax.get_position()
    cbar.ax.set_position([posn.x0, posn.y0 - 0.05, posn.width, 0.02])  # Adjust these values as needed
    cbar.set_label(label)

    # Add a title
    plt.title(title)

    plt.savefig(fname, bbox_inches='tight')
    # Show the Map
    # plt.show()

# light_blues = ['#e0f7ff', '#8de0fc', '#3dc7f5', '#109dcc']
# dark_blues = ['#e0e3ff', '#8da0fc', '#3d6af5', '#104ccc']
# greens = ['#e1ffe0', '#90fc8d', '#43f53d', '#16cc10']
# browns = ['#ffd7b0', '#fbb46d', '#f4912e', '#cc6e10']
# purples = ['#e6d6ff', '#b68afa', '#8744f0', '#5f1ac9']
#
# # Combine the colors
# colors = light_blues + dark_blues + greens + browns + purples
#
# # Create a ListedColormap
# custom_cmap_steps = mcolors.ListedColormap(colors)
