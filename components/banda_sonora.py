"""
Banda Sonora page: Music browser with filters by seleccion / grupo.
Hymns are always visible at the top.
"""
import streamlit as st
import pandas as pd
import re

SHEET_ID = "1HBGfa4EygznWWdKk3CkcM-THGGsUDp6W"
SONGS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-songs"


def _get_video_id(url: str):
    if not isinstance(url, str):
        return None
    for p in [r"youtu\.be\/([^?&]+)", r"youtube\.com\/watch\?v=([^?&]+)", r"youtube\.com\/shorts\/([^?&]+)"]:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def _get_thumbnail(url: str) -> str:
    vid = _get_video_id(url)
    return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else ""


@st.cache_data(ttl=30)
def _load_songs():
    try:
        df = pd.read_csv(SONGS_URL)
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()


def _render_card(row, highlight=False):
    url = str(row.get("url", ""))
    thumb = _get_thumbnail(url)
    nombre = row.get("nombre", "")
    grupo = row.get("grupo", "")
    cls = "destacado" if highlight else ""

    st.markdown(
        f'<div class="video-card {cls}">'
        f'<a href="{url}" target="_blank" style="text-decoration:none;">'
        f'<div class="thumb-container">'
        f'<img class="thumb-img" src="{thumb}">'
        f'<div class="play-btn"></div></div></a>'
        f'<div class="video-info">'
        f'<div class="v-title">{nombre}</div>'
        f'<div class="v-sub">{grupo}</div>'
        f'<a class="v-link" href="{url}" target="_blank">Ver en YouTube</a>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


def render():
    st.markdown(
        '<div class="section-hdr">'
        '<div class="title">BANDA SONORA OFICIAL</div>'
        '</div>', unsafe_allow_html=True)

    songs = _load_songs()
    if songs.empty:
        st.info("Cargando banda sonora...")
        return

    # Detect hymns (grupo starts with "Himno" or similar)
    grupo_col = "grupo" if "grupo" in songs.columns else None
    nombre_col = "nombre" if "nombre" in songs.columns else None

    if grupo_col:
        is_hymn = songs[grupo_col].astype(str).str.lower().str.startswith("himno")
        hymns = songs[is_hymn]
        regular = songs[~is_hymn]
    else:
        hymns = pd.DataFrame()
        regular = songs

    # --- Hymns section (always visible) ---
    if not hymns.empty:
        st.markdown(
            '<div style="text-align:center; margin:10px 0 5px 0;">'
            '<span style="font-size:14px; font-weight:700; color:#f5c542; letter-spacing:1px;">HIMNOS</span>'
            '</div>', unsafe_allow_html=True)
        for _, row in hymns.iterrows():
            _render_card(row, highlight=True)

    # --- Filters ---
    if not regular.empty:
        st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # Group filter
        groups_list = ["Todos"]
        if grupo_col:
            unique_groups = sorted(regular[grupo_col].dropna().unique().tolist())
            groups_list += unique_groups

        with col1:
            sel_group = st.selectbox("Filtrar por grupo", groups_list, key="bs_group")

        # Name search
        with col2:
            search = st.text_input("Buscar seleccion", key="bs_search", placeholder="Ej: Espana...")

        # Apply filters
        filtered = regular.copy()
        if sel_group != "Todos" and grupo_col:
            filtered = filtered[filtered[grupo_col] == sel_group]
        if search and nombre_col:
            filtered = filtered[filtered[nombre_col].astype(str).str.lower().str.contains(search.lower(), na=False)]

        # Show count
        st.markdown(
            f'<div style="text-align:center; font-size:11px; color:rgba(255,255,255,0.4); margin-bottom:5px;">'
            f'Mostrando {len(filtered)} de {len(regular)} canciones</div>',
            unsafe_allow_html=True)

        # Sort: first song highlighted, rest reversed (newest first)
        if not filtered.empty:
            first = filtered.iloc[[0]]
            rest = filtered.iloc[1:][::-1]
            ordered = pd.concat([first, rest]).reset_index(drop=True)

            for i, row in ordered.iterrows():
                _render_card(row, highlight=(i == 0 and sel_group == "Todos" and not search))
        else:
            st.markdown(
                '<div style="text-align:center; color:rgba(255,255,255,0.5); font-size:13px; margin:20px 0;">'
                'No se encontraron canciones con ese filtro.</div>',
                unsafe_allow_html=True)
