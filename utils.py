import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def image_with_caption(url, caption):
    st.image(url, caption=caption, use_column_width=True)

def info_card(title, content):
    st.markdown(f"""
    <div class="info-card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def stat_card(number, label):
    st.markdown(f"""
    <div class="stat-card">
        <h2>{number}</h2>
        <p>{label}</p>
    </div>
    """, unsafe_allow_html=True)
