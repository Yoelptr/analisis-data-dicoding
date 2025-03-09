import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from babel.numbers import format_currency
sns.set(style='dark')

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

st.subheader("Air Quality Correlation Matrix")


corr_matrix = main_df.select_dtypes(include=['number']).corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.subheader("Comparison with WHO Standard")
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(["WHO Standard", "Current Data"], [25, avg_pm25], color=["green", "red"])
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title("Comparison with WHO Standard")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(groupByYear.index, groupByYear['PM2.5'], alpha=0.6, label="PM2.5")
ax.plot(groupByYear.index, groupByYear['PM10'],color='red', alpha=0.6, label="PM10")

st.subheader("Top 5 Worst Air Quality Days")
top_days = main_df.nlargest(5, 'PM2.5')[['date','station', 'PM2.5']]
st.table(top_days)

