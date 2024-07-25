import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pdfplumber import open as open_pdf
from openpyxl import load_workbook

# Function to read file
def read_file(file):
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
        # Read CSV file
        df = pd.read_csv(file)
        return df

# Function to perform exploratory data analysis
def exploratory_data_analysis(df):
    st.write("Exploratory Data Analysis")
    st.write(df.head())
    st.write(df.info())
    st.write(df.describe())

# Function to calculate key performance indicators (KPIs)
def calculate_kpis(df):
    kpis = {}
    kpis['Revenue'] = df['Revenue'].sum()
    kpis['Net Income'] = df['Net Income'].sum()
    kpis['Gross Margin'] = (df['Revenue'] - df['Cost of Goods Sold']).sum() / df['Revenue'].sum()
    return kpis

# Function to create visualizations
def create_visualizations(df):
    st.write("Visualizations")
    fig, ax = plt.subplots()
    sns.barplot(x='Category', y='Amount', data=df)
    st.pyplot(fig)

# Main function
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
