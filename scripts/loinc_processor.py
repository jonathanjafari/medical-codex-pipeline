# loinc_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_loinc_data(filepath: str) -> pd.DataFrame:
    """Load raw LOINC data file."""
    return pd.read_csv(filepath, dtype=str)


def clean_loinc_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize LOINC codes."""
    df = raw.rename(columns={"LOINC_NUM": "code", "COMPONENT": "description"})[
        ["code", "description"]
    ].copy()
    df = df.dropna(subset=["code", "description"])
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    df["is_valid"] = df["code"].apply(lambda c: validate_code_format(c, "loinc"))
    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_loinc_data("input/Loinc.csv")
    clean = clean_loinc_data(raw)
    save_to_formats(clean, "output/csv/loinc_standardized")

    logging.info("LOINC processing completed.")


if __name__ == "__main__":
    main()
