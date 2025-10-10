# src/data_pipeline.py

import pandas as pd
import logging
from typing import Dict, Any

# Configure a professional logging system
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class DataPipeline:
    """
    An encapsulated, robust ETL pipeline for processing clinical data.
    This upgraded version handles common data quality issues like messy
    column names and incorrect data types.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        logger.info("Data Pipeline initialized with provided configuration.")

    def extract(self, file_key: str) -> pd.DataFrame:
        """STAGE 1: Extracts data from a source defined in the config."""
        filepath = self.config['data_sources'][file_key]['path']
        logger.info(f"Starting extraction from source: {filepath}")
        try:
            raw_df = pd.read_csv(filepath)
            logger.info(f"Successfully extracted {len(raw_df)} rows from {filepath}")
            return raw_df
        except FileNotFoundError:
            logger.error(f"Extraction failed: File not found at {filepath}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during extraction from {filepath}: {e}")
            raise

    def validate(self, df: pd.DataFrame, file_key: str) -> bool:
        """STAGE 2: Validates the data against a predefined clean schema."""
        schema = self.config['data_sources'][file_key]['schema']
        logger.info(f"Starting validation for '{file_key}' against CLEAN schema.")
        
        missing_columns = [col for col in schema.keys() if col not in df.columns]
        if missing_columns:
            logger.error(f"Validation failed: Missing required columns after standardization: {missing_columns}")
            return False

        logger.info(f"Validation for '{file_key}' passed successfully.")
        return True

    def transform(self, df: pd.DataFrame, file_key: str) -> pd.DataFrame:
        """STAGE 3: Cleans, coerces types, and enriches the validated data."""
        logger.info(f"Starting transformation for '{file_key}'.")
        transformed_df = df.copy()
        schema = self.config['data_sources'][file_key]['schema']

        # --- Type Coercion and Cleaning ---
        # This is a critical step to ensure the data perfectly matches the schema.
        for col, dtype in schema.items():
            if col in transformed_df.columns:
                try:
                    # Convert to numeric, coercing errors to NaT/NaN
                    transformed_df[col] = pd.to_numeric(transformed_df[col], errors='coerce')
                    
                    if 'int' in dtype:
                        # For integer columns, we must handle missing values before converting.
                        # A common strategy is to fill with the median.
                        median_val = transformed_df[col].median()
                        transformed_df[col] = transformed_df[col].fillna(median_val)
                    
                    # Finally, cast to the specific type defined in the schema
                    transformed_df[col] = transformed_df[col].astype(dtype)

                except Exception as e:
                    logger.error(f"Failed to process column '{col}' with type '{dtype}': {e}")
                    raise
        
        # --- Feature Enrichment ---
        if file_key == 'clinical_data' and 'age' in transformed_df.columns:
            bins = [0, 18, 40, 65, 100]
            labels = ['Pediatric', 'Adult', 'Middle-Aged', 'Senior']
            transformed_df['age_group'] = pd.cut(transformed_df['age'], bins=bins, labels=labels, right=False)
            logger.info("Enriched data with 'age_group' feature.")
        
        logger.info(f"Transformation complete. Final shape: {transformed_df.shape}")
        return transformed_df

    def load(self, df: pd.DataFrame, file_key: str) -> None:
        """💾 STAGE 4: Loads the transformed data to a destination."""
        output_path = self.config['data_sources'][file_key]['output_path']
        logger.info(f"Starting load process to destination: {output_path}")
        try:
            # Ensure the output directory exists
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            logger.info(f"Successfully loaded clean data to {output_path}")
        except Exception as e:
            logger.error(f"Failed to load data to {output_path}: {e}")
            raise

    @staticmethod
    def run_pipeline(config: Dict[str, Any], file_key: str) -> pd.DataFrame:
        """⚙️ ORCHESTRATOR: Executes the full ETL pipeline for a given data source."""
        logger.info(f"===== Starting ETL Pipeline for '{file_key}' =====")
        
        pipeline = DataPipeline(config)
        
        # Stage 1: Extract
        raw_data = pipeline.extract(file_key)
        
        # NEW ROBUST STEP: Standardize column names immediately after extraction.
        clean_columns_data = raw_data.copy()
        clean_columns_data.columns = [col.strip().lower().replace(' ', '_').replace('(', '').replace(')', '') for col in clean_columns_data.columns]
        logger.info("Standardized column names to snake_case.")
        
        # Stage 2: Validate using the clean, standardized column names
        if pipeline.validate(clean_columns_data, file_key):
            # Stage 3: Transform (now operates on data with clean columns)
            transformed_data = pipeline.transform(clean_columns_data, file_key)
            
            # Stage 4: Load
            pipeline.load(transformed_data, file_key)
            
            logger.info(f"===== ETL Pipeline for '{file_key}' Completed Successfully =====")
            return transformed_data
        else:
            logger.error(f"===== ETL Pipeline for '{file_key}' Failed Due to Validation Errors =====")
            raise ValueError(f"Data validation failed for {file_key}. Halting pipeline.")