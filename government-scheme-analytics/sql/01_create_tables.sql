-- Create base table for government scheme records (PostgreSQL syntax)
CREATE TABLE government_scheme_records (
    Record_ID TEXT PRIMARY KEY,
    Financial_Year TEXT,
    Date_of_Fund_Release DATE,
    State TEXT,
    District TEXT,
    Department TEXT,
    Scheme_Name TEXT,
    Scheme_Code TEXT,
    Fund_Source TEXT,
    Implementing_Agency TEXT,
    Sanctioned_Amount_Lakhs NUMERIC,
    Fund_Released_Lakhs NUMERIC,
    Fund_Utilized_Lakhs NUMERIC,
    Utilization_Percent NUMERIC,
    Physical_Target_Units NUMERIC,
    Physical_Achievement_Units NUMERIC,
    Beneficiaries_Target NUMERIC,
    Beneficiaries_Covered NUMERIC,
    Status TEXT,
    Audit_Remarks TEXT,
    Nodal_Officer_Contact TEXT
);
