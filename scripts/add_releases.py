"""Add storage-v3 release archives and registry entries to a Theta Hub checkout.

Usage: add_releases.py HUB ARCHIVE_DIR... --published-at ISO
Then rebuild the feeds with build_index.py and check with validate_manifest.py --check-archives.
Each registry entry is the archive's own manifest plus the Hub-only listing fields of the
existing entry; `releases` lists only the new release (storage-v2 archives no longer install).
Existing archives are never overwritten.
"""
import argparse, hashlib, json, shutil, sys
from pathlib import Path
from zipfile import ZipFile

BASE = "https://raw.githubusercontent.com/ThetaIDE/ThetaHub/main/packages"
LISTING = ("description", "author", "repository", "license", "tags", "icon", "hidden", "suite",
           "created_at", "default_enabled", "extra")
KIND_DIRS = {"datamodule": "datamodules", "env": "envs", "evaluator": "evaluators", "experiment": "experiments",
             "method": "methods", "model": "models", "plotter": "plotters", "plugin": "plugins", "suite": "suites",
             "tuner": "tuners", "package": "packages", "scheduler": "schedulers"}

parser = argparse.ArgumentParser()
parser.add_argument("hub", type=Path)
parser.add_argument("archives", nargs="+", type=Path)
parser.add_argument("--published-at", required=True)
args = parser.parse_args()
hub = args.hub
existing = {json.loads(p.read_text())["id"]: p for p in (hub / "registry").rglob("*.json")}
rows = []
for directory in args.archives:
    for archive in sorted(directory.glob("*.zip")):
        with ZipFile(archive) as bundle:
            manifest = json.loads(bundle.read(".theta_component.json"))
        assert archive.name == f"{manifest['id']}-{manifest['version']}.zip", archive
        target = hub / "packages" / archive.name
        if target.exists():
            if target.read_bytes() != archive.read_bytes():
                sys.exit(f"Refusing to overwrite a different published archive: {target}")
        else:
            shutil.copyfile(archive, target)
        data = archive.read_bytes()
        path = existing.get(manifest["id"])
        old = json.loads(path.read_text()) if path else {}
        entry = dict(manifest)
        for field in LISTING:
            if field not in entry and field in old:
                entry[field] = old[field]
        entry["releases"] = {manifest["version"]: {
            "tag": f"v{manifest['version']}", "url": f"{BASE}/{archive.name}",
            "sha256": hashlib.sha256(data).hexdigest(), "published_at": args.published_at, "size_bytes": len(data)}}
        path = path or hub / "registry" / KIND_DIRS[manifest["kind"]] / f"{manifest['id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(entry, indent=2, ensure_ascii=False) + "\n")
        rows.append((manifest["id"], old.get("version", "-"), manifest["version"], path.relative_to(hub)))
for row in rows:
    print(*row, sep="\t")
