import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


file_path = os.path.join(os.path.dirname(__file__), "all_data.csv")
all_df = pd.read_csv(file_path)


datetime_columns = ["date"]
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    st.title("Yoel")
    # Menambahkan logo perusahaan
    st.image("https://seeklogo.com/images/S/streamlit-logo-1A3B208AE4-seeklogo.com.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Date Filter',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.header('Air Quality Dashboard :sparkles:')

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]


total_days = main_df.shape[0]
avg_pm25 = main_df['PM2.5'].mean()
avg_pm10 = main_df['PM10'].mean()
avg_no2 = main_df['NO2'].mean()

st.subheader("Daily Air Quality Index")


col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Days", value=total_days)
col2.metric(label="Average PM2.5", value=f"{avg_pm25:.2f} µg/m³")
col3.metric(label="Average PM10", value=f"{avg_pm10:.2f} µg/m³")
col4.metric(label="Average NO2", value=f"{avg_no2:.2f} µg/m³")


st.subheader("Tren PM2.5 di Setiap Stasiun")
groupByYear = main_df.groupby(["year", "station"])["PM2.5"].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=groupByYear, x="year", y="PM2.5", hue="station", marker="o", linewidth=2)
plt.title("Tren Rata-rata PM2.5 per Tahun di Setiap Stasiun", fontsize=14)
plt.xlabel("Tahun", fontsize=12)
plt.ylabel("PM2.5 (µg/m³)", fontsize=12)
plt.grid(True)
plt.legend(title="Stasiun")


st.pyplot(plt)

st.subheader("Rata-rata PM2.5 per Musim ")
pollution_colors = ["green", "yellow", "orange", "red", "purple", "brown"]
pollution_levels = ["Good", "Moderate", "Unhealthy (Sensitive)", "Unhealthy", "Very Unhealthy", "Dangerous"]
groupBySeason = main_df.groupby(["Season", "Polusi_Level"]).size().reset_index(name="count")
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=groupBySeason, x="Season", y="count", hue="Polusi_Level" ,hue_order=pollution_levels , palette=pollution_colors)
plt.title("Status Polusi Berdasarkan Musim", fontsize=14)
plt.xlabel("Musim", fontsize=12)
plt.ylabel("Jumlah Hari", fontsize=12)
plt.legend(title="Status Polusi", bbox_to_anchor=(1, 1), loc="upper left")
plt.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(plt)



st.subheader("PM2.5 Polution")
groupByYear = main_df.groupby("date").mean(numeric_only=True)
fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["PM2.5"], label="PM2.5")
plt.xlabel("Year")
plt.ylabel("Concentration (microgram/m3)")
plt.legend()
st.pyplot(fig)

st.subheader("PM10 Polution")
fig = plt.figure(figsize=(10,6))
plt.plot(groupByYear.index, groupByYear["PM10"], label="PM10")
plt.xlabel("Year")
plt.ylabel("Concentration (microgram/m3)")
plt.legend()
st.pyplot(fig)

st.subheader("Faktor apa yang paling mempengaruhi lonjakan polusi udara")
corr_matrix = main_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True,  fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

numeric_data = main_df.select_dtypes(include=['number'])
corr_pm25 = numeric_data.corr()["PM2.5"].drop("PM2.5").sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
ax = sns.barplot(x=corr_pm25.index, y=corr_pm25.values, palette="coolwarm")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", 
                (p.get_x() + p.get_width() / 2, p.get_height()), 
                ha="center", va="bottom", fontsize=10)
    
ax.set_title("Correlation of Factors with PM2.5", fontsize=14, fontweight='bold')
ax.set_ylabel("Koefisien Korelasi", fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
ax.axhline(0, color="black", linestyle="--", alpha=0.7, linewidth=1)
ax.grid(axis="y", linestyle="--", alpha=0.5)
st.pyplot(fig)

st.subheader("Comparison with WHO Standard")
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(["WHO Standard", "Current Data"], [25, avg_pm25], )
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title("Comparison with WHO Standard")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(groupByYear.index, groupByYear['PM2.5'], alpha=0.6, label="PM2.5")
ax.plot(groupByYear.index, groupByYear['PM10'],color='red', alpha=0.6, label="PM10")

st.subheader("Top 5 Worst Air Quality Days")
top_days = main_df.nlargest(5, 'PM2.5')[['date','station', 'PM2.5']]
st.table(top_days)

