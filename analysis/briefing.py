"""Deterministische Erklärung vorhandener Statuswerte; keine neue Diagnose-Logik."""

import pandas as pd


RULE_TEXT = {
    "NORMAL": "|d| < 10 %",
    "WARNING": "10 % ≤ |d| < 25 %",
    "CRITICAL": "|d| ≥ 25 %",
}
NEXT_STEP = {
    "NORMAL": "Verlauf weiter ansehen; NORMAL bedeutet nur, dass keine Demo-Grenze erreicht ist.",
    "WARNING": "Wert, Baseline und Erfassungskontext prüfen; den Verlauf mit benachbarten Tagen vergleichen.",
    "CRITICAL": "Wert und Baseline zuerst verifizieren; bei realen Daten wäre eine fachliche Beurteilung nötig.",
}


def mission_briefing(summary: pd.DataFrame) -> dict:
    """Übernimmt die Klassifikation aus summarize_day, statt sie neu zu berechnen."""
    statuses = set(summary["Status"])
    status = "CRITICAL" if "CRITICAL" in statuses else "WARNING" if "WARNING" in statuses else "NORMAL"
    affected = summary.loc[summary["Status"] != "NORMAL"]
    rows = affected if not affected.empty else summary
    explanations = []
    for _, row in rows.iterrows():
        explanations.append(
            f'**{row["Vitalwert"]} · {row["Status"]}**\n\n'
            f'Synthetischer Wert {row["Aktuell"]:.2f} {row["Einheit"]}; '
            f'Baseline {row["Baseline"]:g} {row["Einheit"]}. '
            f'Abweichung {row["Abweichung (%)"]:+.2f} % '
            f'(Betrag {row["Betrag (%)"]:.2f} %). '
            f'Demo-Regel: {RULE_TEXT[row["Status"]]}.'
        )
    return {
        "status": status,
        "affected": affected["Vitalwert"].tolist(),
        "explanations": explanations,
        "next_step": NEXT_STEP[status],
    }
