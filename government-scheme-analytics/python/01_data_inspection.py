"""01_data_inspection.py
Load dataset and perform an initial professional data audit.
Produces: reports/data_quality_report.csv and a cleaned sample preview in data/processed/ (not overwriting raw data).
"""
import os
from pathlib import Path
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

ROOT = Path(__file__).resolve().parents[1]
RAW_CSV_GUESS = ROOT.parent / "govt_fund_utilization.csv"


def find_csv(files_dir: Path):
    # If a CSV exists at workspace root with expected name, prefer it.
    candidates = list(files_dir.glob("*.csv"))
    if not candidates:
        raise FileNotFoundError(f"No CSV files found in {files_dir}")
    # If exact filename present, return it
    for c in candidates:
        if c.name.lower().startswith("govt_fund_util") or c.name.lower().startswith("government"):
            logging.info(f"Selected CSV: {c.name}")
            return c
    # fallback to largest CSV (heuristic)
    candidates.sort(key=lambda p: p.stat().st_size, reverse=True)
    logging.info(f"Selected CSV (fallback): {candidates[0].name}")
    return candidates[0]


def inspect(df: pd.DataFrame):
    info = {
        'shape': df.shape,
        'dtypes': df.dtypes.astype(str).to_dict(),
        'head': df.head(5),
        'tail': df.tail(5),
        'describe': df.describe(include='all', datetime_is_numeric=True).T,
        'missing': df.isnull().sum().sort_values(ascending=False),
        'duplicates': df.duplicated(keep=False).sum()
    }
    return info


def data_quality_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = []
    n = len(df)
    for c in df.columns:
        ser = df[c]
        dtype = str(ser.dtype)
        non_null = ser.notnull().sum()
        missing = n - non_null
        missing_pct = missing / n * 100
        unique_vals = ser.nunique(dropna=True)
        cols.append({
            'column': c,
            'dtype': dtype,
            'non_null_count': non_null,
            'missing_count': missing,
            'missing_pct': round(missing_pct, 2),
            'unique_values': unique_vals
        })
    return pd.DataFrame(cols)


def main():
    workspace = Path.cwd()
    csv_path = find_csv(workspace)
    logging.info(f"Loading {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)

    logging.info(f"Data loaded. Shape: {df.shape}")

    # Standard inspection outputs
    print("\n-- HEAD --")
    print(df.head().to_string())
    print("\n-- TAIL --")
    print(df.tail().to_string())
    print("\n-- INFO --")
    df.info()
    print("\n-- DESCRIBE --")
    try:
        desc = df.describe(include='all', datetime_is_numeric=True).T
    except TypeError:
        # Older/newer pandas may not accept datetime_is_numeric; fallback
        desc = df.describe(include='all').T
    print(desc)

    dq = data_quality_table(df)
    reports_dir = ROOT / 'reports'
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_csv = reports_dir / 'data_quality_report.csv'
    dq.to_csv(out_csv, index=False)
    logging.info(f"Data quality report written to {out_csv}")


if __name__ == '__main__':
    main()
