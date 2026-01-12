import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS DE RECURSOS ---
LOGO = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- ESTILO VISUAL PREMIUN ---
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
    }}
    .hype-text {{
        color: #f1d592;
        text-align: center;
        font-family: 'Impact', sans-serif;
        font-size: 2.5rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A DATOS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    songs_df = conn.read(spreadsheet=url, worksheet="wc-songs")
    users_df = conn.read(spreadsheet=url, worksheet="wc-user")
except Exception as e:
    st.error("Error de conexión. Revisa que el Secret esté en una sola línea.")
    st.stop()

# --- LÓGICA DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PÁGINA DE INICIO ---
if st.session_state.page == 'home':
    st.image(LOGO, width=250)
    st.markdown("<h1 class='hype-text'>¡BIENVENIDO A FOXE ARENA!</h1>", unsafe_allow_html=True)
    st.write("### Siente la pasión y vibra con la banda sonora oficial.")
    
    st.divider()
    
    if not songs_df.empty:
        st.subheader("🎵 ÚLTIMAS CANCIONES")
        for _, song in songs_df.tail(3).iloc[::-1].iterrows():
            st.markdown(f"<div class='gold-card'><b>{song['nombre']}</b> - {song['grupo']}</div>", unsafe_allow_html=True)
            st.video(song['url'])
    
    if st.button("MOSTRAR TODAS"):
        for grupo, datos in songs_df.groupby("grupo"):
            with st.expander(f"📁 GRUPO: {grupo}"):
                for _, r in datos.iterrows():
                    st.write(f"▶️ [{r['nombre']}]({r['url']})")

    st.markdown("---")
    if st.button("🔐 Admin Portal"):
        st.session_state.page = 'admin_login'
        st.rerun()

# --- LOGIN ADMIN ---
elif st.session_state.page == 'admin_login':
    st.markdown("<h2 class='hype-text'>ACCESO RESTRINGIDO</h2>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.form_submit_button("ACCEDER"):
            # Validación con tu tabla wc-user
            if not users_df[(users_df['user'] == u) & (users_df['password'] == p)].empty:
                st.session_state.page = 'admin_panel'
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    if st.button("Volver"):
        st.session_state.page = 'home'
        st.rerun()

# --- PANEL ADMIN ---
elif st.session_state.page == 'admin_panel':
    st.markdown("<h2 class='hype-text'>GESTIÓN DE CANCIONES</h2>", unsafe_allow_html=True)
    with st.form("new_song"):
        n = st.text_input("Nombre")
        l = st.text_input("URL de YouTube")
        g = st.text_input("Grupo")
        if st.form_submit_button("AÑADIR CANCIÓN"):
            new_row = pd.DataFrame([{"nombre": n, "url": l, "grupo": g}])
            updated_df = pd.concat([songs_df, new_row], ignore_index=True)
            conn.update(spreadsheet=url, worksheet="wc-songs", data=updated_df)
            st.success("Canción añadida con éxito")
            st.balloons()
    
    if st.button("Cerrar Sesión"):
        st.session_state.page = 'home'
        st.rerun()
