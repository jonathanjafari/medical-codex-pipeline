"""
This script processes HCPCS data.
It loads the raw HCPCS sample file, cleans it, validates codes,
and saves the output to a standardized CSV format.
"""

import pandas as pd
import logging
import sys, os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp

def load_hcpcs_data(filepath: str) -> pd.DataFrame:
    """Load raw HCPCS data from text file into a DataFrame."""
    df = pd.read_csv(filepath, sep="\t", dtype=str)
    logging.info(f"Loaded {len(df)} HCPCS records")
    return df

def clean_hcpcs_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean HCPCS data: keep code/description, validate format, add timestamp."""
    df = df[['HCPCS', 'Description']].copy()
    df.rename(columns={'HCPCS': 'code', 'Description': 'description'}, inplace=True)
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("No description").str.strip()
    df = df[df['code'].str.match(r"^[A-Z]\d{4}$")]
    df['last_updated'] = get_timestamp()
    return df

def main():
    """Main function for HCPCS processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/hcpcs_sample.txt")
    output_file = Path("output/csv/hcpcs_cleaned")
    raw = load_hcpcs_data(input_file)
    clean = clean_hcpcs_data(raw)
    save_to_formats(clean, output_file)

if __name__ == "__main__":
    main()
