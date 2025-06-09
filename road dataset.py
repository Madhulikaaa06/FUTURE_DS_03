import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 21)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_excel("roadaccidentdataset.xlsx")
print(df)

import plotly.express as px

# Group by location and count accidents
hotspots = df.groupby(['Latitude', 'Longitude']).size().reset_index(name='Accident_Count')

# Top 100 hotspots
top_hotspots = hotspots.sort_values(by='Accident_Count', ascending=False).head(100)

# Plot on map
fig = px.scatter_mapbox(
    top_hotspots, lat='Latitude', lon='Longitude', size='Accident_Count',
    color='Accident_Count', zoom=10, mapbox_style="carto-positron",
    title='Top 100 Accident Hotspots'
)
fig.show()

df['Accident Date'] = pd.to_datetime(df['Accident Date'])
severity_trend = df.groupby([df['Accident Date'].dt.to_period('M'), 'Accident_Severity']).size().unstack().fillna(0)

# Plot
severity_trend.index = severity_trend.index.astype(str)
severity_trend.plot(kind='line', figsize=(12,6), title='Monthly Accident Severity Trend')

cause_cols = ['Weather_Conditions', 'Light_Conditions', 'Road_Surface_Conditions']

for col in cause_cols:
    print(f"\nTop causes - {col}")
    print(df[col].value_counts().head())

df['Hour'] = pd.to_datetime(df['Time'], errors='coerce').dt.hour
heatmap_data = df.groupby(['Day_of_Week', 'Hour']).size().unstack().fillna(0)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ensure 'Time' is parsed correctly
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.hour

# Fill any missing hours with a placeholder if needed
df['Day_of_Week'] = df['Day_of_Week'].fillna('Unknown')

# Create pivot table for heatmap
heatmap_data = df.groupby(['Day_of_Week', 'Hour']).size().unstack().fillna(0)

# Sort the days
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = heatmap_data.reindex(day_order)

# Plot
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd", annot=True, fmt=".0f")
plt.title("Accidents Heatmap by Day and Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week")
plt.tight_layout()
plt.show()


