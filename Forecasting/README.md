#Monthly Budget Forecasting with NeuralProphet

This project implements a monthly time-series forecasting pipeline using NeuralProphet. It trains a model on historical budget data and generates forecasts with visualization of training, testing, and predicted values.

The project demonstrates:

Time-series preprocessing

Frequency handling (monthly end)

Train/test split

NeuralProphet modeling

Forecast visualization

Reproducible training setup

Project Structure . ├── budgetdata.csv ├── forecast.py └── README.md

budgetdata.csv – Input dataset

forecast.py – Training and forecasting script

README.md – Documentation

Requirements

Recommended stable environment:

Python 3.10

torch 2.5.1

neuralprophet >= 0.6.x

pandas

numpy

matplotlib

Important Compatibility Note

PyTorch 2.6 introduced secure checkpoint loading (weights_only=True by default), which is not fully compatible with current NeuralProphet releases.

If you encounter:

UnpicklingError: Weights only load failed

Downgrade PyTorch to:

torch==2.5.1

This resolves the issue.

Installation

Create a virtual environment:

python -m venv venv source venv/bin/activate # macOS/Linux venv\Scripts\activate # Windows

Install dependencies:

pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pip install neuralprophet pandas numpy matplotlib Dataset Format

The CSV file must contain the following columns:

Date Budget 2020-01-31 5000 2020-02-29 5200

The script renames:

Date → ds

Budget → y

The frequency is automatically handled as monthly end (ME).

Model Configuration

Example configuration:

model = NeuralProphet( seasonality_mode="multiplicative", learning_rate=0.01 )

model.fit(train_df, freq="ME")

Key settings:

seasonality_mode="multiplicative" handles proportional growth

freq="ME" specifies monthly end frequency

85% training split

15% testing split

Fixed random seed for reproducibility

Output

The script produces:

Forecasted monthly budget values

A plot comparing:

Training data

Test data

Model forecast

Model Extensions

This project can be extended with:

MAE, RMSE, and MAPE evaluation

Cross-validation

Hyperparameter tuning

Model comparison (Prophet, SARIMA, XGBoost)

API deployment (Flask or FastAPI)

Dashboard visualization (Streamlit)

Alternative Models

If NeuralProphet compatibility issues persist, consider:

Prophet

SARIMA (statsmodels)

Gradient boosting regression for time-series

License

MIT License
