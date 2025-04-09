# app.py

import streamlit as st
import pandas as pd
from cleaner import clean_data, generate_profile
from io import BytesIO

st.set_page_config(page_title="CleanXpress", layout="wide")
st.title("🧼 CleanXpress – Smart & Simple Data Cleaner")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Raw Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Data Profile")
    profile = generate_profile(df)
    st.text(profile)

    st.markdown("---")
    st.subheader("🧠 Select Cleaning Operations")

    drop_duplicates = st.checkbox("Remove Duplicates")
    handle_missing = st.selectbox("Handle Missing Values", ["None", "Fill with Mean", "Fill with Median", "Drop Rows"])
    format_columns = st.checkbox("Fix Column Formatting (Trim & Lowercase)")
    remove_outliers = st.checkbox("Remove Outliers (IQR Method)")

    st.markdown("---")
    st.subheader("🧬 Data Type Conversion")

    convert_column_types = {}
    columns_to_convert = st.multiselect("Select columns to convert", df.columns)

    for col in columns_to_convert:
        col_type = st.selectbox(f"Convert '{col}' to:", ["int", "float", "datetime"], key=col)
        convert_column_types[col] = col_type

    if st.button("🚀 Clean My Data"):
        cleaned_df, report = clean_data(
            df,
            drop_duplicates=drop_duplicates,
            handle_missing=handle_missing,
            format_columns=format_columns,
            remove_outliers=remove_outliers,
            convert_column_types=convert_column_types
        )

        st.success("✅ Data cleaned successfully!")

        st.subheader("📈 Summary")
        original_shape = df.shape
        cleaned_shape = cleaned_df.shape
        st.markdown(f"**Rows:** {original_shape[0]} → {cleaned_shape[0]}  |  **Columns:** {original_shape[1]}")
        st.text(report)

        st.subheader("🧾 Cleaned Data Preview")
        st.dataframe(cleaned_df.head())

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=cleaned_df.to_csv(index=False).encode('utf-8'),
            file_name="cleaned_data.csv",
            mime='text/csv'
        )

        st.download_button(
            label="📄 Download Report",
            data=report.encode('utf-8'),
            file_name="cleaning_report.txt",
            mime='text/plain'
        )
