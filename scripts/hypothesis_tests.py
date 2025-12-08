import pandas as pd
import numpy as np
from scipy import stats

class HypothesisTester:
    def __init__(self, df):
        self.df = df.copy()
        self.df['IsClaimed'] = self.df['TotalClaims'].apply(lambda x: 1 if x > 0 else 0)
        self.df['Margin'] = self.df['TotalPremium'] - self.df['TotalClaims']

    def test_province_risk(self):

        print(f"\n{'='*20} HYPOTHESIS 1: Risk Across Provinces {'='*20}")
        
        contingency_table = pd.crosstab(self.df['Province'], self.df['IsClaimed'])
        
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
        
        print(f"Test Statistic (Chi2): {chi2:.4f}")
        print(f"P-Value: {p_val:.4e}")
        self._interpret(p_val, "Province Risk Differences")
        return p_val

    def test_zipcode_risk(self):
        print(f"\n{'='*20} HYPOTHESIS 2: Risk Between Zip Codes {'='*20}")

        top_zips = self.df['PostalCode'].value_counts().head(2).index.tolist()
        zip_a, zip_b = top_zips[0], top_zips[1]
        
        print(f"Comparing Zip Code A ({zip_a}) vs Zip Code B ({zip_b})")
        
        sub_df = self.df[self.df['PostalCode'].isin([zip_a, zip_b])]
        contingency_table = pd.crosstab(sub_df['PostalCode'], sub_df['IsClaimed'])
        
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
        
        print(f"P-Value: {p_val:.4f}")
        self._interpret(p_val, f"Risk Difference between {zip_a} and {zip_b}")

    def test_margin_difference_zipcodes(self):
        print(f"\n{'='*20} HYPOTHESIS 3: Margin Differences (Zip Codes) {'='*20}")
        
        top_zips = self.df['PostalCode'].value_counts().head(2).index.tolist()
        zip_a, zip_b = top_zips[0], top_zips[1]
        
        group_a = self.df[self.df['PostalCode'] == zip_a]['Margin']
        group_b = self.df[self.df['PostalCode'] == zip_b]['Margin']
        
        t_stat, p_val = stats.ttest_ind(group_a, group_b, equal_var=False)
        
        print(f"Mean Margin A ({zip_a}): {group_a.mean():.2f}")
        print(f"Mean Margin B ({zip_b}): {group_b.mean():.2f}")
        print(f"P-Value: {p_val:.4f}")
        self._interpret(p_val, "Margin Difference")

    def test_gender_risk(self):
        """
        H0: There is no significant risk difference between Women and Men.
        Metric: Claim Frequency (Chi-Squared)
        """
        print(f"\n{'='*20} HYPOTHESIS 4: Risk Women vs Men {'='*20}")
        gender_df = self.df[self.df['Gender'].isin(['Male', 'Female'])]
        
        contingency_table = pd.crosstab(gender_df['Gender'], gender_df['IsClaimed'])
        
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
        
        print(f"P-Value: {p_val:.4f}")
        self._interpret(p_val, "Gender Risk Difference")

    def _interpret(self, p_value, context):
        if p_value < 0.05:
            print(f"🔴 RESULT: REJECT Null Hypothesis. There is a statistically significant {context}.")
        else:
            print(f"🟢 RESULT: FAIL TO REJECT Null Hypothesis. No significant {context} found.")