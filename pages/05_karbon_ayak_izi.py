
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import local_css, info_card, stat_card
from database import run_query, create_tables

local_css("styles.css")

st.title("Karbon Ayak İzi Hesaplayıcı")

st.markdown("""
    Günlük alışkanlıklarınız ve tercihleriniz doğrultusunda karbon ayak izinizi hesaplayın.
    Bu hesaplama, çevresel etkilerinizi anlamanıza ve azaltmanıza yardımcı olabilir.
""")

# Veritabanı tablolarını oluştur
create_tables()

# Kullanıcı bilgileri
kullanici_adi = st.text_input("İsminiz")

# Hesaplama formu
with st.form("karbon_hesaplama_formu"):
    st.subheader("Ulaşım Alışkanlıkları")
    
    ulasim_tipi = st.selectbox(
        "Genellikle hangi ulaşım aracını kullanıyorsunuz?",
        ["Otomobil (Benzin/Dizel)", "Otomobil (Hibrit)", "Otomobil (Elektrikli)", "Toplu Taşıma", "Motosiklet", "Bisiklet/Yürüyüş"]
    )
    
    ulasim_mesafe = st.slider("Haftada ortalama kaç km yol yapıyorsunuz?", 0, 500, 100)
    
    st.subheader("Ev & Enerji Kullanımı")
    
    ev_tipi = st.selectbox(
        "Yaşadığınız ev tipi:",
        ["Apartman Dairesi", "Müstakil Ev", "Villa"]
    )
    
    enerji_kaynaklari = st.multiselect(
        "Evinizde kullandığınız enerji kaynakları:",
        ["Doğalgaz", "Elektrik", "Kömür", "Odun", "Güneş Enerjisi"]
    )
    
    elektrik_tuketimi = st.slider("Aylık ortalama elektrik tüketiminiz (kWh):", 0, 1000, 200)
    
    st.subheader("Beslenme Alışkanlıkları")
    
    et_tuketimi = st.select_slider(
        "Et tüketim sıklığınız:",
        options=["Hiç (Vegan)", "Nadiren", "Haftada 1-2 kez", "Haftada 3-5 kez", "Her gün"]
    )
    
    yerel_gida = st.slider("Tükettiğiniz gıdaların ne kadarı yerel kaynaklı? (%)", 0, 100, 30)
    
    hesapla_butonu = st.form_submit_button("Karbon Ayak İzimi Hesapla")
    
    if hesapla_butonu and kullanici_adi:
        # Ulaşım puanı hesaplama
        ulasim_carpani = {
            "Otomobil (Benzin/Dizel)": 1.0,
            "Otomobil (Hibrit)": 0.6,
            "Otomobil (Elektrikli)": 0.4,
            "Toplu Taşıma": 0.3,
            "Motosiklet": 0.5,
            "Bisiklet/Yürüyüş": 0.0
        }
        
        ulasim_puani = (ulasim_carpani[ulasim_tipi] * ulasim_mesafe) / 10
        
        # Enerji puanı hesaplama
        ev_carpani = {"Apartman Dairesi": 0.7, "Müstakil Ev": 1.0, "Villa": 1.3}
        enerji_carpani = 0.0
        
        for kaynak in enerji_kaynaklari:
            if kaynak == "Doğalgaz":
                enerji_carpani += 0.7
            elif kaynak == "Elektrik":
                enerji_carpani += 0.8
            elif kaynak == "Kömür":
                enerji_carpani += 1.2
            elif kaynak == "Odun":
                enerji_carpani += 0.9
            elif kaynak == "Güneş Enerjisi":
                enerji_carpani -= 0.3
        
        enerji_puani = (ev_carpani[ev_tipi] * enerji_carpani * elektrik_tuketimi) / 100
        
        # Beslenme puanı hesaplama
        et_carpani = {
            "Hiç (Vegan)": 0.2,
            "Nadiren": 0.4,
            "Haftada 1-2 kez": 0.6,
            "Haftada 3-5 kez": 0.8,
            "Her gün": 1.0
        }
        
        yerel_gida_etkisi = 1 - (yerel_gida / 100)
        beslenme_puani = et_carpani[et_tuketimi] * (1 + yerel_gida_etkisi) * 10
        
        # Toplam puan
        toplam_puan = ulasim_puani + enerji_puani + beslenme_puani
        
        # Veritabanına kaydet
        result = run_query(
            "INSERT INTO karbon_hesaplamalari (kullanici, ulasim_puani, enerji_puani, beslenme_puani, toplam_puan) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (kullanici_adi, ulasim_puani, enerji_puani, beslenme_puani, toplam_puan)
        )
        
        # Sonuçları göster
        st.success(f"Karbon ayak izi hesaplamanız tamamlandı, {kullanici_adi}!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            stat_card(f"{ulasim_puani:.1f}", "Ulaşım Puanı")
        with col2:
            stat_card(f"{enerji_puani:.1f}", "Enerji Puanı")
        with col3:
            stat_card(f"{beslenme_puani:.1f}", "Beslenme Puanı")
            
        st.subheader("Toplam Karbon Ayak İzi Puanınız")
        
        # Puan skalası
        if toplam_puan < 10:
            sonuc_mesaji = "Harika! Karbon ayak iziniz oldukça düşük."
            renk = "green"
        elif toplam_puan < 20:
            sonuc_mesaji = "İyi! Karbon ayak iziniz ortalamanın altında."
            renk = "lightgreen"
        elif toplam_puan < 30:
            sonuc_mesaji = "Ortalama bir karbon ayak izine sahipsiniz."
            renk = "yellow"
        elif toplam_puan < 40:
            sonuc_mesaji = "Karbon ayak iziniz ortalamanın üstünde."
            renk = "orange"
        else:
            sonuc_mesaji = "Karbon ayak iziniz yüksek. Azaltmak için adımlar atabilirsiniz."
            renk = "red"
        
        st.markdown(f"""
        <div style="background-color: {renk}; padding: 20px; border-radius: 10px; text-align: center;">
            <h1 style="color: white;">{toplam_puan:.1f}</h1>
            <p style="color: white;">{sonuc_mesaji}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Grafik
        fig = px.pie(
            values=[ulasim_puani, enerji_puani, beslenme_puani],
            names=["Ulaşım", "Enerji", "Beslenme"],
            title="Karbon Ayak İzi Dağılımı"
        )
        st.plotly_chart(fig)
        
        # Öneriler
        st.subheader("Karbon Ayak İzinizi Azaltmak İçin Öneriler")
        
        if ulasim_puani > 5:
            info_card(
                "Ulaşım Önerileri",
                "Toplu taşıma kullanmayı, bisiklete binmeyi veya yürümeyi tercih edin. "
                "Mümkünse araç paylaşımı yapın veya elektrikli araçlara geçmeyi düşünün."
            )
            
        if enerji_puani > 5:
            info_card(
                "Enerji Kullanımı Önerileri",
                "Enerji verimli cihazlar kullanın, gereksiz yanan ışıkları kapatın, "
                "mümkünse yenilenebilir enerji kaynaklarına geçiş yapın."
            )
            
        if beslenme_puani > 5:
            info_card(
                "Beslenme Önerileri",
                "Et tüketiminizi azaltın, yerel ve mevsimsel gıdaları tercih edin, "
                "gıda israfından kaçının."
            )
    
    elif hesapla_butonu and not kullanici_adi:
        st.warning("Lütfen isminizi giriniz.")

# Ortalama istatistikler (Demo verisi)
st.markdown("---")
st.subheader("Topluluk İstatistikleri")

# Veritabanından ortalama veriler alınabilir
# Şimdilik demo verisi kullanıyoruz
demo_veri = {
    "Kategoriler": ["Ulaşım", "Enerji", "Beslenme"],
    "Ortalama Puanlar": [12.3, 15.7, 8.2]
}

fig = px.bar(
    demo_veri,
    x="Kategoriler",
    y="Ortalama Puanlar",
    title="Topluluk Karbon Ayak İzi Ortalamaları"
)
st.plotly_chart(fig)
