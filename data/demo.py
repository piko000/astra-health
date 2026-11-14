"""Fiktive Werte; keine NASA-Messdaten oder medizinischen Referenzwerte."""

from random import Random
from typing import Protocol

import pandas as pd


SCENARIOS = ("Normaler Missionsverlauf", "Auffälliger Missionsverlauf")
# Schlüssel: (Anzeigename, Einheit, frei gewählte Demo-Baseline)
METRICS = {
    "resting_heart_rate": ("Ruheherzfrequenz", "bpm", 60.0),
    "sleep_hours": ("Schlafdauer", "h", 8.0),
    "activity_minutes": ("Aktivität", "min/Tag", 60.0),
}


class VitalDataSource(Protocol):
    """Adaptervertrag: 30 Tageszeilen, mission_day und METRICS-Spalten.

    Werte müssen endlich, numerisch und in den oben definierten Einheiten
    vorliegen. Ein künftiger Adapter muss Herkunft, Einheiten, Fehlwerte und
    geeignete Baselines explizit klären; hier ist keine NASA-Quelle angebunden.
    """

    def load(self, scenario: str) -> pd.DataFrame: ...


class SyntheticDataSource:
    """Deterministische Demo mit lokalem Zufallsgenerator, Seed 2026."""

    def load(self, scenario: str) -> pd.DataFrame:
        if scenario not in SCENARIOS:
            raise ValueError(f"Unbekanntes Szenario: {scenario}")
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
