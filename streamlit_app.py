import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS DE IMÁGENES ---
LOGO_PATH = "assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO_PATH = "assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- ESTILO CSS PERSONALIZADO (Look Premium) ---
st.markdown(f"""
    <style>
    /* Fondo con overlay oscuro y la imagen de tu repo */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), 
                    url("https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/{ESTADIO_PATH}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Tarjetas doradas con efecto de brillo */
    .gold-card {{
        border: 2px solid #f1d592;
        border-radius: 15px;
        padding: 20px;
        background-color: rgba(15, 23, 15, 0.85);
        box-shadow: 0 0 20px rgba(241, 213, 146, 0.4);
        margin-bottom: 15px;
        text-align: center;
        color: white;
    }}
    
    .hype-title {{
        color: #f1d592;
        text-align: center;
        font-family: 'Impact', sans-serif;
        font-size: 3rem;
        text-shadow: 3px 3px 5px #000;
        margin-top: -10px;
    }}
    
    .section-title {{
        color: #f1d592;
        border-left: 5px solid #f1d592;
        padding-left: 15px;
        margin-top: 30px;
        font-weight: bold;
    }}

    /* Estilo para los botones */
    .stButton>button {{
        width: 100%;
        border-radius: 10px;
        border: 1px solid #f1d592;
        background-color: rgba(241, 213, 146, 0.1);
        color: #f1d592;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    songs_df = conn.read(worksheet="wc-songs")
    users_df = conn.read(worksheet="wc-user")
except Exception as e:
    st.error("⚠️ Error de conexión. Revisa los Secrets en Streamlit Cloud.")
    songs_df = pd.DataFrame(columns=["nombre", "url", "grupo"])
    users_df = pd.DataFrame(columns=["user", "password", "role"])

# --- GESTIÓN DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 1. HOME PAGE ---
if st.session_state.page == 'home':
    # Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown("<h1 class='hype-title'>FOXE ARENA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2rem; color:white;'>🔥 ¡Siente la pasión del mundial y vibra con la banda sonora oficial! 🔥</p>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='section-title'>🎵 ÚLTIMOS TEMAS</h3>", unsafe_allow_html=True)
    
    if not songs_df.empty:
        # Mostramos las 3 últimas en orden inverso
        ultimas_3 = songs_df.tail(3).iloc[::-1]
        for _, song in ultimas_3.iterrows():
            st.markdown(f"<div class='gold-card'><b>{song['nombre']}</b><br><small>{song['grupo']}</small></div>", unsafe_allow_html=True)
            st.video(song['url'])
    
    if st.button("VER TODAS LAS CANCIONES"):
        for grupo, datos in songs_df.groupby("grupo"):
            with st.expander(f"📁 GRUPO: {grupo}"):
                for _, r in datos.iterrows():
                    st.write(f"▶️ [{r['nombre']}]({r['url']})")

    # Footer discreto
    st.write("---")
    if st.button("🔐 Admin Portal"):
        st.session_state.page = 'admin_login'
        st.rerun()

# --- 2. LOGIN DE ADMIN ---
elif st.session_state.page == 'admin_login':
    st.markdown("<h2 class='hype-title'>ACCESO ADMIN</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        user_input = st.text_input("Usuario")
        pass_input = st.text_input("Contraseña", type="password")
        if st.form_submit_button("ENTRAR"):
            # Validación contra la tabla wc-user
            match = users_df[(users_df['user'] == user_input) & (users_df['password'] == pass_input)]
            if not match.empty:
                st.session_state.page = 'admin_panel'
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    
    if st.button("← Volver al Inicio"):
        st.session_state.page = 'home'
        st.rerun()

# --- 3. PANEL DE CONTROL (Añadir canciones) ---
elif st.session_state.page == 'admin_panel':
    st.markdown("<h2 class='hype-title'>PANEL DE CONTROL</h2>", unsafe_allow_html=True)
    
    with st.form("new_song"):
        st.write("### ➕ Añadir Nueva Canción")
        n_nombre = st.text_input("Nombre del Tema")
        n_url = st.text_input("URL de YouTube")
        n_grupo = st.text_input("Grupo (ej: Finales, Grupo B...)")
        
        if st.form_submit_button("PUBLICAR CANCIÓN"):
            if n_nombre and n_url:
                new_row = pd.DataFrame([{"nombre": n_nombre, "url": n_url, "grupo": n_grupo}])
                updated_df = pd.concat([songs_df, new_row], ignore_index=True)
                conn.update(worksheet="wc-songs", data=updated_df)
                st.success("✅ ¡Canción añadida! Los fans ya pueden verla.")
                st.balloons()
            else:
                st.warning("Rellena al menos Nombre y URL")

    if st.button("Cerrar Sesión"):
        st.session_state.page = 'home'
        st.rerun()
