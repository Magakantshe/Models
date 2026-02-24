import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import random

# ---- Fix PyTorch 2.6 issue ----
from torch.serialization import add_safe_globals
add_safe_globals([np.core.multiarray.scalar])

from neuralprophet import NeuralProphet

# ---- Reproducibility ----
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)

# ---- Load Data ----
df = pd.read_csv("/content/budgetdata.csv")
df.rename(columns={'Date': 'ds', 'Budget': 'y'}, inplace=True)
df['ds'] = pd.to_datetime(df['ds'])

# ---- Train/Test Split ----
split_idx = int(len(df) * 0.85)
train_df = df.iloc[:split_idx]
test_df = df.iloc[split_idx:]

# ---- Model ----
model = NeuralProphet(seasonality_mode="multiplicative")

# IMPORTANT: Your data is MONTHLY
model.fit(train_df, freq="ME")

# ---- Forecast ----
future = model.make_future_dataframe(test_df, n_historic_predictions=True)
forecast = model.predict(future)

# ---- Plot ----
plt.figure(figsize=(12,6))
plt.plot(train_df['ds'], train_df['y'], label='Train')
plt.plot(test_df['ds'], test_df['y'], label='Test')
plt.plot(forecast['ds'], forecast['yhat1'], '--', label='Forecast')

plt.legend()
plt.title("Monthly Budget Forecast")
plt.grid(True)
plt.show()
