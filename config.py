# config.py
# Configuration file for Clinical Decision Support System (CDSS)

import streamlit as st
import os

# -------------------------------------------------------
# 🩺 Streamlit App Configuration
# -------------------------------------------------------
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
            
            This application provides comprehensive healthcare analytics and decision support
            through data mining and NLP.
            
            **Features:**
            - Medical text analysis & entity extraction
            - Drug interaction severity classification
            - Patient risk stratification & recommendations
            - Interactive analytics dashboard
            
            **Version:** 1.0.0
            """
        }
    )


# -------------------------------------------------------
# 🧱 ETL Pipeline Configuration (For DataPipeline.py)
# -------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# config.py

# ETL Data Pipeline Configuration
DATA_PIPELINE_CONFIG = {
    'clinical_data': {
        'description': 'Processed clinical dataset for cancer survival analysis'
    }
}




# -------------------------------------------------------
# 📊 Dataset Metadata (for UI or documentation)
# -------------------------------------------------------
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
    'drug_reviews_train': {
        'filename': 'drugsComTrain_raw.csv',
        'type': 'csv',
        'description': 'Patient drug reviews and ratings (training set)'
    },
    'medical_transcriptions': {
        'filename': 'mtsamples.csv',
        'type': 'csv',
        'description': 'Medical transcription samples'
    }
}


# -------------------------------------------------------
# 🧬 NLP Configuration
# -------------------------------------------------------
NLP_CONFIG = {
    'max_text_length': 10000,
    'min_text_length': 10,
    'medical_entity_patterns': {
        'medications': r'\b(mg|mcg|ml|tablet|capsule|injection|dose|drug|aspirin|ibuprofen|metformin|atorvastatin)\b',
        'symptoms': r'\b(pain|fever|nausea|headache|fatigue|cough|shortness of breath)\b',
        'procedures': r'\b(surgery|therapy|treatment|test|biopsy|endoscopy)\b',
        'body_parts': r'\b(heart|lung|liver|kidney|brain|blood|chest|abdomen)\b',
        'lab_values': r'\b(glucose|cholesterol|blood pressure|hemoglobin|creatinine)\b'
    },
    'phi_patterns': {
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'mrn': r'\bMRN\s*:?\s*\d+\b'
    }
}


# -------------------------------------------------------
# ❤️ Risk Assessment Configuration
# -------------------------------------------------------
RISK_CONFIG = {
    'age_thresholds': {'high_risk': 65, 'moderate_risk': 50},
    'medication_thresholds': {'polypharmacy': 5, 'multiple_meds': 3},
    'high_risk_conditions': [
        'diabetes', 'hypertension', 'heart disease', 'kidney disease',
        'cancer', 'stroke', 'heart failure', 'coronary artery disease'
    ],
    'risk_levels': {
        'low': {'min': 0, 'max': 3, 'color': 'green'},
        'moderate': {'min': 4, 'max': 6, 'color': 'orange'},
        'high': {'min': 7, 'max': 10, 'color': 'red'}
    }
}


# -------------------------------------------------------
# 📈 Visualization Configuration
# -------------------------------------------------------
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


# -------------------------------------------------------
# 🧠 Clinical Decision Support Configuration
# -------------------------------------------------------
CDS_CONFIG = {
    'interaction_severity_keywords': {
        'high': ['contraindicated', 'avoid', 'dangerous', 'severe', 'major'],
        'moderate': ['monitor', 'caution', 'potentiate', 'enhance'],
        'minor': ['slight', 'minimal', 'observe']
    },
    'icd10_codes': {
        'diabetes': 'E11.9 - Type 2 diabetes mellitus',
        'hypertension': 'I10 - Essential hypertension',
        'depression': 'F32.9 - Major depressive disorder',
        'asthma': 'J45.9 - Asthma, unspecified',
        'copd': 'J44.1 - Chronic obstructive pulmonary disease'
    }
}


# -------------------------------------------------------
# ⚙️ Performance Configuration
# -------------------------------------------------------
PERFORMANCE_CONFIG = {
    'cache_ttl': 3600,
    'max_dataframe_size': 50000,
    'chunk_size': 1000,
    'max_concurrent_operations': 5
}
