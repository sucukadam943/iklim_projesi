import streamlit as st
from utils import local_css, info_card

local_css("styles.css")

st.title("İklim Değişikliği ile Mücadele")

st.markdown("""
    İklim değişikliği ile mücadelede hem bireysel hem de toplumsal düzeyde yapabileceğimiz 
    birçok şey var. İşte bazı önemli adımlar:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Bireysel Çözümler")
    
    st.markdown("""
    <div class="tip-card">
        <h4>🚶‍♂️ Ulaşım</h4>
        <ul>
            <li>Toplu taşıma kullanın</li>
            <li>Bisiklet veya yürüyüş tercih edin</li>
            <li>Elektrikli araçlara geçiş yapın</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tip-card">
        <h4>🏠 Ev ve Enerji</h4>
        <ul>
            <li>Enerji tasarruflu cihazlar kullanın</li>
            <li>Yenilenebilir enerji tercih edin</li>
            <li>İzolasyon yaptırın</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Toplumsal Çözümler")
    
    st.markdown("""
    <div class="tip-card">
        <h4>🌱 Sürdürülebilirlik</h4>
        <ul>
            <li>Geri dönüşüm yapın</li>
            <li>Tek kullanımlık ürünlerden kaçının</li>
            <li>Yerel ve mevsimsel gıdalar tüketin</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tip-card">
        <h4>📢 Farkındalık</h4>
        <ul>
            <li>İklim değişikliği hakkında bilgi edinin</li>
            <li>Çevrenizdekileri bilinçlendirin</li>
            <li>Çevre projelerine destek olun</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Sürdürülebilir Yaşam İpuçları")

info_card(
    "Enerji Tasarrufu",
    "Kullanmadığınız elektronik cihazları kapatın, LED ampuller kullanın ve doğal "
    "aydınlatmadan maksimum faydalanın."
)

info_card(
    "Su Tasarrufu",
    "Daha kısa duş alın, damlatmayan muslukları tamir edin ve yağmur suyunu biriktirin."
)

info_card(
    "Atık Yönetimi",
    "Atıklarınızı ayrıştırın, kompost yapın ve tekrar kullanılabilir ürünleri tercih edin."
)
