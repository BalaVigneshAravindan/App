import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pdfplumber
from openpyxl import load_workbook

def read_file(file):
    file_type = file.type
    
    if file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Read Excel file
        return pd.read_excel(file)
    elif file_type == "application/pdf":
        # Read PDF file
        text = ''
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        # Convert text to DataFrame; customize this according to your PDF structure
        data = [line.split() for line in text.split('\n') if line.strip()]
        return pd.DataFrame(data[1:], columns=data[0])
    elif file_type == "text/csv":
        # Read CSV file
        return pd.read_csv(file)
    else:
        st.write("Unsupported file format.")
        return None


def display_financial_statement(df):
    st.write("Financial Statement")
    st.write(df)
    
def calculate_kpis(df):
    kpis = {}
    
    try:
        # Extracting relevant rows based on known labels
        total_income_row = df[df.iloc[:, 0].str.contains("Total Income", na=False)]
        operating_profit_row = df[df.iloc[:, 0].str.contains("Operating Profit", na=False)]
        total_expenditure_row = df[df.iloc[:, 0].str.contains("Total Expenditure", na=False)]
        
        if not total_income_row.empty and not operating_profit_row.empty and not total_expenditure_row.empty:
            years = df.columns[1:]  # Extract years from column headers
            
            for year in years:
                total_income = float(total_income_row[year].values[0])
                operating_profit = float(operating_profit_row[year].values[0])
                total_expenditure = float(total_expenditure_row[year].values[0])
                
                kpis[year] = {
                    'Total Income': total_income,
                    'Operating Profit': operating_profit,
                    'Operating Profit Margin': (operating_profit / total_income) * 100 if total_income != 0 else 0
                }
                
                if not df[df.iloc[:, 0].str.contains("Employee Cost", na=False)].empty:
                    employee_cost_row = df[df.iloc[:, 0].str.contains("Employee Cost", na=False)]
                    employee_cost = float(employee_cost_row[year].values[0])
                    kpis[year]['Employee Cost Percentage'] = (employee_cost / total_expenditure) * 100
                
                if not df[df.iloc[:, 0].str.contains("Dividend Per Share(Rs)", na=False)].empty:
                    dps_row = df[df.iloc[:, 0].str.contains("Dividend Per Share(Rs)", na=False)]
                    eps_row = df[df.iloc[:, 0].str.contains("Earnings Per Share-Unit Curr", na=False)]
                    dps = float(dps_row[year].values[0])
                    eps = float(eps_row[year].values[0])
                    kpis[year]['Dividend Yield'] = (dps / eps) * 100 if eps != 0 else 0
                    kpis[year]['Payout Ratio'] = (dps / eps) * 100 if eps != 0 else 0
        else:
            st.write("Error: Required rows not found in the data.")
    
    except KeyError as e:
        st.write(f"Error: Column not found - {str(e)}")
    except ValueError as e:
        st.write(f"Error: Value error - {str(e)}")
    
    return kpis

# Displaying KPIs year-wise
def display_kpis(kpis):
    st.write("Key Performance Indicators (KPIs) Year-wise")
    for year, metrics in kpis.items():
        st.write(f"### {year}")
        for metric, value in metrics.items():
            st.write(f"{metric}: {value}")

def create_visualizations(df):
    st.write("Visualizations")
    
    # Check if 'Total Income' is in the DataFrame index
    if not df[df.iloc[:, 0].str.contains("Total Income", na=False)].empty:
        income_row = df[df.iloc[:, 0].str.contains("Total Income", na=False)]
        data = income_row.iloc[0, 1:].astype(float)
        data.index = df.columns[1:]  # Set index to year columns
        
        # Create the bar chart using matplotlib
        fig, ax = plt.subplots()
        data.plot(kind='bar', ax=ax)
        ax.set_title("Total Income Over Years")
        ax.set_xlabel("Years")
        ax.set_ylabel("Total Income (in currency units)")
        plt.xticks(rotation=45)  # Rotate x-axis labels if needed
        
        st.pyplot(fig)
    
    # Check if 'Operating Profit' is in the DataFrame index
    if not df[df.iloc[:, 0].str.contains("Operating Profit", na=False)].empty:
        profit_row = df[df.iloc[:, 0].str.contains("Operating Profit", na=False)]
        data = profit_row.iloc[0, 1:].astype(float)
        data.index = df.columns[1:]  # Set index to year columns
        
        # Create the bar chart using matplotlib
        fig, ax = plt.subplots()
        data.plot(kind='bar', ax=ax, color='orange')
        ax.set_title("Operating Profit Over Years")
        ax.set_xlabel("Years")
        ax.set_ylabel("Operating Profit (in currency units)")
        plt.xticks(rotation=45)  # Rotate x-axis labels if needed
        
        st.pyplot(fig)
    
def evaluate_company_performance(kpis_df):
    kpis_df = kpis_df.set_index('Year')  # Set 'Year' column as index
    total_income_growth_rate = (kpis_df.iloc[-1]['Total Income'] - kpis_df.iloc[0]['Total Income']) / kpis_df.iloc[0]['Total Income']
    operating_profit_margin_avg = kpis_df['Operating Profit Margin'].mean()
    employee_cost_percentage_avg = kpis_df['Employee Cost Percentage'].mean()

    if total_income_growth_rate > 0.1 and operating_profit_margin_avg > 25 and employee_cost_percentage_avg < 70:
        return "The company is in a good position."
    else:
        return "The company needs to improve its performance."

def display_performance_result(result):
    if result == "The company is in a good position.":
        st.markdown(f"**_✅ {result}_**")
    else:
        st.markdown(f"**_❌ {result}_**")
     

def main():
    st.title("Financial Analysis App")
    
    file = st.file_uploader("Upload your file", type=["csv", "xlsx", "pdf"])
    
    if file is not None:
        df = read_file(file)  # Pass only the file object
        if df is not None:
            display_financial_statement(df)
            kpis = calculate_kpis(df)
            display_kpis(kpis)
            
            # Calculate and display overall performance
            kpis_df = pd.DataFrame(kpis).T.reset_index()
            kpis_df.rename(columns={'index': 'Year'}, inplace=True)
            result = evaluate_company_performance(kpis_df)
            st.write("Company Performance Evaluation:")
            display_performance_result(result)
            
            create_visualizations(df)

if __name__ == "__main__":
    main()
