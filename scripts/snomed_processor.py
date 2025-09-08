"""
This script processes SNOMED data.
It loads the raw SNOMED sample file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp

def load_snomed_data(filepath: str) -> pd.DataFrame:
    """
    Load raw SNOMED data from a CSV file.

    Args:
        filepath (str): Path to SNOMED sample CSV file.

    Returns:
        pd.DataFrame: DataFrame with SNOMED data.
    """
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"Loaded {len(df)} SNOMED records")
    return df

def clean_snomed_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize SNOMED data.

    Steps:
    - Keep only code and description columns
    - Remove extra whitespace
    - Validate that codes are numeric
    - Add last_updated timestamp
    """
    df = df[['ConceptId', 'Term']].copy()
    df.rename(columns={'ConceptId': 'code', 'Term': 'description'}, inplace=True)
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("No description").str.strip()
    df = df[df['code'].str.match(r"^\d+$")]
    df['last_updated'] = get_timestamp()
    return df

def main():
    """Main function to load, clean, and save SNOMED data."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/snomed_sample.csv")
    output_file = Path("output/csv/snomed_cleaned")
    raw = load_snomed_data(input_file)
    clean = clean_snomed_data(raw)
    save_to_formats(clean, output_file)

if __name__ == "__main__":
    main()
