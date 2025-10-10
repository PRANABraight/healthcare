# src/visualizations.py

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any

class DashboardVisuals:
    """
    An encapsulated, top-tier module for creating all dashboard visualizations.

    This class is responsible for translating dataframes into beautiful,
    interactive Plotly figures. It is completely decoupled from the data loading
    and analytics layers.
    """

    def __init__(self, theme: Dict[str, Any] = None):
        """
        Initializes the visualization module with a consistent theme.

        Args:
            theme (Dict[str, Any], optional): A dictionary defining colors, fonts, etc.
                                              If None, a default theme is used.
        """
        if theme is None:
            # A default professional theme. Centralizing this makes branding easy.
            self.theme = {
                'primary_color': '#1f77b4',  # Muted Blue
                'secondary_color': '#ff7f0e', # Safety Orange
                'tertiary_color': '#2ca02c',   # Cooked Asparagus Green
                'background_color': 'rgba(0,0,0,0)', # Transparent
                'grid_color': '#e5e5e5',
                'font_family': "Arial",
                'font_color': "#333333"
            }
        else:
            self.theme = theme

    def _apply_theme(self, fig: go.Figure) -> go.Figure:
        """
        Private method to apply the consistent theme to any Plotly figure.
        """
        fig.update_layout(
            font=dict(family=self.theme['font_family'], color=self.theme['font_color']),
            plot_bgcolor=self.theme['background_color'],
            paper_bgcolor=self.theme['background_color'],
            xaxis=dict(gridcolor=self.theme['grid_color']),
            yaxis=dict(gridcolor=self.theme['grid_color']),
            margin=dict(l=40, r=20, t=40, b=30)
        )
        return fig

    def plot_patient_vitals_timeseries(self, patient_data: pd.DataFrame) -> go.Figure:
        """
        Creates an interactive time-series chart of a patient's vital signs.
        
        This is a great example of a function-per-chart design.

        Args:
            patient_data (pd.DataFrame): DataFrame containing vitals for a single patient,
                                         sorted by date.

        Returns:
            go.Figure: A Plotly figure object ready to be displayed.
        """
        # Assuming a 'date' column exists for time-series plotting
        if 'date' not in patient_data.columns:
             # Create a dummy date range if not present, for demonstration
             patient_data['date'] = pd.to_datetime(pd.date_range(start='2023-01-01', periods=len(patient_data)))

        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                            subplot_titles=("Blood Pressure", "Heart Rate", "Respiratory Rate"))

        # Systolic BP
        fig.add_trace(go.Scatter(x=patient_data['date'], y=patient_data['blood_pressure_(systolic)'],
                                 mode='lines+markers', name='Systolic',
                                 line=dict(color=self.theme['primary_color'])), row=1, col=1)
        # Diastolic BP
        fig.add_trace(go.Scatter(x=patient_data['date'], y=patient_data['blood_pressure_(diastolic)'],
                                 mode='lines+markers', name='Diastolic',
                                 line=dict(color=self.theme['secondary_color'])), row=1, col=1)

        # Heart Rate
        fig.add_trace(go.Scatter(x=patient_data['date'], y=patient_data['heart_rate_(bpm)'],
                                 mode='lines+markers', name='Heart Rate',
                                 line=dict(color=self.theme['tertiary_color'])), row=2, col=1)

        # Respiratory Rate
        fig.add_trace(go.Scatter(x=patient_data['date'], y=patient_data['respiratory_rate_(breaths/min)'],
                                 mode='lines+markers', name='Resp. Rate',
                                 line=dict(color=self.theme['primary_color'], dash='dash')), row=3, col=1)

        fig.update_layout(height=500, title_text="Patient Vitals Over Time", showlegend=False)
        return self._apply_theme(fig)

    def plot_demographics_distribution(self, cohort_df: pd.DataFrame) -> go.Figure:
        """
        Creates a bar chart showing the distribution of patients by age group.

        Args:
            cohort_df (pd.DataFrame): DataFrame for the entire patient cohort.

        Returns:
            go.Figure: A Plotly figure object.
        """
        age_group_counts = cohort_df['age_group'].value_counts().sort_index()
        fig = px.bar(
            x=age_group_counts.index,
            y=age_group_counts.values,
            labels={'x': 'Age Group', 'y': 'Number of Patients'},
            title='Patient Distribution by Age Group'
        )
        fig.update_traces(marker_color=self.theme['primary_color'])
        return self._apply_theme(fig)

    def create_risk_gauge(self, score: float, level: str, max_score: int = 5) -> go.Figure:
        """
        Creates a visually impressive "gauge" chart for displaying risk scores.
        
        This kind of advanced visualization is a great way to impress.

        Args:
            score (float): The numerical risk score from the analytics engine.
            level (str): The qualitative risk level (e.g., 'Low', 'Moderate', 'High').
            max_score (int): The maximum possible score for the gauge's scale.

        Returns:
            go.Figure: A Plotly figure object.
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            title={'text': f"Risk Level: {level}"},
            delta={'reference': max_score / 2}, # Compare against the midpoint
            gauge={
                'axis': {'range': [0, max_score], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': self.theme['primary_color']},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, max_score * 0.4], 'color': 'lightgreen'},
                    {'range': [max_score * 0.4, max_score * 0.7], 'color': 'yellow'},
                    {'range': [max_score * 0.7, max_score], 'color': 'red'}],
            }))
        
        fig.update_layout(height=250, title_text="Rule-Based Risk Score")
        return self._apply_theme(fig)
    