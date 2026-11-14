"""Local ASTRA Health demo: python -m streamlit run app.py."""

from pathlib import Path
from html import escape

import streamlit as st
from pandas import DataFrame

from analysis.dashboard import summarize_day, vital_chart
from analysis.briefing import mission_briefing
from data.demo import METRICS, SCENARIOS, SyntheticDataSource, VitalDataSource
from ui.theme import stylesheet, STATUS_COLORS
from ui.presentation import data_state, daily_trend, status_period


RESEARCH_PATH = Path(__file__).resolve().parent / "docs" / "RESEARCH_SOURCES.md"


def show_research():
    """Local, sourced information view without network requests or measurement imports."""
    st.info("Research information · No real vital-sign data integration. "
            "All dashboard vital signs remain synthetic.")
    st.subheader("Space Health Research")
    st.caption("Research source: [NASA HRP](https://www.nasa.gov/hrp/) studies "
               "health and performance in space and analog environments.")
    st.caption("Research source: [NTRS 20220014774](https://ntrs.nasa.gov/citations/20220014774) "
               "compares continuous and intermittent sleep measurements. "
               "Sampling intervals and missing measurements affect interpretation.")
    st.caption("These sources do not validate the demo baselines or alert rules.")
    try:
        content = RESEARCH_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        st.error("The research documentation could not be loaded. "
                 "The dashboard remains available.")
        return
    with st.expander("Sources, candidate datasets and limitations"):
        st.markdown(content)


def main():
    st.set_page_config(page_title="ASTRA Health", page_icon="🚀", layout="wide")
    st.html(stylesheet())
    st.title("ASTRA Health")
    st.caption("Mission ASTRA-DEMO · Alex Vega (fictional)")
    view = st.sidebar.radio("View", ("Demo dashboard", "NASA research"))
    if view == "NASA research":
        show_research()
        return
    st.info("SYNTHETIC DEMO DATA · No real NASA measurements or medical diagnosis.")
    st.sidebar.header("Explore mission")
    scenario = st.sidebar.selectbox("Mission scenario", SCENARIOS)
    day = st.sidebar.slider("Assessment day", 1, 30, 30)
    window = st.sidebar.selectbox("Chart time range", ("Entire mission", "Last 14 days", "Last 7 days"),
                                  help="Short time ranges end on the selected assessment day.")
    st.sidebar.caption("Activity = active minutes per day")

    source: VitalDataSource = SyntheticDataSource()
    try:
        frame = source.load(scenario)
    except (OSError, ValueError) as error:
        st.error("UNKNOWN · Data source could not be loaded. No health assessment available.")
        with st.expander("Technical error details"):
            st.code(str(error))
        return
    state, message = data_state(frame, day)
    if state != "READY":
        st.warning(f"{state} · {message} No health assessment available.")
        if isinstance(frame, DataFrame):
            with st.expander("Inspect available source data"):
                st.dataframe(frame, hide_index=True, width="stretch")
        return
    summary = summarize_day(frame, day)
    briefing = mission_briefing(summary)
    status = briefing["status"]
    display = {"NORMAL": st.success, "WARNING": st.warning, "CRITICAL": st.error}
    affected = ", ".join(briefing["affected"]) or "No demo threshold reached"
    display[status](f"**Overall demo status: {status} · Day {day}**\n\n{affected}. "
                    "Demo assessment, not a diagnosis.",
                    icon={"NORMAL": "✅", "WARNING": "⚠️", "CRITICAL": "🚨"}[status])

    for column, (key, (_, row)) in zip(st.columns(3), zip(METRICS, summary.iterrows())):
        with column, st.container(border=True, key=f"vital_{key}"):
            st.html(f'<p class="astra-status" style="color:{STATUS_COLORS[row["Status"]]}">'
                    f'{escape(row["Status"])} · Day {day:02d}</p>')
            st.metric(row["Indicator"], f'{row["Current"]:.2f} {row["Unit"]}',
                      f'{row["Deviation (%)"]:+.2f} % from demo baseline', delta_color="off")
            st.caption(f'Demo baseline: {row["Baseline"]:g} {row["Unit"]}')
            st.caption(daily_trend(frame, key, day))

    with st.container(key="analysis_layout"):
        chart_column, briefing_column = st.columns([2, 1], gap="large")
    with chart_column:
        st.subheader("Mission timeline")
        tabs = st.tabs([label for label, _, _ in METRICS.values()])
        change_day = 16 if scenario == SCENARIOS[1] else None
        for tab, key in zip(tabs, METRICS):
            with tab:
                fig = vital_chart(frame, key, day, change_day=change_day)
                start = 1 if window == "Entire mission" else max(1, day - (14 if "14" in window else 7) + 1)
                end = 30 if window == "Entire mission" else day
                fig.update_xaxes(range=[start - .5, end + .5], dtick=5 if end - start > 14 else 1)
                st.plotly_chart(fig, width="stretch", key=key, theme=None,
                                config={"displaylogo": False, "scrollZoom": False})
        st.caption(f"Day {start}–{end} · automatically scaled y-axis")
        if change_day is not None:
            st.caption("Day 16 marks the start of the artificial change.")
        with st.expander("Chart legend"):
            st.caption("Circle: NORMAL · Triangle: WARNING · Diamond: CRITICAL · "
                       "open square: status change. Dashed: baseline · "
                       "dotted: assessment day.")
    with briefing_column:
        st.subheader("Mission Health Briefing")
        st.write(f'**Next review step:** {briefing["next_step"]}')
        # Prioritization affects presentation only; classification and explanations are preserved.
        ranked = summary.assign(priority=summary["Status"].map({"CRITICAL": 0, "WARNING": 1, "NORMAL": 2}))
        ranked = ranked.sort_values(["priority", "Magnitude (%)"], ascending=[True, False])
        shown = ranked if status == "NORMAL" else ranked[ranked["Status"] != "NORMAL"]
        for position, (_, row) in enumerate(shown.iterrows()):
            key = next(k for k, (label, _, _) in METRICS.items() if label == row["Indicator"])
            explanation = next(e for e in briefing["explanations"] if e.startswith(f'**{row["Indicator"]} ·'))
            with st.expander(f'{row["Status"]} · {row["Indicator"]}', expanded=position == 0):
                st.markdown(explanation)
                st.caption(status_period(frame, key, day))
    st.caption("Demo rules are not medically validated · See Calculation details.")

    with st.expander("Calculation details"):
        st.latex(r"d = \frac{\mathrm{current\ value} - \mathrm{Baseline}}{\mathrm{Baseline}} \cdot 100")
        st.write("Classification uses the absolute deviation: below 10% NORMAL, "
                 "10% to below 25% WARNING, 25% or above CRITICAL. Increases and "
                 "decreases are treated equally. The overall status is "
                 "the highest individual level. Baselines are demo assumptions.")
        for _, row in summary.iterrows():
            st.write(f'**{row["Indicator"]}:** ({row["Current"]:.2f} − {row["Baseline"]:.2f}) '
                     f'/ {row["Baseline"]:.2f} × 100 = {row["Deviation (%)"]:+.2f} % → '
                     f'Magnitude {row["Magnitude (%)"]:.2f} % → **{row["Status"]}**')
        st.caption("Displayed values are rounded; classification uses unrounded deviations.")
        st.caption("The briefing period describes the current uninterrupted "
                   "demo status, not the onset of illness.")
    with st.expander("Demo data and provenance"):
        st.write("Reproducible synthetic daily values. In the anomalous scenario, "
                 "the artificial change starts on day 16. No external measurements.")
        st.dataframe(frame, hide_index=True, width="stretch")


if __name__ == "__main__":
    main()
