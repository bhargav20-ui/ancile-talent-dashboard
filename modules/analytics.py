# -*- coding: utf-8 -*-
"""
analytics.py
All Plotly chart functions for the Ancile dashboard.
Brand: Navy #0A1F44 | Orange #F76C1B | Dark card bg #1A2744
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
print(pd.Timestamp.today())
from collections import Counter

# ── Brand palette ─────────────────────────────────────────────────────────────
NAVY     = "#0A1F44"
ORANGE   = "#F76C1B"
ORANGE2  = "#FF8C42"
CARD_BG  = "#1A2744"
WHITE    = "#FFFFFF"
GRAY     = "#8892A4"
GRID     = "#2A3A5C"

COLOR_SEQ = ["#F76C1B","#1E90FF","#00C9A7","#FFD700","#FF6B9D","#A78BFA","#34D399","#FB923C"]
STATUS_COLORS = {"Placed": "#34D399", "Pending": "#60A5FA", "Rejected": "#F87171"}


def _base(fig, title="", height=340):
    """Apply consistent dark theme to any Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(color=WHITE, size=14, family="Inter"), x=0.02),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=WHITE, family="Inter, sans-serif", size=12),
        height=height,
        margin=dict(l=16, r=16, t=48, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE)),
        xaxis=dict(gridcolor=GRID, color=WHITE, linecolor=GRID),
        yaxis=dict(gridcolor=GRID, color=WHITE, linecolor=GRID),
    )
    return fig


def chart_top_skills(df: pd.DataFrame, top_n: int = 12) -> go.Figure:
    """Horizontal bar — top N skills by frequency."""
    skill_list = []
    for s in df["Skills"].dropna():
        skill_list.extend([x.strip() for x in s.split(",")])
    counts = Counter(skill_list).most_common(top_n)
    sdf = pd.DataFrame(counts, columns=["Skill", "Count"]).sort_values("Count")

    fig = px.bar(sdf, x="Count", y="Skill", orientation="h",
                 color="Count", color_continuous_scale=[[0,"#1A4A8A"],[1,ORANGE]],
                 text="Count")
    fig.update_traces(marker_line_width=0, textposition="outside",
                      textfont=dict(color=WHITE, size=11))
    fig.update_coloraxes(showscale=False)
    fig.update_layout(yaxis_title="", xaxis_title="Frequency")
    return _base(fig, f"Top {top_n} In-Demand Skills")


def chart_domain_distribution(df: pd.DataFrame) -> go.Figure:
    """Donut chart — candidates by domain."""
    dcounts = df["Domain"].value_counts().reset_index()
    dcounts.columns = ["Domain", "Count"]
    fig = px.pie(dcounts, names="Domain", values="Count",
                 hole=0.55, color_discrete_sequence=COLOR_SEQ)
    fig.update_traces(
        textposition="outside", textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Candidates: %{value}<br>%{percent}<extra></extra>",
        pull=[0.04] * len(dcounts),
    )
    fig.update_layout(showlegend=False)
    return _base(fig, "Domain Distribution")


def chart_placement_by_role(df: pd.DataFrame) -> go.Figure:
    """Grouped bar — placement status by role."""
    rs = df.groupby(["Role", "Status"]).size().reset_index(name="Count")
    fig = px.bar(rs, x="Role", y="Count", color="Status",
                 color_discrete_map=STATUS_COLORS, barmode="group",
                 text="Count")
    fig.update_traces(marker_line_width=0, textposition="outside",
                      textfont=dict(size=10))
    fig.update_layout(xaxis_tickangle=-35, legend_title="Status",
                      xaxis_title="", yaxis_title="Candidates")
    return _base(fig, "Placement Status by Role", height=380)


def chart_experience_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram — experience years distribution."""
    fig = px.histogram(df, x="Experience_Years", nbins=18,
                       color_discrete_sequence=[ORANGE])
    fig.update_traces(marker_line_color=NAVY, marker_line_width=1)
    fig.update_layout(xaxis_title="Years of Experience", yaxis_title="Candidates",
                      bargap=0.05)
    return _base(fig, "Experience Distribution")


def chart_monthly_trend(df: pd.DataFrame) -> go.Figure:
    """Area + line — candidates joined per month."""
    MONTH_ORDER = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
                   "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    trend = df["Joined_Month"].value_counts().reset_index()
    trend.columns = ["Month_Year","Count"]
    trend["Month"] = trend["Month_Year"].apply(lambda x: x.split()[0])
    trend["Year"]  = trend["Month_Year"].apply(lambda x: int(x.split()[1]) if len(x.split()) > 1 else 2025)
    trend["Sort"] = trend["Year"] * 100 + trend["Month"].map(MONTH_ORDER).fillna(0).astype(int)

    current_date = pd.Timestamp.today()
    current_sort = current_date.year * 100 + current_date.month

    trend = trend[trend["Sort"] <= current_sort]
    trend = trend.sort_values("Sort")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["Month_Year"], y=trend["Count"],
        mode="lines+markers",
        line=dict(color=ORANGE, width=2.5),
        marker=dict(color=ORANGE2, size=7),
        fill="tozeroy",
        fillcolor="rgba(247,108,27,0.12)",
        name="Candidates",
    ))
    fig.update_layout(xaxis_tickangle=-35, xaxis_title="", yaxis_title="Count",
                      showlegend=False)
    return _base(fig, "Monthly Joining Trend")


def chart_location_map(df: pd.DataFrame) -> go.Figure:
    """Bar chart — candidates by city."""
    lc = df["Location"].value_counts().reset_index()
    lc.columns = ["Location","Count"]
    lc = lc.sort_values("Count")
    fig = px.bar(lc, x="Count", y="Location", orientation="h",
                 color="Count", color_continuous_scale=[[0,"#1A4A8A"],[1,ORANGE]],
                 text="Count")
    fig.update_traces(marker_line_width=0, textposition="outside",
                      textfont=dict(color=WHITE, size=11))
    fig.update_coloraxes(showscale=False)
    fig.update_layout(yaxis_title="", xaxis_title="Candidates")
    return _base(fig, "Candidates by Location")


def chart_match_score_box(df: pd.DataFrame) -> go.Figure:
    """Box plot — match score distribution by domain."""
    fig = px.box(df, x="Domain", y="Match_Score",
                 color="Domain", color_discrete_sequence=COLOR_SEQ,
                 points="outliers")
    fig.update_layout(xaxis_tickangle=-30, showlegend=False,
                      xaxis_title="", yaxis_title="Match Score (%)")
    return _base(fig, "Match Score Distribution by Domain")


def chart_status_funnel(df: pd.DataFrame) -> go.Figure:
    """Funnel chart — recruitment pipeline stages."""
    total   = len(df)
    pending = len(df[df["Status"].isin(["Pending","Placed"])])
    placed  = len(df[df["Status"] == "Placed"])
    fig = go.Figure(go.Funnel(
        y=["Applications Received", "In Review / Pending", "Successfully Placed"],
        x=[total, pending, placed],
        textinfo="value+percent initial",
        marker=dict(color=[ORANGE, "#1E90FF", "#34D399"]),
    ))
    fig.update_layout(showlegend=False)
    return _base(fig, "Recruitment Funnel", height=300)


def chart_client_placements(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar — top clients by placements."""
    placed = df[(df["Status"] == "Placed") & (df["Client_Company"] != "N/A")]
    cc = placed["Client_Company"].value_counts().head(12).reset_index()
    cc.columns = ["Client","Placements"]
    cc = cc.sort_values("Placements")
    fig = px.bar(cc, x="Placements", y="Client", orientation="h",
                 color="Placements",
                 color_continuous_scale=[[0,"#1A4A8A"],[1,"#00C9A7"]],
                 text="Placements")
    fig.update_traces(marker_line_width=0, textposition="outside",
                      textfont=dict(color=WHITE, size=11))
    fig.update_coloraxes(showscale=False)
    fig.update_layout(yaxis_title="", xaxis_title="Placements")
    return _base(fig, "Top Clients by Placements")
