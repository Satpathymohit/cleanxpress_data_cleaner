import pandas as pd
import numpy as np
import re

def clean_data(df, drop_duplicates, handle_missing, format_columns, remove_outliers=False, convert_column_types=None):
    report = []
    original_shape = df.shape
    report.append(f"Original shape: {original_shape}")
    operations = []

    if drop_duplicates:
        before = df.shape[0]
        df = df.drop_duplicates()
        after = df.shape[0]
        report.append(f"Removed {before - after} duplicate rows")
        operations.append("Duplicate Removal")

    if handle_missing != "None":
        if handle_missing == "Fill with Mean":
            df = df.fillna(df.mean(numeric_only=True))
            report.append("Filled missing values with mean")
            operations.append("Missing Value Imputation (Mean)")
        elif handle_missing == "Fill with Median":
            df = df.fillna(df.median(numeric_only=True))
            report.append("Filled missing values with median")
            operations.append("Missing Value Imputation (Median)")
        elif handle_missing == "Drop Rows":
            before = df.shape[0]
            df = df.dropna()
            after = df.shape[0]
            report.append(f"Dropped {before - after} rows with missing values")
            operations.append("Missing Value Row Drop")

    if format_columns:
        df.columns = df.columns.str.strip().str.lower()
        object_cols = df.select_dtypes(include='object').columns
        for col in object_cols:
            df[col] = df[col].astype(str).str.strip().str.lower()
        report.append("Formatted columns and string values")
        operations.append("Column Formatting")

    # ✨ Outlier Removal
    if remove_outliers:
        numeric_cols = df.select_dtypes(include=np.number).columns
        before = df.shape[0]
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower) & (df[col] <= upper)]
        after = df.shape[0]
        report.append(f"Removed {before - after} outlier rows using IQR method")
        operations.append("Outlier Removal")

    # ✨ Data Type Conversion + Cleaning
    if convert_column_types:
        for col, target_type in convert_column_types.items():
            if col in df.columns:
                original_values = df[col].copy()
                try:
                    # Try to clean strings first
                    df[col] = df[col].astype(str).str.replace(r"[^\d\.\-]", "", regex=True)
                    if target_type == "int":
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
                    elif target_type == "float":
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype("Float64")
                    elif target_type == "datetime":
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    report.append(f"Converted column '{col}' to {target_type} after cleaning")
                    operations.append(f"{col} → {target_type}")
                except Exception as e:
                    report.append(f"❌ Failed to convert column '{col}' to {target_type}: {str(e)}")

    final_shape = df.shape
    report.append(f"Final shape: {final_shape}")

    improvement_ratio = (original_shape[0] - final_shape[0]) / max(original_shape[0], 1)
    score = int(100 - improvement_ratio * 100)
    report.append(f"Estimated Data Quality Score: {score}%")
    report.append(f"Operations performed: {', '.join(operations)}")

    return df, "\n".join(report)

def generate_profile(df):
    profile = []
    profile.append("Column Name | Data Type | Missing Values | Unique Values")
    profile.append("-----------------------------------------------------------")
    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = df[col].isnull().sum()
        unique = df[col].nunique()
        profile.append(f"{col} | {dtype} | {missing} | {unique}")
    return "\n".join(profile)
