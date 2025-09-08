"""
This script processes RxNorm data.
It loads the raw RxNorm sample file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp

def load_rxnorm_data(filepath: str) -> pd.DataFrame:
    """Load raw RxNorm data from CSV file into a DataFrame."""
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"Loaded {len(df)} RxNorm records")
    return df

def clean_rxnorm_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean RxNorm data: keep code/description, validate format, add timestamp."""
    df = df[['RXCUI', 'STR']].copy()
    df.rename(columns={'RXCUI': 'code', 'STR': 'description'}, inplace=True)
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("No description").str.strip()
    df = df[df['code'].str.match(r"^\d+$")]
    df['last_updated'] = get_timestamp()
    return df

def main():
    """Main function for RxNorm processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/rxnorm_sample.csv")
    output_file = Path("output/csv/rxnorm_cleaned")
    raw = load_rxnorm_data(input_file)
    clean = clean_rxnorm_data(raw)
    save_to_formats(clean, output_file)

if __name__ == "__main__":
    main()
