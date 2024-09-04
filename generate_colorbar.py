import matplotlib.pyplot as plt
import numpy as np

# Define the color maps and their ranges for each band
color_maps = {
    'Temperature_2m': ('hot', 270, 310, 'K'),
    'Total_Precipitation': ('Blues', 0, 300, 'mm'),
    'Soil_Moisture': ('Greens', 0, 1, 'm³/m³'),
    'Surface_Pressure': ('Oranges', 950, 1050, 'hPa'),
    'Wind_U': ('Purples', 0, 15, 'm/s')
}

def create_colorbar(cmap_name, vmin, vmax, label, filename):
    fig, ax = plt.subplots(figsize=(2, 8), dpi=100, subplot_kw={'frame_on': False})  # Increased height to make it longer
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    fig.patch.set_alpha(0.0)  # Set figure background to transparent
    fig.subplots_adjust(left=0.3, right=0.8, top=0.9, bottom=0.1)

    cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap_name), cax=ax, orientation='vertical')
    cb.set_label(label, fontsize=12)
    cb.outline.set_visible(False)
    cb.ax.yaxis.set_tick_params(color='black')

    plt.savefig(filename, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()

for band, (cmap, vmin, vmax, unit) in color_maps.items():
    create_colorbar(cmap, vmin, vmax, f'{band} ({unit})', f'colorbar_{band}.png')
