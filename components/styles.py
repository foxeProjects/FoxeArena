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
    font-size: 12px;
    color: rgba(255,255,255,0.72);
    font-weight: 650;
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
.match-card-pending {{
    border-color: rgba(88,166,255,0.28);
}}
.match-card-finished {{
    border-color: rgba(99,186,104,0.42);
    background: linear-gradient(145deg, rgba(22,32,24,0.94), rgba(14,14,14,0.94));
}}
.match-card-knockout {{
    border-color: rgba(158,54,103,0.45);
    background: linear-gradient(145deg, rgba(35,15,28,0.94), rgba(14,14,14,0.94));
}}
.match-card-knockout-pending {{
    border-color: rgba(158,54,103,0.45);
    background: linear-gradient(145deg, rgba(35,15,28,0.94), rgba(14,14,14,0.94));
}}
.match-card-knockout-finished {{
    border-color: rgba(245,197,66,0.58);
    background: linear-gradient(145deg, rgba(58,43,12,0.96), rgba(16,12,6,0.96));
    box-shadow: 0 0 24px rgba(245,197,66,0.16);
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
.match-num-pending {{
    background: rgba(88,166,255,0.14);
    color: #85a4ff;
    border: 1px solid rgba(88,166,255,0.24);
}}
.match-num-finished {{
    background: rgba(99,186,104,0.15);
    color: #63ba68;
    border: 1px solid rgba(99,186,104,0.28);
}}
.match-num-knockout {{
    background: rgba(158,54,103,0.18);
    color: #c587a4;
    border: 1px solid rgba(158,54,103,0.34);
}}
.match-num-knockout-pending {{
    background: rgba(158,54,103,0.18);
    color: #c587a4;
    border: 1px solid rgba(158,54,103,0.34);
}}
.match-num-knockout-finished {{
    background: rgba(245,197,66,0.20);
    color: #f5c542;
    border: 1px solid rgba(245,197,66,0.42);
}}
.match-insight-link {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin-top: 10px;
    padding: 7px 10px;
    border-radius: 999px;
    background: rgba(245,197,66,0.12);
    border: 1px solid rgba(245,197,66,0.28);
    color: {GOLD} !important;
    font-size: 11px;
    font-weight: 900;
    text-decoration: none !important;
}}
.match-insight-link:hover {{
    background: rgba(245,197,66,0.2);
    border-color: rgba(245,197,66,0.55);
}}
.match-insight-link-pending {{
    background: rgba(88,166,255,0.10);
    border-color: rgba(88,166,255,0.26);
    color: #85a4ff !important;
}}
.match-insight-link-pending:hover {{
    background: rgba(88,166,255,0.18);
    border-color: rgba(88,166,255,0.48);
}}
.match-insight-link-finished {{
    background: rgba(99,186,104,0.12);
    border-color: rgba(99,186,104,0.30);
    color: #63ba68 !important;
}}
.match-insight-link-finished:hover {{
    background: rgba(99,186,104,0.20);
    border-color: rgba(99,186,104,0.52);
}}
.scoremap-wrap {{
    overflow-x: auto;
    padding-bottom: 2px;
}}
.scoremap-row {{
    display: grid;
    grid-template-columns: 34px repeat(9, minmax(42px, 1fr));
    gap: 5px;
    min-width: 440px;
    margin-bottom: 5px;
}}
.scoremap-cell {{
    min-height: 42px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 800;
}}
.scoremap-cell span {{
    font-size: 10px;
    opacity: 0.78;
}}
.scoremap-cell strong {{
    font-size: 15px;
    line-height: 1.1;
}}
.scoremap-axis,
.scoremap-corner {{
    min-height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.46);
    font-size: 10px;
    font-weight: 900;
}}
.match-kpi-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin: 12px 0;
}}
.match-kpi-card {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, rgba(25,25,25,0.96), rgba(8,8,8,0.96));
    border: 1px solid rgba(245,197,66,0.26);
    border-radius: 16px;
    padding: 14px 12px;
    min-height: 104px;
    text-align: center;
    box-shadow: 0 0 22px rgba(245,197,66,0.07);
}}
.match-kpi-card::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top right, rgba(245,197,66,0.18), transparent 45%);
    pointer-events: none;
}}
.match-kpi-icon {{
    position: relative;
    width: 30px;
    height: 30px;
    margin: 0 auto 6px auto;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(245,197,66,0.12);
    color: {GOLD};
    font-size: 15px;
}}
.match-kpi-value {{
    position: relative;
    color: {GOLD};
    font-size: 25px;
    line-height: 1;
    font-weight: 950;
    letter-spacing: -0.8px;
}}
.match-kpi-label {{
    position: relative;
    margin-top: 6px;
    color: #fff;
    font-size: 11px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}}
.match-kpi-sub {{
    position: relative;
    margin-top: 4px;
    color: rgba(255,255,255,0.45);
    font-size: 10px;
    line-height: 1.25;
}}
.match-banner-card {{
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    border: 1.5px solid rgba(245,197,66,0.35);
    aspect-ratio: 16 / 9;
    margin: 12px 0;
    background: #050505;
    box-shadow: 0 0 28px rgba(245,197,66,0.12);
}}
.match-banner-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}
.match-banner-placeholder {{
    border-radius: 20px;
    border: 2px dashed rgba(245,197,66,0.34);
    aspect-ratio: 16 / 9;
    margin: 12px 0;
    background:
        radial-gradient(circle at 20% 15%, rgba(245,197,66,0.14), transparent 28%),
        linear-gradient(145deg, rgba(26,26,26,0.96), rgba(7,7,7,0.96));
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 18px;
    box-shadow: inset 0 0 45px rgba(245,197,66,0.05);
}}
.match-event-card {{
    margin: 12px 0 16px 0;
    padding: 15px;
    border-radius: 22px;
    background:
        radial-gradient(circle at 50% 0%, rgba(245,197,66,0.14), transparent 30%),
        linear-gradient(145deg, rgba(18,18,18,0.98), rgba(7,7,7,0.98));
    border: 1.5px solid rgba(245,197,66,0.28);
    box-shadow: 0 0 28px rgba(245,197,66,0.10);
}}
.match-event-photo {{
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
}}
.match-event-img {{
    width: min(100%, 330px);
    max-height: 520px;
    aspect-ratio: 9 / 16;
    object-fit: cover;
    border-radius: 20px;
    border: 2px solid rgba(245,197,66,0.32);
    box-shadow: 0 0 28px rgba(245,197,66,0.14);
}}
.match-event-placeholder {{
    width: min(100%, 330px);
    aspect-ratio: 9 / 16;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 20px;
    border: 2px dashed rgba(245,197,66,0.34);
    color: {GOLD};
    font-size: 16px;
    font-weight: 950;
    text-align: center;
}}
.match-event-placeholder span {{
    color: rgba(255,255,255,0.42);
    font-size: 10px;
    margin-top: 8px;
}}
.match-experience-card {{
    margin: -2px 0 14px 0;
    padding: 14px 15px;
    border-radius: 18px;
    background:
        radial-gradient(circle at 15% 0%, rgba(245,197,66,0.12), transparent 28%),
        linear-gradient(145deg, rgba(18,18,18,0.98), rgba(7,7,7,0.98));
    border: 1px solid rgba(245,197,66,0.22);
    box-shadow: 0 0 22px rgba(245,197,66,0.08);
}}
.match-experience-title {{
    color: {GOLD};
    font-size: 13px;
    font-weight: 950;
    text-align: center;
    margin-bottom: 8px;
}}
.match-experience-food {{
    color: rgba(255,255,255,0.88);
    font-size: 13px;
    font-weight: 800;
    text-align: center;
    margin-top: 6px;
}}
.match-experience-food strong {{
    color: {GOLD};
}}
.match-experience-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}}
.match-experience-panel {{
    background: rgba(0,0,0,0.18);
    border: 1px solid rgba(245,197,66,0.16);
    border-radius: 14px;
    padding: 12px;
    min-height: 92px;
}}
.match-experience-songs {{
    display: flex;
    flex-direction: column;
    gap: 6px;
    align-items: center;
    margin-top: 6px;
}}
.match-experience-label {{
    color: rgba(255,255,255,0.46);
    font-size: 10px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .08em;
}}
.match-experience-songs a,
.match-experience-songs span {{
    color: rgba(245,197,66,0.88) !important;
    font-size: 11px;
    font-weight: 850;
    text-decoration: none !important;
    text-align: center;
}}
.yt-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 12px;
    margin-right: 6px;
    border-radius: 4px;
    background: #ff0000;
    color: #ffffff !important;
    font-size: 8px;
    line-height: 1;
    vertical-align: 1px;
}}
.match-experience-songs em {{
    color: rgba(255,255,255,0.45);
    font-style: normal;
    font-weight: 700;
}}
@media (max-width: 720px) {{
    .match-experience-grid {{
        grid-template-columns: 1fr;
    }}
}}
.country-inline-link {{
    color: inherit !important;
    text-decoration: none !important;
    font-weight: 800;
}}
.country-inline-link:hover {{
    color: {GOLD} !important;
    text-shadow: 0 0 12px rgba(245,197,66,0.3);
}}
.country-match-nav {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: -4px 0 12px 0;
}}
.country-match-nav a {{
    color: {GOLD} !important;
    text-decoration: none !important;
    font-size: 13px;
    font-weight: 950;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(245,197,66,0.1);
    border: 1px solid rgba(245,197,66,0.22);
}}
.country-match-nav span {{
    color: rgba(255,255,255,0.42);
    font-size: 11px;
    font-weight: 900;
}}
.country-hero-card {{
    border-radius: 20px;
    overflow: hidden;
    border: 1.5px solid rgba(245,197,66,0.35);
    margin: 12px 0;
    background: #050505;
    box-shadow: 0 0 28px rgba(245,197,66,0.12);
}}
.country-hero-img {{
    width: 100%;
    display: block;
}}
.country-hero-placeholder {{
    border-radius: 20px;
    border: 2px dashed rgba(245,197,66,0.34);
    margin: 12px 0;
    background: linear-gradient(145deg, rgba(26,26,26,0.96), rgba(7,7,7,0.96));
    min-height: 250px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 18px;
}}
.country-info-card {{
    padding: 16px !important;
    text-align: center;
}}
.country-card-title {{
    color: {GOLD};
    font-size: 14px;
    font-weight: 950;
    text-align: center;
    margin-bottom: 10px;
}}
.country-recipe-grid {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
}}
.country-recipe-chip {{
    color: rgba(255,255,255,0.86);
    background: rgba(245,197,66,0.08);
    border: 1px solid rgba(245,197,66,0.20);
    border-radius: 999px;
    padding: 7px 11px;
    font-size: 12px;
    font-weight: 800;
}}
.country-match-card {{
    display: block;
    border-radius: 14px;
    padding: 12px 13px;
    margin: 8px 0;
    text-decoration: none !important;
    background: linear-gradient(145deg, rgba(20,20,20,0.96), rgba(10,10,10,0.96));
    border: 1px solid rgba(245,197,66,0.18);
}}
.country-match-pending {{
    border-color: rgba(88,166,255,0.34);
    background: linear-gradient(145deg, rgba(14,24,38,0.96), rgba(8,10,14,0.96));
}}
.country-match-finished {{
    border-color: rgba(99,186,104,0.42);
    background: linear-gradient(145deg, rgba(14,34,20,0.96), rgba(8,12,9,0.96));
}}
.country-match-knockout {{
    border-color: rgba(158,54,103,0.42);
    background: linear-gradient(145deg, rgba(35,15,28,0.96), rgba(8,8,10,0.96));
}}
.country-match-knockout-pending {{
    border-color: rgba(158,54,103,0.42);
    background: linear-gradient(145deg, rgba(35,15,28,0.96), rgba(8,8,10,0.96));
}}
.country-match-knockout-finished {{
    border-color: rgba(245,197,66,0.58);
    background: linear-gradient(145deg, rgba(58,43,12,0.96), rgba(8,8,10,0.96));
    box-shadow: 0 0 22px rgba(245,197,66,0.14);
}}
.country-match-num {{
    color: {GOLD};
    font-size: 10px;
    font-weight: 950;
    margin-right: 8px;
}}
.country-match-date {{
    color: rgba(255,255,255,0.45);
    font-size: 10px;
    font-weight: 800;
}}
.country-match-teams {{
    color: #fff;
    font-size: 14px;
    font-weight: 900;
    margin-top: 6px;
}}
.country-match-teams span {{
    color: {GOLD};
    margin: 0 6px;
}}
.country-match-stadium {{
    color: rgba(255,255,255,0.42);
    font-size: 10px;
    margin-top: 5px;
}}
.country-scoreia-tip {{
    color: rgba(245,197,66,0.86);
    background: rgba(245,197,66,0.07);
    border: 1px solid rgba(245,197,66,0.13);
    border-radius: 10px;
    padding: 7px 9px;
    font-size: 11px;
    font-weight: 850;
    line-height: 1.35;
    margin-top: 8px;
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
