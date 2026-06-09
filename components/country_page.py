import html
import streamlit as st
from components.styles import local_img_to_b64
from data.countries import find_country, get_country_matches, get_country_recipes, get_country_song
from data.porra import display_match_num


def _render_country_image(country: dict):
    image = local_img_to_b64(f"assets/paises/{country['slug']}.png")
    if image:
        st.markdown(
            '<div class="country-hero-card">'
            f'<img src="{image}" class="country-hero-img">'
            '</div>',
            unsafe_allow_html=True,
        )
        return
    st.markdown(
        '<div class="country-hero-placeholder">'
        f'<div style="font-size:36px;">{country["flag"]}</div>'
        f'<div style="color:#f5c542; font-weight:950; font-size:18px; margin-top:8px;">{html.escape(country["name"])}</div>'
        '<div style="color:rgba(255,255,255,0.45); font-size:11px; margin-top:6px;">Pendiente de imagen en assets/paises</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_song(country_name: str):
    song = get_country_song(country_name)
    song_name = song.get("song_name", "")
    url = song.get("url", "")
    if song_name and url:
        content = (
            f'<div style="color:#fff; font-size:16px; font-weight:900;">{html.escape(song_name)}</div>'
            f'<a href="{html.escape(url)}" target="_blank" style="color:#f5c542; font-size:12px; font-weight:900; text-decoration:none;"><span class="yt-icon">&#9658;</span>Escuchar en YouTube</a>'
        )
    elif song_name:
        content = f'<div style="color:#fff; font-size:16px; font-weight:900;">{html.escape(song_name)}</div><div style="color:rgba(255,255,255,0.48); font-size:12px;">Falta URL en wc-songs.csv</div>'
    else:
        content = '<div style="color:rgba(255,255,255,0.58); font-size:12px; line-height:1.45;">Pendiente de cancion. Rellena <strong>wc-songs.csv</strong> con song_name y url.</div>'

    st.markdown(
        '<div class="fa-card country-info-card">'
        '<div class="country-card-title">&#127925; Cancion del pais</div>'
        f'{content}'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_recipes(country_name: str):
    recipes = get_country_recipes(country_name)
    items = "".join(f'<div class="country-recipe-chip">{html.escape(recipe)}</div>' for recipe in recipes)
    st.markdown(
        '<div class="fa-card country-info-card">'
        '<div class="country-card-title">&#127869; Gastronomia</div>'
        f'<div class="country-recipe-grid">{items}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_matches(country_name: str):
    matches = get_country_matches(country_name)
    rows = ""
    for match in matches:
        is_group_match = match.get("is_group_match", True)
        played = match["score1"] is not None and (match["score2"] is not None or not is_group_match)
        status_class = "country-match-finished" if played else "country-match-pending"
        if not is_group_match:
            status_class = "country-match-knockout-finished" if played else "country-match-knockout-pending"
        if played and is_group_match:
            score = f'{match["score1"]} - {match["score2"]}'
        elif played:
            score = "vs"
        else:
            score = "vs"
        recipes = get_country_recipes(country_name)
        recommendation = recipes[(match["match_num"] - 1) % len(recipes)]
        display_mn = display_match_num(match["match_num"])
        meta = f'{html.escape(match["date"])} · Grupo {html.escape(match["group"])}' if is_group_match else f'{html.escape(match["date"])} · {html.escape(match["group"])}'
        classified = f'<div class="country-scoreia-tip">&#9989; Clasificado: {html.escape(str(match["score1"]))}</div>' if played and not is_group_match else ""
        stadium = f'<div class="country-match-stadium">&#127967; {html.escape(match["stadium"])}</div>' if match["stadium"] else ""
        open_tag = f'<a class="country-match-card {status_class}" href="?match={match["match_num"]}" target="_self">'
        close_tag = '</a>'
        rows += (
            f'{open_tag}'
            f'<div><span class="country-match-num">Partido {display_mn}</span><span class="country-match-date">{meta}</span></div>'
            f'<div class="country-match-teams">{html.escape(match["team1"])} <span>{score}</span> {html.escape(match["team2"])}</div>'
            f'{classified}'
            f'{stadium}'
            f'<div class="country-scoreia-tip">&#129418; SCORE-IA te recomienda ver este partido con {html.escape(recommendation)}</div>'
            f'{close_tag}'
        )
    st.markdown(
        '<div class="fa-card" style="padding:16px;">'
        '<div class="country-card-title">&#9917; Partidos</div>'
        f'{rows}'
        '</div>',
        unsafe_allow_html=True,
    )


def render(country_query: str):
    country = find_country(country_query)
    if not country:
        st.error("No encuentro ese pais.")
        st.markdown('<a href="?" target="_self" style="color:#f5c542; font-weight:900;">← Volver</a>', unsafe_allow_html=True)
        return

    st.markdown('<a href="?" target="_self" style="color:#f5c542; font-size:12px; font-weight:800; text-decoration:none;">← Volver</a>', unsafe_allow_html=True)
    _render_country_image(country)
    _render_song(country["name"])
    _render_recipes(country["name"])
    _render_matches(country["name"])
