"""02_data_cleaning.py
Reproducible cleaning pipeline. Reads raw CSV, performs type conversions, creates validation flags,
and writes cleaned dataset to data/processed/government_scheme_cleaned.csv
"""
import logging
from pathlib import Path
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT.parent / "govt_fund_utilization.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().replace(' ', '_') for c in df.columns]
    return df


def create_validation_flags(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # numeric columns
    num_cols = ['Sanctioned_Amount_Lakhs', 'Fund_Released_Lakhs', 'Fund_Utilized_Lakhs']
    for c in num_cols:
        if c in df.columns:
            df[c + '_orig'] = df[c]
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Date conversion
    if 'Date_of_Fund_Release' in df.columns:
        df['Date_of_Fund_Release'] = pd.to_datetime(df['Date_of_Fund_Release'], errors='coerce')

    # Flags
    df['financial_anomaly_flag'] = False
    df['physical_anomaly_flag'] = False
    df['beneficiary_anomaly_flag'] = False
    df['missing_data_flag'] = df.isnull().any(axis=1)

    # Negative values
    for c in num_cols:
        if c in df.columns:
            df.loc[df[c] < 0, 'financial_anomaly_flag'] = True

    # logical inconsistencies
    if all(x in df.columns for x in ['Fund_Utilized_Lakhs', 'Fund_Released_Lakhs']):
        df.loc[df['Fund_Utilized_Lakhs'] > df['Fund_Released_Lakhs'], 'financial_anomaly_flag'] = True

    if all(x in df.columns for x in ['Fund_Released_Lakhs', 'Sanctioned_Amount_Lakhs']):
        df.loc[df['Fund_Released_Lakhs'] > df['Sanctioned_Amount_Lakhs'], 'financial_anomaly_flag'] = True

    if all(x in df.columns for x in ['Physical_Achievement_Units', 'Physical_Target_Units']):
        df.loc[df['Physical_Achievement_Units'] > df['Physical_Target_Units'], 'physical_anomaly_flag'] = True

    if all(x in df.columns for x in ['Beneficiaries_Covered', 'Beneficiaries_Target']):
        df.loc[df['Beneficiaries_Covered'] > df['Beneficiaries_Target'], 'beneficiary_anomaly_flag'] = True

    return df


def main():
    logging.info(f"Loading raw CSV from {RAW_CSV}")
    df = pd.read_csv(RAW_CSV, low_memory=False)
    df = normalize_columns(df)
    df = create_validation_flags(df)

    # Remove exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    logging.info(f"Dropped {before-after} exact duplicate rows")

    out = PROCESSED_DIR / 'government_scheme_cleaned.csv'
    df.to_csv(out, index=False)
    logging.info(f"Cleaned data written to {out}")


if __name__ == '__main__':
    main()
