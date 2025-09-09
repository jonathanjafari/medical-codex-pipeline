"""
This script processes NPI data.
It loads the raw NPI file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path

# Ensure utils/ is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp, validate_code_format


def load_npi_data(filepath: str) -> pd.DataFrame:
    """Load raw NPI data (CSV)."""
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"Loaded {len(df)} NPI records")
    return df


def clean_npi_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate NPI numbers (10 digits)."""
    df.columns = [c.strip().lower() for c in df.columns]

    # Try common headers: 'npi' and a name/org field -> map to code/description
    col_map = {}
    if "npi" in df.columns:
        col_map["code"] = "npi"
    if "provider organization name (legal business name)" in df.columns:
        col_map["description"] = "provider organization name (legal business name)"
    elif "provider organization name" in df.columns:
        col_map["description"] = "provider organization name"
    elif "provider last name (legal name)" in df.columns:
        col_map["description"] = "provider last name (legal name)"
    else:
        # fallback if file already has code/description
        if {"code", "description"}.issubset(set(df.columns)):
            col_map["code"] = "code"
            col_map["description"] = "description"

    if not col_map or "code" not in col_map or "description" not in col_map:
        # minimal fallback to avoid crashing on unknown columns
        keep = [c for c in ["code", "description"] if c in df.columns]
        if len(keep) == 2:
            df = df[keep].copy()
        else:
            # last-ditch: take first two columns and rename
            df = df.iloc[:, :2].copy()
            df.columns = ["code", "description"]
    else:
        df = df[[col_map["code"], col_map["description"]]].copy()
        df.columns = ["code", "description"]

    df["code"] = df["code"].astype(str).str.strip()
    df["description"] = df["description"].astype(str).fillna("No description").str.strip()

    pattern = r"^\d{10}$"
    df = df[df["code"].apply(lambda x: validate_code_format(x, pattern))]

    df["last_updated"] = get_timestamp()
    return df


def main():
    """Run the NPI processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/npi_registry_2024.csv")
    output_file = Path("output/csv/npi_cleaned")

    raw = load_npi_data(input_file)
    clean = clean_npi_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()
