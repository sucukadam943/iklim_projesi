import streamlit as st
import plotly.express as px
import pandas as pd
from utils import local_css, stat_card

local_css("styles.css")

st.title("İklim Değişikliği İstatistikleri")

# Örnek veri setleri
yillar = list(range(1990, 2024))
sicaklik_artisi = [round(0.2 * (i - 1990) + 13.5, 1) for i in yillar]
emisyon_degerleri = [round(2 * (i - 1990) + 300, 1) for i in yillar]

# İstatistik kartları
col1, col2, col3 = st.columns(3)
with col1:
    stat_card("1.1°C", "Küresel Sıcaklık Artışı (1850'den beri)")
with col2:
    stat_card("419 ppm", "Atmosferik CO₂ Seviyesi")
with col3:
    stat_card("3.3 mm/yıl", "Deniz Seviyesi Yükselme Hızı")

st.markdown("### Sıcaklık Değişimi Trendi")
df_sicaklik = pd.DataFrame({
    'Yıl': yillar,
    'Sıcaklık (°C)': sicaklik_artisi
})

fig_sicaklik = px.line(
    df_sicaklik, 
    x='Yıl', 
    y='Sıcaklık (°C)',
    title='Yıllara Göre Ortalama Sıcaklık Değişimi'
)
st.plotly_chart(fig_sicaklik, use_container_width=True)

st.markdown("### Sera Gazı Emisyonları")
df_emisyon = pd.DataFrame({
    'Yıl': yillar,
    'CO₂ Emisyonu (Mt)': emisyon_degerleri
})

fig_emisyon = px.bar(
    df_emisyon,
    x='Yıl',
    y='CO₂ Emisyonu (Mt)',
    title='Yıllık CO₂ Emisyonları'
)
st.plotly_chart(fig_emisyon, use_container_width=True)
