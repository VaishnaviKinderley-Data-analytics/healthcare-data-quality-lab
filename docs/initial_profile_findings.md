# Initial Patient Data Profiling Findings

## 1. Objective

This document records the initial data profiling performed on synthetic patient data generated using Synthea.

The purpose is to identify potential data quality issues before using the data for healthcare analytics or dashboard development.

## 2. Dataset

* Source: Synthea-generated synthetic patient data
* File: `data/raw/patients.csv`
* Initial observed size: 13 rows and 28 columns
* Status: Exploratory sample; a controlled and reproducible generation process is still required.

## 3. Initial Observations

### Patient identifiers

No missing or duplicate patient IDs were identified in the current sample.

### Date fields

No missing or invalid birthdates were identified by the current profiling checks. Ten death dates were missing. A missing death date is not automatically a data quality error because not every patient has a recorded date of death.

No death date earlier than the corresponding birthdate was identified.

### Financial fields

No negative values were identified in healthcare expenses, healthcare coverage, or income in the current sample.

### Geographic coordinates

Latitude and longitude values were within their expected numeric ranges.

### ZIP and FIPS fields

Three ZIP values were recorded as `0`, and three FIPS values were missing. These records require investigation before any corrections are considered.

No automatic replacement or deletion has been performed.

## 4. Key Learning

Data profiling should distinguish between an actual quality failure and a value that requires further investigation. Missing values do not always indicate errors, and questionable values should not be corrected without understanding their meaning.

## 5. Next Steps

1. Generate a clean, controlled sample of synthetic patient data.
2. Separate missing-date checks from invalid-date checks.
3. Convert the main data quality rules into reusable functions.
4. Add automated tests to verify that the rules behave as expected.

## Disclaimer

This project uses synthetic data for learning and demonstration. It does not use real patient records.
