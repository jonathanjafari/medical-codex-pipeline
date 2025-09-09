"""
This script processes SNOMED CT data.
It loads the raw SNOMED file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path

# allow "from utils..." to work when running this file directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp, validate_code_format


def load_snomed_data(filepath: str) -> pd.DataFrame:
    """Load raw SNOMED data. Try comma CSV first, then pipe or tab if needed."""
    try:
        # Your file is code,description (comma CSV)
        df = pd.read_csv(filepath, sep=",", dtype=str)
    except Exception:
        # fallback for pipe-delimited
        try:
            df = pd.read_csv(filepath, sep="|", dtype=str)
        except Exception:
            # fallback for tab-delimited
            df = pd.read_csv(filepath, sep="\t", dtype=str)

    logging.info(f"Loaded {len(df)} SNOMED records")
    return df


def clean_snomed_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate SNOMED codes."""
    # If headers are already code,description this just works
    # If someone used Code/Description, make them lowercase to match
    df.columns = [c.strip().lower() for c in df.columns]

    # Keep only what we need
    df = df[["code", "description"]].copy()

    # Basic cleanup
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].fillna("No description").str.strip()

    # SNOMED concept IDs are numeric
    df = df[df["code"].apply(lambda x: validate_code_format(x, r"^\d+$"))]

    # Timestamp
    df["last_updated"] = get_timestamp()
    return df


def main():
    """Run the SNOMED processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/snomed_concepts.txt")   # your current sample path
    output_file = Path("output/csv/snomed_cleaned")

    raw = load_snomed_data(input_file)
    clean = clean_snomed_data(raw)
    save_to_formats(clean, output_file)
    logging.info("SNOMED processing completed")


if __name__ == "__main__":
    main()
