import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS ---
LOGO = "assets/IMG_9234.png"
ESTADIO = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- ESTILO CSS PERSONALIZADO ---
st.markdown(f"""
    <style>
    /* Fondo del Estadio */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), 
                    url("https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{ESTADIO}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Logo sin bordes ni fondos */
    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: -20px;
    }}
    
    /* Tarjetas de Video con Borde Dorado (Glow) */
    .video-card {{
        border: 2px solid #f1d592;
        border-radius: 15px;
        padding: 15px;
        background-color: rgba(0, 0, 0, 0.6);
        box-shadow: 0 0 15px rgba(241, 213, 146, 0.4);
        margin-bottom: 30px;
    }}
    
    .video-title {{
        color: #f1d592;
        font-family: 'Impact', sans-serif;
        font-size: 1.5rem;
        margin-bottom: 5px;
    }}

    /* Botones de navegación */
    .stButton>button {{
        border: 1px solid #f1d592;
        background-color: rgba(241, 213, 146, 0.1);
        color: #f1d592;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data(ttl=60)
def load_data(sheet_url, sheet_name):
    csv_url = sheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=" + sheet_name)
    return pd.read_csv(csv_url)

try:
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1-nj5YJsKbm3sAtibZXUZ1EbPYr31Mgx2tvcXzwiygGE/edit?usp=sharing"
    songs_df = load_data(SHEET_URL, "wc-songs")
    users_df = load_data(SHEET_URL, "wc-user")
except:
    st.error("Error de conexión.")
    st.stop()

# --- NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 1. HOME ---
if st.session_state.page == 'home':
    # Logo limpio
    st.markdown(f'<div class="logo-container">', unsafe_allow_html=True)
    st.image(LOGO, width=220)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center; color:#f1d592; font-family:Impact;'>FOXE ARENA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white;'>🔥 ¡BIENVENIDO A LA PORRA OFICIAL! 🔥</p>", unsafe_allow_html=True)
    
    st.markdown("### 🎵 ÚLTIMOS LANZAMIENTOS")
    
    ultimas = songs_df.tail(3).iloc[::-1]
    for _, song in ultimas.iterrows():
        # Contenedor con borde dorado para el video
        with st.container():
            st.markdown(f"""
            <div class="video-card">
                <div class="video-title">{song['nombre']}</div>
                <p style="color:#ccc; font-size:0.9rem;">{song['grupo']}</p>
            </div>
            """, unsafe_allow_html=True)
            # El componente de video de Streamlit muestra la miniatura por defecto
            st.video(song['url'])

    if st.button("📂 VER TODAS LAS CANCIONES", use_container_width=True):
        st.session_state.page = 'all_songs'
        st.rerun()

    # Footer
    st.write("---")
    if st.button("🔐 Panel Admin"):
        st.session_state.page = 'admin_login'
        st.rerun()

# --- 2. TODAS LAS CANCIONES ---
elif st.session_state.page == 'all_songs':
    if st.button("← VOLVER AL INICIO"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown("<h2 style='color:#f1d592; text-align:center;'>BANDA SONORA</h2>", unsafe_allow_html=True)
    
    for grupo, datos in songs_df.groupby("grupo"):
        with st.expander(f"📁 {grupo}", expanded=True):
            for _, r in datos.iterrows():
                st.write(f"**{r['nombre']}**")
                st.video(r['url']) # Muestra miniatura
    
    if st.button("VOLVER ARRIBA"):
        st.session_state.page = 'home'
        st.rerun()

# --- 3. LOGIN ---
elif st.session_state.page == 'admin_login':
    if st.button("← VOLVER"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown("<h2 style='color:#f1d592; text-align:center;'>ADMIN LOGIN</h2>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Usuario")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("ENTRAR"):
            match = users_df[(users_df['user'] == u) & (users_df['password'] == p)]
            if not match.empty:
                st.session_state.page = 'admin_panel'
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
