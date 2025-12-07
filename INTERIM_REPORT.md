Interim Report: Machine Learning for Insurance Risk Rating
Phase 1: Data Engineering Pipeline & Exploratory Analysis
Date: 07 December 2025
Prepared By: Zemicahel Abraham
Repository: GitHub
1. Executive Summary
This interim report outlines the progress achieved during the initial phase of the Insurance Risk Rating project. The primary objective of this project is to develop a machine learning solution capable of predicting insurance claim frequency and severity, thereby enabling more accurate, risk-adjusted premium pricing.
During this phase, the project team focused on two critical foundational pillars: Data Governance and Exploratory Data Analysis (EDA).
Key Accomplishments:
Pipeline Compliance: We successfully established a reproducible and auditable Data Version Control (DVC) pipeline. This system ensures that all data snapshots are versioned alongside the source code, meeting the rigorous audit standards required in the regulated financial services industry.
Risk Profiling: Through extensive statistical analysis of the MachineLearningRating_v3 dataset, we identified significant "Zero-Inflated" distributions in claim data. This confirms that while the majority of policies are profitable (claim-free), the minority of loss events are severe and stochastic.
Strategic Segmentation: Initial visual analysis has revealed distinct risk profiles across different Provinces, Vehicle Makes, and Demographic groups. These findings provide a clear roadmap for the feature engineering phase required for predictive modeling.




2. Project Background & Objectives
2.1 The Business Problem
In the competitive insurance landscape, accurate risk quantification is paramount. Traditional actuarial tables often fail to capture complex, non-linear interactions between driver demographics, vehicle characteristics, and geographic locations. The goal of this project is to transition from static rules-based pricing to dynamic, ML-driven risk rating.
2.2 Scope of Work (Week 3)
Task 1 (EDA): Ingest historical policy data, assess data quality, clean inconsistencies, and perform univariate and multivariate analysis to understand the "physics" of the portfolio.
Task 2 (MLOps Setup): Implement a version control system for datasets to ensure that any model generated can be traced back to the exact data snapshot used for training, ensuring reproducibility.

3. Data Engineering & Governance (DVC Implementation)
In financial modeling, reproducibility is not optional; it is a regulatory requirement. To address this, we implemented Data Version Control (DVC), a tool that brings Git-like versioning to large datasets.
3.1 Architecture Overview
The project architecture decouples the versioning of code from the versioning of data, while keeping them synchronized:
Code Repository (Git): Tracks the Python scripts and the lightweight .dvc metadata files.
Data Storage (DVC Remote): A centralized local storage directory (dvc_storage_insurance) was configured to simulate a secure object store (such as AWS S3). This separates the heavy data load from the codebase.
3.2 The Audit Trail Mechanism
To prove the robustness of the pipeline, a simulation of a "Data Drift" event was conducted:
Version 1 Baseline: The original MachineLearningRating_v3.txt was ingested, hashed, and locked to a specific Git commit hash.
Version 2 Simulation: New policy data was appended to the dataset to simulate a monthly data update. This new state was captured and pushed to the local remote.
Rollback Verification: A rollback test was executed. By checking out the Git commit associated with Version 1 and triggering a dvc checkout, the physical data file on the disk was instantly reverted to its original state (removing the new rows).
3.3 Implications for Modeling
This setup guarantees that when we train our XGBoost or Linear models in future phases, we can tag the specific data version used. If an auditor asks, "Why did the model output this premium for Customer X?", we can regenerate the exact training environment to provide an answer.

4. Exploratory Data Analysis (EDA)
The dataset analyzed is a rich collection of policy transactions including temporal data, financial metrics (Premium, Claims), and categorical features (Vehicle Type, Make, Province).
4.1 Data Quality & Preprocessing
Before analysis, several data integrity steps were taken:
Temporal Formatting: The columns TransactionMonth and VehicleIntroDate were converted from string formats to Python Datetime objects. This allows for the analysis of seasonality and vehicle age.
Demographic Imputation: Missing values were detected in the Gender, MaritalStatus, and Bank columns. Rather than dropping these rows (which would lose valuable claim data), we imputed them with a "Not Specified" category. This allows the model to potentially learn if "unspecified" customers represent a specific risk cohort.
Numeric Sanitization: Financial columns contained formatting artifacts. These were cleaned to ensure precision in Loss Ratio calculations.
4.2 Statistical Distributions
The analysis confirmed a phenomenon known as Zero-Inflation:
TotalClaims: The distribution is heavily right-skewed. Over 95% of the transaction rows have a TotalClaims value of 0.
TotalPremium: Premiums follow a more normal, albeit right-skewed, distribution.
Interpretation: This discrepancy implies that standard Root Mean Squared Error (RMSE) metrics may be misleading during modeling. We will likely need to employ Tweedie Loss functions or separate the model into two stages: (1) Probability of Claim (Classification) and (2) Severity of Claim (Regression).

5. Visual Insights & Strategic Findings
This section details the graphical analysis performed to understand the relationships between variables.
5.1 The Profitability Landscape
We aggregated the portfolio by Vehicle Make to understand where the business is making money versus where it is losing money.

Figure 1: Profitability Landscape by Vehicle Make.
This scatter plot visualizes the Total Premium Collected (X-axis) versus Total Claims Paid (Y-axis). The size and color of the bubbles represent the Loss Ratio. Green bubbles indicate healthy margins, while Red/Orange bubbles indicate segments where claims are disproportionately high compared to premiums. This suggests that underwriting criteria for specific luxury or high-performance makes need review.


5.2 Temporal Trends and Seasonality
An analysis of the TransactionMonth reveals how the portfolio performs over time.

Figure 2: Monthly Financial Timeline.
The dual-axis plot tracks the total cash inflow (Premiums) against cash outflow (Claims) over the 18-month period. While premiums remain relatively stable (showing slight growth), claims exhibit stochastic spikes. Notably, there are specific months where the Loss Ratio (Purple line) spikes significantly, suggesting seasonal risk factors (e.g., holiday travel periods or seasonal weather events).





5.3 Demographic and Vehicle Interaction
We utilized heatmaps to identify cross-segment risks, specifically looking at the interaction between Gender and Vehicle Type.

Figure 3: Risk Pricing Heatmap.
This matrix displays the Average Total Premium calculated for intersections of Gender and Vehicle Type. Darker blue areas indicate higher premiums. The data shows that 'Panel Vans' and 'Utility Vehicles' attract higher premiums regardless of gender, likely due to their commercial usage nature. Interestingly, the variance between genders for standard 'Passenger Vehicles' is minimal, suggesting the current pricing model is gender-neutral.
6. Geographic Analysis
A key component of insurance risk is location. We analyzed the dataset based on Province and PostalCode.
Key Findings:
Urban Concentration: The majority of policies are clustered in major metropolitan provinces (Gauteng, Western Cape).
Loss Ratio Variance: While Gauteng generates the highest volume of premiums, it also generates the highest volume of claims. However, certain rural provinces showed a higher Loss Ratio (Claims per Premium unit), suggesting that while claim frequency is lower in rural areas, the severity (cost) of individual accidents might be higher due to infrastructure quality or speed of emergency services.
7. Correlations and Variable Associations
A correlation matrix was generated to understand linear relationships between numerical features.
Observations:
SumInsured vs. TotalPremium (Positive Correlation): As expected, there is a strong correlation here. More expensive cars cost more to insure. This validates the baseline logic of the current pricing engine.
Premium vs. Claims (Weak Correlation): On an individual policy basis, there is very little correlation between the premium paid and the claim amount. This is expected in insurance; a customer paying a low premium can have a total-loss accident. This lack of linear correlation confirms the need for non-linear machine learning models (like Gradient Boosting) to capture the risk accurately.
8. Conclusion and Next Steps
The work completed in Week 3 has established a solid foundation for the predictive modeling phase. We have verified that the data is of sufficient quality for machine learning, identified the key features that drive risk (Vehicle Make, Location, Sum Insured), and established a secure pipeline to manage this data.
Upcoming Milestones (Week 4):
Feature Engineering:
Create a VehicleAge feature using TransactionMonth - VehicleIntroDate.
Create a ClaimsHistory feature to flag repeat offenders.
Model Selection:
Train an XGBoost model to predict Claim Frequency.
Train a Gamma-Regression model to predict Claim Severity.
AB Testing: Compare the new ML-based ratings against the existing linear pricing 

