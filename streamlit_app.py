{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "0964a8dc-134b-480d-a0b0-30103422de5f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from pdfplumber import open as open_pdf\n",
    "from openpyxl import load_workbook"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "782c1b00-cc45-43ce-826c-7e4ff2e0f3e2",
   "metadata": {},
   "source": [
    "# Function to read file"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "7f851ae4-6bf6-45ab-9e68-8486bd8812f1",
   "metadata": {},
   "outputs": [],
   "source": [
    "def read_file(file):\n",
    "    if file.type == \"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\":\n",
    "        # Read Excel file\n",
    "        wb = load_workbook(file)\n",
    "        sheet = wb.active\n",
    "        df = pd.DataFrame(sheet.values)\n",
    "        return df\n",
    "    elif file.type == \"application/pdf\":\n",
    "        # Read PDF file\n",
    "        with open_pdf(file) as pdf:\n",
    "            page = pdf.pages[0]\n",
    "            text = page.extract_text()\n",
    "            df = pd.DataFrame([x.split() for x in text.split('\\n')])\n",
    "            return df\n",
    "    else:\n",
    "        # Read CSV file\n",
    "        df = pd.read_csv(file)\n",
    "        return df\n",
    "\n",
    "# Function to perform exploratory data analysis\n",
    "def exploratory_data_analysis(df):\n",
    "    st.write(\"Exploratory Data Analysis\")\n",
    "    st.write(df.head())\n",
    "    st.write(df.info())\n",
    "    st.write(df.describe())"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5de73e79-a157-4a29-8f46-7e8c90ddf1dd",
   "metadata": {},
   "source": [
    "# Function to calculate key performance indicators (KPIs)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "b3ea326a-4e87-4ee4-924f-29bcd23a1938",
   "metadata": {},
   "outputs": [],
   "source": [
    "def calculate_kpis(df):\n",
    "    kpis = {}\n",
    "    kpis['Revenue'] = df['Revenue'].sum()\n",
    "    kpis['Net Income'] = df['Net Income'].sum()\n",
    "    kpis['Gross Margin'] = (df['Revenue'] - df['Cost of Goods Sold']).sum() / df['Revenue'].sum()\n",
    "    return kpis"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4bef38eb-e4c7-4b72-b7cc-98418b37192b",
   "metadata": {},
   "source": [
    "# Function to create visualizations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "6fa88d95-e445-4e8d-aec8-37e0116180fe",
   "metadata": {},
   "outputs": [],
   "source": [
    "def create_visualizations(df):\n",
    "    st.write(\"Visualizations\")\n",
    "    fig, ax = plt.subplots()\n",
    "    sns.barplot(x='Category', y='Amount', data=df)\n",
    "    st.pyplot(fig)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f41c21c1-680d-4be1-af80-c31f76069c6a",
   "metadata": {},
   "source": [
    "# Main function"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "c7b28b87-da20-4984-a845-22ccd7a120c9",
   "metadata": {},
   "outputs": [],
   "source": [
    "def main():\n",
    "    st.title(\"Financial Statement Analyzer\")\n",
    "    file = st.file_uploader(\"Choose a file\", type=[\"csv\", \"xlsx\", \"xls\", \"pdf\"])\n",
    "    if file is not None:\n",
    "        df = read_file(file)\n",
    "        if df is not None:\n",
    "            st.write(\"Exploratory Data Analysis\")\n",
    "            st.write(df.head())\n",
    "            st.write(df.info())\n",
    "            st.write(df.describe())\n",
    "            kpis = calculate_kpis(df)\n",
    "            st.write(\"Key Performance Indicators (KPIs)\")\n",
    "            st.write(kpis)\n",
    "            create_visualizations(df)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
