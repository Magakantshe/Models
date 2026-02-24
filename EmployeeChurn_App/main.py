# -*- coding: utf-8 -*-
import os
import sys

# Force Matplotlib to use PySide2
os.environ['QT_API'] = 'pyside2'

import matplotlib
matplotlib.use('Qt5Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # direct import
from matplotlib.figure import Figure
from PySide2.QtWidgets import (QApplication, QDialog, QVBoxLayout,
                               QFileDialog, QMessageBox, QWidget)
from PySide2.QtCore import Qt

# Survival analysis libraries
from lifelines import KaplanMeierFitter, CoxPHFitter

# Import the generated UI class
from FrontEnd import Ui_Dialog


class MainDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        # Connect page switching buttons
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        # Connect load button
        self.pushButton.clicked.connect(self.load_data_and_plot)

        # Placeholder for the current DataFrame
        self.df = None

        # Show an initial empty plot or a message
        self.show_welcome_message()

    def show_welcome_message(self):
        """Display a welcome message in each frame before data is loaded."""
        for frame in [self.frame_3, self.frame, self.frame_2, self.frame_4]:
            self._clear_layout(frame)
            layout = self._ensure_layout(frame)
            from PySide2.QtWidgets import QLabel
            label = QLabel("Click 'load' to select an Excel file\nand generate survival plots.")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

    def _ensure_layout(self, frame):
        """Return the layout of a frame, creating a QVBoxLayout if none exists."""
        if frame.layout() is None:
            layout = QVBoxLayout(frame)
            frame.setLayout(layout)
        else:
            layout = frame.layout()
        return layout

    def _clear_layout(self, frame):
        """Remove all widgets from the frame's layout."""
        layout = frame.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def load_data_and_plot(self):
        """Open file dialog, load Excel, preprocess data, and update all graphs."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Excel file", "", "Excel files (*.xlsx *.xls)")
        if not file_path:
            return

        try:
            # Read the Excel file
            df_raw = pd.read_excel(file_path)

            # --- Preprocessing (exactly as in your code) ---
            date_columns = ['StartDate', 'EndDate', 'DOB']
            df_raw[date_columns] = df_raw[date_columns].apply(pd.to_datetime, errors='coerce')

            today = pd.Timestamp.today()
            df_raw['EffectiveEndDate'] = df_raw['EndDate'].fillna(today)

            # Duration in months (using 30.44 days per month)
            df_raw['Duration'] = (df_raw['EffectiveEndDate'] - df_raw['StartDate']).dt.days / 30.44

            # Event: 1 if left, 0 if still employed
            df_raw['Event'] = df_raw['EndDate'].notna().astype(int)

            # Age
            df_raw['Age'] = today.year - df_raw['DOB'].dt.year

            # Age groups
            age_bins = [18, 25, 31, 37, 43, 49, 100]
            age_labels = ['18-25', '26-31', '32-37', '38-43', '44-49', '50+']
            df_raw['AgeGroup'] = pd.cut(df_raw['Age'], bins=age_bins, labels=age_labels)

            # Experience groups in months
            exp_bins = [0, 24, 60, 120, float('inf')]
            exp_labels = ['0-2 yrs', '2-5 yrs', '5-10 yrs', '10+ yrs']
            df_raw['ExperienceGroup'] = pd.cut(df_raw['Duration'], bins=exp_bins,
                                                labels=exp_labels, right=False)

            # Drop rows with missing essential data
            df_clean = df_raw.dropna(subset=['StartDate', 'DOB', 'Duration', 'Age'])

            self.df = df_clean

            # Update all graphs
            self.refresh_graphs()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load or process data:\n{e}")

    def refresh_graphs(self):
        """Clear all frames and embed new plots using the current DataFrame."""
        if self.df is None or self.df.empty:
            self.show_welcome_message()
            return

        # Clear each frame
        for frame in [self.frame_3, self.frame, self.frame_2, self.frame_4]:
            self._clear_layout(frame)

        # Embed the four plots
        self.embed_km_curve(self.frame_3, group_col='AgeGroup',
                            title='Survival by Age Group (6 months)')
        self.embed_km_curve(self.frame, group_col='ExperienceGroup',
                            title='Survival by Experience Group (6 months)')
        self.embed_km_curve(self.frame_2, group_col='Department',
                            title='Survival by Department (6 months)')
        self.embed_cox_barplot(self.frame_4)

    def embed_km_curve(self, frame, group_col, title, predict_months=6):
        """Plot Kaplan-Meier curves for the given group column and embed in frame."""
        try:
            layout = self._ensure_layout(frame)

            fig = Figure(figsize=(5, 4), dpi=100)
            canvas = FigureCanvasQTAgg(fig)  # use direct class

            # Safety check: ensure canvas is a QWidget
            if not isinstance(canvas, QWidget):
                raise TypeError(f"Canvas is not a QWidget, it's a {type(canvas)}")

            ax = fig.add_subplot(111)
            kmf = KaplanMeierFitter()

            # Loop over groups
            for group in self.df[group_col].dropna().unique():
                group_data = self.df[self.df[group_col] == group]
                durations = group_data['Duration']
                events = group_data['Event']
                kmf.fit(durations, event_observed=events, label=str(group))
                kmf.plot(ax=ax)

                # Print stats to console (optional)
                total = len(durations)
                surv_prob = kmf.predict(predict_months)
                est_leavers = total * (1 - surv_prob)
                print(f"{group_col} = {group}: total={total}, "
                      f"est. leavers after {predict_months:.1f} months = {est_leavers:.0f}")

            ax.set_title(title)
            ax.set_xlabel('Months since start')
            ax.set_ylabel('Survival Probability')
            ax.grid(True)
            ax.legend(title=group_col)

            layout.addWidget(canvas)
        except Exception as e:
            self._fallback_label(frame, f"KM plot failed: {e}")

    def embed_cox_barplot(self, frame):
        """Fit Cox model and plot horizontal bar chart of -log2(p-values)."""
        try:
            layout = self._ensure_layout(frame)

            # Prepare data for Cox model
            df_cox = self.df[['Duration', 'Event', 'Age', 'AgeGroup',
                              'ExperienceGroup', 'Department']].copy()
            df_cox = pd.get_dummies(df_cox, columns=['AgeGroup', 'ExperienceGroup', 'Department'],
                                    drop_first=True)

            cph = CoxPHFitter()
            cph.fit(df_cox, duration_col='Duration', event_col='Event')

            summary_df = cph.summary
            p_vals = summary_df['p']
            neglog2_p = -np.log2(p_vals)

            # Build DataFrame for plotting
            plot_df = (neglog2_p
                       .reset_index()
                       .rename(columns={'index': 'covariate', 0: '-log2(p)'})
                       .sort_values('-log2(p)'))

            # Create figure
            fig = Figure(figsize=(5, 4), dpi=100)
            canvas = FigureCanvasQTAgg(fig)

            if not isinstance(canvas, QWidget):
                raise TypeError(f"Canvas is not a QWidget, it's a {type(canvas)}")

            ax = fig.add_subplot(111)

            # Color bars based on significance (p < 0.05  <=>  -log2(p) > 4.32)
            colors = ['green' if x > 4.32 else 'gray' for x in plot_df['-log2(p)']]
            ax.barh(plot_df['covariate'], plot_df['-log2(p)'], color=colors)

            # Significance threshold line (p = 0.05)
            ax.axvline(4.32, color='red', linestyle='--', label='p = 0.05')
            ax.set_xlabel('-log₂(p-value)')
            ax.set_title('Cox Model – Variable Significance')
            ax.legend()

            layout.addWidget(canvas)
        except Exception as e:
            self._fallback_label(frame, f"Cox plot failed: {e}")

    def _fallback_label(self, frame, message):
        """Display an error label inside a frame when plotting fails."""
        layout = self._ensure_layout(frame)
        from PySide2.QtWidgets import QLabel
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)


def main():
    app = QApplication(sys.argv)
    dialog = MainDialog()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
