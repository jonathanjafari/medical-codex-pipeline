# Medical Codex Pipeline

**Student:** Jonathan Jafari  
**Course:** HHA 507  
**Assignment:** Medical Codex Data Processing

## Overview

This project processes 7 medical coding standards into clean CSV files. Healthcare companies like Epic need updated medical codes for their systems, so I built a pipeline that handles different file formats, validates the codes, and enforces consistent outputs.

**Medical Codexes Processed:**
- SNOMED CT (clinical terms)
- ICD-10-CM / ICD-10-WHO (diagnosis codes)
- HCPCS (procedures)
- LOINC (lab tests)
- RxNorm (medications)
- NPI (provider IDs)

## Quick Start

**Setup:**
```bash
git clone https://github.com/jonathanjafari/medical-codex-pipeline.git
cd medical-codex-pipeline
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Create directories:**
```bash
mkdir input output logs
mkdir output/csv
```

## How It Works

Each processor script:
1. Loads a raw data file from `input/`
2. Cleans and standardizes codes + descriptions
3. Validates codes using regex rules
4. Saves the results as a clean CSV in `output/csv/`

**Standard Output Format:**
```csv
code,description,last_updated
A00.0,Cholera due to Vibrio cholerae,2025-09-11 01:30:00
```

**Row Limit:**
All outputs are automatically capped at 100 rows via the shared `save_to_formats()` function in `utils/common_functions.py`.

## File Structure

```
medical-codex-pipeline/
├── scripts/           # 7 processor scripts
│   ├── snomed_processor.py
│   ├── icd10cm_processor.py
│   ├── icd10who_processor.py
│   ├── hcpcs_processor.py
│   ├── loinc_processor.py
│   ├── rxnorm_processor.py
│   └── npi_processor.py
├── input/            # Raw + sample data files
│   ├── sct2_Description_Full-en_US1000124_20250901.txt   # SNOMED CT full (excluded from GitHub)
│   ├── snomed_sample.txt                                # SNOMED CT sample (100 rows)
│   ├── icd10cm_order_2025.csv
│   ├── icd10cm_sample.csv
│   ├── icd102019syst_codes_WHO.txt
│   ├── icd10who_sample.txt
│   ├── HCPC2025_OCT_ANWEB.csv
│   ├── Loinc.csv
│   ├── Loinc_sample.csv
│   ├── npidata_pfile_20050523-20250907.csv
│   ├── npidata_sample.csv
│   ├── RXNCONSO.RRF                                     # RxNorm full (excluded from GitHub)
│   └── rxnorm_sample.RRF                                # RxNorm sample (100 rows)
├── output/csv/       # Clean CSV outputs  
├── utils/            # Common functions
│   └── common_functions.py
├── logs/             # Logging folder
├── .gitignore        # Git exclusion rules
├── requirements.txt
└── README.md
```

## Input Files

- Full datasets (ICD-10-CM, ICD-10-WHO, LOINC, NPI, SNOMED CT, RxNorm) are very large and require licensing.
- These are excluded from GitHub via `.gitignore` but can be used locally if downloaded.
- For demonstration, sample files (100 rows) are included in `input/`:
  - `icd10cm_sample.csv`
  - `icd10who_sample.txt`
  - `npidata_sample.csv`
  - `Loinc_sample.csv`
  - `snomed_sample.txt`
  - `rxnorm_sample.RRF`
  - `HCPC2025_OCT_ANWEB.csv` → first full file of HCPCS (publicly available, included since size is manageable)

This ensures the repository stays lightweight and GitHub-friendly, while still allowing the processors to run end-to-end.

## Vocabularies: SNOMED CT & RxNorm

### SNOMED CT

- **Raw input**: Download the latest SNOMED CT release and place the description file (e.g., `sct2_Description_Full-en_US1000124_20250901.txt`) into `input/`.
- **Sample input**: `input/snomed_sample.txt` (100 rows).
- **Processor**:
  ```bash
  python3 scripts/snomed_processor.py
  ```

### RxNorm

- **Raw input**: Download the latest RxNorm release and place `RXNCONSO.RRF` into `input/`.
- **Sample input**: `input/rxnorm_sample.RRF` (100 rows).
- **Processor**:
  ```bash
  python3 scripts/rxnorm_processor.py
  ```

### Outputs

- Standardized outputs are written to output/csv/ and included in GitHub (capped at 100 rows for readability).
- Sample inputs ensure the pipeline can be tested and verified on GitHub.

## Output Files

All processors standardize to the same format:

```csv
code,description,last_updated
```

Outputs are saved under `output/csv/`:

```
output/csv/icd10cm_standardized.csv
output/csv/icd10who_standardized.csv
output/csv/hcpcs_standardized.csv
output/csv/loinc_standardized.csv
output/csv/npi_standardized.csv
output/csv/rxnorm_standardized.csv
output/csv/snomed_standardized.csv
```

Each output is capped at **100 rows** for GitHub readability.

## Why Two ICD-10 Inputs?

- **ICD-10-CM** → U.S. version, more detailed, used for billing/reimbursement.
- **ICD-10-WHO** → international version, less granular, used for morbidity/mortality reporting.
- Both share the same disease categories, but ICD-10-CM expands into subcodes.

## Running Individual Processors

From the project root:

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
- **SNOMED:** Numeric codes (123456789)
- **ICD-10-CM/WHO:** Letter + digits (A00.0)
- **HCPCS:** Letter + 4 digits (A0021)
- **LOINC:** Digits-digits (1234-5)
- **RxNorm:** Alphanumeric drug codes
- **NPI:** 10 digits (1234567890)

### Error Handling
- Centralized logging with `init_logging()`
- Unified output saving with `save_to_formats()`
- Missing/duplicate data dropped automatically
- Regex-based code validation

## Challenges & Solutions

**Problem:** Very large, licensed datasets (SNOMED CT, RxNorm, etc.)  
**Solution:** Excluded from GitHub; sample files included for testing.

**Problem:** Different file formats (CSV, TXT, RRF)  
**Solution:** Custom loaders for each processor.

**Problem:** Inconsistent column names  
**Solution:** Renamed to standard `code` and `description`.

**Problem:** Large file performance  
**Solution:** Outputs capped at 100 rows for testing.

**Problem:** macOS vs Windows Python usage  
**Solution:** Standardized examples with `python3`.

## Testing

Processors can be tested with included sample files in `input/`. Each run will:
- Load raw data
- Clean and validate codes
- Output standardized CSV (100 rows)
- Log processing steps

## What I Learned

- Healthcare vocabularies have unique formats.
- Pipelines benefit from shared utilities (logging, validation).
- Consistency across processors prevents bugs.
- Managing large licensed datasets requires balancing local use vs. GitHub-friendly samples.

## Assignment Requirements ✓

- [x] 7 processor scripts
- [x] Common utilities module
- [x] Standardized CSV output
- [x] Data validation & cleaning
- [x] Error handling & logging
- [x] Documentation
- [x] Sample inputs included
- [x] requirements.txt

## Dependencies

**Required packages:**
- **pandas >= 1.5.0** – Data manipulation
- **lxml >= 4.9.0** – XML parsing (future extension)
- **requests >= 2.28.0** – (optional) download support

**Standard libraries:**
- pathlib, datetime, logging, re

Install with:

```bash
pip install -r requirements.txt
```

## Real-World Context

This simulates actual healthcare IT workflows:
- EHR vendors (Epic, Cerner) update vocabularies regularly.
- Insurers require current HCPCS/ICD codes for billing.
- Labs rely on LOINC for test interoperability.
- RxNorm ensures standardized medication vocabularies.
- SNOMED CT supports clinical decision support.

---

**Note:** This is a class project. Real-world use would require full licensed datasets, secure storage, and HIPAA compliance.