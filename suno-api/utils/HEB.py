import pandas as pd
from pyvis.network import Network
import json
import numpy as np

# Load the data <enter the path to the CSV file>
data = pd.read_csv('plot_average_bp_0.csv')

# Compute the average bandpower for each combination of genre and sensor-band frequency
average_bandpower = data.groupby(['Marker Label', 'Band Name'])['Bandpower (dB)'].mean().reset_index()

# Normalize the bandpower values
average_bandpower['Normalized Bandpower'] = (
                                                    average_bandpower['Bandpower (dB)'] - average_bandpower[
                                                'Bandpower (dB)'].min()
                                            ) / (
                                                    average_bandpower['Bandpower (dB)'].max() - average_bandpower[
                                                'Bandpower (dB)'].min()
                                            )

# Genre color mapping
genre_color = {
    "Pop": "#f4d03f",  # Mustard Yellow
    "Rock": "#a569bd",  # Soft Purple
    "Jazz": "#52be80",  # Light Green
    "HipHop": "#5dade2",  # Sky Blue
    "Electronic": "#45b39d",  # Seafoam Green
    "Classical": "#e74c3c",  # Soft Red
    "Custom": "#bdc3c7"   # Silver Gray
}

edge_color = "rgba(200, 200, 200, 0.5)"  # Soft Gray with 50% opacity

# Initialize the PyVis network
net = Network(height='2160px', width='100%', bgcolor='#222222', font_color='white')
net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=95, spring_strength=0.001, damping=0.09)

min_edge_width = 0.1
max_edge_width = 2

# Calculate the maximum weight to normalize the edge widths
max_weight = average_bandpower['Normalized Bandpower'].max()

# First add all nodes
for index, row in average_bandpower.iterrows():
    genre_node = row['Marker Label']
    sensor_band_node = row['Band Name']
    weight = row['Normalized Bandpower']
    normalized_weight = (weight - average_bandpower['Normalized Bandpower'].min()) / \
                        (average_bandpower['Normalized Bandpower'].max() - average_bandpower['Normalized Bandpower'].min())

    node_mass = 1 + normalized_weight * 6 # Adjust the multiplier as needed for desired effect

    # Add genre nodes with specific color and mass
    if genre_node in genre_color:
        genre_color_value = genre_color[genre_node]
        net.add_node(genre_node, label=genre_node, color=genre_color_value, size=15, mass=node_mass)

    # Add sensor nodes with a default color and mass
    net.add_node(sensor_band_node, label=sensor_band_node, color="rgba(150, 150, 150, 0.8)", size=5, mass=node_mass)


# Then add edges
# Calculate normalized edge widths and apply them
for index, row in average_bandpower.iterrows():
    genre_node = row['Marker Label']
    sensor_band_node = row['Band Name']
    weight = row['Normalized Bandpower']
    genre_color_value = genre_color.get(genre_node, "rgba(255, 255, 255, 0.8)")


    # Normalize the weight
    normalized_weight = (weight - average_bandpower['Normalized Bandpower'].min()) / \
                        (average_bandpower['Normalized Bandpower'].max() - average_bandpower['Normalized Bandpower'].min())

    # Scale the edge width based on the normalized weight
    edge_width = normalized_weight * (max_edge_width - min_edge_width) + min_edge_width
    shadow_size = normalized_weight * 4  # adjust the multiplier as needed for desired effect

    if genre_node in genre_color and genre_node in net.get_nodes() and sensor_band_node in net.get_nodes():
        net.add_edge(genre_node, sensor_band_node, width=edge_width, color=genre_color_value,
                     shadow={'enabled': True, 'size': shadow_size, 'color': genre_color_value})



# Define the options as a Python dictionary
options = {
    "nodes": {
        "font": {
            "size": 12
        }
    },
    "edges": {
        "color": {
            "inherit": False,
            "opacity": 0.5
        },
        "smooth": {
            "enabled": False,
            "type": "continuous"
        }
    },
    "physics": {
        "forceAtlas2Based": {
            "gravitationalConstant": -40,
            "centralGravity": 0.04,
            "springLength": 100,
            "springConstant": 0.05
        },
        "maxVelocity": 24,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
            "enabled": True,
            "iterations": 1000,
            "updateInterval": 25,
            "onlyDynamicEdges": False,
            "fit": True
        }
    },
    "interaction": {
        "tooltipDelay": 200,
        "hideEdgesOnDrag": False,
        "hideNodesOnDrag": False
    }
}

# Convert the options dictionary to a JSON string
options_json = json.dumps(options)

# Set the options using the JSON string
net.set_options(options_json)
net.show('eeg_network.html', notebook=False)