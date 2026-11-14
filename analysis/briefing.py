"""Deterministic explanation of existing statuses; no new diagnostic logic."""

import pandas as pd


RULE_TEXT = {
    "NORMAL": "|d| < 10 %",
    "WARNING": "10 % ≤ |d| < 25 %",
    "CRITICAL": "|d| ≥ 25 %",
}
NEXT_STEP = {
    "NORMAL": "Continue reviewing the trend; NORMAL only means that no demo threshold has been reached.",
    "WARNING": "Check the value, baseline and measurement context; compare with adjacent days.",
    "CRITICAL": "Verify the value and baseline first; real data would require professional assessment.",
}


def mission_briefing(summary: pd.DataFrame) -> dict:
    """Uses the classification from summarize_day without recalculating it."""
    statuses = set(summary["Status"])
    status = "CRITICAL" if "CRITICAL" in statuses else "WARNING" if "WARNING" in statuses else "NORMAL"
    affected = summary.loc[summary["Status"] != "NORMAL"]
    rows = affected if not affected.empty else summary
    explanations = []
    for _, row in rows.iterrows():
        explanations.append(
            f'**{row["Indicator"]} · {row["Status"]}**\n\n'
            f'Synthetic value {row["Current"]:.2f} {row["Unit"]}; '
            f'Baseline {row["Baseline"]:g} {row["Unit"]}. '
            f'Deviation {row["Deviation (%)"]:+.2f} % '
            f'(Magnitude {row["Magnitude (%)"]:.2f} %). '
            f'Demo rule: {RULE_TEXT[row["Status"]]}.'
        )
    return {
        "status": status,
        "affected": affected["Indicator"].tolist(),
        "explanations": explanations,
        "next_step": NEXT_STEP[status],
    }
