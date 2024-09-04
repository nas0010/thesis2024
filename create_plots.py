import os
import numpy as np
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from rasterio.plot import show

# Define paths
base_paths = {
    'temperature_2m': 'C:/Users/nboub/Pictures/Crete_Temperature',
    'total_Precipitation': 'C:/Users/nboub/Pictures/Crete_total_Precipitation',
    'soil_Moisture': 'C:/Users/nboub/Pictures/Crete_Soil_Moisture',
    'surface_Pressure': 'C:/Users/nboub/Pictures/Crete_Surface_Pressure',
    'wind_U': 'C:/Users/nboub/Pictures/Crete_Wind_U'
}
dem_path = 'C:/Users/nboub/Desktop/crete_dem.tif'

# Define units for each band
units = {
    'temperature_2m': 'K',
    'total_Precipitation': 'mm',
    'soil_Moisture': 'm³/m³',
    'surface_Pressure': 'Pa',
    'wind_U': 'm/s'
}

# Load the DEM file
print(f"Loading DEM file from {dem_path}")
with rasterio.open(dem_path) as dem_data:
    dem_array = dem_data.read(1)
    dest_crs = dem_data.crs
    dest_transform = dem_data.transform
print(f"Destination CRS: {dest_crs}")

# Function to read and verify each year's data for a given band
def process_yearly_data(year, band, base_path):
    try:
        # Define file path for the data
        data_path = os.path.join(base_path, f'Crete_{band.capitalize()}_{year}.tif')

        # Check if file exists
        if not os.path.exists(data_path):
            print(f"File not found: {data_path}")
            return {'year': year, band: np.nan, f'{band}_array': np.nan}

        # Load the data
        print(f"Loading {band} data from {data_path}")
        with rasterio.open(data_path) as data:
            data_array = data.read(1)
            metadata = data.meta

            # Debugging: Check the metadata and some data values
            print(f"Metadata for {year} {band}: {metadata}")
            print(f"{band.capitalize()} data sample for {year}: {data_array[0:5, 0:5]}")

            # Debugging: Check the data
            min_val = np.nanmin(data_array)
            max_val = np.nanmax(data_array)
            mean_val = np.nanmean(data_array)
            print(f"{band.capitalize()} data for {year}: min={min_val}, max={max_val}, mean={mean_val}")

            # Return the processed data
            return {
                'year': year,
                band: mean_val,
                f'{band}_array': data_array  # Store the array for later plotting
            }
    except Exception as e:
        print(f"Error processing data for year {year} band {band}: {e}")
        return {
            'year': year,
            band: np.nan,
            f'{band}_array': np.nan
        }

# Bands to process
bands = ['temperature_2m', 'total_Precipitation', 'soil_Moisture', 'surface_Pressure', 'wind_U']

# Process data for all years and all bands
all_data = {band: [] for band in bands}
global_min_max = {band: {'min': np.inf, 'max': -np.inf} for band in bands}

for year in range(1990, 2021):
    for band in bands:
        data = process_yearly_data(year, band, base_paths[band])
        all_data[band].append(data)
        
        # Update global min and max for the band
        if not np.isnan(data[f'{band}_array']).all():
            global_min_max[band]['min'] = min(global_min_max[band]['min'], np.nanmin(data[f'{band}_array']))
            global_min_max[band]['max'] = max(global_min_max[band]['max'], np.nanmax(data[f'{band}_array']))

# Convert results to DataFrames
df_all = {band: pd.DataFrame(all_data[band]) for band in bands}

# Normalize the data
def normalize_data(df):
    df_normalized = df.copy()
    for column in df.columns:
        if column != 'year' and not column.endswith('_array'):
            df_normalized[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
    return df_normalized

df_all_normalized = {band: normalize_data(df_all[band]) for band in bands}

# Save the normalized data
for band, df in df_all_normalized.items():
    output_csv_path = os.path.join('C:/Users/nboub/Desktop', f'normalized_crete_{band}_data.csv')
    df.to_csv(output_csv_path, index=False)
    print(f"Normalized {band} data saved to {output_csv_path}")

# Plotting the data and saving to files
def plot_and_save_data(df, band, cmap, global_min, global_max, unit):
    plot_dir = os.path.join('C:/Users/nboub/Desktop/Plots', band)
    os.makedirs(plot_dir, exist_ok=True)
    for index, row in df.iterrows():
        data_array = row[f'{band}_array']  # Access the stored data array
        if np.isnan(data_array).all():
            print(f"Skipping plot for {band} in {row['year']} due to all NaN values")
            continue
        plt.figure(figsize=(10, 6))
        plt.imshow(data_array, cmap=cmap, norm=Normalize(vmin=global_min, vmax=global_max))
        cbar = plt.colorbar()
        cbar.set_label(f'Unit: {unit}')
        plt.title(f'{band.capitalize()} Data for {row["year"]}')
        plot_path = os.path.join(plot_dir, f'{band}_data_{row["year"]}.png')
        plt.savefig(plot_path)
        plt.close()
        print(f'Saved plot to {plot_path}')

# Define color maps for each band
cmap_dict = {
    'temperature_2m': 'hot',
    'total_Precipitation': 'Blues',
    'soil_Moisture': 'Greens',
    'surface_Pressure': 'Oranges',
    'wind_U': 'Purples'
}

# Plot the data for each band and save to files
for band in bands:
    plot_and_save_data(df_all[band], band, cmap_dict[band], global_min_max[band]['min'], global_min_max[band]['max'], units[band])
