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
  Beispielcode bleibt erhalten und schreibt beim Import ins Terminal.
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

## M4: Wissenschaftliche Grundlage

In der Seitenleiste unter **Ansicht → NASA-Forschung** stehen die recherchierten
Quellen, Kandidaten und Einschränkungen. Die Ansicht liest lokal
[`docs/RESEARCH_SOURCES.md`](docs/RESEARCH_SOURCES.md); sie benötigt keine
Netzwerkverbindung. Externe Links benötigen zum Öffnen Internet. Bei einer
fehlenden oder unlesbaren Dokumentation zeigt sie einen Hinweis; die Demo bleibt
nutzbar. Neue Abhängigkeiten oder Modelle wurden nicht ergänzt.

Das [NASA Human Research Program](https://www.nasa.gov/hrp/) liefert den
Forschungskontext. Der [NASA-Konferenzbeitrag NTRS 20220014774](https://ntrs.nasa.gov/citations/20220014774)
belegt die Relevanz von Erhebungsintervallen bei Schlafmessungen. Diese Quellen
validieren weder unsere Warnregeln noch unsere synthetischen Missionsverläufe.

### Datensatzherkunft und synthetische Kennzeichnung

Es wurden **keine echten Messdaten importiert**. Alle drei Vitalwertkurven stammen
unverändert aus `SyntheticDataSource` und sind als synthetisch gekennzeichnet.
Die NASA-Integration besteht aus einer belegten Informationsansicht.
Recherchiert wurden HRP, OSDR, NLSP und die offizielle Challenge-Seite. Das Dossier
führt konkrete UTMB-, OSDR- und Schlafdatenkandidaten einschließlich Population,
Zugangsstand, ungeklärten Formaten/Nutzungsrechten und Eignungsentscheidung auf.

### Medizinische und technische Grenzen

Kein direkt nutzbarer, vollständig verifizierter Datensatz für die vorhandene
Tagesauswertung wurde gefunden. Einige Portalansichten waren im Recherchewerkzeug
nicht lesbar; die Challenge-Seite lieferte beim direkten Abruf HTTP 502. Das ist
kein Nachweis, dass passende NASA-Daten grundsätzlich nicht verfügbar sind.
Spitzen- oder Belastungsherzfrequenz sowie Tierdaten dürfen nicht als menschliche
Ruheherzfrequenz verwendet werden. Forschungsergebnisse sind keine individuellen
Missionskurven. Demo-Baselines und 10-/25-Prozent-Schwellen bleiben unverändert
und medizinisch unvalidiert; es gibt keine Diagnose- oder NASA-Zertifizierung.

Für die Hackathon-Abgabe empfehlen wir die Bezeichnung „Prototyp mit synthetischen
Vitaldaten und belegtem NASA-Forschungskontext“. Eine echte Datenintegration bleibt
ein nächster Schritt nach Quellen-, Rechte- und Protokollprüfung.

### M4-Testresultat (14.11.2026)

`python -m pytest -q -p no:cacheprovider`: **23 passed in 3.74s**.
Alle bisherigen 20 Tests sind erhalten; drei neue Testfälle prüfen die getrennte
Forschungsansicht, die Rückkehr zur Demo sowie fehlende/unlesbare Dokumentation.
Ein erster Lauf ergab 22 bestandene Tests und einen Vergleichsfehler wegen des
von Streamlit entfernten abschließenden Zeilenumbruchs; der neue Test normalisiert
nun äußere Leerzeichen. Der abschließende vollständige Lauf ist erfolgreich.
Prüfsummen vor/nach M4 bestätigen unveränderte Analyse-, Demo- und bisherige
Testdateien. Externe Erreichbarkeit wird nicht durch automatisierte Tests geprüft;
ein visueller Browsertest wurde nicht durchgeführt.

## M4: Kompakte Demo und Mission Health Briefing

Oben stehen die Gesamtstatus-/Warnkarte und drei Vitalwert-Karten. Darunter zeigt
der erste Tab die Ruheherzfrequenz als großes Hauptdiagramm; Schlaf und Aktivität
sind in benachbarten Tabs erreichbar. Das Briefing steht daneben. Formel und
Datentabelle sind einklappbar. Auf schmalen Bildschirmen kann Scrollen nötig sein.

`analysis/briefing.py` erklärt die von der bestehenden Analyse gelieferten
Statuswerte mit festen Textvorlagen: betroffene Indikatoren, synthetische Werte,
Baseline, vorzeichenbehaftete Abweichung, Betrag, Regel und nächster Prüfschritt.
Bei NORMAL werden alle drei Indikatoren erklärt; sonst nur auffällige. Der
Gesamtstatus bleibt die höchste Einzelstufe. Keine neue klinische Regel.

Im auffälligen Szenario markiert jedes Diagramm **Tag 16** als Beginn der
programmierten Veränderung. Dieser Zeitpunkt ist weder eine erkannte Diagnose
noch zwingend der erste Warnungstag. Der normale Verlauf erhält keine solche
Markierung. Beide Szenarien und der Seed bleiben unverändert.

Unter **NASA-Forschung → Space Health Research** steht eine kurze belegte
Einordnung; das vollständige Quellen-Dossier ist einklappbar. Synthetische Daten,
Forschungsbelege und Demo-Regeln bleiben getrennt beschriftet. Der erneute Abruf
der offiziellen Challenge-/Resources-Seite scheiterte; die vollständige Prüfung
dieses Reiters bleibt offen. Die Informationsansicht funktioniert lokal offline.

### KI-Transparenz

Codex unterstützte Implementierung, Recherche, Dokumentation und Tests. Die
Anwendung selbst verwendet kein KI-Modell und keinen kostenpflichtigen Dienst.
Details und Grenzen stehen in [docs/AI_USAGE.md](docs/AI_USAGE.md).

### Kurzer Demo-Ablauf

1. Normaler Verlauf, Tag 30: NORMAL und die drei Kennzahlen erklären.
2. Auffälliger Verlauf, Tag 16: künstlichen Änderungsbeginn zeigen.
3. Tag 22: WARNING-Karte, betroffene Kennzahlen und Briefing erläutern.
4. Tag 30: CRITICAL als Demo-Stufe zeigen, keine Diagnose behaupten.
5. Space Health Research öffnen und Quellen sowie KI-Nutzung offenlegen.

### Prüfung der Dashboard-Überarbeitung (14.11.2026)

- Ausgangsstand: 23 Tests bestanden.
- Szenarien-/Briefingtests: `python -m pytest tests/test_briefing.py -q -p no:cacheprovider`
  → **14 passed in 4.01s**.
- Anschließend vollständige Testsuite: `python -m pytest -q -p no:cacheprovider`
  → **37 passed in 5.87s**. Alle bisherigen Tests sind unverändert erhalten.
- Geprüft: Warnkarten, angezeigte Erklärungen, beide Szenarien, Tage 15/16/22/30,
  positive und negative Grenzfälle, Diagramm-Tabs und optionale Tag-16-Markierung.
- SHA-256-Vergleich bestätigt unveränderte `analysis/health_monitor.py` und
  `data/demo.py`. Keine neuen Abhängigkeiten.
- AppTest prüft die Streamlit-Ausführung, nicht Bildschirmgeometrie, Farben oder
  Plotly-Mausinteraktionen. Eine visuelle Browserprüfung war hier nicht verfügbar;
  insbesondere die Darstellung auf dem Präsentationsbildschirm ist noch manuell
  zu prüfen. Die kompakte Anordnung ist implementiert, ihre genaue Höhe hängt von
  Bildschirm, Zoom und Fensterbreite ab.
