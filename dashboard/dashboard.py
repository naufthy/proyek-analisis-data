import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Dashboard Analisis Kualitas Udara",
    page_icon="💨😷",
    layout="wide"
)


all_df = pd.read_csv('submission/dashboard/main_data.csv')
all_df['datetime'] = pd.to_datetime(all_df['datetime'])

st.title("💨Dashboard Analisis Kualitas Udara😷")

st.header("Bagaimana tren untuk polutan PM2.5?")
st.subheader("Pada bulan apa saja biasanya terjadi puncak polusi dan penurunan polusi paling signifikan?")

monthly_pm25_df = all_df.groupby(by=all_df['datetime'].dt.month)['PM2.5'].mean()
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
monthly_pm25_df.index = month_labels

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Bulan Polusi Tertinggi (PM2.5)", value="Desember", delta=f"{monthly_pm25_df.max():.2f} µg/m³")
with col2:
    st.metric(label="Bulan Polusi Terendah (PM2.5)", value="Agustus", delta=f"{monthly_pm25_df.min():.2f} µg/m³", delta_color="inverse")


fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(monthly_pm25_df.index, monthly_pm25_df.values, marker='o', color='black', label="PM2.5")
ax1.plot('Des', monthly_pm25_df.loc['Des'], marker='o', markersize=10, color='red')
ax1.plot('Agu', monthly_pm25_df.loc['Agu'], marker='o', markersize=10, color='green')
ax1.set_title('Rata-rata Tren Musiman PM2.5 di Semua Stasiun', fontsize=16)
ax1.set_xlabel('Bulan', fontsize=12)
ax1.set_ylabel('Rata-rata Konsentrasi PM2.5 (µg/m³)', fontsize=12)
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)


st.header("Stasiun mana yang memiliki jumlah hari dengan kategori 'Tidak Sehat' paling banyak?")
st.subheader("Perbandingan berdasarkan level PM10.")

kategori_bins = [0, 50, 150, float('inf')]
kategori_labels = ['Baik', 'Sedang', 'Tidak Sehat']
all_df['pm10_category'] = pd.cut(all_df['PM10'], bins=kategori_bins, labels=kategori_labels, right=True)

unhealthy_days = all_df[all_df['pm10_category'] =='Tidak Sehat']

station_ranking = unhealthy_days['station'].value_counts().sort_values()

fig2, ax2 = plt.subplots(figsize=(12, 4))
colors = ['pink'] * len(station_ranking)
colors[-1] = 'red'
station_ranking.plot(kind='barh', color=colors, ax=ax2)
ax2.set_title("Peringkat Stasiun Berdasarkan Jumlah Hari 'Tidak Sehat'", fontsize=16)
ax2.set_ylabel('Stasiun', fontsize=12)
ax2.set_xlabel('Jumlah Hari dengan Kategori "Tidak Sehat"', fontsize=12)
plt.tight_layout()
st.pyplot(fig2)

st.caption("Dashboard dibuat berdasarkan Proyek Analisis Data oleh Tubagus Naufal Fathurahman.")
