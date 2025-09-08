"""
This script processes NPI data.
It loads the raw NPI CSV file, cleans it, validates NPI codes,
and saves the result to a standardized CSV file.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp

def load_npi_data(filepath: str) -> pd.DataFrame:
    """
    Load raw NPI data from a CSV file.

    Args:
        filepath (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the raw NPI data.
    """
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"Loaded {len(df)} NPI records")
    return df

def clean_npi_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize NPI data.

    Steps:
    - Keep only NPI and Provider Organization Name columns
    - Strip whitespace and handle missing values
    - Validate that NPI is 10 digits
    - Add last_updated timestamp

    Args:
        df (pd.DataFrame): Raw NPI data.

    Returns:
        pd.DataFrame: Cleaned NPI data.
    """
    df = df[['NPI', 'Provider Organization Name (Legal Business Name)']].copy()
    df.rename(columns={'NPI': 'code',
                       'Provider Organization Name (Legal Business Name)': 'description'}, inplace=True)
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("No description").str.strip()
    df = df[df['code'].str.match(r"^\d{10}$")]
    df['last_updated'] = get_timestamp()
    return df

def main():
    """
    Main function for running the NPI processor.
    Loads raw input, cleans it, and saves to output CSV.
    """
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/npidata_sample.csv")
    output_file = Path("output/csv/npi_cleaned")
    raw = load_npi_data(input_file)
    clean = clean_npi_data(raw)
    save_to_formats(clean, output_file)

if __name__ == "__main__":
    main()
