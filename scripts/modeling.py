import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report

class ModelTrainer:
    def __init__(self, X, y, task='regression'):
        self.X = X
        self.y = y
        self.task = task
        self.models = {}
        
        # Split Data (80/20)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

    def train_models(self):
        print(f"🚀 Training Models for {self.task}...")
        
        if self.task == 'regression':
            # 1. Linear Regression
            lr = LinearRegression()
            lr.fit(self.X_train, self.y_train)
            self.models['LinearRegression'] = lr
            
            # 2. Random Forest
            rf = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
            rf.fit(self.X_train, self.y_train)
            self.models['RandomForest'] = rf
            
            # 3. Gradient Boosting (Scikit-Learn version)
            gb_reg = GradientBoostingRegressor(n_estimators=50, max_depth=5, random_state=42)
            gb_reg.fit(self.X_train, self.y_train)
            self.models['GradientBoosting'] = gb_reg

        elif self.task == 'classification':
            # 1. Random Forest Classifier
            rf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, class_weight='balanced')
            rf.fit(self.X_train, self.y_train)
            self.models['RandomForest'] = rf
            
            # 2. Gradient Boosting Classifier
            gb_clf = GradientBoostingClassifier(n_estimators=50, max_depth=5, random_state=42)
            gb_clf.fit(self.X_train, self.y_train)
            self.models['GradientBoosting'] = gb_clf
            
    def evaluate(self):
        results = {}
        for name, model in self.models.items():
            preds = model.predict(self.X_test)
            
            if self.task == 'regression':
                mse = mean_squared_error(self.y_test, preds)
                rmse = np.sqrt(mse)
                r2 = r2_score(self.y_test, preds)
                results[name] = {'RMSE': rmse, 'R2': r2}
                print(f"📊 {name}: RMSE={rmse:.2f}, R2={r2:.4f}")
            
            elif self.task == 'classification':
                acc = accuracy_score(self.y_test, preds)
                print(f"📊 {name} Accuracy: {acc:.2%}")
                results[name] = {'Accuracy': acc}
                
        return results

    def get_best_model(self):
        return self.models.get('GradientBoosting')