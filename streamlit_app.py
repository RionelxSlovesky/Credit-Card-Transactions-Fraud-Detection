import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Credit Card Transactions Fraud Detection Analysis Dashboard")

st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

st.sidebar.title("Fraud Analysis Sections")
section = st.sidebar.radio(
    "Choose a section to explore:",
    ("Dataset Information", "Time-Based Analysis", "Demographic and Geographic Analysis", "Contextual Analysis")
)

if section == "Dataset Information":
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, index_col=0)

        st.subheader("Dataset Preview")
        st.write(df.head())

        st.title("Dataset Column Descriptions")
        st.text("""
                trans_date_trans_time - Transaction DateTime
                cc_num - Credit Card Number of Customer
                merchant - Merchant Name
                category - Category of Merchant
                amt - Amount of Transaction
                first - First Name of Credit Card Holder
                last - Last Name of Credit Card Holder
                gender - Gender of Credit Card Holder
                street - Street Address of Credit Card Holder
                city - City of Credit Card Holder
                state - State of Credit Card Holder
                zip - Zip of Credit Card Holder
                lat - Latitude Location of Credit Card Holder
                long - Longitude Location of Credit Card Holder
                city_pop - Credit Card Holder's City Population
                job - Job of Credit Card Holder
                dob - Date of Birth of Credit Card Holder
                trans_num - Transaction Number
                unix_time - UNIX Time of transaction
                merch_lat - Latitude Location of Merchant
                merch_long - Longitude Location of Merchant
                is_fraud - Fraud Flag
                """)
    else:
        st.warning("Please upload a CSV file to begin analysis.")

elif section == "Time-Based Analysis":
    st.header("Time-Based Analysis")
    st.write("Explore fraud patterns based on time or day-specific trends.")
    if uploaded_file is not None:
        time_option = st.selectbox("Choose Time Analysis Type:", ["Time-based", "Day-based"])
        st.write(f"You selected: {time_option}")
    else:
        st.warning("Please upload a dataset to analyze.")

elif section == "Demographic and Geographic Analysis":
    st.header("Demographic and Geographic Analysis")
    st.write("Analyze fraud based on demographic and geographic factors.")
    if uploaded_file is not None:
        demo_geo_option = st.selectbox(
            "Choose Analysis Type:",
            ["Gender-based", "Age-based", "State-based", "City-based"]
        )
        st.write(f"You selected: {demo_geo_option}")
    else:
        st.warning("Please upload a dataset to analyze.")

elif section == "Contextual Analysis":
    st.header("Contextual Analysis")
    st.write("Examine fraud based on contextual factors like merchant category.")
    if uploaded_file is not None:
        st.write(f"Contextual Analysis Section")
    else:
        st.warning("Please upload a dataset to analyze.")
