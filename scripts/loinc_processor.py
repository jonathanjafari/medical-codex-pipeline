# scripts/loinc_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_loinc_data(filepath: str) -> pd.DataFrame:
    """Load raw LOINC data file."""
    return pd.read_csv(filepath, dtype=str, low_memory=False)


def clean_loinc_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize LOINC codes."""
    # Use LOINC_NUM as code and COMPONENT as description
    df = raw.rename(columns={"LOINC_NUM": "code", "COMPONENT": "description"}).copy()

    # Drop rows without code or description
    df = df.dropna(subset=["code", "description"])

    # Strip whitespace
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()

    # Drop duplicates
    df = df.drop_duplicates()

    # Keep only standardized columns
    df = df[["code", "description"]]

    return df


def main() -> None:
    import logging
    init_logging()

    try:
        raw = load_loinc_data("input/Loinc.csv")
        clean = clean_loinc_data(raw)
        save_to_formats(clean, "output/csv/loinc_standardized")
        logging.info("LOINC processing completed.")
    except Exception as e:
        logging.error(f"LOINC processing failed: {e}")


if __name__ == "__main__":
    main()
