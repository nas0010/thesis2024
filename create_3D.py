import os
import numpy as np
import rioxarray as riox
import pyvista as pv
import time

# Paths to your data files
base_folder = 'C:/Users/nboub/Pictures'
folders = {
    'Crete_Temperature': 'Crete_Temperature',
    'Crete_Precipitation': 'Crete_total_Precipitation',
    'Crete_Soil_Moisture': 'Crete_Soil_Moisture',
    'Crete_Wind_U': 'Crete_Wind_U',
    'Crete_Surface_Pressure': 'Crete_Surface_Pressure'
}

# Color maps for each data type
color_maps = {
    'Crete_Temperature': 'coolwarm',
    'Crete_Precipitation': 'Blues',
    'Crete_Soil_Moisture': 'Greens',
    'Crete_Wind_U': 'Purples',
    'Crete_Surface_Pressure': 'Oranges'
}

# Define units for each band
units = {
    'Crete_Temperature': 'K',
    'Crete_Precipitation': 'mm',
    'Crete_Soil_Moisture': 'm³/m³',
    'Crete_Wind_U': 'm/s',
    'Crete_Surface_Pressure': 'Pa'
}

# Load the DEM data
print("Loading DEM data...")
dem_path = 'C:/Users/nboub/Desktop/crete_dem.tif'
dem_data = riox.open_rasterio(dem_path)
dem_data = dem_data[0]  # Select the first band
print(f"DEM data shape: {dem_data.shape}")

# Function to load and resample data
def load_and_resample(path, dem_data):
    print(f"Loading data from {path}...")
    data = riox.open_rasterio(path)
    data = data[0]  # Select the first band
    print(f"Original data shape: {data.shape}")
    data = data.rio.reproject_match(dem_data)
    print(f"Resampled data shape: {data.shape}")
    return np.asarray(data)

# Create a mesh grid for the DEM
print("Creating mesh grid...")
x, y = np.meshgrid(dem_data['x'], dem_data['y'])
print(f"Mesh grid shapes - x: {x.shape}, y: {y.shape}")

# Set the z values and create a StructuredGrid
print("Creating StructuredGrid...")
z = np.zeros_like(x)
mesh = pv.StructuredGrid(x.astype(np.float32), y.astype(np.float32), z.astype(np.float32))
print(f"StructuredGrid created with {mesh.n_points} points.")

# Assign Elevation Values
print("Assigning elevation values...")
mesh["Elevation"] = np.asarray(dem_data).ravel(order='F')
print("Elevation values assigned.")

# Warp the mesh by scalar to visualize the terrain
print("Warping the mesh by scalar...")
topo = mesh.warp_by_scalar(scalars="Elevation", factor=0.00005)  # Adjust the factor as needed
print("Mesh warped by scalar.")

# Function to get global min and max values for each data type
def get_global_min_max(folder_full_path):
    global_min = np.inf
    global_max = -np.inf
    for file_name in os.listdir(folder_full_path):
        if file_name.endswith('.tif'):
            file_path = os.path.join(folder_full_path, file_name)
            data = load_and_resample(file_path, dem_data)
            global_min = min(global_min, np.nanmin(data))
            global_max = max(global_max, np.nanmax(data))
    return global_min, global_max

# Function to plot data and save the output
def plot_data(topo, data, title, cmap, output_folder, global_min, global_max, unit):
    print(f"Overlaying {title} data...")
    raveled_data = data.ravel(order='F')
    topo[title] = raveled_data
    print(f"{title} data overlayed.")
   
    print(f"Plotting the 3D terrain with {title} overlay...")
    p = pv.Plotter(off_screen=True)
    p.add_mesh(topo, scalars=title, cmap=cmap, scalar_bar_args={'title': f'{title} ({unit})', 'label_font_size': 10})
    p.set_background(color='white')
    p.show_bounds(grid='back', location='outer', ticks='both', font_size=7)  # Move the grid to the back

    # Adjust the camera position
    p.camera_position = 'xy'
    p.camera.azimuth = 320  # Rotate around the vertical axis
    p.camera.elevation = 20  # Rotate around the horizontal axis to view from above
    p.camera.roll = 0 # Adjust roll to ensure north is up


    # Ensure the plot is fully rendered before taking the screenshot
    p.show(auto_close=False)
    time.sleep(1)  # Add a short delay to ensure the render window is updated
    output_path = os.path.join(output_folder, f"{title}.png")
    p.screenshot(output_path)
    p.close()
    print(f"Plot saved for {title} at {output_path}.")

# Process each folder and file
for folder_name, folder_path in folders.items():
    folder_full_path = os.path.join(base_folder, folder_path)
    output_folder = os.path.join(base_folder, f"{folder_path}_Output")
    os.makedirs(output_folder, exist_ok=True)
    cmap = color_maps[folder_name]
    unit = units[folder_name]
   
    # Get global min and max values for consistent color bar
    global_min, global_max = get_global_min_max(folder_full_path)
   
    for file_name in os.listdir(folder_full_path):
        if file_name.endswith('.tif'):
            file_path = os.path.join(folder_full_path, file_name)
            data = load_and_resample(file_path, dem_data)
            title = os.path.splitext(file_name)[0]
            plot_data(topo, data, title, cmap, output_folder, global_min, global_max, unit)
