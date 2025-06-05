import geopandas as gpd
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import numpy as np
import os
import imageio

# File paths
netcdf_path = "Data/PERSIANN_India_2025-06-04094807pm_2023.nc"  # Replace with your actual NetCDF path
shapefile_path = "IND_SHP/India_State_Boundary.shp"  # Replace with your shapefile path
gif_output_path = "monsoon_progression.gif"

# Load shapefile with full boundary (including J&K)
india_gdf = gpd.read_file(shapefile_path)
india_gdf = india_gdf.to_crs(epsg=4326)

# Read NetCDF rainfall data
ds = Dataset(netcdf_path)
rain = ds.variables['precip'][:]  # Shape: (datetime, lat, lon)
lats = ds.variables['lat'][:]
lons = ds.variables['lon'][:]

# Time variable is named 'datetime'
time_var = ds.variables['datetime']
times = num2date(time_var[:], time_var.units)

# Create a meshgrid for plotting
lon2d, lat2d = np.meshgrid(lons, lats)

# Prepare animation frames
frames = []
for i in range(len(times)):
    fig, ax = plt.subplots(figsize=(8, 10))

    # Plot rainfall
    data = rain[i, :, :]
    pcm = ax.pcolormesh(lon2d, lat2d, data, cmap='Blues', shading='auto')

    # Plot shapefile boundary
    india_gdf.boundary.plot(ax=ax, color='black', linewidth=0.8, zorder=2)

    # Title and annotations
    fig.suptitle("Monsoon Rainfall Progression over India (2023)", fontsize=18, fontweight='bold', y=0.98)
    fig.text(0.5, 0.92, "Data Source: CHRS | Visualization by Ansh Upadhyay", ha='center',
             fontsize=11, style='italic', alpha=0.7)

    fig.text(0.5, 0.88,
             "Monsoon Phases: Incoming → Peak → Retreat\nObserve the south-to-north progression of rainfall",
             ha='center', fontsize=12, fontweight='medium', color='darkgreen')

    # Date label
    fig.text(0.05, 0.05, times[i].strftime('%Y-%m-%d'), fontsize=12,
             bbox=dict(facecolor='white', alpha=0.8))

    # Colorbar
    cbar = fig.colorbar(pcm, ax=ax, orientation='horizontal', pad=0.05, aspect=50)
    cbar.set_label("Rainfall (mm)")

    # Set plot limits
    ax.set_xlim(65, 100)
    ax.set_ylim(2, 30)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.axis('equal')
    plt.tight_layout()

    # Save frame and append
    frame_path = f"frame_{i:03d}.png"
    fig.savefig(frame_path, dpi=100)
    plt.close(fig)
    frames.append(imageio.imread(frame_path))
    os.remove(frame_path)

# Save all frames as GIF
imageio.mimsave(gif_output_path, frames, duration=0.3)

print(f"GIF saved to {gif_output_path}")
