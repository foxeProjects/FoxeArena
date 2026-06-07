"""
Read match results from Google Sheets and compute group standings
using FIFA World Cup tiebreaker rules.

Tiebreaker order:
  1. Points
  2. Head-to-head virtual group (only matches between tied teams):
     a. Points
     b. Goal difference
     c. Goals scored
  3. Overall group stats:
     a. Goal difference
     b. Goals scored
  4. Fair play points (fewer penalty points = better):
     - Yellow card = 1 pt
     - Red card    = 2 pts
"""
import streamlit as st
import pandas as pd
from data.groups import GROUPS

SHEET_ID = "1HBGfa4EygznWWdKk3CkcM-THGGsUDp6W"
RESULTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=wc-results"


@st.cache_data(ttl=60)
def load_results() -> pd.DataFrame:
    """Load wc-results sheet. Returns empty DataFrame if unavailable."""
    try:
        df = pd.read_csv(RESULTS_URL)
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()


def _safe_int(val, default=0) -> int:
    """Convert a value to int, returning default if NaN or invalid."""
    if pd.isna(val):
        return default
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def _parse_group_matches(df: pd.DataFrame, group_letter: str) -> list[tuple]:
    """Return list of (team1, team2, goals1, goals2, match_num, y1, r1, y2, r2)
    for played matches."""
    grp = df[df["group"].astype(str).str.strip().str.upper() == group_letter.upper()]
    played = []
    for _, row in grp.iterrows():
        s1, s2 = row.get("score1"), row.get("score2")
        t1 = str(row.get("team1", "")).strip()
        t2 = str(row.get("team2", "")).strip()
        mn = row.get("match_num")
        if pd.notna(s1) and pd.notna(s2) and t1 and t2:
            try:
                y1 = _safe_int(row.get("yellow1"))
                r1 = _safe_int(row.get("red1"))
                y2 = _safe_int(row.get("yellow2"))
                r2 = _safe_int(row.get("red2"))
                played.append((t1, t2, int(float(s1)), int(float(s2)),
                               int(float(mn)), y1, r1, y2, r2))
            except (ValueError, TypeError):
                continue
    return played


def _build_stats(team_names: set, matches: list[tuple]) -> dict:
    """Build stats dict for a set of teams from a list of matches.

    Only considers matches where BOTH teams are in team_names.
    """
    stats = {n: {"pts": 0, "gf": 0, "gc": 0, "dif": 0, "fair_play": 0}
             for n in team_names}
    for t1, t2, g1, g2, _, y1, r1, y2, r2 in matches:
        if t1 not in team_names or t2 not in team_names:
            continue
        # goals
        stats[t1]["gf"] += g1
        stats[t1]["gc"] += g2
        stats[t2]["gf"] += g2
        stats[t2]["gc"] += g1
        # cards (penalty points — lower is better)
        stats[t1]["fair_play"] += y1 + r1 * 2
        stats[t2]["fair_play"] += y2 + r2 * 2
        # points
        if g1 > g2:
            stats[t1]["pts"] += 3
        elif g1 < g2:
            stats[t2]["pts"] += 3
        else:
            stats[t1]["pts"] += 1
            stats[t2]["pts"] += 1

    for s in stats.values():
        s["dif"] = s["gf"] - s["gc"]
    return stats


def _sort_tied_group(tied_names: list[str], all_matches: list[tuple],
                     overall: dict) -> list[str]:
    """Sort a group of teams tied on overall points using FIFA tiebreakers.

    1. H2H virtual group: pts, dif, gf
    2. Overall: dif, gf
    3. Fair play (fewer penalty points = better, so we negate)
    """
    if len(tied_names) <= 1:
        return tied_names

    tied_set = set(tied_names)
    h2h = _build_stats(tied_set, all_matches)

    def sort_key(name):
        h = h2h[name]
        o = overall[name]
        return (
            h["pts"],              # h2h points
            h["dif"],              # h2h goal difference
            h["gf"],               # h2h goals scored
            o["dif"],              # overall goal difference
            o["gf"],               # overall goals scored
            -o["fair_play"],       # fair play (negate: fewer penalty pts = better)
        )

    return sorted(tied_names, key=sort_key, reverse=True)


def get_match_scores(group_letter: str) -> dict:
    """Return {match_num: (score1, score2)} for matches that have results."""
    df = load_results()
    if df.empty:
        return {}
    played = _parse_group_matches(df, group_letter)
    return {mn: (g1, g2) for _, _, g1, g2, mn, *_ in played}


def compute_standings(group_letter: str) -> list[dict]:
    """Compute group standings with FIFA tiebreaker rules."""
    group = GROUPS[group_letter]
    team_names = [t["name"] for t in group["teams"]]

    # Init standings
    standings = {}
    for name in team_names:
        standings[name] = {
            "name": name,
            "pts": 0, "pj": 0, "pg": 0, "pe": 0, "pp": 0,
            "gf": 0, "gc": 0, "dif": 0, "fair_play": 0,
        }

    df = load_results()
    if df.empty:
        return list(standings.values())

    played = _parse_group_matches(df, group_letter)
    if not played:
        return list(standings.values())

    # Accumulate overall stats
    for t1, t2, g1, g2, _, y1, r1, y2, r2 in played:
        if t1 not in standings or t2 not in standings:
            continue

        for team, gf, gc in [(t1, g1, g2), (t2, g2, g1)]:
            standings[team]["pj"] += 1
            standings[team]["gf"] += gf
            standings[team]["gc"] += gc

        # cards
        standings[t1]["fair_play"] += y1 + r1 * 2
        standings[t2]["fair_play"] += y2 + r2 * 2

        if g1 > g2:
            standings[t1]["pg"] += 1
            standings[t1]["pts"] += 3
            standings[t2]["pp"] += 1
        elif g1 < g2:
            standings[t2]["pg"] += 1
            standings[t2]["pts"] += 3
            standings[t1]["pp"] += 1
        else:
            standings[t1]["pe"] += 1
            standings[t1]["pts"] += 1
            standings[t2]["pe"] += 1
            standings[t2]["pts"] += 1

    for s in standings.values():
        s["dif"] = s["gf"] - s["gc"]

    # --- Sort with tiebreakers ---
    names_sorted = sorted(team_names, key=lambda n: standings[n]["pts"], reverse=True)

    # Build overall stats lookup for tiebreaker
    overall_stats = {
        n: {"dif": standings[n]["dif"], "gf": standings[n]["gf"],
            "fair_play": standings[n]["fair_play"]}
        for n in team_names
    }

    # Process tied groups
    result_order = []
    i = 0
    while i < len(names_sorted):
        pts = standings[names_sorted[i]]["pts"]
        tied = []
        while i < len(names_sorted) and standings[names_sorted[i]]["pts"] == pts:
            tied.append(names_sorted[i])
            i += 1

        if len(tied) == 1:
            result_order.append(tied[0])
        else:
            resolved = _sort_tied_group(tied, played, overall_stats)
            result_order.extend(resolved)

    return [standings[n] for n in result_order]
