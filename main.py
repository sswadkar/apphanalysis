import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
from shapely.geometry import Point
import json

###########################################

crs = ccrs.LambertConformal(central_longitude=-100.0, central_latitude=45.0)

reader = shpreader.Reader('mygeodata/border_level8_polygon.shp')

counties = list(reader.geometries())

with open ("data.json") as f:
    analysis = json.load(f)

COUNTIES = cfeature.ShapelyFeature(counties, ccrs.PlateCarree())

# Function used to create the map subplots
def plot_background(ax):
    ax.set_extent([-83.622061, -83.770847, 42.931121, 43.097155]) # michigan extent
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(COUNTIES, linewidth=1.0, facecolor="white", edgecolor="black")
    for datum in analysis:
        if datum["lead_levels"] >= 15:
            color = "orange"
            if datum["copper_levels"] >= 1300:
                color = "red"
        elif datum["copper_levels"] >= 1300:
            color = "blue"
        ax.add_feature(cfeature.ShapelyFeature(Point(float(datum["long"]), float(datum["lat"])).buffer(0.001), ccrs.PlateCarree()), facecolor=color)
    # ax.add_patch(plt.Circle((83.705521, 43.016193), radius=5, color='r'))
    return ax

# Create the figure and plot background on different axes
fig, axarr = plt.subplots(figsize=(20, 13), constrained_layout=True,
                          subplot_kw={'projection': crs})

plot_background(axarr)

axarr.set_title('Highest Concentrations of Lead and Copper in Flint, Michigan', fontsize=16)

# Set height padding for plots
fig.set_constrained_layout_pads(w_pad=0., h_pad=0.1, hspace=0., wspace=0.)

# Display the plot
plt.show()
