"""05_analysis.py
Statistical analysis and outlier detection.
Outputs: reports/correlation_matrix.csv, reports/group_stats.csv, reports/outliers.csv
"""
import logging
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / 'data' / 'processed' / 'government_scheme_features.csv'
OUT_DIR = ROOT / 'reports'
OUT_DIR.mkdir(parents=True, exist_ok=True)


def correlation_analysis(df: pd.DataFrame):
    cols = ['Sanctioned_Amount_Lakhs','Fund_Released_Lakhs','Fund_Utilized_Lakhs','Fund_Utilization_Ratio','Physical_Achievement_Rate','Beneficiary_Coverage_Rate']
    present = [c for c in cols if c in df.columns]
    corr_pearson = df[present].corr(method='pearson')
    corr_spearman = df[present].corr(method='spearman')
    corr_pearson.to_csv(OUT_DIR / 'correlation_pearson.csv')
    corr_spearman.to_csv(OUT_DIR / 'correlation_spearman.csv')
    logging.info('Correlation matrices written')


def group_stats(df: pd.DataFrame, group_by: str = 'Financial_Year'):
    agg = df.groupby(group_by).agg(
        records=('Record_ID','count'),
        sanctioned_mean=('Sanctioned_Amount_Lakhs','mean'),
        released_mean=('Fund_Released_Lakhs','mean'),
        utilized_mean=('Fund_Utilized_Lakhs','mean'),
        utilization_mean=('Fund_Utilization_Ratio','mean')
    ).reset_index()
    agg.to_csv(OUT_DIR / 'group_stats_{}.csv'.format(group_by), index=False)
    logging.info('Group stats written for %s', group_by)


def outlier_detection(df: pd.DataFrame):
    num_cols = ['Sanctioned_Amount_Lakhs','Fund_Released_Lakhs','Fund_Utilized_Lakhs','Fund_Utilization_Ratio']
    candidates = [c for c in num_cols if c in df.columns]
    outlier_rows = []
    for c in candidates:
        ser = df[c]
        # IQR method
        q1 = ser.quantile(0.25)
        q3 = ser.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        iqr_out = df[(ser < lower) | (ser > upper)].copy()
        iqr_out['outlier_metric'] = 'IQR'
        iqr_out['outlier_on'] = c
        outlier_rows.append(iqr_out)

        # Z-score method
        z = np.abs(stats.zscore(ser.dropna()))
        z_idx = ser.dropna().index[z > 3]
        z_out = df.loc[z_idx].copy()
        z_out['outlier_metric'] = 'Zscore'
        z_out['outlier_on'] = c
        outlier_rows.append(z_out)

    if outlier_rows:
        outdf = pd.concat(outlier_rows).drop_duplicates(subset=['Record_ID','outlier_on','outlier_metric'])
        outdf.to_csv(OUT_DIR / 'outliers.csv', index=False)
        logging.info('Outliers written to %s', OUT_DIR / 'outliers.csv')
    else:
        logging.info('No outliers detected with chosen methods')


def main():
    logging.info(f"Loading data from {IN_FILE}")
    df = pd.read_csv(IN_FILE, low_memory=False)
    correlation_analysis(df)
    group_stats(df, 'Financial_Year')
    group_stats(df, 'State')
    outlier_detection(df)


if __name__ == '__main__':
    main()
