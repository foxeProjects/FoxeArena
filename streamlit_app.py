import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS DE RECURSOS ---
LOGO = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- ESTILO CSS MEJORADO ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), 
                    url("https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{ESTADIO}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .gold-card {{
        border: 2px solid #f1d592;
        border-radius: 15px;
        padding: 25px;
        background-color: rgba(15, 23, 15, 0.9);
        box-shadow: 0 0 15px rgba(241, 213, 146, 0.3);
        margin-bottom: 25px; /* Más espacio entre tarjetas */
        text-align: center;
        color: white;
    }}
    .hype-title {{
        color: #f1d592;
        text-align: center;
        font-family: 'Impact', sans-serif;
        font-size: 3.5rem;
        margin-bottom: 10px;
    }}
    /* Espaciado para los botones de YouTube */
    .yt-button {{
        display: inline-block;
        padding: 10px 20px;
        background-color: #ff0000;
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 10px;
    }}
    .section-spacing {{
        margin-top: 40px;
        margin-bottom: 20px;
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
except Exception as e:
    st.error("Error cargando base de datos.")
    st.stop()

# --- GESTIÓN DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 1. HOME PAGE ---
if st.session_state.page == 'home':
    # Espacio superior
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(LOGO, use_container_width=True)
    
    st.markdown("<h1 class='hype-title'>FOXE ARENA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#f1d592; font-size:1.3rem;'>🔥 LA PORRA OFICIAL DEL MUNDIAL 🔥</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)
    st.subheader("🎵 ÚLTIMOS LANZAMIENTOS")
    
    # Mostrar 3 últimas canciones con link externo
    ultimas = songs_df.tail(3).iloc[::-1]
    for _, song in ultimas.iterrows():
        with st.container():
            st.markdown(f"""
            <div class='gold-card'>
                <h3 style='color:#f1d592; margin-bottom:5px;'>{song['nombre']}</h3>
                <p style='color:#ccc;'>Grupo: {song['grupo']}</p>
                <a href='{song['url']}' target='_blank' class='yt-button'>📺 VER EN YOUTUBE</a>
            </div>
            """, unsafe_allow_html=True)

    # Botón Ver Todas
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📂 MOSTRAR TODA LA BANDA SONORA", use_container_width=True):
        st.session_state.page = 'all_songs'
        st.rerun()

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("---")
    if st.button("🔐 Acceso Administración"):
        st.session_state.page = 'admin_login'
        st.rerun()

# --- 2. TODAS LAS CANCIONES ---
elif st.session_state.page == 'all_songs':
    if st.button("← VOLVER ATRÁS"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown("<h2 style='color:#f1d592; text-align:center;'>BANDA SONORA COMPLETA</h2>", unsafe_allow_html=True)
    
    for grupo, datos in songs_df.groupby("grupo"):
        with st.expander(f"📁 GRUPO: {grupo}", expanded=True):
            for _, r in datos.iterrows():
                col_a, col_b = st.columns([3, 1])
                col_a.write(f"**{r['nombre']}**")
                col_b.markdown(f"[Ver 📺]({r['url']})")
    
    if st.button("VOLVER AL INICIO", key="back_bottom"):
        st.session_state.page = 'home'
        st.rerun()

# --- 3. LOGIN ---
elif st.session_state.page == 'admin_login':
    if st.button("← CANCELAR"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown("<div class='gold-card'>", unsafe_allow_html=True)
    st.subheader("ACCESO ADMIN")
    with st.form("login"):
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.form_submit_button("ENTRAR"):
            match = users_df[(users_df['user'] == u) & (users_df['password'] == p)]
            if not match.empty:
                st.session_state.page = 'admin_panel'
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.markdown("</div>", unsafe_allow_html=True)
