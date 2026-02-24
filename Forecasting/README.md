# Monthly Budget Forecasting with NeuralProphet

This project implements a monthly time-series forecasting pipeline using NeuralProphet. It trains a model on historical budget data and generates forecasts with visualization of training, testing, and predicted values.

## Features

- Time-series preprocessing
- Frequency handling (monthly end)
- Train/test split
- NeuralProphet modeling
- Forecast visualization
- Reproducible training setup

## Requirements

Important: NeuralProphet currently has a compatibility issue with PyTorch 2.6+. Use the recommended versions below.

- Python 3.10
- torch == 2.5.1
- neuralprophet >= 0.6.x
- pandas
- numpy
- matplotlib

### Installation

Create a virtual environment and install dependencies:

```bash
cd forecasting_model
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1
pip install neuralprophet pandas numpy matplotlib


Dataset Format
Place a CSV file (e.g., budgetdata.csv) in the folder with the following columns:

Date	Budget
2020-01-31	5000
2020-02-29	5200
The script automatically renames:

Date → ds

Budget → y

Frequency is handled as monthly end (ME).

Usage
Run the forecasting script:

bash
python forecast.py
The script will:

Load and preprocess the data

Split into training (85%) and testing (15%) sets

Train a NeuralProphet model with multiplicative seasonality

Generate a forecast plot comparing training, test, and predicted values

Model Configuration Example
python
model = NeuralProphet(
    seasonality_mode="multiplicative",
    learning_rate=0.01
)
model.fit(train_df, freq="ME")
Key settings:

seasonality_mode="multiplicative" handles proportional growth

freq="ME" specifies monthly end frequency

Fixed random seed ensures reproducibility

Output
A plot showing the training data, test data, and forecast.

Forecasted monthly budget values (printed or optionally saved).

Extending the Model
This basic pipeline can be enhanced with:

Evaluation metrics (MAE, RMSE, MAPE)

Cross-validation

Hyperparameter tuning

Model comparison (Prophet, SARIMA, XGBoost)

API deployment (Flask/FastAPI)

Interactive dashboard (Streamlit)

License
This project is provided for educational and professional use.

Author

Elphus
