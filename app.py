import streamlit as st
import pandas as pd

st.title("Football AI Analysis - Hidden Value Index")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    metrics = [
        "player rating",
        "progressive passes",
        "progressive passes per 90",
        "total passes completed in final third",
        "total progressive passes received in final third",
        "chances created",
        "chance creation contribution"
    ]

    existing_metrics = [m for m in metrics if m in df.columns]

    if len(existing_metrics) == 0:
        st.error("Required metrics not found in dataset.")
    else:
        for col in existing_metrics:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        for col in existing_metrics:
            df[col + "_norm"] = (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-6)

        norm_cols = [col + "_norm" for col in existing_metrics]
        df["hidden_value_index"] = df[norm_cols].mean(axis=1) * 100

        output_cols = ["hidden_value_index"]

        if "user name" in df.columns:
        output_cols.insert(0, "user name")
        if "team name" in df.columns:
        output_cols.insert(1, "team name")
        if "preferred position" in df.columns:
        output_cols.insert(2, "preferred position")

        result = df[output_cols].sort_values(by="hidden_value_index", ascending=False)

        st.subheader("Top Hidden Value Players")
        st.dataframe(result.head(10), use_container_width=True)

        st.subheader("All Players")
        st.dataframe(result, use_container_width=True)