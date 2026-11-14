"""Fictional values; no NASA measurements or medical reference values."""

from random import Random
from typing import Protocol

import pandas as pd


SCENARIOS = ("Normal mission scenario", "Anomalous mission scenario")
# Key: (display name, unit, arbitrary demo baseline)
METRICS = {
    "resting_heart_rate": ("Resting heart rate", "bpm", 60.0),
    "sleep_hours": ("Sleep duration", "h", 8.0),
    "activity_minutes": ("Activity", "min/day", 60.0),
}


class VitalDataSource(Protocol):
    """Adapter contract: 30 daily rows, mission_day and METRICS columns.

    Values must be finite, numeric and use the units defined above.
    A future adapter must explicitly address provenance, units, missing values
    and suitable baselines; no NASA data source is connected here.
    """

    def load(self, scenario: str) -> pd.DataFrame: ...


class SyntheticDataSource:
    """Deterministic demo using a local random generator, seed 2026."""

    def load(self, scenario: str) -> pd.DataFrame:
        if scenario not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        rng = Random(2026)
        rows = []
        for day in range(1, 31):
            progress = max(0, day - 15) / 15 if scenario == SCENARIOS[1] else 0
            row = {"mission_day": day}
            for key, shift in zip(METRICS, (0.35, -0.30, -0.40)):
                baseline = METRICS[key][2]
                row[key] = round(baseline * (1 + rng.uniform(-0.04, 0.04) + shift * progress), 2)
            rows.append(row)
        return pd.DataFrame(rows)
