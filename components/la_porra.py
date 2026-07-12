"""
La Porra page: KICK OFF (how to participate) + scoring system.
"""
import streamlit as st
import pandas as pd
from html import escape
from data.insights import get_general_insights, is_porra_closed
from data.porra import load_participants, _safe_int


def _render_kickoff():
    # How to participate
    st.markdown(
        '<div class="fa-card" style="padding:20px 22px;">'
        '<div style="font-size:16px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:15px;">'
        'COMO PARTICIPAR</div>'
        '<div style="color:rgba(255,255,255,0.85); font-size:13px; line-height:1.8;">'
        '<div style="margin-bottom:14px;">'
        '<span style="color:#f5c542; font-weight:700;">1.</span> '
        '<strong>Descarga la plantilla</strong><br>'
        '<code style="background:rgba(245,197,66,0.1); color:#f5c542; padding:2px 8px; border-radius:6px; font-size:12px;">'
        'FOXE_Arena_Mundial_2026_Nombre_Apellido.xlsx</code></div>'
        '<div style="margin-bottom:14px;">'
        '<span style="color:#f5c542; font-weight:700;">2.</span> '
        '<strong>Renombra el fichero</strong> con tu nombre<br>'
        '<span style="font-size:12px; color:rgba(255,255,255,0.5);">Ej: FOXE_Arena_Mundial_2026_Juan_Garcia.xlsx</span></div>'
        '<div style="margin-bottom:14px;">'
        '<span style="color:#f5c542; font-weight:700;">3.</span> '
        '<strong>Rellena la pestana HOME</strong> del Excel con tu nombre completo</div>'
        '<div style="margin-bottom:14px;">'
        '<span style="color:#f5c542; font-weight:700;">4.</span> '
        '<strong>Completa tus pronosticos</strong> para las 48 selecciones</div>'
        '<div style="margin-bottom:14px;">'
        '<span style="color:#f5c542; font-weight:700;">5.</span> '
        '<strong>Realiza el pago</strong> &middot; '
        '<span style="color:#f5c542; font-weight:700;">25 EUR</span> antes del 9 de junio</div>'
        '<div style="margin-bottom:6px;">'
        '<span style="color:#f5c542; font-weight:700;">6.</span> '
        '<strong>Envia tu Excel + comprobante de pago</strong></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    # Payment info
    st.markdown(
        '<div class="fa-card glow" style="text-align:center; padding:18px;">'
        '<div style="font-size:14px; font-weight:800; color:#f5c542; margin-bottom:10px;">DATOS DE PAGO</div>'
        '<div style="color:rgba(255,255,255,0.85); font-size:13px; line-height:2;">'
        '<strong>Bizum:</strong> 663 911 987<br>'
        '<strong>Transferencia:</strong><br>'
        '<code style="font-size:11px; color:#f5c542; background:rgba(245,197,66,0.1); padding:3px 8px; border-radius:6px;">'
        'ES21 0049 6560 3523 9509 5761</code></div>'
        '<div style="margin-top:10px; font-size:11px; color:rgba(255,255,255,0.4);">'
        'Enviar a: foxearena@gmail.com</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Prizes
    st.markdown(
        '<div class="fa-card" style="padding:20px 22px;">'
        '<div style="font-size:15px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:12px;">'
        'PREMIOS</div>'
        '<div style="color:rgba(255,255,255,0.8); font-size:13px; margin-bottom:12px; text-align:center;">'
        'Al entregar la porra eliges una modalidad:</div>'
        '<div style="display:flex; gap:10px; flex-wrap:wrap; justify-content:center;">'
        '<div style="flex:1; min-width:180px; background:rgba(245,197,66,0.06); border:1px solid rgba(245,197,66,0.2); border-radius:14px; padding:14px; text-align:center;">'
        '<div style="font-size:24px; margin-bottom:4px;">&#127942;</div>'
        '<div style="font-size:13px; font-weight:700; color:#f5c542;">Podio Clasico</div>'
        '<div style="font-size:11px; color:rgba(255,255,255,0.6); margin-top:4px;">'
        'Premios para los 3 primeros clasificados</div></div>'
        '<div style="flex:1; min-width:180px; background:rgba(245,197,66,0.06); border:1px solid rgba(245,197,66,0.2); border-radius:14px; padding:14px; text-align:center;">'
        '<div style="font-size:24px; margin-bottom:4px;">&#129689;</div>'
        '<div style="font-size:13px; font-weight:700; color:#f5c542;">Escalonados</div>'
        '<div style="font-size:11px; color:rgba(255,255,255,0.6); margin-top:4px;">'
        'Hasta 10 premiados segun participantes</div></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )


def _render_scoring():
    # Match scoring
    st.markdown(
        '<div class="fa-card" style="padding:20px 22px;">'
        '<div style="font-size:15px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:14px;">'
        'FASE DE GRUPOS &middot; Partidos 1x2</div>'
        '<table class="score-table"><thead>'
        '<tr><th>Concepto</th><th style="text-align:right;">Puntos</th></tr></thead><tbody>'
        '<tr><td>Acierto 1X2</td><td style="text-align:right; color:#f5c542; font-weight:700;">+3</td></tr>'
        '<tr><td>Bonus: gol exacto de un equipo</td><td style="text-align:right; color:#f5c542; font-weight:700;">+1</td></tr>'
        '<tr><td>Bonus: marcador exacto</td><td style="text-align:right; color:#f5c542; font-weight:700;">+3</td></tr>'
        '</tbody></table></div>',
        unsafe_allow_html=True,
    )

    # Example
    st.markdown(
        '<div class="fa-card" style="padding:18px 22px;">'
        '<div style="font-size:13px; font-weight:700; color:#f5c542; margin-bottom:10px;">'
        'EJEMPLO: Mexico 2 - 0 Corea</div>'
        '<table class="score-table" style="font-size:12px;"><thead>'
        '<tr><th>Jugador</th><th>Pronostico</th><th style="text-align:right;">Pts</th></tr></thead><tbody>'
        '<tr><td>Diego Mateos</td><td>2-0</td>'
        '<td style="text-align:right; color:#f5c542; font-weight:700;">8</td></tr>'
        '<tr><td colspan="3" style="font-size:11px; color:rgba(255,255,255,0.5); padding:2px 12px;">'
        '1X2: 3 + Goles exactos: 2 + Marcador exacto: 3</td></tr>'
        '<tr><td>Juan Martinez</td><td>3-1</td>'
        '<td style="text-align:right; color:#f5c542; font-weight:700;">3</td></tr>'
        '<tr><td colspan="3" style="font-size:11px; color:rgba(255,255,255,0.5); padding:2px 12px;">'
        '1X2: 3 + Goles exactos: 0 + Marcador exacto: 0</td></tr>'
        '<tr><td>Carlos Jimenez</td><td>2-3</td>'
        '<td style="text-align:right; color:#f5c542; font-weight:700;">1</td></tr>'
        '<tr><td colspan="3" style="font-size:11px; color:rgba(255,255,255,0.5); padding:2px 12px;">'
        '1X2: 0 + Goles exactos: 1 + Marcador exacto: 0</td></tr>'
        '</tbody></table></div>',
        unsafe_allow_html=True,
    )

    # Group classification bonus
    st.markdown(
        '<div class="fa-card" style="padding:20px 22px;">'
        '<div style="font-size:15px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:14px;">'
        'CLASIFICACION DE GRUPO</div>'
        '<table class="score-table"><thead>'
        '<tr><th>Concepto</th><th style="text-align:right;">Puntos</th></tr></thead><tbody>'
        '<tr><td>Acertar 1ro del grupo</td><td style="text-align:right; color:#f5c542; font-weight:700;">+10</td></tr>'
        '<tr><td>Acertar 2do del grupo</td><td style="text-align:right; color:#f5c542; font-weight:700;">+5</td></tr>'
        '</tbody></table></div>',
        unsafe_allow_html=True,
    )

    # Knockout rounds
    st.markdown(
        '<div class="fa-card" style="padding:20px 22px;">'
        '<div style="font-size:15px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:14px;">'
        'FASES ELIMINATORIAS</div>'
        '<table class="score-table"><thead>'
        '<tr><th>Ronda</th><th style="text-align:right;">Puntos</th></tr></thead><tbody>'
        '<tr><td>Clasificado a 16avos</td><td style="text-align:right; color:#f5c542; font-weight:700;">25</td></tr>'
        '<tr><td>Clasificado a 8vos</td><td style="text-align:right; color:#f5c542; font-weight:700;">40</td></tr>'
        '<tr><td>Clasificado a 4tos</td><td style="text-align:right; color:#f5c542; font-weight:700;">70</td></tr>'
        '<tr><td>Clasificado a Semifinales</td><td style="text-align:right; color:#f5c542; font-weight:700;">150</td></tr>'
        '<tr><td>Clasificado a la Final</td><td style="text-align:right; color:#f5c542; font-weight:700;">220</td></tr>'
        '</tbody></table></div>',
        unsafe_allow_html=True,
    )

    # Final positions
    st.markdown(
        '<div class="fa-card glow" style="padding:20px 22px;">'
        '<div style="font-size:15px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:14px;">'
        'POSICIONES FINALES</div>'
        '<table class="score-table"><thead>'
        '<tr><th>Posicion</th><th style="text-align:right;">Puntos</th></tr></thead><tbody>'
        '<tr><td>&#127942; Campeon</td><td style="text-align:right; color:#ffd700; font-weight:900; font-size:16px;">400</td></tr>'
        '<tr><td>&#129352; Subcampeon</td><td style="text-align:right; color:#c0c0c0; font-weight:700;">250</td></tr>'
        '<tr><td>&#129353; Tercer puesto</td><td style="text-align:right; color:#cd7f32; font-weight:700;">125</td></tr>'
        '</tbody></table></div>',
        unsafe_allow_html=True,
    )

    # Bonus questions
    st.markdown(
        '<div class="fa-card" style="padding:20px 22px;">'
        '<div style="font-size:15px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:14px;">'
        'PREGUNTAS BONUS</div>'
        '<table class="score-table"><thead>'
        '<tr><th>Premio Individual</th><th style="text-align:right;">Puntos</th></tr></thead><tbody>'
        '<tr><td>&#9917; Balon de Oro</td><td style="text-align:right; color:#f5c542; font-weight:700;">50</td></tr>'
        '<tr><td>&#129349; Goleador</td><td style="text-align:right; color:#f5c542; font-weight:700;">50</td></tr>'
        '<tr><td>&#129502; Mejor Portero</td><td style="text-align:right; color:#f5c542; font-weight:700;">35</td></tr>'
        '<tr><td>&#11088; Mejor Jugador Joven</td><td style="text-align:right; color:#f5c542; font-weight:700;">35</td></tr>'
        '<tr><td>&#129309; Fair Play</td><td style="text-align:right; color:#f5c542; font-weight:700;">25</td></tr>'
        '</tbody></table></div>',
        unsafe_allow_html=True,
    )


def _render_general_insights():
    insights = get_general_insights()

    def render_bar_list(title, counts, icon, score_ia_pick):
        if not counts:
            return
        max_votes = max(counts.values()) if counts else 1
        leader = next(iter(counts))
        score_ia_votes = counts.get(score_ia_pick, 0) if score_ia_pick else 0
        if not score_ia_pick:
            message = "SCORE-IA no se ha mojado aqui. El mundo juega solo."
        elif leader == score_ia_pick:
            message = f"El mundo va con SCORE-IA: {score_ia_pick} lidera esta apuesta."
        elif score_ia_votes:
            message = f"SCORE-IA eligio {score_ia_pick}, pero el mundo prefiere {leader}."
        else:
            message = f"SCORE-IA eligio {score_ia_pick}, pero casi nadie le compra el relato."
        rows = ""
        for name, votes in counts.items():
            pct = round((votes / insights["participants"]) * 100) if insights["participants"] else 0
            width = max(4, round((votes / max_votes) * 100))
            rows += (
                '<div style="margin:10px 0;">'
                '<div style="display:flex; justify-content:space-between; gap:10px; font-size:12px; margin-bottom:4px;">'
                f'<span style="font-weight:800; color:#fff;">{name}</span>'
                f'<span style="color:#f5c542; font-weight:900;">{votes} votos · {pct}%</span>'
                '</div>'
                '<div style="height:10px; background:rgba(255,255,255,0.08); border-radius:999px; overflow:hidden;">'
                f'<div style="height:10px; width:{width}%; background:linear-gradient(90deg,#f5c542,#fff0a8); border-radius:999px;"></div>'
                '</div></div>'
            )
        st.markdown(
            '<div class="fa-card" style="padding:18px;">'
            f'<div style="font-size:15px; font-weight:900; color:#f5c542; text-align:center; margin-bottom:12px;">{icon} {title}</div>'
            '<div style="font-size:12px; color:rgba(255,255,255,0.72); text-align:center; line-height:1.45; '
            'background:rgba(245,197,66,0.07); border:1px solid rgba(245,197,66,0.16); border-radius:12px; padding:9px 10px; margin-bottom:12px;">'
            f'&#129418; {message}</div>'
            f'{rows}'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-hdr">'
        '<div class="title">INSIGHTS DE LA PORRA</div>'
        '<div class="sub">La porra ya esta cerrada. Empieza el juego de los datos.</div>'
        '</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="stats-row">'
        f'<div class="stat-chip"><strong>{insights["participants"]}</strong> participantes</div>'
        f'<div class="stat-chip"><strong>{insights["different_champions"]}</strong> campeones distintos</div>'
        f'<div class="stat-chip"><strong>{insights["different_finalists"]}</strong> finalistas distintos</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    score_ia = insights["score_ia"]
    render_bar_list("Favoritos a campeon", insights["champion_counts"], "&#127942;", score_ia.get(137))
    render_bar_list("Candidatos a subcampeon", insights["runner_up_counts"], "&#129352;", score_ia.get(138))
    render_bar_list("Tercer puesto mas elegido", insights["third_place_counts"], "&#129353;", score_ia.get(139))
    render_bar_list("Maximo goleador", insights["top_scorer_counts"], "&#9917;", score_ia.get(140))
    render_bar_list("Mejor portero", insights["best_keeper_counts"], "&#129349;", score_ia.get(141))
    render_bar_list("Balon de Oro", insights["best_player_counts"], "&#11088;", score_ia.get(142))
    render_bar_list("Mejor joven", insights["young_player_counts"], "&#128640;", score_ia.get(143))
    render_bar_list("Fair Play", insights["fair_play_counts"], "&#129309;", score_ia.get(144))


def _render_bigdata():
    df = load_participants()
    if df.empty:
        return

    st.markdown(
        '<div class="section-hdr" style="margin-top:18px;">'
        '<div class="title">BIGDATA</div>'
        '<div class="sub">Consolidado completo de predicciones para explorar la porra.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<style>'
        'div[data-testid="stDownloadButton"] button {'
        'background:linear-gradient(135deg,#f5c542,#fff0a8) !important; color:#151515 !important;'
        'border:0 !important; border-radius:14px !important; font-weight:950 !important;'
        'box-shadow:0 0 24px rgba(245,197,66,0.22) !important; min-height:46px !important;}'
        'div[data-testid="stDownloadButton"] button:hover {'
        'background:linear-gradient(135deg,#fff0a8,#f5c542) !important; color:#000 !important;'
        'border:0 !important; transform:translateY(-1px);}'
        'div[role="radiogroup"] label, div[role="radiogroup"] p {color:#ffffff !important; font-weight:900 !important;}'
        'div[role="radiogroup"] label span {color:#ffffff !important;}'
        '</style>',
        unsafe_allow_html=True,
    )
    st.download_button(
        label="DESCARGAR CONSOLIDADO",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="CONSOLIDADO.csv",
        mime="text/csv",
        use_container_width=True,
    )

    mode = st.radio(
        "Tipo de prediccion",
        ["Fase de grupos", "Eliminatorias"],
        horizontal=True,
        key="bigdata_mode",
    )

    df = df.copy()
    df["_match_num_int"] = df["match_num"].astype(int)
    if mode == "Fase de grupos":
        base = df[df["_match_num_int"].between(1, 72)].copy()
        description = "Marcadores 1X2 de la fase de grupos."
        st.markdown(
            '<div class="fa-card glow" style="padding:16px 18px; margin-top:12px;">'
            f'<div style="font-size:15px; font-weight:950; color:#f5c542; text-align:center; margin-bottom:6px;">&#128269; Explorador BIGDATA · {mode}</div>'
            f'<div style="font-size:12px; color:rgba(255,255,255,0.70); text-align:center; line-height:1.45;">{description}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        participant_options = ["Todos"] + sorted(base["participante"].dropna().astype(str).unique().tolist())
        group_options = ["Todos"] + sorted(base["group"].dropna().astype(str).unique().tolist())
        match_values = sorted(base["match_num"].dropna().astype(int).unique().tolist())
        match_options = ["Todos"] + [str(value) for value in match_values]
        team_options = ["Todos"] + sorted(
            set(base["team1"].dropna().astype(str).tolist())
            | set(base["team2"].dropna().astype(str).tolist())
        )
        top_cols = st.columns([1.6, 0.8])
        bottom_cols = st.columns([0.8, 1.0])

        with top_cols[0]:
            selected_participant = st.selectbox("Participante", participant_options, key="bigdata_groups_participant")
        with top_cols[1]:
            selected_group = st.selectbox("Grupo", group_options, key="bigdata_groups_group")
        with bottom_cols[0]:
            selected_match = st.selectbox("Partido", match_options, key="bigdata_groups_match_num")
        with bottom_cols[1]:
            selected_team = st.selectbox("Equipo", team_options, key="bigdata_groups_team")

        visible = base
        if selected_participant != "Todos":
            visible = visible[visible["participante"].astype(str) == selected_participant]
        if selected_match != "Todos":
            visible = visible[visible["match_num"].astype(int) == int(selected_match)]
        if selected_group != "Todos":
            visible = visible[visible["group"].astype(str) == selected_group]
        if selected_team != "Todos":
            selected = selected_team.lower()
            visible = visible[
                visible["team1"].fillna("").astype(str).str.lower().eq(selected)
                | visible["team2"].fillna("").astype(str).str.lower().eq(selected)
            ]
        columns = ["participante", "team1", "pred1", "pred2", "team2"]
        headers = ["Participante", "Equipo A", "Goles A", "Goles B", "Equipo B"]
        third_kpi_label = "partidos filtrados"
        third_kpi_value = visible["match_num"].nunique()
    else:
        base = df[df["_match_num_int"] > 72].copy()
        description = "Cruces, posiciones finales y preguntas bonus."
        st.markdown(
            '<div class="fa-card glow" style="padding:16px 18px; margin-top:12px;">'
            f'<div style="font-size:15px; font-weight:950; color:#f5c542; text-align:center; margin-bottom:6px;">&#128269; Explorador BIGDATA · {mode}</div>'
            f'<div style="font-size:12px; color:rgba(255,255,255,0.70); text-align:center; line-height:1.45;">{description}</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        participant_options = ["Todos"] + sorted(base["participante"].dropna().astype(str).unique().tolist())
        phase_options = ["Todos"] + sorted(base["group"].dropna().astype(str).unique().tolist())
        prediction_options = ["Todos"] + sorted(
            {
                value
                for value in (
                    base["pred1"].fillna("").astype(str).tolist()
                    + base["pred2"].fillna("").astype(str).tolist()
                )
                if value.strip()
            }
        )
        cols = st.columns([1.6, 0.8, 1.0])

        with cols[0]:
            selected_participant = st.selectbox("Participante", participant_options, key="bigdata_knockout_participant")
        with cols[1]:
            selected_phase = st.selectbox("Fase", phase_options, key="bigdata_knockout_phase")
        with cols[2]:
            selected_prediction = st.selectbox("Equipo", prediction_options, key="bigdata_knockout_prediction")
        st.markdown(
            '<div class="fa-card" style="padding:12px 14px; margin-top:8px; border-color:rgba(245,197,66,0.18);">'
            '<div style="font-size:11px; color:#f5c542; font-weight:950; margin-bottom:4px;">Busqueda auxiliar</div>'
            '<div style="font-size:10px; color:rgba(255,255,255,0.48);">Refina sobre los filtros anteriores: participante, fase y equipo.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        participant_search = st.text_input("Buscar", "", key="bigdata_knockout_search")

        visible = base
        if selected_participant != "Todos":
            visible = visible[visible["participante"].astype(str) == selected_participant]
        if selected_phase != "Todos":
            visible = visible[visible["group"].astype(str) == selected_phase]
        if selected_prediction != "Todos":
            selected = selected_prediction.lower()
            visible = visible[
                visible["pred1"].fillna("").astype(str).str.lower().eq(selected)
                | visible["pred2"].fillna("").astype(str).str.lower().eq(selected)
            ]
        if participant_search.strip():
            query = participant_search.strip().lower()
            visible = visible[
                visible["team1"].fillna("").astype(str).str.lower().str.contains(query, regex=False)
                | visible["team2"].fillna("").astype(str).str.lower().str.contains(query, regex=False)
                | visible["pred1"].fillna("").astype(str).str.lower().str.contains(query, regex=False)
                | visible["pred2"].fillna("").astype(str).str.lower().str.contains(query, regex=False)
            ]
        # Exclude rows explicitly labelled as FINAL or 3er PUESTO (text in 'group').
        # Keep PODIO entries (they are specific match_num 137-139 and should be shown as PODIO labels).
        visible = visible[~visible["group"].fillna("").astype(str).str.strip().str.upper().isin(["FINAL", "3ER PUESTO"])]
        columns = ["participante", "group", "pred1"]
        headers = ["Participante", "Fase", "Respuesta"]
        third_kpi_label = "fases filtradas"
        third_kpi_value = visible["group"].nunique()

    st.markdown(
        '<div class="stats-row" style="margin-top:12px;">'
        f'<div class="stat-chip"><strong>{len(visible)}</strong> filas</div>'
        f'<div class="stat-chip"><strong>{visible["participante"].nunique()}</strong> participantes</div>'
        f'<div class="stat-chip"><strong>{third_kpi_value}</strong> {third_kpi_label}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Labels for PODIUM and BONUS
    podium_labels = {
        137: "PODIO: Campeón",
        138: "PODIO: Subcampeón",
        139: "PODIO: Tercer Puesto",
    }
    bonus_labels = {
        140: "BONUS: Balón de Oro",
        141: "BONUS: Mejor Portero",
        142: "BONUS: Goleador",
        143: "BONUS: Mejor Joven",
        144: "BONUS: Fair Play",
    }

    def format_cell_value(column, value, match_num_val=None):
        if column in {"pred1", "pred2"}:
            numeric = pd.to_numeric(value, errors="coerce")
            if pd.notna(numeric):
                return str(int(numeric))
        if pd.isna(value):
            return ""
        text = str(value)
        if mode == "Eliminatorias" and column == "group":
            # Check if this is a PODIO or BONUS phase
            if match_num_val in podium_labels:
                return podium_labels[match_num_val]
            if match_num_val in bonus_labels:
                return bonus_labels[match_num_val]
            phase_aliases = {
                "1o GRUPO": "16AVOS",
                "2o GRUPO": "16AVOS",
                "MEJOR 3o": "16AVOS",
                "16AVOS": "OCTAVOS",
                "OCTAVOS": "CUARTOS",
                "CUARTOS": "SEMIFINAL",
                "SEMIFINAL": "FINAL",
            }
            return phase_aliases.get(text, text)
        display_aliases = {
            "Bosnia y Herzegovina": "Bosnia",
            "Estados Unidos": "USA",
            "Republica Checa": "Chequia",
        }
        return display_aliases.get(text, text)

    if mode == "Fase de grupos":
        col_widths = ["30%", "20%", "10%", "10%", "20%"]
        table_width_style = "width:100%;"
    else:
        col_widths = ["40%", "22%", "38%"]
        table_width_style = "width:100%;"

    body = ""
    for _, row in visible.head(300).iterrows():
        match_num_val = _safe_int(row.get("match_num")) if mode == "Eliminatorias" else None
        cells = "".join(
            f'<td style="width:{col_widths[idx]}; {"text-align:center;" if column in {"pred1", "pred2"} else ""}">{escape(format_cell_value(column, row.get(column, ""), match_num_val))}</td>'
            for idx, column in enumerate(columns)
        )
        body += f"<tr>{cells}</tr>"
    head = "".join(
        f'<th style="width:{col_widths[idx]}; white-space:nowrap; {"text-align:center;" if columns[idx] in {"pred1", "pred2"} else ""}">{header}</th>'
        for idx, header in enumerate(headers)
    )
    st.markdown(
        '<div class="fa-card" style="padding:0; overflow-y:auto; overflow-x:hidden; max-height:520px; margin-top:10px;">'
        f'<table class="score-table" style="{table_width_style} table-layout:fixed;">'
        f'<thead><tr>{head}</tr></thead>'
        f'<tbody>{body}</tbody>'
        '</table>'
        '</div>'
        '<div style="font-size:11px; color:rgba(255,255,255,0.42); text-align:center; margin-top:6px;">'
        'Mostrando maximo 300 filas para mantener la navegacion fluida.</div>',
        unsafe_allow_html=True,
    )


def render():
    if is_porra_closed():
        _render_general_insights()
        _render_bigdata()
    else:
        st.markdown(
            '<div class="section-hdr">'
            '<div class="title">KICK OFF</div>'
            '</div>', unsafe_allow_html=True)
        _render_kickoff()

    st.markdown('<div style="height:25px;"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-hdr">'
        '<div class="title">COMO PUNTUAMOS</div>'
        '</div>', unsafe_allow_html=True)
    _render_scoring()
