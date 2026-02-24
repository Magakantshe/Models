Project Structure

├── main.py                     # Application entry point
├── userInterfaceForGraphsSufABQ.py  # Generated UI file (from Qt Designer)
├── README.md                   # This file
└── dummy_data.csv              # Example test data (optional)

Usage
Prepare your Excel file
Ensure it contains at least the following columns:

StartDate – start date of employment (e.g., 2020-01-15)

EndDate – leave date (leave blank if employee still active)

DOB – date of birth

Department – department name (e.g., Engineering, Sales)

Run the application

python main.py

Click the load button and select your Excel file.

After loading, three pages will be populated with:

Page 1 – Kaplan‑Meier curve by Age Group

Page 2 – Kaplan‑Meier curve by Experience Group (left) and Department (right)

Page 3 – Cox model significance bar chart

Use the buttons (frame1, frame2, frame3) to switch between pages.

Customization
Adjust bin edges – Modify age_bins, age_labels, exp_bins, or exp_labels in load_data_and_plot().

Change prediction horizon – The KM curves display survival after 6 months; you can change the predict_months argument in embed_km_curve().

Add more plots – Extend the embed_graphs method to include additional frames.

Example Dummy Data
A sample dummy_data.csv is provided for testing. It contains 20 records with plausible dates and departments. To use it, open the CSV in Excel and save as an .xlsx file, then load it into the app.

Troubleshooting
TypeError: addWidget with FigureCanvas – Ensure Matplotlib is using the Qt5Agg backend and that FigureCanvasQTAgg is correctly imported. The code in main.py includes a safety check and fallback label.

Missing columns – The app expects StartDate, EndDate, DOB, and Department. If your columns have different names, adjust the preprocessing part.

Empty graphs after loading – Check the console for error messages. The app will display a fallback label inside the frame if plotting fails.

Author
Created by Elphus Kgatla
