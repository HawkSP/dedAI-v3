# EEG Data Interpretation Utilities

This directory contains utility scripts designed for the analysis and visualization of EEG data specific to music genres. These tools are used to interpret EEG band power, generate radar charts, and visualize hierarchical edge bundling diagrams based on EEG data.

## Utilities Overview

### `eeg_band_power.py`

This script calculates the total band power for different music genres from EEG data and visualizes this data in a radar chart format. It scales the band power values and provides a visual comparison across genres.

#### Features:
- Grouping data by genre.
- Calculating total bandpower.
- Scaling and visualizing band power in a radar chart.

### `eeg_data_analysis.py`

Analyzes EEG data by segmenting it based on music genres, computes statistical features, and visualizes both time-domain and frequency-domain EEG signals.

#### Features:
- Handling missing data and normalizing it if required.
- Segmenting EEG data by genres.
- Extracting statistical and frequency-domain features.
- Visualizing EEG readings and power spectrum density for different genres.

### `head.py`

This script performs an analysis of EEG data by computing average band power for combinations of genres and bands, normalizing these values, and plotting them.

#### Features:
- Grouping and averaging band power by genre and EEG bands.
- Normalizing band power.
- Plotting average band power for each genre-band combination.

### `HEB.py` (Hierarchical Edge Bundling)

Generates a hierarchical edge bundling diagram to visualize the relationships between music genres and EEG sensor-band frequencies based on the band power.

#### Features:
- Normalizing band power data for visualization.
- Mapping genres to specific colors.
- Creating and displaying a network graph with customizable physics and interaction settings.

## Installation

To use these scripts, you need Python 3.x and several dependencies:

```bash
pip install pandas numpy matplotlib scipy pyvis
