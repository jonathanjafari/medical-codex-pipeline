# scripts/icd10who_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_icd10who_data(filepath: str) -> pd.DataFrame:
    """Load raw ICD-10-WHO data file (semicolon-delimited)."""
    return pd.read_csv(filepath, sep=";", header=None, dtype=str, low_memory=False)


def clean_icd10who_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize ICD-10-WHO codes."""
    # Extract only code (col 4) and description (col 8)
    df = raw[[4, 8]].rename(columns={4: "code", 8: "description"}).copy()

    # Drop rows missing either field
    df = df.dropna(subset=["code", "description"])

    # Strip whitespace
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()

    # Drop duplicates
    df = df.drop_duplicates()

    # Keep only the two columns
    df = df[["code", "description"]]

    return df


def main() -> None:
    import logging
    init_logging()

    try:
        raw = load_icd10who_data("input/icd102019syst_codes_WHO.txt")
        clean = clean_icd10who_data(raw)
        save_to_formats(clean, "output/csv/icd10who_standardized")
        logging.info("ICD-10-WHO processing completed.")
    except Exception as e:
        logging.error(f"ICD-10-WHO processing failed: {e}")


if __name__ == "__main__":
    main()
