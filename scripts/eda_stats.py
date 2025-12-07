import pandas as pd

class EDAAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_summary_stats(self):
        """Returns numerical description."""
        return self.df.describe().T

    def get_missing_values(self):
        """Returns columns with missing values count."""
        missing = self.df.isnull().sum()
        return missing[missing > 0].sort_values(ascending=False)

    def calculate_overall_loss_ratio(self):
        """Calculates TotalClaims / TotalPremium."""
        total_premium = self.df['TotalPremium'].sum()
        total_claims = self.df['TotalClaims'].sum()
        ratio = total_claims / total_premium if total_premium > 0 else 0
        return ratio

    def get_correlation_matrix(self, columns):
        """Returns correlation matrix for specific columns."""
        existing_cols = [c for c in columns if c in self.df.columns]
        return self.df[existing_cols].corr()