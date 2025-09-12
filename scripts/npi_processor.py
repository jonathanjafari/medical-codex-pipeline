# scripts/npi_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_npi_data(filepath: str) -> pd.DataFrame:
    """Load raw NPI data file (limit for performance)."""
    return pd.read_csv(filepath, sep=",", dtype=str, nrows=10000)  # limit to 10k rows


def clean_npi_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize NPI records."""
    df = raw.copy()

    # Standardize code column
    df = df.rename(columns={"NPI": "code"})

    # Build description column
    def build_description(row):
        if row.get("Entity Type Code") == "1":  # Individual
            last = row.get("Provider Last Name (Legal Name)", "")
            first = row.get("Provider First Name", "")
            cred = row.get("Provider Credential Text", "")
            return f"{last}, {first} {cred}".strip()
        else:  # Organization
            return row.get("Provider Organization Name (Legal Business Name)", "")

    df["description"] = df.apply(build_description, axis=1)

    # Keep only code + description
    df = df[["code", "description"]].dropna()

    # Strip spaces
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()

    # Drop duplicates
    df = df.drop_duplicates()

    return df


def main() -> None:
    import logging
    init_logging()

    try:
        raw = load_npi_data("input/npidata_pfile_20050523-20250907.csv")
        clean = clean_npi_data(raw)
        save_to_formats(clean, "output/csv/npi_standardized")
        logging.info("NPI processing completed.")
    except Exception as e:
        logging.error(f"NPI processing failed: {e}")


if __name__ == "__main__":
    main()
