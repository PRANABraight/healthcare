from src.controllers.main_controller import MainController
import os

if __name__ == "__main__":
    # Define paths directly here
    raw_path = r"C:/Users/prana/OneDrive/Desktop/4trimester/healthcare/data/Clinical_Data_Validation_Cohort.csv"
    cleaned_path = r"C:/Users/prana/OneDrive/Desktop/4trimester/healthcare/data/processed/Clinical_Data_Clean.csv"
    analytics_dir = r"C:/Users/prana/OneDrive/Desktop/4trimester/healthcare/data/analytics/plots"

    # Build a local pipeline config dictionary
    DATA_PIPELINE_CONFIG = {
        "input_path": raw_path,
        "file_type": "csv",
        "output_path": cleaned_path
    }

    # Ensure analytics directory exists
    os.makedirs(analytics_dir, exist_ok=True)

    # Initialize controller with config
    controller = MainController(DATA_PIPELINE_CONFIG, cleaned_path, analytics_dir)

    # Run ETL and Analytics
    controller.run_etl()
    controller.run_analytics()
