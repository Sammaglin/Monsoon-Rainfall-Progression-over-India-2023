import geopandas as gpd
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import numpy as np
import os
import imageio

# File paths
netcdf_path = "Data/PERSIANN_India_2025-06-04094807pm_2023.nc"
shapefile_path = "IND_SHP/India_State_Boundary.shp"
gif_output_path = "monsoon_progression.gif"

# Load shapefile
india_gdf = gpd.read_file(shapefile_path)
india_gdf = india_gdf.to_crs(epsg=4326)

# Read NetCDF rainfall data
ds = Dataset(netcdf_path)
rain = ds.variables['precip'][:]
lats = ds.variables['lat'][:]
lons = ds.variables['lon'][:]

# Time variable
time_var = ds.variables['datetime']
times = num2date(time_var[:], time_var.units)

# Create meshgrid
lon2d, lat2d = np.meshgrid(lons, lats)

# Prepare animation frames
frames = []
for i in range(len(times)):
    fig = plt.figure(figsize=(8, 10))
    ax = fig.add_axes([0.08, 0.15, 0.85, 0.72])  # [left, bottom, width, height]
    
    # Plot rainfall
    data = rain[i, :, :]
    pcm = ax.pcolormesh(lon2d, lat2d, data, cmap='Blues', shading='auto', vmin=0, vmax=50)

    # Plot shapefile boundary
    india_gdf.boundary.plot(ax=ax, color='black', linewidth=0.8, zorder=2)

    # Set plot limits with extra top space
    ax.set_xlim(65, 100)
    ax.set_ylim(5, 38)  # reduced top limit slightly for breathing space

    # Labels and grid
    ax.set_xlabel("Longitude", fontsize=10)
    ax.set_ylabel("Latitude", fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)

    # Run tight_layout early
    plt.tight_layout()

    # Main title
    fig.suptitle("Monsoon Rainfall Progression over India (2023)", 
                 fontsize=18, fontweight='bold', y=0.96)

    # Move annotation slightly lower to avoid overlap
    ax.annotate(times[i].strftime('%d %B %Y'), 
                xy=(0.7, 0.9), xycoords='axes fraction',  # changed from 1.05
                ha='center', va='bottom', fontsize=14, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='gray', alpha=0.8))

    # Info text
    fig.text(0.5, 0.91, "Data Source: CHRS | Visualization by Ansh Upadhyay", 
             ha='center', fontsize=11, style='italic', alpha=0.7)

    fig.text(0.5, 0.87,
             "Monsoon Phases: Incoming → Peak → Retreat\nObserve the south-to-north progression",
             ha='center', fontsize=12, fontweight='medium', color='darkgreen')

    # Colorbar
    cax = fig.add_axes([0.15, 0.08, 0.7, 0.03])
    cbar = fig.colorbar(pcm, cax=cax, orientation='horizontal')
    cbar.set_label("Rainfall (mm)", fontsize=10)
    cbar.ax.tick_params(labelsize=9)

    # Save frame (remove bbox_inches='tight')
    frame_path = f"frame_{i:03d}.png"
    fig.savefig(frame_path, dpi=100)
    plt.close(fig)
    frames.append(imageio.imread(frame_path))
    os.remove(frame_path)


# Save as GIF
imageio.mimsave(gif_output_path, frames, duration=0.4, loop=0)  # duration in seconds
print(f"GIF saved to {gif_output_path}")