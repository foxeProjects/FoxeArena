"""
Home page: Logo, mascot placeholder, countdown to World Cup, YouTube channel.
"""
import streamlit as st
from datetime import datetime, timezone

WC_START = datetime(2026, 6, 11, tzinfo=timezone.utc)

YT_LOGO = ("https://upload.wikimedia.org/wikipedia/commons/thumb/"
            "0/09/YouTube_full-color_icon_%282017%29.svg/120px-YouTube_full-color_icon_%282017%29.svg.png")


def _countdown():
    now = datetime.now(timezone.utc)
    delta = WC_START - now
    if delta.total_seconds() <= 0:
        return None
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    mins, _ = divmod(rem, 60)
    return days, hours, mins


def render():
    # --- Countdown ---
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

    # --- Mascot placeholder ---
    st.markdown(
        '<div class="placeholder-card">'
        '<div class="placeholder-icon">&#129418;</div>'
        '<div class="placeholder-title">Mascota Oficial</div>'
        '<div class="placeholder-sub">Proximamente se revelara la mascota de FOXE Arena 2026</div>'
        '</div>', unsafe_allow_html=True)

    # --- YouTube channel promo ---
    st.markdown(
        '<div class="fa-card" style="text-align:center; padding:20px;">'
        f'<img src="{YT_LOGO}" width="48" style="margin-bottom:10px;">'
        '<div style="font-size:13px; color:rgba(255,255,255,0.55); margin-bottom:6px;">Canal oficial</div>'
        '<a href="https://www.youtube.com/@foxearena" target="_blank"'
        ' style="font-size:20px; font-weight:800; color:#f5c542; text-decoration:none;">'
        '@foxearena</a>'
        '</div>', unsafe_allow_html=True)
