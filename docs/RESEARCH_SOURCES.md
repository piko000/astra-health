# NASA-Forschung und Datenherkunft

Recherchestand: **14.11.2026**. Diese lokal gespeicherte Informationsansicht
enthält Quellen und eigene Einordnungen, keine importierten Vitalmessungen.

Erneute Prüfung für das Mission Health Briefing am 14.11.2026: Die offizielle
Challenge-Seite lieferte weiterhin HTTP 502; auch der Abruf mit `?tab=resources`
war nicht zugänglich. HRP und NTRS 20220014774 waren erreichbar. Die vollständige
Resources-Liste bleibt daher ungeprüft. Das Briefing verwendet ausschließlich
Projektregeln und eigene vorsichtige Prüfschritte, keine NASA-Handlungsprotokolle.

## Ergebnis und Datenlücke

In der durchgeführten Recherche wurde **kein für die vorhandene Tagesauswertung
geeigneter, vollständig verifizierter und direkt nutzbarer Messdatensatz** gefunden.
Deshalb gibt es in M4 keinen NASA-Messdatenadapter. Das bedeutet ausdrücklich
nicht, dass solche Daten nicht existieren. Dynamische Portalseiten und ungeklärte
Dateiformate bzw. Nutzungsbedingungen begrenzen die Prüfung.

| Bestandteil | Herkunft | Verwendung |
| --- | --- | --- |
| Herzfrequenz, Schlaf, Aktivität | Lokal erzeugt in `data/demo.py`, Seed 2026 | Ausschließlich synthetische Diagramme und Demo-Status |
| Baselines 60 bpm, 8 h, 60 min/Tag; Grenzen 10 % und 25 % | Projektannahmen | Nicht medizinisch validierte Demo-Regeln |
| NASA-Forschungsinformationen | Offizielle Seiten und NTRS-Bericht unten | Belegte Hintergrundinformationen, keine Kalibrierung |
| Echte individuelle Forschungs- oder Missionsmessdaten | Keine übernommen | Keine echte Vitaldatenintegration |

## Wissenschaftlicher Bezug

**Forschungskontext:** Das [NASA Human Research Program (HRP)](https://www.nasa.gov/hrp/)
untersucht Gesundheit und Leistungsfähigkeit mit Forschung am Boden, in
Analogumgebungen und im Weltraum. Das begründet den Themenbezug von ASTRA Health,
validiert jedoch weder unsere Kennzahlenkombination noch unsere Warnschwellen.

**Schlaf und Messlücken:** Flynn-Evans, Glaros und Jansen vergleichen in
[Comparison Between Continuous and Intermittent Actigraphy Outcomes During
Long-Duration Missions, NTRS 20220014774](https://ntrs.nasa.gov/citations/20220014774)
kontinuierliche mit intermittierenden Actigraphie-Messungen bei 19 Crewmitgliedern
(9 kontinuierlich, 10 jeweils zwei Wochen alle zwei Monate; Erhebung 2019–2022).
Der Konferenzbeitrag berichtet Unterschiede der Schlafkennzahlen und fehlende
Messungen bei Missionsereignissen. Er belegt die Bedeutung des Erhebungsplans,
keine individuelle Diagnose oder Kausalität. **Unsere Ableitung:** Ein späterer
Adapter muss Messlücken und Erhebungsintervalle sichtbar erhalten. Aus
Gruppenstatistiken werden keine individuellen Tageskurven rekonstruiert.

## Geprüfte offizielle Ressourcen

- [Challenge: Create Health Monitoring Software for Astronauts on Space Missions](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/):
  Titel und Aufgabenübersicht waren im Suchindex der offiziellen Seite sichtbar.
  Direkte Abrufe lieferten wiederholt HTTP 502; der Resources-Reiter konnte
  nicht unabhängig vollständig geprüft werden. Daher keine Behauptung über
  eine vollständige Liste empfohlener Challenge-Datensätze.
- [HRP](https://www.nasa.gov/hrp/): lesbare Programmübersicht, kein Vitaldatenfeed.
- [OSDR](https://osdr.nasa.gov/): leitete auf
  [BPS Data](https://science.nasa.gov/biological-physical/data/) weiter.
  Die verlinkte Studiensuche lieferte im Textwerkzeug keine lesbaren Inhalte.
  Laut [OSDR FAQ](https://science.nasa.gov/reference/osdr-faq/) ist der Großteil
  der Daten ohne Authentifizierung zugänglich; das ersetzt keine Prüfung des
  einzelnen Datensatzes und seiner Nutzungsbedingungen.
- [NASA Life Sciences Portal (NLSP)](https://www.nasa.gov/hrp/nlsp/):
  lesbare Übersicht mit Links zu LSDA, Antragswegen und ausdrücklich als offen
  bezeichneten UTMB-Bettruhe-Analogstudien. Die verlinkten Detailseiten zu
  Campaign 1 und 3 lieferten im Recherchewerkzeug keine lesbaren Dateilisten.
  Öffentlich sichtbare Katalogmetadaten sind nicht mit heruntergeladenen
  Messdaten gleichzusetzen.

## Potenzielle Datensätze und Entscheidung

Die folgenden Einträge sind **Kandidaten**, keine integrierten Datenquellen.
„Nicht verifiziert“ bedeutet eine offene Prüfung, nicht ein festgestelltes Verbot.

### 1. UTMB Bedrest Campaign 1 Physical Fitness Evaluation – Cycle Ergometry

- Offizieller [NLSP-Eintrag](https://nlsp.nasa.gov/search/data/details/07f12dd0-6725-582c-a4d2-618ed8b8c452?dataType=EXPERIMENTS).
- Inhalt: Im Suchindex des früheren NLSP-Record-Viewers sind verarbeitete
  Fitnessdaten mit Bezeichnungen wie HR, VO2, Workload sowie Pre-/Post-Messung
  gelistet. Einheiten, Spaltenschema und Auswertungsprotokoll wurden nicht verifiziert.
- Population: menschliche Teilnehmende einer Bettruhe-Analogkampagne auf der Erde;
  keine Weltraummission. Demografie und vollständige Stichprobengröße ungeprüft.
- Format/Zugang: HTML-Metadaten auffindbar; aktuelle Detailseite ohne lesbaren
  Text im Werkzeug. Kein Rohdatenformat und kein Dateidownload verifiziert.
- Nutzung: Kampagne in der offiziellen Open-Access-Übersicht genannt;
  dateispezifische Lizenz, Weiterverteilung und Zitierpflicht ungeklärt.
- Eignung: interessanter Kandidat für eine spätere separate Forschungsansicht.
  Belastungs-Herzfrequenz darf nicht als tägliche Ruheherzfrequenz eingesetzt werden.

### 2. BEDREST IRATS POWER CYCLE SUMMARY DATA

- Offizieller [NLSP-Datensatzeintrag](https://nlsp.nasa.gov/search/data/details/0e311656-88ad-5871-9749-2922e6e0ff7a?dataType=DATASETS).
- Inhalt: Suchindex nennt UTMB Campaign 11 iRATS14 und „Peak heart rate“.
  Weitere Messgrößen, Einheiten und Verarbeitung nicht verifiziert.
- Population: Bettruhe-Analogstudie; Anzahl und Demografie nicht verifiziert.
- Format/Zugang: Metadatentitel auffindbar; direkte Seite ohne lesbaren Inhalt.
  Kein Dateiformat oder Rohdatendownload bestätigt.
- Nutzung: datensatzspezifische Bedingungen nicht verifiziert.
- Eignung: Spitzen-Herzfrequenz ist keine Ruheherzfrequenz. Keine Übernahme in
  die bestehende Auswertung; zunächst Protokoll und Datenwörterbuch prüfen.

### 3. OSD-435: Effects of low-dose oxygen ions and protons on cardiac function and structure in male C57BL/6J mice (echocardiogram/ultrasonography)

- Offizieller Nachweis in der [OSDR-Payload-Liste High Dose Irradiation](https://osdr.nasa.gov/bio/repo/data/payloads/High_Dose_Irradiation).
- Inhalt: Untersuchung der Herzfunktion und -struktur nach Bestrahlung mittels
  Echokardiographie/Ultraschall; konkrete Spalten und Einheiten ungeprüft.
- Population: männliche C57BL/6J-Mäuse, keine Astronauten.
- Format/Zugang: Titel im Index der offiziellen Liste verifiziert; dynamische
  Seite ohne lesbaren Text. Dateiformat und einzelne Downloads nicht geprüft.
- Nutzung: keine datensatzspezifische Weiterverteilungslizenz verifiziert.
- Eignung: für menschliche Vitalwerte fachlich ungeeignet. Auch ein verfügbarer
  Download rechtfertigt keine Übertragung auf menschliche Demo-Baselines.

### 4. Schlafdaten hinter NTRS 20220014774

- Titel und [offizielle URL](https://ntrs.nasa.gov/citations/20220014774) wie oben.
- Messgrößen: Schlafdauer, Wachzeit nach Schlafbeginn (WASO), Schlafeffizienz;
  Population und Erhebungsplan siehe wissenschaftlicher Bezug.
- Format/Zugang: öffentlicher HTML-Abstract und verlinkter PDF-Konferenzbeitrag.
  Kein individueller Zeitreihendownload auf diesem Eintrag nachgewiesen.
- Nutzung: NTRS kennzeichnet das Dokument als „Public Use Permitted“; das ist
  keine Freigabe der zugrunde liegenden personenbezogenen Messdaten.
- Eignung: als Forschungsbeleg verwendet, nicht als Datenlieferant.

## Zugang und Nutzungsbedingungen

Die [NASA-Leitlinien für retrospektive Datenanfragen](https://www.nasa.gov/wp-content/uploads/2015/05/hrp_retrospective_data_request_study_information_package_guidelines_final.pdf)
beschreiben sowohl direkt verfügbare nicht zuordenbare Daten als auch
Antrags- und Freigabeprozesse. Personenbeziehbare Daten erfordern Zustimmung;
auch Variablenkombinationen können Identifizierbarkeit erzeugen. Das ältere
Dokument ist eine Orientierung, keine aktuelle pauschale Lizenz. Aktuelle Details
sind über die [NLSP Data Request Guidelines](https://nlsp.nasa.gov/data-request-guidelines)
zu prüfen; diese Seite war im Werkzeug nicht lesbar. Es wurde keine Anfrage
gestellt und kein Datensatz heruntergeladen oder weiterverteilt.

## Annahmen, Grenzen und offene Fragen

- Wissenschaftlich belegt ist der Forschungskontext, **nicht die medizinische
  Wirksamkeit von ASTRA Health**. Keine NASA-Zertifizierung oder Diagnosesicherheit.
- Die synthetischen 30 Tage bilden weder eine echte Mission noch eine validierte
  physiologische Simulation ab. „Aktivität“ bedeutet hier frei gewählte aktive
  Minuten; das ist nicht automatisch mit Actigraphie-Zählwerten vergleichbar.
- Die unveränderte Betragsregel bewertet Zu- und Abnahmen gleich. Baselines,
  10-/25-Prozent-Grenzen und höchster Einzelstatus wurden nicht aus NASA-Forschung
  abgeleitet. Sensitivität, Spezifität und klinische Aussagekraft sind unbekannt.
- Vor einer Integration: echte Datei, Version/Prüfsumme, Lizenz, Datenwörterbuch,
  Ruhe-/Belastungsprotokoll, Einheiten, Zeitbezug und Fehlwertcodes verifizieren.
  Forschungsteilnehmende und Messzeitpunkte dürfen nicht zu einer fiktiven
  durchgehenden Astronautenmission zusammengesetzt werden.
- Der bestehende Adaptervertrag erwartet 30 vollständige Tage und drei Kennzahlen.
  Reale Daten dürfen nicht durch erfundene Ergänzungen passend gemacht werden.
  Gegebenenfalls ist später eine eigenständige Forschungsdatenauswertung nötig.
- Offen: Challenge-Resources-Reiter im Browser prüfen; UTMB-Readmes und Dateien
  manuell prüfen; Nutzungsrechte klären; Messgrößen fachlich begutachten lassen.

## Empfehlung für die Abgabe

ASTRA Health als **Prototyp mit synthetischen Vitaldaten und belegtem
NASA-Forschungskontext** präsentieren. Den Wechsel zwischen Demo und dieser
Quellenansicht zeigen, die mathematische Regel erklären und die Datenlücke
offen benennen. Keine echte NASA-Telemetrie oder klinische Validierung behaupten.
Eine spätere Dateneinbindung erst nach Prüfung der oben genannten offenen Punkte.
