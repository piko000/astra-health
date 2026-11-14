# ASTRA Health

A local Streamlit prototype for the NASA Space Apps Hackathon 2026.
All vital signs belong to **fictional astronaut Alex Vega** and are **synthetic**.
No real NASA measurements, medical diagnosis or NASA certification is claimed.

## Start (Python 3.13, PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501`. You can reuse an existing `.venv`. Version pins
reflect the tested local environment. After installation, no measurement service,
AI API or paid service is required. Restart Streamlit if theme changes do not appear.

## Using the dashboard

Choose a mission scenario, assessment day and chart time range in the sidebar.
The overall status and three vital-sign cards show the selected day's values,
baselines, deviations and previous-day trends. The first chart tab shows resting
heart rate; adjacent tabs show sleep duration and activity.

The Mission Health Briefing explains affected indicators, values, baselines,
signed and absolute deviations, the triggered rule and a cautious next review
step. NORMAL includes all three indicators; otherwise only flagged indicators
are included. CRITICAL is prioritized over WARNING, then larger deviations.
The status period identifies the current uninterrupted demo status, not illness onset.

Charts distinguish status by color **and shape**: circle = NORMAL, triangle =
WARNING, diamond = CRITICAL, open square = status change. The anomalous scenario
marks **day 16** as the programmed change onset, not a diagnosis or necessarily
the first warning. The normal scenario has no artificial-change marker.

Time ranges cover the entire mission or the last 14/7 days ending on the selected
day. They change only the visible x-axis, not analysis or source values. The full
mission includes days after the selected day. Y-axes use automatic scaling;
adequate margins and automatic margin adjustment protect titles and numbers.
Formula, chart legend and full source table remain available in expanders.

Empty data or a missing selected day produces **NO DATA**. Invalid values,
schema errors, missing days within the timeline or loading failures produce
**UNKNOWN**. Neither is treated as NORMAL. No assessment is displayed in these
states, and no values are silently repaired or invented.

## Simple architecture

- `app.py`: interface, navigation, metrics and explanations.
- `data/demo.py`: `VitalDataSource` protocol and deterministic generator using
  local `Random(2026)`; identical inputs produce identical values.
- `analysis/health_monitor.py`: original analysis calculations and thresholds.
- `analysis/dashboard.py`: analysis integration and Plotly charts.
- `analysis/briefing.py`: fixed explanation templates; no additional clinical rules.
- `ui/theme.py`: shared color tokens and CSS; `.streamlit/config.toml`: native theme.
- `ui/presentation.py`: defensive UI checks, trend and status-period presentation.
- `tests/`: analysis, data, chart, contrast and Streamlit integration tests.

The arbitrary baselines are 60 bpm resting heart rate, 8 hours of sleep and 60
active minutes per day. The normal scenario varies by ±4%. The anomalous scenario
adds a linear shift starting on day 16, reaching +35%, −30% and −40% respectively
on day 30, in addition to the same random variation. This is a constructed demo,
not a physiological model.

`calculate_deviation(baseline, current)` computes
`(current - baseline) / baseline * 100`.
`classify_health_status(abs(deviation))` classifies the magnitude: below 10% is
NORMAL, 10% to below 25% is WARNING, and 25% or above is CRITICAL. These **demo
rules are not medically validated** and treat increases and decreases equally.
The overall status is the highest individual level, not an additional medical
assessment. Only display values are rounded.

## Scientific foundation and data provenance

Under **View → NASA research**, the Space Health Research view provides sourced
context and an expandable [research dossier](docs/RESEARCH_SOURCES.md). It reads
local documentation and works offline; opening external links requires internet.
Missing or unreadable documentation produces an error without disabling the demo.

The [NASA Human Research Program](https://www.nasa.gov/hrp/) supplies research
context. [NTRS 20220014774](https://ntrs.nasa.gov/citations/20220014774) describes
the relevance of sampling intervals in sleep measurement. These sources do not
validate our alert rules or synthetic trajectories.

**No real measurement data was imported.** HRP, OSDR, NLSP and the official
challenge page were investigated. The dossier documents UTMB, OSDR and sleep-data
candidates, populations, access status, unknown formats/rights and suitability.
No directly usable, fully verified dataset for this assessment was identified.
Some portal pages were unreadable in the tool and the challenge page returned
HTTP 502. This does not establish that suitable NASA data is unavailable.

Peak/exercise heart rate and animal data must not be substituted for human resting
heart rate. Research summaries are not individual mission trajectories. Medical
effectiveness, sensitivity and specificity are unknown.

## Future data integration

A future adapter may implement `VitalDataSource.load()` and replace the instance
in `app.py`. Verify the actual source, rights, UI attribution, schema, units,
time reference, missing values and appropriate baselines first. Adapt the synthetic
labels and scenario selection accordingly. The protocol alone does not validate
external data. Real records must not be filled with invented measurements to fit
the 30-day, three-indicator demo contract.

English localization changes scenario labels to `Normal mission scenario` and
`Anomalous mission scenario`. Summary-table labels are now `Indicator`, `Unit`,
`Baseline`, `Current`, `Deviation (%)`, `Magnitude (%)`, `Status`. Code consuming
the former display labels must use these names. Raw columns (`mission_day`,
`resting_heart_rate`, `sleep_hours`, `activity_minutes`) and function signatures
are unchanged. Exception messages are now English; exception types are unchanged.

## External resources and AI disclosure

All demo measurements are generated locally. No external images, font files,
datasets or NASA assets are embedded. Software resources:

- [Python](https://www.python.org/): runtime and standard library (`random`).
- [Streamlit](https://streamlit.io/): local UI and AppTest.
- [Pandas](https://pandas.pydata.org/): tables.
- [Plotly](https://plotly.com/python/): interactive charts.
- [pytest](https://docs.pytest.org/): tests.

Codex assisted implementation, research, documentation, translation and tests.
The application itself does not use an AI model. See [AI_USAGE.md](docs/AI_USAGE.md).
Design decisions, official NASA/W3C references, contrast calculations, responsive
rules and verification limits are documented in [UI_DESIGN.md](docs/UI_DESIGN.md).

## Tests and verification history

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

Caching is disabled because the existing `.pytest_cache` was not writable in the
working environment; this does not affect test behavior. AppTest verifies UI
execution and interactions, not actual browser geometry or Plotly mouse behavior.

Recorded runs on 14 November 2026, Python 3.13.16:

| Milestone | Result |
| --- | --- |
| Original analysis | 12 passed; cache-permission warning only |
| Initial dashboard | 20 passed in 4.81s |
| Research view | 23 passed in 3.74s |
| Briefing/scenario tests | 14 passed in 4.01s; full suite 37 passed in 5.87s |
| Interface redesign | 76 passed in 9.83s |
| Axis correction | 76 passed in 10.24s |
| Interface text cleanup | 76 passed in 10.10s |
| English translation | 76 passed in 9.87s |

During research-view development, one initial assertion failed because Streamlit
removed a trailing newline; the test now normalizes outer whitespace. During
redesign, two parametrization deprecation warnings were resolved by using lists.
All original test cases remain; English localization updates their text expectations.

The redesign's before/after comparison found identical results for all 60 daily
assessments and unchanged core analysis, generator and briefing file hashes.
The translation check compares values and statuses independently of display labels.
All synthetic values and all 60 daily assessments were identical before and after
translation. A final scan found no remaining German text in project code, tests
or documentation. English rendering has not been visually checked in a browser.

Calculated text contrast is at least 4.5:1 for tested combinations, and relevant
borders at least 3:1. **This is not a complete WCAG audit.** Browser/screenshot
tools were unavailable. Desktop, laptop, tablet and mobile layouts are implemented,
but geometry, focus behavior, screen readers and overflow need manual checks.

## Suggested demonstration

1. Normal scenario, day 30: explain NORMAL and the three indicators.
2. Anomalous scenario, day 16: show the artificial change marker.
3. Day 22: explain WARNING, affected indicators and the briefing.
4. Day 30: show CRITICAL as a demo level, not a diagnosis.
5. Open Space Health Research and disclose sources and AI assistance.

For submission, describe the project as a **prototype with synthetic vital signs
and sourced NASA research context**. Real data integration remains future work
after source, rights and protocol verification.
