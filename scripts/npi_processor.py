# npi_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_npi_data(filepath):
    """Load raw NPI data file (sample only)."""
    return pd.read_csv(filepath, sep=",", dtype=str, nrows=10000)  # limit to 10k rows


def clean_npi_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize NPI records."""
    df = raw.rename(columns={"NPI": "code", "Entity Type Code": "description"})[
        ["code", "description"]
    ].copy()
    df = df.dropna(subset=["code", "description"])
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    df["is_valid"] = df["code"].apply(lambda c: validate_code_format(c, "npi"))
    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_npi_data("input/npidata_pfile_20050523-20250907.csv")
    clean = clean_npi_data(raw)
    save_to_formats(clean, "output/csv/npi_standardized")

    logging.info("NPI processing completed.")


if __name__ == "__main__":
    main()
