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
    """Load raw ICD-10-CM data file."""
    try:
        return pd.read_csv(filepath, dtype=str)
    except FileNotFoundError:
        import logging
        logging.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        import logging
        logging.error(f"Error loading ICD-10-CM data: {e}")
        raise


def clean_icd10cm_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize ICD-10-CM codes."""
    try:
        df = raw.rename(columns={"code": "code", "description": "description"}).copy()
        df = df.dropna(subset=["code", "description"])
        df["code"] = df["code"].str.strip()
        df["description"] = df["description"].str.strip()
        df = df.drop_duplicates()
        df = df[["code", "description"]]
        return df
    except Exception as e:
        import logging
        logging.error(f"Error cleaning ICD-10-CM data: {e}")
        raise


def main() -> None:
    import logging
    init_logging()

    try:
        raw = load_icd10cm_data("input/icd10cm_order_2025.csv")
        clean = clean_icd10cm_data(raw)
        save_to_formats(clean, "output/csv/icd10cm_standardized")
        logging.info("ICD-10-CM processing completed.")
    except Exception as e:
        logging.error(f"ICD-10-CM processing failed: {e}")


if __name__ == "__main__":
    main()
