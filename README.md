# Medical Codex Pipeline

**Student:** Jonathan Jafari  
**Course:** HHA 507  
**Assignment:** Medical Codex Data Processing

## Overview

This project processes 7 major medical coding standards into clean, standardized CSV outputs. Healthcare companies like Epic need updated vocabularies for their systems, so this pipeline loads raw files, validates code formats, and outputs lightweight standardized CSVs.

**Medical Codexes Processed:**
- SNOMED CT (clinical terms)
- ICD-10-CM / ICD-10-WHO (diagnosis codes)
- HCPCS (procedures)
- LOINC (lab tests)
- RxNorm (medications)
- NPI (provider IDs)

## Quick Start

**Setup environment:**
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
1. Loads a data file from `input/`
2. Cleans and standardizes codes + descriptions
3. Validates codes with regex rules
4. Saves results to `output/csv/`

**Standard Output Format:**
```csv
code,description,last_updated
A00.0,Cholera due to Vibrio cholerae,2025-09-11 01:30:00
```

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
├── input/            # Sample + public data files
│   ├── snomed_sample.txt
│   ├── icd10cm_sample.csv
│   ├── icd10who_sample.txt
│   ├── HCPC2025_OCT_ANWEB.csv        # Full, public dataset
│   ├── Loinc_sample.csv
│   ├── npidata_sample.csv
│   └── rxnorm_sample.RRF
├── output/csv/       # Clean standardized outputs
├── utils/            # Common functions
│   └── common_functions.py
├── logs/
├── .gitignore
├── requirements.txt
└── README.md
```

## Input Files

- Full datasets (ICD-10-CM, ICD-10-WHO, LOINC, NPI, SNOMED CT, RxNorm) are large and/or licensed.
- These are excluded from GitHub with `.gitignore`.

**Included in the repo for testing:**
- `icd10cm_sample.csv` (100 rows)
- `icd10who_sample.txt` (100 rows)
- `npidata_sample.csv` (100 rows)
- `Loinc_sample.csv` (100 rows)
- `snomed_sample.txt` (100 rows)
- `rxnorm_sample.RRF` (100 rows)
- `HCPC2025_OCT_ANWEB.csv` (full, public HCPCS dataset)

This keeps the repo lightweight while still runnable end-to-end.

## Vocabularies: SNOMED CT & RxNorm

### SNOMED CT

- **Raw input**: Download the SNOMED CT release and place `sct2_Description_Full-en_US*.txt` into `input/`.
- **Sample input**: `input/snomed_sample.txt`
- **Processor**:
  ```bash
  python3 scripts/snomed_processor.py
  ```

### RxNorm

- **Raw input**: Download RxNorm and place `RXNCONSO.RRF` into `input/`.
- **Sample input**: `input/rxnorm_sample.RRF`
- **Processor**:
  ```bash
  python3 scripts/rxnorm_processor.py
  ```

## Outputs

All processors produce standardized CSVs under `output/csv/`:

```
output/csv/icd10cm_standardized.csv
output/csv/icd10who_standardized.csv
output/csv/hcpcs_standardized.csv
output/csv/loinc_standardized.csv
output/csv/npi_standardized.csv
output/csv/rxnorm_standardized.csv
output/csv/snomed_standardized.csv
```

Each output:
- **Columns**: `code,description,last_updated`
- **Row limit**: capped at 100 rows for readability

## Why Two ICD-10 Inputs?

- **ICD-10-CM** → U.S. version, detailed, used for billing/reimbursement.
- **ICD-10-WHO** → International version, less granular, used for public health reporting.

## Key Features

- **Validation**: Regex-based checks (e.g., ICD-10: A00.0, NPI: 10 digits).
- **Error Handling**: Logging, duplicate/missing row removal.
- **Consistency**: Shared utility functions across processors.
- **Lightweight Repo**: Large datasets excluded, samples provided.

## Challenges & Solutions

- **Large licensed datasets** → excluded from GitHub, use samples instead.
- **Mixed file formats** → handled with custom loaders.
- **Duplicate/empty rows** → dropped in cleaning functions.
- **Cross-platform differences** → standardized commands with `python3`.

## Dependencies

**Required packages:**
- **pandas >= 1.5.0** – data manipulation
- **lxml >= 4.9.0** – XML parsing (future extension)
- **requests >= 2.28.0** – optional, for file downloads

**Standard libraries:** pathlib, datetime, logging, re

Install with:
```bash
pip install -r requirements.txt
```

## Development Notes

- `.gitignore` excludes large raw datasets (e.g., NPI full >10GB, LOINC full >70MB) that exceed GitHub limits.
- Only sample inputs + HCPCS are committed.
- Repo was cleaned with `git filter-repo` to remove oversized history.

## Real-World Context

This simulates how healthcare IT teams manage vocabularies:
- EHR vendors update vocabularies regularly.
- Insurers require current HCPCS/ICD codes for billing.
- Labs use LOINC for interoperability.
- SNOMED CT + RxNorm enable decision support and medication safety.

---

**Note:** This is a class project using sample data. Real-world deployment requires licensed datasets, secure storage, and HIPAA compliance.