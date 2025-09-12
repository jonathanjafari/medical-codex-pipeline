# Medical Codex Pipeline

**Student:** Jonathan Jafari  
**Course:** HHA 507  
**Assignment:** Medical Codex Data Processing

## Overview

This project processes 7 medical coding standards into clean CSV files. Healthcare companies like Epic need updated vocabularies for their systems, so I built a pipeline that handles different file formats, validates the codes, enforces consistent outputs, and includes logging and error handling for robustness.

### Medical Codexes Processed:

- **SNOMED CT** (clinical terms)
- **ICD-10-CM / ICD-10-WHO** (diagnosis codes)
- **HCPCS** (procedures)
- **LOINC** (lab tests)
- **RxNorm** (medications)
- **NPI** (provider IDs)

## Quick Start

### Setup:

```bash
git clone https://github.com/jonathanjafari/medical-codex-pipeline.git
cd medical-codex-pipeline
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Create directories:

```bash
mkdir input output logs
mkdir output/csv
```

## How It Works

Each processor script:

1. Loads a raw data file from `input/`
2. Cleans and standardizes codes + descriptions
3. Validates codes with regex rules
4. Saves results to `output/csv/`

### Standard Output Format:

```csv
code,description,last_updated
A00.0,Cholera due to Vibrio cholerae,2025-09-11 01:30:00
code,description,last_updated
A00.0,Cholera due to Vibrio cholerae,2025-09-11 01:30:00
```

### Row Limit:
All outputs are capped at 100 rows using the shared `save_to_formats()` function in `utils/common_functions.py`.

## File Structure

```
medical-codex-pipeline/
├── scripts/            # 7 processor scripts
│   ├── snomed_processor.py
│   ├── icd10cm_processor.py
│   ├── icd10who_processor.py
│   ├── hcpcs_processor.py
│   ├── loinc_processor.py
│   ├── rxnorm_processor.py
│   └── npi_processor.py
├── output/csv/         # Standardized CSV outputs (capped at 100 rows)
│   ├── hcpcs_standardized.csv
│   ├── icd10cm_standardized.csv
│   ├── icd10who_standardized.csv
│   ├── loinc_standardized.csv
│   ├── npi_standardized.csv
│   ├── rxnorm_standardized.csv
│   └── snomed_standardized.csv
├── utils/              # Shared helper functions
│   └── common_functions.py
├── .gitignore
├── requirements.txt
└── README.md
```
⚠️ Input datasets are not included in this repository (due to licensing and size). To run processors locally, place raw datasets into an input/ folder at the project root.

## Input Files

Expected input files in `input/` (local only):

- `sct2_Description_Full-en_US1000124_20250901.txt` → SNOMED CT (requires UMLS license)  
- `icd10cm_order_2025.csv` → ICD-10-CM  
- `icd102019syst_codes_WHO.txt` → ICD-10-WHO  
- `HCPC2025_OCT_ANWEB.csv` → HCPCS (public dataset)  
- `Loinc.csv` → LOINC  
- `RXNCONSO.RRF` → RxNorm (requires UMLS license)  
- `npidata_pfile_20050523-20250907.csv` → NPI (public dataset, very large)  

⚠️ **Note**: These full datasets are **excluded from GitHub** with `.gitignore` to avoid size and licensing issues.  
They must be placed in a local `input/` folder before running the processors.

## Output Files

All processors standardize to the same format:

```csv
code,description,last_updated
```

Outputs are saved under `output/csv/`:

- `output/csv/icd10cm_standardized.csv`
- `output/csv/icd10who_standardized.csv`
- `output/csv/hcpcs_standardized.csv`
- `output/csv/loinc_standardized.csv`
- `output/csv/npi_standardized.csv`
- `output/csv/rxnorm_standardized.csv`
- `output/csv/snomed_standardized.csv`

Each output is capped at 100 rows for readability and GitHub rendering.

## Running Individual Processors

Run any processor from the project root:

```bash
python3 scripts/snomed_processor.py
python3 scripts/icd10cm_processor.py
python3 scripts/icd10who_processor.py
python3 scripts/hcpcs_processor.py
python3 scripts/loinc_processor.py
python3 scripts/rxnorm_processor.py
python3 scripts/npi_processor.py
```

## Key Features

### Data Validation

- **SNOMED CT:** Numeric identifiers
- **ICD-10-CM/WHO:** Alphanumeric with optional decimal (e.g., A00.0)
- **HCPCS:** Letter + 4 digits (A0021)
- **LOINC:** Digits-dash-digits (1234-5)
- **RxNorm:** RXCUI numeric identifiers
- **NPI:** 10 digits (1234567890)

### Error Handling & Logging

- Centralized logging with `init_logging()`
- Robust try/except in each processor's `main()`
- Errors logged as `ERROR:` instead of silent failures
- `save_to_formats()` ensures outputs always include `last_updated`

## Challenges & Solutions

**Problem:** Different file formats (CSV, TXT, semicolon-delimited, RRF)  
**Solution:** Custom loaders for each source type.

**Problem:** Inconsistent column names  
**Solution:** Renamed all to `code` and `description`.

**Problem:** Large licensed datasets (SNOMED CT, RxNorm)  
**Solution:** Use official files locally and exclude them from GitHub via `.gitignore`

**Problem:** Duplicate or empty rows  
**Solution:** Removed with `.dropna()` and `.drop_duplicates()`.

**Problem:** macOS/Linux command differences  
**Solution:** Usage examples standardized with `python3`.

## Assignment Requirements ✓

- ✅ 7 processing scripts
- ✅ Common utilities module
- ✅ Standardized CSV outputs
- ✅ Data validation & cleaning
- ✅ Error handling & logging
- ✅ Full dataset support with lightweight standardized outputs
- ✅ Complete documentation
- ✅ requirements.txt

## Dependencies

### Required packages (see `requirements.txt`):

- **pandas** – Data manipulation
- **polars** – Fast DataFrame library (alternative to pandas)
- **numpy** – Numerical computing
- **scipy** – Scientific computing utilities
- **matplotlib** – Plotting and visualization
- **sqlalchemy** – Database connectivity
- **requests** – Optional, for auto-downloads

### Standard libraries used:

pathlib, datetime, logging, re, os

Install with:

```bash
pip install -r requirements.txt

### Standard libraries used:

pathlib, datetime, logging, re, os

Install with:
```bash
pip install -r requirements.txt
```

## Development Notes

- `.gitignore` excludes all raw input datasets (e.g., NPI full >10GB, LOINC full >70MB).
- Only processor scripts, utilities, outputs, and documentation are committed.
- This keeps the repo clean, lightweight, and runnable with local data.

## Real-World Context

This simulates how healthcare IT manages vocabularies:

- EHR vendors (Epic, Cerner) update SNOMED & ICD regularly
- Insurers require HCPCS/ICD for billing
- Labs use LOINC for test interoperability
- RxNorm ensures medication names are standardized
- NPI validates provider identifiers

**Note:** This is a class project using full datasets locally. Real-world deployment requires licensed datasets, secure storage, and HIPAA compliance.