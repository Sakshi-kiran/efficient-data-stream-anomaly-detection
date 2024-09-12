import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Data stream simulation function
def data_stream(length=1000, period=50, anomaly_prob=0.02):
    """
    Simulates a real-time data stream with seasonal patterns and random noise.
    Occasionally introduces anomalies.
    
    Parameters:
        length (int): Number of data points to generate.
        period (int): Period for the seasonal component (sine wave).
        anomaly_prob (float): Probability of an anomaly occurring.

    Yields:
        float: A value from the simulated data stream.
    """
    for i in range(length):
        seasonal_component = np.sin(2 * np.pi * i / period)
        noise = np.random.normal(0, 0.1)
        value = seasonal_component + noise
        
        # Introduce anomalies with a specified probability
        if np.random.rand() < anomaly_prob:
            value += np.random.normal(5, 2)  # Large deviation to simulate anomaly
        yield value

# Anomaly detection function using moving Z-Score
def anomaly_detection(window, threshold=3):
    """
    Detects anomalies in the data stream using the moving Z-Score method.
    
    Parameters:
        window (deque): Recent data points for anomaly detection.
        threshold (float): Z-score threshold for detecting anomalies.

    Returns:
        bool: True if the last value in the window is an anomaly, False otherwise.
    """
    if len(window) < 2:  # Not enough data to compute statistics
        return False
    
    mean = np.mean(window)
    std_dev = np.std(window)
    
    # Avoid division by zero if std_dev is 0
    if std_dev == 0:
        return False
    
    # Calculate Z-score of the last value and compare with threshold
    z_score = (window[-1] - mean) / std_dev
    return abs(z_score) > threshold

# Real-time visualization of data stream and anomalies
def visualize(stream_generator, window_size=30, threshold=3):
    """
    Visualizes the real-time data stream and detected anomalies.

    Parameters:
        stream_generator (generator): Generator for the data stream.
        window_size (int): Number of recent data points to consider for anomaly detection.
        threshold (float): Z-score threshold for detecting anomalies.
    """
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    window = deque(maxlen=window_size)
    anomalies = []

    try:
        for i, value in enumerate(stream_generator):
            x_data.append(i)
            y_data.append(value)
            window.append(value)

            if len(window) == window_size:
                if anomaly_detection(window, threshold):
                    anomalies.append(i)
                    print(f"Anomaly detected at index {i}: {value:.2f}")

            ax.clear()
            ax.plot(x_data, y_data, label='Data Stream')
            ax.scatter(anomalies, [y_data[idx] for idx in anomalies], color='r', label='Anomalies')
            ax.set_xlabel('Time Step')
            ax.set_ylabel('Stream Value')
            ax.set_title('Real-time Data Stream with Anomaly Detection')
            ax.legend()
            plt.pause(0.01)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        plt.ioff()  # Disable interactive mode
        plt.show()

if __name__ == "__main__":
    # Create the data stream generator
    stream_gen = data_stream(length=1000, period=50, anomaly_prob=0.02)
    # Visualize the data stream and detected anomalies
    visualize(stream_gen, window_size=30, threshold=3)
