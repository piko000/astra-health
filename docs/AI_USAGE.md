# AI tool usage disclosure

As of 14 November 2026. This statement describes documented project assistance;
it does not attest to unobserved work by other contributors.

- **OpenAI Codex:** assisted with the Streamlit interface, synthetic generator,
  integration with existing analysis, Plotly charts, research documentation,
  Mission Health Briefing and additional tests.
- **Core logic ownership:** the developer supplied the analysis functions.
  Dashboard work preserved their calculations and thresholds. Codex added
  presentation and explanations of their outputs.
- **Research:** web research tools were used to consult official NASA and
  challenge pages. Sources and access limitations appear in
  [RESEARCH_SOURCES.md](RESEARCH_SOURCES.md). Generated summaries are not primary
  sources and do not replace expert review.
- **Data:** the generator was created with Codex assistance. Values are generated
  deterministically with seed 2026, not obtained from NASA or a medically
  validated model.
- **Briefing:** fixed Python templates explain existing classifications. No
  language model, AI API or paid service runs in the application. Review steps
  are project demo text, not NASA protocols, diagnoses or treatment recommendations.
- **Other AI tools:** no other AI models or image generators were used in the
  documented steps. Team members should disclose any additional use before submission.

Before submission, review code, sources, limitations and this statement against
the challenge's disclosure requirements. No independent medical review or NASA
approval is claimed.

## Mission interface redesign

Codex assisted with design tokens, CSS, the Streamlit theme, Plotly status symbols,
time ranges, UI data checks, briefing prioritization, tests and `UI_DESIGN.md`.
That redesign left core analysis, simulation logic and the original briefing file
unchanged. Official NASA/W3C sources informed design. No images or external fonts
were generated or used. Python, pytest and AppTest checked contrast and behavior;
no visual browser test was performed. Review layout and keyboard operation manually.

Disclosure remains in project documentation. Developer-facing Codex/AI notices
were removed from the operational interface at the user's request so that it
focuses on statuses, measurements and review steps.

## English translation

Codex translated the interface, charts, explanations, errors, comments, docstrings,
test expectations and documentation for international submission. Scenario names
and summary-table labels were translated consistently. Calculations, thresholds,
raw data keys and synthetic values were preserved. Translation does not constitute
an independent scientific or medical review.
