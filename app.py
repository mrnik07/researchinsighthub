import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# ==========================================
# 1. SETUP HALAMAN & CSS
# ==========================================
st.set_page_config(page_title="Kalodata UI - ResearchInsight Hub", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .kalo-card { background-color: #f8f9fa; border-radius: 12px; padding: 15px; border: 1px solid #e9ecef; margin-bottom: 15px; }
    .top-badge { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); color: #d63384; padding: 3px 10px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; margin-bottom: 8px; }
    .chip-btn { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 20px; padding: 6px 15px; font-size: 13px; display: inline-block; margin-right: 8px; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# Konfigurasi AI
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if gemini_api_key: genai.configure(api_key=gemini_api_key)

if "ai_response" not in st.session_state: st.session_state.ai_response = ""

# ==========================================
# 2. SISTEM PENGAMBILAN DATA (SIDEBAR)
# ==========================================
st.sidebar.markdown("### ⚙️ Pengurusan Data")
st.sidebar.info("Muat naik data analitik TikTok (format CSV) untuk menjana papan pemuka ini.")

uploaded_file = st.sidebar.file_uploader("Muat Naik Data CSV", type=["csv"])

# Fungsi untuk membaca dan memformat data
def dapatkan_data():
    if uploaded_file is not None:
        try:
            # Baca CSV yang dimuat naik pengguna
            df = pd.read_csv(uploaded_file)
            # Andaikan CSV ada column: Tajuk, Kategori, Views, Engagement
            # Susun mengikut Views tertinggi
            df = df.sort_values(by="Views", ascending=False).head(5)
            
            data_baru = []
            for idx, row in df.iterrows():
                # Convert format nombor besar
                views_str = f"{int(row['Views'])/1000:.1f}K" if row['Views'] >= 1000 else str(row['Views'])
                
                data_baru.append({
                    "rank": f"TOP {len(data_baru) + 1}",
                    "tajuk": row['Tajuk'],
                    "kategori": row['Kategori'],
                    "views": views_str,
                    "engagement": f"{row['Engagement']}%",
                    "bg": "📈" # Boleh dinamikkan mengikut kategori
                })
            return data_baru
        except Exception as e:
            st.sidebar.error(f"Ralat format CSV: {e}")
            return tiada_data_template()
    else:
        # Jika tiada fail, guna data simulasi (Mock Data)
        return data_simulasi()

def data_simulasi():
    return [
        {"rank": "TOP 1", "tajuk": "Cara Guna AI Untuk Assignment", "kategori": "Pendidikan AI", "views": "320K", "engagement": "12.5%", "bg": "🧠"},
        {"rank": "TOP 2", "tajuk": "Bahaya Scam Link Telegram", "kategori": "Keselamatan Siber", "views": "210K", "engagement": "9.8%", "bg": "🔒"},
        {"rank": "TOP 3", "tajuk": "Edit Video Pendek Pakai CapCut", "kategori": "Kandungan Kreatif", "views": "150K", "engagement": "8.4%", "bg": "🎬"}
    ]

def tiada_data_template():
    return []

# Panggil fungsi untuk set data utama
data_videos = dapatkan_data()

# ==========================================
# 3. ANTARAMUKA AI "JUST ASK"
# ==========================================
st.markdown("<h3 style='text-align: center; color: #0d6efd;'>✨ Just Ask – Get AI-Powered Insights</h3>", unsafe_allow_html=True)
user_query = st.text_input(label="Soalan", placeholder="Contoh: 'Berikan saya idea kandungan trending seterusnya...'", label_visibility="collapsed")
st.markdown("<span class='chip-btn'>📊 Video Impact</span> <span class='chip-btn'>💡 Topic Suggestions</span>", unsafe_allow_html=True)
st.markdown("<br><hr>", unsafe_allow_html=True)

if user_query and gemini_api_key:
    with st.spinner("Menganalisis data semasa..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Konteks Data: {data_videos}. Jawab soalan ini: {user_query}")
            st.session_state.ai_response = response.text
        except Exception as e:
            st.error(f"Ralat AI: {e}")

if st.session_state.ai_response:
    with st.chat_message("assistant"):
        st.write(st.session_state.ai_response)
        if st.button("Tutup"):
            st.session_state.ai_response = ""
            st.rerun()

# ==========================================
# 4. KAD VISUAL RANKING
# ==========================================
tab_ranking, tab_following = st.tabs(["🔥 Hot-trending Ranking", "📁 My Following Topics"])

with tab_ranking:
    if len(data_videos) > 0:
        cols = st.columns(len(data_videos) if len(data_videos) < 5 else 5)
        for idx, vid in enumerate(data_videos[:5]):
            with cols[idx]:
                st.markdown(f"""
                    <div class='kalo-card'>
                        <div class='top-badge'>👑 {vid['rank']}</div>
                        <div style='font-size: 40px; text-align: center;'>{vid['bg']}</div>
                        <b style='font-size:14px; display:block; min-height:45px;'>{vid['tajuk']}</b>
                        <p style='font-size:12px; color:gray;'>{vid['kategori']}</p>
                        <hr style='margin: 8px 0;'>
                        <div style='display:flex; justify-content:space-between; font-size:12px;'>
                            <span>👁️ <b>{vid['views']}</b></span>
                            <span style='color:green;'>📈 <b>{vid['engagement']}</b></span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Sila muat naik fail CSV yang sah.")
