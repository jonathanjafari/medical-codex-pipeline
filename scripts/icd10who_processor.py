"""
This script processes ICD-10-WHO data.
It loads the raw ICD-10-WHO sample file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp

def load_icd10who_data(filepath: str) -> pd.DataFrame:
    """Load raw ICD-10-WHO data from text file into a DataFrame."""
    df = pd.read_csv(filepath, sep="\t", dtype=str)
    logging.info(f"Loaded {len(df)} ICD-10-WHO records")
    return df

def clean_icd10who_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean ICD-10-WHO data: keep code/description, validate format, add timestamp."""
    df = df[['Code', 'Description']].copy()
    df.rename(columns={'Code': 'code', 'Description': 'description'}, inplace=True)
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("No description").str.strip()
    df = df[df['code'].str.match(r"^[A-Z]\d+(\.\d+)?$")]
    df['last_updated'] = get_timestamp()
    return df

def main():
    """Main function for ICD-10-WHO processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/icd10who_sample.txt")
    output_file = Path("output/csv/icd10who_cleaned")
    raw = load_icd10who_data(input_file)
    clean = clean_icd10who_data(raw)
    save_to_formats(clean, output_file)

if __name__ == "__main__":
    main()
