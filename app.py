import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import os
import random

# ==========================================
# 1. TETAPAN HALAMAN (Gaya Kalodata - Wide)
# ==========================================
st.set_page_config(page_title="ResearchInsight Hub", page_icon="📈", layout="wide")

# ==========================================
# 2. KONFIGURASI GEMINI AI
# ==========================================
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# ==========================================
# 3. JANAAN DATA SIMULASI (Dummy Data)
# ==========================================
# Kita jana data secara automatik untuk memudahkan anda menguji UI
@st.cache_data
def load_data():
    data = {
        "Tajuk_Video": [
            "Cara Guna AI Untuk Assignment", "Bahaya Scam Telegram", 
            "Apa Itu Literasi Digital?", "Excel Hacks untuk Pelajar", 
            "Cara Buat Password Kuat", "Kenapa Kena Verify Akaun?",
            "Edit Video Pakai CapCut AI", "Jaga Privasi di TikTok"
        ],
        "Kategori": ["Pendidikan AI", "Keselamatan Siber", "Asas Digital", "Pendidikan AI", "Keselamatan Siber", "Asas Digital", "Pendidikan AI", "Keselamatan Siber"],
        "Gaya_Penyampaian": ["Impromptu", "Formal", "Impromptu", "Formal", "Impromptu", "Formal", "Impromptu", "Impromptu"],
        "Views": [120000, 85000, 45000, 210000, 150000, 30000, 320000, 95000],
        "Likes": [15000, 8000, 3000, 25000, 18000, 2000, 45000, 12000],
        "Comments": [450, 800, 150, 600, 1200, 100, 1500, 500],
        "Shares": [1200, 3000, 200, 4000, 5000, 150, 8000, 1100]
    }
    df = pd.DataFrame(data)
    # Kira Engagement Rate = ((Likes + Comments + Shares) / Views) * 100
    df["Engagement_Rate_%"] = round(((df["Likes"] + df["Comments"] + df["Shares"]) / df["Views"]) * 100, 2)
    return df

df = load_data()

# ==========================================
# 4. BAHAGIAN ATAS: HEADER & PENAPIS (FILTERS)
# ==========================================
st.title("📈 ResearchInsight Hub - TikTok Analytics")
st.markdown("Menganalisis Impak Video Pendidikan & Literasi Digital Komuniti")
st.markdown("---")

st.subheader("🔍 Penapis Pasaran (Market Filters)")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    filter_kategori = st.selectbox("Pilih Kategori Topik:", ["Semua"] + list(df["Kategori"].unique()))
with col_f2:
    filter_gaya = st.selectbox("Gaya Penyampaian:", ["Semua"] + list(df["Gaya_Penyampaian"].unique()))
with col_f3:
    susunan = st.radio("Susun Berdasarkan:", ["Views Tertinggi", "Engagement Tertinggi"], horizontal=True)

# Logik Penapisan Data
df_filtered = df.copy()
if filter_kategori != "Semua":
    df_filtered = df_filtered[df_filtered["Kategori"] == filter_kategori]
if filter_gaya != "Semua":
    df_filtered = df_filtered[df_filtered["Gaya_Penyampaian"] == filter_gaya]

if susunan == "Views Tertinggi":
    df_filtered = df_filtered.sort_values(by="Views", ascending=False)
else:
    df_filtered = df_filtered.sort_values(by="Engagement_Rate_%", ascending=False)

st.markdown("---")

# ==========================================
# 5. KAD KPI UTAMA (GAYA KALODATA)
# ==========================================
total_views = df_filtered["Views"].sum()
avg_engagement = round(df_filtered["Engagement_Rate_%"].mean(), 2)
total_shares = df_filtered["Shares"].sum()
top_video = df_filtered.iloc[0]["Tajuk_Video"] if not df_filtered.empty else "Tiada Data"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="👁️ Jumlah Keseluruhan Views", value=f"{total_views:,}")
with col2:
    st.metric(label="💬 Purata Engagement Rate", value=f"{avg_engagement}%")
with col3:
    st.metric(label="🚀 Jumlah Perkongsian (Virality)", value=f"{total_shares:,}")
with col4:
    st.metric(label="🏆 Video Paling Berprestasi", value=top_video)

st.markdown("---")

# ==========================================
# 6. STRUKTUR MAKLUMAT (TABS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 Ringkasan Kandungan", "🧑‍🏫 Analisis Gaya Penyampaian", "🤖 Kalodata AI Assistant"])

# --- TAB 1: RINGKASAN KANDUNGAN ---
with tab1:
    st.subheader("Top Video Mengikut Capaian (Reach)")
    col_chart1, col_table1 = st.columns([6, 4]) # Pecahan saiz lajur 60% dan 40%
    
    with col_chart1:
        # Carta Bar Melintang yang dibaiki
        fig_views = px.bar(
            df_filtered, 
            x='Views', 
            y='Tajuk_Video', 
            orientation='h',
            color='Engagement_Rate_%',
            color_continuous_scale='Blues',
            title="Prestasi Tontonan Video"
        )
        fig_views.update_layout(yaxis={'categoryorder':'total ascending'}) # Susun graf dari bawah ke atas
        st.plotly_chart(fig_views, use_container_width=True)
        
    with col_table1:
        st.dataframe(df_filtered[["Tajuk_Video", "Kategori", "Views", "Engagement_Rate_%"]], use_container_width=True, hide_index=True)

# --- TAB 2: ANALISIS PENCIPTA & GAYA ---
with tab2:
    st.subheader("Impak Gaya Penyampaian terhadap Keterlibatan (Engagement)")
    
    # Carta Pie untuk melihat perkongsian metrik
    fig_pie = px.pie(
        df_filtered, 
        names='Gaya_Penyampaian', 
        values='Views', 
        hole=0.4, 
        title="Sumbangan Tontonan Mengikut Gaya Video",
        color_discrete_sequence=['#ff9999','#66b3ff']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 3: AI INSIGHTS (GEMINI) ---
with tab3:
    st.subheader("🧠 ResearchInsight AI Market Consultant")
    st.info("AI akan menganalisis data semasa di dashboard ini dan memberikan strategi kandungan yang boleh terus digunakan (Actionable Insights) persis penganalisis Kalodata.")
    
    if st.button("Jana Laporan Strategi AI", type="primary"):
        if not gemini_api_key:
            st.error("Ralat: GEMINI_API_KEY tidak dijumpai dalam sistem. Sila tetapkan di platform hosting anda.")
        else:
            with st.spinner("AI sedang mengkaji metrik dan merangka strategi..."):
                # Tukar data ringkas kepada bentuk teks
                data_string = df_filtered[["Tajuk_Video", "Kategori", "Gaya_Penyampaian", "Views", "Engagement_Rate_%"]].to_string()
                
                prompt = f"""
                Anda adalah 'ResearchInsight AI', seorang pakar data analitik tahap tinggi seperti sistem Kalodata, khusus untuk pasaran TikTok.
                Berikut adalah data metrik prestasi video pendek tentang literasi digital:
                
                {data_string}
                
                Tugas anda:
                1. Buat rumusan eksekutif ringkas mengenai trend yang berjaya (gaya penyampaian mana yang paling mendapat sambutan).
                2. Berikan 3 cadangan tajuk video baru (Actionable Strategy) yang patut dicipta seterusnya berdasarkan apa yang trending di atas.
                3. Gunakan nada profesional, yakin, dan tepat (seperti penganalisis data korporat).
                """
                
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    st.success("Analisis Pasaran Berjaya Dijana!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Berlaku ralat semasa menghubungi Gemini AI: {e}")
