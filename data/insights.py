import pandas as pd
import streamlit as st
from components.styles import PROJECT_ROOT
from data.porra import load_official_results, load_participants, _outcome, _safe_int, _stage_prediction

STATUS_PATH = PROJECT_ROOT / "assets" / "porra-status.csv"


@st.cache_data(ttl=60)
def is_porra_closed() -> bool:
    if not STATUS_PATH.exists():
        return False
    try:
        df = pd.read_csv(STATUS_PATH)
        if df.empty or "closed" not in df.columns:
            return False
        return str(df.iloc[0]["closed"]).strip().lower() in {"true", "1", "yes", "si", "sí"}
    except Exception:
        return False


def _participants_count(participants_df: pd.DataFrame) -> int:
    if participants_df.empty:
        return 0
    return participants_df["participante"].nunique()


def _match_predictions(match_num: int) -> pd.DataFrame:
    participants_df = load_participants()
    if participants_df.empty:
        return pd.DataFrame()
    df = participants_df[participants_df["match_num"] == match_num].copy()
    df["pred1_int"] = df["pred1"].apply(_safe_int)
    df["pred2_int"] = df["pred2"].apply(_safe_int)
    return df[df["pred1_int"].notna() & df["pred2_int"].notna()]


def get_general_insights() -> dict:
    participants_df = load_participants()
    results_df = load_official_results()
    played = 0
    if not results_df.empty:
        played = len(results_df[(results_df["score1"].notna()) & (results_df["score2"].notna()) & (results_df["match_num"] <= 72)])

    def counts_for(match_num: int, limit: int = 8) -> dict:
        rows = participants_df[participants_df["match_num"] == match_num] if not participants_df.empty else pd.DataFrame()
        if rows.empty:
            return {}
        return rows.apply(_stage_prediction, axis=1).value_counts().head(limit).to_dict()

    def unique_count_for(match_num: int) -> int:
        rows = participants_df[participants_df["match_num"] == match_num] if not participants_df.empty else pd.DataFrame()
        if rows.empty:
            return 0
        return rows.apply(_stage_prediction, axis=1).replace("", pd.NA).dropna().nunique()

    def score_ia_for(match_num: int) -> str:
        if participants_df.empty:
            return ""
        rows = participants_df[
            (participants_df["participante"].str.lower() == "score-ia")
            & (participants_df["match_num"] == match_num)
        ]
        if rows.empty:
            return ""
        return _stage_prediction(rows.iloc[0])

    return {
        "participants": _participants_count(participants_df),
        "played_matches": played,
        "total_group_matches": 72,
        "champion_counts": counts_for(137),
        "runner_up_counts": counts_for(138),
        "third_place_counts": counts_for(139),
        "top_scorer_counts": counts_for(140),
        "best_keeper_counts": counts_for(141),
        "best_player_counts": counts_for(142),
        "young_player_counts": counts_for(143),
        "fair_play_counts": counts_for(144),
        "different_champions": unique_count_for(137),
        "different_finalists": len(set(counts_for(137, 200)) | set(counts_for(138, 200))),
        "score_ia": {
            137: score_ia_for(137),
            138: score_ia_for(138),
            139: score_ia_for(139),
            140: score_ia_for(140),
            141: score_ia_for(141),
            142: score_ia_for(142),
            143: score_ia_for(143),
            144: score_ia_for(144),
        },
    }


def get_match_insights(match_num: int) -> dict:
    df = _match_predictions(match_num)
    results_df = load_official_results()
    result_row = pd.DataFrame()
    if not results_df.empty:
        result_row = results_df[results_df["match_num"] == match_num]

    if df.empty:
        return {
            "total": 0,
            "home_win": 0,
            "draw": 0,
            "away_win": 0,
            "score_counts": {},
            "score_counts_full": {},
            "max_goal": 5,
            "avg_home_goals": 0,
            "avg_away_goals": 0,
            "result": None,
            "outcome_hits": 0,
            "exact_hits": 0,
            "exact_participants": [],
            "outcome_participants": [],
        }

    outcomes = df.apply(lambda row: _outcome(int(row["pred1_int"]), int(row["pred2_int"])), axis=1)
    score_labels = df.apply(lambda row: f'{int(row["pred1_int"])}-{int(row["pred2_int"])}', axis=1)
    score_counts_full = score_labels.value_counts().to_dict()
    max_goal = int(max(df["pred1_int"].max(), df["pred2_int"].max(), 5))

    result = None
    outcome_hits = 0
    exact_hits = 0
    exact_participants = []
    outcome_participants = []
    if not result_row.empty:
        score1 = _safe_int(result_row.iloc[0].get("score1"))
        score2 = _safe_int(result_row.iloc[0].get("score2"))
        if score1 is not None and score2 is not None:
            result = (score1, score2)
            actual_outcome = _outcome(score1, score2)
            exact_mask = (df["pred1_int"] == score1) & (df["pred2_int"] == score2)
            outcome_mask = (outcomes == actual_outcome) & ~exact_mask
            outcome_hits = int(outcome_mask.sum())
            exact_hits = int(exact_mask.sum())
            exact_participants = df.loc[exact_mask, "participante"].tolist()
            outcome_participants = df.loc[outcome_mask, "participante"].tolist()

    return {
        "total": len(df),
        "home_win": int((outcomes == "1").sum()),
        "draw": int((outcomes == "X").sum()),
        "away_win": int((outcomes == "2").sum()),
        "score_counts": score_labels.value_counts().head(12).to_dict(),
        "score_counts_full": score_counts_full,
        "max_goal": max_goal,
        "avg_home_goals": round(float(df["pred1_int"].mean()), 2),
        "avg_away_goals": round(float(df["pred2_int"].mean()), 2),
        "result": result,
        "outcome_hits": outcome_hits,
        "exact_hits": exact_hits,
        "exact_participants": exact_participants,
        "outcome_participants": outcome_participants,
    }
