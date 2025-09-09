"""
This script processes HCPCS data.
It loads the raw HCPCS codes file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path

# Ensure utils/ is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp, validate_code_format


def load_hcpcs_data(filepath: str) -> pd.DataFrame:
    """Load raw HCPCS data (pipe-delimited)."""
    df = pd.read_csv(filepath, sep="|", dtype=str)
    logging.info(f"Loaded {len(df)} HCPCS records")
    return df


def clean_hcpcs_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate HCPCS codes (Letter + 4 digits)."""
    df.columns = [c.strip().lower() for c in df.columns]
    df = df[["code", "description"]].copy()

    df["code"] = df["code"].astype(str).str.strip().str.upper()
    df["description"] = df["description"].astype(str).fillna("No description").str.strip()

    pattern = r"^[A-Z]\d{4}$"
    df = df[df["code"].apply(lambda x: validate_code_format(x, pattern))]

    df["last_updated"] = get_timestamp()
    return df


def main():
    """Run the HCPCS processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/hcpcs_codes_2024.txt")
    output_file = Path("output/csv/hcpcs_cleaned")

    raw = load_hcpcs_data(input_file)
    clean = clean_hcpcs_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()
