#!/usr/bin/env python3
"""Validates individual component manifests for schema conformity and integrity."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.request
from urllib.parse import urlparse
from zipfile import ZipFile

VALID_KINDS = {"plugin", "method", "model", "env", "experiment", "suite", "package", "datamodule", "evaluator", "plotter"}
SEMVER_REGEX = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$")
ID_REGEX = re.compile(r"^[a-z0-9][a-z0-9-_]{1,63}$")


def validate_manifest(file_path: Path, check_urls: bool = False, check_archives: bool = False) -> list[str]:
    errors = []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"JSON Parse Error: {exc}"]

    # Required fields
    required_fields = ["id", "name", "kind", "version", "description", "author", "repository", "releases",
                       "storage_version", "api_version", "capabilities", "payload"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    if errors:
        return errors

    if data["storage_version"] != 2 or data["api_version"] != 1:
        errors.append("Current releases require storage_version: 2 and api_version: 1")
    for field in ("target_path", "legacy_paths", "module_aliases", "legacy_archive"):
        if field in data:
            errors.append(f"Native listings cannot declare '{field}'")
    if not isinstance(data["capabilities"], list):
        errors.append("'capabilities' must be an explicit list")
    payload = data["payload"]
    if not isinstance(payload, dict) or not all(k in payload for k in ("implementations", "resources", "configs")):
        errors.append("'payload' must declare implementations, resources and configs")

    # ID validation
    if not ID_REGEX.match(data["id"]):
        errors.append(f"Invalid id '{data['id']}': must match ^[a-z0-9][a-z0-9-_]{{1,63}}$")

    # Filename matching ID
    if file_path.stem != data["id"]:
        errors.append(f"Filename '{file_path.name}' does not match component id '{data['id']}.json'")

    # Kind validation
    if data["kind"] not in VALID_KINDS:
        errors.append(f"Invalid kind '{data['kind']}': must be one of {sorted(VALID_KINDS)}")

    # Version validation
    if not SEMVER_REGEX.match(data["version"]):
        errors.append(f"Invalid semver version '{data['version']}': must be like '1.0.0'")

    # Description length
    if len(data.get("description", "")) < 10:
        errors.append("Description must be at least 10 characters long.")

    # Author
    author = data.get("author")
    if not isinstance(author, (dict, str)):
        errors.append("'author' must be an object or string")
    elif isinstance(author, dict) and "name" not in author:
        errors.append("'author' object must contain 'name'")

    # Releases
    releases = data.get("releases", {})
    if not isinstance(releases, dict) or not releases:
        errors.append("'releases' must be a non-empty dictionary of versions")
    else:
        if data["version"] not in releases:
            errors.append("The current version must have an explicit release entry")
        for ver, rdata in releases.items():
            if not isinstance(rdata, dict):
                errors.append(f"Release '{ver}' must be an object")
                continue
            if "url" not in rdata or "tag" not in rdata:
                errors.append(f"Release '{ver}' must contain 'url' and 'tag'")
            sha = rdata.get("sha256", "")
            if sha and (len(sha) != 64 or not all(c in "0123456789abcdefABCDEF" for c in sha)):
                errors.append(f"Release '{ver}' sha256 must be a 64-character hex string")

            if check_urls and "url" in rdata:
                url = rdata["url"]
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "ThetaHub-Validator/1.0"}, method="HEAD")
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        if resp.status >= 400:
                            errors.append(f"Release '{ver}' URL returned HTTP status {resp.status}: {url}")
                except Exception as exc:
                    errors.append(f"Release '{ver}' URL is unreachable: {exc}")

        if check_archives and data["version"] in releases:
            release = releases[data["version"]]
            archive_name = Path(urlparse(release.get("url", "")).path).name
            archive = Path(__file__).resolve().parent.parent / "packages" / archive_name
            try:
                if not archive_name or archive.suffix != ".zip":
                    raise ValueError("Release URL must identify a ZIP archive")
                digest = hashlib.sha256(archive.read_bytes()).hexdigest()
                if digest != release.get("sha256"):
                    raise ValueError("Current archive SHA-256 does not match its release entry")
                with ZipFile(archive) as package:
                    native = json.loads(package.read(".theta_component.json"))
                    for field in ("id", "kind", "version", "storage_version", "api_version", "capabilities", "payload", "dependencies"):
                        if native.get(field) != data.get(field):
                            raise ValueError(f"Current archive manifest differs from registry field '{field}'")
                    if any(field in native for field in ("target_path", "legacy_paths", "module_aliases", "legacy_archive")):
                        raise ValueError("Current archive contains obsolete ownership fields")
            except Exception as exc:
                errors.append(f"Current archive is invalid: {exc}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate Theta Hub component manifests.")
    parser.add_argument("manifests", nargs="*", type=Path, help="Paths to manifest json files")
    parser.add_argument("--check-urls", action="store_true", help="Perform HTTP HEAD requests on release URLs")
    parser.add_argument("--check-archives", action="store_true", help="Verify current package hashes and embedded native manifests")
    args = parser.parse_args()

    files = args.manifests
    if not files:
        registry_dir = Path(__file__).resolve().parent.parent / "registry"
        files = list(registry_dir.rglob("*.json"))

    total_errors = 0
    for path in files:
        if path.name.startswith(".") or "schemas" in path.parts:
            continue
        errors = validate_manifest(path, check_urls=args.check_urls, check_archives=args.check_archives)
        if errors:
            print(f"❌ FAIL: {path}")
            for err in errors:
                print(f"   • {err}")
            total_errors += len(errors)
        else:
            print(f"✅ PASS: {path}")

    if total_errors > 0:
        print(f"\nTotal errors found: {total_errors}", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nAll manifests validated successfully!")


if __name__ == "__main__":
    main()
