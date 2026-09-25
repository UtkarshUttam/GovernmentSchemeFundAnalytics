"""04_eda.py
Exploratory Data Analysis producing key charts and CSV summaries.
"""
import logging
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / 'data' / 'processed' / 'government_scheme_features.csv'
FIG_DIR = ROOT / 'reports' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)


def top_n_summary(df, group_col, value_col, n=10):
    return df.groupby(group_col)[value_col].sum().sort_values(ascending=False).head(n)


def main():
    logging.info(f"Loading feature data from {IN_FILE}")
    df = pd.read_csv(IN_FILE, low_memory=False)

    # Financial year summary
    if 'Financial_Year' in df.columns:
        fy = df.groupby('Financial_Year').agg(
            records=('Record_ID','count'),
            sanctioned_lakhs=('Sanctioned_Amount_Lakhs','sum'),
            released_lakhs=('Fund_Released_Lakhs','sum'),
            utilized_lakhs=('Fund_Utilized_Lakhs','sum'),
            avg_utilization=('Fund_Utilization_Ratio','mean')
        ).reset_index()
        fy.to_csv(ROOT / 'reports' / 'financial_year_summary.csv', index=False)

    # Top schemes by sanctioned amount
    top_schemes = top_n_summary(df, 'Scheme_Name', 'Sanctioned_Amount_Lakhs', n=10)
    top_schemes.to_csv(ROOT / 'reports' / 'top_schemes_by_sanctioned.csv')

    # Plot sanctioned vs released vs utilized by financial year
    if 'Financial_Year' in df.columns:
        plot_df = df.groupby('Financial_Year')[['Sanctioned_Amount_Lakhs','Fund_Released_Lakhs','Fund_Utilized_Lakhs']].sum()
        ax = plot_df.plot(kind='bar', figsize=(10,6))
        ax.set_ylabel('Amount (Lakhs)')
        plt.tight_layout()
        plt.savefig(FIG_DIR / 'sanctioned_released_utilized_by_fy.png')
        plt.close()

    # State-wise utilization distribution
    if 'State' in df.columns:
        state_df = df.groupby('State').agg(sanctioned=('Sanctioned_Amount_Lakhs','sum'),
                                           released=('Fund_Released_Lakhs','sum'),
                                           utilized=('Fund_Utilized_Lakhs','sum'))
        state_df['unutilized'] = state_df['released'] - state_df['utilized']
        state_df = state_df.sort_values('utilized', ascending=False)
        state_df.to_csv(ROOT / 'reports' / 'state_funding_summary.csv')

    logging.info("EDA artifacts written to reports/")


if __name__ == '__main__':
    main()
