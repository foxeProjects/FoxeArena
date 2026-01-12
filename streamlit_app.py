import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS DE IMÁGENES ---
LOGO = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- ESTILO CSS (DISEÑO PREMIUM) ---
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
    .hype-title {{
        color: #f1d592;
        text-align: center;
        font-family: 'Impact', sans-serif;
        font-size: 3rem;
        text-shadow: 2px 2px 4px #000;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A DATOS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    url_sheet = st.secrets["connections"]["gsheets"]["spreadsheet"]
    songs_df = conn.read(spreadsheet=url_sheet, worksheet="wc-songs")
    users_df = conn.read(spreadsheet=url_sheet, worksheet="wc-user")
except Exception as e:
    st.error("⚠️ Error de conexión. Revisa que el Secret esté en una sola línea y la hoja sea pública.")
    st.stop()

# --- NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PÁGINA: HOME ---
if st.session_state.page == 'home':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(LOGO, use_container_width=True)
    
    st.markdown("<h1 class='hype-title'>FOXE ARENA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white; font-size:1.2rem;'>🔥 ¡Bienvenido a la porra oficial! Siente la música del mundial. 🔥</p>", unsafe_allow_html=True)
    
    st.markdown("### 🎵 ÚLTIMOS LANZAMIENTOS")
    if not songs_df.empty:
        # Mostramos las 3 últimas canciones
        ultimas = songs_df.tail(3).iloc[::-1]
        for _, song in ultimas.iterrows():
            st.markdown(f"<div class='gold-card'><b>{song['nombre']}</b><br><small>{song['grupo']}</small></div>", unsafe_allow_html=True)
            st.video(song['url'])
    
    if st.button("VER TODAS LAS CANCIONES"):
        for grupo, datos in songs_df.groupby("grupo"):
            with st.expander(f"📁 GRUPO: {grupo}"):
                for _, r in datos.iterrows():
                    st.write(f"▶️ [{r['nombre']}]({r['url']})")

    st.write("---")
    if st.button("🔐 Acceso Admin"):
        st.session_state.page = 'admin_login'
        st.rerun()

# --- PÁGINA: LOGIN ---
elif st.session_state.page == 'admin_login':
    st.markdown("<h2 class='hype-title'>LOGIN</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        user_in = st.text_input("Usuario")
        pass_in = st.text_input("Contraseña", type="password")
        if st.form_submit_button("ENTRAR"):
            match = users_df[(users_df['user'] == user_in) & (users_df['password'] == pass_in)]
            if not match.empty:
                st.session_state.page = 'admin_panel'
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    
    if st.button("Volver al Inicio"):
        st.session_state.page = 'home'
        st.rerun()

# --- PÁGINA: PANEL ADMIN ---
elif st.session_state.page == 'admin_panel':
    st.markdown("<h2 class='hype-title'>PANEL DE CONTROL</h2>", unsafe_allow_html=True)
    with st.form("add_song"):
        st.write("Añadir nueva canción:")
        n = st.text_input("Nombre")
        u = st.text_input("YouTube URL")
        g = st.text_input("Grupo")
        if st.form_submit_button("PUBLICAR"):
            new_row = pd.DataFrame([{"nombre": n, "url": u, "grupo": g}])
            updated_df = pd.concat([songs_df, new_row], ignore_index=True)
            conn.update(spreadsheet=url_sheet, worksheet="wc-songs", data=updated_df)
            st.success("¡Canción añadida!")
            st.balloons()
            
    if st.button("Cerrar Sesión"):
        st.session_state.page = 'home'
        st.rerun()
