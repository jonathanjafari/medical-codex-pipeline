"""
Common utility functions used across all codex processors.
Includes save_to_formats for saving cleaned data,
and get_timestamp for adding timestamps.
"""

import pandas as pd
import logging
from datetime import datetime

def save_to_formats(df: pd.DataFrame, base_filename: str) -> None:
    """
    Save a DataFrame to CSV format.

    Args:
        df (pd.DataFrame): Cleaned data.
        base_filename (str): Path + base filename (without extension).

    Returns:
        None
    """
    try:
        df.to_csv(f"{base_filename}.csv", index=False)
        logging.info(f"Saved {base_filename}.csv")
    except Exception as e:
        logging.error(f"Error saving file: {e}")

def get_timestamp() -> str:
    """
    Get the current UTC timestamp as a string.

    Returns:
        str: Timestamp in YYYY-MM-DD HH:MM:SS format.
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
