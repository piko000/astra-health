"""Thin UI integration; domain logic remains in health_monitor."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from analysis.health_monitor import calculate_deviation, classify_health_status
from data.demo import METRICS
from ui.theme import COLORS, STATUS_COLORS
from ui.presentation import status_series


def summarize_day(frame: pd.DataFrame, day: int) -> pd.DataFrame:
    current = frame.loc[frame["mission_day"] == day].iloc[0]
    rows = []
    for key, (label, unit, baseline) in METRICS.items():
        value = float(current[key])
        deviation = calculate_deviation(baseline, value)
        rows.append({
            "Indicator": label, "Unit": unit, "Baseline": baseline,
            "Current": value, "Deviation (%)": deviation,
            "Magnitude (%)": abs(deviation),
            "Status": classify_health_status(abs(deviation)),
        })
    return pd.DataFrame(rows)


def vital_chart(frame: pd.DataFrame, key: str, day: int, *, change_day: int | None = None):
    label, unit, baseline = METRICS[key]
    fig = px.line(frame, x="mission_day", y=key, markers=True,
                  labels={"mission_day": "Mission day", key: f"{label} ({unit})"})
    statuses = status_series(frame, key)
    symbols = {"NORMAL": "circle", "WARNING": "triangle-up", "CRITICAL": "diamond"}
    fig.update_traces(
        line=dict(color=COLORS["accent"], width=2.5),
        marker=dict(color=[STATUS_COLORS[s] for s in statuses],
                    symbol=[symbols[s] for s in statuses], size=8),
        customdata=[[s, calculate_deviation(baseline, v)] for s, v in zip(statuses, frame[key])],
        hovertemplate=(f"Day %{{x}} · {label}<br>%{{y:.2f}} {unit}<br>"
                       "Deviation %{customdata[1]:+.2f} %<br>"
                       "%{customdata[0]} · synthetic<extra></extra>"),
    )
    changes = [i for i in range(1, len(statuses)) if statuses[i] != statuses[i - 1]]
    if changes:
        fig.add_trace(go.Scatter(
            x=frame.iloc[changes]["mission_day"], y=frame.iloc[changes][key],
            mode="markers", name="Status change", hoverinfo="skip",
            marker=dict(symbol="square-open", size=16, color=COLORS["text"], line_width=2),
        ))
    fig.add_hline(y=baseline, line_dash="dash", line_color=COLORS["muted"], annotation_text="Demo baseline")
    fig.add_vline(x=day, line_dash="dot", line_color=COLORS["text"])
    if change_day is not None:
        fig.add_vline(x=change_day, line_dash="dashdot", line_color=COLORS["muted"],
                      annotation_text=f"Day {change_day}: artificial change",
                      annotation_position="top left")
    fig.update_layout(
        height=400, margin=dict(l=88, r=32, t=64, b=72, autoexpand=True),
        paper_bgcolor=COLORS["background"], plot_bgcolor=COLORS["background"],
        font=dict(family="Segoe UI, sans-serif", size=14, color=COLORS["text"]),
        hoverlabel=dict(bgcolor=COLORS["elevated"], font_color=COLORS["text"]),
        legend=dict(orientation="h", y=1.12, x=0),
    )
    # As before the redesign: Plotly scales the range to the data.
    # Automatic margins reserve space for numbers and complete titles.
    fig.update_yaxes(autorange=True, automargin=True, tickformat="~g",
                     title_standoff=16, gridcolor=COLORS["surface"], zeroline=False)
    fig.update_xaxes(dtick=5, tick0=0, tickformat="d", automargin=True,
                     title_standoff=16, showgrid=False, title="Mission day")
    return fig
