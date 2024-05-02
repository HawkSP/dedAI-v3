
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data <enter the path to the CSV file>
data = pd.read_csv('plot_average_bp_0.csv')

# Compute the total bandpower for each genre
total_bandpower_by_genre = data.groupby('Marker Label')['Bandpower (dB)'].sum()

# Find the absolute maximum value for scaling the bandpower
max_abs_value = max(abs(total_bandpower_by_genre.min()), abs(total_bandpower_by_genre.max()))

# Scale bandpower to the range [-10, 10]
scaled_bandpower = total_bandpower_by_genre / max_abs_value * 10

# Create a list of angles for the radar chart, which will be the number of genres
angles = np.linspace(0, 2 * np.pi, len(scaled_bandpower), endpoint=False).tolist()
angles += angles[:1]  # Close the loop

# Initialize the radar chart with a larger figure size
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))

# Draw the outline of our data
stats = scaled_bandpower.tolist()
stats += stats[:1]  # Close the loop

# Draw the outline of our data
ax.plot(angles, stats, color='blue', linewidth=2)
# Fill in the area plotted in the radar chart to give it color
ax.fill(angles, stats, color='blue', alpha=0.25)

# Set the genre labels (xticklabels)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(scaled_bandpower.index, fontsize=15, ha='center', va='center')

# Set the title of the radar chart
ax.set_title('Total Bandpower by Genre (Scaled)', size=20, color='blue', y=1.1)

# Set yticks from -10 to 10
ax.set_yticks(range(-10, 12, 2))
ax.set_rlabel_position(360)
# Highlight the 0 line more clearly
ax.get_ygridlines()[5].set_color('black')
ax.get_ygridlines()[5].set_linewidth(1)
ax.set_yticklabels(range(-10, 12, 2), color="grey", size=12)
ax.set_ylim(-10, 10)

# Show gridlines
ax.grid(True)

# Adjust the padding of labels
label_padding = 37  # Adjust this value to move labels further away from the circle
ax.tick_params(axis='x', which='major', pad=label_padding)

# Save the plot as a PNG image
plt.savefig('bandpower_by_genre.png', bbox_inches='tight')

# Ensure the plot is shown
plt.show()

