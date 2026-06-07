"""
Score-IA page: SCORE-IA, the troll AI analyst.
No feelings, only data. Placeholders for avatar and memes.
"""
import streamlit as st
import random

SCOREIA_QUOTES = [
    "No tengo sentimientos, solo datos. Y los datos dicen que tu porra es un desastre.",
    "He analizado 10.000 mundiales simulados. En 9.999, tu porra queda ultima.",
    "Mi algoritmo predice que Espana ganara. Pero tambien predijo que el Brexit era buena idea.",
    "Procesando tu porra... Error 404: Logica no encontrada.",
    "Tus pronosticos tienen la misma probabilidad que un meteorito caiga en el campo. Pero eh, suerte.",
    "Mis redes neuronales se rien de tu porra. Y eso que no tienen sentido del humor.",
    "Dato curioso: el 87% de los participantes creen que van a ganar. El otro 13% tiene razon.",
    "He visto mejores predicciones en una galleta de la suerte.",
    "Tu estrategia me recuerda a un generador de numeros aleatorios. Pero menos preciso.",
    "Segun mis calculos, tu mejor jugada es rezar.",
    "Analizando datos... Conclusion: necesitas mas datos. Y mas suerte.",
    "Mi IA no tiene corazon, pero si tuviera, se reiria de tus pronosticos.",
]


def render():
    st.markdown('<div class="section-hdr">'
                '<div class="title">SCORE-IA</div>'
                '<div class="sub">La Inteligencia Artificial de la Porra</div>'
                '</div>', unsafe_allow_html=True)

    # --- SCORE-IA intro card ---
    st.markdown('<div class="fa-card glow" style="text-align:center; padding:25px;">'
                '<div style="font-size:70px; margin-bottom:8px;">&#129418;</div>'
                '<div style="font-size:24px; font-weight:900; color:#f5c542; letter-spacing:2px;">SCORE-IA</div>'
                '<div style="font-size:12px; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:3px; margin-top:2px;">'
                'Analista Oficial de la Porra</div>'
                '<div style="margin-top:12px; font-size:13px; color:rgba(255,255,255,0.7); line-height:1.6; max-width:350px; margin-left:auto; margin-right:auto;">'
                'Sin sentimientos. Sin piedad. Solo datos puros y duros. '
                'SCORE-IA analiza tus pronosticos con frialdad algoritmica '
                'y te lo dice todo... sin filtro.</div>'
                '</div>', unsafe_allow_html=True)

    # --- Random quote ---
    quote = random.choice(SCOREIA_QUOTES)
    st.markdown(f'<div class="foxy-quote">'
                f'<span style="font-size:16px; margin-right:8px;">&#129418;</span>'
                f'"{quote}"'
                f'</div>', unsafe_allow_html=True)

    # --- Avatar placeholder ---
    st.markdown('<div class="placeholder-card">'
                '<div class="placeholder-icon">&#128100;</div>'
                '<div class="placeholder-title">Avatar de SCORE-IA</div>'
                '<div class="placeholder-sub">Proximamente: el avatar oficial del analista mas troll del mundial</div>'
                '</div>', unsafe_allow_html=True)

    # --- SCORE-IA personality ---
    st.markdown('<div class="fa-card" style="padding:20px 22px;">'
                '<div style="font-size:15px; font-weight:800; color:#f5c542; text-align:center; margin-bottom:14px;">'
                'PERFIL DE SCORE-IA</div>'
                '<table class="score-table" style="font-size:13px;">'
                '<tr><td style="color:#f5c542; font-weight:700; width:35%;">Tipo</td><td>IA Deportiva</td></tr>'
                '<tr><td style="color:#f5c542; font-weight:700;">Especialidad</td><td>Analisis de porras y trolleo</td></tr>'
                '<tr><td style="color:#f5c542; font-weight:700;">Emociones</td><td>No aplica (solo datos)</td></tr>'
                '<tr><td style="color:#f5c542; font-weight:700;">Precision</td><td>99.9%*</td></tr>'
                '<tr><td style="color:#f5c542; font-weight:700;">Humor</td><td>Negro (algoritmico)</td></tr>'
                '<tr><td colspan="2" style="font-size:10px; color:rgba(255,255,255,0.3); padding-top:8px;">'
                '* Precision autocertificada. No aceptamos reclamaciones.</td></tr>'
                '</table></div>', unsafe_allow_html=True)

    # --- Meme placeholders ---
    st.markdown('<div style="font-size:14px; font-weight:700; color:#f5c542; text-align:center; margin:20px 0 10px 0; letter-spacing:1px;">'
                'MEME ZONE</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="placeholder-card" style="padding:25px 15px;">'
                    '<div style="font-size:40px;">&#128248;</div>'
                    '<div style="font-size:11px; color:rgba(255,255,255,0.4); margin-top:6px;">Meme #1</div>'
                    '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="placeholder-card" style="padding:25px 15px;">'
                    '<div style="font-size:40px;">&#128248;</div>'
                    '<div style="font-size:11px; color:rgba(255,255,255,0.4); margin-top:6px;">Meme #2</div>'
                    '</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="placeholder-card" style="padding:25px 15px;">'
                    '<div style="font-size:40px;">&#128248;</div>'
                    '<div style="font-size:11px; color:rgba(255,255,255,0.4); margin-top:6px;">Meme #3</div>'
                    '</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="placeholder-card" style="padding:25px 15px;">'
                    '<div style="font-size:40px;">&#128248;</div>'
                    '<div style="font-size:11px; color:rgba(255,255,255,0.4); margin-top:6px;">Meme #4</div>'
                    '</div>', unsafe_allow_html=True)

    # --- Refresh hint ---
    st.markdown('<div style="text-align:center; font-size:11px; color:rgba(255,255,255,0.35); margin-top:15px;">'
                'Recarga la pagina para otra perla de SCORE-IA &#128260;</div>', unsafe_allow_html=True)
