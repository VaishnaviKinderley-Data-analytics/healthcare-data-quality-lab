
import pandas as pd


# ============================================================
# LOAD DATA
# ============================================================

patients = pd.read_csv("data/raw/patients.csv")

print("Patient data loaded successfully!")
print()


# ============================================================
# BASIC PROFILE
# ============================================================

print("=== BASIC PROFILE ===")
print("Rows:", len(patients))
print("Columns:", len(patients.columns))
print()


# ============================================================
# COLUMN NAMES
# ============================================================

print("=== COLUMN NAMES ===")
print(patients.columns.tolist())
print()


# ============================================================
# DATA TYPES
# ============================================================

print("=== DATA TYPES ===")
print(patients.dtypes)
print()


# ============================================================
# MISSING VALUES
# ============================================================

print("=== MISSING VALUES ===")
print(patients.isnull().sum())
print()


# ============================================================
# DUPLICATE PATIENT IDS
# ============================================================

print("=== DUPLICATE PATIENT IDS ===")
print("Duplicate IDs:", patients["Id"].duplicated().sum())
print()


# ============================================================
# UNIQUE VALUES
# ============================================================

print("=== UNIQUE VALUES ===")

print("Gender:")
print(patients["GENDER"].value_counts(dropna=False))

print()

print("Race:")
print(patients["RACE"].value_counts(dropna=False))

print()

print("Ethnicity:")
print(patients["ETHNICITY"].value_counts(dropna=False))

print()

print("Marital Status:")
print(patients["MARITAL"].value_counts(dropna=False))

print()


# ============================================================
# DATE QUALITY CHECKS
# ============================================================

print("=== DATE QUALITY CHECKS ===")

# Convert dates to datetime for validation
patients["BIRTHDATE"] = pd.to_datetime(
    patients["BIRTHDATE"],
    errors="coerce"
)

patients["DEATHDATE"] = pd.to_datetime(
    patients["DEATHDATE"],
    errors="coerce"
)

# Missing/invalid birthdates
birthdate_invalid = patients["BIRTHDATE"].isna().sum()

# Missing deathdates
deathdate_missing = patients["DEATHDATE"].isna().sum()

# Death before birth
death_before_birth = (
    patients["DEATHDATE"].notna()
    & (patients["DEATHDATE"] < patients["BIRTHDATE"])
).sum()

# Patients with deathdates
patients_with_deathdates = patients["DEATHDATE"].notna().sum()

print("Missing or invalid birthdates:", birthdate_invalid)
print("Missing deathdates:", deathdate_missing)
print("Death before birth:", death_before_birth)
print("Patients with deathdates:", patients_with_deathdates)

print()


# ============================================================
# NUMERIC QUALITY CHECKS
# ============================================================

print("=== NUMERIC QUALITY CHECKS ===")

negative_expenses = (
    patients["HEALTHCARE_EXPENSES"] < 0
).sum()

negative_coverage = (
    patients["HEALTHCARE_COVERAGE"] < 0
).sum()

negative_income = (
    patients["INCOME"] < 0
).sum()

print("Negative healthcare expenses:", negative_expenses)
print("Negative healthcare coverage:", negative_coverage)
print("Negative income:", negative_income)

print()


# ============================================================
# GEOGRAPHIC QUALITY CHECKS
# ============================================================

print("=== GEOGRAPHIC QUALITY CHECKS ===")

invalid_latitude = (
    (patients["LAT"] < -90)
    | (patients["LAT"] > 90)
).sum()

invalid_longitude = (
    (patients["LON"] < -180)
    | (patients["LON"] > 180)
).sum()

print("Invalid latitude:", invalid_latitude)
print("Invalid longitude:", invalid_longitude)

print()


# ============================================================
# CODE QUALITY CHECKS
# ============================================================

print("=== CODE QUALITY CHECKS ===")

print("Unique ZIP codes:")
print(patients["ZIP"].value_counts(dropna=False))

print()

print("Unique FIPS codes:")
print(patients["FIPS"].value_counts(dropna=False))

print()


# ============================================================
# ZIP AND FIPS INVESTIGATION
# ============================================================

print("=== ZIP AND FIPS INVESTIGATION ===")

print("Records with ZIP = 0:")
print(
    patients.loc[
        patients["ZIP"] == 0,
        ["Id", "CITY", "STATE", "COUNTY", "FIPS", "ZIP"]
    ]
)

print()

print("Records with missing FIPS:")
print(
    patients.loc[
        patients["FIPS"].isna(),
        ["Id", "CITY", "STATE", "COUNTY", "FIPS", "ZIP"]
    ]
)

print()


# ============================================================
# AUTOMATED DATA QUALITY RESULTS
# ============================================================

print("========================================")
print("       DATA QUALITY RESULTS")
print("========================================")


# ------------------------------------------------------------
# DQ001 - Patient ID
# Patient ID must not be missing or duplicated.
# ------------------------------------------------------------

dq001_failed = (
    patients["Id"].isna().sum()
    + patients["Id"].duplicated().sum()
)

print()
print("DQ001 - Patient ID uniqueness")
print("Failed rows:", dq001_failed)


# ------------------------------------------------------------
# DQ002 - Birthdate
# Birthdate must be present and valid.
# ------------------------------------------------------------

dq002_failed = patients["BIRTHDATE"].isna().sum()

print()
print("DQ002 - Birthdate validity")
print("Failed rows:", dq002_failed)


# ------------------------------------------------------------
# DQ003 - Deathdate
# Deathdate must not occur before birthdate.
# Missing deathdates are allowed.
# ------------------------------------------------------------

dq003_failed = (
    patients["DEATHDATE"].notna()
    & (patients["DEATHDATE"] < patients["BIRTHDATE"])
).sum()

print()
print("DQ003 - Deathdate after birthdate")
print("Failed rows:", dq003_failed)


# ------------------------------------------------------------
# DQ004 - Gender
# Gender must contain an approved value.
# ------------------------------------------------------------

allowed_gender = {"F", "M"}

dq004_failed = (
    ~patients["GENDER"].isin(allowed_gender)
).sum()

print()
print("DQ004 - Valid gender values")
print("Failed rows:", dq004_failed)


# ------------------------------------------------------------
# DQ007 - Healthcare expenses
# Healthcare expenses must not be negative.
# ------------------------------------------------------------

dq007_failed = (
    patients["HEALTHCARE_EXPENSES"] < 0
).sum()

print()
print("DQ007 - Non-negative healthcare expenses")
print("Failed rows:", dq007_failed)


# ------------------------------------------------------------
# DQ008 - Healthcare coverage
# Healthcare coverage must not be negative.
# ------------------------------------------------------------

dq008_failed = (
    patients["HEALTHCARE_COVERAGE"] < 0
).sum()

print()
print("DQ008 - Non-negative healthcare coverage")
print("Failed rows:", dq008_failed)


# ------------------------------------------------------------
# DQ009 - Income
# Income must not be negative.
# ------------------------------------------------------------

dq009_failed = (
    patients["INCOME"] < 0
).sum()

print()
print("DQ009 - Non-negative income")
print("Failed rows:", dq009_failed)


# ------------------------------------------------------------
# DQ010 - Latitude
# Latitude must be between -90 and 90.
# ------------------------------------------------------------

dq010_failed = (
    (patients["LAT"] < -90)
    | (patients["LAT"] > 90)
).sum()

print()
print("DQ010 - Valid latitude")
print("Failed rows:", dq010_failed)


# ------------------------------------------------------------
# DQ011 - Longitude
# Longitude must be between -180 and 180.
# ------------------------------------------------------------

dq011_failed = (
    (patients["LON"] < -180)
    | (patients["LON"] > 180)
).sum()

print()
print("DQ011 - Valid longitude")
print("Failed rows:", dq011_failed)


# ------------------------------------------------------------
# DQ012 - ZIP
# ZIP = 0 is treated as a warning rather than an automatic failure.
# ------------------------------------------------------------

dq012_warning = (
    patients["ZIP"] == 0
).sum()

print()
print("DQ012 - ZIP placeholder values")
print("Warning rows:", dq012_warning)


# ------------------------------------------------------------
# DQ013 - FIPS
# Missing FIPS values are reported as warnings.
# ------------------------------------------------------------

dq013_warning = (
    patients["FIPS"].isna()
).sum()

print()
print("DQ013 - Missing FIPS")
print("Warning rows:", dq013_warning)


# ============================================================
# END
# ============================================================

print()
print("========================================")
print("       PROFILING COMPLETE")
print("========================================")
