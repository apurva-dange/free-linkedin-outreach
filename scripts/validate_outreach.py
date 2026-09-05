#!/usr/bin/env python3
"""Validate a Free LinkedIn Outreach JSON or CSV contact batch."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

REQUIRED = {
    "company",
    "name",
    "title",
    "function",
    "relationship_status",
    "linkedin_url",
    "message",
}

ALLOWED_STATUS = {
    "Current",
    "Alumni",
    "Parent company",
    "Founder/advisor",
    "Ecosystem",
    "Uncertain",
}

TALENT_FUNCTIONS = {"talent", "recruiting", "human resources", "people", "hr"}


def load_rows(path: Path) -> list[dict[str, str]]:
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("JSON input must be an array of contact objects")
    return data


def normalize_linkedin(url: str) -> str:
    parts = urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    path = parts.path.rstrip("/").lower()
    return urlunsplit(("https", host, path, "", ""))


def validate(rows: list[dict[str, str]], per_company: int, max_length: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    company_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    normalized_urls: list[str] = []

    for index, row in enumerate(rows, start=1):
        missing = sorted(field for field in REQUIRED if not str(row.get(field, "")).strip())
        if missing:
            errors.append(f"Row {index}: missing {', '.join(missing)}")
            continue

        company = str(row["company"]).strip()
        company_rows[company].append(row)
        message = str(row["message"])
        url = str(row["linkedin_url"]).strip()
        status = str(row["relationship_status"]).strip()

        if len(message) > max_length:
            errors.append(f"Row {index}: message is {len(message)} characters; maximum is {max_length}")
        if "linkedin.com/in/" not in url.lower():
            errors.append(f"Row {index}: linkedin_url is not a direct /in/ profile URL")
        else:
            normalized_urls.append(normalize_linkedin(url))
        if status not in ALLOWED_STATUS:
            errors.append(f"Row {index}: unsupported relationship_status {status!r}")
        if status in {"Alumni", "Uncertain"} and company.lower() in message.lower():
            warnings.append(f"Row {index}: {status} message mentions the company; verify wording")

    duplicates = [url for url, count in Counter(normalized_urls).items() if count > 1]
    for url in duplicates:
        errors.append(f"Duplicate LinkedIn profile: {url}")

    for company, group in company_rows.items():
        if len(group) != per_company:
            errors.append(f"{company}: expected {per_company} contacts, found {len(group)}")
        talent_count = sum(
            str(row.get("function", "")).strip().lower() in TALENT_FUNCTIONS for row in group
        )
        if talent_count < 2:
            warnings.append(f"{company}: only {talent_count} talent/people contacts")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON or CSV contact file")
    parser.add_argument("--contacts-per-company", type=int, default=5)
    parser.add_argument("--max-message-length", type=int, default=299)
    args = parser.parse_args()

    try:
        rows = load_rows(args.input)
        errors, warnings = validate(rows, args.contacts_per_company, args.max_message_length)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"Validation passed: {len(rows)} contacts, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
