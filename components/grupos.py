"""
Grupos page: Browse groups A-L with standings table and match calendar.
Standings and scores are read live from the wc-results Google Sheet.
"""
import streamlit as st
import random
import csv
from data.groups import GROUPS, GROUP_LETTERS
from data.results import compute_standings, get_match_scores
from components.styles import PROJECT_ROOT, local_img_to_b64

SCORE_IA_GROUP_TEASERS = [
    "SCORE-IA ya ha visto este grupo. No todos salen bien parados.",
    "Hay datos. Hay favoritos. Y luego esta tu intuicion.",
    "La estadistica tiene una opinion y viene con mala leche.",
    "SCORE-IA ha calculado el grupo. El drama viene incluido.",
    "Antes de apostar con el corazon, consulta al zorro sin alma.",
    "El algoritmo ya eligio a quien hundir primero.",
    "Este grupo parece tranquilo hasta que SCORE-IA abre la boca.",
    "Spoiler: los datos no son tan romanticos como tu porra.",
]


@st.cache_data(ttl=60)
def _load_score_ia_predictions():
    path = PROJECT_ROOT / "assets" / "wc-participantes-score-ia.csv"
    predictions = {}
    if not path.exists():
        return predictions
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                match_num = int(row.get("match_num", ""))
                pred1 = row.get("pred1", "").strip()
                pred2 = row.get("pred2", "").strip()
                if pred1 != "" and pred2 != "":
                    predictions[match_num] = (int(pred1), int(pred2))
            except (TypeError, ValueError):
                continue
    return predictions


def _render_banner(group_data):
    banner_path = group_data.get("banner")
    b64 = local_img_to_b64(banner_path) if banner_path else None
    if b64:
        st.markdown(
            '<div style="border-radius:16px; overflow:hidden; margin-bottom:12px; border:2px solid rgba(245,197,66,0.3); aspect-ratio: 16 / 9;">'
            f'<img src="{b64}" style="width:100%; height:100%; object-fit:cover; display:block;">'
            '</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="placeholder-card" style="padding:30px 15px; margin-bottom:12px; aspect-ratio: 16 / 9; display:flex; flex-direction:column; justify-content:center;">'
            '<div style="font-size:40px;">&#127944;</div>'
            '<div class="placeholder-title" style="font-size:14px;">Banner del Grupo</div>'
            '<div class="placeholder-sub">Proximamente</div>'
            '</div>', unsafe_allow_html=True)


def _render_table(group_letter):
    """Render standings calculated from real results."""
    teams = compute_standings(group_letter)

    header = "<tr><th>Seleccion</th><th>Pts</th><th>PJ</th><th>PG</th><th>PE</th><th>PP</th><th>GF</th><th>GC</th><th>Dif</th></tr>"
    rows = ""
    for t in teams:
        pts_style = ' style="color:#f5c542; font-weight:700;"' if t["pts"] > 0 else ""
        rows += (f'<tr><td>{t["name"]}</td>'
                 f'<td{pts_style}>{t["pts"]}</td><td>{t["pj"]}</td><td>{t["pg"]}</td>'
                 f'<td>{t["pe"]}</td><td>{t["pp"]}</td><td>{t["gf"]}</td>'
                 f'<td>{t["gc"]}</td><td>{t["dif"]}</td></tr>')

    st.markdown(
        '<div class="fa-card" style="padding:14px 10px; overflow-x:auto;">'
        '<div style="font-size:14px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:10px;">'
        'CLASIFICACION</div>'
        f'<table class="group-tbl"><thead>{header}</thead><tbody>{rows}</tbody></table>'
        '</div>', unsafe_allow_html=True)


def _render_score_ia_link(group_letter):
    teaser = random.choice(SCORE_IA_GROUP_TEASERS)
    st.markdown(
        '<div style="text-align:center; margin:10px 0 14px 0; line-height:1.5;">'
        f'<div style="font-size:12px; color:rgba(255,255,255,0.55); font-style:italic;">&#129418; {teaser}</div>'
        '</div>', unsafe_allow_html=True)


def _render_calendar(group_data, group_letter):
    """Render match calendar. Shows scores for played matches."""
    matches = group_data["matches"]
    if not matches:
        return

    scores = get_match_scores(group_letter)
    score_ia_predictions = _load_score_ia_predictions()

    st.markdown(
        '<div style="font-size:14px; font-weight:800; color:#f5c542; text-align:center; margin:16px 0 8px 0;">'
        'CALENDARIO</div>', unsafe_allow_html=True)

    by_date = {}
    for m in matches:
        by_date.setdefault(m["date"], []).append(m)

    for date, ms in by_date.items():
        st.markdown(
            f'<div style="font-size:12px; font-weight:700; color:rgba(255,255,255,0.5); text-transform:uppercase; '
            f'letter-spacing:1px; margin:12px 0 6px 14px;">{date} 2026</div>',
            unsafe_allow_html=True)
        for m in ms:
            mn = m["match_num"]
            result = scores.get(mn)
            score_ia = score_ia_predictions.get(mn)
            score_ia_html = ""
            if score_ia:
                p1, p2 = score_ia
                score_ia_html = (
                    '<div style="font-size:11px; color:rgba(245,197,66,0.82); margin-top:6px; font-weight:700;">'
                    f'&#129418; SCORE-IA prediction: {p1} - {p2}</div>'
                )

            if result:
                s1, s2 = result
                teams_html = (
                    f'<div class="match-teams">{m["team1"]}'
                    f'<span style="color:#f5c542; font-weight:900; margin:0 8px;">{s1} - {s2}</span>'
                    f'{m["team2"]}</div>'
                )
                card_style = 'border-color: rgba(245,197,66,0.4);'
            else:
                teams_html = (
                    f'<div class="match-teams">{m["team1"]}'
                    f'<span class="match-vs">vs</span>'
                    f'{m["team2"]}</div>'
                )
                card_style = ''

            st.markdown(
                f'<div class="match-card" style="{card_style}">'
                f'<div class="match-num">Partido {mn}</div>'
                f'{teams_html}'
                f'{score_ia_html}'
                f'<div class="match-stadium">&#127967; {m["stadium"]}</div>'
                '</div>', unsafe_allow_html=True)


def render():
    st.markdown(
        '<div class="section-hdr">'
        '<div class="title">GRUPOS</div>'
        '</div>', unsafe_allow_html=True)

    options = [f"Grupo {g}" for g in GROUP_LETTERS]
    selected = st.selectbox("Selecciona un grupo", options, key="grp_select")
    letter = selected.replace("Grupo ", "")
    group = GROUPS[letter]

    _render_banner(group)
    _render_score_ia_link(letter)
    _render_table(letter)
    _render_calendar(group, letter)
