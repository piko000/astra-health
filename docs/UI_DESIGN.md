# ASTRA Health — UI design and validation

M5 addition (15 November 2026): the NASA research view now has a separate measured
serum-biomarker scatter plot and missing-value table. Its categorical sampling
axis and participant symbols are independent of the synthetic charts and demo
alert colors/rules. See [OSD575.md](OSD575.md) for provenance and validation.

As of 14 November 2026. A local hackathon prototype, not certified mission software.

## Baseline review and implementation priorities

The redesign started with Streamlit 1.67.0, Pandas 3.1.1, Plotly 7.1.0, pytest
9.2.0 and 37 passing tests. `app.py` controlled two views; `analysis/dashboard.py`
connected analysis to charts, while `analysis/briefing.py` generated explanations.
The analysis and synthetic generator were preserved.

Existing interactions included scenario/day selection, three chart tabs, Plotly
hover/zoom, briefing, formula, source table and research view. Weaknesses included
inconsistent styling, equally weighted explanatory text, no chart status markers,
no time ranges and insufficient protection against invalid data.

Priorities: shared tokens → compact overview → explainable chart symbols →
defensive UI states → contrast/integration tests. No framework migration, added
services, images, external fonts or new dependencies.

## Design philosophy and references

Calm surfaces, limited accents, clear language and progressive disclosure.
The hierarchy is Overview → Detect → Explain → Investigate → Act. Related
information is grouped spatially. Alerts always include text, not just color.
Full details remain accessible through expanders.

The [NASA Human Integration Design Handbook, Revision 1, section 10.6](https://www.nasa.gov/wp-content/uploads/2023/03/human-integration-design-handbook-revision-1.pdf)
addresses relevant, interpretable and readable information. It informs the
presentation of values, deviations and references here; no formal NASA compliance
or human-in-the-loop study is claimed. The
[official HIDH overview](https://www.nasa.gov/human-integration-design-handbook/)
describes its role as a supplementary design reference.

[WCAG 2.2](https://www.w3.org/TR/WCAG22/) informs text/non-text contrast, visible
focus and operability. Calculated color tests are partial evidence, not complete
WCAG certification. Labeled states, consistent cards, data checks and named tabs
implement visibility, consistency, error prevention and recognition. This is a
heuristic design, not a completed usability study.

## Tokens and contrast

`ui/theme.py` defines shared colors; `.streamlit/config.toml` applies matching
base colors to native widgets. Plotly uses the same tokens.

| Token | Color | Purpose |
| --- | --- | --- |
| background | `#0B1220` | Page and chart background |
| surface | `#172235` | Cards, navigation, status surfaces |
| elevated | `#1E2D42` | Active tabs and tooltips |
| accent | `#38BDF8` | Trend line, links, focus |
| text | `#F1F5F9` | Primary text |
| muted | `#A8B6C9` | Metadata and reference lines |
| success | `#34D399` | NORMAL |
| warning | `#FBBF24` | WARNING |
| critical | `#FB7185` | CRITICAL |
| border | `#718399` | Relevant outlines |

Warning and critical colors were lightened from the initial proposal to give
small status labels sufficient contrast. No animations, shadows or decorative gradients.

Calculated contrast using relative sRGB luminance:

| Foreground | background | surface | elevated |
| --- | ---: | ---: | ---: |
| text | 17.09 | 14.56 | 12.70 |
| muted | 9.09 | 7.75 | 6.76 |
| accent | 8.74 | 7.45 | 6.50 |
| success | 9.74 | 8.30 | 7.24 |
| warning | 11.22 | 9.55 | 8.34 |
| critical | 6.96 | 5.93 | 5.17 |
| border | 4.82 | 4.11 | 3.58 |

Tested text combinations meet 4.5:1; outlines meet 3:1. The formula is
`(L_lighter + 0.05) / (L_darker + 0.05)` using linearized sRGB channels.
Decorative gridlines intentionally have lower contrast and carry no independent
information. Native overlays, toolbars and actual browser states are not fully audited.

## Typography and spacing

System fonts (`system-ui`, Segoe UI fallback); Plotly uses Segoe UI/sans-serif.
No font downloads. Tabular numerals for measurements and UI.

- Heading: 32 px, 28 px on mobile; section headings approximately 21 px.
- Measurements: 32 px; card labels: 15 px; body: 16 px; metadata: 14 px.
- Base spacing: 8 px, small gaps: 4 px, tabs: 8/16 px, top padding: 24 px,
  desktop side padding: 32 px, mobile: 16 px. Streamlit still controls some native
  spacing; an exact universal 8 px grid is not claimed.
- Maximum content width: 1600 px.

## Information architecture

1. Header: ASTRA Health, fictional mission ASTRA-DEMO and fictional participant.
   No invented sensor, live connection or measurement timestamp.
2. One prominent synthetic-data notice. Assessment day appears in status and cards.
3. Overall status and affected indicators; three cards show status, value, unit,
   demo baseline, relative deviation and previous-day trend.
4. Chart and briefing side by side. Higher severity comes first, then larger
   absolute deviation. The first briefing entry is expanded; further entries are
   collapsible. The cautious next review step is shown first.
5. Formula, complete source data, legend and a separate research view remain accessible.

The baseline is an arbitrary demo assumption, not a measured personal reference.
Trend means absolute change from the immediately preceding day, not a medical
judgment. Day 1 explicitly has no previous-day comparison. The briefing's period
describes an uninterrupted demo status, not illness onset.

Developer notices, repeated explanations, seed details and implementation names
have been removed from the main interface. AI disclosure remains in project
documentation. Essential provenance and demo-rule limitations remain visible.

## Chart guidelines

- Three line charts in tabs, consistent interactions, indicator-specific units.
- Dashed baseline, dotted assessment day, optional dash-dot marker for the
  programmed artificial change on day 16.
- NORMAL = circle, WARNING = triangle, CRITICAL = diamond. An open square marks
  status changes. Tooltips show value, unit, signed deviation and status; the
  expandable text legend explains all symbols.
- Entire mission or last 14/7 days ending on the selected day. Time selection
  changes only the x-axis, not analysis or values. The full mission includes
  days after the selected day.
- Following user feedback, forced zero-based scaling was removed. Plotly again
  scales y-axes automatically to the data, explicitly noted in the UI. Numbers
  use no SI abbreviations and mission days are integers. Chart height: 400 px;
  left/right/top/bottom margins: 88/32/64/72 px, with automatic margin adjustment.
  The compact x-axis title is “Mission day”. Values and baselines are unchanged.
- No clinical reference bands, 3D charts or pie charts. The UI stops assessment
  as UNKNOWN rather than drawing continuous curves across missing days.
- The source table provides an alternative to visual charts. Full Plotly
  screen-reader accessibility has not been established.

## Error states and accessibility

`ui/presentation.py` checks table type, schema, finite numeric values and unique,
sorted integer mission days before calling the existing analysis.

| UI state | Meaning and presentation |
| --- | --- |
| NORMAL | Existing demo rule; labeled status, no promise of health |
| WARNING | Existing demo rule; alert card with symbol and affected indicators |
| CRITICAL | Existing demo rule; prioritized alert and explanation |
| NO DATA | Empty source or missing selected day; no assessment/cards |
| UNKNOWN | Invalid schema, NaN/Inf, timeline gaps or loading failure; no assessment/cards |

UNKNOWN/NO DATA never become NORMAL. Even one invalid indicator conservatively
stops the complete assessment in this UI version. Available tabular source data
remains inspectable; no silent imputation occurs. Research navigation remains usable.

Native widgets retain semantics and labels. CSS adds a 3 px focus ring, buttons
at least 44 px high, underlined links and an active tab distinguished by text,
surface and underline. Focus, screen readers and hover still need browser review.
Some CSS uses Streamlit `data-testid` selectors and may require updates when the
framework changes.

## Responsive behavior and limits

| Target viewport | Implemented layout | Visually verified? |
| --- | --- | --- |
| 1920 × 1080 | Maximum width 1600 px; three cards; chart and briefing side by side | No |
| 1366 × 768 | Compact header; three cards; chart and briefing side by side | No |
| 1024 × 768 | Analysis area stacked below 1100 CSS px | No |
| 390 × 844 | Stacked cards, wrapping tabs, 16 px margins below 700 px | No |

Sidebar width and zoom affect available space. Charts scale with their containers;
long card labels can wrap. Vertical scrolling is expected on small displays.
Overflow, clipping and exact first-screen visibility are **not verified** without
a browser tool. English labels may need different space from the former German labels.

## Validation and open work

Automated coverage includes NORMAL/WARNING/CRITICAL scenarios, color calculations,
chart values versus source data, status symbols/transitions, time ranges without
analysis changes, empty data, missing days, NaN/Inf, schema errors, duplicates,
text values, timeline gaps, loading errors, long labels and research navigation.
A long label passing AppTest does not establish correct screen geometry.

Before presenting, manually check all four target sizes, 200% zoom, Tab/arrow-key
operation, focus with sidebar open, chart hover, day-16 labels, long labels and
all status/error states. No browser/screenshot test or medical validation was performed.

The redesign's full test run passed **76 tests in 9.83s** (37 existing, 39 new).
Earlier iterator-parametrization warnings were fixed by converting iterators to
lists. The final redesign run had no test warnings.

The redesign's comparison of 60 daily assessments had identical serialized JSON
SHA-256 `eb3d4395432a5f403f1b0374445657d1a8347d6ea8b2d1d202aa3331989785c3`.
At that stage, core analysis, generator and briefing files were byte-identical.
The later English translation intentionally changes labels, error text and
comments, so that historical byte-level claim does not apply to translation.
Translation verification instead compares numeric outputs and statuses across
all days and both scenarios; existing test expectations are translated in place.
