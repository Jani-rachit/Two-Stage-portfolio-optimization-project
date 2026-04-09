import numpy as np

def create_sequences(data, seq_length=30):
    X, y = [], []

    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        # Assuming index 1 corresponds to the 'Return' column in your data array
        y.append(data[i+seq_length][1])  

    # Fixed the cut-off return statement here:
    return np.array(X), np.array(y)