# src/analytics_engine.py

import pandas as pd
import joblib
import logging
from typing import Dict, Any, List, Tuple

# Configure a logger for the analytics engine module
logger = logging.getLogger(__name__)

class AnalyticsEngine:
    """
    A top-tier, decoupled engine for performing all clinical analytics.

    This engine is stateless and operates solely on the data it receives,
    making it predictable, testable, and independent of the UI or data sources.
    It encapsulates the core business logic and data science models of the application.
    """

    def __init__(self, model_path: str = 'C:/Users/prana/OneDrive/Desktop/4trimester/healthcare/EDA/final_patient_outcome_model.pkl.pkl'):
        """
        Initializes the Analytics Engine.

        Args:
            model_path (str): The file path to the pre-trained machine learning model.
        """
        self.model = self._load_model(model_path)
        if self.model:
            logger.info("Analytics Engine initialized with a pre-trained prediction model.")
        else:
            logger.warning("Analytics Engine initialized WITHOUT a prediction model. Predictive features will be disabled.")

    def _load_model(self, model_path: str) -> Any:
        """
        Private method to safely load a pre-trained model from disk.
        
        Using a dedicated method for this encapsulates the model loading logic.
        """
        try:
            # joblib is standard for scikit-learn models
            return joblib.load(model_path)
        except FileNotFoundError:
            logger.error(f"Prediction model not found at path: {model_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading prediction model: {e}")
            return None

    def calculate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        📚 STATISTICAL MODULE: Computes key descriptive statistics for a cohort.

        This demonstrates core data analysis skills.

        Args:
            df (pd.DataFrame): The clinical dataset.

        Returns:
            Dict[str, Any]: A dictionary of calculated summary statistics.
        """
        logger.info("Calculating summary statistics for the provided dataset.")
        if df.empty:
            return {}
        
        return {
            "total_patients": len(df),
            "average_age": round(df['age'].mean(), 1),
            "gender_distribution": df['gender'].value_counts(normalize=True).to_dict(),
            "average_systolic_bp": round(df['blood_pressure_(systolic)'].mean(), 2),
        }

    def perform_risk_stratification(self, patient_data: pd.DataFrame) -> Tuple[str, float]:
        """
        ⚖️ BUSINESS RULES MODULE: Stratifies patient risk based on a defined rule-set.

        This function is a perfect example of encapsulating domain-specific business logic.
        It is easily testable and can be updated without affecting other parts of the app.

        Args:
            patient_data (pd.Series): A single row DataFrame representing one patient.

        Returns:
            Tuple[str, float]: A tuple containing the risk level ('Low', 'Moderate', 'High')
                               and a numerical risk score.
        """
        logger.info(f"Performing rule-based risk stratification for patient.")
        if patient_data.empty:
            return "Unknown", 0.0

        patient = patient_data.iloc[0]
        score = 0
        
        # Rule 1: Age-based risk
        if patient['age'] > 75:
            score += 2
        elif patient['age'] > 60:
            score += 1

        # Rule 2: Blood Pressure-based risk
        if patient['blood_pressure_(systolic)'] > 160:
            score += 2
        elif patient['blood_pressure_(systolic)'] > 140:
            score += 1
            
        # Determine risk level based on the final score
        if score >= 3:
            level = "High"
        elif score >= 1:
            level = "Moderate"
        else:
            level = "Low"
            
        return level, float(score)

    def predict_clinical_risk(self, patient_data: pd.DataFrame) -> Tuple[str, float]:
        """
        🤖 MACHINE LEARNING INFERENCE MODULE: Uses a pre-trained model for prediction.

        This showcases the ability to productionize data science models.
        It handles data preparation for the model and returns a clean, usable output.

        Args:
            patient_data (pd.DataFrame): A single row DataFrame for one patient.

        Returns:
            Tuple[str, float]: A tuple containing the predicted outcome ('High Risk' or 'Low Risk')
                               and the model's confidence probability.
        """
        if self.model is None:
            logger.warning("Prediction model is not loaded. Cannot perform prediction.")
            return "Not Available", 0.0

        if patient_data.empty:
            return "No Data", 0.0

        logger.info(f"Making prediction for patient.")
        
        # Prepare the feature vector for the model (must match training)
        # This is a critical step in productionizing models.
        features = ['age', 'blood_pressure_(systolic)', 'blood_pressure_(diastolic)', 'heart_rate_(bpm)']
        
        # Ensure the feature order is the same as during model training
        patient_features = patient_data[features].copy()

        # Basic imputation: handle missing values before prediction
        patient_features.fillna(patient_features.mean(), inplace=True)

        try:
            prediction = self.model.predict(patient_features)[0]
            probability = self.model.predict_proba(patient_features)[0][1] # Probability of class '1' (High Risk)
            
            outcome = "High Risk" if prediction == 1 else "Low Risk"
            logger.info(f"Prediction successful: Outcome='{outcome}', Confidence={probability:.2f}")
            
            return outcome, round(probability, 2)
        except Exception as e:
            logger.error(f"An error occurred during model prediction: {e}")
            return "Error", 0.0

    def analyze_drug_interactions(self, selected_drugs: List[str], interactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        💊 Performs a SQL-like query to find potential drug interactions.
        
        Args:
            selected_drugs (List[str]): A list of drug names to check.
            interactions_df (pd.DataFrame): The dataframe of known interactions.

        Returns:
            pd.DataFrame: A filtered DataFrame containing only relevant interactions.
        """
        if not selected_drugs or interactions_df.empty:
            return pd.DataFrame()
            
        logger.info(f"Analyzing interactions for drugs: {selected_drugs}")
        
        # This powerful boolean indexing is highly efficient and showcases strong pandas skills.
        # It's equivalent to a SQL `WHERE drug1 IN (...) OR drug2 IN (...)`
        mask = interactions_df['drug1_name'].isin(selected_drugs) | \
               interactions_df['drug2_name'].isin(selected_drugs)
               
        return interactions_df[mask]