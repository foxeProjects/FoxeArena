"""
Global CSS theme for FOXE Arena.
"""
import base64
from pathlib import Path
import streamlit as st

GOLD = "#f5c542"
GOLD_GLOW = "rgba(245,197,66,0.7)"
DARK_BG = "rgba(20, 20, 20, 0.95)"
GITHUB_ASSETS = "https://raw.githubusercontent.com/foxeProjects/FoxeArena/main/assets"
LOGO_URL = f"{GITHUB_ASSETS}/IMG_9234.png"
BG_URL = f"{GITHUB_ASSETS}/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png"

# Root of the project (where streamlit_app.py lives)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def local_img_to_b64(relative_path: str) -> str | None:
    """Convert a local image (relative to project root) to a base64 data URI."""
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        return None
    data = base64.b64encode(path.read_bytes()).decode()
    suffix = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(suffix, "image/png")
    return f"data:{mime};base64,{data}"


def inject_css():
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

/* ---------- Hide Streamlit chrome ---------- */
#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stDecoration"] {{
    visibility: hidden;
    display: none !important;
}}

/* ---------- Background ---------- */
[data-testid="stAppViewContainer"] {{
    background: linear-gradient(rgba(0,0,0,0.50), rgba(0,0,0,0.88)),
                url("{BG_URL}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    max-width: 540px;
    padding-top: 1rem !important;
}}

/* ---------- Typography ---------- */
h1, h2, h3, h4, p, span, div, label {{
    font-family: 'Inter', sans-serif !important;
}}

/* ---------- Gold accent classes ---------- */
.gold {{ color: {GOLD}; }}
.gold-glow {{ color: {GOLD}; text-shadow: 0 0 15px {GOLD_GLOW}; }}

/* ---------- Section header ---------- */
.section-hdr {{
    text-align: center;
    margin: 5px 0 15px 0;
}}
.section-hdr .title {{
    font-size: 22px;
    font-weight: 900;
    color: {GOLD};
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.section-hdr .sub {{
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    margin-top: -2px;
}}

/* ---------- Generic card ---------- */
.fa-card {{
    background: {DARK_BG};
    border: 1.5px solid rgba(245,197,66,0.35);
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
    box-shadow: 0 0 20px rgba(245,197,66,0.08);
}}
.fa-card.glow {{
    border-color: {GOLD};
    box-shadow: 0 0 40px rgba(245,197,66,0.25);
}}

/* ---------- Video card (banda sonora) ---------- */
.video-card {{
    background: {DARK_BG};
    border: 2px solid {GOLD};
    border-radius: 22px;
    overflow: hidden;
    margin-top: 15px;
    box-shadow: 0 0 30px rgba(245,197,66,0.2);
}}
.video-card.destacado {{
    box-shadow: 0 0 60px rgba(245,197,66,0.6);
    border: 3px solid #ffd700;
}}
.thumb-container {{
    position: relative;
    width: 100%;
    aspect-ratio: 16/9;
    background: #000;
    overflow: hidden;
}}
.thumb-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}
.play-btn {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    width: 55px; height: 55px;
    background: #ff0000;
    border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    box-shadow: 0 0 15px rgba(0,0,0,0.5);
}}
.play-btn::after {{
    content: ''; margin-left: 5px;
    border-left: 14px solid white;
    border-top: 9px solid transparent;
    border-bottom: 9px solid transparent;
}}
.video-info {{ padding: 16px 20px; }}
.v-title {{ font-size: 18px; font-weight: 700; color: {GOLD}; margin-bottom: 2px; }}
.v-sub {{ color: #fff; font-size: 13px; opacity: 0.85; margin-bottom: 10px; }}
.v-link {{ color: {GOLD} !important; font-size: 12px; text-decoration: underline !important; font-weight: 500; }}

/* ---------- Match card ---------- */
.match-card {{
    background: rgba(25,25,25,0.92);
    border: 1px solid rgba(245,197,66,0.25);
    border-radius: 14px;
    padding: 14px 18px;
    margin: 8px 0;
}}
.match-date {{
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
}}
.match-teams {{
    font-size: 16px;
    font-weight: 700;
    color: #fff;
    margin: 6px 0 4px 0;
}}
.match-vs {{
    color: {GOLD};
    font-weight: 400;
    margin: 0 6px;
}}
.match-stadium {{
    font-size: 11px;
    color: rgba(255,255,255,0.4);
}}
.match-num {{
    display: inline-block;
    background: rgba(245,197,66,0.15);
    color: {GOLD};
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 8px;
    margin-bottom: 4px;
}}

/* ---------- Placeholder card ---------- */
.placeholder-card {{
    background: linear-gradient(145deg, rgba(30,30,30,0.95), rgba(15,15,15,0.95));
    border: 2px dashed rgba(245,197,66,0.35);
    border-radius: 20px;
    padding: 35px 20px;
    text-align: center;
    margin: 15px 0;
}}
.placeholder-icon {{
    font-size: 60px;
    margin-bottom: 10px;
}}
.placeholder-title {{
    font-size: 16px;
    font-weight: 800;
    color: {GOLD};
    text-transform: uppercase;
    letter-spacing: 2px;
}}
.placeholder-sub {{
    font-size: 12px;
    color: rgba(255,255,255,0.45);
    margin-top: 5px;
}}

/* ---------- Countdown ---------- */
.countdown-row {{
    display: flex;
    justify-content: center;
    gap: 12px;
    margin: 15px 0;
}}
.cd-box {{
    background: rgba(245,197,66,0.1);
    border: 1px solid rgba(245,197,66,0.3);
    border-radius: 12px;
    padding: 10px 14px;
    text-align: center;
    min-width: 60px;
}}
.cd-num {{
    font-size: 26px;
    font-weight: 900;
    color: {GOLD};
}}
.cd-label {{
    font-size: 9px;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* ---------- Stats row ---------- */
.stats-row {{
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 12px 0;
    flex-wrap: wrap;
}}
.stat-chip {{
    background: rgba(245,197,66,0.08);
    border: 1px solid rgba(245,197,66,0.2);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: rgba(255,255,255,0.8);
    white-space: nowrap;
}}
.stat-chip strong {{
    color: {GOLD};
}}

/* ---------- Scoring table ---------- */
.score-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 10px 0;
    font-size: 13px;
}}
.score-table th {{
    background: rgba(245,197,66,0.15);
    color: {GOLD};
    padding: 10px 12px;
    text-align: left;
    font-weight: 700;
    border-bottom: 2px solid rgba(245,197,66,0.3);
}}
.score-table td {{
    padding: 9px 12px;
    color: rgba(255,255,255,0.85);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}}
.score-table tr:hover td {{
    background: rgba(245,197,66,0.05);
}}

/* ---------- Tabs (main navigation) ---------- */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
    background: rgba(12,12,12,0.75);
    border-radius: 14px;
    padding: 4px 5px;
    justify-content: center;
    border: 1px solid rgba(255,255,255,0.06);
    overflow-x: hidden !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px;
    color: rgba(255,255,255,0.50);
    font-weight: 600;
    font-size: 11px;
    padding: 7px 7px;
    white-space: nowrap;
    flex-shrink: 1;
    min-width: 0;
}}
.stTabs [aria-selected="true"] {{
    background: rgba(245,197,66,0.14) !important;
    color: {GOLD} !important;
    font-weight: 700;
}}
.stTabs [data-baseweb="tab-highlight"] {{
    display: none;
}}
.stTabs [data-baseweb="tab-border"] {{
    display: none;
}}

/* ---------- Selectbox / inputs overrides ---------- */
[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label {{
    color: rgba(255,255,255,0.7) !important;
    font-size: 13px !important;
}}

/* ---------- Group table ---------- */
.group-tbl {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    margin: 10px 0;
}}
.group-tbl th {{
    background: rgba(245,197,66,0.12);
    color: {GOLD};
    padding: 8px 6px;
    text-align: center;
    font-weight: 700;
    font-size: 11px;
    border-bottom: 2px solid rgba(245,197,66,0.25);
}}
.group-tbl th:first-child {{
    text-align: left;
    padding-left: 12px;
}}
.group-tbl td {{
    padding: 8px 6px;
    color: rgba(255,255,255,0.8);
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}}
.group-tbl td:first-child {{
    text-align: left;
    padding-left: 12px;
    font-weight: 600;
    color: #fff;
}}

/* ---------- Foxy quote ---------- */
.foxy-quote {{
    background: linear-gradient(135deg, rgba(245,197,66,0.08), rgba(245,197,66,0.02));
    border-left: 4px solid {GOLD};
    border-radius: 0 14px 14px 0;
    padding: 16px 20px;
    margin: 12px 0;
    font-style: italic;
    color: rgba(255,255,255,0.85);
    font-size: 14px;
}}

/* ---------- Footer ---------- */
.footer-box {{
    text-align: center;
    margin-top: 40px;
    padding-bottom: 30px;
}}
</style>
""", unsafe_allow_html=True)
