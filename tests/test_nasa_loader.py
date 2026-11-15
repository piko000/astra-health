from io import BytesIO
from pathlib import Path
import socket
import zipfile
import json

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from data.nasa_loader import (BIOMARKERS, CSV_NAME, ZIP_NAME, DATA_DIR,
                              NASADataError, load_cmp, validate_cmp)
from ui.nasa_research import research_chart


def frames():
    values = pd.read_csv(DATA_DIR / CSV_NAME, encoding="utf-8-sig")
    with zipfile.ZipFile(DATA_DIR / ZIP_NAME) as archive:
        samples = pd.read_csv(BytesIO(archive.read("s_OSD-575.txt")), sep="\t")
    return values, samples


def test_verified_snapshot_and_metadata_timepoints():
    data = load_cmp()
    assert len(data) == 28
    assert data.Participant.nunique() == 4
    assert data.Timepoint.drop_duplicates().tolist() == ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]
    assert data.loc[data.Timepoint == "R+194", "Time description"].eq("Return plus 194").all()
    glucose = BIOMARKERS["Glucose"][0]
    assert data.loc[data["Sample Name"] == "C001_serum_L-92", glucose].item() == 83
    assert data[BIOMARKERS["Total bilirubin"][0]].isna().sum() == 1


@pytest.mark.parametrize("kind", ["column", "numeric", "infinity", "duplicate", "unmatched",
                                  "time", "unit", "phase", "organism", "empty"])
def test_rejects_invalid_data_or_metadata(kind):
    values, samples = frames()
    key = BIOMARKERS["Glucose"][0]
    if kind == "column":
        values = values.drop(columns=key)
    elif kind == "numeric":
        values[key] = values[key].astype(object)
        values.loc[0, key] = "invalid"
    elif kind == "infinity":
        values[key] = values[key].astype(float)
        values.loc[0, key] = float("inf")
    elif kind == "duplicate":
        values.loc[1, "Sample Name"] = values.loc[0, "Sample Name"]
    elif kind == "unmatched":
        samples = samples.iloc[1:]
    elif kind == "time":
        samples.loc[0, "Factor Value[Time]"] = "Unknown"
    elif kind == "unit":
        samples.loc[0, "Unit"] = "hour"
    elif kind == "phase":
        samples.loc[0, "Factor Value[Spaceflight]"] = "In-flight"
    elif kind == "organism":
        samples.loc[0, "Characteristics[Organism]"] = "Mus musculus"
    else:
        values = values.iloc[:0]
    with pytest.raises(NASADataError):
        validate_cmp(values, samples)


def test_missing_and_changed_local_files_fail_closed(tmp_path):
    with pytest.raises(NASADataError, match="could not be loaded"):
        load_cmp(tmp_path)
    for name in (CSV_NAME, ZIP_NAME):
        (tmp_path / name).write_bytes((DATA_DIR / name).read_bytes())
    (tmp_path / CSV_NAME).write_bytes(b"unverified replacement")
    with pytest.raises(NASADataError, match="Checksum mismatch"):
        load_cmp(tmp_path)


@pytest.mark.parametrize("biomarker", BIOMARKERS)
def test_chart_contains_only_real_measurements(biomarker):
    data = load_cmp()
    column, unit, _ = BIOMARKERS[biomarker]
    chart = research_chart(data, biomarker)
    assert chart.layout.xaxis.type == "category"
    assert unit in chart.layout.yaxis.title.text
    assert sum(len(trace.y) for trace in chart.data) == data[column].notna().sum()
    for trace in chart.data:
        expected = data.loc[(data.Participant == trace.name) & data[column].notna()]
        assert list(trace.y) == expected[column].tolist()
        assert trace.mode == "markers"


def test_research_ui_is_offline_and_handles_missing_values(monkeypatch):
    def no_network(*args, **kwargs):
        raise AssertionError("UI must not access the network")
    monkeypatch.setattr(socket, "create_connection", no_network)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    app.radio[0].set_value("NASA research").run()
    assert not app.exception
    app.selectbox[0].select("Total bilirubin").run()
    assert not app.exception
    assert any("27 measured values" in c.value and "1 missing values" in c.value for c in app.caption)
    assert not app.metric and not app.success and not app.error
    assert len(app.get("plotly_chart")) == 1


def test_missing_nasa_data_does_not_disable_demo(monkeypatch):
    def fail():
        raise NASADataError("NASA files missing")
    monkeypatch.setattr("ui.nasa_research.load_cmp", fail)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    app.radio[0].set_value("NASA research").run()
    assert not app.exception
    assert "NASA files missing" in app.warning[0].value
    assert not app.get("plotly_chart")
    app.radio[0].set_value("Demo dashboard").run()
    assert not app.exception
    assert len(app.metric) == 3


@pytest.mark.parametrize("failure", ["restricted", "changed", "version"])
def test_downloader_rejects_unreviewed_changes_before_overwriting(monkeypatch, tmp_path, failure):
    from data import download_nasa
    catalog = json.loads((DATA_DIR / "files_catalog.json").read_text())
    entries = catalog["studies"]["OSD-575"]["study_files"]
    if failure == "restricted":
        next(e for e in entries if e["file_name"] == CSV_NAME)["restricted"] = True
    def fake_open(url, timeout):
        if url == download_nasa.API:
            payload = json.dumps(catalog).encode()
        elif "/meta/575" in url:
            payload = json.dumps({"study": {"OSD-575": {"version": 4 if failure == "version" else 3}}}).encode()
        else:
            name = CSV_NAME if CSV_NAME in url else ZIP_NAME
            payload = (DATA_DIR / name).read_bytes()
            if failure == "changed" and name == CSV_NAME:
                payload = b"X" + payload[1:]
        response = BytesIO(payload)
        response.url = url
        return response
    monkeypatch.setattr(download_nasa, "ROOT", tmp_path)
    monkeypatch.setattr(download_nasa, "urlopen", fake_open)
    target = tmp_path / CSV_NAME
    target.write_bytes(b"existing snapshot")
    with pytest.raises(ValueError):
        download_nasa.download()
    assert target.read_bytes() == b"existing snapshot"
