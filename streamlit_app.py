import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pdfplumber import open as open_pdf
from openpyxl import load_workbook

def read_file(file):
    try:
        if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            # Read Excel file
            wb = load_workbook(file)
            sheet = wb.active
            df = pd.DataFrame(sheet.values)
            return df
        elif file.type == "application/pdf":
            # Read PDF file
            with open_pdf(file) as pdf:
                page = pdf.pages[0]
                text = page.extract_text()
                df = pd.DataFrame([x.split() for x in text.split('\n')])
                return df
        else:
        def read_file(file):
    try:
        # Read CSV file
        df = pd.read_csv(file, error_bad_lines=False)
        return df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def exploratory_data_analysis(df):
    st.write("Exploratory Data Analysis")
    st.write(df.head())
    st.write(df.info())
    st.write(df.describe())

def calculate_kpis(df):
    kpis = {}
    if 'Revenue' in df.columns and 'Net Income' in df.columns and 'Cost of Goods Sold' in df.columns:
        kpis['Revenue'] = df['Revenue'].sum()
        kpis['Net Income'] = df['Net Income'].sum()
        if df['Revenue'].sum() != 0:
            kpis['Gross Margin'] = (df['Revenue'] - df['Cost of Goods Sold']).sum() / df['Revenue'].sum()
        else:
            kpis['Gross Margin'] = 0
    return kpis

def create_visualizations(df):
    st.write("Visualizations")
    if 'Category' in df.columns and 'Amount' in df.columns:
        fig, ax = plt.subplots()
        sns.barplot(x='Category', y='Amount', data=df)
        st.pyplot(fig)
    else:
        st.write("Error: The DataFrame must contain 'Category' and 'Amount' columns for visualization.")

def main():
    st.title("Financial Statement Analyzer")
    file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls", "pdf"])
    if file is not None:
        df = read_file(file)
        if df is not None:
            exploratory_data_analysis(df)
            kpis = calculate_kpis(df)
            st.write("Key Performance Indicators (KPIs)")
            st.write(kpis)
            create_visualizations(df)

if __name__ == "__main__":
    main()
