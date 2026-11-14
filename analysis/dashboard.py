"""Dünne UI-Anbindung; die Fachlogik liegt weiterhin in health_monitor."""

import pandas as pd
import plotly.express as px

from analysis.health_monitor import calculate_deviation, classify_health_status
from data.demo import METRICS


def summarize_day(frame: pd.DataFrame, day: int) -> pd.DataFrame:
    current = frame.loc[frame["mission_day"] == day].iloc[0]
    rows = []
    for key, (label, unit, baseline) in METRICS.items():
        value = float(current[key])
        deviation = calculate_deviation(baseline, value)
        rows.append({
            "Vitalwert": label, "Einheit": unit, "Baseline": baseline,
            "Aktuell": value, "Abweichung (%)": deviation,
            "Betrag (%)": abs(deviation),
            "Status": classify_health_status(abs(deviation)),
        })
    return pd.DataFrame(rows)


def vital_chart(frame: pd.DataFrame, key: str, day: int, *, change_day: int | None = None):
    label, unit, baseline = METRICS[key]
    fig = px.line(frame, x="mission_day", y=key, markers=True,
                  labels={"mission_day": "Missionstag", key: f"{label} ({unit})"})
    fig.update_traces(line_color="#38bdf8")
    fig.add_hline(y=baseline, line_dash="dash", annotation_text="Demo-Baseline")
    fig.add_vline(x=day, line_dash="dot", line_color="#f59e0b")
    if change_day is not None:
        fig.add_vline(x=change_day, line_dash="dashdot", line_color="#e879f9",
                      annotation_text=f"Tag {change_day}: künstliche Veränderung",
                      annotation_position="top left")
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
    return fig
