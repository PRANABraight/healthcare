# 📚 Data Dictionary

## Overview

This document provides comprehensive descriptions of all datasets, variables, and data structures used in the Clinical Decision Support System.

---

## Datasets

### 1. Clinical Discovery Cohort
**File**: `data/Clinical_Data_Discovery_Cohort.csv`  
**Purpose**: Training dataset for ML models  
**Records**: 1,000+  
**Source**: De-identified clinical trial data

| Variable | Type | Description | Range/Values | Missing % |
|----------|------|-------------|--------------|-----------|
| `PatientID` | String | Unique patient identifier | Alphanumeric | 0% |
| `Age` | Integer | Patient age in years | 18-100 | 0% |
| `sex` | Categorical | Patient gender | M, F | 0% |
| `Time` | Integer | Follow-up time in days | 1-3650 | 0% |
| `Event` | Binary | Adverse event occurred | 0=No, 1=Yes | 0% |
| `Dead or Alive` | Categorical | Survival status | Alive, Dead | 0% |
| `Comorbidity_Count` | Integer | Number of chronic conditions | 0-10 | 2% |
| `Medication_Count` | Integer | Number of medications | 0-20 | 1% |
| `Lab_Abnormal` | Integer | Number of abnormal lab values | 0-15 | 3% |
| `Smoking` | Binary | Current smoking status | 0=No, 1=Yes | 5% |
| `Alcohol` | Binary | Regular alcohol use | 0=No, 1=Yes | 5% |
| `BMI` | Float | Body Mass Index | 15-50 | 8% |
| `Blood_Pressure_Systolic` | Integer | Systolic BP (mmHg) | 80-200 | 4% |
| `Blood_Pressure_Diastolic` | Integer | Diastolic BP (mmHg) | 40-120 | 4% |
| `Creatinine` | Float | Serum creatinine (mg/dL) | 0.5-10 | 6% |

**Data Quality Notes:**
- All patient identifiers are de-identified
- Missing values imputed using median (numerical) or mode (categorical)
- Outliers validated against clinical plausibility

---

### 2. Clinical Validation Cohort
**File**: `data/Clinical_Data_Validation_Cohort.csv`  
**Purpose**: Independent validation of ML models  
**Records**: 500+  
**Source**: Separate clinical trial cohort

**Schema**: Same as Clinical Discovery Cohort (see above)

**Usage**: 
- Used only for final model validation
- Never used in training or hyperparameter tuning
- Ensures unbiased performance estimates

---

### 3. Drug Interactions Database
**File**: `data/db_drug_interactions.csv`  
**Purpose**: Drug-drug interaction checking  
**Records**: 22,000,000+  
**Source**: DrugBank, FDA databases

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `Drug 1` | String | First drug name (generic) | Warfarin |
| `Drug 2` | String | Second drug name (generic) | Aspirin |
| `Interaction Description` | Text | Description of interaction | Increased bleeding risk due to additive anticoagulant effects |

**Severity Classification** (derived from description):
- **High**: Contains "contraindicated", "avoid", "dangerous"
- **Moderate**: Contains "increase", "enhance", "monitor"
- **Minor**: All other interactions

**Data Quality Notes:**
- All drug names standardized to generic names
- Interactions are bidirectional (A-B same as B-A)
- Regular updates from FDA safety communications

---

### 4. Drug Reviews Dataset
**File**: `data/drugsComTrain_raw.csv` (training), `data/drugsComTest_raw.csv` (test)  
**Purpose**: Patient sentiment analysis and drug effectiveness insights  
**Records**: 110,000+ (combined)  
**Source**: Drugs.com patient reviews

| Variable | Type | Description | Range/Values |
|----------|------|-------------|--------------|
| `drugName` | String | Name of medication | Various |
| `condition` | String | Medical condition being treated | Various |
| `review` | Text | Patient review text | Free text |
| `rating` | Integer | Patient rating | 1-10 |
| `date` | Date | Review submission date | YYYY-MM-DD |
| `usefulCount` | Integer | Number of users who found review helpful | 0-1000+ |

**Sentiment Mapping:**
- Rating 1-3: Negative
- Rating 4-7: Neutral
- Rating 8-10: Positive

**Data Quality Notes:**
- Reviews anonymized
- HTML tags and special characters removed
- Duplicate reviews filtered

---

### 5. Medical Transcriptions
**File**: `data/mtsamples.csv`  
**Purpose**: Clinical text analysis and NLP training  
**Records**: 5,000+  
**Source**: MTSamples medical transcription database

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `description` | String | Brief description of case | Consult for laparoscopic gastric bypass |
| `medical_specialty` | String | Medical specialty | Surgery, Cardiology, etc. |
| `sample_name` | String | Type of medical document | Discharge Summary, Consult Note |
| `transcription` | Text | Full medical transcription | Complete clinical note |
| `keywords` | String | Key medical terms | Comma-separated keywords |

**Medical Specialties** (Top 10):
1. Surgery (15%)
2. Consult - History and Phy. (12%)
3. Cardiovascular / Pulmonary (10%)
4. Orthopedic (8%)
5. Radiology (7%)
6. Gastroenterology (6%)
7. Neurology (5%)
8. General Medicine (5%)
9. Obstetrics / Gynecology (4%)
10. Urology (4%)

---

### 6. Stroke Dataset
**File**: `data/healthcare-dataset-stroke-data.csv`  
**Purpose**: Risk factor analysis for cerebrovascular events  
**Records**: 5,000+  
**Source**: Healthcare records

| Variable | Type | Description | Range/Values | Missing % |
|----------|------|-------------|--------------|-----------|
| `id` | Integer | Unique identifier | Sequential | 0% |
| `gender` | Categorical | Patient gender | Male, Female, Other | 0% |
| `age` | Float | Patient age | 0.08-82 | 0% |
| `hypertension` | Binary | Hypertension diagnosis | 0=No, 1=Yes | 0% |
| `heart_disease` | Binary | Heart disease diagnosis | 0=No, 1=Yes | 0% |
| `ever_married` | Categorical | Marital status | Yes, No | 0% |
| `work_type` | Categorical | Employment type | Private, Self-employed, Govt_job, children, Never_worked | 0% |
| `Residence_type` | Categorical | Residence location | Urban, Rural | 0% |
| `avg_glucose_level` | Float | Average glucose (mg/dL) | 55-271 | 0% |
| `bmi` | Float | Body Mass Index | 10.3-97.6 | 4% |
| `smoking_status` | Categorical | Smoking history | formerly smoked, never smoked, smokes, Unknown | 30% |
| `stroke` | Binary | Stroke occurrence | 0=No, 1=Yes | 0% |

**Class Distribution:**
- No Stroke: 95.1%
- Stroke: 4.9%
- **Note**: Imbalanced dataset - SMOTE used for training

---

## Derived Features

### Clinical Risk Scores

#### Comorbidity Score
**Formula**: Weighted sum based on Charlson Comorbidity Index
```python
score = (
    diabetes * 1 +
    heart_disease * 1 +
    kidney_disease * 2 +
    liver_disease * 3 +
    cancer * 6
)
```

#### Polypharmacy Risk Level
**Categories**:
- Low: 0-3 medications
- Moderate: 4-6 medications
- High: 7-9 medications
- Severe: 10+ medications

#### Age Risk Category
**Categories**:
- Young Adult: 18-49 years
- Middle Age: 50-64 years
- Older Adult: 65-79 years
- Elderly: 80+ years

### Temporal Features

| Feature | Description | Calculation |
|---------|-------------|-------------|
| `days_since_diagnosis` | Time since initial diagnosis | Current date - diagnosis date |
| `treatment_duration` | Length of treatment period | End date - start date |
| `follow_up_period` | Total follow-up time | Last visit - first visit |
| `visit_frequency` | Average visits per month | Total visits / months |

### Interaction Features

| Feature | Description | Rationale |
|---------|-------------|-----------|
| `age_comorbidity_interaction` | Age × Comorbidity count | Synergistic risk effect |
| `medication_kidney_interaction` | Medication count × Kidney function | Drug clearance impact |
| `age_gender_interaction` | Age category × Gender | Gender-specific aging effects |

---

## Data Processing Pipeline

### 1. Data Loading
```python
# Load raw data
df = pd.read_csv('data/Clinical_Data_Discovery_Cohort.csv')
```

### 2. Data Cleaning
```python
# Handle missing values
df['BMI'].fillna(df['BMI'].median(), inplace=True)
df['Smoking'].fillna(0, inplace=True)

# Remove duplicates
df.drop_duplicates(subset='PatientID', inplace=True)

# Validate ranges
df = df[(df['Age'] >= 18) & (df['Age'] <= 100)]
```

### 3. Feature Engineering
```python
# Create derived features
df['age_category'] = pd.cut(df['Age'], bins=[0, 50, 65, 80, 100], 
                             labels=['Young', 'Middle', 'Older', 'Elderly'])
df['polypharmacy_level'] = pd.cut(df['Medication_Count'], 
                                   bins=[0, 3, 6, 9, 100],
                                   labels=['Low', 'Moderate', 'High', 'Severe'])
```

### 4. Data Validation
```python
# Ensure data quality
assert df['PatientID'].is_unique
assert df['Age'].between(18, 100).all()
assert df['Event'].isin([0, 1]).all()
```

---

## Data Storage

### File Formats

**CSV Files:**
- Encoding: UTF-8
- Delimiter: Comma (,)
- Quote Character: Double quote (")
- Line Terminator: \n

**Database Schema:**
```sql
CREATE TABLE patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    age INTEGER NOT NULL,
    gender VARCHAR(10),
    comorbidity_count INTEGER,
    medication_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE outcomes (
    outcome_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    event BOOLEAN,
    time_to_event INTEGER,
    status VARCHAR(20),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drug_interactions (
    interaction_id SERIAL PRIMARY KEY,
    drug_1 VARCHAR(100),
    drug_2 VARCHAR(100),
    description TEXT,
    severity VARCHAR(20)
);
```

---

## Data Governance

### Privacy & Security
- ✅ All patient data de-identified (HIPAA compliant)
- ✅ No PHI (Protected Health Information) included
- ✅ Secure storage with access controls
- ✅ Audit logging for data access

### Data Retention
- **Raw Data**: Retained indefinitely for reproducibility
- **Processed Data**: Cached for 30 days
- **Model Predictions**: Logged for 90 days
- **Audit Logs**: Retained for 7 years

### Data Quality Metrics
- **Completeness**: 95%+ for critical variables
- **Accuracy**: Validated against source systems
- **Consistency**: Cross-dataset validation
- **Timeliness**: Updated quarterly

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11 | Initial data dictionary creation |

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Maintained By:** Data Engineering Team
