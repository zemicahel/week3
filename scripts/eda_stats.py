import pandas as pd

class EDAAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_summary_stats(self):
        return self.df.describe().T

    def get_missing_values(self):
        missing = self.df.isnull().sum()
        return missing[missing > 0].sort_values(ascending=False)

    def calculate_overall_loss_ratio(self):
        total_premium = self.df['TotalPremium'].sum()
        total_claims = self.df['TotalClaims'].sum()
        ratio = total_claims / total_premium if total_premium > 0 else 0
        return ratio

    def get_correlation_matrix(self, columns):
        existing_cols = [c for c in columns if c in self.df.columns]
        return self.df[existing_cols].corr()

    # --- NEW ADDITION FOR OUTLIER ANALYSIS ---
    def detect_outliers_iqr(self, column):
        """
        Calculates outlier bounds using the Interquartile Range (IQR).
        Returns a dictionary with statistics.
        """
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        
        return {
            "IQR": IQR,
            "Lower Bound": lower_bound,
            "Upper Bound": upper_bound,
            "Outliers Count": len(outliers),
            "Outliers Percentage": (len(outliers) / len(self.df)) * 100
        }