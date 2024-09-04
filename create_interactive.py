import folium

# Coordinates for Greece and Crete
greece_coords = [39.0742, 21.8243]
crete_coords = [35.2401, 24.8093]

# Create a map centered on Greece
m = folium.Map(location=greece_coords, zoom_start=6)

# Add a marker on Crete with a popup that includes a zoom button, dropdown menus, and a slider
popup_html = """
<style>
    .zoom-button {
        background-color: #b6c1ff; /* Green */
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 8px;
    }

    .zoom-button:hover {
        background-color: white;
        color: black;
    }

    .popup-content {
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        color: #333;
        text-align: left;
        padding: 10px;
    }

    .popup-content label {
        font-weight: bold;
        margin-bottom: 5px;
        display: block;
    }

    .popup-content select, .popup-content input {
        width: 100%;
        margin-bottom: 10px;
        padding: 5px;
        border-radius: 4px;
        border: 1px solid #ccc;
    }

    .popup-content input[type="range"] {
        -webkit-appearance: none;
        width: 100%;
        height: 8px;
        border-radius: 5px;
        background: #d3d3d3;
        outline: none;
        opacity: 0.7;
        -webkit-transition: .2s;
        transition: opacity .2s;
    }

    .popup-content input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        background: #4CAF50;
        cursor: pointer;
    }

    .popup-content input[type="range"]::-moz-range-thumb {
        width: 25px;
        height: 25px;
        border-radius: 50%;
        background: #4CAF50;
        cursor: pointer;
    }

    .popup-content output {
        display: block;
        margin-top: 5px;
        font-weight: bold;
    }
</style>
<div class="popup-content">
    <button class="zoom-button" onclick="zoomToCrete()">Zoom to Crete</button>
    <br>
    <label for="bandSelect">Select Band:</label>
    <select id="bandSelect">
        <option value="Temperature_2m">Temperature</option>
        <option value="Total_Precipitation">Precipitation</option>
        <option value="Soil_Moisture">Soil Moisture</option>
        <option value="Surface_Pressure">Surface Pressure</option>
        <option value="Wind_U">Wind U</option>
    </select>
    <br>
    <label for="yearSlider">Select Year:</label>
    <input type="range" id="yearSlider" name="yearSlider" min="1990" max="2020" value="2000" oninput="this.nextElementSibling.value = this.value">
    <output>2000</output>
</div>
"""
popup = folium.Popup(popup_html, max_width=300)

marker = folium.Marker(
    location=crete_coords,
    popup=popup,
    icon=folium.Icon(color="lightred", icon="info-sign")
).add_to(m)

# Additional markers for other locations
athens_coords = [37.9838, 23.7275]
thessaloniki_coords = [40.6401, 22.9444]

folium.Marker(
    location=athens_coords,
    popup="Athens",
    icon=folium.Icon(color="beige", icon="info-sign")
).add_to(m)

folium.Marker(
    location=thessaloniki_coords,
    popup="Thessaloniki",
    icon=folium.Icon(color="lightblue", icon="info-sign")
).add_to(m)

# Get the map ID
map_id = m.get_name()

# Add custom JavaScript to handle the zoom and interactions
zoom_js = f"""
<script>
    var overlayLayer;
    var colorbarLayer;

    document.addEventListener('DOMContentLoaded', function() {{
        window.map = {map_id};  // Ensure the map is available in the global scope
    }});

    function zoomToCrete() {{
        map.setView([35.2401, 24.8093], 8);  // Adjusted zoom level
        document.getElementById('bandSelect').addEventListener('change', updateMap);
        document.getElementById('yearSlider').addEventListener('input', updateMap);
    }}

    function updateMap() {{
        var band = document.getElementById('bandSelect').value;
        var year = document.getElementById('yearSlider').value;
        console.log('Selected Band:', band, 'Selected Year:', year);

        // Example: Update the overlay layer (Assuming you have a server to serve .png files)
        var overlayUrl = `http://localhost:8000/Crete_${{band}}_${{year}}.png`;
        console.log('Overlay URL:', overlayUrl);
        
        // Remove the existing overlay layer if it exists
        if (overlayLayer) {{
            map.removeLayer(overlayLayer);
        }}
        
        // Add the new overlay layer
        var bounds = [[34.8, 23.3], [35.8, 26.7]];
        overlayLayer = L.imageOverlay(overlayUrl, bounds, {{ opacity: 0.6 }});
        overlayLayer.addTo(map);

        // Update the color bar
        if (colorbarLayer) {{
            map.removeLayer(colorbarLayer);
        }}

        var colorbarUrl;
        switch(band) {{
            case 'Temperature_2m':
                colorbarUrl = 'http://localhost:8000/colorbar_Temperature_2m.png';
                break;
            case 'Total_Precipitation':
                colorbarUrl = 'http://localhost:8000/colorbar_Total_Precipitation.png';
                break;
            case 'Soil_Moisture':
                colorbarUrl = 'http://localhost:8000/colorbar_Soil_Moisture.png';
                break;
            case 'Surface_Pressure':
                colorbarUrl = 'http://localhost:8000/colorbar_Surface_Pressure.png';
                break;
            case 'Wind_U':
                colorbarUrl = 'http://localhost:8000/colorbar_Wind_U.png';
                break;
        }}

       var colorbarBounds = [[34.8, 22.9], [36.0, 23.3]];  // Adjusted bounds for a bigger color bar
        colorbarLayer = L.imageOverlay(colorbarUrl, colorbarBounds, {{ opacity: 1.0 }});
        colorbarLayer.addTo(map);
    }}
</script>
"""

# Add the JavaScript to the map
m.get_root().html.add_child(folium.Element(zoom_js))

# Save the map
m.save("C:/Users/nboub/Pictures/Data1/greece_map.html")

print("Map saved as greece_map.html. Open this file in a web browser to view it.")
