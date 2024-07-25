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
            try:
                # Read CSV file
                df = pd.read_csv(file)
                return df
            except pd.errors.ParserError as e:
                st.error(f"Error reading file: {e}")
                return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def display_financial_statement(df):
    st.write("Financial Statement")
    st.write("******************")

    # Create tabs for each financial statement
    tabs = ["Income Statement", "Expenditure Statement", "Balance Sheet", "Cash Flow Statement"]
    tab_contents = [
        df.loc[:, ['Total Income', 'Operating Profit', 'Reported Net Profit']],
        df.loc[:, ['Total Expenditure', 'Employee Cost', 'Depreciation']],
        df.loc[:, ['Total Assets', 'Total Liabilities', 'Total Equity']],
        df.loc[:, ['Net Cash from Operations', 'Net Cash from Investing', 'Net Cash from Financing']]
    ]

    # Create a tab container
    tab_container = st.tabs(tabs)

    # Display each financial statement in a separate tab
    for i, tab in enumerate(tab_container):
        with tab:
            st.write(f"**{tabs[i]}**")
            st.write(tab_contents[i])
            st.write(" ")


def calculate_kpis(df):
    kpis = {}
    if 'Total Income' in df.columns and 'Operating Profit' in df.columns and 'Total Expenditure' in df.columns:
        kpis['Total Income'] = df['Total Income'].sum()
        kpis['Operating Profit'] = df['Operating Profit'].sum()
        if df['Total Income'].sum() != 0:
            kpis['Operating Profit Margin'] = (df['Operating Profit'] / df['Total Income']).sum() * 100
        else:
            kpis['Operating Profit Margin'] = 0
        if 'Employee Cost' in df.columns:
            kpis['Employee Cost Percentage'] = (df['Employee Cost'] / df['Total Expenditure']).sum() * 100
        if 'Dividend Per Share(Rs)' in df.columns and 'Earnings Per Share-Unit Curr' in df.columns:
            kpis['Dividend Yield'] = (df['Dividend Per Share(Rs)'] / df['Earnings Per Share-Unit Curr']).sum() * 100
            kpis['Payout Ratio'] = (df['Dividend Per Share(Rs)'] / df['Earnings Per Share-Unit Curr']).sum() * 100
    else:
        st.write("Error: The DataFrame must contain 'Total Income', 'Operating Profit', and 'Total Expenditure' columns for KPI calculation.")
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
