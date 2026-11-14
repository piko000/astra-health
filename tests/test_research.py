from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def test_research_view_separates_evidence_from_demo_data():
    app = AppTest.from_file(str(ROOT / "app.py")).run()
    app.radio[0].set_value("NASA-Forschung").run()
    assert not app.exception
    assert "Keine echte Vitaldatenintegration" in app.info[0].value
    assert len(app.metric) == 0
    assert len(app.get("plotly_chart")) == 0
    content = "\n".join(item.value for item in app.markdown)
    assert content.strip() == (ROOT / "docs" / "RESEARCH_SOURCES.md").read_text(encoding="utf-8").strip()
    assert "https://ntrs.nasa.gov/citations/20220014774" in content
    assert "nicht die medizinische" in content

    app.radio[0].set_value("Demo-Dashboard").run()
    assert not app.exception
    assert "SYNTHETISCHE" in app.info[0].value
    assert len(app.get("plotly_chart")) == 3
    assert "NORMAL" in app.success[0].value


@pytest.mark.parametrize("error", [OSError("unavailable"), UnicodeError("invalid encoding")])
def test_unreadable_research_document_keeps_dashboard_available(monkeypatch, error):
    original_read = Path.read_text

    def read_text(path, *args, **kwargs):
        if path.name == "RESEARCH_SOURCES.md":
            raise error
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
    app = AppTest.from_file(str(ROOT / "app.py")).run()
    app.radio[0].set_value("NASA-Forschung").run()
    assert not app.exception
    assert "konnte nicht geladen werden" in app.error[0].value
    app.radio[0].set_value("Demo-Dashboard").run()
    assert not app.exception
    assert len(app.metric) == 3
