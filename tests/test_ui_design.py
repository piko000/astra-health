from pathlib import Path
from itertools import product
import json

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from analysis.dashboard import vital_chart
from analysis.health_monitor import calculate_deviation, classify_health_status
from data.demo import METRICS, SCENARIOS, SyntheticDataSource
from ui.presentation import data_state, daily_trend, status_period
from ui.theme import COLORS


ROOT = Path(__file__).resolve().parents[1]


def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
    return sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))


@pytest.mark.parametrize("foreground,background", list(product(
    ("text", "muted", "accent", "success", "warning", "critical", "border"),
    ("background", "surface", "elevated"))))
def test_design_contrasts(foreground, background):
    light, dark = sorted([luminance(COLORS[foreground]), luminance(COLORS[background])], reverse=True)
    assert (light + .05) / (dark + .05) >= (3 if foreground == "border" else 4.5)


@pytest.mark.parametrize("scenario,key", list(product(SCENARIOS, METRICS)))
def test_chart_source_values_status_symbols_and_readable_axes(scenario, key):
    frame = SyntheticDataSource().load(scenario)
    fig = vital_chart(frame, key, 22)
    assert list(fig.data[0].x) == list(frame.mission_day)
    assert list(fig.data[0].y) == list(frame[key])
    expected = [classify_health_status(abs(calculate_deviation(METRICS[key][2], v))) for v in frame[key]]
    assert [row[0] for row in fig.data[0].customdata] == expected
    assert list(fig.data[0].marker.symbol) == [dict(NORMAL="circle", WARNING="triangle-up", CRITICAL="diamond")[s] for s in expected]
    assert fig.layout.yaxis.range is None
    assert fig.layout.yaxis.autorange is True
    assert fig.layout.yaxis.automargin is True
    assert fig.layout.xaxis.automargin is True
    assert fig.layout.yaxis.title.text == f"{METRICS[key][0]} ({METRICS[key][1]})"
    assert fig.layout.xaxis.title.text == "Mission day"
    assert fig.layout.xaxis.tickformat == "d"
    assert fig.layout.yaxis.tickformat == "~g"
    assert fig.layout.margin.l >= 80
    assert fig.layout.margin.b >= 60
    changes = [i + 1 for i in range(1, 30) if expected[i] != expected[i - 1]]
    if changes:
        assert list(fig.data[1].x) == changes


@pytest.mark.parametrize("kind,state", [("empty", "NO DATA"), ("missing_day", "NO DATA"),
    ("nan", "UNKNOWN"), ("infinite", "UNKNOWN"), ("schema", "UNKNOWN"),
    ("duplicate", "UNKNOWN"), ("text", "UNKNOWN"), ("gap", "UNKNOWN")])
def test_invalid_data_never_becomes_normal(monkeypatch, kind, state):
    frame = SyntheticDataSource().load(SCENARIOS[0])
    if kind == "empty":
        frame = frame.iloc[:0]
    elif kind == "missing_day":
        frame = frame.iloc[:-1]
    elif kind == "nan":
        frame.loc[29, "sleep_hours"] = float("nan")
    elif kind == "infinite":
        frame.loc[0, "sleep_hours"] = float("inf")
    elif kind == "schema":
        frame = frame.drop(columns="sleep_hours")
    elif kind == "duplicate":
        frame.loc[29, "mission_day"] = 29
    elif kind == "text":
        frame["sleep_hours"] = "unknown"
    else:
        frame = frame.drop(index=10)
    assert data_state(frame, 30)[0] == state
    monkeypatch.setattr(SyntheticDataSource, "load", lambda self, scenario: frame)
    app = AppTest.from_file(str(ROOT / "app.py")).run()
    assert not app.exception
    assert state in app.warning[0].value
    assert not app.success and not app.metric and not app.get("plotly_chart")


def test_source_failure_is_unknown_and_research_remains_available(monkeypatch):
    def fail(self, scenario):
        raise OSError("demo read failure")
    monkeypatch.setattr(SyntheticDataSource, "load", fail)
    app = AppTest.from_file(str(ROOT / "app.py")).run()
    assert not app.exception
    assert "UNKNOWN" in app.error[0].value
    assert not app.success
    app.radio[0].set_value("NASA research").run()
    assert not app.exception
    assert any(s.value == "Space Health Research" for s in app.subheader)


def test_window_changes_chart_range_not_current_analysis():
    app = AppTest.from_file(str(ROOT / "app.py")).run()
    app.selectbox[0].select(SCENARIOS[1])
    app.slider[0].set_value(22).run()
    values = [m.value for m in app.metric]
    app.selectbox[1].select("Last 7 days").run()
    assert not app.exception
    assert [m.value for m in app.metric] == values
    assert "WARNING" in app.warning[0].value
    for chart in app.get("plotly_chart"):
        assert json.loads(chart.proto.spec)["layout"]["xaxis"]["range"] == [15.5, 22.5]
    app.slider[0].set_value(1).run()
    assert not app.exception
    assert json.loads(app.get("plotly_chart")[0].proto.spec)["layout"]["xaxis"]["range"] == [.5, 1.5]


def test_trend_and_status_period_do_not_invent_dates():
    frame = SyntheticDataSource().load(SCENARIOS[0])
    assert "unavailable" in daily_trend(frame, "sleep_hours", 1)
    assert "NORMAL since day 1" in status_period(frame, "sleep_hours", 30)
    difference = frame.sleep_hours.iloc[1] - frame.sleep_hours.iloc[0]
    assert f"{difference:+.2f} h" in daily_trend(frame, "sleep_hours", 2)


def test_long_label_renders_without_losing_metric(monkeypatch):
    label = "Resting heart rate with an extended measurement context description"
    monkeypatch.setitem(METRICS, "resting_heart_rate", (label, "bpm", 60.0))
    app = AppTest.from_file(str(ROOT / "app.py")).run()
    assert not app.exception
    assert app.metric[0].label == label
    assert len(app.get("plotly_chart")) == 3
