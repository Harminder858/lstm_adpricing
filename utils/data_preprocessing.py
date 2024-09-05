import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_data(file_path):
    """
    Load data from a CSV file.
    """
    return pd.read_csv(file_path, parse_dates=['date'])

def preprocess_data(df):
    """
    Preprocess the data for LSTM model.
    """
    # Convert categorical variables to one-hot encoding
    df = pd.get_dummies(df, columns=['platform', 'format', 'target_audience'])
    
    # Scale numerical features
    scaler = MinMaxScaler()
    numerical_columns = ['bid_amount', 'impressions', 'clicks', 'conversions', 'spend', 'revenue']
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    
    return df, scaler

def create_sequences(data, sequence_length):
    """
    Create sequences for LSTM model.
    """
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:(i + sequence_length)])
        y.append(data[i + sequence_length])
    return np.array(X), np.array(y)

def split_data(X, y, train_ratio=0.8):
    """
    Split data into training and testing sets.
    """
    split_idx = int(len(X) * train_ratio)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    return X_train, X_test, y_train, y_test