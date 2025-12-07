import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    def __init__(self, df):
        self.df = df
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)

    def plot_histogram(self, column, color='skyblue', log_scale=False):
        """Plots a histogram for a numerical column."""
        plt.figure(figsize=(10, 5))
        sns.histplot(data=self.df, x=column, kde=True, color=color, bins=50)
        if log_scale:
            plt.xscale('log')
        plt.title(f'Distribution of {column}')
        plt.show()

    def plot_counts(self, column, top_n=10):
        """Plots a count plot for a categorical column."""
        plt.figure(figsize=(10, 6))
        order = self.df[column].value_counts().nlargest(top_n).index
        sns.countplot(data=self.df, y=column, order=order, palette='viridis')
        plt.title(f'Top {top_n} Counts: {column}')
        plt.show()

    def plot_correlation_heatmap(self, corr_matrix):
        """Plots a heatmap from a correlation matrix."""
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        plt.show()

    def plot_outliers(self, column):
        """Plots a boxplot to detect outliers."""
        plt.figure(figsize=(10, 5))
        # Filter 0s for better visibility if it's claims data
        data_to_plot = self.df[self.df[column] > 0] if column == 'TotalClaims' else self.df
        sns.boxplot(x=data_to_plot[column], color='salmon')
        plt.title(f'Boxplot of {column}')
        plt.show()

    def plot_creative_loss_ratio_over_time(self):
        """Plots the Loss Ratio trend over time."""
        if 'TransactionMonth' not in self.df.columns:
            print("TransactionMonth not found.")
            return

        monthly = self.df.groupby('TransactionMonth')[['TotalPremium', 'TotalClaims']].sum().reset_index()
        monthly['LossRatio'] = monthly['TotalClaims'] / monthly['TotalPremium']

        plt.figure(figsize=(12, 5))
        sns.lineplot(data=monthly, x='TransactionMonth', y='LossRatio', marker='o', color='purple')
        plt.axhline(monthly['LossRatio'].mean(), color='red', linestyle='--', label='Avg Loss Ratio')
        plt.title('Monthly Loss Ratio Trend')
        plt.legend()
        plt.show()

    def plot_creative_risk_heatmap(self, x_col, y_col, val_col):
        """Plots a pivot table heatmap (e.g., Gender vs VehicleType)."""
        pivot = self.df.pivot_table(index=y_col, columns=x_col, values=val_col, aggfunc='mean')
        plt.figure(figsize=(12, 6))
        sns.heatmap(pivot, cmap='YlGnBu', annot=True, fmt=".0f")
        plt.title(f'Heatmap: Mean {val_col} by {y_col} vs {x_col}')
        plt.show()