
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from utils import local_css, image_with_caption, info_card

local_css("styles.css")

st.title("İklim Haberleri ve Güncel Veriler")

st.markdown("""
    Dünya genelindeki iklim değişikliği ile ilgili güncel haberleri ve verileri takip edin.
    Bu sayfa, çeşitli API'ler ve haber kaynaklarından toplanan bilgileri içerir.
""")

# Demo haberler (gerçek API bağlantıları için API key gerekir)
haberler = [
    {
        "baslik": "BM İklim Zirvesi: Ülkeler Yeni Emisyon Hedeflerini Açıkladı",
        "ozet": "Birleşmiş Milletler İklim Değişikliği Konferansı'nda ülkeler, karbon emisyonlarını azaltmak için yeni taahhütlerde bulundu.",
        "kaynak": "İklim Haberleri",
        "tarih": "2023-12-15",
        "resim": "https://images.unsplash.com/photo-1532187643603-ba119ca4109e"
    },
    {
        "baslik": "Arktik Buz Örtüsü Rekor Seviyede Azaldı",
        "ozet": "Bilim insanları, Arktik bölgedeki buz örtüsünün son 40 yılın en düşük seviyesine ulaştığını açıkladı.",
        "kaynak": "Bilim ve Çevre",
        "tarih": "2023-11-30",
        "resim": "https://images.unsplash.com/photo-1476455553758-5a8b16727e20"
    },
    {
        "baslik": "Yenilenebilir Enerji Yatırımları Artıyor",
        "ozet": "Küresel ölçekte yenilenebilir enerji yatırımları geçen yıla göre %30 artış gösterdi.",
        "kaynak": "Enerji Gündem",
        "tarih": "2023-12-05",
        "resim": "https://images.unsplash.com/photo-1508514177221-188b1cf16e9d"
    },
    {
        "baslik": "Türkiye'nin İklim Eylem Planı Güncellendi",
        "ozet": "Çevre ve Şehircilik Bakanlığı, Türkiye'nin güncellenmiş iklim eylem planını açıkladı.",
        "kaynak": "Ulusal Çevre",
        "tarih": "2023-12-10",
        "resim": "https://images.unsplash.com/photo-1572204097183-e44e08240822"
    }
]

# Haberleri göster
st.subheader("Güncel İklim Haberleri")

for i, haber in enumerate(haberler):
    with st.expander(f"{haber['baslik']} - {haber['tarih']}"):
        st.image(haber['resim'], caption=f"Kaynak: {haber['kaynak']}")
        st.markdown(f"**{haber['ozet']}**")
        st.markdown(f"*{haber['kaynak']} - {haber['tarih']}*")
        
        # Demo için haber detayı
        st.markdown("""
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """)
        
        if st.button(f"Haberi Kaydet", key=f"save_{i}"):
            st.success("Haber kaydedildi!")

# İklim verileri (Demo)
st.subheader("Güncel İklim Verileri")

tab1, tab2 = st.tabs(["Küresel Sıcaklık", "CO2 Emisyonları"])

with tab1:
    st.markdown("### Küresel Sıcaklık Anomalisi")
    
    st.markdown("""
    Son 12 ayın küresel sıcaklık anomalisi verileri (°C)
    *Kaynak: NASA GISS*
    """)
    
    # Demo veri
    son_12_ay = [(datetime.now() - timedelta(days=30*i)).strftime("%Y-%m") for i in range(12)]
    sicaklik_anomalileri = [0.92, 0.97, 0.94, 0.89, 0.91, 0.88, 0.85, 0.82, 0.80, 0.79, 0.81, 0.78]
    
    sicaklik_df = pd.DataFrame({
        "Ay": son_12_ay[::-1],
        "Anomali (°C)": sicaklik_anomalileri
    })
    
    st.line_chart(sicaklik_df.set_index("Ay"))
    
    st.info("Sıcaklık anomalisi, bir bölgenin sıcaklığının uzun vadeli ortalamadan ne kadar saptığını gösterir.")

with tab2:
    st.markdown("### Atmosferik CO2 Konsantrasyonu")
    
    st.markdown("""
    Son 12 ayın atmosferik CO2 konsantrasyonu (ppm)
    *Kaynak: NOAA*
    """)
    
    # Demo veri
    co2_seviyeleri = [417.2, 416.8, 416.5, 416.1, 415.7, 415.0, 414.5, 414.0, 413.7, 413.2, 412.8, 412.5]
    
    co2_df = pd.DataFrame({
        "Ay": son_12_ay[::-1],
        "CO2 (ppm)": co2_seviyeleri
    })
    
    st.line_chart(co2_df.set_index("Ay"))
    
    st.info("CO2 konsantrasyonu 280 ppm'den (sanayi devrimi öncesi) 419 ppm'e (2023) yükselmiştir.")

# İklim API aracı
st.markdown("---")
st.subheader("İklim Veri Aracı")

st.markdown("""
Bu araç ile belirli bir konum için güncel iklim verilerini görüntüleyebilirsiniz.
""")

col1, col2 = st.columns(2)

with col1:
    lokasyon = st.text_input("Şehir adı girin:", "İstanbul")
    
with col2:
    veri_tipi = st.selectbox(
        "Veri tipi seçin:",
        ["Sıcaklık Verileri", "Hava Kalitesi", "İklim Projeksiyonları"]
    )

if st.button("Verileri Getir"):
    with st.spinner("Veriler getiriliyor..."):
        # Demo veri (gerçek API bağlantısı için API key gerekir)
        st.success(f"{lokasyon} için {veri_tipi} getirildi!")
        
        if veri_tipi == "Sıcaklık Verileri":
            st.markdown(f"### {lokasyon} Sıcaklık Verileri")
            
            sicaklik_data = {
                "Yıl": list(range(1980, 2024, 5)),
                "Ortalama Sıcaklık (°C)": [13.2, 13.5, 13.8, 14.1, 14.5, 14.9, 15.2, 15.7, 16.0]
            }
            
            sicaklik_df = pd.DataFrame(sicaklik_data)
            st.line_chart(sicaklik_df.set_index("Yıl"))
            
            st.info(f"{lokasyon} için ortalama sıcaklık artışı son 40 yılda 2.8°C olmuştur.")
            
        elif veri_tipi == "Hava Kalitesi":
            st.markdown(f"### {lokasyon} Hava Kalitesi İndeksi")
            
            st.metric(label="Güncel Hava Kalitesi İndeksi", value="72", delta="3")
            st.markdown("*Hava Kalitesi Değerlendirmesi: Orta*")
            
            st.markdown("""
            - PM2.5: 18 µg/m³
            - PM10: 35 µg/m³
            - Ozon (O3): 45 ppb
            - Azot Dioksit (NO2): 22 ppb
            """)
            
        else:
            st.markdown(f"### {lokasyon} İklim Projeksiyonları (2050)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Tahmini Sıcaklık Artışı", value="2.4°C", delta="1.1°C")
                st.metric(label="Yağış Değişimi", value="-5%", delta="-12%")
                
            with col2:
                st.metric(label="Aşırı Sıcak Günler", value="32 gün/yıl", delta="18")
                st.metric(label="Kuraklık Riski", value="Yüksek", delta="Artış")

# Farkındalık ve Eğitim
st.markdown("---")
info_card(
    "İklim Değişikliği Takibi",
    "Güncel haberleri ve verileri takip ederek iklim değişikliği hakkında bilgi sahibi olmak, "
    "sürdürülebilir bir gelecek için atılacak adımların ilk basamağıdır."
)
