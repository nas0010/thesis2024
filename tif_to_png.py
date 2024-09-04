import rasterio
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# Color maps for each band
color_maps = {
    'Temperature_2m': 'hot',
    'Total_Precipitation': 'Blues',
    'Soil_Moisture': 'Greens',
    'Surface_Pressure': 'Oranges',
    'Wind_U': 'Purples'
}

def apply_color_map_with_transparency(array, cmap):
    norm = Normalize(vmin=np.nanmin(array), vmax=np.nanmax(array))
    colormap = plt.get_cmap(cmap)
    rgba_img = colormap(norm(array))
    rgba_img[:, :, 3] = ~np.isnan(array)  # Set alpha channel: 1 for data, 0 for NaN
    rgba_img = (rgba_img * 255).astype(np.uint8)  # Convert to 8-bit per channel
    return rgba_img

def convert_tif_to_png(tif_path, png_path, cmap):
    with rasterio.open(tif_path) as src:
        array = src.read(1)
        array[array == src.nodata] = np.nan

        # Apply color map with transparency
        color_mapped_array = apply_color_map_with_transparency(array, cmap)

        # Save the color-mapped array as a PNG file with transparency
        img = Image.fromarray(color_mapped_array, 'RGBA')
        img.save(png_path)

# Convert all your TIF files to PNG with color mapping and transparency
for band, cmap in color_maps.items():
    for year in range(1990, 2021):
        tif_path = f"C:/Users/nboub/Pictures/Data/Crete_{band}_{year}.tif"
        png_path = f"C:/Users/nboub/Pictures/Data1/Crete_{band}_{year}.png"
        convert_tif_to_png(tif_path, png_path, cmap)
