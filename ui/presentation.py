"""UI states and time context; no new medical status rules."""

from math import isfinite

import pandas as pd

from analysis.health_monitor import calculate_deviation, classify_health_status
from data.demo import METRICS


def data_state(frame: pd.DataFrame, day: int) -> tuple[str, str]:
    """Stops rendering before analysis; does not impute or repair data."""
    if not isinstance(frame, pd.DataFrame):
        return "UNKNOWN", "The data source did not return a table. Check the data format."
    if frame.empty:
        return "NO DATA", "No daily data available. Check the source and selection."
    required = ["mission_day", *METRICS]
    if any(key not in frame for key in required):
        return "UNKNOWN", "The data format is incomplete. Check the required columns."
    for key in required:
        if not pd.api.types.is_numeric_dtype(frame[key]) or pd.api.types.is_bool_dtype(frame[key]):
            return "UNKNOWN", "Nonnumeric values: check the data format."
        if not frame[key].map(lambda value: pd.notna(value) and isfinite(value)).all():
            return "UNKNOWN", "Missing or nonfinite values: no reliable assessment available."
    days = frame["mission_day"]
    if days.duplicated().any() or not days.is_monotonic_increasing or not days.between(1, 30).all() or (days % 1 != 0).any():
        return "UNKNOWN", "Mission days must be unique, sorted integers between 1 and 30."
    if day not in days.values:
        return "NO DATA", f"No values available for day {day}. Select an available day."
    if (days.diff().dropna() != 1).any():
        return "UNKNOWN", "The timeline contains missing days. A continuous curve cannot be displayed."
    return "READY", "Data available for demo assessment."


def status_series(frame: pd.DataFrame, key: str) -> list[str]:
    baseline = METRICS[key][2]
    return [classify_health_status(abs(calculate_deviation(baseline, value))) for value in frame[key]]


def status_period(frame: pd.DataFrame, key: str, day: int) -> str:
    """Start of the current continuously observed demo status, not illness onset."""
    past = frame.loc[frame["mission_day"] <= day]
    statuses = status_series(past, key)
    days = past["mission_day"].tolist()
    start = len(days) - 1
    while start > 0 and statuses[start - 1] == statuses[-1] and days[start] - days[start - 1] == 1:
        start -= 1
    return f"{statuses[-1]} since day {days[start]:g} · Assessment day {day}"


def daily_trend(frame: pd.DataFrame, key: str, day: int) -> str:
    previous = frame.loc[frame["mission_day"] == day - 1, key]
    if previous.empty:
        return "Previous-day comparison unavailable"
    current = frame.loc[frame["mission_day"] == day, key].iloc[0]
    difference = current - previous.iloc[0]
    direction = "↑ Increase" if difference > 0 else "↓ Decrease" if difference < 0 else "→ Unchanged"
    return f"{direction} · {difference:+.2f} {METRICS[key][1]} from previous day"
