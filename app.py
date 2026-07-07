import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. SETUP HALAMAN (Gaya Kalodata - Wide & Bersih)
# ==========================================
st.set_page_config(page_title="Kalodata UI - ResearchInsight Hub", page_icon="📈", layout="wide")

# CSS Khas untuk mencantikkan elemen (DIBETULKAN: unsafe_allow_html=True)
st.markdown("""
    <style>
    .kalo-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e9ecef;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    .top-badge {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #d63384;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .chip-btn {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 20px;
        padding: 6px 15px;
        font-size: 13px;
        display: inline-block;
        margin-right: 8px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Konfigurasi Gemini AI
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Menyimpan sejarah carian AI menggunakan Session State (FUNGSI BARU)
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

# Data Mock Video Pendidikan 
data_videos = [
    {"rank": "TOP 1", "tajuk": "Cara Guna AI Untuk Assignment", "kategori": "Pendidikan AI", "views": "320K", "engagement": "12.5%", "bg": "🧠"},
    {"rank": "TOP 2", "tajuk": "Bahaya Scam Link Telegram", "kategori": "Keselamatan Siber", "views": "210K", "engagement": "9.8%", "bg": "🔒"},
    {"rank": "TOP 3", "tajuk": "Edit Video Pendek Pakai CapCut", "kategori": "Kandungan Kreatif", "views": "150K", "engagement": "8.4%", "bg": "🎬"},
    {"rank": "TOP 4", "tajuk": "Cara Buat Password Kuat", "kategori": "Keselamatan Siber", "views": "95K", "engagement": "7.2%", "bg": "🔑"},
    {"rank": "TOP 5", "tajuk": "Asas Celik Digital Komuniti", "kategori": "Asas Digital", "views": "45K", "engagement": "6.1%", "bg": "🌐"}
]

# ==========================================
# 2. BAHAGIAN ATAS: AI-POWERED INSIGHTS ("Just Ask")
# ==========================================
st.markdown("<h3 style='text-align: center; color: #0d6efd;'>✨ Just Ask – Get AI-Powered Insights</h3>", unsafe_allow_html=True)

user_query = st.text_input(
    label="Assign a task or ask anything about your TikTok Education Analytics data...",
    placeholder="Contoh: 'Berikan saya idea kandungan trending seterusnya berdasarkan data TOP 1'...",
    label_visibility="collapsed"
)

# Pintasan Strategi
st.markdown("""
    <span class='chip-btn'>📊 Video Impact Analysis</span>
    <span class='chip-btn'>🧑‍🤝‍🧑 Community Engagement</span>
    <span class='chip-btn'>💡 Topic Suggestions</span>
    <span class='chip-btn'>📈 Trend Forecasting</span>
""", unsafe_allow_html=True)

st.markdown("<br><hr>", unsafe_allow_html=True)

# Logik Tindakbalas Kotak AI Utama (DIBETULKAN dengan Error Handling & Session State)
if user_query:
    if gemini_api_key:
        with st.spinner("AI Assistant sedang merangka jawapan..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(
                    f"Anda penganalisis data pakar. Konteks Data semasa (kedudukan video): {str(data_videos)}. Jawab soalan ini secara profesional: {user_query}"
                )
                # Simpan jawapan ke dalam memori
                st.session_state.ai_response = response.text
            except Exception as e:
                st.error(f"Harap maaf, sistem AI mengalami ralat: {e}")
    else:
        st.error("Sila masukkan GEMINI_API_KEY dalam environment variables di Render.")

# Paparkan jawapan AI dari memori (jika ada)
if st.session_state.ai_response:
    with st.chat_message("assistant"):
        st.write(st.session_state.ai_response)
        if st.button("Tutup Laporan AI"):
            st.session_state.ai_response = ""
            st.rerun()

# ==========================================
# 3. SISTEM TAB UTAMA & KAD VISUAL
# ==========================================
tab_ranking, tab_following = st.tabs(["🔥 Hot-trending Ranking", "📁 My Following Topics"])

with tab_ranking:
    st.markdown("<h4>Top Impacting Videos <span style='font-size:13px; color:gray;'>(Semasa)</span></h4>", unsafe_allow_html=True)
    
    cols = st.columns(5)
    
    for idx, vid in enumerate(data_videos):
        with cols[idx]:
            st.markdown(f"""
                <div class='kalo-card'>
                    <div class='top-badge'>👑 {vid['rank']}</div>
                    <div style='font-size: 40px; text-align: center; margin: 10px 0;'>{vid['bg']}</div>
                    <b style='font-size:14px; display:block; min-height:45px; line-height: 1.2;'>{vid['tajuk']}</b>
                    <p style='font-size:12px; color:gray; margin:5px 0 0 0;'>Kategori: {vid['kategori']}</p>
                    <hr style='margin: 8px 0;'>
                    <div style='display:flex; justify-content:space-between; font-size:12px;'>
                        <span>👁️ <b>{vid['views']}</b></span>
                        <span style='color:green;'>📈 <b>{vid['engagement']}</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

with tab_following:
    st.write("📁 Anda belum mengikuti mana-mana tag atau topik komuniti lagi.")
