# Efficient Data Stream Anomaly Detection

## Project Description
This project demonstrates anomaly detection in real-time data streams using Python. It simulates a data stream with seasonal patterns and random noise, and detects anomalies using the moving Z-Score method.

## Algorithm Explanation
### Moving Z-Score Method
The anomaly detection algorithm uses a moving Z-Score to identify outliers. The Z-Score of the most recent data point is calculated based on the mean and standard deviation of the recent data window. Anomalies are flagged if the Z-Score exceeds a specified threshold.

**Effectiveness**: This method adapts to changing data patterns by considering only recent values, making it effective for detecting outliers in dynamic streams.
