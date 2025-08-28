# Configuration file for Clinical Decision Support System

import streamlit as st

def configure_app():
    """Configure Streamlit app settings"""
    st.set_page_config(
        page_title="Clinical Decision Support System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/clinical-decision-support',
            'Report a bug': 'https://github.com/your-repo/clinical-decision-support/issues',
            'About': """
            # Clinical Decision Support System
            
            This application provides comprehensive healthcare analytics and clinical decision support
            through advanced data mining and NLP techniques.
            
            **Features:**
            - Medical text analysis and entity extraction
            - Drug interaction checking with severity classification
            - Patient risk stratification and recommendations
            - Interactive healthcare analytics dashboard
            - Research insights and statistical analysis
            
            **Developed for:** Healthcare professionals, researchers, and data scientists
            
            **Version:** 1.0.0
            """
        }
    )

# Dataset configuration
DATASET_CONFIG = {
    'clinical_discovery': {
        'filename': 'Clinical Data_Discovery_Cohort.csv',
        'type': 'csv',
        'description': 'Primary clinical cohort data with patient outcomes'
    },
    'clinical_validation': {
        'filename': 'Clinical_Data_Validation_Cohort.xlsx',
        'type': 'excel',
        'description': 'Validation cohort for research studies'
    },
    'drug_interactions': {
        'filename': 'db_drug_interactions.csv',
        'type': 'csv',
        'description': 'Comprehensive drug-drug interaction database'
    },
    'drug_reviews_test': {
        'filename': 'drugsComTest_raw.csv',
        'type': 'csv',
        'description': 'Patient drug reviews and ratings (test set)'
    },
    'drug_reviews_train': {
        'filename': 'drugsComTrain_raw.csv',
        'type': 'csv',
        'description': 'Patient drug reviews and ratings (training set)'
    },
    'medical_transcriptions': {
        'filename': 'mtsamples.csv',
        'type': 'csv',
        'description': 'Medical transcription samples across specialties'
    }
}

# NLP Configuration
NLP_CONFIG = {
    'max_text_length': 10000,
    'min_text_length': 10,
    'medical_entity_patterns': {
        'medications': r'\b(mg|mcg|ml|tablet|capsule|injection|dose|medication|drug|pill|aspirin|ibuprofen|acetaminophen|metformin|lisinopril|atorvastatin)\b',
        'symptoms': r'\b(pain|fever|nausea|headache|fatigue|dizzy|anxiety|depression|insomnia|cough|shortness of breath|chest pain)\b',
        'procedures': r'\b(surgery|operation|procedure|therapy|treatment|examination|test|biopsy|endoscopy|catheterization)\b',
        'body_parts': r'\b(heart|lung|liver|kidney|brain|stomach|blood|chest|abdomen|spine|joint|muscle)\b',
        'lab_values': r'\b(glucose|cholesterol|blood pressure|hemoglobin|creatinine|sodium|potassium|wbc|rbc)\b'
    },
    'phi_patterns': {
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'mrn': r'\bMRN\s*:?\s*\d+\b'
    }
}

# Risk Assessment Configuration
RISK_CONFIG = {
    'age_thresholds': {
        'high_risk': 65,
        'moderate_risk': 50
    },
    'medication_thresholds': {
        'polypharmacy': 5,
        'multiple_meds': 3
    },
    'high_risk_conditions': [
        'diabetes', 'hypertension', 'heart disease', 'kidney disease',
        'copd', 'cancer', 'stroke', 'heart failure', 'coronary artery disease'
    ],
    'risk_levels': {
        'low': {'min': 0, 'max': 3, 'color': 'green'},
        'moderate': {'min': 4, 'max': 6, 'color': 'orange'},
        'high': {'min': 7, 'max': 10, 'color': 'red'}
    }
}

# Visualization Configuration
VIZ_CONFIG = {
    'color_schemes': {
        'primary': 'viridis',
        'medical': 'RdBu',
        'risk': ['green', 'orange', 'red'],
        'sentiment': {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
    },
    'chart_height': 400,
    'chart_width': 800,
    'wordcloud_config': {
        'width': 800,
        'height': 400,
        'background_color': 'white',
        'colormap': 'viridis',
        'max_words': 100
    }
}

# Clinical Decision Support Configuration
CDS_CONFIG = {
    'interaction_severity_keywords': {
        'high': ['contraindicated', 'avoid', 'dangerous', 'severe', 'major'],
        'moderate': ['increase', 'enhance', 'potentiate', 'monitor', 'caution'],
        'minor': ['minor', 'slight', 'minimal', 'observe']
    },
    'icd10_codes': {
        'diabetes': 'E11.9 - Type 2 diabetes mellitus without complications',
        'hypertension': 'I10 - Essential hypertension',
        'depression': 'F32.9 - Major depressive disorder, single episode, unspecified',
        'anxiety': 'F41.9 - Anxiety disorder, unspecified',
        'pneumonia': 'J18.9 - Pneumonia, unspecified organism',
        'asthma': 'J45.9 - Asthma, unspecified',
        'copd': 'J44.1 - Chronic obstructive pulmonary disease with acute exacerbation',
        'heart failure': 'I50.9 - Heart failure, unspecified',
        'atrial fibrillation': 'I48.91 - Unspecified atrial fibrillation',
        'migraine': 'G43.909 - Migraine, unspecified, not intractable, without status migrainosus',
        'chest pain': 'R06.02 - Shortness of breath',
        'abdominal pain': 'R10.9 - Unspecified abdominal pain'
    }
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'cache_ttl': 3600,  # 1 hour
    'max_dataframe_size': 50000,  # Maximum rows to process
    'chunk_size': 1000,  # For processing large datasets
    'max_concurrent_operations': 5
}
