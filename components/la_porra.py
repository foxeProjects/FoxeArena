"""
La Porra page: KICK OFF (how to participate) + scoring system.
"""
import streamlit as st


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


def render():
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
