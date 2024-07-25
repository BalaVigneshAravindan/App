import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pdfplumber
from openpyxl import load_workbook

def read_file(file):
    if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Read Excel file
        df = pd.read_excel(file)
        return df
    elif file.type == "application/pdf":
        # Read PDF file
        text = ''
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return pd.DataFrame([text.splitlines()], columns=["Content"])  # Sample processing
    elif file.type == "text/csv":
        # Read CSV file
        df = pd.read_csv(file)
        return df
    else:
        return None

def display_financial_statement(df):
    st.write("Financial Statement")
    st.write(df)
    
def calculate_kpis(df):
    kpis = {}
    
    try:
       
        total_income_row = df[df.iloc[:, 0].str.contains("Total Income", na=False)]
        operating_profit_row = df[df.iloc[:, 0].str.contains("Operating Profit", na=False)]
        total_expenditure_row = df[df.iloc[:, 0].str.contains("Total Expenditure", na=False)]
        
        if not total_income_row.empty and not operating_profit_row.empty and not total_expenditure_row.empty:
          
            total_income = total_income_row.iloc[0, 1:].astype(float).sum()
            operating_profit = operating_profit_row.iloc[0, 1:].astype(float).sum()
            total_expenditure = total_expenditure_row.iloc[0, 1:].astype(float).sum()
            
            kpis['Total Income'] = total_income
            kpis['Operating Profit'] = operating_profit
            kpis['Operating Profit Margin'] = (operating_profit / total_income) * 100 if total_income != 0 else 0
            
            if not df[df.iloc[:, 0].str.contains("Employee Cost", na=False)].empty:
                employee_cost_row = df[df.iloc[:, 0].str.contains("Employee Cost", na=False)]
                employee_cost = employee_cost_row.iloc[0, 1:].astype(float).sum()
                kpis['Employee Cost Percentage'] = (employee_cost / total_expenditure) * 100
            
            if not df[df.iloc[:, 0].str.contains("Dividend Per Share(Rs)", na=False)].empty:
                dps_row = df[df.iloc[:, 0].str.contains("Dividend Per Share(Rs)", na=False)]
                eps_row = df[df.iloc[:, 0].str.contains("Earnings Per Share-Unit Curr", na=False)]
                dps = dps_row.iloc[0, 1:].astype(float).sum()
                eps = eps_row.iloc[0, 1:].astype(float).sum()
                kpis['Dividend Yield'] = (dps / eps) * 100 if eps != 0 else 0
                kpis['Payout Ratio'] = (dps / eps) * 100 if eps != 0 else 0
        else:
            st.write("Error: Required rows not found in the data.")
    
    except KeyError as e:
        st.write(f"Error: Column not found - {str(e)}")
    
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
            display_financial_statement(df)
            kpis = calculate_kpis(df)
            st.write("Key Performance Indicators (KPIs)")
            st.write(kpis)
            create_visualizations(df)
        else:
            st.write("Error: Could not read the file. Please ensure it is in the correct format.")

if __name__ == "__main__":
    main()
