# snomed_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats, get_timestamp


def load_snomed_data(filepath: str) -> pd.DataFrame:
    """Load raw SNOMED CT descriptions file (RF2 format)."""
    return pd.read_csv(filepath, sep="\t", dtype=str)


def clean_snomed_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize SNOMED CT codes."""
    # Keep only active rows
    df = raw[raw["active"] == "1"].copy()

    # Select conceptId and term as code/description
    df = df.rename(columns={"conceptId": "code", "term": "description"})
    df = df[["code", "description"]].copy()

    # Strip whitespace, drop duplicates
    df.loc[:, "code"] = df["code"].str.strip()
    df.loc[:, "description"] = df["description"].str.strip()
    df = df.drop_duplicates()

    # Add last_updated column safely
    df.loc[:, "last_updated"] = get_timestamp()

    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_snomed_data("input/sct2_Description_Full-en_US1000124_20250901.txt")
    clean = clean_snomed_data(raw)
    save_to_formats(clean, "output/csv/snomed_standardized")

    logging.info("SNOMED CT processing completed.")


if __name__ == "__main__":
    main()
