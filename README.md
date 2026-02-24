Summary of Both Projects
1. employeeChurn_App – Survival Analysis Dashboard
An interactive desktop application built with PySide2 that performs survival analysis on employee data.

Features

Loads an Excel file with employee records (StartDate, EndDate, DOB, Department).

Automatically preprocesses data: calculates tenure, event indicator, age groups, and experience groups.

Displays Kaplan‑Meier survival curves by Age Group, Experience Group, and Department.

Fits a Cox proportional hazards model and visualizes variable significance as a horizontal bar chart.

Provides a simple button interface to switch between graph pages.

How to run

bash
cd employeeChurn_App
pip install PySide2 pandas matplotlib numpy lifelines openpyxl
python main.py
Then click load and select your Excel file.

2. forecasting_model – Monthly Budget Forecasting with NeuralProphet
A time‑series forecasting pipeline that uses NeuralProphet to predict monthly budget values.

Features

Reads a CSV file with Date and Budget columns.

Handles monthly frequency (ME) and splits data into training (85%) and testing (15%).

Trains a NeuralProphet model with multiplicative seasonality.

Generates a forecast plot comparing training, test, and predicted values.

Important compatibility note
Requires PyTorch 2.5.1 (not 2.6+) due to NeuralProphet’s checkpoint loading issue.

How to run

bash
cd forecasting_model
pip install torch==2.5.1 neuralprophet pandas numpy matplotlib
python forecast.py
Ensure your CSV file (e.g., budgetdata.csv) follows the expected format.
