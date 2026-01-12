import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS [Asegúrate de que estas URLs sean correctas] ---
LOGO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- CSS: ESTILO PREMIUM DARK ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;700&display=swap');

    /* Fondo general */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.95)), 
                    url("{ESTADIO}");
        background-size: cover;
        background-attachment: fixed;
        color: white;
        font-family: 'Inter', sans-serif;
    }}

    /* Contenedores con borde dorado y resplandor (Glow) */
    .premium-card {{
        border: 1.5px solid #f1d592;
        border-radius: 20px;
        padding: 20px;
        background-color: rgba(10, 15, 13, 0.85);
        box-shadow: 0 0 20px rgba(241, 213, 146, 0.15);
        margin-bottom: 25px;
    }}

    /* Títulos estilo Foxe */
    .foxe-header {{
        font-family: 'Bebas Neue', cursive;
        color: #f1d592;
        text-align: center;
        font-size: 2.8rem;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }}

    /* Inputs personalizados (Parecidos a tus capturas) */
    div[data-baseweb="input"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(241, 213, 146, 0.3) !important;
        border-radius: 12px !important;
    }}
    
    input {{
        color: white !important;
    }}

    /* Botón Principal (Amarillo/Dorado sólido) */
    .stButton>button {{
        background: linear-gradient(180deg, #f1d592 0%, #a67c00 100%) !important;
        color: black !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.4rem !important;
        width: 100%;
        transition: 0.3s;
        height: 3rem;
    }}

    /* Botón Secundario (Cerrar Sesión / Vacío) */
    .logout-btn>div>button {{
        background: transparent !important;
        border: 1px solid #f1d592 !important;
        color: #f1d592 !important;
        font-size: 1rem !important;
    }}

    /* Estilo para la lista de canciones inferior */
    .song-item {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(241, 213, 146, 0.1);
        margin-top: 10px;
    }}

    .footer-text {{
        text-align: center;
        color: rgba(255,255,255,0.4);
        font-size: 0.8rem;
        margin-top: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN SIMPLE ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- INTERFAZ: CABECERA ---
st.markdown(f'<div style="text-align:center"><img src="{LOGO}" width="120"></div>', unsafe_allow_html=True)

# --- VISTA: ADMIN (Basada en tu captura de "Añadir Nueva Canción") ---
if st.session_state.view == 'admin':
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("←", key="back"): st.session_state.view = 'home'; st.rerun()
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="foxe-header">+ AÑADIR NUEVA CANCIÓN</h2>', unsafe_allow_html=True)
    
    st.text_input("Nombre", placeholder="Waka Waka")
    st.text_input("URL de YouTube", placeholder="https://youtube.com/...")
    st.text_input("Grupo", placeholder="Clásicos del Mundial")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("AÑADIR CANCIÓN"):
        st.success("Canción añadida correctamente")
    st.markdown('</div>', unsafe_allow_html=True)

    # Lista de canciones (mini card)
    st.markdown('<h4 style="color:#f1d592; font-family:Bebas Neue;">🎵 LISTA DE CANCIONES (1)</h4>', unsafe_allow_html=True)
    st.markdown("""
        <div class="song-item">
            <div>
                <b style="color:white; font-size:1.2rem;">Baila Baila</b><br>
                <span style="color:gray;">Himno Foxe Arena</span>
            </div>
            <div style="color:#f1d592; font-size:1.5rem;">🗑️</div>
        </div>
    """, unsafe_allow_html=True)

# --- VISTA: HOME (Basada en tu captura de Video) ---
else:
    st.markdown('<h1 class="foxe-header">BANDA SONORA OFICIAL</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray; margin-top:-10px;'>Las últimas canciones añadidas a la porra</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    # Simulación de la miniatura de video con el play rojo central
    st.image("https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg") # Aquí iría el cover del video
    st.markdown("""
        <div style="text-align:center; padding-top:15px;">
            <h2 style="color:#f1d592; font-family:Bebas Neue; margin:0;">Baila Baila</h2>
            <p style="color:gray;">Himno Foxe Arena</p>
            <a href="#" style="color:#f1d592; text-decoration:none; font-size:0.9rem;">🔗 Ver en YouTube</a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("ENTRAR AL ADMIN PORTAL"):
        st.session_state.view = 'admin'
        st.rerun()

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-text">
        <img src="{LOGO}" width="30"><br>
        © 2026 FOXE ARENA. Todos los derechos reservados.
    </div>
""", unsafe_allow_html=True)
