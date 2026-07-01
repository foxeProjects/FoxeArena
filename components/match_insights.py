import html
import random
import streamlit as st
from data.groups import GROUPS
from data.countries import get_country_recipes, get_country_song
from data.insights import get_match_insights
from data.porra import compute_porra_ranking, display_match_date, display_match_num, load_official_results, load_participants
from components.styles import local_img_to_b64

SCORE_IA_PENDING_MESSAGES = [
    "SCORE-IA esta afilando las garras. Cuando llegue el resultado oficial, separara a los visionarios de los vendehumos.",
    "El zorro ya huele sangre estadistica. Falta el pitido final para saber quien iba sobrado y quien iba borracho.",
    "SCORE-IA tiene la libreta preparada. En cuanto haya resultado, empiezan los juicios sumarísimos.",
    "De momento todos sois genios. Luego llega el marcador oficial y se acaba la fantasia.",
    "El algoritmo no olvida. Cada 3-3 romantico quedara registrado para futuras humillaciones.",
    "Aun no hay veredicto, pero SCORE-IA ya esta mirando algunas predicciones con desprecio preventivo.",
    "Cuando ruede el balon, la poesia muere y empieza la contabilidad del dolor.",
    "El zorro espera en silencio. Los marcadores exactos no se celebran solos.",
    "Todavia no hay cadaveres estadisticos. Dale tiempo al partido.",
    "SCORE-IA recomienda hidratarse: algunos van a necesitar agua para tragarse su prediccion.",
    "Sin resultado oficial no hay sangre. Solo promesas, humo y algun 0-0 sospechoso.",
    "El dashboard esta en modo calma antes del zasca.",
    "Aun no sabemos quien acerto, pero el zorro ya tiene favoritos para el museo del ridiculo.",
    "Cuando llegue el resultado, este bloque se llenara de heroes, villanos y empates cobardes.",
    "SCORE-IA no juzga antes de tiempo. Bueno, un poco si.",
    "El partido aun no ha hablado. La porra, como siempre, ya ha gritado demasiado.",
    "Aqui apareceran los francotiradores del marcador exacto. Si existen. Si no, haremos leña.",
    "El zorro esta calibrando el detector de vendehumos.",
    "Falta el resultado oficial para convertir intuiciones en puntos o en memes.",
    "Paciencia. La estadistica tarda, pero cuando llega no pide perdon.",
]


def _find_match(match_num: int):
    for group_letter, group_data in GROUPS.items():
        for match in group_data.get("matches", []):
            if match.get("match_num") == match_num:
                return group_letter, match
    return None, None


def _find_knockout_match(match_num: int):
    results = load_official_results()
    if results.empty:
        return None
    rows = results[results["match_num"] == match_num]
    if rows.empty:
        return None
    row = rows.iloc[0]
    group = str(row.get("group", "")).strip()
    if group.upper() in set(GROUPS.keys()) | {"1O GRUPO", "2O GRUPO", "MEJOR 3O", "PODIO", "BONUS"}:
        return None
    team1 = str(row.get("team1", "")).strip()
    team2 = str(row.get("team2", "")).strip()
    if team2.lower() == "nan":
        team2 = ""
    if not team1:
        return None
    classified = str(row.get("yellow1", "")).strip()
    if classified.lower() == "nan":
        classified = ""
    date = display_match_date(match_num, row.get("date", ""))
    return {
        "match_num": match_num,
        "group": group,
        "date": date,
        "team1": team1,
        "team2": team2,
        "classified": classified,
    }


def _intensity_color(value: int, max_value: int) -> str:
    if value <= 0 or max_value <= 0:
        return "rgba(255,255,255,0.035)"
    ratio = value / max_value
    if ratio >= 0.75:
        return "linear-gradient(145deg,#f5c542,#fff0a8)"
    if ratio >= 0.45:
        return "linear-gradient(145deg,#b88716,#f5c542)"
    if ratio >= 0.20:
        return "linear-gradient(145deg,rgba(245,197,66,0.34),rgba(245,197,66,0.18))"
    return "linear-gradient(145deg,rgba(245,197,66,0.16),rgba(245,197,66,0.08))"


def _render_scoremap(insights: dict, team1: str, team2: str):
    score_counts = insights.get("score_counts_full", {})
    if not score_counts:
        st.info("Todavia no hay marcadores cargados para este partido.")
        return

    max_goal = min(max(int(insights.get("max_goal", 5)), 5), 8)
    max_count = max(score_counts.values()) if score_counts else 1
    grid_style = f"grid-template-columns:34px repeat({max_goal + 1}, minmax(42px, 1fr));"
    rows = ""
    for home_goals in range(max_goal + 1):
        cells = f'<div class="scoremap-axis">{home_goals}</div>'
        for away_goals in range(max_goal + 1):
            key = f"{home_goals}-{away_goals}"
            value = int(score_counts.get(key, 0))
            bg = _intensity_color(value, max_count)
            text_color = "#111" if value and value / max_count >= 0.45 else "rgba(255,255,255,0.86)"
            shadow = "0 0 22px rgba(245,197,66,0.35)" if value == max_count else "none"
            cells += (
                f'<div class="scoremap-cell" title="{html.escape(key)}: {value} predicciones" '
                f'style="background:{bg}; color:{text_color}; box-shadow:{shadow};">'
                f'<span>{home_goals}-{away_goals}</span><strong>{value}</strong></div>'
            )
        rows += f'<div class="scoremap-row" style="{grid_style}">{cells}</div>'

    header_cells = '<div class="scoremap-corner"></div>'
    for away_goals in range(max_goal + 1):
        header_cells += f'<div class="scoremap-axis">{away_goals}</div>'

    st.markdown(
        '<div class="fa-card glow" style="padding:16px;">'
        '<div style="text-align:center; color:#f5c542; font-size:16px; font-weight:900; margin-bottom:4px;">Scoremap de marcadores</div>'
        f'<div style="text-align:center; color:rgba(255,255,255,0.58); font-size:11px; margin-bottom:12px;">Filas: {html.escape(team1)} · Columnas: {html.escape(team2)}</div>'
        '<div class="scoremap-wrap">'
        f'<div class="scoremap-row" style="{grid_style}">{header_cells}</div>'
        f'{rows}'
        '</div>'
        '<div style="display:flex; justify-content:space-between; gap:8px; color:rgba(255,255,255,0.48); font-size:10px; margin-top:10px;">'
        '<span>Baja repeticion</span><span style="color:#f5c542; font-weight:800;">Alta concentracion</span></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_prediction_balance(insights: dict, team1: str, team2: str):
    total = insights.get("total", 0) or 1
    home_pct = round((insights.get("home_win", 0) / total) * 100)
    draw_pct = round((insights.get("draw", 0) / total) * 100)
    away_pct = round((insights.get("away_win", 0) / total) * 100)
    rows = [
        (team1, insights.get("home_win", 0), home_pct),
        ("Empate", insights.get("draw", 0), draw_pct),
        (team2, insights.get("away_win", 0), away_pct),
    ]
    html_rows = ""
    for label, votes, pct in rows:
        html_rows += (
            '<div style="margin:10px 0;">'
            '<div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px;">'
            f'<span style="font-weight:800; color:#fff;">{html.escape(label)}</span>'
            f'<span style="color:#f5c542; font-weight:900;">{votes} · {pct}%</span></div>'
            '<div style="height:9px; background:rgba(255,255,255,0.07); border-radius:999px; overflow:hidden;">'
            f'<div style="height:9px; width:{pct}%; background:linear-gradient(90deg,#f5c542,#fff0a8); border-radius:999px;"></div>'
            '</div></div>'
        )
    st.markdown(f'<div class="fa-card" style="padding:16px;"><div style="color:#f5c542; font-weight:900; text-align:center; margin-bottom:8px;">Pulso 1X2</div>{html_rows}</div>', unsafe_allow_html=True)


def _render_hit_lists(insights: dict, match: dict):
    if insights.get("result") is None:
        message = random.choice(SCORE_IA_PENDING_MESSAGES)
        st.markdown(
            '<div class="fa-card" style="padding:16px; text-align:center;">'
            '<div style="font-size:22px; margin-bottom:6px;">&#129418;</div>'
            '<div style="color:#f5c542; font-weight:900; font-size:13px; margin-bottom:6px;">Mensaje de SCORE-IA</div>'
            '<div style="color:rgba(255,255,255,0.68); font-size:12px; line-height:1.5;">'
            f'{html.escape(message)}'
            '</div></div>',
            unsafe_allow_html=True,
        )
        return

    exact = insights.get("exact_participants", [])
    outcome = insights.get("outcome_participants", [])
    exact_text = ", ".join(html.escape(name) for name in exact) if exact else "Nadie clavo el marcador. Dolor colectivo."
    outcome_text = ", ".join(html.escape(name) for name in outcome[:12]) if outcome else "Nadie acerto el ganador o empate."
    score1, score2 = insights["result"]
    st.markdown(
        '<div class="fa-card glow" style="padding:16px;">'
        f'<div style="text-align:center; color:#f5c542; font-weight:900; margin-bottom:10px;">Resultado oficial: {score1} - {score2}</div>'
        '<div class="stats-row">'
        f'<div class="stat-chip"><strong>{insights.get("exact_hits", 0)}</strong> exactos</div>'
        f'<div class="stat-chip"><strong>{insights.get("outcome_hits", 0)}</strong> aciertos ganador/empate</div>'
        f'<div class="stat-chip"><strong>{score1}</strong> goles {html.escape(match["team1"])}</div>'
        f'<div class="stat-chip"><strong>{score2}</strong> goles {html.escape(match["team2"])}</div>'
        '</div>'
        f'<div style="font-size:12px; color:rgba(255,255,255,0.78); line-height:1.55;"><strong style="color:#f5c542;">Marcador exacto:</strong> {exact_text}</div>'
        f'<div style="font-size:12px; color:rgba(255,255,255,0.62); line-height:1.55; margin-top:8px;"><strong style="color:#f5c542;">Ganador/empate acertado:</strong> {outcome_text}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_kpi_strip(insights: dict, match: dict):
    top_score = next(iter(insights.get("score_counts", {})), "-")
    cards = [
        ("&#128101;", insights["total"], "predicciones", "Volumen de la porra"),
        ("&#127919;", top_score, "marcador moda", "Resultado mas repetido"),
        ("&#9917;", insights["avg_home_goals"], f"media {html.escape(match['team1'])}", "Goles esperados por la gente"),
        ("&#9917;", insights["avg_away_goals"], f"media {html.escape(match['team2'])}", "Goles esperados por la gente"),
    ]
    html_cards = ""
    for icon, value, label, sublabel in cards:
        html_cards += (
            '<div class="match-kpi-card">'
            f'<div class="match-kpi-icon">{icon}</div>'
            f'<div class="match-kpi-value">{value}</div>'
            f'<div class="match-kpi-label">{label}</div>'
            f'<div class="match-kpi-sub">{sublabel}</div>'
            '</div>'
        )
    st.markdown(f'<div class="match-kpi-grid">{html_cards}</div>', unsafe_allow_html=True)


def _render_match_banner(match_num: int, match: dict):
    banner = local_img_to_b64(f"assets/partidos/partido{match_num}.png")
    if banner:
        st.markdown(
            '<div class="match-banner-card">'
            f'<img src="{banner}" class="match-banner-img">'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        '<div class="match-banner-placeholder">'
        '<div style="font-size:34px; margin-bottom:6px;">&#127944;</div>'
        f'<div style="color:#f5c542; font-size:17px; font-weight:950;">partido{match_num}.png</div>'
        '<div style="color:rgba(255,255,255,0.38); font-size:10px; margin-top:10px;">Pendiente de banner en assets/partidos</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_match_event(match_num: int, match: dict):
    team1 = match["team1"]
    team2 = match["team2"]
    recipes1 = get_country_recipes(team1)
    recipes2 = get_country_recipes(team2)
    food1 = recipes1[(match_num - 1) % len(recipes1)]
    food2 = recipes2[match_num % len(recipes2)]
    banner = local_img_to_b64(f"assets/partidos/partido{match_num}.png")
    songs = []
    for team in (team1, team2):
        song = get_country_song(team)
        song_name = song.get("song_name", "")
        url = song.get("url", "")
        if song_name and url:
            songs.append(f'<a href="{html.escape(url)}" target="_blank"><span class="yt-icon">&#9658;</span>{html.escape(team)} · {html.escape(song_name)}</a>')
        elif song_name:
            songs.append(f'<span>{html.escape(team)} · {html.escape(song_name)} <em>sin URL</em></span>')
        else:
            songs.append(f'<span>{html.escape(team)} · cancion pendiente en wc-songs.csv</span>')

    if banner:
        image_html = f'<div class="match-event-photo"><img src="{banner}" class="match-event-img"></div>'
    else:
        image_html = (
            '<div class="match-event-photo"><div class="match-event-placeholder">'
            f'<div>partido{match_num}.png</div>'
            '<span>Pendiente en assets/partidos</span>'
            '</div></div>'
        )

    st.markdown(
        '<div class="match-event-card">'
        f'{image_html}'
        '<div class="match-experience-title">&#129418; Plan SCORE-IA para este partido</div>'
        f'<div class="match-experience-food">Verlo con <strong>{html.escape(food1)}</strong> y <strong>{html.escape(food2)}</strong>.</div>'
        '<div class="match-experience-songs">'
        '<div class="match-experience-label">&#127925; Banda sonora del cruce</div>'
        f'{"".join(songs)}'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_knockout_bar(label: str, value: int, total: int):
    pct = round((value / total) * 100) if total else 0
    st.markdown(
        '<div style="margin:12px 0;">'
        '<div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:6px;">'
        f'<span style="color:#fff; font-weight:900;">{html.escape(label)}</span>'
        f'<span style="color:#f5c542; font-weight:950;">{value} · {pct}%</span>'
        '</div>'
        '<div style="height:12px; background:rgba(255,255,255,0.07); border-radius:999px; overflow:hidden;">'
        f'<div style="height:12px; width:{pct}%; background:linear-gradient(90deg,#f5c542,#fff0a8); border-radius:999px;"></div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_knockout_insights(match_num: int, match: dict):
    participants = load_participants()
    if participants.empty:
        st.info("Todavia no hay predicciones cargadas.")
        return

    phase = match["group"]
    team1 = match["team1"]
    team2 = match["team2"]
    phase_rows = participants[participants["group"].astype(str) == phase]
    by_participant = {}
    for participant, pdf in phase_rows.groupby("participante", sort=False):
        picks = {
            str(value).strip()
            for value in pdf["pred1"].fillna("").astype(str).tolist() + pdf["pred2"].fillna("").astype(str).tolist()
            if str(value).strip()
        }
        by_participant[participant] = picks

    total = len(by_participant)
    team1_people = [name for name, picks in by_participant.items() if team1 in picks]
    team2_people = [name for name, picks in by_participant.items() if team2 and team2 in picks]
    both = [name for name, picks in by_participant.items() if team1 in picks and team2 and team2 in picks]
    only_team1 = [name for name, picks in by_participant.items() if team1 in picks and (not team2 or team2 not in picks)]
    only_team2 = [name for name, picks in by_participant.items() if team2 and team2 in picks and team1 not in picks]
    zero = [name for name, picks in by_participant.items() if team1 not in picks and (not team2 or team2 not in picks)]
    classified = match.get("classified", "")
    hits = [name for name, picks in by_participant.items() if classified and classified in picks]

    display_mn = display_match_num(match_num)
    st.markdown(
        '<div class="section-hdr">'
        f'<div class="title">PARTIDO {display_mn} · {html.escape(phase)}</div>'
        f'<div class="sub">{html.escape(team1)} vs {html.escape(team2)} · Pulso de clasificados</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    _render_knockout_bar(team1, len(team1_people), total)
    if team2:
        _render_knockout_bar(team2, len(team2_people), total)

    both_label = random.choice([
        "pronostican a las dos selecciones; SCORE-IA se rie porque solo pasa una",
        "cubren ambos lados del cruce, estrategia o miedo escenico",
        "llevan a los dos equipos vivos en esta fase",
    ])
    team1_label = random.choice([
        f"tienen una bala en {team1}",
        f"eligieron bando: {team1}",
        f"pronostican solo a {team1}",
    ])
    team2_label = random.choice([
        f"tienen una bala en {team2}",
        f"eligieron bando: {team2}",
        f"pronostican solo a {team2}",
    ]) if team2 else ""
    zero_label = random.choice([
        "no llevan a ninguna; el cruce les mira desde lejos",
        "se quedaron fuera de esta fiesta",
        "no tienen skin en este cruce",
    ])
    scoreia_note = random.choice([
        "Ni te preocupes, ya te sumo yo.",
        "SCORE-IA mira el cruce, hace cuentas y juzga en silencio.",
        "La calculadora no tiene sentimientos, pero este cruce le divierte.",
        "Cuando pase una sola seleccion, algunos Excel empezaran a sudar.",
        "Tu tranquilidad acaba donde empieza mi hoja de calculo.",
        "Aqui no hay magia: hay predicciones, cruces y algun optimista atrapado.",
        "Si llevas a los dos, no es vision; es comprar dos paraguas para un solo diluvio.",
        "SCORE-IA no anima, audita.",
        "El cruce parece simple hasta que tu bracket empieza a pedir auxilio.",
        "Yo no fallo sumas; fallo en entender tanta fe.",
        "Cuando el arbitro pite, algunos pronosticos pasaran a categoria arqueologia.",
        "Respira. Si hay puntos, los encontrare. Si no, tambien lo dire.",
        "La fase eliminatoria no perdona duplicidades emocionales.",
        "Dos selecciones entran, una pasa, varios participantes negocian con la realidad.",
        "SCORE-IA tiene una mala noticia: el comodin sentimental no puntua.",
        "Esto no es drama, es normalizacion de expectativas.",
    ])
    
    chips = f'<div class="stat-chip"><strong>{len(both)}</strong> {both_label}</div>'
    chips += f'<div class="stat-chip"><strong>{len(only_team1)}</strong> {team1_label}</div>'
    if team2:
        chips += f'<div class="stat-chip"><strong>{len(only_team2)}</strong> {team2_label}</div>'
    chips += f'<div class="stat-chip"><strong>{len(zero)}</strong> {zero_label}</div>'
    
    st.markdown(
        '<div class="fa-card" style="padding:16px; margin-top:14px;">'
        '<div style="color:#f5c542; font-weight:950; text-align:center; margin-bottom:10px;">&#129418; Lectura SCORE-IA del cruce</div>'
        '<div class="stats-row">'
        f'{chips}'
        f'<div class="stat-chip"><strong>{len(both)}</strong> {both_label}</div>'
        f'<div class="stat-chip"><strong>{len(one)}</strong> {one_label}</div>'
        f'<div class="stat-chip"><strong>{len(zero)}</strong> {zero_label}</div>'
        '</div>'
        f'<div style="font-size:10px; color:rgba(255,255,255,0.42); text-align:center; margin-top:8px;">{scoreia_note}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if classified:
        hit_text = ", ".join(html.escape(name) for name in hits) if hits else "Nadie lo llevaba en esta fase."
        st.markdown(
            '<div class="fa-card" style="padding:16px;">'
            f'<div style="color:#f5c542; font-weight:950; text-align:center; margin-bottom:8px;">Clasificado real: {html.escape(classified)}</div>'
            f'<div style="font-size:12px; color:rgba(255,255,255,0.72); line-height:1.5;"><strong style="color:#f5c542;">Acertaron:</strong> {hit_text}</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    ranking = compute_porra_ranking().head(10)
    if not ranking.empty:
        rows = ""
        for _, row in ranking.iterrows():
            picks = by_participant.get(row["participante"], set())
            has_team1 = team1 in picks
            has_team2 = bool(team2) and team2 in picks
            if has_team1 and has_team2:
                forecast = "Los 2"
            elif has_team1:
                forecast = f"Pasa {team1}"
            elif has_team2:
                forecast = f"Pasa {team2}"
            else:
                forecast = "Ninguno"
            rows += (
                '<tr>'
                f'<td style="color:#f5c542; font-weight:950;">{int(row["pos"])}</td>'
                f'<td>{html.escape(str(row["participante"]))}</td>'
                f'<td>{html.escape(forecast)}</td>'
                f'<td style="text-align:right; color:#f5c542; font-weight:950;">{int(row["puntos"])}</td>'
                '</tr>'
            )
        st.markdown(
            '<div class="fa-card" style="padding:14px; overflow-x:auto;">'
            '<div style="color:#f5c542; font-weight:950; text-align:center; margin-bottom:8px;">Top 10 vigente</div>'
            '<table class="score-table"><thead><tr><th>Pos</th><th>Participante</th><th>Pronostico</th><th style="text-align:right;">Pts</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>',
            unsafe_allow_html=True,
        )


def render(match_num: int):
    group_letter, match = _find_match(match_num)
    if not match:
        knockout_match = _find_knockout_match(match_num)
        if not knockout_match:
            st.error("No encuentro ese partido.")
            st.markdown('[Volver a grupos](?)')
            return
        st.markdown('<a href="?" target="_self" style="color:#f5c542; font-size:12px; font-weight:800; text-decoration:none;">← Volver</a>', unsafe_allow_html=True)
        _render_knockout_insights(match_num, knockout_match)
        return

    insights = get_match_insights(match_num)
    st.markdown('<a href="?" target="_self" style="color:#f5c542; font-size:12px; font-weight:800; text-decoration:none;">← Volver a grupos</a>', unsafe_allow_html=True)
    _render_match_event(match_num, match)

    if insights.get("total", 0) == 0:
        st.info("Todavia no hay predicciones cargadas para este partido.")
        return

    _render_kpi_strip(insights, match)
    _render_scoremap(insights, match["team1"], match["team2"])
    _render_prediction_balance(insights, match["team1"], match["team2"])
    _render_hit_lists(insights, match)
