import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()

    def create_features(self):
        """Creates new relevant features like VehicleAge."""
        self.df['TransactionMonth'] = pd.to_datetime(self.df['TransactionMonth'], errors='coerce')
        self.df['VehicleIntroDate'] = pd.to_datetime(self.df['VehicleIntroDate'], errors='coerce')

        ref_date = self.df['TransactionMonth'].max()
        self.df['VehicleAge'] = (ref_date - self.df['VehicleIntroDate']).dt.days / 365.25
        self.df['VehicleAge'] = self.df['VehicleAge'].fillna(self.df['VehicleAge'].mean())

        self.df['IsClaimed'] = self.df['TotalClaims'].apply(lambda x: 1 if x > 0 else 0)
        return self.df

    def encode_categorical(self, categorical_cols):
        """Encodes categorical columns."""
        le = LabelEncoder()
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str)
                self.df[col] = le.fit_transform(self.df[col])
        return self.df

    def prepare_data_for_modeling(self, target_col='TotalClaims', drop_cols=None, filter_claims=False):
        """
        Prepares X and y safely.
        """
        data = self.df.copy()

        if filter_claims:
            data = data[data['TotalClaims'] > 0]

        if drop_cols:
            data = data.drop(columns=drop_cols, errors='ignore')

        # Separate Features and Target
        X = data.drop(columns=[target_col])
        y = data[target_col]
        
        # --- FIX: CONVERT BOOLEANS TO INT ---
        # Select columns that are strictly 'object' or 'bool' and encode them
        for col in X.select_dtypes(include=['bool', 'object']).columns:
            # If it's boolean, map to 0/1
            if X[col].dtype == 'bool':
                X[col] = X[col].astype(int)
            else:
                # If it's a string, label encode it
                try:
                    X[col] = pd.to_numeric(X[col])
                except ValueError:
                    # If conversion fails (it's text), use Label Encoding
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col].astype(str))

        # Handle infinite values just in case
        pd.set_option('future.no_silent_downcasting', True) # Fix warning
        X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
        
        return X, y