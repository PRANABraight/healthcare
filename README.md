# Clinical Decision Support System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

An interactive web application designed to assist healthcare professionals by providing data-driven insights for clinical decision-making.

---

### ⚠️ Clinical Disclaimer
This application is a decision support tool designed to assist healthcare professionals. It is **NOT** a substitute for clinical judgment, professional medical advice, diagnosis, or treatment. All clinical decisions should be made by qualified healthcare providers based on individual patient assessment and established clinical guidelines.

---

## 📖 Table of Contents
- [About The Project](#about-the-project)
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [Built With](#-built-with)
- [Data Sources](#-data-sources)
- [Getting Started](#-getting-started)
- [The Team](#-the-team)

## 🎯 About The Project

Healthcare professionals are often faced with vast amounts of patient data from disparate sources. This project aims to address this challenge by providing a unified platform that simplifies complex data, identifies potential risks, and extracts meaningful information from unstructured text. It serves as a supplementary tool to support clinicians in providing safer and more personalized patient care.

## ✨ Key Features

* **📊 Interactive Analytics Dashboard:** An overview of key healthcare metrics, including patient demographics, clinical outcomes, and drug review statistics.
* **✍️ Clinical Text Analysis:** Utilizes NLP to perform word frequency analysis on medical transcriptions to identify key terms.
* **💊 Drug Interaction Checker:** A tool to check for known interactions between multiple drugs from a database of over 191,000 interactions.
* **🩺 Patient Risk Assessment:** A predictive model that calculates a patient's risk score based on demographic, clinical, and lifestyle factors, providing clinical recommendations.
* **📈 Advanced Analytics:** Deeper analysis into drug effectiveness, sentiment analysis of reviews, and clinical patterns across different patient cohorts.

## 📸 Screenshots

| Dashboard Overview | Risk Assessment | Drug Interaction Checker |
| :---: | :---: | :---: |
| ![Dashboard](<INSERT_PATH_TO_DASHBOARD_IMAGE.png>) | ![Risk Assessment](<INSERT_PATH_TO_RISK_ASSESSMENT_IMAGE.png>) | ![Drug Interactions](<INSERT_PATH_TO_DRUG_INTERACTION_IMAGE.png>) |

*(Note: Replace the placeholder paths with actual paths to your screenshots.)*

## 🛠️ Built With

This project was built using the following technologies:

* [**Streamlit**](https://streamlit.io/): For the core web application framework and UI.
* [**Python**](https://www.python.org/): For all backend logic and data processing.
* [**Pandas**](https://pandas.pydata.org/): For data manipulation and analysis.
* [**Scikit-learn**](https://scikit-learn.org/): For machine learning models (e.g., Risk Assessment).
* [**NLTK / spaCy**](https://www.nltk.org/): For Natural Language Processing tasks.
* [**Plotly / Matplotlib**](https://plotly.com/): For creating data visualizations.

## 🗂️ Data Sources

The application is powered by several distinct datasets, sourced from well-known clinical data repositories and web scraping:
* **MIMIC-IV and i2b2:** For clinical patient data.
* **DrugBank / RxNorm (Inferred):** For the drug interaction database.
* **Public Drug Review Datasets:** For patient reviews and sentiment analysis.

A key part of the data preparation process involved the removal of all Protected Health Information (PHI) to ensure patient privacy.

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.9 or higher
* `pip` package manager

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your_username/your_project_repository.git](https://github.com/your_username/your_project_repository.git)
    cd your_project_repository
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```sh
    streamlit run app.py
    ```
The application should now be running and accessible in your web browser.

## 👥 The Team

This project was a collaborative effort by a multidisciplinary team.

* **Anusha** - *Data Collection Specialist*
    * Researched and identified suitable clinical datasets (MIMIC-IV, i2b2).

* **Pranab** - *Data Preparation Engineer*
    * Cleaned, standardized, and normalized data; ensured patient privacy by removing PHI.

* **Sujay** - *Clinical Data Analyst*
    * Performed NLP, statistical analysis, and identified clinical patterns and risk factors.

* **Rakshit** - *Visualization & Insights Lead*
    * Developed the Streamlit dashboard, created visualizations, and generated insights.