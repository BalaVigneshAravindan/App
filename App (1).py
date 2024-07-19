import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

Title of the application
st.title("Financial Statement Analyzer")
DeltaGenerator()

Sidebar inputs
st.sidebar.header("User Input Parameters")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())

Data visualization
st.subheader("Data Visualization")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    columns = data.columns
    selected_column = st.selectbox("Select a column to visualize", columns)
    
    if st.button("Generate Plot"):
        plt.figure(figsize=(10, 5))
        data[selected_column].hist()
        plt.title(f"Distribution of {selected_column}")
        st.pyplot(plt)
else:
    st.write("Please upload a CSV file to get started.")