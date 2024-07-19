# app.py
import streamlit as st
import matplotlib.pyplot as plt

st.title("Hello, World!")

name = st.text_input("Enter your name:")
age = st.slider("Enter your age:", 1, 100)

if st.button("Submit"):
    st.write(f"Hello, {name}! You are {age} years old.")

    fig, ax = plt.subplots()
    ax.bar(["Age"], [age])
    st.pyplot(fig)
