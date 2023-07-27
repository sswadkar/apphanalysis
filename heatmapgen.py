import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import json

crs = ccrs.LambertConformal(central_longitude=-100.0, central_latitude=45.0)

reader = shpreader.Reader('mygeodata/border_level8_polygon.shp')

counties = list(reader.geometries())

with open ("data.json") as f:
    analysis = json.load(f)

analysis = [level for level in analysis if level["copper_levels"] < 1500]

COUNTIES = cfeature.ShapelyFeature(counties, ccrs.PlateCarree())

# Function used to create the map subplots
def plot_background(ax):
    ax.set_extent([-83.622061, -83.770847, 42.931121, 43.097155]) # michigan extent
    ax.add_feature(cfeature.STATES, linewidth=0.5)
    ax.add_feature(COUNTIES, linewidth=1.0, facecolor="none", edgecolor="black")

    return ax

# Create the figure and plot background on different axes
fig, axarr = plt.subplots(figsize=(20, 13), constrained_layout=True,
                          subplot_kw={'projection': crs})
long = [float(datum["long"]) for datum in analysis]
lat = [float(datum["lat"]) for datum in analysis]
lead_levels = [float(datum["copper_levels"]) for datum in analysis]

plot_background(axarr)
C = axarr.tricontourf(long, lat , lead_levels, transform=ccrs.PlateCarree())
fig.colorbar(C, orientation="vertical", extend="max", label="Copper Concentration in Water (ppb)")
plt.title("Concentration of Copper in Flint, Michigan's 2015-2016 Tap Water", fontsize=13, weight='bold', loc="left")

# Set height padding for plots
fig.set_constrained_layout_pads(w_pad=0., h_pad=0.1, hspace=0., wspace=0.)

# Display the plot
plt.show()


