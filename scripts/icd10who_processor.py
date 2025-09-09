"""
This script processes ICD-10 (WHO) data.
It loads the raw ICD-10 WHO XML file (or a delimited fallback),
cleans it, validates codes, and saves the output to CSV.
"""

import logging
import sys, os
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET

# Ensure utils/ is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp, validate_code_format


def load_icd10who_data(filepath: str) -> pd.DataFrame:
    """Load ICD-10 WHO data from XML; fallback to pipe-delimited text if needed."""
    path = Path(filepath)
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        rows = []

        # Try a few common tag combinations (keep it simple for sample files)
        for node in root.iter():
            code = None
            desc = None

            # Common possibilities
            if node.tag.lower().endswith("category") or node.tag.lower().endswith("item"):
                code_elem = node.find(".//code") or node.find(".//Code")
                desc_elem = node.find(".//description") or node.find(".//Description") or node.find(".//title")
                if code_elem is not None and code_elem.text:
                    code = code_elem.text.strip()
                if desc_elem is not None and desc_elem.text:
                    desc = desc_elem.text.strip()
                if code and desc:
                    rows.append({"code": code, "description": desc})

        df = pd.DataFrame(rows, dtype=str)
        logging.info(f"Loaded {len(df)} ICD-10 WHO records (XML)")
        if not df.empty:
            return df
        # If XML structure wasn't as expected, fallback to text
        raise ValueError("Empty or unexpected XML structure")
    except Exception:
        # Fallback: pipe-delimited file with code|description
        df = pd.read_csv(path, sep="|", dtype=str)
        logging.info(f"Loaded {len(df)} ICD-10 WHO records (pipe fallback)")
        return df


def clean_icd10who_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate ICD-10 WHO codes (same pattern as ICD-10-CM)."""
    df.columns = [c.strip().lower() for c in df.columns]
    df = df[["code", "description"]].copy()

    df["code"] = df["code"].astype(str).str.strip().str.upper()
    df["description"] = df["description"].astype(str).fillna("No description").str.strip()

    pattern = r"^[A-TV-Z][0-9]{2}(?:\.[0-9A-TV-Z]{1,4})?$"
    df = df[df["code"].apply(lambda x: validate_code_format(x, pattern))]

    df["last_updated"] = get_timestamp()
    return df


def main():
    """Run the ICD-10 WHO processor."""
    logging.basicConfig(level=logging.INFO)
    input_file = Path("input/icd10who_2024.xml")
    output_file = Path("output/csv/icd10who_cleaned")

    raw = load_icd10who_data(input_file)
    clean = clean_icd10who_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()
