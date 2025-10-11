# models/analytics_engine.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
import re
from difflib import get_close_matches

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


class AnalyticsEngine:
    """
    A clinical analytics engine for generating summaries, statistics,
    and visualizations from cleaned clinical datasets.
    """

    def __init__(self, cleaned_data_path: str, output_dir: str = None):
        self.data_path = cleaned_data_path
        self.output_dir = output_dir
        self.df = None
        self.load_data()
        self.standardize_columns()
        self.convert_numeric_columns()
    def load_data(self):
        """Load cleaned clinical data."""
        try:
            logging.info(f"Loading cleaned data from {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            logging.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def standardize_columns(self):
        """Standardize and normalize column names for consistent access."""
        cleaned_cols = []
        for col in self.df.columns:
            new_col = (
                col.strip()
                .lower()
                .replace(" ", "_")
                .replace(".", "")
                .replace("-", "_")
            )
            new_col = re.sub(r"[\(\)\[\]\{\}]+", "", new_col)
            cleaned_cols.append(new_col)
        self.df.columns = cleaned_cols

    def find_column(self, target_name):
        """Try to find a column even if name is slightly different."""
        available_cols = list(self.df.columns)
        if target_name in available_cols:
            return target_name
        matches = get_close_matches(target_name, available_cols, n=1, cutoff=0.6)
        if matches:
            found = matches[0]
            logging.warning(f"Column name '{target_name}' not found; using '{found}' instead.")
            return found
        logging.warning(f"Column '{target_name}' not found in dataset.")
        return None

    def convert_numeric_columns(self):
        """Convert numeric-like columns to numeric safely."""
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    self.df[col] = pd.to_numeric(self.df[col], errors='ignore')
                except Exception:
                    pass

    def summary_statistics(self):
        """Compute descriptive statistics."""
        logging.info("Generating summary statistics...")
        summary = self.df.describe(include='all')
        print("\n=== Summary Statistics ===")
        print(summary)
        return summary

    def survival_statistics(self):
        """Compute survival statistics by groups."""
        survival_col = self.find_column('event_death_1_alive_0')
        time_col = self.find_column('survival_time_days')

        if not survival_col or not time_col:
            logging.warning("Survival-related columns not found.")
            return None

        df = self.df.dropna(subset=[survival_col, time_col])
        total_patients = len(df)
        deaths = df[survival_col].sum()
        alive = total_patients - deaths
        median_survival = df[time_col].median()

        print("\n=== Survival Statistics ===")
        print(f"Total patients: {total_patients}")
        print(f"Deaths: {deaths}, Alive: {alive}")
        print(f"Median survival (days): {median_survival}")

        return {'total': total_patients, 'deaths': deaths, 'alive': alive, 'median_survival': median_survival}

    def plot_histogram(self, column, bins=10, save_path=None):
        """Plot histogram for a numeric column."""
        col = self.find_column(column)
        if not col:
            return

        plt.figure(figsize=(8, 5))
        sns.histplot(self.df[col].dropna(), kde=True, bins=bins)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            logging.info(f"Saved histogram to {save_path}")
        else:
            plt.show()
        plt.close()

    def plot_boxplot(self, numeric_col, group_col, save_path=None):
        """Plot boxplot for a numeric column grouped by a categorical column."""
        num_col = self.find_column(numeric_col)
        grp_col = self.find_column(group_col)
        if not num_col or not grp_col:
            return

        plt.figure(figsize=(8, 5))
        sns.boxplot(x=self.df[grp_col], y=self.df[num_col])
        plt.title(f"{num_col} by {grp_col}")
        plt.xlabel(grp_col)
        plt.ylabel(num_col)
        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            logging.info(f"Saved boxplot to {save_path}")
        else:
            plt.show()
        plt.close()

    def correlation_matrix(self, save_path=None):
        """Compute and plot correlation matrix."""
        numeric_cols = self.df.select_dtypes(include='number').columns
        if len(numeric_cols) < 2:
            logging.warning("Not enough numeric columns for correlation matrix.")
            return

        corr = self.df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Correlation Matrix")
        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            logging.info(f"Saved correlation matrix to {save_path}")
        else:
            plt.show()
        plt.close()

        return corr

    def run_all(self):
        # """Run a full analytics pipeline with summary, survival, and plots."""
        self.summary_statistics()
        self.survival_statistics()

        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)
            plots_dir = os.path.join(self.output_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)

            self.plot_histogram('age', save_path=os.path.join(plots_dir, 'age_hist.png'))
            self.plot_histogram('tumor_size_(cm)', save_path=os.path.join(plots_dir, 'tumor_size_hist.png'))
            self.plot_boxplot('survival_time_days', 'grade', save_path=os.path.join(plots_dir, 'survival_by_grade.png'))
            self.correlation_matrix(save_path=os.path.join(plots_dir, 'correlation_matrix.png'))
        else:
            self.plot_histogram('age')
            self.plot_histogram('tumor_size_(cm)')
            self.plot_boxplot('survival_time_days', 'grade')
            self.correlation_matrix()
