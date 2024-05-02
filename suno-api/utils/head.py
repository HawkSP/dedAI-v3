import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data <enter the path to the CSV file>
data = pd.read_csv('plot_average_bp_0.csv')

# Assuming 'Band Name' column includes 'alpha', 'beta', 'delta', 'theta' as part of the string for the respective bands.
# Compute the average bandpower for each combination of genre and band
average_bandpower = data.groupby(['Marker Label', 'Band Name'])['Bandpower (dB)'].mean().reset_index()

# Normalize the bandpower values
average_bandpower['Normalized Bandpower'] = (
    average_bandpower['Bandpower (dB)'] - average_bandpower['Bandpower (dB)'].min()
) / (
    average_bandpower['Bandpower (dB)'].max() - average_bandpower['Bandpower (dB)'].min()
)

# Plotting the average bandpower for each genre-band combination
fig, ax = plt.subplots(figsize=(12, 8))

for label, df in average_bandpower.groupby('Marker Label'):
    ax.plot(df['Band Name'], df['Normalized Bandpower'], label=label)

ax.set_ylabel('Normalized Bandpower')
ax.set_title('Average Bandpower for Each Genre-Band Combination')
ax.legend(title='Genres')
plt.xticks(rotation=45)
plt.show()

# Assuming there's a 'Genre' column for simplicity
# If genres are in the 'Marker Label', replace 'Genre' with 'Marker Label' below
genres = average_bandpower['Marker Label'].unique()
angles = np.linspace(0, 2 * np.pi, len(genres), endpoint=False).tolist()
angles += angles[:1]  # Ensure the radar chart is a closed shape

#fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Define the number of variables (bands), this should be the same as the number of unique bands
num_vars = len(average_bandpower['Band Name'].unique())

# There will be as many angles as there are bands
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Complete the loop

# Draw one axe per variable + close the loop
plt.xticks(angles[:-1], average_bandpower['Band Name'].unique())

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=7)
plt.ylim(0, 1)
# Plot data + fill
for genre in genres:
    # Filter the data for each genre and sort by band name to align with angles
    genre_data = average_bandpower[average_bandpower['Marker Label'] == genre].sort_values('Band Name')
    # If there are missing bands for the genre, it will cause an error, so we handle it
    if len(genre_data) == num_vars:
        values = genre_data['Normalized Bandpower'].tolist()
        values += values[:1]  # Complete the loop
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=genre)
        ax.fill(angles, values, alpha=0.4)
    else:
        print(f"Not enough data for genre {genre} to plot radar chart.")

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()
