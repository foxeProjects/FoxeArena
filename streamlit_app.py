import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS ---
LOGO = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- CSS: AJUSTE DE DISEÑO FIEL ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.9)), 
                    url("https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{ESTADIO}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* CENTRADO ABSOLUTO DEL LOGO */
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: -30px;
    }}
    .logo-container img {{
        width: 200px;
        height: auto;
    }}

    /* TÍTULO IMPACTANTE */
    .foxe-title {{
        font-family: 'Bebas Neue', cursive;
        font-size: 5rem;
        text-align: center;
        background: linear-gradient(to bottom, #f1d592, #a67c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -10px;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }}

    /* CAJA DORADA PARA EL VIDEO */
    .video-card {{
        border: 2px solid #f1d592;
        border-radius: 15px;
        padding: 10px;
        background-color: rgba(0, 0, 0, 0.8);
        box-shadow: 0 0 25px rgba(241, 213, 146, 0.3);
        margin-bottom: 40px;
    }}

    .card-info {{
        padding: 15px 10px;
        text-align: center;
    }}

    .card-info h3 {{
        color: #f1d592;
        margin: 0;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.8rem;
        letter-spacing: 1px;
    }}

    /* BOTONES SUTILES Y ELEGANTES */
    .stButton>button {{
        background: transparent;
        border: 1px solid rgba(241, 213, 146, 0.5);
        color: #f1d592;
        border-radius: 5px;
        padding: 10px 30px;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.2rem;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        border-color: #f1d592;
        background: rgba(241, 213, 146, 0.1);
        box-shadow: 0 0 10px rgba(241, 213, 146, 0.2);
    }}
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

# --- INTERFAZ ---
# 1. Logo Centrado
st.markdown(f'<div class="logo-container"><img src="https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{LOGO}"></div>', unsafe_allow_html=True)

# 2. Título Foxe Arena
st.markdown('<h1 class="foxe-title">FOXE ARENA</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; font-size:1.1rem; margin-top:-15px; letter-spacing:2px;'>LA PORRA OFICIAL DEL MUNDIAL</p>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 3. Sección de Videos
if st.session_state.get('page', 'home') == 'home':
    st.markdown("<h4 style='color:#f1d592; font-family:Bebas Neue; letter-spacing:1px;'>🎵 ÚLTIMOS LANZAMIENTOS</h4>", unsafe_allow_html=True)
    
    ultimas = songs_df.tail(3).iloc[::-1]
    for _, song in ultimas.iterrows():
        # Iniciamos la Card Dorada
        st.markdown('<div class="video-card">', unsafe_allow_html=True)
        
        # El Video embebido directamente (Streamlit lo pone dentro del div de la card)
        st.video(song['url'])
        
        # Info de la canción debajo del video, dentro de la card
        st.markdown(f"""
            <div class="card-info">
                <h3>{song['nombre']}</h3>
                <p style="color:#888; margin:0;">{song['grupo']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # Cerramos Card

    # Botones de Navegación sutiles
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("EXPLORAR BANDA SONORA COMPLETA", use_container_width=True):
        st.session_state.page = 'all_songs'
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_b:
        if st.button("GESTIÓN ADMIN"):
            # Lógica de login aquí
            pass
