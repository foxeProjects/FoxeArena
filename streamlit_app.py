import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config[page_title="FOXE ARENA", page_icon="🏆", layout="centered"]

# --- RUTAS DE IMÁGENES ---
LOGO_PATH = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO_PATH = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- ESTILO CSS PERSONALIZADO ---
st.markdown[f"""
    <style>
    /* Fondo con overlay oscuro para legibilidad */
    .stApp {{
        background: linear-gradient[rgba[0,0,0,0.7], rgba[0,0,0,0.8]], 
                    url["https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{ESTADIO_PATH}"];
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Tarjetas doradas estilo Premium */
    .gold-card {{
        border: 2px solid #f1d592;
        border-radius: 15px;
        padding: 20px;
        background-color: rgba[15, 23, 15, 0.85];
        box-shadow: 0 0 20px rgba[241, 213, 146, 0.4];
        margin-bottom: 10px;
        text-align: center;
        color: white;
    }}
    
    .hype-title {{
        color: #f1d592;
        text-align: center;
        font-family: 'Impact', sans-serif;
        font-size: 2.8rem;
        text-shadow: 3px 3px 5px #000;
        margin-top: -20px;
    }}
    
    .section-title {{
        color: #f1d592;
        border-left: 5px solid #f1d592;
        padding-left: 10px;
        margin-top: 30px;
    }}
    
    /* Ajuste para el footer */
    .footer {{
        text-align: center;
        color: #666;
        padding-top: 50px;
        font-size: 0.8rem;
    }}
    </style>
    """, unsafe_allow_html=True]

# --- CONEXIÓN A GOOGLE SHEETS ---
try:
    conn = st.connection["gsheets", type=GSheetsConnection]
    songs_df = conn.read[worksheet="wc-songs"]
    users_df = conn.read[worksheet="wc-user"]
except Exception as e:
    st.error["Error de conexión con la base de datos. Revisa tus Secrets."]
    songs_df = pd.DataFrame[columns=["nombre", "url", "grupo"]]

# --- GESTIÓN DE ESTADO DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- LÓGICA DE PÁGINAS ---

# 1. PÁGINA PRINCIPAL
if st.session_state.page == 'home':
    # Logo
    col1, col2, col3 = st.columns[[1, 2, 1]]
    with col2:
        st.image[LOGO_PATH, use_container_width=True]
    
    st.markdown["<h1 class='hype-title'>FOXE ARENA</h1>", unsafe_allow_html=True]
    st.markdown["<p style='text-align:center; font-size:1.2rem;'>🔥 ¡Bienvenido a la porra donde cada gol cuenta y cada canción se siente! 🔥</p>", unsafe_allow_html=True]
    
    st.markdown["<h3 class='section-title'>🎵 BANDA SONORA OFICIAL</h3>", unsafe_allow_html=True]
    
    # Mostrar las últimas 3 canciones
    if not songs_df.empty:
        ultimas_3 = songs_df.tail[3].iloc[::-1]
        for _, song in ultimas_3.iterrows[]:
            st.markdown[f"<div class='gold-card'><b>{song['nombre']}</b> - {song['grupo']}</div>", unsafe_allow_html=True]
            st.video[song['url']]
    
    # Botón Ver Todas
    if st.button["MOSTRAR TODAS LAS CANCIONES"]:
        for grupo, datos in songs_df.groupby["grupo"]:
            with st.expander[f"📁 GRUPO: {grupo}"]:
                for _, r in datos.iterrows[]:
                    st.markdown[f"🔗 [{r['nombre']}]({r['url']})"]

    # Footer con link a Admin
    st.markdown["<div class='footer'>© 2026 FOXE ARENA | Mundial 🏆</div>", unsafe_allow_html=True]
    if st.button["Acceso Admin"]:
        st.session_state.page = 'admin_login'
        st.rerun[]

# 2. LOGIN DE ADMIN
elif st.session_state.page == 'admin_login':
    st.markdown["<h2 class='hype-title'>ADMIN LOGIN</h2>", unsafe_allow_html=True]
    with st.form["login"]:
        user_input = st.text_input["Usuario"]
        pass_input = st.text_input["Password", type="password"]
        if st.form_submit_button["Entrar"]:
            match = users_df[[users_df['user'] == user_input] & [users_df['password'] == pass_input]]
            if not match.empty:
                st.session_state.is_admin = True
                st.session_state.page = 'admin_panel'
                st.rerun[]
            else:
                st.error["Credenciales no válidas"]
    
    if st.button["← Volver"]:
        st.session_state.page = 'home'
        st.rerun[]

# 3. PANEL DE CONTROL (ADMIN)
elif st.session_state.page == 'admin_panel':
    st.markdown["<h2 class='hype-title'>GESTIÓN FOXE</h2>", unsafe_allow_html=True]
    
    with st.form["add_song"]:
        st.write["### Añadir Nueva Canción"]
        n_nombre = st.text_input["Nombre de la Canción"]
        n_url = st.text_input["URL de YouTube"]
        n_grupo = st.text_input["Grupo [Texto libre]"]
        
        if st.form_submit_button["GUARDAR CANCIÓN"]:
            new_row = pd.DataFrame[[{"nombre": n_nombre, "url": n_url, "grupo": n_grupo}]]
            updated_df = pd.concat[[songs_df, new_row], ignore_index=True]
            conn.update[worksheet="wc-songs", data=updated_df]
            st.success["¡Canción añadida con éxito!"]
            st.balloons[]

    if st.button["Cerrar Sesión"]:
        st.session_state.page = 'home'
        st.rerun[]
