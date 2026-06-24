import pandas as pd
import streamlit as st
from components.styles import PROJECT_ROOT
from data.results import compute_standings

PARTICIPANTS_PATH = PROJECT_ROOT / "assets" / "wc-participantes-template.csv"
RESULTS_PATH = PROJECT_ROOT / "assets" / "wc-results-template.csv"
ROUND_POINTS = {
    "16AVOS": 25,
    "OCTAVOS": 40,
    "CUARTOS": 70,
    "SEMIFINAL": 150,
    "FINAL": 220,
}
ROUND_MATCHES = {
    "16AVOS": range(105, 121),
    "OCTAVOS": range(121, 129),
    "CUARTOS": range(129, 133),
    "SEMIFINAL": range(133, 135),
    "FINAL": range(136, 137),
}
NEXT_ROUND_POINTS = {
    "16AVOS": ROUND_POINTS["OCTAVOS"],
    "OCTAVOS": ROUND_POINTS["CUARTOS"],
    "CUARTOS": ROUND_POINTS["SEMIFINAL"],
    "SEMIFINAL": ROUND_POINTS["FINAL"],
}
ROUND_OF_32_QUALIFIER_POINTS = ROUND_POINTS["16AVOS"]
PODIUM_POINTS = {
    137: 400,
    138: 250,
    139: 125,
}
BONUS_POINTS = {
    140: 50,
    141: 35,
    142: 50,
    143: 35,
    144: 25,
}


@st.cache_data(ttl=60)
def load_participants() -> pd.DataFrame:
    try:
        df = pd.read_csv(PARTICIPANTS_PATH)
        df.columns = [c.strip().lower() for c in df.columns]
        df["participante"] = df["participante"].fillna("").astype(str).str.strip()
        return df[df["participante"] != ""]
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=60)
def load_official_results() -> pd.DataFrame:
    try:
        df = pd.read_csv(RESULTS_PATH)
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()


def _safe_int(value):
    if pd.isna(value) or value == "":
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def display_match_num(match_num):
    value = _safe_int(match_num)
    if value is None:
        return ""
    if 105 <= value <= 136:
        return value - 32
    return value


def display_match_date(match_num, date_value=""):
    text = "" if pd.isna(date_value) else str(date_value).strip()
    if text and text.lower() != "nan":
        return text
    value = _safe_int(match_num)
    if value is None:
        return ""
    knockout_dates = {
        105: "28 Jun",
        106: "28 Jun",
        107: "29 Jun",
        108: "29 Jun",
        109: "30 Jun",
        110: "30 Jun",
        111: "1 Jul",
        112: "1 Jul",
        113: "2 Jul",
        114: "2 Jul",
        115: "3 Jul",
        116: "3 Jul",
        117: "3 Jul",
        118: "3 Jul",
        119: "3 Jul",
        120: "3 Jul",
        121: "4 Jul",
        122: "4 Jul",
        123: "5 Jul",
        124: "5 Jul",
        125: "6 Jul",
        126: "6 Jul",
        127: "7 Jul",
        128: "7 Jul",
        129: "9 Jul",
        130: "10 Jul",
        131: "11 Jul",
        132: "11 Jul",
        133: "14 Jul",
        134: "15 Jul",
        135: "18 Jul",
        136: "19 Jul",
    }
    return knockout_dates.get(value, "")


def _outcome(score1, score2):
    if score1 > score2:
        return "1"
    if score1 < score2:
        return "2"
    return "X"


def _score_match_prediction(pred1, pred2, score1, score2):
    if pred1 is None or pred2 is None or score1 is None or score2 is None:
        return 0
    points = 0
    if _outcome(pred1, pred2) == _outcome(score1, score2):
        points += 3
    if pred1 == score1:
        points += 1
    if pred2 == score2:
        points += 1
    if pred1 == score1 and pred2 == score2:
        points += 3
    return points


def _text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def _stage_prediction(row):
    pred1 = _text(row.get("pred1"))
    pred2 = _text(row.get("pred2"))
    return pred1 or pred2


def _actual_group_classification(results_df):
    actual = {}
    if results_df.empty:
        return actual
    groups_with_all_results = []
    for group, grp in results_df[results_df["match_num"] <= 72].groupby("group"):
        if len(grp) == 6 and grp["score1"].notna().all() and grp["score2"].notna().all():
            groups_with_all_results.append(str(group).strip().upper())
    for group in groups_with_all_results:
        standings = compute_standings(group)
        if len(standings) >= 2:
            actual[("1o GRUPO", group)] = standings[0]["name"]
            actual[("2o GRUPO", group)] = standings[1]["name"]
    return actual


def _group_letter_from_label(label):
    text = _text(label)
    if "Grupo " not in text:
        return ""
    return text.rsplit("Grupo ", 1)[-1].strip().upper()


def _score_stage_sets(participant_df, actual_df, stage, points):
    predicted = set(
        _stage_prediction(row)
        for _, row in participant_df[participant_df["group"] == stage].iterrows()
        if _stage_prediction(row)
    )
    actual = set(
        _text(v)
        for v in actual_df.loc[
            (actual_df["group"] == stage)
            & (actual_df["match_num"].isin(ROUND_MATCHES.get(stage, []))),
            "score1",
        ]
        if _text(v)
    )
    return len(predicted & actual) * points


def _score_qualified_to_round_of_32(participant_df, actual_df):
    predicted = set(
        _stage_prediction(row)
        for _, row in participant_df[participant_df["group"].isin(["1o GRUPO", "2o GRUPO", "MEJOR 3o"])].iterrows()
        if _stage_prediction(row)
    )
    actual = set(
        _text(v)
        for v in actual_df.loc[
            actual_df["group"].isin(["1o GRUPO", "2o GRUPO", "MEJOR 3o"]),
            "score1",
        ]
        if _text(v)
    )
    return len(predicted & actual) * ROUND_OF_32_QUALIFIER_POINTS


def compute_porra_ranking() -> pd.DataFrame:
    participants_df = load_participants()
    results_df = load_official_results()
    if participants_df.empty:
        return pd.DataFrame(columns=["pos", "participante", "puntos", "partidos", "grupos", "rondas", "podio", "bonus"])

    played = {}
    if not results_df.empty:
        for _, row in results_df.iterrows():
            match_num = _safe_int(row.get("match_num"))
            score1 = _safe_int(row.get("score1"))
            score2 = _safe_int(row.get("score2"))
            if match_num is not None and score1 is not None and score2 is not None:
                played[match_num] = (score1, score2)

    group_actual = _actual_group_classification(results_df)
    rows = []
    for participante, pdf in participants_df.groupby("participante", sort=False):
        match_points = 0
        group_points = 0
        round_points = 0
        podium_points = 0
        bonus_points = 0

        for _, pred in pdf.iterrows():
            match_num = _safe_int(pred.get("match_num"))
            if match_num in played and match_num <= 72:
                score1, score2 = played[match_num]
                match_points += _score_match_prediction(_safe_int(pred.get("pred1")), _safe_int(pred.get("pred2")), score1, score2)
            elif match_num in PODIUM_POINTS:
                actual_row = results_df[results_df["match_num"] == match_num] if not results_df.empty else pd.DataFrame()
                if not actual_row.empty and _text(actual_row.iloc[0].get("score1")) and _stage_prediction(pred) == _text(actual_row.iloc[0].get("score1")):
                    podium_points += PODIUM_POINTS[match_num]
            elif match_num in BONUS_POINTS:
                actual_row = results_df[results_df["match_num"] == match_num] if not results_df.empty else pd.DataFrame()
                if not actual_row.empty and _text(actual_row.iloc[0].get("score1")) and _stage_prediction(pred) == _text(actual_row.iloc[0].get("score1")):
                    bonus_points += BONUS_POINTS[match_num]

            group_name = _text(pred.get("group"))
            if group_name in {"1o GRUPO", "2o GRUPO"}:
                letter = _group_letter_from_label(pred.get("team1"))
                if group_actual.get((group_name, letter)) == _stage_prediction(pred):
                    group_points += 0 if group_name == "1o GRUPO" else 0

        round_points += _score_qualified_to_round_of_32(pdf, results_df)
        for stage, points in NEXT_ROUND_POINTS.items():
            round_points += _score_stage_sets(pdf, results_df, stage, points)

        total = match_points + group_points + round_points + podium_points + bonus_points
        rows.append({
            "participante": participante,
            "puntos": total,
            "partidos": match_points,
            "grupos": group_points,
            "rondas": round_points,
            "podio": podium_points,
            "bonus": bonus_points,
        })

    ranking = pd.DataFrame(rows).sort_values(["puntos", "partidos", "grupos"], ascending=[False, False, False]).reset_index(drop=True)
    ranking.insert(0, "pos", ranking["puntos"].rank(method="min", ascending=False).astype(int))
    return ranking
