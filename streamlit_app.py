import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS DE IMÁGENES ---
LOGO = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- ESTILO CSS ---
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
        padding: 20px;
        background-color: rgba(15, 23, 15, 0.9);
        box-shadow: 0 0 15px rgba(241, 213, 146, 0.4);
        margin-bottom: 20px;
        text-align: center;
        color: white;
    }}
    .hype-title {{ color: #f1d592; text-align: center; font-family: 'Impact'; font-size: 3rem; }}
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN DIRECTA (SIN LIBRERÍAS EXTRA) ---
@st.cache_data(ttl=60)
def load_data(sheet_url, sheet_name):
    # Convertimos la URL normal en una URL de descarga directa de CSV
    csv_url = sheet_url.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=" + sheet_name)
    return pd.read_csv(csv_url)

try:
    # Usamos la URL que me pasaste antes
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1-nj5YJsKbm3sAtibZXUZ1EbPYr31Mgx2tvcXzwiygGE/edit?usp=sharing"
    songs_df = load_data(SHEET_URL, "wc-songs")
    users_df = load_data(SHEET_URL, "wc-user")
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.stop()

# --- NAVEGACIÓN ---
if 'page' not in st.session_state: st.session_state.page = 'home'

if st.session_state.page == 'home':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.image(LOGO, use_container_width=True)
    
    st.markdown("<h1 class='hype-title'>FOXE ARENA</h1>", unsafe_allow_html=True)
    
    st.markdown("### 🎵 ÚLTIMOS TEMAS")
    for _, song in songs_df.tail(3).iloc[::-1].iterrows():
        st.markdown(f"<div class='gold-card'><b>{song['nombre']}</b><br>{song['grupo']}</div>", unsafe_allow_html=True)
        st.video(song['url'])
    
    if st.button("MOSTRAR TODAS"):
        for grupo, datos in songs_df.groupby("grupo"):
            with st.expander(f"📁 {grupo}"):
                for _, r in datos.iterrows(): st.write(f"▶️ [{r['nombre']}]({r['url']})")

    st.write("---")
    if st.button("🔐 Admin"):
        st.session_state.page = 'admin_login'
        st.rerun()

elif st.session_state.page == 'admin_login':
    with st.form("login"):
        u = st.text_input("Usuario")
        p = st.text_input("Pass", type="password")
        if st.form_submit_button("Entrar"):
            if not users_df[(users_df['user'] == u) & (users_df['password'] == p)].empty:
                st.session_state.page = 'admin_panel'
                st.rerun()
            else: st.error("Fallo")
    if st.button("Volver"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'admin_panel':
    st.write("Panel Admin (Solo lectura con este método)")
    if st.button("Cerrar"):
        st.session_state.page = 'home'
        st.rerun()
