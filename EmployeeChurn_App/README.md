
---

## 📊 EmployeeChurn_App – Survival Analysis Dashboard

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
cd EmployeeChurn_App
pip install -r requirements.txt   # or install individually
python main.py

Click load and select your Excel file.

Data Format
The input Excel file must contain at least these columns:

StartDate – start date of employment (e.g., 2020-01-15)

EndDate – leave date (leave blank if still active)

DOB – date of birth

Department – department name
file, then load it into the app.

Troubleshooting
TypeError: addWidget with FigureCanvas – Ensure Matplotlib is using the Qt5Agg backend and that FigureCanvasQTAgg is correctly imported. The code in main.py includes a safety check and fallback label.

Missing columns – The app expects StartDate, EndDate, DOB, and Department. If your columns have different names, adjust the preprocessing part.

Empty graphs after loading – Check the console for error messages. The app will display a fallback label inside the frame if plotting fails.

Author
Created by Elphus Kgatla
