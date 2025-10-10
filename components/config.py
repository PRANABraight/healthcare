# src/config.py

# Using 'string' for object/str types is more modern and explicit.
# This schema defines the FINAL, CLEAN structure of your data.
PIPELINE_CONFIG = {
    'data_sources': {
        'clinical_data': {
            'path': 'data/Clinical Data_Discovery_Cohort.csv',
            'output_path': 'data/clean/clean_clinical_data.csv',
            'schema': {
                'patient_id': 'string',
                'age': 'int64',
                'gender': 'string',
                'blood_pressure_(systolic)': 'int64',
                'blood_pressure_(diastolic)': 'int64',
                'heart_rate_(bpm)': 'float64',
                'respiratory_rate_(breaths/min)': 'float64',
                'body_temperature_(c)': 'float64',
                'oxygen_saturation_(%)': 'float64'
            }
        },
        'drug_interactions': {
            'path': 'data/db_drug_interactions.csv',
            'output_path': 'data/clean/clean_drug_interactions.csv',
            'schema': {
                'drug1_name': 'string',
                'drug2_name': 'string',
                'interaction_description': 'string'
            }
        }
    }
}