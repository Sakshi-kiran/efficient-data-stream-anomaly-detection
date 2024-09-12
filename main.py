import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Data stream simulation function
def data_stream(length=1000, period=50, anomaly_prob=0.02):
    for i in range(length):
        seasonal_component = np.sin(2 * np.pi * i / period)
        noise = np.random.normal(0, 0.1)
        value = seasonal_component + noise
        
        if np.random.rand() < anomaly_prob:
            value += np.random.normal(5, 2)  # Large deviation
        yield value

# Anomaly detection function using moving Z-Score
def anomaly_detection(window, threshold=3):
    mean = np.mean(window)
    std_dev = np.std(window)
    return abs(window[-1] - mean) > threshold * std_dev

# Real-time visualization of data stream and anomalies
def visualize(stream_generator, window_size=30, threshold=3):
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    window = deque(maxlen=window_size)
    anomalies = []

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

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    stream_gen = data_stream(length=1000, period=50, anomaly_prob=0.02)
    visualize(stream_gen, window_size=30, threshold=3)
