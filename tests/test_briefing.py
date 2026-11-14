from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from analysis.briefing import mission_briefing, RULE_TEXT
from analysis.dashboard import summarize_day, vital_chart
from data.demo import METRICS, SCENARIOS, SyntheticDataSource


@pytest.mark.parametrize("deviation,status", [(-25, "CRITICAL"), (-10, "WARNING"),
                                              (0, "NORMAL"), (9, "NORMAL"),
                                              (10, "WARNING"), (25, "CRITICAL")])
def test_briefing_explains_existing_boundaries_in_both_directions(deviation, status):
    row = {key: baseline for key, (_, _, baseline) in METRICS.items()}
    row.update(mission_day=1, resting_heart_rate=60 * (1 + deviation / 100))
    briefing = mission_briefing(summarize_day(pd.DataFrame([row]), 1))
    assert briefing["status"] == status
    assert RULE_TEXT[status] in briefing["explanations"][0]
    assert f"{deviation:+.2f} %" in briefing["explanations"][0]
    assert "Baseline 60 bpm" in briefing["explanations"][0]
    assert briefing["affected"] == ([] if status == "NORMAL" else ["Ruheherzfrequenz"])
    assert briefing["next_step"]


@pytest.mark.parametrize("key", METRICS)
def test_artificial_change_marker_is_explicit_and_optional(key):
    frame = SyntheticDataSource().load(SCENARIOS[1])
    fig = vital_chart(frame, key, 16, change_day=16)
    assert fig.layout.shapes[2].x0 == 16
    assert any("Tag 16: künstliche Veränderung" in a.text for a in fig.layout.annotations)
    assert len(vital_chart(frame, key, 16).layout.shapes) == 2


@pytest.mark.parametrize("scenario,day,status", [
    (SCENARIOS[0], 30, "NORMAL"),
    (SCENARIOS[1], 15, "NORMAL"),
    (SCENARIOS[1], 16, "NORMAL"),
    (SCENARIOS[1], 22, "WARNING"),
    (SCENARIOS[1], 30, "CRITICAL"),
])
def test_mission_warning_card_and_briefing(scenario, day, status):
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    app.selectbox[0].select(scenario)
    app.slider[0].set_value(day).run()
    assert not app.exception
    alerts = {"NORMAL": app.success, "WARNING": app.warning, "CRITICAL": app.error}
    assert len(alerts[status]) == 1
    card = alerts[status][0].value
    assert f"Demo-Gesamtstatus: {status} · Tag {day}" in card
    assert "keine Diagnose" in card
    assert len(app.metric) == 3
    assert [tab.label for tab in app.tabs] == [label for label, _, _ in METRICS.values()]
    summary = summarize_day(SyntheticDataSource().load(scenario), day)
    expected = mission_briefing(summary)
    markdown = "\n".join(item.value for item in app.markdown)
    for indicator in expected["affected"]:
        assert indicator in card
    for explanation in expected["explanations"]:
        assert explanation in markdown
    assert expected["next_step"] in markdown
    if scenario == SCENARIOS[1]:
        assert any("Tag 16 markiert" in c.value for c in app.caption)
    else:
        assert not any("Tag 16 markiert" in c.value for c in app.caption)
