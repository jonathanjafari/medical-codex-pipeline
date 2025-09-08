"""
This script processes LOINC data.
It loads the raw LOINC sample file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp

def load_loinc_data(filepath: str) -> pd.DataFrame:
    """Load raw LOINC data from CSV file into a DataFrame."""
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"Loaded {len(df)} LOINC records")
    return df

def clean_loinc_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean LOINC data: keep code/description, validate format, add timestamp."""
    df = df[['LOINC_NUM', 'LONG_COMMON_NAME']].copy()
    df.rename(columns={'LOINC_NUM': 'code', 'LONG_COMMON_NAME': 'description'}, inplace=True)
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("No description").str.strip()
    df = df[df['code'].str.match(r"^\d+-\d$")]
    df['last_updated'] = get_timestamp()
    return df

def main():
    """Main function for LOINC processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/loinc_sample.csv")
    output_file = Path("output/csv/loinc_cleaned")
    raw = load_loinc_data(input_file)
    clean = clean_loinc_data(raw)
    save_to_formats(clean, output_file)

if __name__ == "__main__":
    main()
