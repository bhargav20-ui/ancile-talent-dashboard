# -*- coding: utf-8 -*-
"""
data_loader.py
Loads and caches the candidates CSV. Returns KPI dict.
"""
import os
import pandas as pd
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load candidates.csv from data/ folder, safe for all OS."""
    # Try multiple path strategies so it works locally AND on Streamlit Cloud
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "data", "candidates.csv"),
        os.path.join(os.getcwd(), "data", "candidates.csv"),
        "data/candidates.csv",
    ]
    for path in candidates:
        path = os.path.normpath(path)
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["Experience_Years"] = pd.to_numeric(df["Experience_Years"], errors="coerce")
            df["Match_Score"]      = pd.to_numeric(df["Match_Score"],      errors="coerce")
            for col in ["Domain", "Status", "Role", "Location", "Name", "Skills"]:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
            df["Client_Company"] = df["Client_Company"].fillna("N/A").astype(str).str.strip()
            return df

    st.error("Dataset not found. Expected: data/candidates.csv")
    st.stop()


def get_kpis(df: pd.DataFrame) -> dict:
    """Compute KPIs from a (potentially filtered) dataframe."""
    total     = len(df)
    placed    = len(df[df["Status"] == "Placed"])
    rejected  = len(df[df["Status"] == "Rejected"])
    pending   = len(df[df["Status"] == "Pending"])
    p_rate    = round(placed / total * 100, 1) if total else 0
    avg_exp   = round(df["Experience_Years"].mean(), 1) if total else 0
    avg_score = round(df["Match_Score"].mean(), 1) if total else 0
    top_domain = df["Domain"].value_counts().idxmax() if total else "N/A"

    return {
        "total_candidates": total,
        "placed":           placed,
        "pending":          pending,
        "rejected":         rejected,
        "placement_rate":   p_rate,
        "avg_experience":   avg_exp,
        "avg_match_score":  avg_score,
        "top_domain":       top_domain,
    }
