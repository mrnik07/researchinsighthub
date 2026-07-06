
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Research Insight Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Research Insight Hub")
page = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Dashboard", "📈 Analisis", "📚 Penelitian", "⚙️ Pengaturan"]
)

st.sidebar.markdown("---")
st.sidebar.info("📌 Aplikasi untuk analisis dan visualisasi data penelitian")

# ==================== HALAMAN DASHBOARD ====================
if page == "🏠 Dashboard":
    st.title("📊 Dashboard Utama")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Penelitian",
            value="245",
            delta="+12 minggu ini"
        )
    
    with col2:
        st.metric(
            label="Peneliti Aktif",
            value="87",
            delta="+5 baru"
        )
    
    with col3:
        st.metric(
            label="Publikasi",
            value="156",
            delta="+23 bulan ini"
        )
    
    with col4:
        st.metric(
            label="Skor Rata-rata",
            value="8.5/10",
            delta="+0.3"
        )
    
    st.markdown("---")
    
    # Row 1: Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tren Penelitian")
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
        trend_data = pd.DataFrame({
            'Bulan': dates,
            'Penelitian': np.random.randint(10, 50, 12),
            'Publikasi': np.random.randint(5, 30, 12)
        })
        
        fig = px.line(
            trend_data,
            x='Bulan',
            y=['Penelitian', 'Publikasi'],
            markers=True,
            title='Tren Penelitian 12 Bulan Terakhir'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Distribusi Kategori")
        categories = pd.DataFrame({
            'Kategori': ['AI/ML', 'Biologi', 'Fisika', 'Kimia', 'Lainnya'],
            'Jumlah': [45, 38, 32, 28, 102]
        })
        
        fig = px.pie(
            categories,
            names='Kategori',
            values='Jumlah',
            title='Distribusi Penelitian per Kategori'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Row 2: Recent publications
    st.subheader("📚 Publikasi Terbaru")
    recent_data = {
        'Judul': [
            'Aplikasi Machine Learning dalam Diagnosa Medis',
            'Analisis Perubahan Iklim Global',
            'Inovasi Material Berkelanjutan'
        ],
        'Peneliti': ['Dr. Ahmad', 'Dr. Siti', 'Prof. Budi'],
        'Kategori': ['AI/ML', 'Biologi', 'Kimia'],
        'Tanggal': ['2024-06-15', '2024-06-12', '2024-06-10'],
        'Sitas': [45, 23, 18]
    }
    
    df_recent = pd.DataFrame(recent_data)
    st.dataframe(df_recent, use_container_width=True)

# ==================== HALAMAN ANALISIS ====================
elif page == "📈 Analisis":
    st.title("📊 Analisis Mendalam")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Filter Data")
    with col2:
        if st.button("🔄 Refresh"):
            st.toast("Data diperbarui!", icon="✅")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kategori = st.multiselect(
            "Kategori Penelitian",
            ["AI/ML", "Biologi", "Fisika", "Kimia", "Lainnya"],
            default=["AI/ML", "Biologi"]
        )
    
    with col2:
        tahun = st.slider("Tahun", 2020, 2024, (2022, 2024))
    
    with col3:
        min_sitas = st.number_input("Min. Sitasi", 0, 1000, 0)
    
    st.markdown("---")
    
    # Analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Produktivitas Peneliti")
        researchers = pd.DataFrame({
            'Peneliti': ['Dr. Ahmad', 'Dr. Siti', 'Prof. Budi', 'Dr. Eka', 'Dr. Farid'],
            'Publikasi': [15, 12, 18, 9, 14]
        }).sort_values('Publikasi', ascending=True)
        
        fig = px.barh(researchers, x='Publikasi', y='Peneliti', color='Publikasi')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Pengaruh Penelitian")
        impact = pd.DataFrame({
            'Penelitian': ['Penelitian A', 'Penelitian B', 'Penelitian C', 'Penelitian D'],
            'h-index': [25, 18, 22, 15]
        })
        
        fig = px.bar(impact, x='Penelitian', y='h-index', color='h-index')
        st.plotly_chart(fig, use_container_width=True)

# ==================== HALAMAN PENELITIAN ====================
elif page == "📚 Penelitian":
    st.title("🔬 Daftar Penelitian")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search = st.text_input("🔍 Cari penelitian...")
    with col2:
        sort_by = st.selectbox("Urutkan", ["Terbaru", "Paling Dikutip", "Judul A-Z"])
    
    st.markdown("---")
    
    # Sample research data
    penelitian = [
        {
            "judul": "Machine Learning untuk Analisis Genomik",
            "peneliti": "Dr. Ahmad Rizki",
            "kategori": "AI/ML",
            "tahun": 2024,
            "sitasi": 125,
            "deskripsi": "Penelitian tentang aplikasi machine learning dalam analisis data genomik"
        },
        {
            "judul": "Dampak Perubahan Iklim pada Ekosistem Laut",
            "peneliti": "Dr. Siti Nurhaliza",
            "kategori": "Biologi",
            "tahun": 2023,
            "sitasi": 87,
            "deskripsi": "Studi longitudinal mengenai pengaruh perubahan iklim terhadap kehidupan laut"
        },
        {
            "judul": "Material Polimer Biodegradable Berkelanjutan",
            "peneliti": "Prof. Budi Santoso",
            "kategori": "Kimia",
            "tahun": 2024,
            "sitasi": 56,
            "deskripsi": "Pengembangan material polimer yang ramah lingkungan dan dapat terurai"
        }
    ]
    
    for idx, paper in enumerate(penelitian):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {paper['judul']}")
                st.caption(f"👨‍🔬 {paper['peneliti']} | 📅 {paper['tahun']}")
                st.write(paper['deskripsi'])
                
                col_cat, col_cit = st.columns(2)
                with col_cat:
                    st.badge(paper['kategori'])
                with col_cit:
                    st.metric("Sitasi", paper['sitasi'])
            
            with col2:
                st.button("📖 Baca", key=f"read_{idx}")
                st.button("⭐ Simpan", key=f"save_{idx}")

# ==================== HALAMAN PENGATURAN ====================
elif page == "⚙️ Pengaturan":
    st.title("⚙️ Pengaturan")
    
    st.subheader("👤 Profil Pengguna")
    col1, col2 = st.columns(2)
    
    with col1:
        nama = st.text_input("Nama", "John Doe")
        email = st.text_input("Email", "john@example.com")
        institusi = st.text_input("Institusi", "Universitas Indonesia")
    
    with col2:
        spesialisasi = st.multiselect(
            "Spesialisasi",
            ["AI/ML", "Biologi", "Fisika", "Kimia"],
            default=["AI/ML"]
        )
        bio = st.text_area("Bio Singkat", "Masukkan biografi singkat Anda")
    
    st.markdown("---")
    
    st.subheader("🔔 Notifikasi")
    col1, col2 = st.columns(2)
    
    with col1:
        st.toggle("Notifikasi Email", value=True)
        st.toggle("Update Penelitian Terbaru", value=True)
    
    with col2:
        st.toggle("Rekomendasi Penelitian", value=False)
        st.toggle("Laporan Mingguan", value=True)
    
    st.markdown("---")
    
    st.subheader("🎨 Tampilan")
    tema = st.radio("Tema", ["Terang", "Gelap", "Otomatis"], index=2)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Simpan Perubahan", type="primary"):
            st.success("Pengaturan berhasil disimpan!")
    with col2:
        if st.button("🔄 Reset ke Default"):
            st.warning("Pengaturan direset ke default")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <p>© 2024 Research Insight Hub | Dibuat dengan ❤️ menggunakan Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
