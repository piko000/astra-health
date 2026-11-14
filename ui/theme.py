"""Shared colors for Streamlit and Plotly; no external assets."""

COLORS = {
    "background": "#0B1220", "surface": "#172235", "elevated": "#1E2D42",
    "accent": "#38BDF8", "text": "#F1F5F9", "muted": "#A8B6C9",
    "warning": "#FBBF24", "critical": "#FB7185", "success": "#34D399",
    "border": "#718399",
}
STATUS_COLORS = {"NORMAL": COLORS["success"], "WARNING": COLORS["warning"],
                 "CRITICAL": COLORS["critical"], "UNKNOWN": COLORS["muted"],
                 "NO DATA": COLORS["muted"]}


def stylesheet() -> str:
    variables = ";".join(f"--astra-{k}:{v}" for k, v in COLORS.items())
    return "<style>:root{" + variables + "}" + """
    .stApp {background:var(--astra-background); color:var(--astra-text);}
    .stApp, .stApp button, .stApp input, .stApp select {
        font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
        font-variant-numeric:tabular-nums;
    }
    .stMainBlockContainer {padding:1.5rem 2rem 2rem; max-width:1600px;}
    [data-testid="stSidebar"] {background:var(--astra-surface);}
    .stApp h1 {font-size:2rem; font-weight:650; letter-spacing:-.03em; padding-top:0;}
    .stApp h2, .stApp h3 {font-size:1.3rem; font-weight:600;}
    .stApp p, .stApp li {font-size:1rem; line-height:1.5;}
    [data-testid="stCaptionContainer"] p {color:var(--astra-muted); font-size:.875rem;}
    [data-testid="stMetricValue"] {font-size:2rem; color:var(--astra-text);}
    [data-testid="stMetricLabel"] p {font-size:.9375rem;}
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        white-space:normal; overflow:visible; overflow-wrap:anywhere;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color:var(--astra-border) !important; border-radius:8px;
    }
    [class*="st-key-vital_"] {background:var(--astra-surface); border-radius:8px;}
    .stApp a {color:var(--astra-accent); text-decoration:underline;}
    .stApp :is(button, input, select, a, [tabindex]):focus-visible {
        outline:3px solid var(--astra-accent) !important; outline-offset:3px;
    }
    .stApp button {min-height:44px;}
    .stApp button[role="tab"] {color:var(--astra-muted); padding:8px 16px;}
    .stApp button[role="tab"][aria-selected="true"] {
        color:var(--astra-text); background:var(--astra-elevated);
        border-bottom:3px solid var(--astra-accent);
    }
    .stApp button[role="tab"]:hover {background:var(--astra-elevated);}
    [data-testid="stAlert"] {background:var(--astra-surface); color:var(--astra-text);}
    [data-testid="stAlert"] p {color:var(--astra-text);}
    .astra-status {font-size:.875rem; font-weight:650; margin:0;}
    @media (max-width:1100px) {
        .st-key-analysis_layout > [data-testid="stHorizontalBlock"] {flex-wrap:wrap;}
        .st-key-analysis_layout > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            width:100% !important; flex:1 1 100% !important; min-width:0;
        }
    }
    @media (max-width:700px) {
        .stMainBlockContainer {padding:1rem;}
        [data-testid="stHorizontalBlock"] {flex-wrap:wrap;}
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            width:100% !important; flex:1 1 100% !important; min-width:0;
        }
        [role="tablist"] {flex-wrap:wrap; height:auto; gap:4px;}
        .stApp button[role="tab"] {white-space:normal; height:auto; padding:8px;}
        .stApp h1 {font-size:1.75rem;}
    }
    </style>"""
