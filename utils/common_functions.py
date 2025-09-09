"""
Common utility functions for the medical codex pipeline.
These functions are shared across all processor scripts.
"""

import pandas as pd
import logging
from datetime import datetime
import re

def save_to_formats(df: pd.DataFrame, base_filename: str) -> None:
    """
    Save a DataFrame to CSV format.

    Args:
        df (pd.DataFrame): The cleaned DataFrame to save.
        base_filename (str): Path and base filename (without extension).

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
    Get the current UTC timestamp.

    Returns:
        str: Timestamp in YYYY-MM-DD HH:MM:SS format.
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def validate_code_format(code: str, pattern: str) -> bool:
    """
    Validate that a code matches the expected regex pattern.

    Args:
        code (str): The code string to validate.
        pattern (str): A regex pattern to check against.

    Returns:
        bool: True if the code matches the pattern, False otherwise.
    """
    return bool(re.match(pattern, str(code)))
