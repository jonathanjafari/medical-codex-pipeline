# icd10who_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_icd10who_data(filepath: str) -> pd.DataFrame:
    """Load raw ICD-10-WHO data file (semicolon-delimited)."""
    return pd.read_csv(filepath, sep=";", header=None, dtype=str)


def clean_icd10who_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize ICD-10-WHO codes."""
    df = raw[[4, 8]].rename(columns={4: "code", 8: "description"}).copy()
    df = df.dropna(subset=["code", "description"])
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    df["is_valid"] = df["code"].apply(lambda c: validate_code_format(c, "icd10who"))
    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_icd10who_data("input/icd102019syst_codes_WHO.txt")
    clean = clean_icd10who_data(raw)
    save_to_formats(clean, "output/csv/icd10who_standardized")

    logging.info("ICD-10-WHO processing completed.")


if __name__ == "__main__":
    main()
