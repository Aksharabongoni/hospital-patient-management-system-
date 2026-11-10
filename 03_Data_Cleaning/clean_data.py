import pandas as pd
from pathlib import Path

# STEP 1: Load original dataset
folder = Path(__file__).parent

file_path = (
    folder.parent
    / "02_Data_Collection"
    / "hospital_patient_management_dataset.csv"
)

df = pd.read_csv(file_path)

print("Original Dataset Shape:", df.shape)

# STEP 2: Remove extra spaces from column names
df.columns = df.columns.str.strip()

# STEP 3: Remove unwanted spaces in text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# STEP 4: Check duplicate rows
print("\nDuplicate Rows:", df.duplicated().sum())

df = df.drop_duplicates()

# STEP 5: Check duplicate Patient IDs
print("Duplicate Patient IDs:",
      df["Patient_ID"].duplicated().sum())

# STEP 6: Convert date columns
df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"], errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"], errors="coerce"
)

# STEP 7: Convert numeric columns
numeric_columns = [
    "Age",
    "Length_of_Stay_Days",
    "Total_Bill_INR"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# STEP 8: Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# STEP 9: Check invalid values
print("\nInvalid Age:", 
      ((df["Age"] < 0) | (df["Age"] > 120)).sum())

print("Negative Bills:",
      (df["Total_Bill_INR"] < 0).sum())

# STEP 10: Check date errors
invalid_dates = (
    df["Discharge_Date"].notna() &
    (df["Discharge_Date"] < df["Admission_Date"])
)

print("Invalid Discharge Dates:", invalid_dates.sum())

# STEP 11: Check length of stay
expected_stay = (
    df["Discharge_Date"] - df["Admission_Date"]
).dt.days

stay_mismatch = (
    df["Patient_Status"].eq("Discharged") &
    df["Length_of_Stay_Days"].notna() &
    (df["Length_of_Stay_Days"] != expected_stay)
)

print("Length of Stay Mismatches:", stay_mismatch.sum())

# STEP 12: Check future discharge dates
future_discharge = (
    df["Discharge_Date"] > pd.Timestamp.today().normalize()
)

print("Future Discharge Dates:", future_discharge.sum())

# STEP 13: Save future date records for manual review
df.loc[future_discharge].to_csv(
    folder / "records_to_review.csv",
    index=False
)

# STEP 14: Save cleaned dataset
df.to_csv(
    folder / "cleaned_hospital_data.csv",
    index=False
)

# STEP 15: Generate missing values report
report = pd.DataFrame({
    "Column": df.columns,
    "Missing_Values": df.isnull().sum().values,
    "Data_Type": df.dtypes.astype(str).values
})

report.to_csv(
    folder / "data_quality_report.csv",
    index=False
)

print("\n========== CLEANING COMPLETED ==========")
print("Final Dataset Shape:", df.shape)
print("Cleaned Dataset Saved Successfully!")
print("Data Quality Report Saved Successfully!")
