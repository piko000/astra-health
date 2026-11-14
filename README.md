# ASTRA Health

Lokaler Streamlit-Prototyp für das Projekt beim NASA Space Apps Hackathon 2026.
Alle Vitaldaten gehören zum **fiktiven Astronauten Alex Vega** und sind
**synthetisch**. Keine echten NASA-Messdaten, keine medizinische Diagnose.

## Start (Python 3.13, PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Anschließend `http://localhost:8501` öffnen. Eine bereits vorhandene `.venv`
kann weiterverwendet werden. Die Versionspins entsprechen der lokal getesteten
Umgebung; die Anwendung braucht nach Installation keinen Messdaten-Service.

In der Seitenleiste den Missionsverlauf und den Auswertungstag auswählen.
Die drei interaktiven Plotly-Diagramme zeigen alle 30 Missionstage; die
Tagesauswertung bezieht sich auf den ausgewählten Tag.

## Einfacher Aufbau

- `app.py`: Streamlit-Oberfläche, Auswahl, Kennzahlen und Erklärungen.
- `data/demo.py`: austauschbarer `VitalDataSource`-Vertrag und synthetischer
  Generator mit lokalem `Random(2026)`; identische Eingaben liefern identische Werte.
- `analysis/dashboard.py`: verbindet Daten mit den bestehenden Funktionen und
  erstellt Plotly-Diagramme. Keine neue fachliche Klassifikationslogik.
- `analysis/health_monitor.py`: bestehende Analyse unverändert. Auch der vorhandene
  Beispielcode bleibt erhalten und schreibt beim Import zwei Zeilen ins Terminal.
- `tests/`: bestehende Tests sowie neue Daten-, Diagramm- und Streamlit-AppTests.

Die frei gewählten Baselines sind 60 bpm Ruheherzfrequenz, 8 Stunden Schlaf und
60 aktive Minuten pro Tag. Der normale Verlauf streut jeweils um ±4 %.
Der auffällige Verlauf ergänzt ab Tag 16 eine lineare Veränderung, bis Tag 30
um +35 %, −30 % bzw. −40 % zusätzlich zur gleichen Zufallsstreuung.
Dies ist ein bewusst konstruiertes Demonstrationsmuster, kein physiologisches Modell.

`calculate_deviation(baseline, current)` berechnet
`(current - baseline) / baseline * 100`.
Die bestehende `classify_health_status(abs(deviation))` bewertet den Betrag:
unter 10 % NORMAL, von 10 % bis unter 25 % WARNING, ab 25 % CRITICAL.
Diese **nicht medizinisch validierten Demo-Regeln** behandeln beide Richtungen
gleich. Der Gesamtstatus zeigt die höchste Einzelstufe; er ist keine zusätzliche
medizinische Bewertung. Die UI rundet nur die Anzeige.

## Spätere Datenintegration und Ressourcenherkunft

Es ist keine NASA-Datenquelle angebunden oder vorausgesetzt. Ein späterer Adapter
kann `VitalDataSource.load()` implementieren und die Instanz in `app.py` ersetzen.
Er muss das dokumentierte Tabellenschema liefern. Vor einer echten Integration
sind eine tatsächlich verifizierte Quelle, Nutzungsrechte, Quellenangabe in der UI,
Einheiten, Zeitbezug, fehlende Werte und geeignete Baselines zu klären. Die aktuelle
synthetische Beschriftung und Szenarioauswahl müssen dann entsprechend angepasst
werden. Der Vertrag allein ist keine Validierung externer Daten.

Alle Demo-Messwerte entstehen im Projektcode. Keine externen Bilder, Schriftdateien,
Datensätze oder NASA-Assets werden eingebunden. Verwendete externe Software:

- [Python](https://www.python.org/): Laufzeit und Standardbibliothek (`random`).
- [Streamlit](https://streamlit.io/): lokale UI und AppTest.
- [Pandas](https://pandas.pydata.org/): Tabellen.
- [Plotly](https://plotly.com/python/): interaktive Diagramme.
- [pytest](https://docs.pytest.org/): Tests.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

Der Cache ist im Befehl deaktiviert, weil der vorhandene `.pytest_cache` in der
Arbeitsumgebung nicht beschreibbar ist. Das beeinflusst die Tests nicht.
AppTest prüft UI-Ausführung und Auswahlwechsel, aber kein tatsächliches
Browser-Rendering und keine Mausinteraktion mit Plotly.

Testergebnis am 14.11.2026 unter Python 3.13.16 mit den Versionen aus
`requirements.txt`: **20 passed in 4.81s** (12 bestehende und 8 neue Tests).
Die ursprünglichen Tests bestanden auch vor den Änderungen (12 passed);
dabei entstand lediglich eine Warnung wegen des nicht beschreibbaren pytest-Caches.
