import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGS = REPORTS / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(ROOT / "data" / "processed" / "government_scheme_features.csv")

# Financials by Year - bar (already exists)
fy = df.groupby('Financial_Year').agg({'Sanctioned_Amount_Lakhs':'sum','Fund_Released_Lakhs':'sum','Fund_Utilized_Lakhs':'sum'}).reset_index()
plt.figure(figsize=(10,5))
fy.plot(x='Financial_Year', kind='bar', stacked=False, color=['#1f77b4','#ff7f0e','#2ca02c'])
plt.ylabel('Amount (Lakhs)')
plt.title('Sanctioned / Released / Utilized by Financial Year')
plt.tight_layout()
plt.savefig(FIGS / 'sanctioned_released_utilized_by_fy.png')
plt.close()

# Utilization ratio distribution - histogram
plt.figure(figsize=(8,4))
sns.histplot(df['Fund_Utilization_Ratio'].dropna(), bins=20, kde=True)
plt.xlabel('Fund Utilization Ratio (%)')
plt.title('Distribution of Fund Utilization Ratio')
plt.tight_layout()
plt.savefig(FIGS / 'utilization_ratio_distribution.png')
plt.close()

# Top schemes pie (top 6)
top = df.groupby('Scheme_Name')['Sanctioned_Amount_Lakhs'].sum().nlargest(6)
plt.figure(figsize=(6,6))
top.plot.pie(autopct='%1.1f%%', startangle=140)
plt.ylabel('')
plt.title('Top 6 Schemes by Sanctioned Amount (%)')
plt.tight_layout()
plt.savefig(FIGS / 'top_schemes_pie.png')
plt.close()

# State funded bar - top 10
state = df.groupby('State')['Sanctioned_Amount_Lakhs'].sum().nlargest(10)
plt.figure(figsize=(10,5))
sns.barplot(x=state.values, y=state.index, palette='viridis')
plt.xlabel('Sanctioned Amount (Lakhs)')
plt.title('Top 10 States by Sanctioned Amount')
plt.tight_layout()
plt.savefig(FIGS / 'top_states_sanctioned.png')
plt.close()

print('Figures generated in', FIGS)
