-- SQL view templates for analytical exploration (PostgreSQL syntax)

-- View: scheme-level summary
CREATE OR REPLACE VIEW vw_scheme_summary AS
SELECT
  Scheme_Code,
  Scheme_Name,
  COUNT(*) AS records,
  SUM(Sanctioned_Amount_Lakhs) AS total_sanctioned_lakhs,
  SUM(Fund_Released_Lakhs) AS total_released_lakhs,
  SUM(Fund_Utilized_Lakhs) AS total_utilized_lakhs,
  ROUND(100.0 * SUM(Fund_Utilized_Lakhs) / NULLIF(SUM(Fund_Released_Lakhs),0),2) AS utilization_percent,
  AVG(Fund_Utilized_Lakhs) AS avg_utilized_lakhs
FROM government_scheme_records
GROUP BY Scheme_Code, Scheme_Name;

-- View: state-level summary
CREATE OR REPLACE VIEW vw_state_summary AS
SELECT
  State,
  COUNT(*) AS records,
  SUM(Sanctioned_Amount_Lakhs) AS sanctioned_lakhs,
  SUM(Fund_Released_Lakhs) AS released_lakhs,
  SUM(Fund_Utilized_Lakhs) AS utilized_lakhs,
  (SUM(Fund_Released_Lakhs) - SUM(Fund_Utilized_Lakhs)) AS unutilized_lakhs,
  ROUND(100.0 * SUM(Fund_Utilized_Lakhs) / NULLIF(SUM(Fund_Released_Lakhs),0),2) AS utilization_percent
FROM government_scheme_records
GROUP BY State;

-- Example analytical query using window functions
-- Top 5 schemes by sanctioned amount with rank
SELECT
  Scheme_Name,
  total_sanctioned_lakhs,
  RANK() OVER (ORDER BY total_sanctioned_lakhs DESC) AS sanction_rank
FROM vw_scheme_summary
ORDER BY sanction_rank
LIMIT 5;
