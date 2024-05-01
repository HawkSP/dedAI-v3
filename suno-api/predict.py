import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def process_graph_bpm_emotions(data):
    """
    Fits multiple linear regression models for different emotions across BPM for all provided data.

    :param data: List containing BPM and emotional metrics across all genres.
    """
    emotions = ['Attention', 'Engagement', 'Excitement', 'Interest', 'Relaxation', 'Stress']
    # Define color cycle for plots for clarity
    colors = plt.cm.viridis(np.linspace(0, 1, len(emotions)))

    # Prepare the plot
    fig, ax = plt.subplots()

    for i, emotion in enumerate(emotions):
        bpm_data = [item['bpm'] for item in data]
        emotion_data = [item[emotion] for item in data]

        # Convert lists to numpy arrays for fitting the model
        bpm_array = np.array(bpm_data).reshape(-1, 1)
        emotion_array = np.array(emotion_data)

        # Fit the linear regression model
        model = LinearRegression()
        model.fit(bpm_array, emotion_array)

        # Generate BPM values for predictions from minimum to maximum observed BPM
        min_bpm, max_bpm = min(bpm_data), max(bpm_data)
        test_bpm = np.linspace(min_bpm, max_bpm, 300).reshape(-1, 1)
        predictions = model.predict(test_bpm)

        # Plotting the results
        ax.plot(test_bpm, predictions, label=f'{emotion}', color=colors[i])

    #ax.scatter(bpm_data, emotion_data, color='red')  # actual data points
    ax.set_title('Emotion Response by BPM Across All Genres')
    ax.set_xlabel('BPM')
    ax.set_ylabel('Emotion Level (%)')
    ax.legend()
    plt.show()



def process_bpm_emotions(data):
    """
    Fits multiple linear regression models for different emotions across BPM for all provided data.
    Returns a dictionary of fitted models for each emotion.
    :param data: List containing BPM and emotional metrics.
    :return: Dictionary of models.
    """
    emotions = ['Attention', 'Engagement', 'Excitement', 'Interest', 'Relaxation', 'Stress']
    models = {}

    for emotion in emotions:
        bpm_data = [item['bpm'] for item in data]
        emotion_data = [item[emotion] for item in data]

        # Convert lists to numpy arrays for fitting the model
        bpm_array = np.array(bpm_data).reshape(-1, 1)
        emotion_array = np.array(emotion_data).reshape(-1, 1)

        # Initialize and fit the linear regression model
        model = LinearRegression()
        model.fit(emotion_array, bpm_array)  # Corrected the order here
        models[emotion] = model

    return models


def predict_bpm(models, emotion_values):
    """
    Predicts BPM based on emotion values using fitted models.
    :param models: Dictionary of fitted LinearRegression models for each emotion.
    :param emotion_values: Dictionary of emotion metrics.
    :return: Predicted BPM.
    """
    predictions = []
    for emotion, value in emotion_values.items():
        if emotion in models:
            pred = models[emotion].predict(np.array([[value]]))
            predictions.append(pred[0][0])  # Access the predicted value

    if predictions:
        return np.mean(predictions)  # Return the average of predictions
    else:
        return None



# Function to flatten the genre-based data into a single list
def flatten_genre_data(genre_data):
    flat_data = []
    for genre, entries in genre_data.items():
        for entry in entries:
            flat_data.append(entry)
    return flat_data

def main():
    # Use the function to flatten the data
    flat_data = flatten_genre_data(genre_data)

    # Process data to fit models
    models = process_bpm_emotions(flat_data)

    # Example prediction
    emotion_values = {'Attention': 10, 'Engagement': 10, 'Excitement': 13, 'Interest': 10, 'Relaxation': 90, 'Stress': 20}
    predicted_bpm = predict_bpm(models, emotion_values)
    rounded_bpm = round(predicted_bpm) if predicted_bpm else None
    print(f"Predicted BPM: {rounded_bpm}")

    # Example of using the flat_data in the previously defined function to process BPM and emotions
    process_graph_bpm_emotions(flat_data)

if __name__ == "__main__":
    main()