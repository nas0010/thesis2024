import os
from PIL import Image

# Define paths
base_plot_path = 'C:/Users/nboub/Desktop/Plots'
output_gif_path = 'C:/Users/nboub/Desktop/GIFs'

# Ensure the output directory exists
os.makedirs(output_gif_path, exist_ok=True)

# Define the bands
bands = ['temperature_2m', 'total_Precipitation', 'soil_Moisture', 'surface_Pressure', 'wind_U']

# Define the speed of the GIF (duration in milliseconds between frames)
frame_duration = 400 # 1 second per frame

# Function to create a GIF for a given band
def create_gif(band):
    plot_dir = os.path.join(base_plot_path, band)
    output_gif_file = os.path.join(output_gif_path, f'{band}.gif')

    # Get all PNG files in the directory and sort them
    image_files = sorted([os.path.join(plot_dir, file) for file in os.listdir(plot_dir) if file.endswith('.png')])

    # Load images
    images = [Image.open(image_file) for image_file in image_files]

    # Save as GIF
    images[0].save(output_gif_file, save_all=True, append_images=images[1:], duration=frame_duration, loop=0)
    print(f'Saved GIF for {band} to {output_gif_file}')

# Create GIFs for each band
for band in bands:
    create_gif(band)
