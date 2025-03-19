<<<<<<< HEAD
# Heart-Disease-Prediction
Final Year Project
=======

# ECG Analysis Tool

An application that analyzes ECG images to classify heart conditions and provide health insights.

## Overview

This tool uses machine learning to process and analyze ECG images. It can detect various conditions including:
- COVID-19
- Myocardial Infarction
- Abnormal Heartbeat
- History of MI
- Normal ECG

## Requirements

- Python 3.11 or higher
- PostgreSQL database

## Installation Instructions

### 1. Extract the Zip File

```bash
unzip ecg_analysis_app.zip -d ecg_analysis_app
cd ecg_analysis_app
```

### 2. Install Dependencies

```bash
pip install streamlit numpy opencv-python pillow scikit-learn plotly psycopg2-binary sqlalchemy
```

### 3. Set Up Database

Make sure PostgreSQL is installed and running. The application will automatically create the required tables in the database.

By default, the application connects to a PostgreSQL database with the following configuration:
- Host: localhost
- Port: 5432
- Database name: ecg_analysis
- Username: postgres
- Password: postgres

To use different database credentials, modify the `DATABASE_URL` in `src/database.py`.

## Running the Application

```bash
streamlit run main.py
```

The application will be available at http://localhost:8501 in your web browser.

## Using the Application

1. Upload an ECG image (PNG, JPG, or JPEG format)
2. The system will analyze the image and display:
   - Classification result with confidence level
   - Preprocessed ECG image
   - Feature analysis
   - Health analysis with recommendations
   - Option to download a detailed report

## Guidelines for Best Results

- Use clear, high-resolution ECG images
- Ensure the ECG grid is visible in the image
- Avoid blurry or distorted images

## Troubleshooting

If you encounter database errors, make sure:
1. PostgreSQL is running
2. Database credentials are correct
3. The database exists or you have permission to create it

If you have issues with image processing, verify that:
1. Image format is supported (PNG, JPG, JPEG)
2. Image is clear and readable
>>>>>>> fd948b5 (Assistant checkpoint: Created README.md with installation instructions)
