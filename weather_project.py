# WEATHER DATA ANALYSIS 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

# Task 1
df = pd.read_csv("hrly_Irish_weather.csv", low_memory=False)

df['date'] = pd.to_datetime(df['date'], format="%d-%b-%Y %H:%M", errors="coerce")
print("\n=== HEAD ===")
print(df.head())
print("\n=== INFO ===")
print(df.info())
print("\n=== DESCRIBE ===")
print(df.describe())

#Task 2 - Data cleaning
numeric_cols = ['rain', 'temp', 'wetb', 'dewpt', 'vappr', 'rhum', 'msl',
                'wdsp', 'wddir', 'sun', 'vis', 'clht', 'clamt']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].mean())

df_clean = df[['date', 'temp', 'rain', 'rhum']]
print("\n=== CLEANED DATA SAMPLE ===")
print(df_clean.head())


#Task 3 - Grouping and aggregation
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

daily_mean = df.groupby(['year', 'month', 'day'])['temp'].mean()
monthly_mean = df.groupby(['year', 'month'])['temp'].mean()
yearly_mean = df.groupby(['year'])['temp'].mean()

print("\nDaily Temperature Mean:\n", daily_mean.head())
print("\nMonthly Temperature Mean:\n", monthly_mean.head())
print("\nYearly Temperature Mean:\n", yearly_mean.head())

#Task - 4 Visualization
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['temp'])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()

monthly_rainfall = df.groupby(df['date'].dt.month)['rain'].sum()
plt.figure(figsize=(8, 4))
plt.bar(monthly_rainfall.index, monthly_rainfall.values)
plt.title("Monthly Rainfall Totals")
plt.xlabel("Month")
plt.ylabel("Rain (mm)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 5))
plt.scatter(df['temp'], df['rhum'])
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].plot(df['date'], df['temp'])
ax[0].set_title("Daily Temperature")
ax[1].scatter(df['temp'], df['rhum'])
ax[1].set_title("Humidity vs Temperature")
plt.tight_layout()
plt.show()


#Task 5 Seasonal Analysis
df = df.dropna(subset=['date'])
df.set_index('date', inplace=True)

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

df['season'] = df.index.month.map(get_season)

season_stats = df.groupby('season').agg({
    'temp': ['mean', 'min', 'max', 'std'],
    'rhum': ['mean', 'min', 'max', 'std'],
    'rain': 'sum'
})
print("\nSeasonal Statistics:\n", season_stats)

#Task 6 - Exporting report and plot

# Task 6 - Exporting report and plots


output_dir = "weather_outputs"
os.makedirs(output_dir, exist_ok=True)

# Save cleaned CSV
clean_csv_path = os.path.join(output_dir, "cleaned_weather_data.csv")
df_clean.to_csv(clean_csv_path, index=False)
print(f"Cleaned CSV saved at: {clean_csv_path}")

# Prepare variables for plotting
daily_temp = daily_mean          # Task 3 se
monthly_rain = df.groupby(df.index.month)['rain'].sum()
df_stats = df.reset_index()      # for scatterplot
temp_col = 'temp'
humidity_col = 'rhum'
date_col = 'date'

# Daily Temperature Trend
plt.figure(figsize=(12, 5))
plt.plot(daily_temp.index, daily_temp.values)
plt.title("Daily Temperature Trend")
plt.xlabel("Day")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_dir, "daily_temperature_trend.png"))
plt.close()

# Monthly Rainfall Total
plt.figure(figsize=(12, 5))
plt.bar(monthly_rain.index.astype(str), monthly_rain.values)
plt.title("Monthly Rainfall Total")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_dir, "monthly_rainfall.png"))
plt.close()

# Humidity vs Temperature
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_stats, x=temp_col, y=humidity_col)
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.savefig(os.path.join(output_dir, "humidity_vs_temperature.png"))
plt.close()

print("All CSV and plots saved successfully!")

# Generate Markdown report
report_path = os.path.join(output_dir, "Weather_Report.md")
with open(report_path, "w", encoding="utf-8") as report:
    report.write("# Weather Data Analysis Report\n\n")
    report.write("## Project Summary\n")
    report.write("This project analyzes real-world weather data to understand temperature, rainfall, and humidity patterns using Python.\n\n")

    report.write("## Key Insights\n")
    report.write(f"- Total records analyzed: **{len(df_clean)}**\n")
    report.write(f"- Temperature column used: **{temp_col}**\n")
    report.write(f"- Date range: **{df_stats[date_col].min().date()} → {df_stats[date_col].max().date()}**\n\n")

    report.write("## Temperature Trends\n")
    report.write("- Daily temperatures fluctuate across the dataset.\n")
    report.write("- Line plot saved as: `daily_temperature_trend.png`\n\n")

    report.write("## Rainfall Patterns\n")
    report.write("- Monthly rainfall varies significantly.\n")
    report.write("- Bar chart saved as: `monthly_rainfall.png`\n\n")

    report.write("## Humidity & Temperature Relationship\n")
    report.write("- Scatter plot shows correlation between humidity and temperature.\n")
    report.write("- Saved as: `humidity_vs_temperature.png`\n\n")

    report.write("## Seasonal Behavior\n")
    report.write("- Grouping by seasons shows how weather varies across Winter, Summer, Monsoon, and Post-Monsoon.\n\n")

    report.write("## Output Directory\n")
    report.write("All exported assets are saved in the **weather_outputs/** folder:\n")
    report.write("- Cleaned dataset CSV\n")
    report.write("- PNG visualizations\n")
    report.write("- Markdown report\n")


print(f"Report generated at: {report_path}")