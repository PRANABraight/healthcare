import pandas as pd

# Read Excel file
try:
    df = pd.read_excel('Clinical_Data_Validation_Cohort.xlsx')
    print("Excel file structure:")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("\nFirst 5 rows:")
    print(df.head())
except Exception as e:
    print(f"Error reading Excel: {e}")

# Also check CSV files structure
print("\n" + "="*50)
print("CSV FILES STRUCTURE:")

# Clinical discovery cohort
try:
    df1 = pd.read_csv('Clinical Data_Discovery_Cohort.csv')
    print(f"\nClinical Data_Discovery_Cohort.csv - Shape: {df1.shape}")
    print("Columns:", list(df1.columns))
except Exception as e:
    print(f"Error: {e}")

# Drug interactions
try:
    df2 = pd.read_csv('db_drug_interactions.csv')
    print(f"\ndb_drug_interactions.csv - Shape: {df2.shape}")
    print("Columns:", list(df2.columns))
except Exception as e:
    print(f"Error: {e}")

# Medical transcriptions
try:
    df3 = pd.read_csv('mtsamples.csv')
    print(f"\nmtsamples.csv - Shape: {df3.shape}")
    print("Columns:", list(df3.columns))
except Exception as e:
    print(f"Error: {e}")

# Drug reviews
try:
    df4 = pd.read_csv('drugsComTest_raw.csv')
    print(f"\ndrugsComTest_raw.csv - Shape: {df4.shape}")
    print("Columns:", list(df4.columns))
except Exception as e:
    print(f"Error: {e}")
