import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Create sample hospital dataset
data = {
    "Patient_ID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "Age": [25, 32, 45, 29, 51, 37, 60, 22, 48, 34],
    "Gender": [
        "Male", "Female", "Male", "Female", "Male",
        "Female", "Male", "Female", "Male", "Female"
    ],
    "Department": [
        "Cardiology", "Neurology", "Orthopedics", "Cardiology",
        "Pediatrics", "Neurology", "Orthopedics", "Pediatrics",
        "Cardiology", "Neurology"
    ],
    "Status": [
        "Admitted", "Discharged", "Admitted", "Discharged",
        "Admitted", "Admitted", "Discharged", "Admitted",
        "Discharged", "Admitted"
    ],
    "Admission_Date": [
        "2026-01-05", "2026-01-10", "2026-02-12",
        "2026-02-18", "2026-03-02", "2026-03-15",
        "2026-04-04", "2026-04-19", "2026-05-08",
        "2026-05-20"
    ]
}

df = pd.DataFrame(data)

# 2. Save dataset
df.to_csv("hospital_data.csv", index=False)

print("\n===== HOSPITAL DATA ANALYSIS =====")

# 3. Display dataset
print("\nHospital Dataset:")
print(df)

print("\nDataset Shape (Rows, Columns):")
print(df.shape)

# 4. Basic statistical analysis
print("\nStatistical Summary:")
print(df.describe(include="all"))

print("\nAverage Patient Age:")
print(round(df["Age"].mean(), 2))

print("\nMinimum Patient Age:")
print(df["Age"].min())

print("\nMaximum Patient Age:")
print(df["Age"].max())

# 5. Data quality analysis
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

# 6. Gender analysis
print("\nPatients by Gender:")
print(df["Gender"].value_counts())

# 7. Department analysis
print("\nPatients by Department:")
print(df["Department"].value_counts())

# 8. Patient status analysis
print("\nPatient Status:")
print(df["Status"].value_counts())

# 9. Monthly admission analysis
df["Admission_Date"] = pd.to_datetime(df["Admission_Date"])
df["Month"] = df["Admission_Date"].dt.strftime("%b")

print("\nMonthly Admissions:")
print(df.groupby("Month")["Patient_ID"].count())

# 10. Visualize department-wise patients
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Department")
plt.title("Department-wise Patient Distribution")
plt.xlabel("Department")
plt.ylabel("Number of Patients")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("department_analysis.png")
plt.show()

# 11. Visualize gender distribution
plt.figure(figsize=(6, 5))
df["Gender"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Gender Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("gender_analysis.png")
plt.show()

# 12. Visualize monthly admissions
monthly = df.groupby("Month")["Patient_ID"].count()

plt.figure(figsize=(8, 5))
monthly.plot(kind="bar", color="steelblue")
plt.title("Monthly Hospital Admissions")
plt.xlabel("Month")
plt.ylabel("Number of Admissions")
plt.tight_layout()
plt.savefig("monthly_admissions.png")
plt.show()

# 13. Analyze patient age distribution
plt.figure(figsize=(8, 5))
plt.hist(df["Age"], bins=5, edgecolor="black")
plt.title("Patient Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("age_distribution.png")
plt.show()

# 14. Export analysis summary
summary = {
    "Total Patients": len(df),
    "Average Age": round(df["Age"].mean(), 2),
    "Total Departments": df["Department"].nunique(),
    "Admitted Patients": int((df["Status"] == "Admitted").sum()),
    "Discharged Patients": int((df["Status"] == "Discharged").sum()),
    "Missing Values": int(df.isnull().sum().sum()),
    "Duplicate Records": int(df.duplicated().sum())
}

summary_df = pd.DataFrame([summary])
summary_df.to_csv("analysis_summary.csv", index=False)

print("\nAnalysis Summary:")
print(summary_df.to_string(index=False))

print("\nData analysis completed successfully!")
print("Generated: hospital_data.csv")
print("Generated: analysis_summary.csv")
print("Generated: department_analysis.png")
print("Generated: gender_analysis.png")
print("Generated: monthly_admissions.png")
print("Generated: age_distribution.png")