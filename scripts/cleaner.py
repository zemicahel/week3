import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df

    def convert_to_datetime(self, columns):
        """Converts specific columns to datetime objects."""
        for col in columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        return self.df

    def convert_to_numeric(self, columns):
        """Converts specific columns to numeric, coercing errors to 0."""
        for col in columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        return self.df

    def impute_categorical(self, columns, fill_value='Not specified'):
        """Fills missing values in categorical columns."""
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(fill_value)
        return self.df
    
    def get_cleaned_data(self):
        return self.df