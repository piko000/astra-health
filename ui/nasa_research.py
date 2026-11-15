"""Research-only visualization: measured serum biomarkers, no demo alerts."""
import plotly.express as px
import streamlit as st

from data.nasa_loader import BIOMARKERS, DOI, STUDY_URL, NASADataError, load_cmp
from ui.theme import COLORS


def research_chart(frame, biomarker):
    column, unit, _ = BIOMARKERS[biomarker]
    order = frame.sort_values("Timepoint order")["Timepoint"].drop_duplicates().tolist()
    measured = frame.loc[frame[column].notna()]
    fig = px.scatter(measured, x="Timepoint", y=column, color="Participant", symbol="Participant",
                     category_orders={"Timepoint": order},
                     labels={column: f"{biomarker} ({unit})"},
                     hover_data=["Sample Name", "Time description", "Phase"],
                     color_discrete_sequence=["#38BDF8", "#FBBF24", "#34D399", "#FB7185"])
    fig.update_traces(marker_size=11)
    fig.update_layout(height=420, margin=dict(l=80, r=24, t=32, b=80),
                      paper_bgcolor=COLORS["background"], plot_bgcolor=COLORS["background"],
                      font=dict(color=COLORS["text"], size=14),
                      legend=dict(orientation="h", y=1.12))
    fig.update_xaxes(type="category", categoryorder="array", categoryarray=order,
                     title="Sampling occasion (categorical; not to scale)", automargin=True)
    fig.update_yaxes(automargin=True, title_standoff=16, gridcolor=COLORS["surface"])
    return fig


def show_nasa_measurements():
    st.info("NASA Research Data · OSD-575 · Measured serum biomarkers from four Inspiration4 participants.")
    st.caption(f"[Original NASA study]({STUDY_URL}) · [DOI: {DOI}](https://doi.org/{DOI}) · "
               "Version 3 · CC0-1.0 · Locally stored research data")
    try:
        frame = load_cmp()
    except NASADataError as error:
        st.warning(str(error))
        st.caption("Restore the local files with: python -m data.download_nasa. "
                   "Synthetic Mission Telemetry remains available in Demo dashboard.")
        return
    biomarker = st.selectbox("Research biomarker", list(BIOMARKERS))
    column, unit, description = BIOMARKERS[biomarker]
    st.caption(f"{description} Original unit: {unit}. No unit conversion.")
    count = int(frame[column].notna().sum())
    missing = int(frame[column].isna().sum())
    st.caption(f"{count} measured values · {missing} missing values · "
               f'{frame["Participant"].nunique()} participants · Missing values are not replaced or plotted.')
    if count:
        st.plotly_chart(research_chart(frame, biomarker), width="stretch", theme=None,
                        key="nasa_cmp", config={"displaylogo": False})
    else:
        st.warning("No measured values available for this biomarker.")
    st.caption("L = days before launch; R = days after return. The sample metadata includes R+194. "
               "Points show separate sampling occasions, not daily telemetry. No interpolation.")
    st.caption("Small observational sample; no causal or diagnostic conclusions. "
               "Demo Alert Rules and synthetic mission baselines are not applied to research data.")
    with st.expander("Research measurements and missing values"):
        table = frame[["Participant", "Timepoint", "Time description", "Phase", column]].copy()
        table = table.rename(columns={column: f"{biomarker} ({unit})"})
        table["Availability"] = frame[column].notna().map({True: "Measured", False: "Missing in NASA file"})
        st.dataframe(table, hide_index=True, width="stretch")
