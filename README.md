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
code,description,is_valid
A00.0,Cholera due to Vibrio cholerae,True
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
├── input/            # Raw data files
│   ├── snomed_concepts.txt
│   ├── icd10cm_order_2025.csv
│   ├── icd102019syst_codes_WHO.txt
│   ├── HCPC2025_OCT_ANWEB.csv
│   ├── Loinc.csv
│   ├── npidata_pfile_20050523-20250907.csv
│   └── rxnorm_2024.txt
├── output/csv/       # Clean CSV outputs  
├── utils/            # Common functions
│   └── common_functions.py
├── logs/             # Logging folder
├── .gitignore        # Git exclusion rules
├── requirements.txt
└── README.md
```
## Updates to Project Structure & Data Handling

### Input Files

- The **full ICD-10-CM** (`icd10cm_order_2025.csv`) and **ICD-10-WHO** (`icd102019syst_codes_WHO.txt`) raw files are very large and **not committed** to GitHub (excluded via `.gitignore`).
- Instead, **sample files** are provided so reviewers can preview the structure:
  - `input/icd10cm_sample.csv` → first 100 lines of ICD-10-CM
  - `input/icd10who_sample.txt` → first 100 lines of ICD-10-WHO
  - `input/npidata_sample.csv` → first 100 lines of the NPI registry
  - `input/Loinc_sample.csv` → first 100 lines of the LOINC file
- This approach keeps the repo lightweight and GitHub-friendly, while allowing full datasets to be used locally when running the processors.

### Output Files

All processors now standardize to the same format:

```csv
code,description,last_updated
```

Outputs are saved under `output/csv/` for organization:

```
output/csv/icd10cm_standardized.csv
output/csv/icd10who_standardized.csv
output/csv/hcpcs_standardized.csv
output/csv/loinc_standardized.csv
output/csv/npi_standardized.csv
output/csv/rxnorm_standardized.csv
output/csv/snomed_standardized.csv
```

Each output is capped at **100 rows** (via `save_to_formats`) so that GitHub renders them quickly.

### Why Two ICD-10 Inputs?

- **ICD-10-CM** → U.S. version, more detailed, used for billing/reimbursement.
- **ICD-10-WHO** → international version, less granular, used for morbidity/mortality reporting.
- Both share the same core disease categories (e.g., Cholera, Typhoid), but ICD-10-CM expands into subcodes.

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

**Expected input files in `input/`:**
- `snomed_concepts.txt`
- `icd10cm_order_2025.csv`
- `icd102019syst_codes_WHO.txt`
- `HCPC2025_OCT_ANWEB.csv`
- `Loinc.csv`
- `rxnorm_2024.txt`
- `npidata_pfile_20050523-20250907.csv`

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
- Missing data dropped automatically
- Regex-based code validation

## Challenges & Solutions

**Problem:** Different file formats (CSV, semicolon-delimited, TXT)  
**Solution:** Each loader is customized for its source file format.

**Problem:** Inconsistent column names  
**Solution:** Renamed to standard `code` and `description` in all processors.

**Problem:** Large files slowing down processing  
**Solution:** Outputs automatically capped at 100 rows in `save_to_formats()` for testing.

**Problem:** Duplicate or empty rows  
**Solution:** Dropped missing and duplicate entries in every cleaner.

**Problem:** macOS command confusion  
**Solution:** All usage examples standardized with `python3`.

## Testing

Each processor can be tested individually with the sample files in `input/`.

The processors will:
- Load the raw data
- Clean and validate codes
- Output a CSV limited to 100 rows
- Log processing steps

## What I Learned

- Healthcare coding systems each have unique formats
- Pipelines benefit from shared utilities (logging, saving, validation)
- Data validation and cleaning are critical steps before integration
- Consistency across multiple scripts prevents bugs

## Assignment Requirements ✓

- [x] 7 processing scripts
- [x] Common utilities module
- [x] Standardized CSV output
- [x] Data validation & cleaning
- [x] Error handling & logging
- [x] Complete documentation
- [x] Sample outputs
- [x] requirements.txt

## Dependencies

**Required packages:**
- **pandas >= 1.5.0** – Data manipulation
- **lxml >= 4.9.0** – For XML parsing (future extension)
- **requests >= 2.28.0** – (Optional) For downloading codex files

**Standard Python libraries used:**
- **pathlib** – File paths
- **datetime** – Timestamps
- **logging** – Logging output
- **re** – Regex validation

Install with:

```bash
pip install -r requirements.txt
```

## Real-World Context

This simulates actual work at healthcare tech companies:
- EHR vendors (e.g., Epic) update SNOMED and ICD-10 regularly
- Insurers require current HCPCS codes for billing
- Clinical labs rely on LOINC for test interoperability
- RxNorm ensures medication names are standardized

---

**Note:** This is a class project with sample data. Real-world use would require licensed datasets, secure storage, and HIPAA compliance.