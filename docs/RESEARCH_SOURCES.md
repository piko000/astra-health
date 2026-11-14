# NASA research and data provenance

Research checked on **14 November 2026**. This locally stored view contains
sources and project interpretations, not imported vital-sign measurements.

The repeat check for the Mission Health Briefing still returned HTTP 502 for the
official challenge page; `?tab=resources` was also inaccessible. HRP and NTRS
20220014774 were accessible. The complete Resources list remains unverified.
The briefing uses project rules and cautious review steps, not NASA protocols.

## Findings and data gap

This research did **not identify a fully verified, directly usable measurement
dataset suitable for the existing daily assessment**. M4 therefore has no NASA
measurement adapter. This does not imply that suitable datasets do not exist.
Dynamic pages, unverified file formats and unclear usage terms limited the review.

| Component | Provenance | Use |
| --- | --- | --- |
| Heart rate, sleep, activity | Generated in `data/demo.py`, seed 2026 | Synthetic charts and demo statuses |
| Baselines: 60 bpm, 8 h, 60 min/day; thresholds: 10% and 25% | Project assumptions | Demo rules, not medically validated |
| NASA research information | Official pages and NTRS report below | Sourced context, not calibration |
| Individual research or mission measurements | None imported | No real vital-sign data integration |

## Scientific context

The [NASA Human Research Program (HRP)](https://www.nasa.gov/hrp/) studies health
and performance through ground, analog and space research. This supports the
project's subject matter, but does not validate its indicators or alert thresholds.

Flynn-Evans, Glaros and Jansen's [Comparison Between Continuous and Intermittent
Actigraphy Outcomes During Long-Duration Missions, NTRS 20220014774](https://ntrs.nasa.gov/citations/20220014774)
compares 19 crew members: 9 continuously monitored and 10 monitored for two weeks
every two months, with observations collected in 2019–2022. The conference paper
reports differences in sleep metrics and missing observations around mission
events. It supports the importance of collection schedules, not individual
diagnosis or causation. **Our interpretation:** a future adapter must preserve
measurement gaps and sampling intervals. Group statistics must not be reconstructed
into individual daily trajectories.

## Official resources checked

- [Challenge: Create Health Monitoring Software for Astronauts on Space Missions](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/):
  title and task overview appeared in the official page's search index. Direct
  requests repeatedly returned HTTP 502. The Resources tab could not be fully
  checked; no complete list of recommended datasets is claimed.
- [HRP](https://www.nasa.gov/hrp/): readable program overview, not a vital-sign feed.
- [OSDR](https://osdr.nasa.gov/) redirected to
  [BPS Data](https://science.nasa.gov/biological-physical/data/). The linked study
  search produced no readable text in the research tool. The
  [OSDR FAQ](https://science.nasa.gov/reference/osdr-faq/) states that most data
  can be accessed without authentication. Individual datasets and terms still
  require verification.
- [NASA Life Sciences Portal (NLSP)](https://www.nasa.gov/hrp/nlsp/): readable
  overview linking LSDA, request procedures and explicitly open UTMB bed-rest
  analog studies. Campaign 1 and 3 detail pages did not expose readable file
  lists in the tool. Public catalog metadata is not downloaded measurement data.

## Candidate datasets and decisions

These are **candidates**, not integrated sources. “Unverified” means further
investigation is needed, not that use is prohibited.

### 1. UTMB Bedrest Campaign 1 Physical Fitness Evaluation – Cycle Ergometry

- Official [NLSP record](https://nlsp.nasa.gov/search/data/details/07f12dd0-6725-582c-a4d2-618ed8b8c452?dataType=EXPERIMENTS).
- Contents: the former record viewer's search index lists processed fitness data
  labeled HR, VO2, workload and pre-/post-measurement. Units, schema and assessment
  protocol were not verified.
- Population: human participants in an Earth-based bed-rest analog campaign,
  not a space mission. Demographics and complete sample size unverified.
- Format/access: HTML metadata discoverable; current detail page unreadable in
  the tool. No raw format or file download verified.
- Terms: campaign listed in the official open-access overview; file-specific
  license, redistribution rights and citation requirements unresolved.
- Suitability: possible future research view. Exercise heart rate must not be
  substituted for daily resting heart rate.

### 2. BEDREST IRATS POWER CYCLE SUMMARY DATA

- Official [NLSP dataset record](https://nlsp.nasa.gov/search/data/details/0e311656-88ad-5871-9749-2922e6e0ff7a?dataType=DATASETS).
- Contents: index identifies UTMB Campaign 11 iRATS14 and peak heart rate.
  Other variables, units and processing unverified.
- Population: bed-rest analog participants; sample size and demographics unverified.
- Format/access: metadata title discoverable; direct page unreadable. No file
  format or raw-data download confirmed.
- Terms: dataset-specific conditions unverified.
- Suitability: peak heart rate is not resting heart rate. Check the protocol and
  data dictionary before considering integration.

### 3. OSD-435: Effects of low-dose oxygen ions and protons on cardiac function and structure in male C57BL/6J mice (echocardiogram/ultrasonography)

- Official listing: [OSDR High Dose Irradiation payload](https://osdr.nasa.gov/bio/repo/data/payloads/High_Dose_Irradiation).
- Contents: cardiac function and structure after irradiation using ultrasound;
  specific columns and units unverified.
- Population: male C57BL/6J mice, not astronauts.
- Format/access: title verified in the official listing's index; dynamic page
  unreadable. File formats and individual downloads not checked.
- Terms: no dataset-specific redistribution license verified.
- Suitability: unsuitable for human vital-sign assessment. Availability would
  not justify applying human demo baselines to animal measurements.

### 4. Sleep data underlying NTRS 20220014774

- Title and [official URL](https://ntrs.nasa.gov/citations/20220014774) as above.
- Variables: sleep duration, wake after sleep onset (WASO), sleep efficiency.
  See scientific context for population and collection schedule.
- Format/access: public HTML abstract and linked PDF conference paper. No
  individual time-series download identified on this record.
- Terms: NTRS labels the document “Public Use Permitted”; this does not release
  the underlying personal measurements.
- Suitability: used as research evidence, not as a measurement provider.

## Access and usage terms

[NASA's retrospective data request guidelines](https://www.nasa.gov/wp-content/uploads/2015/05/hrp_retrospective_data_request_study_information_package_guidelines_final.pdf)
describe directly available non-attributable data and request/approval processes.
Attributable data requires consent; combinations of variables may also identify
individuals. This older document provides context, not a current blanket license.
Current details should be checked through the
[NLSP Data Request Guidelines](https://nlsp.nasa.gov/data-request-guidelines),
which were unreadable in the tool. No request was submitted and no dataset was
downloaded or redistributed.

## Assumptions, limitations and open questions

- Evidence supports the research context, **not medical effectiveness of ASTRA
  Health**. No NASA certification or diagnostic certainty is claimed.
- The 30 synthetic days are neither a real mission nor a validated physiological
  simulation. Activity means generated active minutes, not necessarily comparable
  to actigraphy counts.
- Absolute deviation treats increases and decreases equally. Baselines, 10%/25%
  thresholds and the highest-individual-status summary were not derived from NASA
  research. Sensitivity, specificity and clinical utility are unknown.
- Before integration, verify the file, version/checksum, license, dictionary,
  resting/exercise protocol, units, time reference and missing-value codes.
  Do not combine participants or dates into a fictional continuous mission.
- The adapter expects 30 complete days and three indicators. Never invent values
  to make real data fit; a separate research-data assessment may be necessary.
- Open work: inspect the challenge Resources tab in a browser, check UTMB readmes
  and files, clarify rights and obtain expert review of variables.

## Submission recommendation

Present ASTRA Health as a **prototype with synthetic vital signs and sourced NASA
research context**. Demonstrate the dashboard and sources view, explain the rule
and disclose the data gap. Do not claim NASA telemetry or clinical validation.
Integrate measurements only after resolving the checks above.
