import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler

def preprocess_stock(df, config):
    df = df.copy()

    # --- THE DATE FIX ---
    df = df.reset_index()
    if 'index' in df.columns:
        df = df.rename(columns={'index': 'Date'})

    # Convert Date to datetime, ignoring errors if there's a weird row
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # --- NEW: THE NUMERIC FIX ---
    # This forces the 'Close' column to be standard numbers. 
    # 'coerce' turns any text (like a sub-header or the word 'null') into a NaN (blank)
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    df.sort_values('Date', inplace=True)
    
    # --- FIXED WARNING ---
    # Using ffill() and bfill() directly instead of fillna(method='ffill')
    df.ffill(inplace=True)
    df.bfill(inplace=True)

    # SG FILTER
    if config["USE_SG_FILTER"]:
        try:
            df['Smooth_Close'] = savgol_filter(
                df['Close'],
                config["WINDOW_LENGTH"],
                config["POLYORDER"]
            )
        except:
            df['Smooth_Close'] = df['Close']
    else:
        df['Smooth_Close'] = df['Close']

    base_col = 'Smooth_Close' if config["USE_SMOOTHED_FOR_FEATURES"] else 'Close'

    df['Return'] = df[base_col].pct_change()

    # Outlier removal
    z = np.abs((df['Return'] - df['Return'].mean()) / df['Return'].std())
    df = df[z < 3]

    df['MA_10'] = df[base_col].rolling(10).mean()
    df['EMA_10'] = df[base_col].ewm(span=10).mean()

    df.dropna(inplace=True)

    # Normalization
    if config["USE_NORMALIZATION"]:
        features = ['Smooth_Close', 'Return', 'MA_10', 'EMA_10']
        scaler = MinMaxScaler()
        df[features] = scaler.fit_transform(df[features])

    return df