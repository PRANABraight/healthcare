import os
import logging
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


class DataPipeline:
    def __init__(self, path, file_type, output_path):
        self.config = {
            'clinical_data': {
                'path': path,
                'type': file_type,
                'output_path': output_path
            }
        }


    def extract(self, file_path, file_type):
        """Extract data from CSV or Excel file"""
        try:
            logging.info(f"Extracting data from {file_path}")
            if file_type == 'csv':
                df = pd.read_csv(file_path)
            elif file_type == 'excel':
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file type.")
            return df
        except Exception as e:
            logging.error(f"Error in extraction: {e}")
            return None

    def transform(self, df):
        """Perform data transformations"""
        logging.info("Standardizing column names...")
        df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

        logging.info("Handling missing values...")
        df = df.fillna("Unknown")

        logging.info("Converting data types where applicable...")
        if "age" in df.columns:
            df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0).astype(int)

        if "tumor_size_(cm)" in df.columns:
            df["tumor_size_(cm)"] = pd.to_numeric(df["tumor_size_(cm)"], errors="coerce")

        return df

    def validate(self, df):
        """Validate dataset schema"""
        logging.info("Validating data against schema...")

        required_columns = [
            "patient_id",
            "survival_time_(days)",
            "event_(death:_1,_alive:_0)",
            "tumor_size_(cm)",
            "grade",
            "stage_(tnm_8th_edition)",
            "age",
            "sex",
            "cigarette",
            "pack_per_year",
            "type.adjuvant",
            "batch",
            "egfr",
            "kras"
        ]

        df_columns = df.columns.tolist()
        missing = [col for col in required_columns if col not in df_columns]

        if missing:
            logging.error(f"Missing columns: {missing}")
            return False

        logging.info("✅ Validation passed successfully.")
        return True

    def load(self, df, output_path):
        """Save the cleaned and validated data"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            logging.info(f"Saved cleaned data to {output_path}")
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def run_pipeline(self):
        """Run the full ETL process"""
        for file_key, cfg in self.config.items():
            logging.info(f"===== Starting ETL Pipeline for '{file_key}' =====")

            df = self.extract(cfg['path'], cfg['type'])
            if df is None:
                logging.error(f"Extraction failed for {file_key}")
                continue

            df = self.transform(df)
            if not self.validate(df):
                logging.error(f"Validation failed for {file_key}")
                raise ValueError(f"Data validation failed for {file_key}")

            self.load(df, cfg['output_path'])
            
            logging.info(f"===== Pipeline for '{file_key}' Completed Successfully =====\n")
