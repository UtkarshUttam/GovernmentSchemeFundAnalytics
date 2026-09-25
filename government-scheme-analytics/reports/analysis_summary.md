# Analysis Summary

This document summarizes key observations from the analysis, evidence (reports/ CSVs), interpretation, and recommended next investigations.

- Observation: Average fund utilization across financial years is ~68%.
	- Evidence: `reports/financial_year_summary.csv` shows avg_utilization per FY.
	- Interpretation: A consistent gap exists between released and utilized funds, indicating implementation or absorption issues.
	- Recommended Investigation: Break down by scheme and state; check timing (late releases) and administrative bottlenecks.

- Observation: Top schemes receive a disproportionate share of sanctioned funds.
	- Evidence: `reports/top_schemes_by_sanctioned.csv`.
	- Interpretation: Program-level prioritization concentrates resources; variance in utilization across these schemes can materially affect overall performance.
	- Recommended Investigation: For each top scheme, compute state-level utilization bands and identify underperforming states.

- Observation: Several high-value records show near-zero utilization or unusually high utilization (outliers).
	- Evidence: `reports/outliers.csv`.
	- Interpretation: Could indicate reporting lags, data-entry issues, or exceptional one-off expenditures.
	- Recommended Investigation: Cross-check with audit remarks/attachments and implementing agency communications.

- Observation: Positive correlation between utilization ratio and physical/beneficiary achievement.
	- Evidence: `reports/correlation_pearson.csv` and `reports/correlation_spearman.csv`.
	- Interpretation: Where funds are utilized, physical outputs and beneficiary coverage tend to increase, supporting program effectiveness hypotheses.
	- Recommended Investigation: Run per-scheme and per-state causal checks (time-lagged regressions) to test causality.

- Observation: Missing or flagged data in key outcome columns (beneficiaries, physical achievement).
	- Evidence: `reports/data_quality_report.csv` and `data/processed/government_scheme_features.csv` (Data_Quality_Flag).
	- Interpretation: Missing outcome reporting reduces confidence in impact assessments.
	- Recommended Investigation: Engage data providers to standardize reporting cadence and mandatory fields; implement validation checks at data submission.

## Actionable Deliverables

- `data/processed/government_scheme_features.csv`: Use as fact table for SQL views and Power BI model.
- `reports/outliers.csv`: Review and reconcile with source documents.
- `sql/01_create_tables.sql`: Load cleaned data into Postgres for analytical queries.

