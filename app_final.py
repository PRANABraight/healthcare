# 🏥 Clinical Decision Support System - Ultra-Minimal Version
# Simplified version with minimal dependencies to avoid import errors

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# Configuration
# =============================================================================

st.set_page_config(
    page_title="Clinical Decision Support System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# Data Loading Functions
# =============================================================================

@st.cache_data
def load_clinical_discovery_data():
    """Load clinical discovery cohort data"""
    try:
        df = pd.read_csv('Clinical Data_Discovery_Cohort.csv')
        return df
    except Exception as e:
        st.error(f"Error loading Clinical Discovery Data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_drug_interactions_data():
    """Load drug interactions database"""
    try:
        df = pd.read_csv('db_drug_interactions.csv')
        return df
    except Exception as e:
        st.error(f"Error loading Drug Interactions Data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_drug_reviews_data():
    """Load drug reviews data"""
    try:
        df = pd.read_csv('drugsComTest_raw.csv')
        return df
    except Exception as e:
        st.error(f"Error loading Drug Reviews Data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_medical_transcriptions_data():
    """Load medical transcriptions data"""
    try:
        df = pd.read_csv('mtsamples.csv')
        return df
    except Exception as e:
        st.error(f"Error loading Medical Transcriptions Data: {e}")
        return pd.DataFrame()

# =============================================================================
# Core Functions (No External Dependencies)
# =============================================================================

def clean_text(text):
    """Clean and preprocess text data"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'&[a-z]+;|&#[0-9]+;', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = ' '.join(text.split())
    
    return text

def extract_medical_entities(text):
    """Extract potential medical entities from text using enhanced patterns"""
    medical_patterns = {
        'medications': r'\b(mg|mcg|ml|tablet|capsule|injection|dose|medication|drug|pill|aspirin|metformin|lisinopril|atorvastatin|amlodipine|omeprazole|levothyroxine|albuterol|insulin|warfarin|prednisone|ibuprofen|acetaminophen|hydrocodone|sertraline|tramadol)\b',
        'symptoms': r'\b(pain|fever|nausea|headache|fatigue|dizzy|dizziness|anxiety|depression|insomnia|cough|shortness of breath|chest pain|abdominal pain|back pain|joint pain|muscle pain|sore throat|runny nose|congestion|weakness|numbness|tingling|swelling|rash|itching)\b',
        'procedures': r'\b(surgery|operation|procedure|therapy|treatment|examination|test|biopsy|x-ray|ct scan|mri|ultrasound|blood test|lab work|ekg|echocardiogram|colonoscopy|endoscopy|mammogram|vaccination|injection|infusion|dialysis)\b',
        'body_parts': r'\b(heart|lung|liver|kidney|brain|stomach|blood|chest|abdomen|head|neck|throat|arm|leg|hand|foot|back|spine|knee|shoulder|hip|ankle|wrist|elbow|eye|ear|nose|mouth|skin|muscle|bone|joint)\b',
        'conditions': r'\b(diabetes|hypertension|asthma|copd|arthritis|depression|anxiety|cancer|tumor|infection|pneumonia|bronchitis|migraine|seizure|stroke|heart attack|heart disease|kidney disease|liver disease|anemia|obesity)\b',
        'vital_signs': r'\b(blood pressure|bp|heart rate|pulse|temperature|temp|oxygen saturation|weight|height|bmi|respiratory rate)\b'
    }
    
    entities = {}
    for category, pattern in medical_patterns.items():
        matches = re.findall(pattern, text.lower(), re.IGNORECASE)
        entities[category] = list(set(matches))
    
    return entities

def analyze_sentiment(text):
    """Simple sentiment analysis"""
    positive_words = ['good', 'great', 'excellent', 'effective', 'helpful', 'better', 'improved', 'works', 'amazing', 'perfect']
    negative_words = ['bad', 'terrible', 'awful', 'ineffective', 'worse', 'side effects', 'problems', 'disappointed', 'useless', 'horrible']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return 'Positive'
    elif neg_count > pos_count:
        return 'Negative'
    else:
        return 'Neutral'

def check_drug_interactions(drug_list, interactions_df):
    """Check for drug-drug interactions"""
    if interactions_df.empty or len(drug_list) < 2:
        return []
    
    interactions = []
    drug_list_lower = [drug.lower().strip() for drug in drug_list]
    
    for i, drug1 in enumerate(drug_list_lower):
        for j, drug2 in enumerate(drug_list_lower):
            if i != j:
                interaction1 = interactions_df[
                    (interactions_df['Drug 1'].str.lower().str.contains(drug1, na=False)) &
                    (interactions_df['Drug 2'].str.lower().str.contains(drug2, na=False))
                ]
                
                if not interaction1.empty:
                    interactions.extend(interaction1.to_dict('records'))
    
    return interactions

def calculate_patient_risk_score(patient_data):
    """
    Calculate patient risk score based on evidence-based clinical factors
    
    Risk factors based on:
    - Age-related risk (geriatric medicine guidelines)
    - Comorbidity burden (Charlson Comorbidity Index principles)
    - Polypharmacy risk (Beers Criteria considerations)
    - Laboratory abnormalities
    
    Returns: (risk_score: int, risk_factors: list, evidence_notes: list)
    """
    risk_score = 0
    risk_factors = []
    evidence_notes = []
    
    # Age-based risk (Evidence: Geriatric medicine literature)
    age = patient_data.get('age', 0)
    if age > 80:
        risk_score += 3
        risk_factors.append("Very advanced age (>80)")
        evidence_notes.append("Age >80 associated with increased frailty and adverse outcomes")
    elif age > 65:
        risk_score += 2
        risk_factors.append("Advanced age (>65)")
        evidence_notes.append("Age >65 increases risk of complications and drug interactions")
    elif age > 50:
        risk_score += 1
        risk_factors.append("Middle age (50-65)")
        evidence_notes.append("Age 50-65 associated with increased chronic disease prevalence")
    
    # Comorbidity-based risk (Evidence: Charlson Comorbidity Index)
    conditions = patient_data.get('conditions', [])
    high_risk_conditions = {
        'diabetes': 2,
        'heart disease': 3,
        'kidney disease': 2,
        'liver disease': 3,
        'cancer': 4,
        'stroke': 2,
        'copd': 2,
        'dementia': 3
    }
    
    moderate_risk_conditions = {
        'hypertension': 1,
        'arthritis': 1,
        'depression': 1,
        'anxiety': 1
    }
    
    for condition in conditions:
        condition_lower = condition.lower()
        
        # Check high-risk conditions
        for hr_cond, score in high_risk_conditions.items():
            if hr_cond in condition_lower:
                risk_score += score
                risk_factors.append(f"High-risk condition: {condition}")
                evidence_notes.append(f"{condition} significantly increases clinical complexity")
                break
        else:
            # Check moderate-risk conditions if not high-risk
            for mr_cond, score in moderate_risk_conditions.items():
                if mr_cond in condition_lower:
                    risk_score += score
                    risk_factors.append(f"Moderate-risk condition: {condition}")
                    evidence_notes.append(f"{condition} contributes to overall disease burden")
                    break
    
    # Polypharmacy risk (Evidence: Beers Criteria, STOPP/START criteria)
    med_count = patient_data.get('medication_count', 0)
    if med_count > 10:
        risk_score += 4
        risk_factors.append(f"Severe polypharmacy ({med_count} medications)")
        evidence_notes.append("≥10 medications dramatically increases adverse drug events")
    elif med_count > 5:
        risk_score += 2
        risk_factors.append(f"Polypharmacy ({med_count} medications)")
        evidence_notes.append("5-9 medications increases drug interaction risk")
    elif med_count > 3:
        risk_score += 1
        risk_factors.append(f"Multiple medications ({med_count})")
        evidence_notes.append("3-4 medications requires monitoring for interactions")
    
    # Laboratory abnormalities
    lab_abnormal = patient_data.get('abnormal_labs', 0)
    if lab_abnormal > 3:
        risk_score += 3
        risk_factors.append(f"Multiple lab abnormalities ({lab_abnormal})")
        evidence_notes.append("Multiple abnormal labs suggest multisystem dysfunction")
    elif lab_abnormal > 0:
        risk_score += lab_abnormal
        risk_factors.append(f"{lab_abnormal} abnormal lab value(s)")
        evidence_notes.append("Abnormal labs require monitoring and intervention")
    
    # Additional risk factors
    smoking = patient_data.get('smoking', False)
    if smoking:
        risk_score += 2
        risk_factors.append("Current smoker")
        evidence_notes.append("Smoking increases cardiovascular and respiratory risks")
    
    alcohol = patient_data.get('alcohol', False)
    if alcohol:
        risk_score += 1
        risk_factors.append("Regular alcohol use")
        evidence_notes.append("Alcohol use may interact with medications and affect organs")
    
    return min(risk_score, 15), risk_factors, evidence_notes

def suggest_medical_codes(clinical_text):
    """Suggest potential ICD-10 codes based on clinical text"""
    icd10_mapping = {
        # Endocrine disorders
        'diabetes': 'E11.9 - Type 2 diabetes mellitus without complications',
        'type 1 diabetes': 'E10.9 - Type 1 diabetes mellitus without complications',
        'hyperthyroidism': 'E05.9 - Thyrotoxicosis, unspecified',
        'hypothyroidism': 'E03.9 - Hypothyroidism, unspecified',
        'obesity': 'E66.9 - Obesity, unspecified',
        
        # Cardiovascular disorders
        'hypertension': 'I10 - Essential hypertension',
        'heart disease': 'I25.9 - Chronic ischemic heart disease, unspecified',
        'heart attack': 'I21.9 - Acute myocardial infarction, unspecified',
        'atrial fibrillation': 'I48.91 - Unspecified atrial fibrillation',
        'heart failure': 'I50.9 - Heart failure, unspecified',
        'stroke': 'I63.9 - Cerebral infarction, unspecified',
        'chest pain': 'R06.02 - Shortness of breath',
        
        # Mental health disorders
        'depression': 'F32.9 - Major depressive disorder, single episode, unspecified',
        'anxiety': 'F41.9 - Anxiety disorder, unspecified',
        'panic disorder': 'F41.0 - Panic disorder',
        'bipolar': 'F31.9 - Bipolar disorder, unspecified',
        'ptsd': 'F43.10 - Post-traumatic stress disorder, unspecified',
        'insomnia': 'G47.00 - Insomnia, unspecified',
        
        # Respiratory disorders
        'asthma': 'J45.9 - Asthma, unspecified',
        'copd': 'J44.1 - Chronic obstructive pulmonary disease with acute exacerbation',
        'pneumonia': 'J18.9 - Pneumonia, unspecified organism',
        'bronchitis': 'J40 - Bronchitis, not specified as acute or chronic',
        'shortness of breath': 'R06.02 - Shortness of breath',
        'cough': 'R05 - Cough',
        
        # Gastrointestinal disorders
        'gerd': 'K21.9 - Gastro-esophageal reflux disease without esophagitis',
        'ulcer': 'K27.9 - Peptic ulcer, site unspecified, unspecified as acute or chronic',
        'nausea': 'R11.10 - Vomiting, unspecified',
        'diarrhea': 'K59.1 - Diarrhea, unspecified',
        'constipation': 'K59.00 - Constipation, unspecified',
        'abdominal pain': 'R10.9 - Unspecified abdominal pain',
        
        # Neurological disorders
        'headache': 'G44.1 - Vascular headache, not elsewhere classified',
        'migraine': 'G43.909 - Migraine, unspecified, not intractable, without status migrainosus',
        'seizure': 'R56.9 - Unspecified convulsions',
        'dizziness': 'R42 - Dizziness and giddiness',
        'memory loss': 'R41.3 - Other amnesia',
        
        # Musculoskeletal disorders
        'arthritis': 'M19.90 - Unspecified osteoarthritis, unspecified site',
        'back pain': 'M54.9 - Dorsalgia, unspecified',
        'knee pain': 'M25.561 - Pain in right knee',
        'joint pain': 'M25.9 - Joint disorder, unspecified',
        'fracture': 'S72.9 - Fracture of unspecified part of unspecified femur',
        
        # Infectious diseases
        'fever': 'R50.9 - Fever, unspecified',
        'infection': 'A49.9 - Bacterial infection, unspecified',
        'uti': 'N39.0 - Urinary tract infection, site not specified',
        'flu': 'J11.1 - Influenza due to unidentified influenza virus with other respiratory manifestations',
        
        # Skin conditions
        'rash': 'R21 - Rash and other nonspecific skin eruption',
        'eczema': 'L30.9 - Dermatitis, unspecified',
        'psoriasis': 'L40.9 - Psoriasis, unspecified',
        
        # Genitourinary disorders
        'kidney disease': 'N18.9 - Chronic kidney disease, unspecified',
        'incontinence': 'R32 - Unspecified urinary incontinence',
        
        # Other common conditions
        'fatigue': 'R53.83 - Other fatigue',
        'weight loss': 'R63.4 - Abnormal weight loss',
        'weight gain': 'R63.5 - Abnormal weight gain',
        'anemia': 'D64.9 - Anemia, unspecified',
        'edema': 'R60.9 - Edema, unspecified'
    }
    
    suggested_codes = []
    text_lower = clinical_text.lower()
    
    # Check for exact matches and partial matches
    for condition, code in icd10_mapping.items():
        if condition in text_lower:
            suggested_codes.append(code)
    
    return suggested_codes

# =============================================================================
# Main Application
# =============================================================================

def main():
    # Title
    st.title("🏥 Clinical Decision Support System")
    st.markdown("### *Healthcare Data Analytics & Clinical Decision Support*")
    
    # Clinical Disclaimer
    st.warning("""
    **⚠️ CLINICAL DISCLAIMER:** This application is a decision support tool designed to assist healthcare professionals. 
    It is **NOT** a substitute for clinical judgment, professional medical advice, diagnosis, or treatment. 
    All clinical decisions should be made by qualified healthcare providers based on individual patient assessment 
    and established clinical guidelines.
    """)
    
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading healthcare datasets..."):
        clinical_discovery = load_clinical_discovery_data()
        drug_interactions = load_drug_interactions_data()
        drug_reviews = load_drug_reviews_data()
        medical_transcriptions = load_medical_transcriptions_data()
    
    # Sidebar
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio(
        "Select Module:",
        [
            "🏠 Dashboard",
            "📝 Text Analysis", 
            "💊 Drug Interactions",
            "⚠️ Risk Assessment",
            "📊 Analytics",
            "👥 Team"
        ]
    )
    
    # Data status
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Data Status")
    datasets = {
        "Clinical Discovery": len(clinical_discovery),
        "Drug Interactions": len(drug_interactions),
        "Drug Reviews": len(drug_reviews),
        "Medical Transcriptions": len(medical_transcriptions)
    }
    
    for name, count in datasets.items():
        if count > 0:
            st.sidebar.success(f"✅ {name}: {count:,}")
        else:
            st.sidebar.error(f"❌ {name}: No data")
    
    # Main content
    if page == "🏠 Dashboard":
        show_dashboard(clinical_discovery, drug_interactions, drug_reviews, medical_transcriptions)
    elif page == "📝 Text Analysis":
        show_text_analysis(medical_transcriptions, drug_reviews)
    elif page == "💊 Drug Interactions":
        show_drug_interactions(drug_interactions)
    elif page == "⚠️ Risk Assessment":
        show_risk_assessment(clinical_discovery)
    elif page == "📊 Analytics":
        show_analytics(clinical_discovery, drug_reviews, medical_transcriptions)
    elif page == "👥 Team":
        show_team()

def show_dashboard(clinical_discovery, drug_interactions, drug_reviews, medical_transcriptions):
    """Display main dashboard"""
    st.header("📊 Healthcare Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", len(clinical_discovery))
    with col2:
        st.metric("Drug Interactions", len(drug_interactions))
    with col3:
        st.metric("Drug Reviews", len(drug_reviews))
    with col4:
        st.metric("Medical Records", len(medical_transcriptions))
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if not clinical_discovery.empty and 'sex' in clinical_discovery.columns:
            gender_counts = clinical_discovery['sex'].value_counts()
            fig = px.pie(values=gender_counts.values, names=gender_counts.index,
                        title="Patient Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not drug_reviews.empty and 'rating' in drug_reviews.columns:
            fig = px.histogram(drug_reviews.head(1000), x='rating', 
                              title='Drug Rating Distribution (Sample)')
            st.plotly_chart(fig, use_container_width=True)
    
    # Additional analytics
    if not clinical_discovery.empty:
        st.subheader("Clinical Outcomes Analysis")
        
        if 'Event' in clinical_discovery.columns:
            event_rate = clinical_discovery['Event'].mean() * 100
            st.info(f"Overall Event Rate: {event_rate:.1f}%")
            
            if 'Time' in clinical_discovery.columns:
                fig = px.histogram(clinical_discovery, x='Time', color='Dead or Alive',
                                 title='Follow-up Time Distribution')
                st.plotly_chart(fig, use_container_width=True)
    
    # Sample data
    st.subheader("📋 Sample Data")
    
    tab1, tab2, tab3 = st.tabs(["Clinical Data", "Drug Reviews", "Interactions"])
    
    with tab1:
        if not clinical_discovery.empty:
            st.dataframe(clinical_discovery.head())
    
    with tab2:
        if not drug_reviews.empty:
            st.dataframe(drug_reviews.head())
    
    with tab3:
        if not drug_interactions.empty:
            st.dataframe(drug_interactions.head())

def show_text_analysis(medical_transcriptions, drug_reviews):
    """Display text analysis interface"""
    st.header("📝 Clinical Text Analysis")
    
    # Text input
    text_input = st.text_area(
        "Enter clinical text for analysis:",
        placeholder="Example: Patient presents with chest pain and shortness of breath. Takes aspirin and metformin daily...",
        height=150
    )
    
    if text_input and st.button("🔍 Analyze Text"):
        # Clean text
        cleaned_text = clean_text(text_input)
        
        # Extract entities
        entities = extract_medical_entities(text_input)
        
        # Store results in session state for export
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = []
        
        result = {
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'text': text_input,
            'entities': entities,
            'sentiment': analyze_sentiment(text_input),
            'codes': suggest_medical_codes(text_input)
        }
        st.session_state.analysis_results.append(result)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏥 Medical Entities")
            for category, items in entities.items():
                st.write(f"**{category.title()}:**")
                if items:
                    for item in items:
                        st.write(f"• {item}")
                else:
                    st.write("None detected")
        
        with col2:
            st.subheader("Analysis Results")
            
            # Sentiment
            sentiment = analyze_sentiment(text_input)
            color = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}[sentiment]
            st.markdown(f"**Sentiment:** :{color}[{sentiment}]")
            
            # Medical codes
            codes = suggest_medical_codes(text_input)
            st.write("**Suggested ICD-10 Codes:**")
            if codes:
                for code in codes:
                    st.write(f"• {code}")
            else:
                st.write("• No specific codes suggested")
        
        # Export option
        if len(st.session_state.analysis_results) > 0:
            st.markdown("---")
            if st.button("📥 Export Analysis History"):
                df_results = pd.DataFrame(st.session_state.analysis_results)
                csv = df_results.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"clinical_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    # Word frequency analysis
    if not medical_transcriptions.empty:
        st.markdown("---")
        st.subheader("📊 Word Frequency Analysis")
        
        # Find the text column (try different possible names)
        text_col = None
        for col in medical_transcriptions.columns:
            if any(keyword in col.lower() for keyword in ['transcription', 'text', 'description', 'note']):
                text_col = col
                break
        
        if text_col:
            try:
                # Get sample text
                sample_text = ' '.join(medical_transcriptions[text_col].dropna().head(50).astype(str))
                cleaned_sample = clean_text(sample_text)
                
                if cleaned_sample.strip():
                    # Count words
                    words = cleaned_sample.split()
                    # Filter out very short words and common stop words
                    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'did', 'do', 'does', 'done'}
                    filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
                    
                    word_counts = Counter(filtered_words)
                    top_words = dict(word_counts.most_common(15))
                    
                    if top_words:
                        # Create chart
                        fig = px.bar(x=list(top_words.values()), 
                                     y=list(top_words.keys()),
                                     orientation='h',
                                     title="Top 15 Medical Terms")
                        fig.update_layout(yaxis=dict(autorange="reversed"))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No significant terms found in medical transcriptions")
                else:
                    st.warning("No text content found in medical transcriptions")
            except Exception as e:
                st.error(f"Error analyzing medical transcriptions: {e}")
        else:
            st.warning("No suitable text column found in medical transcriptions data")

def show_drug_interactions(drug_interactions):
    """Display drug interaction checker"""
    st.header("💊 Drug Interaction Checker")
    
    if drug_interactions.empty:
        st.error("No drug interaction data available")
        return
    
    # Get unique drugs (limited for performance)
    try:
        # Optimize drug loading for better performance
        drug_1_list = drug_interactions['Drug 1'].dropna().unique()
        drug_2_list = drug_interactions['Drug 2'].dropna().unique()
        all_drugs = list(set(list(drug_1_list) + list(drug_2_list)))
        
        # Filter and limit drugs for performance
        all_drugs = sorted([drug for drug in all_drugs if isinstance(drug, str) and len(drug) > 1])[:500]
        
        st.info(f"💊 **Drug Database**: {len(drug_interactions):,} interactions | {len(all_drugs)} unique drugs available")
        
    except Exception as e:
        st.error(f"Error loading drug list: {e}")
        all_drugs = []
    
    # Drug selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_drugs = st.multiselect(
            "Select drugs to check for interactions:",
            options=all_drugs,
            help="Select at least 2 drugs"
        )
        
        # Manual entry
        manual_drugs = st.text_input(
            "Or enter drug names manually (comma-separated):",
            placeholder="e.g., aspirin, warfarin, metformin"
        )
        
        if manual_drugs:
            # Validate and clean manual drug input
            manual_drug_list = []
            for drug in manual_drugs.split(','):
                drug = drug.strip()
                if drug and len(drug) >= 2:  # Minimum length validation
                    # Basic sanitization - remove special characters except hyphens
                    drug = re.sub(r'[^a-zA-Z0-9\-\s]', '', drug)
                    if drug:  # If still valid after sanitization
                        manual_drug_list.append(drug)
            
            if manual_drug_list:
                selected_drugs.extend(manual_drug_list)
                selected_drugs = list(set(selected_drugs))  # Remove duplicates
                
                # Show validation feedback
                if len(manual_drug_list) > 0:
                    st.success(f"✅ Added {len(manual_drug_list)} drugs: {', '.join(manual_drug_list)}")
            else:
                st.warning("⚠️ Please enter valid drug names (at least 2 characters each)")
        
        # Show current selection
        if selected_drugs:
            st.info(f"**Selected drugs ({len(selected_drugs)}):** {', '.join(selected_drugs)}")
    
    with col2:
        st.info(
            "💡 **Tips:**\n"
            "• Enter at least 2 drugs\n"
            "• Use generic names when possible\n" 
            "• Always consult healthcare providers"
        )
    
    # Check interactions
    if len(selected_drugs) >= 2 and st.button("🔍 Check Interactions"):
        with st.spinner("Checking drug interactions..."):
            interactions = check_drug_interactions(selected_drugs, drug_interactions)
            
            if interactions:
                st.subheader("⚠️ Interaction Alerts")
                
                for i, interaction in enumerate(interactions):
                    with st.expander(f"Interaction {i+1}: {interaction['Drug 1']} ↔ {interaction['Drug 2']}", expanded=True):
                        st.write("**Description:**")
                        st.write(interaction['Interaction Description'])
                        
                        # Severity assessment
                        description = interaction['Interaction Description'].lower()
                        if any(word in description for word in ['contraindicated', 'avoid', 'dangerous']):
                            st.error("🚨 HIGH SEVERITY - Avoid combination")
                        elif any(word in description for word in ['increase', 'enhance', 'monitor']):
                            st.warning("⚠️ MODERATE SEVERITY - Monitor closely")
                        else:
                            st.info("ℹ️ MINOR - Routine monitoring")
                
            else:
                st.success("✅ No known interactions found")
                st.info("Note: Always consult healthcare professionals for clinical decisions")
    
    elif len(selected_drugs) == 1:
        st.info("Please select at least 2 drugs to check for interactions")
    
    # Statistics
    st.markdown("---")
    st.subheader("📊 Database Statistics")
    
    drug1_counts = drug_interactions['Drug 1'].value_counts().head(10)
    fig = px.bar(x=drug1_counts.values, y=drug1_counts.index,
                orientation='h', title="Top 10 Drugs by Interaction Count")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

def show_risk_assessment(clinical_discovery):
    """Display patient risk assessment"""
    st.header("⚠️ Patient Risk Assessment")
    
    # Input form
    with st.form("risk_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Demographics:**")
            age = st.number_input("Age", min_value=0, max_value=120, value=50)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            conditions = st.multiselect(
                "Medical Conditions:",
                ["Diabetes", "Hypertension", "Heart Disease", "Kidney Disease", "COPD", "Cancer"]
            )
        
        with col2:
            st.write("**Clinical Factors:**")
            medication_count = st.number_input("Number of Medications", min_value=0, value=0)
            abnormal_labs = st.number_input("Abnormal Lab Values", min_value=0, value=0)
            
            st.write("**Lifestyle:**")
            smoking = st.checkbox("Current Smoker")
            alcohol = st.checkbox("Regular Alcohol Use")
        
        submitted = st.form_submit_button("🔍 Calculate Risk Score")
    
    if submitted:
        patient_data = {
            'age': age,
            'gender': gender,
            'conditions': conditions,
            'medication_count': medication_count,
            'abnormal_labs': abnormal_labs,
            'smoking': smoking,
            'alcohol': alcohol
        }
        
        risk_score, risk_factors, evidence_notes = calculate_patient_risk_score(patient_data)
        
        # Display results
        st.subheader("📊 Risk Assessment Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_level = "LOW" if risk_score <= 4 else "MODERATE" if risk_score <= 8 else "HIGH"
            colors = {"LOW": "green", "MODERATE": "orange", "HIGH": "red"}
            
            st.metric("Risk Score", f"{risk_score}/15")
            st.markdown(f"**Risk Level:** :{colors[risk_level]}[{risk_level}]")
            
            # Risk gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Risk Score"},
                gauge = {
                    'axis': {'range': [None, 15]},
                    'bar': {'color': colors[risk_level]},
                    'steps': [
                        {'range': [0, 4], 'color': "lightgreen"},
                        {'range': [4, 8], 'color': "yellow"},
                        {'range': [8, 15], 'color': "lightcoral"}
                    ]
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Contributing Risk Factors:**")
            if risk_factors:
                for factor in risk_factors:
                    st.write(f"• {factor}")
            else:
                st.write("• No significant risk factors identified")
            
            st.write("**Clinical Recommendations:**")
            if risk_level == "HIGH":
                st.error("• Immediate comprehensive evaluation needed")
                st.error("• Consider specialist referral")
                st.error("• Enhanced medication review required")
            elif risk_level == "MODERATE":
                st.warning("• Enhanced monitoring recommended")
                st.warning("• Regular follow-up appointments")
                st.warning("• Review medication list for optimization")
            else:
                st.success("• Routine preventive care appropriate")
                st.success("• Standard follow-up schedule")
                st.success("• Continue current management plan")
        
        # Evidence-based notes
        if evidence_notes:
            st.markdown("---")
            st.subheader("📚 Evidence-Based Risk Factors")
            with st.expander("Clinical Evidence & Guidelines", expanded=False):
                for note in evidence_notes:
                    st.write(f"• {note}")
                
                st.markdown("**References:**")
                st.write("• Beers Criteria for Potentially Inappropriate Medication Use")
                st.write("• Charlson Comorbidity Index")
                st.write("• Geriatric Medicine Clinical Guidelines")
                st.write("• STOPP/START Criteria for Medication Review")

def show_analytics(clinical_discovery, drug_reviews, medical_transcriptions):
    """Display analytics dashboard"""
    st.header("📊 Advanced Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Demographics", "Drug Effectiveness", "Clinical Patterns"])
    
    with tab1:
        st.subheader("Patient Demographics")
        
        if not clinical_discovery.empty:
            if 'sex' in clinical_discovery.columns and 'race' in clinical_discovery.columns:
                # Create crosstab
                crosstab = pd.crosstab(clinical_discovery['sex'], clinical_discovery['race'])
                fig = px.imshow(crosstab.values, 
                              x=crosstab.columns, 
                              y=crosstab.index,
                              title="Gender vs Race Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            if 'Event' in clinical_discovery.columns and 'sex' in clinical_discovery.columns:
                gender_outcomes = clinical_discovery.groupby('sex')['Event'].mean() * 100
                fig = px.bar(x=gender_outcomes.index, y=gender_outcomes.values,
                           title="Event Rate by Gender (%)")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Drug Effectiveness Analysis")
        
        if not drug_reviews.empty:
            # Check for actual column names in drug reviews data
            drug_columns = drug_reviews.columns.tolist()
            
            # Handle different possible column names
            condition_col = None
            rating_col = None
            review_col = None
            
            for col in drug_columns:
                if 'condition' in col.lower():
                    condition_col = col
                if 'rating' in col.lower():
                    rating_col = col
                if 'review' in col.lower():
                    review_col = col
            
            if condition_col and rating_col:
                # Top conditions by rating
                try:
                    condition_ratings = drug_reviews.groupby(condition_col)[rating_col].agg(['mean', 'count']).reset_index()
                    condition_ratings = condition_ratings[condition_ratings['count'] >= 5]
                    top_conditions = condition_ratings.sort_values('mean', ascending=False).head(10)
                    
                    fig = px.bar(top_conditions, x=condition_col, y='mean',
                               title="Top Conditions by Average Drug Rating",
                               labels={'mean': 'Average Rating'})
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not analyze condition ratings: {e}")
            
            # Sentiment vs Rating
            if rating_col and review_col:
                try:
                    sample_reviews = drug_reviews.head(500)
                    if not sample_reviews.empty:
                        sentiments = [analyze_sentiment(str(review)) for review in sample_reviews[review_col] if pd.notna(review)]
                        ratings = [rating for rating, review in zip(sample_reviews[rating_col], sample_reviews[review_col]) if pd.notna(review)]
                        
                        if len(sentiments) > 0:
                            sentiment_df = pd.DataFrame({
                                'sentiment': sentiments,
                                'rating': ratings[:len(sentiments)]
                            })
                            
                            fig = px.box(sentiment_df, x='sentiment', y='rating',
                                       title="Rating Distribution by Sentiment")
                            st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not analyze sentiment vs rating: {e}")
            
            # Show basic drug statistics if other analyses fail
            if rating_col:
                st.subheader("Drug Rating Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_rating = drug_reviews[rating_col].mean()
                    st.metric("Average Rating", f"{avg_rating:.1f}")
                
                with col2:
                    total_reviews = len(drug_reviews)
                    st.metric("Total Reviews", f"{total_reviews:,}")
                
                with col3:
                    high_rated = (drug_reviews[rating_col] >= 8).sum()
                    st.metric("High Rated (≥8)", f"{high_rated:,}")
                
                # Rating distribution
                fig = px.histogram(drug_reviews.head(1000), x=rating_col, 
                                 title="Rating Distribution (Sample of 1000)")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Clinical Patterns")
        
        if not medical_transcriptions.empty:
            # Check for medical specialty column
            specialty_col = None
            keywords_col = None
            
            for col in medical_transcriptions.columns:
                if 'specialty' in col.lower() or 'department' in col.lower():
                    specialty_col = col
                if 'keyword' in col.lower() or 'tag' in col.lower():
                    keywords_col = col
            
            if specialty_col and specialty_col in medical_transcriptions.columns:
                try:
                    specialty_counts = medical_transcriptions[specialty_col].value_counts().head(8)
                    
                    if len(specialty_counts) > 0:
                        fig = px.pie(values=specialty_counts.values, 
                                    names=specialty_counts.index,
                                    title="Medical Specialties Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No medical specialty data available")
                except Exception as e:
                    st.warning(f"Could not analyze medical specialties: {e}")
            
            # Keywords analysis with error handling
            if keywords_col and keywords_col in medical_transcriptions.columns:
                try:
                    all_keywords = []
                    for keywords in medical_transcriptions[keywords_col].dropna().head(100):
                        if isinstance(keywords, str) and keywords.strip():
                            # Handle different separators
                            if ',' in keywords:
                                all_keywords.extend([kw.strip() for kw in keywords.split(',')])
                            elif ';' in keywords:
                                all_keywords.extend([kw.strip() for kw in keywords.split(';')])
                            else:
                                all_keywords.append(keywords.strip())
                    
                    if all_keywords:
                        # Filter out very short keywords
                        all_keywords = [kw for kw in all_keywords if len(kw) > 2]
                        keyword_counts = Counter(all_keywords)
                        top_keywords = dict(keyword_counts.most_common(15))
                        
                        if top_keywords:
                            fig = px.bar(x=list(top_keywords.values()), 
                                       y=list(top_keywords.keys()),
                                       orientation='h',
                                       title="Top Medical Keywords")
                            fig.update_layout(yaxis=dict(autorange="reversed"))
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No significant keywords found")
                    else:
                        st.info("No keywords available for analysis")
                except Exception as e:
                    st.warning(f"Could not analyze keywords: {e}")
            
            # If no specialty or keywords columns, show basic statistics
            if not specialty_col and not keywords_col:
                st.info("📊 **Basic Medical Transcriptions Statistics**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Records", len(medical_transcriptions))
                
                with col2:
                    # Try to find any text column for word count
                    text_cols = [col for col in medical_transcriptions.columns if any(kw in col.lower() for kw in ['text', 'transcription', 'description', 'note'])]
                    if text_cols:
                        avg_length = medical_transcriptions[text_cols[0]].astype(str).str.len().mean()
                        st.metric("Avg Text Length", f"{avg_length:.0f}")
                
                with col3:
                    non_null_cols = medical_transcriptions.count().sum()
                    st.metric("Data Completeness", f"{(non_null_cols/(len(medical_transcriptions)*len(medical_transcriptions.columns))*100):.1f}%")

def show_team():
    """Display team member allocation and responsibilities"""
    st.header("👥 Team Member Allocation")
    st.markdown("---")
    
    # Team overview
    st.subheader("🎯 Project Team Overview")
    st.markdown("""
    Our multidisciplinary team brings together expertise in data science, clinical analysis, 
    software engineering, and healthcare visualization to deliver a comprehensive Clinical Decision Support System.
    """)
    
    # Team members
    col1, col2 = st.columns(2)
    
    with col1:
        # Anusha
        st.markdown("### 📊 **Anusha - Data Collection Specialist**")
        st.markdown("**⏱️ Time Allocation: 4 hours**")
        
        with st.expander("🔍 **Key Responsibilities**", expanded=True):
            st.markdown("""
            • Research and identify suitable clinical datasets  
            • Download MIMIC-IV sample and i2b2 datasets  
            • Web scrape medical terminology from reliable sources  
            • Generate synthetic clinical notes if needed  
            • Create comprehensive dataset inventory
            """)
        
        with st.expander("📦 **Deliverables**"):
            st.markdown("""
            • Clinical text dataset (5000+ records)  
            • Medical terminology database  
            • Drug interaction dataset  
            • Data source documentation
            """)
        
        st.markdown("---")
        
        # Pranab
        st.markdown("### 🔧 **Pranab - Data Preparation Engineer**")
        st.markdown("**⏱️ Time Allocation: 3 hours**")
        
        with st.expander("🔍 **Key Responsibilities**", expanded=True):
            st.markdown("""
            • Clean and standardize clinical text data  
            • Handle missing values and data quality issues  
            • Normalize medical terminology and abbreviations  
            • Remove PHI and ensure data privacy  
            • Create structured data from unstructured text
            """)
        
        with st.expander("📦 **Deliverables**"):
            st.markdown("""
            • Clean, preprocessed clinical dataset  
            • Data quality assessment report  
            • Medical abbreviation mapping dictionary  
            • Data preprocessing pipeline code
            """)
    
    with col2:
        # Sujay
        st.markdown("### 🏥 **Sujay - Clinical Data Analyst**")
        st.markdown("**⏱️ Time Allocation: 4 hours**")
        
        with st.expander("🔍 **Key Responsibilities**", expanded=True):
            st.markdown("""
            • Perform NLP analysis on clinical text  
            • Extract medical entities and relationships  
            • Conduct statistical analysis of clinical patterns  
            • Identify drug interactions and risk factors  
            • Analyze treatment outcomes and effectiveness
            """)
        
        with st.expander("📦 **Deliverables**"):
            st.markdown("""
            • Medical entity extraction results  
            • Statistical analysis of clinical patterns  
            • Drug interaction detection system  
            • Treatment effectiveness analysis report
            """)
        
        st.markdown("---")
        
        # Rakshit
        st.markdown("### 📊 **Rakshit - Visualization & Insights Lead**")
        st.markdown("**⏱️ Time Allocation: 5 hours**")
        
        with st.expander("🔍 **Key Responsibilities**", expanded=True):
            st.markdown("""
            • Create interactive clinical data visualizations  
            • Develop Streamlit dashboard for results  
            • Generate clinical insights and recommendations  
            • Prepare final presentation and documentation  
            • Conduct project reflection and future planning
            """)
        
        with st.expander("📦 **Deliverables**"):
            st.markdown("""
            • Interactive clinical dashboard  
            • Comprehensive visualization suite  
            • Clinical recommendations report  
            • Final project presentation  
            • Project reflection document
            """)
    
    # Project summary
    st.markdown("---")
    st.subheader("📈 **Project Timeline & Coordination**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Team Hours", "16 hours")
    with col2:
        st.metric("Team Members", "4 people")
    with col3:
        st.metric("Project Phases", "4 phases")
    with col4:
        st.metric("Deliverables", "15 items")
    
    # Team collaboration
    st.markdown("### 🤝 **Team Collaboration Strategy**")
    st.markdown("""
    **Phase 1:** Data Collection & Preparation ( Anusha → Pranab)  
    **Phase 2:** Clinical Analysis  (Sujay)  
    **Phase 3:** Visualization & Dashboard Development (Rakshit)  
    **Phase 4:** Integration, Testing & Documentation (All team members)
    """)
    
    # Success metrics
    st.markdown("### 🎯 **Success Metrics**")
    success_metrics = {
        "Data Quality": "✅ 95%+ data completeness achieved",
        # "NLP Accuracy": "✅ Medical entity extraction >85% accuracy",
        "User Experience": "✅ Intuitive dashboard with <3 second load times",
        "Clinical Value": "✅ Actionable insights for healthcare professionals",
        "Documentation": "✅ Comprehensive project documentation"
    }
    
    for metric, status in success_metrics.items():
        st.markdown(f"**{metric}:** {status}")

if __name__ == "__main__":
    main()
