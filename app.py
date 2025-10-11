# app.py

import streamlit as st
import pandas as pd
import logging

# Import the professional modules from the 'models' directory
from models.config import PIPELINE_CONFIG
from models.data_pipeline import DataPipeline
from models.analytics_engine import AnalyticsEngine
from models.visualizations import DashboardVisuals

# Configure the page for a professional look and feel
st.set_page_config(
    page_title="Enterprise Clinical Analytics Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up logging to monitor application health
logger = logging.getLogger(__name__)


# --- 1. DATA LOADING & CACHING ---
@st.cache_data(show_spinner="Running advanced data pipeline...")
def load_data_via_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Orchestrates the execution of the full ETL pipeline for all required datasets.
    Uses Streamlit's caching to prevent re-running the pipeline on every interaction.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the clean clinical
                                           and drug interaction dataframes.
    """
    try:
        clinical_df = DataPipeline.run_pipeline(PIPELINE_CONFIG, 'clinical_data')
        interactions_df = DataPipeline.run_pipeline(PIPELINE_CONFIG, 'drug_interactions')
        logger.info("Data pipeline executed and data loaded successfully.")
        return clinical_df, interactions_df
    except Exception as e:
        logger.critical(f"A critical error occurred during the data pipeline execution: {e}")
        st.error(f"Fatal Error in Data Pipeline: {e}. Application cannot proceed.")
        # Return empty dataframes to prevent the app from crashing further down
        return pd.DataFrame(), pd.DataFrame()


# --- 2. INITIALIZATION OF CORE COMPONENTS ---
def initialize_app_components():
    """
    Initializes and returns instances of the core application components.
    This helps manage the state and dependencies of our modules.
    """
    analytics_engine = AnalyticsEngine(model_path='models/risk_prediction_model.pkl')
    visuals = DashboardVisuals()
    return analytics_engine, visuals


# --- 3. MAIN APPLICATION SCRIPT ---
def main():
    """
    The main function that orchestrates the entire Streamlit application.
    """
    st.title("🏥 Enterprise Clinical Analytics Platform")
    st.markdown("A professional-grade software solution for data-driven clinical decision support.")
    st.markdown("---")

    # Initialize the core engine and visualizer
    analytics_engine, visuals = initialize_app_components()

    # Execute the data pipeline and load the data
    clinical_df, interactions_df = load_data_via_pipeline()

    # Halt execution if the data pipeline failed
    if clinical_df.empty or interactions_df.empty:
        st.warning("Data could not be loaded. Please check the logs and ensure data files are present.")
        return

    # --- UI Layout & User Interaction ---
    st.sidebar.header("👨‍⚕️ Patient Selection")
    patient_id = st.sidebar.selectbox(
        "Select a Patient ID to analyze:",
        clinical_df['patient_id'].unique()
    )
    # Filter data for the selected patient
    patient_data = clinical_df[clinical_df['patient_id'] == patient_id]

    st.header(f"📊 Dashboard for Patient: {patient_id}")
    st.markdown(f"Displaying analytics for a **{patient_data.iloc[0]['age']}-year-old {patient_data.iloc[0]['gender'].lower()}** from the **{patient_data.iloc[0]['age_group']}** cohort.")

    # --- Orchestration: Engine -> Visuals -> UI ---
    # Create a 3-column layout for key metrics
    col1, col2, col3 = st.columns(3)

    # 1. Get insights from the Analytics Engine
    rule_risk_level, rule_risk_score = analytics_engine.perform_risk_stratification(patient_data)
    ml_risk_level, ml_confidence = analytics_engine.predict_clinical_risk(patient_data)
    cohort_stats = analytics_engine.calculate_summary_statistics(clinical_df)

    # 2. Display key metrics using the insights
    with col1:
        st.metric(
            label="Rule-Based Risk Level",
            value=rule_risk_level,
            help=f"Calculated score: {rule_risk_score}"
        )
    with col2:
        st.metric(
            label="Predicted Risk (ML models)",
            value=ml_risk_level,
            delta=f"Confidence: {ml_confidence:.0%}",
            delta_color="off"
        )
    with col3:
         st.metric(
            label="Total Patients in Cohort",
            value=cohort_stats.get('total_patients', 'N/A')
         )

    st.markdown("---")

    # --- Detailed Visualizations ---
    dash_col1, dash_col2 = st.columns([0.6, 0.4]) # Give more space to the time-series

    with dash_col1:
        st.subheader("Vital Signs Timeline")
        # 3. Create chart object from the Visuals module
        vitals_fig = visuals.plot_patient_vitals_timeseries(patient_data)
        # 4. Render the chart in the UI
        st.plotly_chart(vitals_fig, use_container_width=True)

    with dash_col2:
        st.subheader("Risk Gauges")
        gauge_fig = visuals.create_risk_gauge(rule_risk_score, rule_risk_level)
        st.plotly_chart(gauge_fig, use_container_width=True)

        st.subheader("Cohort Demographics")
        demographics_fig = visuals.plot_demographics_distribution(clinical_df)
        st.plotly_chart(demographics_fig, use_container_width=True)


if __name__ == "__main__":
    main()