import pandas as pd

class DataLoader:
    def __init__(self, file_path, separator='|'):
        self.file_path = file_path
        self.separator = separator

    def load_data(self):
        """Loads data from the CSV/TXT file."""
        try:
            print(f"🔄 Loading data from {self.file_path}...")
            # low_memory=False handles mixed types in large files better
            df = pd.read_csv(self.file_path, sep=self.separator, low_memory=False)
            print(f"✅ Data loaded successfully! Shape: {df.shape}")
            return df
        except FileNotFoundError:
            print(f"❌ Error: File not found at {self.file_path}")
            return None
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return None