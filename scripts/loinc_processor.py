"""
This script processes LOINC data.
It loads the raw LOINC codes file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path

# Ensure utils/ is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp, validate_code_format


def load_loinc_data(filepath: str) -> pd.DataFrame:
    """Load raw LOINC data (CSV)."""
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"Loaded {len(df)} LOINC records")
    return df


def clean_loinc_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate LOINC codes (digits-digits like 1234-5)."""
    df.columns = [c.strip().lower() for c in df.columns]
    df = df[["code", "description"]].copy()

    df["code"] = df["code"].astype(str).str.strip()
    df["description"] = df["description"].astype(str).fillna("No description").str.strip()

    # Allow a reasonable LOINC pattern (flexible)
    pattern = r"^\d{1,7}-\d{1,2}$"
    df = df[df["code"].apply(lambda x: validate_code_format(x, pattern))]

    df["last_updated"] = get_timestamp()
    return df


def main():
    """Run the LOINC processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/loinc_2024.csv")
    output_file = Path("output/csv/loinc_cleaned")

    raw = load_loinc_data(input_file)
    clean = clean_loinc_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()
