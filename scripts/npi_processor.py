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
    df = raw.copy()

    # Standardize code column
    df = df.rename(columns={"NPI": "code"})

    # Build description column (individuals get Last, First + credential; orgs get org name)
    df["description"] = df.apply(
        lambda row: (
            f"{row['Provider Last Name (Legal Name)']}, {row['Provider First Name']} {row['Provider Credential Text'] or ''}".strip()
            if row["Entity Type Code"] == "1"
            else row["Provider Organization Name (Legal Business Name)"]
        ),
        axis=1,
    )

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

    raw = load_npi_data("input/npidata_pfile_20050523-20250907.csv")
    clean = clean_npi_data(raw)
    save_to_formats(clean, "output/csv/npi_standardized")

    logging.info("NPI processing completed.")


if __name__ == "__main__":
    main()
