"""Offline, validated OSD-575 CMP adapter. Never feeds the demo alert rules."""
from io import BytesIO
from pathlib import Path
import hashlib
import re
import zipfile

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "nasa" / "OSD-575"
CSV_NAME = "LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv"
ZIP_NAME = "OSD-575_metadata_OSD-575-ISA.zip"
STUDY_URL = "https://osdr.nasa.gov/bio/repo/data/studies/OSD-575"
DOI = "10.26030/mc5d-p710"
# Pinned to the NASA files verified on 2026-11-15, study version 3.
HASHES = {
    CSV_NAME: "5eb1e7f025dd8443a9e70111e62bc32afae3432753024489c5c013e401d709d9",
    ZIP_NAME: "a1d3e49e2b61ab427a8760d0c98e0324a53272d0e1314632290266b014476f1d",
}
# Exact source columns; units are abbreviated, never converted.
BIOMARKERS = {
    "Glucose": ("glucose_value_milligram_per_deciliter", "mg/dL", "Serum glucose concentration."),
    "Albumin": ("albumin_value_gram_per_deciliter", "g/dL", "Serum albumin protein concentration."),
    "Creatinine": ("creatinine_value_milligram_per_deciliter", "mg/dL", "Serum creatinine concentration."),
    "Sodium": ("sodium_value_millimol_per_liter", "mmol/L", "Serum sodium concentration."),
    "Potassium": ("potassium_value_millimol_per_liter", "mmol/L", "Serum potassium concentration."),
    "Total bilirubin": ("total_bilirubin_value_milligram_per_deciliter", "mg/dL", "Total serum bilirubin concentration."),
}


class NASADataError(ValueError):
    """Local NASA files are missing, changed or scientifically ambiguous."""


def validate_cmp(values: pd.DataFrame, samples: pd.DataFrame) -> pd.DataFrame:
    """Validate and join measurements to the ISA sample table, preserving gaps."""
    required_values = {"Sample Name", *(spec[0] for spec in BIOMARKERS.values())}
    required_samples = {"Sample Name", "Source Name", "Factor Value[Time]", "Unit",
                        "Factor Value[Spaceflight]", "Characteristics[Organism]",
                        "Characteristics[Material Type]"}
    if not required_values.issubset(values.columns) or not required_samples.issubset(samples.columns):
        raise NASADataError("Required CMP columns or sample metadata are missing.")
    if values.empty or samples.empty:
        raise NASADataError("CMP data or metadata is empty.")
    for frame in (values, samples):
        if frame["Sample Name"].isna().any() or frame["Sample Name"].duplicated().any():
            raise NASADataError("Missing or duplicate sample identifiers.")
    if not set(values["Sample Name"]).issubset(set(samples["Sample Name"])):
        raise NASADataError("A measurement has no matching sample metadata.")
    selected = values[["Sample Name", *(s[0] for s in BIOMARKERS.values())]].copy()
    for column in selected.columns[1:]:
        try:
            selected[column] = pd.to_numeric(selected[column], errors="raise")
        except (ValueError, TypeError) as error:
            raise NASADataError(f"Invalid numeric value in {column}.") from error
        if selected[column].isin([float("inf"), float("-inf")]).any():
            raise NASADataError(f"Infinite value in {column}.")
    merged = selected.merge(samples[list(required_samples)], on="Sample Name", validate="one_to_one")
    if not (merged["Characteristics[Organism]"].eq("Homo sapiens").all()
            and merged["Characteristics[Material Type]"].eq("Serum").all()
            and merged["Unit"].eq("day").all()):
        raise NASADataError("Unexpected organism, sample material or time unit.")
    labels, order = [], []
    for _, row in merged.iterrows():
        match = re.fullmatch(r"(Launch minus|Return plus) (\d+)", str(row["Factor Value[Time]"]))
        if not match or pd.isna(row["Source Name"]):
            raise NASADataError("Unknown time metadata or missing participant.")
        before, offset = match[1] == "Launch minus", int(match[2])
        expected_phase = "Pre-flight" if before else "Post-flight"
        label = f"L-{offset}" if before else f"R+{offset}"
        if row["Factor Value[Spaceflight]"] != expected_phase:
            raise NASADataError("Timepoint and flight phase disagree.")
        if row["Sample Name"] != f'{row["Source Name"]}_serum_{label}':
            raise NASADataError("Sample identifier and metadata disagree.")
        labels.append(label)
        # Ordering only: not an elapsed-day axis or conversion between L and R.
        order.append(-offset if before else offset)
    merged["Timepoint"] = labels
    merged["Timepoint order"] = order
    merged = merged.rename(columns={"Source Name": "Participant", "Factor Value[Time]": "Time description",
                                     "Factor Value[Spaceflight]": "Phase"})
    if merged.duplicated(["Participant", "Timepoint"]).any():
        raise NASADataError("Duplicate participant/timepoint pair.")
    return merged.sort_values(["Timepoint order", "Participant"]).reset_index(drop=True)


def load_cmp(folder: Path = DATA_DIR) -> pd.DataFrame:
    """Load the pinned NASA snapshot locally; no implicit download or fallback."""
    try:
        payloads = {name: (folder / name).read_bytes() for name in HASHES}
        for name, payload in payloads.items():
            if hashlib.sha256(payload).hexdigest() != HASHES[name]:
                raise NASADataError(f"Checksum mismatch for {name}; verify the NASA version before use.")
        values = pd.read_csv(BytesIO(payloads[CSV_NAME]), encoding="utf-8-sig",
                             keep_default_na=False, na_values=["", "NA", "N/A"])
        with zipfile.ZipFile(BytesIO(payloads[ZIP_NAME])) as archive:
            samples = pd.read_csv(BytesIO(archive.read("s_OSD-575.txt")), sep="\t", encoding="utf-8-sig")
        return validate_cmp(values, samples)
    except (OSError, UnicodeError, zipfile.BadZipFile, KeyError, pd.errors.ParserError) as error:
        raise NASADataError("NASA data could not be loaded. Restore the verified local CMP and metadata files.") from error
