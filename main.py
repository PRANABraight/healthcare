
from src.data_pipeline import DataPipeline

# Correct assignments — NO trailing commas
path = r"C:/Users/prana/OneDrive/Desktop/4trimester/healthcare/data/Clinical_Data_Validation_Cohort.csv"
file_type = 'csv'
output_path = r"C:/Users/prana/OneDrive/Desktop/4trimester/healthcare/data/processed/Clinical_Data_Clean.csv"

if __name__ == "__main__":
    pipeline = DataPipeline(path, file_type, output_path)
    pipeline.run_pipeline()
