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
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create directories
mkdir input output logs
mkdir output/csv
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
│   ├── snomed_sample.csv
│   ├── icd10cm_sample.txt
│   ├── icd10who_sample.txt
│   ├── hcpcs_sample.txt
│   ├── loinc_sample.csv
│   ├── npidata_sample.csv
│   └── rxnorm_sample.csv
├── output/csv/       # Clean CSV outputs  
├── utils/            # Common functions
│   └── common_functions.py
├── logs/             # Empty folder for logging (with .gitkeep)
├── .gitignore        # Git exclusion rules
├── requirements.txt
└── README.md
```

## Data Handling & Version Control

The `.gitignore` file excludes sensitive and temporary files from version control:

```gitignore
# Raw data files (exclude large medical datasets)
input/
*.txt
*.xml
*.zip
raw_downloads/

# Python cache and build files
__pycache__/
*.pyc
*.pyo
.env
venv/

# IDE and system files
.vscode/
.idea/
.DS_Store

# Log files
logs/
*.log
```

This ensures that:
- Large raw medical data files aren't committed to Git
- Personal environment files remain private
- Only the processed outputs and code are version controlled

## Running Individual Processors

```bash
python3 scripts/snomed_processor.py
python3 scripts/icd10cm_processor.py
python3 scripts/icd10who_processor.py
python3 scripts/hcpcs_processor.py
python3 scripts/loinc_processor.py
python3 scripts/rxnorm_processor.py --input input/rxnorm_2024.txt --out output/csv/rxnorm_cleaned
python3 scripts/npi_processor.py
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

**Problem:** Different file formats (CSV, tab, pipe, XML)  
**Solution:** Wrote flexible loaders with auto-delimiter detection and XML parsing support.

**Problem:** Inconsistent column names across datasets  
**Solution:** Added a header normalization step and alias mapping so all outputs follow `code, description, last_updated`.

**Problem:** Empty or double `.csv.csv` outputs  
**Solution:** Fixed output path handling by omitting the `.csv` extension when using the shared `save_to_formats()` utility.

**Problem:** Huge files crashing my computer  
**Solution:** Tested on smaller sample files and structured code to support chunked processing with pandas.

**Problem:** No real test data  
**Solution:** Created synthetic "sample" files in `input/` so each processor can be verified quickly.

**Problem:** Confusion running commands on macOS  
**Solution:** Standardized all usage examples to use `python3` instead of `python`.

## Testing

Each processor can be tested individually with the sample data files provided in the `input/` directory. The processors will:
- Load the sample data
- Process and validate codes according to each codex's format rules
- Generate clean CSV output files
- Log processing information

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

- **pandas >= 1.5.0** – Data manipulation and cleaning
- **requests >= 2.28.0** – (Optional) For future extension, e.g., downloading codex files directly from official sources
- **lxml >= 4.9.0** – XML parsing support (useful for ICD-10-WHO and other XML-based codexes)

It also uses standard Python libraries (included with Python, no need to install):
- **pathlib** – File and path handling
- **datetime** – Used to generate timestamps
- **logging** – Tracks processing steps and errors

You can install all dependencies with:

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