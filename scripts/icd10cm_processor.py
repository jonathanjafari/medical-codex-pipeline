"""
This script processes ICD-10-CM data.
It loads the raw ICD-10-CM codes file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path

# Ensure utils/ is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp, validate_code_format


def load_icd10cm_data(filepath: str) -> pd.DataFrame:
    """Load raw ICD-10-CM data from a pipe-delimited file."""
    df = pd.read_csv(filepath, sep="|", dtype=str)
    logging.info(f"Loaded {len(df)} ICD-10-CM records")
    return df


def clean_icd10cm_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate ICD-10-CM codes."""
    # normalize headers to lowercase
    df.columns = [c.strip().lower() for c in df.columns]

    # keep only code + description
    df = df[["code", "description"]].copy()
    df["code"] = df["code"].str.strip().str.upper()
    df["description"] = df["description"].fillna("No description").str.strip()

    # ICD-10/ICD-10-CM format: Letter + 2 digits, optional . + 1-4 alphanumerics
    pattern = r"^[A-TV-Z][0-9]{2}(?:\.[0-9A-TV-Z]{1,4})?$"
    df = df[df["code"].apply(lambda x: validate_code_format(x, pattern))]

    # add timestamp
    df["last_updated"] = get_timestamp()
    return df


def main():
    """Run the ICD-10-CM processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/icd10cm_codes_2024.txt")
    output_file = Path("output/csv/icd10cm_cleaned")

    raw = load_icd10cm_data(input_file)
    clean = clean_icd10cm_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()

