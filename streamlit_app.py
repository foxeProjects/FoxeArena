import streamlit as st
from components.styles import inject_css, LOGO_URL
from components import home, la_porra, banda_sonora, score_ia, grupos

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FOXE ARENA", page_icon="⚽", layout="centered")

inject_css()

# ---------------- LOGO ----------------
st.markdown(
    f'<div style="text-align:center; margin-bottom:6px;">'
    f'<img src="{LOGO_URL}" width="120"></div>',
    unsafe_allow_html=True,
)

# ---------------- NAVIGATION (native tabs) ----------------
tab_home, tab_porra, tab_soundtrack, tab_score, tab_grupos = st.tabs(
    ["\U0001f3e0 Home", "\U0001f3c6 La Porra", "\U0001f3b5 Soundtrack", "\U0001f98a Score-IA", "\u26bd Grupos"]
)

with tab_home:
    home.render()
with tab_porra:
    la_porra.render()
with tab_soundtrack:
    banda_sonora.render()
with tab_score:
    score_ia.render()
with tab_grupos:
    grupos.render()

# ---------------- FOOTER ----------------
st.markdown(
    f'<div class="footer-box">'
    f'<img src="{LOGO_URL}" width="42"><br>'
    f'<div style="font-size:10px; color:rgba(255,255,255,0.35); margin-top:10px;">'
    f'&copy; 2026 FOXE ARENA &middot; Todos los derechos reservados</div></div>',
    unsafe_allow_html=True,
)
