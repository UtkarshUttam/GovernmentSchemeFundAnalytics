# DAX Measures (examples)

Use `DIVIDE()` to avoid divide-by-zero.

Example measures:

- Total Sanctioned := SUM(government_scheme_records[Sanctioned_Amount_Lakhs])
- Total Released := SUM(government_scheme_records[Fund_Released_Lakhs])
- Total Utilized := SUM(government_scheme_records[Fund_Utilized_Lakhs])
- Release Ratio % := DIVIDE([Total Released],[Total Sanctioned])*100
- Utilization Ratio % := DIVIDE([Total Utilized],[Total Released])*100

Time-intelligence examples:
- Prev Year Utilized := CALCULATE([Total Utilized], SAMEPERIODLASTYEAR('Date'[Date]))
- YoY Utilized Change := [Total Utilized] - [Prev Year Utilized]
- YoY Utilized Change % := DIVIDE([YoY Utilized Change],[Prev Year Utilized])

Additional examples:
- FYTD Utilized := CALCULATE([Total Utilized], DATESYTD('Date'[Date], "03/31"))
- YoY Utilization Ratio :=
VAR Current = [Utilization Ratio %]
VAR Prior = CALCULATE([Utilization Ratio %], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN DIVIDE(Current - Prior, Prior)
