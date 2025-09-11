# snomed_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_snomed_data(filepath: str) -> pd.DataFrame:
    """Load raw SNOMED CT data file."""
    return pd.read_csv(filepath, dtype=str)


def clean_snomed_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize SNOMED CT codes."""
    df = raw.dropna(subset=["code", "description"]).copy()
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    df = df[["code", "description"]]
    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_snomed_data("input/snomed_concepts.txt")
    clean = clean_snomed_data(raw)
    save_to_formats(clean, "output/csv/snomed_standardized")

    logging.info("SNOMED CT processing completed.")


if __name__ == "__main__":
    main()
