import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import welch

# Load the data
df = pd.read_csv('enter_raw_eeg_file_here.csv')

# Check for missing values and fill them
df.fillna(0, inplace=True)

# Normalize or scale data if necessary (optional based on your data)
# df['column_name'] = (df['column_name'] - df['column_name'].mean()) / df['column_name'].std()

# Segmenting data based on musical genres
genres = df['marker_name'].unique()
segmented_data = {genre: df[df['marker_name'] == genre] for genre in genres}

# Feature Extraction: Calculate statistical features for each segment
features = {}
for genre, data in segmented_data.items():
    # Select only EEG reading columns for numerical operations
    eeg_columns = data.select_dtypes(include=[np.number]).columns
    features[genre] = {
        'mean': data[eeg_columns].mean(),
        'median': data[eeg_columns].median(),
        'variance': data[eeg_columns].var(),
        'std_dev': data[eeg_columns].std()
    }


# Frequency domain feature extraction using Fourier Transform
# Example for one segment
sample_segment = segmented_data['Pop']
frequency_domain_features = {}
for column in sample_segment.select_dtypes(include=[np.number]).columns:  # Only numerical columns
    # Convert the Pandas Series to a NumPy array before applying FFT
    column_data = sample_segment[column].to_numpy()
    # Applying Fourier Transform
    freq_data = fft(column_data)
    # Calculating power spectrum density
    psd = np.abs(freq_data) ** 2
    frequency_domain_features[column] = {
        'freq_data': freq_data,
        'psd': psd
    }



# Basic Data Analysis: Compare mean values across genres
mean_values = pd.DataFrame({genre: features[genre]['mean'] for genre in genres})
print("Mean Values by Genre:\n", mean_values)

# Graph Generation: Visualize the data
# Time-series plot for 'eeg.af3' in Pop music
plt.figure(figsize=(10, 6))
plt.plot(sample_segment['time'], sample_segment['eeg.af3'], label='Pop - eeg.af3')
plt.xlabel('Time')
plt.ylabel('EEG Reading')
plt.title('EEG Readings Over Time for Pop Genre (eeg.af3)')
plt.legend()
plt.show()

# Frequency domain graph for 'eeg.af3' in Pop music
plt.figure(figsize=(10, 6))
plt.plot(frequency_domain_features['eeg.af3']['psd'], label='Pop - eeg.af3 PSD')
plt.xlabel('Frequency')
plt.ylabel('Power Spectrum Density')
plt.title('Power Spectrum Density for Pop Genre (eeg.af3)')
plt.legend()
plt.show()

