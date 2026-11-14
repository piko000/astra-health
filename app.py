"""Lokale ASTRA-Health-Demo: python -m streamlit run app.py."""

import streamlit as st

from analysis.dashboard import summarize_day, vital_chart
from data.demo import METRICS, SCENARIOS, SyntheticDataSource, VitalDataSource


def main():
    st.set_page_config(page_title="ASTRA Health", page_icon="🚀", layout="wide")
    st.title("ASTRA Health")
    st.caption("NASA Space Apps Hackathon 2026 · lokaler Projektprototyp")
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
    st.subheader(f"Tagesauswertung · Missionstag {day}")
    statuses = set(summary["Status"])
    status = "CRITICAL" if "CRITICAL" in statuses else "WARNING" if "WARNING" in statuses else "NORMAL"
    display = {"NORMAL": st.success, "WARNING": st.warning, "CRITICAL": st.error}
    display[status](f"Demo-Gesamtstatus: {status} · höchste Demo-Stufe der drei Vitalwerte")
    st.caption("Nicht medizinisch validierte Demo-Regeln: Betrag der Abweichung < 10 % = NORMAL; "
               "10 % bis < 25 % = WARNING; ab 25 % = CRITICAL. "
               "Die Regel bewertet Zunahmen und Abnahmen gleich.")

    for column, (_, row) in zip(st.columns(3), summary.iterrows()):
        with column:
            st.metric(row["Vitalwert"], f'{row["Aktuell"]:.2f} {row["Einheit"]}',
                      f'{row["Abweichung (%)"]:+.2f} % zur Demo-Baseline', delta_color="off")
            st.caption(f'Baseline: {row["Baseline"]:g} {row["Einheit"]} · {row["Status"]}')

    st.subheader("Verlauf der synthetischen Vitaldaten")
    st.caption("Gestrichelt: frei gewählte Demo-Baseline · gepunktet: ausgewählter Tag. "
               "Die Diagramme zeigen jeweils alle 30 Tage; Details per Mauszeiger, Zoom per Auswahl.")
    for key, (label, _, _) in METRICS.items():
        st.markdown(f"**{label}**")
        st.plotly_chart(vital_chart(frame, key, day), width="stretch", key=key)

    st.subheader("Mathematische Begründung")
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
