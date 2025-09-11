# icd10cm_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_icd10cm_data(filepath: str) -> pd.DataFrame:
    """Load raw ICD-10-CM data file."""
    return pd.read_csv(filepath, dtype=str)


def clean_icd10cm_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize ICD-10-CM codes."""
    df = raw.dropna(subset=["code", "description"]).copy()
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    df["is_valid"] = df["code"].apply(lambda c: validate_code_format(c, "icd10cm"))
    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_icd10cm_data("input/icd10cm_order_2025.csv")
    clean = clean_icd10cm_data(raw)
    save_to_formats(clean, "output/csv/icd10cm_standardized")

    logging.info("ICD-10-CM processing completed.")


if __name__ == "__main__":
    main()
