# icd10cm_processor.py
"""
This script processes ICD-10-CM data.
It loads the raw ICD-10-CM codes file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats, get_timestamp

# Input file (local only, excluded from GitHub)
INPUT_FILE = "input/icd10cm_order_2025.csv"


def load_icd10cm_data(filepath: str) -> pd.DataFrame:
    """Load raw ICD-10-CM data from a CSV file."""
    df = pd.read_csv(filepath, sep=",", dtype=str)
    return df


def clean_icd10cm_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize ICD-10-CM codes."""
    df = raw.rename(columns={"code": "code", "description": "description"}).copy()

    # Drop missing values
    df = df.dropna(subset=["code", "description"])

    # Strip spaces
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()

    # Validate codes
    df = df[df["code"].apply(lambda x: validate_code_format(x, "icd10cm"))]

    # Remove duplicates
    df = df.drop_duplicates()

    # Add last_updated
    if not df.empty:
        df["last_updated"] = get_timestamp()

    return df[["code", "description", "last_updated"]]


def main() -> None:
    import logging
    init_logging()

    raw = load_icd10cm_data(INPUT_FILE)
    clean = clean_icd10cm_data(raw)
    save_to_formats(clean, "output/csv/icd10cm_standardized")

    logging.info("ICD-10-CM processing completed.")


if __name__ == "__main__":
    main()
