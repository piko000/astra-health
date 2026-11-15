from pathlib import Path
import pandas as pd

path = (
    Path(__file__).parent
    / "nasa"
    / "OSD-575"
    / "LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv"
)

if not path.is_file():
    raise FileNotFoundError(f"Datei nicht gefunden: {path}")

df = pd.read_csv(path, encoding="utf-8-sig")

print("Zeilen und Spalten:", df.shape)
print("\nSpaltennamen:")
print(df.columns.tolist())

print("\nErste fünf Zeilen:")
print(df.head().to_string())