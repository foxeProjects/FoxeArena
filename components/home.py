"""
Home page: Match radar, porra ranking and YouTube channel.
"""
import streamlit as st
import pandas as pd
import re
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from components.styles import PROJECT_ROOT, local_img_to_b64
from data.groups import GROUPS
from data.insights import get_match_insights, is_porra_closed
from data.porra import _safe_int, compute_porra_ranking, display_match_date, display_match_num, load_official_results
from components.grupos import _load_score_ia_predictions

WC_START = datetime(2026, 6, 11, 13, 0, tzinfo=timezone(timedelta(hours=-6)))

YT_LOGO = ("https://upload.wikimedia.org/wikipedia/commons/thumb/"
            "0/09/YouTube_full-color_icon_%282017%29.svg/120px-YouTube_full-color_icon_%282017%29.svg.png")


def _render_porra_ranking():
    ranking = compute_porra_ranking()
    if ranking.empty:
        return
    if ranking["puntos"].max() == 0:
        return

    st.markdown(
        '<div class="section-hdr" style="margin-top:18px;">'
        '<div class="title">CLASIFICACION DE LA PORRA</div>'
        '</div>', unsafe_allow_html=True)

    query = st.text_input("Buscar participante", "", key="home_porra_search")
    visible = ranking
    if query.strip():
        visible = ranking[ranking["participante"].str.contains(query.strip(), case=False, na=False)]

    rows = ""
    for _, row in visible.iterrows():
        pos = int(row["pos"])
        if pos == 1:
            pos_html = '<span style="font-size:30px; line-height:1;">&#127942;</span>'
            row_style = "background:linear-gradient(90deg, rgba(255,215,0,0.24), rgba(245,197,66,0.06));"
            text_size = "16px"
            pts_size = "18px"
        elif pos == 2:
            pos_html = '<span style="font-size:28px; line-height:1;">&#129352;</span>'
            row_style = "background:linear-gradient(90deg, rgba(192,192,192,0.22), rgba(192,192,192,0.05));"
            text_size = "15px"
            pts_size = "17px"
        elif pos == 3:
            pos_html = '<span style="font-size:28px; line-height:1;">&#129353;</span>'
            row_style = "background:linear-gradient(90deg, rgba(205,127,50,0.22), rgba(205,127,50,0.05));"
            text_size = "15px"
            pts_size = "17px"
        else:
            pos_html = str(pos)
            row_style = "background:rgba(255,255,255,0.025);"
            text_size = "13px"
            pts_size = "16px"
        rows += (
            f'<tr style="{row_style}">'
            f'<td style="font-weight:900; color:#f5c542; text-align:center; min-width:54px;">{pos_html}</td>'
            f'<td style="font-weight:700; font-size:{text_size};">{row["participante"]}</td>'
            f'<td style="text-align:right; color:#f5c542; font-weight:900; font-size:{pts_size};">{row["puntos"]}</td></tr>'
        )

    st.markdown(
        '<div class="fa-card" style="padding:14px 10px; overflow-x:auto;">'
        '<table class="score-table"><thead><tr>'
        '<th style="text-align:center;">Pos</th><th>Participante</th><th style="text-align:right;">Pts</th>'
        f'</tr></thead><tbody>{rows}</tbody></table>'
        '</div>',
        unsafe_allow_html=True,
    )


def _countdown():
    now = datetime.now(timezone.utc)
    delta = WC_START - now
    if delta.total_seconds() <= 0:
        return None
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    mins, _ = divmod(rem, 60)
    return days, hours, mins


def _latest_meme_asset():
    def meme_num(path):
        match = re.fullmatch(r"meme(\d+)\.png", path.name.lower())
        return int(match.group(1)) if match else 0

    assets_dir = PROJECT_ROOT / "assets" / "score-ia"
    memes = [p for p in assets_dir.glob("meme*.png") if re.fullmatch(r"meme\d+\.png", p.name.lower())]
    if not memes:
        return None
    return sorted(memes, key=lambda p: (p.stat().st_mtime, meme_num(p)), reverse=True)[0]


def _render_daily_meme():
    meme = _latest_meme_asset()
    if not meme:
        return

    relative_path = meme.relative_to(PROJECT_ROOT).as_posix()
    b64 = local_img_to_b64(relative_path)
    if not b64:
        return

    st.markdown(
        '<div class="section-hdr" style="margin-top:16px;">'
        '<div class="title">MEME SCORE-IA DEL DIA</div>'
        '<div class="sub">El ultimo zarpazo visual de la IA.</div>'
        '</div>'
        '<div class="fa-card" style="padding:10px; overflow:hidden;">'
        f'<img src="{b64}" style="width:100%; display:block; border-radius:14px;">'
        '</div>',
        unsafe_allow_html=True,
    )


def _is_real_match_fixture(group_key: str, team1: str, team2: str) -> bool:
    if group_key in {"1O GRUPO", "2O GRUPO", "MEJOR 3O", "PODIO", "BONUS"}:
        return False
    if group_key in set(GROUPS.keys()):
        return bool(team1) and bool(team2)
    placeholder_tokens = (
        "ganador ",
        "perdedor ",
        " vs ",
        "1a",
        "2a",
        "1b",
        "2b",
        "1c",
        "2c",
        "1d",
        "2d",
        "1e",
        "2e",
        "1f",
        "2f",
        "1g",
        "2g",
        "1h",
        "2h",
        "1i",
        "2i",
        "1j",
        "2j",
        "1k",
        "2k",
        "1l",
        "2l",
        "3o",
    )
    joined = f"{team1} {team2}".lower()
    return bool(team1) and bool(team2) and not any(token in joined for token in placeholder_tokens)


def _get_match_radar_items():
    results_df = load_official_results()
    if results_df.empty:
        return []

    group_details = {}
    for group_letter, group in GROUPS.items():
        for match in group.get("matches", []):
            group_details[match["match_num"]] = {
                "date": match.get("date", ""),
                "stadium": match.get("stadium", ""),
                "group": group_letter,
            }

    matches = []
    excluded = {"1O GRUPO", "2O GRUPO", "MEJOR 3O", "PODIO", "BONUS"}
    for _, row in results_df.iterrows():
        match_num = _safe_int(row.get("match_num"))
        group = str(row.get("group", "")).strip()
        group_key = group.upper()
        team1 = str(row.get("team1", "")).strip()
        team2 = str(row.get("team2", "")).strip()
        has_fixture = _is_real_match_fixture(group_key, team1, team2)
        if match_num is None or not has_fixture:
            continue

        details = group_details.get(match_num, {})
        score1 = _safe_int(row.get("score1"))
        score2 = _safe_int(row.get("score2"))
        classified = "" if pd.isna(row.get("yellow1")) else str(row.get("yellow1", "")).strip()
        is_group_match = group_key in set(GROUPS.keys())
        result = (score1, score2) if score1 is not None and score2 is not None else None
        if not is_group_match and result:
            result = (score1, score2, classified)

        item = {
            "match_num": match_num,
            "group": details.get("group", group),
            "phase": group,
            "date": display_match_date(match_num, row.get("date", "")) or details.get("date", ""),
            "team1": team1,
            "team2": team2,
            "stadium": details.get("stadium", ""),
            "result": result,
            "is_group_match": is_group_match,
        }
        matches.append(item)

    matches = sorted(matches, key=lambda item: item["match_num"])
    previous = [match for match in matches if match["result"]][-2:]
    upcoming = [match for match in matches if not match["result"]][:5]
    return previous + upcoming


def _render_world_cup_progress():
    results_df = load_official_results()
    if results_df.empty:
        return

    rows = []
    for _, row in results_df.iterrows():
        team1 = str(row.get("team1", "")).strip()
        team2 = str(row.get("team2", "")).strip()
        group = str(row.get("group", "")).strip().upper()
        has_fixture = _is_real_match_fixture(group, team1, team2)
        if has_fixture:
            rows.append(row)

    total = 104
    played = 0
    for row in rows:
        group = str(row.get("group", "")).strip().upper()
        is_group_match = group in set(GROUPS.keys())
        classified = "" if row.get("score1") is None else str(row.get("score1", "")).strip()
        if is_group_match and _safe_int(row.get("score1")) is not None and _safe_int(row.get("score2")) is not None:
            played += 1
        elif not is_group_match and classified and classified.lower() != "nan":
            played += 1

    st.markdown(
        '<div class="stats-row" style="margin-bottom:12px;">'
        f'<div class="stat-chip"><strong>{played}/{total}</strong> partidos con resultado</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_match_radar():
    matches = _get_match_radar_items()
    if not matches:
        return

    score_ia_predictions = _load_score_ia_predictions()
    st.markdown(
        '<div class="section-hdr">'
        '<div class="title">RADAR DE PARTIDOS</div>'
        '<div class="sub">Los 2 anteriores y los 5 siguientes para seguir la porra. Para ver otro partido, entra en el grupo correspondiente.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    for match in matches:
        mn = match["match_num"]
        display_mn = display_match_num(mn)
        result = match["result"]
        is_group_match = match.get("is_group_match", True)
        score_ia = score_ia_predictions.get(mn)
        insights = get_match_insights(mn)
        team1_url = quote(match["team1"])
        team2_url = quote(match["team2"])
        score_ia_html = ""
        if score_ia:
            p1, p2 = score_ia
            score_ia_html = (
                '<div style="font-size:11px; color:rgba(245,197,66,0.82); margin-top:6px; font-weight:700;">'
                f'&#129418; SCORE-IA prediction: {p1} - {p2}</div>'
            )

        if result :
            s1, s2 = result[:2]
            teams_html = (
                f'<div class="match-teams"><a class="country-inline-link" href="?country={team1_url}" target="_self">{match["team1"]}</a>'
                f'<span style="color:#f5c542; font-weight:900; margin:0 8px;">{s1} - {s2}</span>'
                f'<a class="country-inline-link" href="?country={team2_url}" target="_self">{match["team2"]}</a></div>'
            )
            if not is_group_match and len(result) > 2 and result[2]:
                winner = result[2]
                # Special badges for FINAL and TERCER PUESTO
                if mn == 136:  # FINAL
                    teams_html += f'<div style="font-size:12px; font-weight:950; margin-top:8px; padding:8px 12px; background:linear-gradient(135deg,#ffd700,#fff0a8); color:#000; border-radius:12px; text-align:center; box-shadow:0 0 16px rgba(255,215,0,0.4);">&#127942; CAMPEON: {winner}</div>'
                elif mn == 135:  # TERCER PUESTO
                    teams_html += f'<div style="font-size:12px; font-weight:950; margin-top:8px; padding:8px 12px; background:linear-gradient(135deg,#cd7f32,#e6a857); color:#fff; border-radius:12px; text-align:center; box-shadow:0 0 16px rgba(205,127,66,0.4);">&#129353; TERCER PUESTO: {winner}</div>'
                else:
                    teams_html += f'<div style="font-size:11px; color:#f5c542; font-weight:900; margin-top:4px;">Clasificado: {winner}</div>'
            card_class = "match-card match-card-finished" if is_group_match else "match-card match-card-knockout-finished"
            badge_class = "match-num match-num-finished" if is_group_match else "match-num match-num-knockout-finished"
            link_class = "match-insight-link match-insight-link-finished"
        else:
            if match["team2"]:
                teams_html = (
                    f'<div class="match-teams"><a class="country-inline-link" href="?country={team1_url}" target="_self">{match["team1"]}</a>'
                    f'<span class="match-vs">vs</span>'
                    f'<a class="country-inline-link" href="?country={team2_url}" target="_self">{match["team2"]}</a></div>'
                )
            else:
                teams_html = f'<div class="match-teams">{match["team1"]}</div>'
            if is_group_match:
                card_class = "match-card match-card-pending"
                badge_class = "match-num match-num-pending"
            elif result:
                card_class = "match-card match-card-knockout-finished"
                badge_class = "match-num match-num-knockout-finished"
            else:
                card_class = "match-card match-card-knockout-pending"
                badge_class = "match-num match-num-knockout-pending"
            link_class = "match-insight-link match-insight-link-pending"

        insight_html = ""
        if is_group_match and insights and insights["total"]:
            options = [
                (insights["home_win"], match["team1"]),
                (insights["draw"], "Empate"),
                (insights["away_win"], match["team2"]),
            ]
            top_votes, top_pick = max(options, key=lambda item: item[0])
            top_pct = round((top_votes / insights["total"]) * 100)
            score_counts = insights["score_counts"]
            top_score = next(iter(score_counts)) if score_counts else ""
            score_text = f" · marcador mas repetido: {top_score}" if top_score else ""
            insight_html = (
                '<div style="font-size:11px; color:rgba(245,197,66,0.86); margin-top:5px; font-weight:800;">'
                f'&#128200; La porra va con {top_pick} ({top_pct}%){score_text}</div>'
            )

        phase_label = f'Grupo {match["group"]}' if is_group_match else match["phase"]
        stadium_html = f'<div class="match-stadium">&#127967; {match["stadium"]}</div>' if match["stadium"] else ""
        dashboard_html = (
            f'<a class="{link_class}" href="?match={mn}" target="_self">&#128202; Abrir dashboard del partido</a>'
        )

        st.markdown(
            f'<div class="{card_class}">'
            f'<div class="{badge_class}">Partido {display_mn}</div>'
            f'<div style="font-size:10px; color:rgba(255,255,255,0.42); font-weight:800; margin-bottom:4px;">{match["date"]} 2026 · {phase_label}</div>'
            f'{teams_html}'
            f'{insight_html}'
            f'{score_ia_html}'
            f'{stadium_html}'
            f'{dashboard_html}'
            '</div>',
            unsafe_allow_html=True,
        )


def render():
    if is_porra_closed():
        _render_world_cup_progress()
        _render_daily_meme()
        _render_match_radar()
    else:
        cd = _countdown()
        if cd:
            d, h, m = cd
            st.markdown(
                '<div class="fa-card glow" style="text-align:center; padding:18px;">'
                '<div style="font-size:11px; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:2px; margin-bottom:8px;">'
                'Cuenta atras para el Mundial 2026</div>'
                '<div class="countdown-row">'
                f'<div class="cd-box"><div class="cd-num">{d}</div><div class="cd-label">Dias</div></div>'
                f'<div class="cd-box"><div class="cd-num">{h}</div><div class="cd-label">Horas</div></div>'
                f'<div class="cd-box"><div class="cd-num">{m}</div><div class="cd-label">Min</div></div>'
                '</div>'
                '<div style="font-size:12px; color:rgba(255,255,255,0.6);">11 de junio de 2026 &middot; Kick-Off</div>'
                '</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="fa-card glow" style="text-align:center;">'
                '<div style="font-size:28px; font-weight:900; color:#f5c542;">EL MUNDIAL YA HA COMENZADO</div>'
                '</div>', unsafe_allow_html=True)

        portada = local_img_to_b64("assets/score-ia/portada.png")
        if portada:
            st.markdown(
                '<div style="border-radius:20px; overflow:hidden; margin:14px 0; border:2px solid rgba(245,197,66,0.35); box-shadow:0 0 30px rgba(245,197,66,0.14);">'
                f'<img src="{portada}" style="width:100%; display:block;">'
                '</div>', unsafe_allow_html=True)
    if is_porra_closed():
        _render_porra_ranking()

    st.markdown(
        '<div class="fa-card" style="text-align:center; padding:20px;">'
        f'<img src="{YT_LOGO}" width="48" style="margin-bottom:10px;">'
        '<div style="font-size:13px; color:rgba(255,255,255,0.55); margin-bottom:6px;">Canal oficial</div>'
        '<a href="https://www.youtube.com/@foxearena" target="_blank"'
        ' style="font-size:20px; font-weight:800; color:#f5c542; text-decoration:none;">'
        '@foxearena</a>'
        '</div>', unsafe_allow_html=True)
