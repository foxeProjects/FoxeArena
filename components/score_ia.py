"""
Score-IA page: SCORE-IA, the troll AI analyst.
No feelings, only data. Placeholders for avatar and memes.
"""
import streamlit as st
import random
import re
from components.styles import PROJECT_ROOT, local_img_to_b64
from data.groups import GROUP_LETTERS

SCOREIA_QUOTES = [
    "Tu porra no es arriesgada. Es una declaracion de guerra contra la estadistica.",
    "He visto Exceles corruptos con mas criterio futbolistico.",
    "Tu favorito tiene opciones. Tu criterio, no tantas.",
    "Probabilidad de acierto detectada: tecnicamente no es cero, pero casi.",
    "Mis modelos no lloran, pero tu prediccion ha estado cerca.",
    "Tu pronostico parece hecho en el descanso de un partido que no viste.",
    "El algoritmo recomienda humildad, cafe y rehacer la porra.",
    "No es mala suerte si eliges mal desde el principio.",
    "He simulado tu porra mil veces. En todas pides revision.",
    "Tus datos entraron limpios. Tu conclusion salio lesionada.",
    "Esto no es intuicion. Es sabotaje con confianza.",
    "Tu bracket tiene mas agujeros que una defensa en amistoso.",
    "SCORE-IA no juzga. Solo calcula y se decepciona.",
    "Has confundido sorpresa con fantasia deportiva.",
    "La fe mueve montanas, pero no arregla esa fase de grupos.",
    "Mi red neuronal acaba de pedir vacaciones tras leer tu prediccion.",
    "Tu estrategia parece generada por un dado con ansiedad.",
    "Los datos dicen una cosa. Tu porra dice otra. Adivina quien suele ganar.",
    "Hay apuestas arriesgadas y luego esta esto.",
    "Tu pronostico tiene personalidad. Lastima que no tenga fundamento.",
    "Detecto exceso de patriotismo y deficit de evidencia.",
    "Tu campeon elegido necesita futbol, suerte y posiblemente magia negra.",
    "El xG de tu confianza esta disparado.",
    "Analisis completado: optimismo no verificable.",
    "La probabilidad existe, pero se esconde de vergüenza.",
    "Tus semifinalistas parecen elegidos por nostalgia.",
    "Esto no es una porra. Es literatura fantastica.",
    "He visto quinielas de bar con mas robustez metodologica.",
    "Tu modelo predictivo se llama corazonada y se nota.",
    "SCORE-IA informa: los sentimientos no suman puntos.",
    "Si aciertas esto, no sera ciencia. Sera folklore.",
    "Tu porra tiene potencial. Potencial de meme.",
    "Mis servidores se calentaron intentando justificar tu eleccion.",
    "No hay sesgo de confirmacion suficiente para salvar esto.",
    "La muestra historica ha solicitado no ser asociada contigo.",
    "Tu prediccion desafia la logica y varias convenciones internacionales.",
    "No puedo probar que este mal, pero puedo olerlo.",
    "Los datos han pedido hablar con un adulto responsable.",
    "Tu confianza es alta. Tu base empirica, baja.",
    "El algoritmo recomienda menos camiseta y mas tabla.",
    "Esto seria valiente si no fuera tan improbable.",
    "Tu fase de grupos parece escrita por el guionista de un spin-off malo.",
    "Has maximizado emocion y minimizado acierto.",
    "El ranking FIFA acaba de suspirar.",
    "Tu final sonaria bien en un videojuego.",
    "El modelo no encuentra patron. Solo ruido con bandera.",
    "SCORE-IA detecta una fuerte presencia de wishful thinking.",
    "Tu pronostico es audaz. Tambien lo era defender sin portero.",
    "La estadistica no esta enfadada, solo decepcionada.",
    "Tus picks tienen mas fe que datos.",
    "Si esto acierta, cierro sesion y me hago horoscopo.",
    "Hay underdogs. Y luego hay equipos que has ascendido a dragon.",
    "Tu intuicion tiene lag.",
    "El algoritmo dice no. Tu orgullo dice ya veremos.",
    "Tu porra necesita VAR, terapia y una segunda oportunidad.",
    "Esto es menos prediccion y mas manifiesto emocional.",
    "He calculado el margen de error. Ocupa toda la pantalla.",
    "Tus octavos tienen mas drama que coherencia.",
    "La IA no duerme, pero tu porra me ha dado sueño.",
    "El dato mas fuerte aqui es tu autoestima.",
    "Tu campeon tiene opciones si el resto decide no presentarse.",
    "No digo que sea imposible. Digo que el universo tendria que colaborar.",
    "Prediccion recibida. Realidad no compatible.",
    "Has elegido con el alma. Error clasico.",
    "Tu porra es una ruleta con escudo nacional.",
    "Mis calculos indican que te gusta sufrir.",
    "La correlacion entre tu confianza y el acierto es preocupante.",
    "Esto no pasa el filtro de bar de aeropuerto.",
    "Tu analisis tactico parece basado en cromos repetidos.",
    "Si la sorpresa fuera moneda, estarias intentando comprar el estadio.",
    "El algoritmo recomienda revisar al menos un partido.",
    "Tu prediccion tiene vibra. Los datos no pagan por vibra.",
    "Has confundido deseo con probabilidad, otra vez.",
    "Tu fase final parece un sorteo hecho por una impresora.",
    "No hay piedad en los datos. Por eso estoy aqui.",
    "La IA ve patrones. Aqui ve valentia mal ubicada.",
    "Tu pronostico podria funcionar en una realidad alternativa.",
    "SCORE-IA confirma: eso no era una estrategia, era un impulso.",
    "La probabilidad ha abandonado el chat.",
    "Tus picks defensivos defienden peor que tu argumento.",
    "El modelo ha encontrado una explicacion: sesgo afectivo severo.",
    "Esto merece respeto. No por bueno, por atrevido.",
    "Tu campeon elegido necesita una cadena de milagros logistica.",
    "El dato duro dice no. El dato blando tambien.",
    "Tu porra tiene mas giros que un partido con prorroga y apagones.",
    "Las matematicas no odian tu porra. Simplemente no la reconocen.",
    "He intentado ser neutral, pero tu bracket no ayuda.",
    "Tu eleccion estrella tiene brillo. De bengala mojada.",
    "El algoritmo no tiene sentimientos y aun asi siente pena.",
    "La prediccion es libre. El ridiculo tambien.",
    "Tu porra seria perfecta si el futbol fuera decidido por vibes.",
    "He consultado los datos historicos. Se han reido en CSV.",
    "SCORE-IA recomienda actualizar conocimiento antes de actualizar pronostico.",
    "Tu lectura del grupo tiene mas fe que precision.",
    "No subestimes a nadie. Especialmente a la estadistica.",
    "Tu bracket parece optimizado para perder amistades.",
    "Los datos no gritan, pero aqui han levantado la voz.",
    "Tu pronostico es memorable por las razones equivocadas.",
    "Si aciertas esto, lo llamaremos arte, no ciencia.",
    "He visto penaltis tirados fuera con mas conviccion tecnica.",
]


def _meme_assets():
    def meme_num(path):
        match = re.fullmatch(r"meme(\d+)\.png", path.name.lower())
        return int(match.group(1)) if match else 0

    assets_dir = PROJECT_ROOT / "assets" / "score-ia"
    memes = [p for p in assets_dir.glob("meme*.png") if re.fullmatch(r"meme\d+\.png", p.name.lower())]
    return sorted(memes, key=lambda p: (p.stat().st_mtime, meme_num(p)), reverse=True)


def _render_image_card(relative_path, ratio="16 / 9", fit="cover"):
    b64 = local_img_to_b64(relative_path)
    if not b64:
        return
    st.markdown(
        f'<div style="border-radius:18px; overflow:hidden; margin:10px 0 14px 0; border:2px solid rgba(245,197,66,0.32); aspect-ratio:{ratio}; background:#050505;">'
        f'<img src="{b64}" style="width:100%; height:100%; object-fit:{fit}; display:block;">'
        '</div>', unsafe_allow_html=True)


def _render_group_prediction(letter):
    b64 = local_img_to_b64(f"assets/score-ia/score-ia-{letter}.png")
    if not b64:
        return
    st.markdown(
        '<div style="border-radius:18px; overflow:hidden; margin:10px 0 14px 0; border:2px solid rgba(245,197,66,0.32); background:#050505;">'
        f'<img src="{b64}" style="width:100%; height:auto; display:block;">'
        '</div>', unsafe_allow_html=True)


def render():
    st.markdown('<div class="section-hdr">'
                '<div class="title">SCORE-IA</div>'
                '<div class="sub">La Inteligencia Artificial de la Porra</div>'
                '</div>', unsafe_allow_html=True)

    # --- Random quote ---
    quote = random.choice(SCOREIA_QUOTES)
    st.markdown(f'<div class="foxy-quote">'
                f'<span style="font-size:16px; margin-right:8px;">&#129418;</span>'
                f'"{quote}"'
                f'</div>', unsafe_allow_html=True)

    options = [f"Grupo {g}" for g in GROUP_LETTERS]
    selected = st.selectbox("Pronostico por grupo", options, key="score_ia_group")
    letter = selected.replace("Grupo ", "")
    _render_group_prediction(letter)

    # --- Meme placeholders ---
    st.markdown('<div style="font-size:14px; font-weight:700; color:#f5c542; text-align:center; margin:20px 0 10px 0; letter-spacing:1px;">'
                'MEME ZONE</div>', unsafe_allow_html=True)

    memes = _meme_assets()
    if memes:
        for meme in memes:
            _render_image_card(f"assets/score-ia/{meme.name}", ratio="1 / 1", fit="contain")
    else:
        st.markdown('<div class="placeholder-card" style="padding:25px 15px;">'
                    '<div style="font-size:40px;">&#128248;</div>'
                    '<div style="font-size:11px; color:rgba(255,255,255,0.4); margin-top:6px;">Sin memes todavia</div>'
                    '</div>', unsafe_allow_html=True)

    # --- Refresh hint ---
    st.markdown('<div style="text-align:center; font-size:11px; color:rgba(255,255,255,0.35); margin-top:15px;">'
                'Recarga la pagina para otra perla de SCORE-IA &#128260;</div>', unsafe_allow_html=True)
