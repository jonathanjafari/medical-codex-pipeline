# Medical Codex Pipeline

**Student:** Jonathan Jafari  
**Course:** HHA 507  
**Assignment:** Medical Codex Data Processing

## Overview

This project processes 7 medical coding standards into clean CSV files. Healthcare companies like Epic need updated medical codes for their systems, so I built a pipeline that handles different file formats and validates the codes.

**Medical Codexes Processed:**
- SNOMED CT (clinical terms)
- ICD-10-CM/WHO (diagnosis codes) 
- HCPCS (procedures)
- LOINC (lab tests)
- RxNorm (medications)
- NPI (provider IDs)

## Quick Start

```bash
# Setup
git clone https://github.com/jonathanjafari/medical-codex-pipeline.git
cd medical-codex-pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create directories
mkdir input output logs
mkdir output/csv

# Run demo with test data
python test_runner.py
```

## How It Works

Each processor script:
1. Loads raw data file from `input/`
2. Validates codes using regex patterns
3. Cleans and standardizes data
4. Saves to CSV in `output/csv/`

**Standard Output Format:**
```csv
code,description,last_updated
A00.0,Cholera due to Vibrio cholerae,2024-09-08 14:30:00
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
├── input/            # Raw data files
├── output/csv/       # Clean CSV outputs  
├── utils/            # Common functions
│   └── common_functions.py
├── logs/             # Processing logs
├── test_runner.py    # Demo script
├── requirements.txt
└── README.md
```

## Running Individual Processors

```bash
python scripts/snomed_processor.py
python scripts/icd10cm_processor.py
python scripts/icd10who_processor.py
python scripts/hcpcs_processor.py
python scripts/loinc_processor.py
python scripts/rxnorm_processor.py
python scripts/npi_processor.py
```

**Expected input files in `input/`:**
- `snomed_concepts.txt`
- `icd10cm_codes_2024.txt` 
- `icd10who_2024.xml`
- `hcpcs_codes_2024.txt`
- `loinc_2024.csv`
- `rxnorm_2024.txt`
- `npi_registry_2024.csv`

## Key Features

### Data Validation
- **SNOMED:** Numeric codes (123456789)
- **ICD-10:** Letter + digits (A00.0)
- **HCPCS:** Letter + 4 digits (A0021)
- **LOINC:** Digits-digits (1234-5)
- **NPI:** 10 digits (1234567890)

### Error Handling
- Logs all processing steps
- Validates file formats
- Handles missing data
- Reports data quality issues

## Challenges & Solutions

**Problem:** Different file formats (tab, pipe, XML)  
**Solution:** Custom loader for each codex type

**Problem:** Huge files crash my computer  
**Solution:** Process in chunks with pandas

**Problem:** No real test data  
**Solution:** Built fake data generator

## Testing

The `test_runner.py` creates sample data and runs the full pipeline:
- Generates realistic test files
- Processes all 7 codexes
- Validates output format
- Shows processing summary

## What I Learned

- Real healthcare data is messy and needs lots of validation
- Each medical coding system has specific format rules
- ETL pipelines need robust error handling
- Regex is essential for data validation
- Good logging saves time when debugging

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

This project requires the following Python packages:

```
pandas>=1.5.0  
requests>=2.28.0  
lxml>=4.9.0  
```

Install them with:

```bash
pip install -r requirements.txt
```

## Real-World Context

This simulates actual work at healthcare tech companies:
- Epic updates SNOMED codes for clinical documentation
- Insurance companies need current procedure codes for billing
- EHR systems require validated terminology databases

---

**Note:** Class project using simulated data. Real healthcare applications require proper licensing and HIPAA compliance.