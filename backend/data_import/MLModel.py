import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

load_dotenv()

api_key = os.getenv('API_KEY')

# Get database connection
def get_db_connection():
    return sqlite3.connect(r'backend\data\financial_data.db')

# Fetch table from the database
def get_table(table):
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(f'SELECT * FROM {table}', conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching table {table}: {e}")
        return None

# Load datasets
df_ratios = get_table('RatiosQuarter')
df_keyMetrics = get_table('KeyMetricsQuarter')
df_historic_prices = get_table('HistoricalPricesQuarter')
df_ratios.drop(columns=['period', 'calendarYear'], inplace=True, errors='ignore')
df_keyMetrics.drop(columns=['period', 'calendarYear'], inplace=True, errors='ignore')



# Merge dataframes on symbol and date
df = pd.merge(df_ratios, df_keyMetrics, on=['symbol', 'date'])
df = pd.merge(df, df_historic_prices[['symbol', 'date', 'stockPrice']], on=['symbol', 'date'])

# Drop irrelevant columns and target creation
df = df.dropna()  # Drop rows with missing values
X = df.drop(columns=['stockPrice', 'symbol', 'date'])
y = df['stockPrice'].diff().shift(-1).dropna()  # Target: Next quarter price - current quarter price

# Align the features with target
X = X.iloc[:-1]  # Drop the last row to match shifted target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)



# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),  # Regularization
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)  # Output: Single stock price prediction
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train the model
history = model.fit(X_train, y_train, validation_split=0.2, epochs=50, batch_size=32, verbose=1)

# Evaluate the model
loss, mae = model.evaluate(X_test, y_test, verbose=0)
print(f"Mean Absolute Error: {mae}")

# Make predictions
predictions = model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.plot(range(len(y_test)), y_test, label='Actual')
plt.plot(range(len(predictions)), predictions.flatten(), label='Predicted')
plt.legend()
plt.title('Stock Price Prediction')
plt.show()
