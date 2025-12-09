This usually happens because of spacing alignment or missing "code block" formatting in Markdown.

Here is the raw source code for the entire README.md.

Copy the code block below exactly and paste it into your README.md file. It uses a text code block to ensure the directory tree lines stay perfectly aligned on GitHub.

code
Markdown
download
content_copy
expand_less
# 🛡️ Insurance Risk Rating & Predictive Modeling
### *AlphaCare Insurance Solutions*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-9cf)
![Status](https://img.shields.io/badge/Status-Interim%20Submission-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**Repository:** [https://github.com/zemicahel/week3](https://github.com/zemicahel/week3)  
**Author:** Zemicahel Abraham  
**Date:** December 2025

---

## 📖 Executive Summary

This project focuses on building a robust data pipeline and predictive models for **AlphaCare Insurance Solutions**. The primary goal is to transition from traditional linear pricing models to data-driven, machine learning-based risk scoring.

This repository represents a complete end-to-end workflow including **Exploratory Data Analysis (EDA)**, **Statistical Hypothesis Testing**, and **Predictive Modeling**. Crucially, it employs **Data Version Control (DVC)** to ensure auditability and reproducibility, complying with regulated financial environment standards.

---

## 🎯 Business Objective

Insurance companies face the challenge of pricing policies accurately while minimizing losses from claims. This project seeks to answer:

1.  **Risk Segmentation:** Which customer segments or regions represent higher claim risk?
2.  **Profitability:** Which vehicle types contribute most to losses versus profits?
3.  **Prediction:** Can we accurately predict the probability (frequency) and severity (amount) of claims?
4.  **Actionability:** What data-driven insights can inform marketing and pricing strategies?

---

## 🛠️ Data Engineering & DVC Setup

To comply with financial auditing standards, this project uses **DVC (Data Version Control)**. This ensures that every model result can be traced back to the exact version of the data used to train it, separating code versioning (Git) from data versioning (DVC).

### **How it works**
*   **Git:** Tracks the code and the `.dvc` metadata files (pointers).
*   **DVC:** Tracks the large dataset (`MachineLearningRating_v3.txt`).
*   **Local Remote:** A local directory serves as a simulated secure storage (e.g., S3 bucket) for the pipeline.

### **Data Versioning Capabilities**
*   **Version 1:** Raw data ingestion.
*   **Version 2:** Processed/Imputed data updates.
*   **Rollback:** The system allows for instant rollback to previous data states using `dvc checkout`.

---

## 📂 Repository Structure

```text
insurance_analysis/
│
├── .dvc/                       # DVC configuration files
├── .github/workflows           # CI/CD pipelines
│
├── data/                       # Raw and processed data (tracked by DVC)
│   ├── .gitignore              # Ignores large data files
│   └── MachineLearningRating_v3.txt.dvc  # DVC pointer file
│
├── logs/                       # System and Analysis logs
│
├── notebooks/                  # Jupyter Notebooks for interactive analysis
│   ├── 01_eda_analysis.ipynb
│   ├── 02_hypothesis_tests.ipynb      
│   └── 03_predictive_modeling.ipynb 
│
├── plots/                      # Generated plots for reports
│   ├── profitability_landscape.png
│   └── risk_heatmap.png
│
├── scripts/                    # Modular Python scripts
│   ├── __init__.py
│   ├── loader.py               # Data ingestion
│   ├── cleaner.py              # Preprocessing & typing
│   ├── eda_stats.py            # Statistical calculations
│   ├── visualizer.py           # Plotting logic
│   ├── feature_engineering.py  # Feature creation & encoding
│   ├── modeling.py             # Regression & Classification models
│   └── logger.py               # Logger setup
│
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
📊 Key Findings (EDA & Statistics)

Our analysis of the historical policy dataset revealed critical insights into the portfolio's risk profile:

1. Zero-Inflated Claims

Over 95% of policies have zero claims. This extreme skewness indicates that standard linear regression is unsuitable. The modeling strategy shifted to Two-Stage models (Classification for occurrence, Regression for severity) or Tweedie loss functions.

2. Geographic Risk

While major metropolitan provinces (Gauteng, Western Cape) generate the most premiums, specific zip-code clusters exhibit disproportionately high claim frequencies, warranting geographic risk loading.

3. Profitability Landscape

A scatter analysis of TotalPremium vs. TotalClaims identified:

Underpriced Risks: Specific vehicle makes with high claim averages but low relative premiums.

Profit Drivers: Segments with consistent premiums and negligible loss ratios.

4. Hypothesis Testing Results

Risk by Province: Statistically significant differences in risk profiles exist across provinces.

Gender: No statistically significant difference in risk was found between genders for this dataset.

Zip Codes: Specific postal codes show statistically significant higher margins (profitability).

🤖 Predictive Modeling

The project implements a comprehensive modeling approach:

Algorithms

Classification (Claim Occurrence): Random Forest Classifier, XGBoost.

Regression (Claim Severity): Linear Regression, Random Forest Regressor, Gradient Boosting.

Model Explainability

SHAP (SHapley Additive exPlanations): Used to interpret the "Black Box" models, identifying that features like SumInsured, VehicleType, and Province are the strongest predictors of claim severity.

🚀 Getting Started
1. Clone the Repository
code
Bash
download
content_copy
expand_less
git clone https://github.com/zemicahel/week3.git
cd week3
2. Set up Virtual Environment
code
Bash
download
content_copy
expand_less
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
3. Initialize DVC

If you are running this locally and want to simulate the data pipeline:

code
Bash
download
content_copy
expand_less
# Initialize DVC
dvc init

# Setup local remote storage (simulating S3)
mkdir /tmp/dvc_storage
dvc remote add -d localstorage /tmp/dvc_storage

# Pull data (if configured) or Add data
dvc add data/MachineLearningRating_v3.txt
dvc push
4. Run the Analysis

You can run the full pipeline via the main script or explore interactively via notebooks:

code
Bash
download
content_copy
expand_less
# Run the main analysis script
python scripts/main_analysis.py

# OR open Jupyter
jupyter notebook notebooks/01_eda_analysis.ipynb
📈 Visualizations Included

The analysis generates specific insights found in the plots/ folder:

Profitability Landscape: Scatter plot of Premium vs. Claims by vehicle make.

Correlation Heatmap: Relationships between numerical features.

Outlier Boxplots: Visualizing extreme claim events.

SHAP Summary Plot: Feature importance ranking for the predictive models.

Monthly Loss Ratio: Time-series trend of profitability.

🔮 Limitations & Future Work

Data Imbalance: The high number of zero-claim policies requires advanced sampling techniques (SMOTE) or specialized loss functions.

External Factors: Weather, traffic data, and inflation are not currently included but would enhance prediction.

Future Scope:

Deploy model via REST API / Docker.

Integrate real-time dashboarding (Streamlit/Dash).

Automate hyperparameter tuning using MLflow.

🤝 Acknowledgements

ACIS Insurance for the dataset.

10 Academy for the project scope and guidance.

DVC.org for data versioning tools.

code
Code
download
content_copy
expand_less