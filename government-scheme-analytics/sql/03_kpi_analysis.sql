-- KPI aggregation examples
-- Total sanctioned, released, utilized by financial year
WITH kpi AS (
    SELECT Financial_Year,
           COUNT(*) AS records,
           SUM(Sanctioned_Amount_Lakhs) AS total_sanctioned_lakhs,
           SUM(Fund_Released_Lakhs) AS total_released_lakhs,
           SUM(Fund_Utilized_Lakhs) AS total_utilized_lakhs
    FROM government_scheme_records
    GROUP BY Financial_Year
)
SELECT *,
       CASE WHEN total_sanctioned_lakhs = 0 THEN NULL ELSE total_released_lakhs / total_sanctioned_lakhs * 100 END AS release_pct,
       CASE WHEN total_released_lakhs = 0 THEN NULL ELSE total_utilized_lakhs / total_released_lakhs * 100 END AS utilization_pct
FROM kpi
ORDER BY Financial_Year;
