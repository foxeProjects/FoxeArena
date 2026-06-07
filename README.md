# 🦊 FOXE Arena

<div align="center">

**Streamlit app para la porra del Mundial 2026: grupos, calendario, SCORE-IA, banda sonora y reglas de puntuación.**

</div>

---

## Navegación

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Uso de la app](#uso-de-la-app)
- [Datos y configuración](#datos-y-configuración)
- [Arquitectura](#arquitectura)
- [Assets principales](#assets-principales)
- [Dependencias](#dependencias)
- [Desarrollo](#desarrollo)

---

## Overview

FOXE Arena es una aplicación web construida con **Streamlit** para gestionar y visualizar una porra del Mundial 2026.

La app combina:

- Información de participación y sistema de puntos.
- Calendario de fase de grupos.
- Clasificación dinámica de grupos desde resultados reales.
- Predicciones visuales de **SCORE-IA**.
- Banda sonora oficial conectada a Google Sheets.
- Assets gráficos personalizados para grupos, banners, memes y pronósticos.

---

## Features

| Módulo | Descripción | Fuente de datos |
|---|---|---|
| 🏠 Home | Cuenta atrás, portada SCORE-IA y enlace al canal oficial | Assets locales |
| 🏆 La Porra | Instrucciones, pago, premios y sistema de puntuación | Código estático |
| 🎵 Soundtrack | Canciones e himnos con filtros por grupo/selección | Google Sheet `wc-songs` |
| 🦊 Score-IA | Frases aleatorias, memes dinámicos y pronóstico visual por grupo | `assets/score-ia/` |
| ⚽ Grupos | Banners, clasificación, calendario y predicción SCORE-IA por partido | `data/groups.py`, Google Sheet `wc-results`, CSV local |

---

## Quick Start

### 1. Crear entorno e instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la app

```bash
streamlit run streamlit_app.py
```

### 3. Abrir en navegador

Streamlit abrirá normalmente:

```text
http://localhost:8501
```

---

## Uso de la app

### Home

Muestra la cuenta atrás del Mundial 2026 y la portada de SCORE-IA:

```text
assets/score-ia/portada.png
```

### La Porra

Incluye:

- Cómo participar.
- Datos de pago.
- Modalidades de premio.
- Sistema de puntuación:
  - Acierto 1X2.
  - Gol exacto por equipo.
  - Marcador exacto.
  - Clasificación de grupo.
  - Fases eliminatorias.
  - Bonus finales.

### Score-IA

Permite seleccionar un grupo de `A` a `L` y visualizar su pronóstico:

```text
assets/score-ia/score-ia-A.png
...
assets/score-ia/score-ia-L.png
```

También carga memes automáticamente con el patrón:

```text
assets/score-ia/meme1.png
assets/score-ia/meme2.png
...
```

Los memes se ordenan dinámicamente con los más recientes primero.

### Grupos

Para cada grupo:

- Muestra banner del grupo.
- Calcula clasificación de selecciones.
- Muestra calendario.
- Añade predicción de SCORE-IA dentro de cada partido si existe en:

```text
assets/wc-participantes-score-ia.csv
```

---

## Datos y configuración

### Resultados reales

Los resultados se cargan desde Google Sheets en `data/results.py`:

```python
SHEET_ID = "1HBGfa4EygznWWdKk3CkcM-THGGsUDp6W"
RESULTS_URL = "...&sheet=wc-results"
```

La clasificación de grupos se recalcula con:

```python
compute_standings(group_letter)
```

### Banda sonora

La banda sonora se carga desde la hoja:

```text
wc-songs
```

### Predicciones SCORE-IA

El CSV local:

```text
assets/wc-participantes-score-ia.csv
```

tiene el formato:

```csv
participante,match_num,group,date,team1,team2,pred1,pred2
score-ia,1,A,11 Jun,Mexico,Sudafrica,2,1
```

El calendario de grupos lee `match_num`, `pred1` y `pred2` para pintar:

```text
🦊 SCORE-IA prediction: 2 - 1
```

---

## Arquitectura

```text
FoxeArena/
├── streamlit_app.py              # Entry point principal
├── requirements.txt              # Dependencias Python
├── README.md                     # Documentación del proyecto
├── components/
│   ├── home.py                   # Home y cuenta atrás
│   ├── la_porra.py               # Reglas, premios e instrucciones
│   ├── banda_sonora.py           # Música desde Google Sheets
│   ├── score_ia.py               # SCORE-IA, memes y pronósticos visuales
│   ├── grupos.py                 # Grupos, calendario, clasificación y predicciones
│   └── styles.py                 # CSS global y utilidades de imagen
├── data/
│   ├── groups.py                 # Equipos, partidos, banners y estadios
│   └── results.py                # Carga de resultados y cálculo de standings
└── assets/
    ├── wc-results-template.csv
    ├── wc-participantes-template.csv
    ├── wc-participantes-score-ia.csv
    ├── score-ia/
    │   ├── portada.png
    │   ├── meme1.png
    │   └── score-ia-A.png ... score-ia-L.png
    └── grupoA/ ... grupoL/
        └── bannerX.png
```

---

## Assets principales

| Asset | Uso |
|---|---|
| `assets/IMG_9234.png` | Logo principal |
| `assets/8B390EC8-EB25-48F3-8838-76DE0F4416D9.png` | Fondo global |
| `assets/score-ia/portada.png` | Portada en Home |
| `assets/score-ia/memeX.png` | Memes dinámicos de SCORE-IA |
| `assets/score-ia/score-ia-X.png` | Pronóstico visual por grupo |
| `assets/grupoX/bannerX.png` | Banner visual de cada grupo |
| `assets/wc-participantes-score-ia.csv` | Marcadores propuestos por SCORE-IA |

---

## Dependencias

| Paquete | Uso |
|---|---|
| `streamlit` | Framework web de la app |
| `pandas` | Lectura de CSV/Google Sheets y tratamiento de datos |

Instalación:

```bash
pip install -r requirements.txt
```

---

## Desarrollo

### Validar sintaxis

```bash
python -m py_compile streamlit_app.py components/*.py data/*.py
```

### Ejecutar localmente

```bash
streamlit run streamlit_app.py
```

### Flujo de datos simplificado

```text
Google Sheets wc-results
        │
        ▼
data/results.py
        │
        ▼
compute_standings()
        │
        ▼
components/grupos.py
```

```text
assets/wc-participantes-score-ia.csv
        │
        ▼
_load_score_ia_predictions()
        │
        ▼
Calendario de cada grupo
```

---

## Estado actual

- La app usa navegación con `st.tabs`.
- La clasificación de grupos se calcula con resultados reales.
- SCORE-IA tiene pronósticos visuales por grupo.
- El calendario muestra la predicción de SCORE-IA por partido.
- El ranking automático de participantes queda pendiente para una fase posterior.

---

## License

Proyecto privado/comunitario de FOXE Arena. Definir licencia si se publica para uso externo.
