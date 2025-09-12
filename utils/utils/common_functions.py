# utils/common_functions.py
import re
from pathlib import Path
import pandas as pd
from datetime import datetime
import os


def init_logging(level=None) -> None:
    """
    Initialize logging for the project.
    Keeps everything inside the function to avoid circular import errors.
    """
    import logging

    if level is None:
        level = getattr(logging, "INFO", 20)

    try:
        logging.basicConfig(level=level, format="%(levelname)s:%(message)s")
        if not logging.getLogger().handlers:
            raise RuntimeError("no handlers after basicConfig")
    except Exception:
        root = logging.getLogger()
        root.setLevel(level)
        if not root.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
            root.addHandler(h)


def save_to_formats(df: pd.DataFrame, base_filename: str, limit: int = 100) -> None:
    """
    Save DataFrame to CSV, limiting rows to avoid huge files.

    Args:
        df: DataFrame to save
        base_filename: output path without extension
        limit: maximum rows to save (default 100)
    """
    import logging
    try:
        if limit is not None:
            # Use .copy() to avoid SettingWithCopyWarning
            df = df.head(limit).copy()

        # Add last_updated column cleanly with assign()
        df = df.assign(last_updated=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

        # Make a safe copy before adding columns (prevents SettingWithCopyWarning)
        df = df.copy()
        df["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        Path(base_filename).parent.mkdir(parents=True, exist_ok=True)
        out_path = f"{base_filename}.csv"
        print("SAVING TO:", os.path.abspath(out_path))
        df.to_csv(out_path, index=False)
        logging.info(f"Saved {out_path} with {len(df)} rows (limit={limit})")
    except Exception as e:
        logging.error(f"Error saving file: {e}")


def get_timestamp() -> str:
    """Return current UTC timestamp as 'YYYY-MM-DD HH:MM:SS'."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def validate_code_format(code: str, system: str) -> bool:
    """
    Basic code validity check.

    For now: code must be a non-empty string with only letters,
    numbers, dots, or dashes.
    """
    if not isinstance(code, str) or not code.strip():
        return False
    return bool(re.match(r"^[A-Za-z0-9.\-]+$", code.strip()))
