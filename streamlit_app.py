import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="FOXE ARENA", page_icon="🏆", layout="centered")

# --- RUTAS ---
LOGO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/6516920E-25CA-423F-AD08-57D6C48BDDE1.png"
ESTADIO = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# --- CSS: PREMIUM DARK (más fiel a tus capturas) ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');

:root {{
  --gold: #f1d592;
  --gold2:#a67c00;
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.55);
  --panel: rgba(10, 15, 13, 0.78);
  --panel2: rgba(10, 15, 13, 0.60);
  --stroke: rgba(241, 213, 146, 0.22);
}}

.stApp {{
  background:
    radial-gradient(1200px 900px at 50% -20%, rgba(241,213,146,0.16), transparent 55%),
    linear-gradient(rgba(0,0,0,0.70), rgba(0,0,0,0.93)),
    url("{ESTADIO}");
  background-size: cover;
  background-attachment: fixed;
  color: var(--text);
  font-family: 'Inter', sans-serif;
}}

.block-container {{
  padding-top: 18px !important;
  padding-bottom: 40px !important;
  max-width: 520px !important;  /* look mobile premium */
}}

a {{
  color: var(--gold);
  text-decoration: none;
}}
a:hover {{ text-decoration: underline; }}

/* Logo */
.foxe-logo {{
  display:flex;
  justify-content:center;
  margin: 6px 0 10px 0;
}}
.foxe-logo img {{
  width: 96px;
  filter: drop-shadow(0 10px 22px rgba(0,0,0,0.55));
}}

/* Header */
.foxe-header {{
  font-family: 'Bebas Neue', sans-serif;
  color: var(--gold);
  text-align: center;
  font-size: 44px;
  letter-spacing: 2px;
  margin: 0;
  text-transform: uppercase;
}}
.foxe-sub {{
  text-align:center;
  color: var(--muted);
  margin-top: -6px;
  margin-bottom: 18px;
  font-size: 14px;
}}

/* Premium card */
.premium-card {{
  border: 1.2px solid rgba(241, 213, 146, 0.35);
  border-radius: 22px;
  padding: 18px 18px 16px 18px;
  background: linear-gradient(180deg, rgba(10,15,13,0.82), rgba(10,15,13,0.70));
  box-shadow:
    0 0 0 1px rgba(241,213,146,0.06) inset,
    0 18px 40px rgba(0,0,0,0.45),
    0 0 26px rgba(241,213,146,0.10);
  backdrop-filter: blur(8px);
  margin-bottom: 18px;
}}

/* Welcome hero panel like screenshot */
.hero {{
  text-align:center;
  padding: 18px 14px 10px 14px;
}}
.hero-title {{
  font-family:'Bebas Neue', sans-serif;
  font-size: 44px;
  color: var(--text);
  margin: 10px 0 6px 0;
  letter-spacing: 1px;
}}
.hero-title span {{
  color: var(--gold);
}}
.hero-copy {{
  color: rgba(255,255,255,0.68);
  font-size: 15px;
  line-height: 1.45;
  margin: 0 auto 14px auto;
  max-width: 360px;
}}
.scroll-hint {{
  display:flex;
  justify-content:center;
  margin-top: 4px;
  opacity: .85;
}}
.scroll-mouse {{
  width: 28px;
  height: 42px;
  border: 2px solid rgba(241,213,146,0.70);
  border-radius: 22px;
  position: relative;
}}
.scroll-mouse::after {{
  content:"";
  width: 6px;
  height: 6px;
  background: rgba(241,213,146,0.95);
  border-radius: 50%;
  position: absolute;
  left: 50%;
  top: 10px;
  transform: translateX(-50%);
  animation: wheel 1.2s infinite ease-in-out;
}}
@keyframes wheel {{
  0% {{ transform: translateX(-50%) translateY(0); opacity: 0.9; }}
  70% {{ transform: translateX(-50%) translateY(14px); opacity: 0.25; }}
  100% {{ transform: translateX(-50%) translateY(0); opacity: 0.9; }}
}}

/* YouTube card */
.yt-card {{
  padding: 0;
  overflow: hidden;
}}
.yt-thumb {{
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(241,213,146,0.18);
}}
.yt-thumb img {{
  width: 100%;
  display: block;
}}
.yt-thumb::before {{
  content:"";
  position:absolute;
  inset:0;
  background: linear-gradient(180deg, rgba(0,0,0,0.05), rgba(0,0,0,0.65));
}}
.play-btn {{
  position:absolute;
  left:50%;
  top:50%;
  transform: translate(-50%, -50%);
  width: 74px;
  height: 74px;
  border-radius: 50%;
  background: rgba(255, 0, 0, 0.92);
  box-shadow: 0 18px 40px rgba(0,0,0,0.55);
  display:flex;
  align-items:center;
  justify-content:center;
}}
.play-btn:before {{
  content:"";
  border-left: 18px solid white;
  border-top: 12px solid transparent;
  border-bottom: 12px solid transparent;
  margin-left: 4px;
}}

.yt-meta {{
  text-align: left;
  padding: 14px 16px 16px 16px;
}}
.yt-title {{
  font-family:'Bebas Neue', sans-serif;
  font-size: 28px;
  margin: 0;
  color: var(--gold);
  letter-spacing: 1px;
}}
.yt-sub {{
  margin: 2px 0 10px 0;
  color: rgba(255,255,255,0.60);
  font-size: 14px;
}}
.yt-link {{
  display:inline-flex;
  gap: 8px;
  align-items:center;
  color: var(--gold);
  font-size: 14px;
}}

/* Inputs */
div[data-baseweb="input"], div[data-baseweb="textarea"] {{
  background-color: rgba(255, 255, 255, 0.04) !important;
  border: 1px solid rgba(241, 213, 146, 0.25) !important;
  border-radius: 14px !important;
}}
input, textarea {{
  color: rgba(255,255,255,0.92) !important;
}}
label {{
  color: rgba(255,255,255,0.70) !important;
}}

/* Buttons */
.stButton>button {{
  background: linear-gradient(180deg, var(--gold) 0%, var(--gold2) 100%) !important;
  color: #141414 !important;
  border: none !important;
  border-radius: 14px !important;
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 22px !important;
  width: 100%;
  transition: transform .08s ease, filter .2s ease;
  height: 48px;
  letter-spacing: 1px;
}}
.stButton>button:hover {{
  filter: brightness(1.05);
}}
.stButton>button:active {{
  transform: scale(0.99);
}}

.secondary-btn .stButton>button {{
  background: transparent !important;
  border: 1px solid rgba(241,213,146,0.65) !important;
  color: var(--gold) !important;
  height: 44px;
  font-size: 18px !important;
}}

/* Song list */
.song-head {{
  font-family:'Bebas Neue', sans-serif;
  color: var(--gold);
  font-size: 22px;
  letter-spacing: 1px;
  margin: 8px 0 8px 0;
}}
.song-item {{
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 14px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid rgba(241, 213, 146, 0.12);
  margin-top: 10px;
}}
.song-name {{
  color: rgba(255,255,255,0.92);
  font-size: 16px;
  font-weight: 700;
  margin: 0;
}}
.song-desc {{
  color: rgba(255,255,255,0.52);
  font-size: 13px;
  margin: 2px 0 0 0;
}}
.song-trash {{
  width: 38px;
  height: 38px;
  border-radius: 12px;
  border: 1px solid rgba(241,213,146,0.22);
  display:flex;
  align-items:center;
  justify-content:center;
  color: var(--gold);
  font-size: 18px;
  background: rgba(241,213,146,0.05);
}}

/* Footer */
.footer-text {{
  text-align: center;
  color: rgba(255,255,255,0.35);
  font-size: 12px;
  margin-top: 24px;
  padding-bottom: 14px;
}}
.footer-text img {{
  width: 28px;
  opacity: 0.92;
  filter: drop-shadow(0 10px 18px rgba(0,0,0,0.55));
}}

/* Reduce top whitespace from Streamlit */
header {{ visibility: hidden; height: 0px; }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if "view" not in st.session_state:
    st.session_state.view = "home"

# --- CABECERA (logo siempre) ---
st.markdown(f'<div class="foxe-logo"><img src="{LOGO}"></div>', unsafe_allow_html=True)

# --- VISTA: ADMIN ---
if st.session_state.view == "admin":
    cols = st.columns([1, 5, 1])
    with cols[0]:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("←", key="back"):
            st.session_state.view = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="foxe-header" style="font-size:40px;margin-bottom:10px;">+ AÑADIR NUEVA CANCIÓN</h2>', unsafe_allow_html=True)

    st.text_input("Nombre", placeholder="Waka Waka")
    st.text_input("URL de YouTube", placeholder="https://youtube.com/...")
    st.text_input("Grupo", placeholder="Clásicos del Mundial")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("AÑADIR CANCIÓN"):
        st.success("✅ Diseño listo (sin conexión).")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="song-head">🎵 LISTA DE CANCIONES (1)</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="song-item">
            <div>
                <p class="song-name">Baila Baila</p>
                <p class="song-desc">Himno Foxe Arena</p>
            </div>
            <div class="song-trash">🗑️</div>
        </div>
    """, unsafe_allow_html=True)

# --- VISTA: HOME ---
else:
    # Header como screenshot
    st.markdown('<h1 class="foxe-header">BANDA SONORA OFICIAL</h1>', unsafe_allow_html=True)
    st.markdown('<div class="foxe-sub">Las últimas canciones añadidas a la porra</div>', unsafe_allow_html=True)

    # Card Youtube (más fiel)
    st.markdown('<div class="premium-card yt-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="yt-thumb">
          <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg" />
          <div class="play-btn"></div>
        </div>
        <div class="yt-meta">
          <p class="yt-title">Baila Baila</p>
          <p class="yt-sub">Himno Foxe Arena</p>
          <a class="yt-link" href="#" target="_blank">🔗 Ver en YouTube</a>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("ENTRAR AL ADMIN PORTAL"):
        st.session_state.view = "admin"
        st.rerun()

# --- FOOTER ---
st.markdown(f"""
<div class="footer-text">
  <img src="{LOGO}"><br>
  © 2026 FOXE ARENA. Todos los derechos reservados.
</div>
""", unsafe_allow_html=True)
