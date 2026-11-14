"""Lokale ASTRA-Health-Demo: python -m streamlit run app.py."""

from pathlib import Path

import streamlit as st

from analysis.dashboard import summarize_day, vital_chart
from analysis.briefing import mission_briefing
from data.demo import METRICS, SCENARIOS, SyntheticDataSource, VitalDataSource


RESEARCH_PATH = Path(__file__).resolve().parent / "docs" / "RESEARCH_SOURCES.md"


def show_research():
    """Lokale, belegte Informationsansicht ohne Netzwerkzugriffe oder Messdatenimport."""
    st.info("Forschungsinformationen · Keine echte Vitaldatenintegration. "
            "Alle Vitalwerte im Dashboard bleiben synthetisch.")
    st.subheader("Space Health Research")
    st.caption("Forschungsbeleg: Das [NASA HRP](https://www.nasa.gov/hrp/) untersucht "
               "Gesundheit und Leistungsfähigkeit in Weltraum- und Analogumgebungen.")
    st.caption("Forschungsbeleg: [NTRS 20220014774](https://ntrs.nasa.gov/citations/20220014774) "
               "vergleicht kontinuierliche und intermittierende Schlafmessungen. "
               "Erhebungsintervalle und Messlücken sind für die Interpretation relevant.")
    st.caption("Projektannahmen: Baselines und 10-/25-Prozent-Regeln sind nicht durch diese "
               "Quellen validiert. Challenge-Resources-Prüfung am 14.11.2026: "
               "direkter Abruf fehlgeschlagen; Details im Dossier.")
    try:
        content = RESEARCH_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        st.error("Die Forschungsdokumentation konnte nicht geladen werden. "
                 "Bitte docs/RESEARCH_SOURCES.md aus dem Projekt wiederherstellen. "
                 "Das Demo-Dashboard bleibt verfügbar.")
        return
    with st.expander("Quellen-Dossier, Datenkandidaten und Grenzen"):
        st.markdown(content)


def main():
    st.set_page_config(page_title="ASTRA Health", page_icon="🚀", layout="wide")
    st.title("ASTRA Health")
    st.caption("NASA Space Apps Hackathon 2026 · lokaler Projektprototyp")
    view = st.sidebar.radio("Ansicht", ("Demo-Dashboard", "NASA-Forschung"))
    st.sidebar.caption("NASA-Forschung: Space Health Research · "
                       "Mit Codex entwickelt; das Briefing nutzt feste Textregeln, kein KI-Modell.")
    if view == "NASA-Forschung":
        show_research()
        return
    st.info("SYNTHETISCHE DEMO-DATEN · Fiktiver Astronaut Alex Vega · "
            "Keine echten NASA-Messdaten. Keine medizinische Diagnose.")
    st.sidebar.header("Mission erkunden")
    scenario = st.sidebar.selectbox("Missionsverlauf", SCENARIOS)
    day = st.sidebar.slider("Missionstag für Auswertung", 1, 30, 30)
    st.sidebar.caption("30 synthetische Missionstage · Seed 2026 · "
                       "Aktivität = aktive Minuten pro Tag")

    source: VitalDataSource = SyntheticDataSource()
    frame = source.load(scenario)
    summary = summarize_day(frame, day)
    briefing = mission_briefing(summary)
    status = briefing["status"]
    display = {"NORMAL": st.success, "WARNING": st.warning, "CRITICAL": st.error}
    affected = ", ".join(briefing["affected"]) or "Keine Demo-Grenze erreicht"
    display[status](f"**Demo-Gesamtstatus: {status} · Tag {day}**\n\n{affected}. "
                    "Höchste Demo-Stufe; keine Diagnose.",
                    icon={"NORMAL": "✅", "WARNING": "⚠️", "CRITICAL": "🚨"}[status])

    for column, (_, row) in zip(st.columns(3), summary.iterrows()):
        with column, st.container(border=True):
            st.metric(row["Vitalwert"], f'{row["Aktuell"]:.2f} {row["Einheit"]}',
                      f'{row["Abweichung (%)"]:+.2f} % zur Demo-Baseline', delta_color="off")
            st.caption(f'Baseline: {row["Baseline"]:g} {row["Einheit"]} · {row["Status"]}')

    chart_column, briefing_column = st.columns([2, 1])
    with chart_column:
        st.subheader("Synthetischer Missionsverlauf")
        tabs = st.tabs([label for label, _, _ in METRICS.values()])
        change_day = 16 if scenario == SCENARIOS[1] else None
        for tab, key in zip(tabs, METRICS):
            with tab:
                st.plotly_chart(vital_chart(frame, key, day, change_day=change_day),
                                width="stretch", key=key)
        st.caption("Alle 30 Tage · gestrichelt: Demo-Baseline · gepunktet: ausgewählter Tag. "
                   "Details per Mauszeiger, Zoom per Auswahl.")
        if change_day is not None:
            st.caption("Tag 16 markiert den programmierten Beginn der künstlichen Veränderung, "
                       "nicht den Zeitpunkt einer Diagnose oder der ersten Warnung.")
    with briefing_column:
        st.subheader("Mission Health Briefing")
        st.caption("Regelbasiert · synthetische Werte · keine NASA-Handlungsanweisung")
        for explanation in briefing["explanations"]:
            st.markdown(explanation)
        st.write(f'**Nächster Prüfschritt:** {briefing["next_step"]}')
    st.caption("Nicht medizinisch validierte Demo-Regeln: Betrag der Abweichung < 10 % = NORMAL; "
               "10 % bis < 25 % = WARNING; ab 25 % = CRITICAL. "
               "Die Regel bewertet Zunahmen und Abnahmen gleich.")

    with st.expander("Mathematische Begründung"):
        st.latex(r"d = \frac{\mathrm{aktueller\ Wert} - \mathrm{Baseline}}{\mathrm{Baseline}} \cdot 100")
        st.write("calculate_deviation() liefert d mit Vorzeichen. "
                 "classify_health_status() erhält |d|, weil sie keine negativen Abweichungen akzeptiert. "
                 "Die Baselines sind feste Demo-Annahmen, keine medizinischen Normwerte.")
        for _, row in summary.iterrows():
            st.write(f'**{row["Vitalwert"]}:** ({row["Aktuell"]:.2f} − {row["Baseline"]:.2f}) '
                     f'/ {row["Baseline"]:.2f} × 100 = {row["Abweichung (%)"]:+.2f} % → '
                     f'Betrag {row["Betrag (%)"]:.2f} % → **{row["Status"]}**')
        st.caption("Anzeigewerte sind gerundet; die Klassifikation verwendet ungerundete Abweichungen.")
    with st.expander("Demo-Daten und Herkunft"):
        st.write("Alle Werte werden lokal in data/demo.py mit Seed 2026 erzeugt. "
                 "Im auffälligen Verlauf wird ab Tag 16 eine künstliche Veränderung ergänzt. "
                 "Es werden keine externen Messdaten, Bilder oder NASA-Schnittstellen verwendet.")
        st.dataframe(frame, hide_index=True, width="stretch")


if __name__ == "__main__":
    main()
