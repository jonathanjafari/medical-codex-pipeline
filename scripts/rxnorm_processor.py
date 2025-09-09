#!/usr/bin/env python3
"""
This script processes RxNorm data.
It loads the raw RxNorm file, cleans it, (optionally) validates codes,
and saves the output to a standardized CSV format.

Run examples:
  python3 scripts/rxnorm_processor.py --input input/rxnorm_2024.txt --out output/csv/rxnorm_cleaned.csv
  python3 scripts/rxnorm_processor.py --input input/rxnorm_2024.txt --out output/csv/rxnorm_cleaned.csv --sep '|' --strict
"""

import argparse
import logging
import sys, os
from pathlib import Path
import pandas as pd

# Ensure utils/ is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp, validate_code_format


def _read_as_str(path: str | Path, sep: str | None) -> pd.DataFrame:
    """Read as strings; if sep not given, try ',', '\\t', '|' in that order."""
    kwargs = dict(dtype=str, keep_default_na=False, na_filter=False, low_memory=False)
    if sep:
        return pd.read_csv(path, sep=sep, **kwargs)
    for trial in [",", "\t", "|"]:
        try:
            return pd.read_csv(path, sep=trial, **kwargs)
        except Exception:
            continue
    return pd.read_csv(path, **kwargs)


def load_rxnorm_data(filepath: str | Path, sep: str | None) -> pd.DataFrame:
    """Load raw RxNorm data (CSV, tab, or pipe)."""
    df = _read_as_str(filepath, sep)
    logging.info(f"Loaded {len(df)} RxNorm records")
    return df


def clean_rxnorm_data(df: pd.DataFrame, strict_numeric: bool = False) -> pd.DataFrame:
    """Normalize headers, map to code/description, basic clean, optional numeric validation."""
    # Normalize headers
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # Determine which columns to use
    code_key = None
    desc_key = None

    # If file already has code/description, honor it
    if {"code", "description"}.issubset(df.columns):
        code_key, desc_key = "code", "description"
    else:
        # Common RxNorm headers
        if "rxcui" in df.columns:
            code_key = "rxcui"
        if "str" in df.columns:
            desc_key = "str"
        elif "name" in df.columns:
            desc_key = "name"
        elif "description" in df.columns:
            desc_key = "description"

    # As a last resort, take the first two columns as code/description
    if not code_key or not desc_key:
        if df.shape[1] >= 2:
            df = df.iloc[:, :2].copy()
            df.columns = ["code", "description"]
        else:
            # Nothing usable; return empty with required columns
            out = pd.DataFrame(columns=["code", "description", "last_updated"])
            return out

    if code_key and desc_key:
        df = df[[code_key, desc_key]].copy()
        df.columns = ["code", "description"]

    # Clean
    df["code"] = df["code"].astype(str).str.strip()
    df["description"] = df["description"].astype(str).fillna("No description").str.strip()

    # Drop empty codes
    df = df[df["code"].str.len() > 0]

    # Optional strict numeric check (only keep codes that are all digits)
    if strict_numeric:
        pattern = r"^\d+$"
        before = len(df)
        df = df[df["code"].apply(lambda x: validate_code_format(x, pattern))]
        logging.info("Strict numeric filter kept %d / %d rows", len(df), before)

    # Timestamp
    df["last_updated"] = get_timestamp()
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw RxNorm file (e.g., input/rxnorm_2024.txt)")
    parser.add_argument("--out", required=True, help="Output CSV path (e.g., output/csv/rxnorm_cleaned.csv)")
    parser.add_argument("--sep", default=None, help="Delimiter (',', '\\t', or '|'); auto-detect if omitted")
    parser.add_argument("--strict", action="store_true", help="Only keep rows where code is all digits")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    raw = load_rxnorm_data(args.input, sep=args.sep)
    clean = clean_rxnorm_data(raw, strict_numeric=args.strict)

    # Ensure parent dir exists
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    # Save via shared util
    save_to_formats(clean, Path(args.out))

    logging.info("Saved %s (%d rows, %d cols)", args.out, len(clean), clean.shape[1])


if __name__ == "__main__":
    main()
