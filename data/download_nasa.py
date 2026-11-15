"""Download the public OSD-575 CMP and metadata files directly from NASA."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlsplit
from data.nasa_loader import HASHES

ROOT = Path(__file__).resolve().parent / "nasa" / "OSD-575"
API = "https://osdr.nasa.gov/osdr/data/osd/files/575/"
FILES = ("LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv",
         "OSD-575_metadata_OSD-575-ISA.zip")


def download():
    ROOT.mkdir(parents=True, exist_ok=True)
    with urlopen(API, timeout=60) as response:
        catalog_bytes = response.read()
    catalog = json.loads(catalog_bytes)
    metadata_url = "https://osdr.nasa.gov/osdr/data/osd/meta/575"
    with urlopen(metadata_url, timeout=60) as response:
        metadata_bytes = response.read()
    if json.loads(metadata_bytes)["study"]["OSD-575"]["version"] != 3:
        raise ValueError("Study version changed; review before updating this snapshot.")
    entries = {f["file_name"]: f for f in catalog["studies"]["OSD-575"]["study_files"]}
    pending = []
    for name in FILES:
        entry = entries[name]
        if entry["restricted"] or not entry["visible"]:
            raise ValueError(f"File is not public: {name}")
        url = "https://osdr.nasa.gov" + entry["remote_url"]
        if not entry["remote_url"].startswith("/geode-py/ws/studies/OSD-575/download?"):
            raise ValueError("Unexpected download route")
        with urlopen(url, timeout=60) as response:
            location = urlsplit(response.url)
            if location.scheme != "https" or location.netloc not in {
                "osdr.nasa.gov", "genelab-alsda-repo-prod.s3.amazonaws.com",
                "genelab-shared-repo-prod.s3.amazonaws.com",
            }:
                raise ValueError("Unexpected download host")
            payload = response.read()
        if len(payload) != entry["file_size"]:
            raise ValueError(f"Size mismatch: {name}")
        if hashlib.sha256(payload).hexdigest() != HASHES[name]:
            raise ValueError(f"NASA file changed: {name}. Review before replacing the pinned snapshot.")
        pending.append((name, payload, {"name": name, "url": url, "bytes": len(payload),
                                      "sha256": hashlib.sha256(payload).hexdigest(),
                                      "resolved_url": location._replace(query="", fragment="").geturl()}))
    for name, payload, _ in pending:
        (ROOT / name).write_bytes(payload)
    (ROOT / "files_catalog.json").write_bytes(catalog_bytes)
    (ROOT / "study_metadata.json").write_bytes(metadata_bytes)
    (ROOT / "download_manifest.json").write_text(json.dumps({
        "study": "OSD-575", "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "catalog_url": API, "study_version": 3, "metadata_url": metadata_url,
        "metadata_sha256": hashlib.sha256(metadata_bytes).hexdigest(),
        "files": [record for _, _, record in pending],
    }, indent=2), encoding="utf-8")
    print("Downloaded and recorded:", ", ".join(FILES))


if __name__ == "__main__":
    download()
