
---

## 📊 employeeChurn_App – Survival Analysis Dashboard

A PySide2 desktop application that performs survival analysis on employee data and visualizes retention patterns.

### Features

- Load an Excel file (`.xlsx` or `.xls`) containing employee records.
- Automatically preprocess the data:
  - Convert date columns (`StartDate`, `EndDate`, `DOB`) to datetime.
  - Calculate employment duration in months.
  - Create an event indicator (1 if employee left, 0 if still active).
  - Compute age and assign age groups (`18‑25`, `26‑31`, `32‑37`, `38‑43`, `44‑49`, `50+`).
  - Assign experience groups based on tenure (`0‑2 yrs`, `2‑5 yrs`, `5‑10 yrs`, `10+ yrs`).
- Display three Kaplan‑Meier survival curves (by **Age Group**, **Experience Group**, and **Department**) in separate pages of a stacked widget.
- Fit a Cox proportional hazards model and show a horizontal bar chart of variable significance (`‑log₂(p‑value)`).
- Switch between graph pages using simple buttons.

### Requirements

- Python 3.7+
- PySide2
- pandas
- matplotlib
- numpy
- lifelines
- openpyxl

### How to Run

```bash
cd employeeChurn_App
pip install -r requirements.txt   # or install individually
python main.py
