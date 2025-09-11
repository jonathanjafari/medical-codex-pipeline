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
1. Loads a data file from `input/` (local only, ignored by GitHub)
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
├── input/             # Raw datasets (local only, ignored in Git)
│   └── (place full vocabularies here before running)
├── output/csv/        # Clean standardized outputs
├── utils/             # Common functions
│   └── common_functions.py
├── logs/
├── .gitignore
├── requirements.txt
└── README.md
```

## Input Files

Full datasets (ICD-10-CM, ICD-10-WHO, LOINC, NPI, SNOMED CT, RxNorm, HCPCS) are large and/or licensed.

These are excluded from GitHub with `.gitignore`.

**To run processors locally, place the raw files into `input/`:**
- `icd10cm_order_2025.csv`
- `icd102019syst_codes_WHO.txt`
- `Loinc.csv`
- `npidata_pfile_20050523-20250907.csv`
- `RXNCONSO.RRF`
- `sct2_Description_Full-en_US*.txt`
- `HCPC2025_OCT_ANWEB.csv`

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
- **Lightweight Repo**: Large datasets excluded, only outputs and code tracked.

## Challenges & Solutions

- **Large licensed datasets** → excluded from GitHub, used locally only.
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

- `.gitignore` excludes all raw input datasets (e.g., NPI full >10GB, LOINC full >70MB).
- Only processor scripts, utilities, outputs, and documentation are committed.
- This keeps the repo clean, lightweight, and runnable with local data.

## Real-World Context

This simulates how healthcare IT teams manage vocabularies:
- EHR vendors update vocabularies regularly.
- Insurers require current HCPCS/ICD codes for billing.
- Labs use LOINC for interoperability.
- SNOMED CT + RxNorm enable decision support and medication safety.

---

**Note:** This is a class project using local raw data. Real-world deployment requires licensed datasets, secure storage, and HIPAA compliance.