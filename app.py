import streamlit as st
import pandas as pd

st.title("Football AI Analysis")

uploaded_file = st.file_uploader("Upload your CSV file")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.write(df.head())

    st.subheader("Basic Summary")
    st.write(df.describe())
