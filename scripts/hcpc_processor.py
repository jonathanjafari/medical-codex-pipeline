# hcpcs_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from pathlib import Path
from utils.common_functions import init_logging, save_to_formats


def load_hcpcs_data(filepath: str) -> pd.DataFrame:
    """Load raw HCPCS data file."""
    return pd.read_csv(filepath, dtype=str)


def clean_hcpcs_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize HCPCS codes."""
    df = raw.rename(columns={"Code": "code", "Description1": "description"}).copy()
    df = df.dropna(subset=["code", "description"])
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    return df[["code", "description"]]


def main() -> None:
    import logging
    init_logging()

    full_path = Path("input/HCPC2025_OCT_ANWEB.csv")
    sample_path = Path("input/HCPC_sample.csv")

    # Prefer full dataset if it exists, else sample
    filepath = full_path if full_path.exists() else sample_path
    if filepath == sample_path:
        logging.info("Using HCPC sample input")

    raw = load_hcpcs_data(filepath)
    clean = clean_hcpcs_data(raw)
    save_to_formats(clean, "output/csv/hcpcs_standardized")

    logging.info("HCPC processing completed.")


if __name__ == "__main__":
    main()
