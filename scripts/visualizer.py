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

    def plot_profitability_landscape(self):
        """
        Plots Total Premium vs Total Claims by Vehicle Make.
        Size and Color represent the Loss Ratio.
        """
        if 'make' not in self.df.columns:
            print("Column 'make' not found in dataset.")
            return

        # 1. Prepare Data
        make_stats = self.df.groupby('make')[['TotalPremium', 'TotalClaims']].sum().reset_index()
        make_stats['LossRatio'] = make_stats['TotalClaims'] / make_stats['TotalPremium']

        # 2. Plot
        plt.figure(figsize=(14, 8))
        sns.scatterplot(
            data=make_stats,
            x='TotalPremium',
            y='TotalClaims',
            size='LossRatio',
            hue='LossRatio',
            palette='RdYlGn_r', # Red is Bad (High Loss), Green is Good (Low Loss)
            sizes=(100, 1000),
            alpha=0.8
        )
        plt.title('Profitability Landscape: Vehicle Make Risk Analysis')
        plt.xlabel('Total Premium (Revenue)')
        plt.ylabel('Total Claims (Cost)')
        plt.show()

    def plot_bivariate_scatter(self, x_col, y_col, hue=None):
        """Plots a scatter plot to show relationship between two variables."""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=hue, alpha=0.6)
        plt.title(f'Bivariate Analysis: {x_col} vs {y_col}')
        plt.show()