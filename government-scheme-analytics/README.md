# Government Scheme Fund Analytics

Synthetic dataset portfolio project delivering a professional end-to-end analysis of simulated Indian government scheme funding, utilization, physical achievement, and beneficiary coverage.

IMPORTANT: This repository uses a synthetic dataset for educational purposes only. See the `data/` folder for the original CSV location and the `reports/` folder for data-quality notes.

Structure:
- `data/` - raw and processed datasets
- `python/` - Python scripts for inspection, cleaning, feature engineering, EDA, and analysis
- `sql/` - SQL schema, views and analytical queries
- `powerbi/` - Power BI model and measure documentation
- `reports/` - figures and analysis summaries
- `notebooks/` - exploratory notebook

See `python/01_data_inspection.py` to start.

## Executive Summary

- **Dataset:** Synthetic government fund utilization records (1,000 rows, 21 columns). Contains financials (sanctioned, released, utilized), physical targets/achievement, and beneficiary targets/coverage.
- **Key findings:**
	- **Top-funded schemes:** Jal Jeevan Mission, Swachh Bharat Mission - Gramin, National Health Mission, PM Kisan Samman Nidhi, and PM Awas Gramin account for the largest sanctioned amounts.
	- **State funding distribution:** West Bengal, Rajasthan, Tamil Nadu, Kerala, and Bihar show the highest sanctioned totals; unutilized funds are material in several large states.
	- **Utilization & outcomes:** Overall average utilization by financial year hovers around ~68% with modest variation across years. Financial amounts (sanctioned → released → utilized) are strongly correlated (Pearson ~0.93 between sanctioned and released). Fund utilization ratio correlates with physical achievement and beneficiary coverage (Spearman ~0.66–0.96), suggesting funds translated to outputs in many high-performing cases.
	- **Data quality & risks:** Missing values exist in `Fund_Utilized_Lakhs`, `Physical_Achievement_Units`, and `Beneficiaries_Covered` among others. Several records flagged as outliers (IQR and Z-score) for unusually high utilization or zero utilization despite large releases — these are written to `reports/outliers.csv` for review.
- **Recommendations:**
	- Investigate top outlier records in `reports/outliers.csv` for reporting errors or exceptional programme cases.
	- Prioritize reconciliations for states with large unutilized balances (e.g., West Bengal, Tamil Nadu, Kerala) and for top-funded schemes.
	- Use the cleaned features file `data/processed/government_scheme_features.csv` as the analytical fact table for BI and SQL views.

## Next steps

- Draft SQL analytical views and queries under `sql/` (vw_scheme_summary, vw_state_summary, vw_department_summary, vw_financial_year_summary).
- Expand `powerbi/` with a 3-page dashboard spec and DAX measures (drafts present in `powerbi/dax_measures.md`).
- Finalize `reports/analysis_summary.md` with Observation / Evidence / Interpretation / Recommended Investigation entries.

## Quick Start (run locally)

1. Create a Python environment and install dependencies:

```powershell
c:/python313/python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the inspection and pipelines (they write outputs to `reports/` and `data/processed/`):

```powershell
python python/01_data_inspection.py
python python/02_data_cleaning.py
python python/03_feature_engineering.py
python python/04_eda.py
python python/05_analysis.py
```

3. Open `reports/executive_summary.txt` and `reports/analysis_summary.md` for key findings.

## Project Deliverables (highlight)

- `data/processed/government_scheme_cleaned.csv` — cleaned dataset (preserves raw values and flags).
- `data/processed/government_scheme_features.csv` — feature-engineered fact table for analysis and BI.
- `reports/` — data-quality, EDA tables, correlation matrices, outliers, and figures.
- `sql/` — DDL and view templates to load the cleaned data into Postgres for analytical queries.
- `powerbi/` — DAX measure examples and dashboard design notes.


## Key Visuals

Below are the core charts produced during exploratory analysis. Full-resolution images are in `reports/figures/`.

- Sanctioned / Released / Utilized by Financial Year

	![Sanctioned/Released/Utilized by FY](reports/figures/sanctioned_released_utilized_by_fy.png)

- Distribution of Fund Utilization Ratio

	![Utilization Ratio Distribution](reports/figures/utilization_ratio_distribution.png)

- Top 6 Schemes by Sanctioned Amount (pie)

	![Top Schemes by Sanctioned Amount](reports/figures/top_schemes_pie.png)

- Top 10 States by Sanctioned Amount

	![Top States by Sanctioned Amount](reports/figures/top_states_sanctioned.png)


