# hcpcs_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from pathlib import Path
from utils.common_functions import init_logging, validate_code_format, save_to_formats


# File paths
INPUT_FILE = "input/HCPC2025_OCT_ANWEB.csv"

# Public dataset URL (CMS official site)
HCPCS_URL = "https://www.cms.gov/medicare/coding-billing/HCPCSReleaseCodeSets/Downloads/HCPC2025_OCT_ANWEB.csv"


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
    df = df[["code", "description"]]
    return df


def main() -> None:
    import logging
    init_logging()

    # Auto-download if missing
    if not Path(INPUT_FILE).exists():
        logging.info("HCPCS file not found locally, downloading...")
        try:
            download_file(HCPCS_URL, INPUT_FILE)
            logging.info("HCPCS dataset downloaded successfully.")
        except Exception as e:
            logging.error(f"Failed to download HCPCS dataset: {e}")
            return

    try:
        raw = load_hcpcs_data(INPUT_FILE)
        clean = clean_hcpcs_data(raw)
        save_to_formats(clean, "output/csv/hcpcs_standardized")
        logging.info("HCPCS processing completed successfully.")
    except Exception as e:
        logging.error(f"Error processing HCPCS data: {e}")


if __name__ == "__main__":
    main()
