"""03_feature_engineering.py
Create analytical fields and handle safe divisions.
"""
import logging
from pathlib import Path
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / 'data' / 'processed'
IN_FILE = PROCESSED_DIR / 'government_scheme_cleaned.csv'
OUT_FILE = PROCESSED_DIR / 'government_scheme_features.csv'


def safe_divide(num, den):
    return np.where((den == 0) | pd.isnull(den) | pd.isnull(num), np.nan, num / den)


def main():
    logging.info(f"Loading cleaned data from {IN_FILE}")
    df = pd.read_csv(IN_FILE, parse_dates=['Date_of_Fund_Release'], low_memory=False)

    # Ensure numeric
    for c in ['Sanctioned_Amount_Lakhs', 'Fund_Released_Lakhs', 'Fund_Utilized_Lakhs',
              'Physical_Target_Units', 'Physical_Achievement_Units', 'Beneficiaries_Target', 'Beneficiaries_Covered']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Financial metrics
    df['Fund_Release_Ratio'] = safe_divide(df['Fund_Released_Lakhs'], df['Sanctioned_Amount_Lakhs']) * 100
    df['Fund_Utilization_Ratio'] = safe_divide(df['Fund_Utilized_Lakhs'], df['Fund_Released_Lakhs']) * 100
    df['Unutilized_Funds_Lakhs'] = df['Fund_Released_Lakhs'] - df['Fund_Utilized_Lakhs']
    df['Sanction_to_Release_Gap_Lakhs'] = df['Sanctioned_Amount_Lakhs'] - df['Fund_Released_Lakhs']

    # Physical metrics
    df['Physical_Achievement_Rate'] = safe_divide(df['Physical_Achievement_Units'], df['Physical_Target_Units']) * 100
    df['Achievement_Gap'] = df['Physical_Target_Units'] - df['Physical_Achievement_Units']

    # Beneficiary metrics
    df['Beneficiary_Coverage_Rate'] = safe_divide(df['Beneficiaries_Covered'], df['Beneficiaries_Target']) * 100
    df['Beneficiary_Gap'] = df['Beneficiaries_Target'] - df['Beneficiaries_Covered']

    # Date derived
    if 'Date_of_Fund_Release' in df.columns:
        df['YearMonth'] = df['Date_of_Fund_Release'].dt.to_period('M').astype(str)
        df['Quarter'] = df['Date_of_Fund_Release'].dt.to_period('Q').astype(str)
        df['Year'] = df['Date_of_Fund_Release'].dt.year

    # Sort key for financial year if present
    if 'Financial_Year' in df.columns:
        df['Financial_Year_Sort'] = df['Financial_Year']

    # Bins
    df['Utilization_Band'] = pd.cut(df['Fund_Utilization_Ratio'], bins=[-1,25,50,75,90,100,200], labels=['0-25','25-50','50-75','75-90','90-100','100+'])
    df['Achievement_Band'] = pd.cut(df['Physical_Achievement_Rate'], bins=[-1,25,50,75,90,100,200], labels=['0-25','25-50','50-75','75-90','90-100','100+'])
    df['Beneficiary_Coverage_Band'] = pd.cut(df['Beneficiary_Coverage_Rate'], bins=[-1,25,50,75,90,100,200], labels=['0-25','25-50','50-75','75-90','90-100','100+'])

    df['Data_Quality_Flag'] = df[['financial_anomaly_flag', 'physical_anomaly_flag', 'beneficiary_anomaly_flag', 'missing_data_flag']].any(axis=1)

    df.to_csv(OUT_FILE, index=False)
    logging.info(f"Feature-engineered data written to {OUT_FILE}")


if __name__ == '__main__':
    main()
