from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from analysis.dashboard import summarize_day, vital_chart
from analysis.health_monitor import calculate_deviation, classify_health_status
from data.demo import METRICS, SCENARIOS, SyntheticDataSource


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_reproducible_complete_data(scenario):
    source = SyntheticDataSource()
    frame = source.load(scenario)
    pd.testing.assert_frame_equal(frame, source.load(scenario))
    assert list(frame["mission_day"]) == list(range(1, 31))
    assert frame[list(METRICS)].notna().all().all()
    assert (frame[list(METRICS)] > 0).all().all()


def test_unknown_scenario_rejected():
    with pytest.raises(ValueError, match="Unknown scenario"):
        SyntheticDataSource().load("NASA live")


def test_scenarios_and_existing_analysis_are_connected():
    source = SyntheticDataSource()
    normal, unusual = [source.load(s) for s in SCENARIOS]
    pd.testing.assert_frame_equal(normal.iloc[:15], unusual.iloc[:15])
    for day in range(1, 31):
        assert set(summarize_day(normal, day)["Status"]) == {"NORMAL"}
    assert "WARNING" in set(summarize_day(unusual, 22)["Status"])
    summary = summarize_day(unusual, 30)
    assert set(summary["Status"]) == {"CRITICAL"}
    assert summary.iloc[1]["Deviation (%)"] < 0
    for _, row in summary.iterrows():
        deviation = calculate_deviation(row["Baseline"], row["Current"])
        assert row["Deviation (%)"] == pytest.approx(deviation)
        assert row["Status"] == classify_health_status(abs(deviation))


@pytest.mark.parametrize("key", METRICS)
def test_chart_contains_data_baseline_and_selected_day(key):
    frame = SyntheticDataSource().load(SCENARIOS[0])
    fig = vital_chart(frame, key, 22)
    assert list(fig.data[0].x) == list(frame["mission_day"])
    assert list(fig.data[0].y) == list(frame[key])
    assert fig.layout.shapes[0].y0 == METRICS[key][2]
    assert fig.layout.shapes[1].x0 == 22


def test_ui_scenario_and_day_selection():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    assert not app.exception
    assert app.title[0].value == "ASTRA Health"
    assert "SYNTHETIC" in app.info[0].value
    assert "NORMAL" in app.success[0].value
    assert len(app.metric) == 3
    assert len(app.get("plotly_chart")) == 3
    assert any("Demo rules are not medically validated" in c.value for c in app.caption)

    app.selectbox[0].select(SCENARIOS[1]).run()
    assert not app.exception
    assert "CRITICAL" in app.error[0].value
    assert any("Magnitude" in m.value and "CRITICAL" in m.value for m in app.markdown)

    app.slider[0].set_value(22).run()
    assert not app.exception
    assert "WARNING" in app.warning[0].value

    app.slider[0].set_value(1).run()
    assert not app.exception
    assert "NORMAL" in app.success[0].value
