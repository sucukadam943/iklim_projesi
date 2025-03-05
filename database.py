import os
import streamlit as st
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# Bağlantı havuzu oluşturma
@st.cache_resource
def create_pool():
    try:
        return SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=os.environ.get("DATABASE_URL", ""),
            cursor_factory=RealDictCursor
        )
    except psycopg2.Error as e:
        st.error(f"Veritabanı bağlantı havuzu oluşturma hatası: {e}")
        return None

# Bağlantı yönetici
@contextmanager
def get_connection():
    pool = create_pool()
    if pool is None:
        raise Exception("Veritabanı bağlantı havuzu oluşturulamadı")

    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)

def run_query(query, params=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cur.fetchall()
                conn.commit()
                return True
    except Exception as e:
        st.error(f"Sorgu hatası: {e}")
        return None

# Tablo oluşturma fonksiyonu
def create_tables():
    try:
        # Proje fikirleri tablosu
        run_query("""
        CREATE TABLE IF NOT EXISTS proje_fikirleri (
            id SERIAL PRIMARY KEY,
            baslik TEXT NOT NULL,
            aciklama TEXT NOT NULL,
            kategori TEXT NOT NULL,
            kullanici TEXT NOT NULL,
            tarih DATE DEFAULT CURRENT_DATE
        )
        """)

        # Karbon ayak izi hesaplamaları tablosu
        run_query("""
        CREATE TABLE IF NOT EXISTS karbon_hesaplamalari (
            id SERIAL PRIMARY KEY,
            kullanici TEXT NOT NULL,
            ulasim_puani FLOAT NOT NULL,
            enerji_puani FLOAT NOT NULL,
            beslenme_puani FLOAT NOT NULL,
            toplam_puan FLOAT NOT NULL,
            tarih DATE DEFAULT CURRENT_DATE
        )
        """)

        # Forum yorumları tablosu
        run_query("""
        CREATE TABLE IF NOT EXISTS forum_yorumlari (
            id SERIAL PRIMARY KEY,
            baslik TEXT NOT NULL,
            yorum TEXT NOT NULL,
            kullanici TEXT NOT NULL,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        return True
    except Exception as e:
        st.error(f"Tablo oluşturma hatası: {e}")
        return False