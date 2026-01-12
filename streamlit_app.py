import streamlit as st
import pandas as pd
import re

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS ---
LOGO = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- EXTRACCIÓN DE MINIATURA ---
def get_yt_thumb(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
    return ""

# --- CSS: SUTILEZA Y GLOW ---
st.markdown(f"""
    <style>
    /* Fondo con degradado profundo */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.9)), 
                    url("https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{ESTADIO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Logo Limpio */
    .logo-container {{
        text-align: center;
        margin-bottom: 20px;
    }}
    .logo-container img {{
        width: 180px;
        filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.5));
    }}

    /* Card con Glow Sutil */
    .video-card {{
        border: 1px solid rgba(241, 213, 146, 0.3);
        border-radius: 12px;
        background: rgba(10, 10, 10, 0.7);
        overflow: hidden;
        margin-bottom: 25px;
        transition: all 0.4s ease;
    }}
    .video-card:hover {{
        border: 1px solid rgba(241, 213, 146, 0.8);
        box-shadow: 0 0 20px rgba(241, 213, 146, 0.2);
        transform: translateY(-3px);
    }}

    .card-img {{
        width: 100%;
        aspect-ratio: 16/9;
        object-fit: cover;
    }}

    .card-content {{
        padding: 18px;
    }}

    .card-title {{
        color: #f1d592;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 0.5px;
    }}

    /* Botones Sutiles */
    .stButton>button {{
        background: transparent;
        border: 1px solid rgba(241, 213, 146, 0.4);
        color: #f1d592;
        font-size: 0.85rem;
        font-weight: 400;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 8px 20px;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        border: 1px solid #f1d592;
        background: rgba(241, 213, 146, 0.05);
        color: white;
    }}

    /* Quitar estilos por defecto de links */
    a {{ text-decoration: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1-nj5YJsKbm3sAtibZXUZ1EbPYr31Mgx2tvcXzwiygGE/edit?usp=sharing"
    csv_url = url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=wc-songs")
    user_url = url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=wc-user")
    return pd.read_csv(csv_url), pd.read_csv(user_url)

try:
    songs_df, users_df = load_data()
except:
    st.stop()

# --- NAVEGACIÓN ---
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- 1. HOME ---
if st.session_state.page == 'home':
    st.markdown(f'<div class="logo-container"><img src="https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{LOGO}"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; color:white; font-weight:200; letter-spacing:3px; margin-bottom:40px;'>FOXE ARENA</h2>", unsafe_allow_html=True)
    
    st.write("#### 🎵 ÚLTIMOS LANZAMIENTOS")
    
    ultimas = songs_df.tail(3).iloc[::-1]
    for _, song in ultimas.iterrows():
        thumb = get_yt_thumb(song['url'])
        st.markdown(f"""
            <a href="{song['url']}" target="_blank">
                <div class="video-card">
                    <img src="{thumb}" class="card-img">
                    <div class="card-content">
                        <p class="card-title">{song['nombre']}</p>
                        <p style="color: #888; font-size: 0.8rem; margin-top:5px;">{song['grupo']}</p>
                    </div>
                </div>
            </a>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Explorar Banda Sonora Completa", use_container_width=True):
        st.session_state.page = 'all_songs'
        st.rerun()

    # Footer Admin sutil
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_b:
        if st.button("Gestión Admin"):
            st.session_state.page = 'admin_login'
            st.rerun()

# --- 2. TODAS LAS CANCIONES ---
elif st.session_state.page == 'all_songs':
    if st.button("← VOLVER"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("<h3 style='color:#f1d592; letter-spacing:2px;'>BANDA SONORA COMPLETA</h3>", unsafe_allow_html=True)
    for grupo, datos in songs_df.groupby("grupo"):
        with st.expander(f"{grupo.upper()}", expanded=False):
            for _, r in datos.iterrows():
                st.markdown(f"• [{r['nombre']}]({r['url']})", unsafe_allow_html=True)

# --- 3. LOGIN ---
elif st.session_state.page == 'admin_login':
    if st.button("← CANCELAR"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("<div style='max-width:300px; margin:auto; padding-top:50px;'>", unsafe_allow_html=True)
    with st.form("login"):
        st.markdown("<p style='color:#f1d592; text-align:center;'>ACCESO PRIVADO</p>", unsafe_allow_html=True)
        u = st.text_input("User")
        p = st.text_input("Pass", type="password")
        if st.form_submit_button("ACCEDER"):
            match = users_df[(users_df['user'] == u) & (users_df['password'] == p)]
            if not match.empty:
                st.session_state.page = 'admin_panel'
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
