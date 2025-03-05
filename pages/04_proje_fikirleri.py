import streamlit as st
import pandas as pd
from utils import local_css, info_card
from database import run_query, create_tables
import time

local_css("styles.css")

st.title("İklim Projeleri")

st.markdown("""
    İklim değişikliğiyle mücadele için proje fikirlerinizi paylaşın veya başkalarının 
    fikirlerinden ilham alın. Birlikte daha büyük bir etki yaratabiliriz!
""")

# Veritabanı tablolarını oluştur
if not create_tables():
    st.error("Veritabanı tabloları oluşturulurken bir hata oluştu.")
    st.stop()

# Sekmeler
tab1, tab2 = st.tabs(["Proje Fikirleri", "Yeni Proje Ekle"])

with tab1:
    st.header("Topluluk Proje Fikirleri")

    try:
        # Filtreleme
        kategoriler = ["Tümü", "Enerji", "Geri Dönüşüm", "Su Tasarrufu", "Yeşillendirme", "Eğitim", "Diğer"]
        secilen_kategori = st.selectbox("Kategori Filtrele:", kategoriler)

        # Veritabanından proje fikirlerini çek
        if secilen_kategori == "Tümü":
            projeler = run_query("SELECT * FROM proje_fikirleri ORDER BY tarih DESC")
        else:
            projeler = run_query(
                "SELECT * FROM proje_fikirleri WHERE kategori = %s ORDER BY tarih DESC",
                (secilen_kategori,)
            )

        if projeler is None:
            st.error("Proje fikirleri yüklenirken bir hata oluştu.")
        elif not projeler:
            st.info("Henüz hiç proje fikri paylaşılmamış. İlk fikri siz ekleyin!")
        else:
            for proje in projeler:
                with st.expander(f"{proje['baslik']} - {proje['kullanici']} ({proje['tarih']})"):
                    st.markdown(f"**Kategori:** {proje['kategori']}")
                    st.markdown(f"**Açıklama:** {proje['aciklama']}")
                    st.markdown(f"__{proje['kullanici']} tarafından {proje['tarih']} tarihinde paylaşıldı__")

                    # Beğeni butonu
                    if st.button(f"👍 Beğen", key=f"like_{proje['id']}"):
                        st.balloons()
                        st.success("Proje fikri beğenildi!")

    except Exception as e:
        st.error(f"Bir hata oluştu: {str(e)}")

with tab2:
    st.header("Yeni Proje Fikri Ekle")

    with st.form("proje_formu"):
        proje_baslik = st.text_input("Proje Başlığı")
        proje_aciklama = st.text_area("Proje Açıklaması")
        proje_kategori = st.selectbox(
            "Kategori",
            ["Enerji", "Geri Dönüşüm", "Su Tasarrufu", "Yeşillendirme", "Eğitim", "Diğer"]
        )
        kullanici_adi = st.text_input("İsminiz")

        submitted = st.form_submit_button("Fikrinizi Paylaşın")

        if submitted:
            if not all([proje_baslik, proje_aciklama, kullanici_adi]):
                st.warning("Lütfen tüm alanları doldurunuz.")
            else:
                try:
                    # Veritabanına kaydet
                    result = run_query(
                        """
                        INSERT INTO proje_fikirleri (baslik, aciklama, kategori, kullanici)
                        VALUES (%s, %s, %s, %s) RETURNING id
                        """,
                        (proje_baslik, proje_aciklama, proje_kategori, kullanici_adi)
                    )

                    if result:
                        st.success("Proje fikriniz başarıyla kaydedildi!")
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                    else:
                        st.error("Proje kaydedilirken bir hata oluştu.")
                except Exception as e:
                    st.error(f"Proje kaydedilirken bir hata oluştu: {str(e)}")

st.markdown("---")
info_card(
    "Nasıl Katkıda Bulunabilirsiniz?",
    "Fikirlerinizi paylaşın, başkalarının fikirlerini inceleyin ve beğendiğiniz projelere destek olun. "
    "Unutmayın, küçük adımlar büyük değişimlere yol açabilir!"
)