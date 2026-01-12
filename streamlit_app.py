import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- ESTILO CSS PARA REPLICAR EL DISEÑO ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://tu-imagen-estadio.jpg");
        background-size: cover;
    }
    .gold-card {
        border: 2px solid #f1d592;
        border-radius: 15px;
        padding: 20px;
        background-color: rgba(15, 23, 15, 0.9);
        box-shadow: 0 0 15px rgba(241, 213, 146, 0.3);
        margin-bottom: 20px;
    }
    .hype-title {
        color: #f1d592;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 12px;
        color: #888;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A DATOS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    songs = conn.read(worksheet="wc-songs")
    users = conn.read(worksheet="wc-user")
    return songs, users

# --- LÓGICA DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- HOME PAGE ---
if st.session_state.page == 'home':
    # Logo y Bienvenida
    st.image("tu-logo-foxe.png", width=200) #
    st.markdown("<h1 class='hype-title'>¡BIENVENIDO A FOXE ARENA!</h1>", unsafe_allow_html=True)
    st.write("Siente la pasión del mundial, haz tus pronósticos y vibra con la banda sonora oficial.")

    st.markdown("### 🎵 BANDA SONORA OFICIAL")
    
    songs_df, _ = get_data()
    # Últimas 3 canciones
    ultimas = songs_df.tail(3).iloc[::-1]
    
    for _, song in ultimas.iterrows():
        with st.container():
            st.markdown(f"""
            <div class='gold-card'>
                <h4 style='color:#f1d592;'>{song['nombre']}</h4>
                <p style='color:white;'>{song['grupo']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.video(song['url'])

    if st.button("MOSTRAR TODAS"):
        for grupo, datos in songs_df.groupby("grupo"):
            with st.expander(f"GRUPO: {grupo}"):
                for _, r in datos.iterrows():
                    st.write(f"▶️ [{r['nombre']}]({r['url']})")

    # Footer
    st.markdown("<div class='footer'>© 2026 FOXE ARENA. Todos los derechos reservados.</div>", unsafe_allow_html=True)
    if st.button("Admin Portal"):
        st.session_state.page = 'admin_login'
        st.rerun()

# --- ADMIN LOGIN ---
elif st.session_state.page == 'admin_login':
    st.markdown("<h2 class='hype-title'>ADMIN PORTAL</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("Usuario")
        pwd = st.text_input("Contraseña", type="password")
        if st.form_submit_button("ACCEDER"):
            _, users_df = get_data()
            if not users_df[(users_df['user'] == user) & (users_df['password'] == pwd)].empty:
                st.session_state.logged_in = True
                st.session_state.page = 'admin_panel'
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    
    if st.button("Volver al inicio"):
        st.session_state.page = 'home'
        st.rerun()

# --- ADMIN PANEL ---
elif st.session_state.page == 'admin_panel':
    st.markdown("<h2 class='hype-title'>GESTIÓN DE CANCIONES</h2>", unsafe_allow_html=True)
    
    with st.expander("➕ AÑADIR NUEVA CANCIÓN", expanded=True):
        with st.form("new_song"):
            nombre = st.text_input("Nombre")
            url = st.text_input("URL de YouTube")
            grupo = st.text_input("Grupo")
            if st.form_submit_button("AÑADIR CANCIÓN"):
                # Aquí iría la lógica conn.update() para Google Sheets
                st.success(f"Canción {nombre} añadida con éxito")

    if st.button("CERRAR SESIÓN"):
        st.session_state.page = 'home'
        st.rerun()

