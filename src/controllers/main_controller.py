import logging
from src.models.data_pipeline import DataPipeline
from src.models.analytics_engine import AnalyticsEngine

class MainController:
    def __init__(self, pipeline_config, cleaned_path, analytics_dir):
        self.cleaned_path = cleaned_path
        self.analytics_dir = analytics_dir
        self.pipeline_config = pipeline_config

        # Initialize pipeline with required parameters
        self.pipeline = DataPipeline(
            pipeline_config["input_path"],
            pipeline_config["file_type"],
            pipeline_config["output_path"]
        )

    def run_etl(self):
        try:
            logging.info("===== Starting ETL Process =====")
            self.pipeline.run()
            logging.info("ETL process completed successfully.")
        except Exception as e:
            logging.error(f"ETL process failed: {e}")

    def run_analytics(self):
        try:
            logging.info("===== Starting Analytics Process =====")
            analytics_engine = AnalyticsEngine(self.cleaned_path, self.analytics_dir)
            analytics_engine.run_all()
            logging.info("Analytics process completed successfully.")
        except Exception as e:
            logging.error(f"Analytics process failed: {e}")
