# Healthcare — Clinical Decision Support (compact)

Brief
-----
This repository contains a compact Clinical Decision Support project: a Streamlit dashboard (`app.py` / `app_final.py`), a small ETL/analytics pipeline (`main.py` → `src.controllers.main_controller.MainController`), model and analytics code under `src/models/`, and example data under `data/`.

Quick facts
-----------
- Python: 3.9+
- Primary app: Streamlit (`app.py`, `app_final.py`)
- CLI/ETL entrypoint: `main.py`
<!-- - Tests: `tests/test_analytics_engine.py` -->

Repository layout
-----------------
- `app.py`, `app_final.py` — Streamlit front-end(s)
- `main.py` — CLI entrypoint to run the ETL + analytics controller
- `src/controllers/` — controller code
- `src/models/` — data pipeline, analytics engine, visualizations, and a saved model (`final_patient_outcome_model.pkl`)
- `data/` — raw and processed CSVs and small images used by the app


Important data files
--------------------
- `data/Clinical Data_Discovery_Cohort.csv`
- `data/Clinical_Data_Validation_Cohort.csv`
- `data/drugsComTrain_raw.csv`, `data/drugsComTest_raw.csv`
- `data/db_drug_interactions.csv`
- `data/processed/clinical_data_clean.csv` (processed dataset used by analytics)

How to run
----------

1) Create and activate a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2) Run the Streamlit app:

```bash
streamlit run app.py
# or
streamlit run app_final.py
```

3) Run the ETL + analytics pipeline (non-interactive):

```bash
python main.py
```

Notes & assumptions
-------------------
- `main.py` currently contains absolute Windows paths. Change these to relative paths or environment-based configs for portability.
- Keep PHI out of the repository and test data.


License
-------
MIT

