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

# Time-based Fraud Analysis
def plot_frauds_by_hour(df):
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    fraud_data = df[df['is_fraud'] == 1].copy()
    fraud_data['hour'] = fraud_data['trans_date_trans_time'].dt.hour
    fraud_counts_by_hour = fraud_data.groupby('hour').size()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        fraud_counts_by_hour.index, 
        fraud_counts_by_hour.values, 
        marker='o', 
        linestyle='-', 
        color='tab:red'
    )
    
    ax.set_title('Number of Frauds by Time of Day', fontsize=16)
    ax.set_xlabel('Time of Day (Hour)', fontsize=14)
    ax.set_ylabel('Number of Frauds', fontsize=14)
    ax.grid(True)
    ax.set_xticks(range(0, 24))
    
    st.pyplot(fig)

def plot_frauds_by_day_of_week(df):
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    fraud_data = df[df['is_fraud'] == 1].copy()
    fraud_data['day_of_week'] = fraud_data['trans_date_trans_time'].dt.dayofweek
    fraud_counts_by_day = fraud_data.groupby('day_of_week').size()
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    fraud_counts_by_day.index = fraud_counts_by_day.index.map(lambda x: day_names[x])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        fraud_counts_by_day.index, 
        fraud_counts_by_day.values, 
        marker='o', 
        linestyle='-', 
        color='tab:red'
    )
    
    ax.set_title('Number of Frauds by Day of the Week', fontsize=16)
    ax.set_xlabel('Day of the Week', fontsize=14)
    ax.set_ylabel('Number of Frauds', fontsize=14)
    ax.grid(True)
    
    st.pyplot(fig)
    
# Demographic and Geographic Analysis
def plot_fraud_by_gender_bar(df):
    fraud_data = df[df['is_fraud'] == 1]
    fraud_counts_by_gender = fraud_data.groupby('gender').size()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fraud_counts_by_gender.plot(kind='bar', color=['tab:pink', 'tab:blue'], edgecolor='black', ax=ax)
    ax.set_title('Number of Fraud Transactions by Gender', fontsize=16)
    ax.set_xlabel('Gender', fontsize=14)
    ax.set_ylabel('Number of Fraud Transactions', fontsize=14)
    ax.set_xticks(range(len(fraud_counts_by_gender.index)))
    ax.set_xticklabels(fraud_counts_by_gender.index, rotation=0)
    
    st.pyplot(fig)

def plot_fraud_vs_nonfraud_gender_pie(df):
    fraud_gender_counts = df.groupby(['gender', 'is_fraud']).size().unstack(fill_value=0)

    male_data = fraud_gender_counts.loc['M'] if 'M' in fraud_gender_counts.index else [0, 0]
    female_data = fraud_gender_counts.loc['F'] if 'F' in fraud_gender_counts.index else [0, 0]

    labels = ['Not Fraud', 'Fraud']
    colors = ['tab:blue', 'tab:pink']

    fig, axes = plt.subplots(1, 2, figsize=(12, 7))
    
    axes[0].pie(male_data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
    axes[0].set_title('Male Transactions', fontsize=14)
    
    axes[1].pie(female_data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
    axes[1].set_title('Female Transactions', fontsize=14)
    
    plt.suptitle('Fraud vs. Not Fraud Transactions by Gender', fontsize=16)
    plt.tight_layout()
    st.pyplot(fig)

def plot_fraud_by_age_group_bar_streamlit(df):
    
    df['dob'] = pd.to_datetime(df['dob'])

    reference_date = pd.Timestamp('2020-12-31')

    df['age'] = (reference_date - df['dob']).dt.days // 365
    
    age_bins = [12, 19, 64, 150]
    age_labels = ['Teens', 'Adults', 'Seniors']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
    
    fraud_data = df[df['is_fraud'] == 1]
    fraud_by_age_group = fraud_data['age_group'].value_counts().reindex(age_labels)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fraud_by_age_group.plot(kind='bar', color='tab:red', edgecolor='black', ax=ax)
    
    ax.set_title('Fraud Transactions by Age Group', fontsize=16)
    ax.set_xlabel('Age Group', fontsize=14)
    ax.set_ylabel('Number of Fraud Transactions', fontsize=14)
    ax.set_xticks(range(len(age_labels)))
    ax.set_xticklabels(age_labels, rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    st.pyplot(fig)

def plot_fraud_vs_nonfraud_pie_streamlit(df):
    
    df['dob'] = pd.to_datetime(df['dob'])

    reference_date = pd.Timestamp('2020-12-31')

    df['age'] = (reference_date - df['dob']).dt.days // 365
    age_bins = [12, 19, 64, 150]
    age_labels = ['Teens', 'Adults', 'Seniors']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
    
    age_fraud_distribution = df.groupby(['age_group', 'is_fraud'], observed=False).size().unstack(fill_value=0)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 8))
    for i, (group, title) in enumerate(zip(age_labels, ['Teens (13–19)', 'Adults (20–64)', 'Seniors (65+)'])):
        data = age_fraud_distribution.loc[group]
        axes[i].pie(data, labels=['Non-Fraud', 'Fraud'], autopct='%1.1f%%', colors=['tab:blue', 'tab:pink'], startangle=90)
        axes[i].set_title(title, fontsize=14)
    
    plt.suptitle('Fraud vs Non-Fraud Transactions by Age Group', fontsize=16)
    plt.tight_layout()
    st.pyplot(fig)

def plot_fraud_nonfraud_state_barcharts(df):
    state_fraud_counts = df.groupby(['state', 'is_fraud']).size().unstack(fill_value=0)
    
    fraud_counts = state_fraud_counts[1] 
    non_fraud_counts = state_fraud_counts[0] 
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    
    axes[0].bar(fraud_counts.index, fraud_counts.values, color='tab:blue', edgecolor='black')
    axes[0].set_title('Fraud Transactions by State', fontsize=16)
    axes[0].set_xlabel('State', fontsize=14)
    axes[0].set_ylabel('Number of Transactions', fontsize=14)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_ylim(0, fraud_counts.max() + 10)
    
    axes[1].bar(non_fraud_counts.index, non_fraud_counts.values, color='tab:pink', edgecolor='black')
    axes[1].set_title('Non-Fraud Transactions by State', fontsize=16)
    axes[1].set_xlabel('State', fontsize=14)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].set_ylim(0, non_fraud_counts.max() + 10)
    
    plt.tight_layout()
    st.pyplot(fig)

def display_fraud_ratio_table(df):
    state_fraud_counts = df.groupby(['state', 'is_fraud']).size().unstack(fill_value=0)
    state_fraud_counts.columns = ['Non-Fraud Count', 'Fraud Count']
    state_fraud_counts['Fraud Ratio'] = state_fraud_counts['Fraud Count'] / (state_fraud_counts['Fraud Count'] + state_fraud_counts['Non-Fraud Count'])
    
    fraud_ratio_table = state_fraud_counts.reset_index()
    fraud_ratio_table.rename(columns={'state': 'State'}, inplace=True)
    fraud_ratio_table = fraud_ratio_table.sort_values(by='Fraud Ratio', ascending=False)
    
    st.subheader("Fraud Ratio by State")
    st.dataframe(fraud_ratio_table, use_container_width=True)

def plot_fraud_by_city_population(df):
    fraud_transactions = df[df['is_fraud'] == 1]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    scatter = ax.scatter(
        fraud_transactions['city_pop'], 
        fraud_transactions['amt'], 
        color='tab:red', 
        alpha=0.7, 
        edgecolor='black', 
        s=50
    )
    
    ax.set_title('Fraud Transactions by City Population', fontsize=16)
    ax.set_xlabel('City Population', fontsize=14)
    ax.set_ylabel('Transaction Amount (amt)', fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    st.pyplot(fig)

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
        df = pd.read_csv(uploaded_file, index_col=0)
        time_option = st.selectbox("Choose Time Analysis Type:", ["Time-based", "Day-based"])
        st.write(f"You selected: {time_option}")
        if time_option is "Time-based":
            st.header("Time-Based Analysis")
            st.subheader("Frauds by Time of Day")
            plot_frauds_by_hour(df)
        else:
            st.header("Day-Based Analysis")
            st.subheader("Frauds by Day of the Week")
            plot_frauds_by_day_of_week(df)
    else:
        st.warning("Please upload a dataset to analyze.")

elif section == "Demographic and Geographic Analysis":
    st.header("Demographic and Geographic Analysis")
    st.write("Analyze fraud based on demographic and geographic factors.")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, index_col=0)
        demo_geo_option = st.selectbox(
            "Choose Analysis Type:",
            ["Gender-based", "Age-based", "State-based", "City-based"]
        )
        st.write(f"You selected: {demo_geo_option}")
        if demo_geo_option is "Gender-based":
            st.header("Gender-Based Analysis")
            st.subheader("Number of Fraud Transactions by Gender")
            plot_fraud_by_gender_bar(df)
            st.subheader("Fraud vs. Non-Fraud Transactions by Gender")
            plot_fraud_vs_nonfraud_gender_pie(df)
        elif demo_geo_option is "Age-based":
            st.header("Age-Based Analysis")
            st.subheader("Fraud Transactions by Age Group")
            plot_fraud_by_age_group_bar_streamlit(df)
            st.subheader("Fraud vs. Non-Fraud Transactions by Age Group")
            plot_fraud_vs_nonfraud_pie_streamlit(df)
        elif demo_geo_option is "State-based":
            st.header("State-Based Analysis")
            st.subheader("Fraud and Non-Fraud Transactions by State")
            plot_fraud_nonfraud_state_barcharts(df)
            st.subheader("Fraud Ratio Table by State")
            display_fraud_ratio_table(df)
        else:
            st.header("City-Based Analysis")
            st.subheader("Fraud Transactions by City Population")
            plot_fraud_by_city_population(df)
    else:
        st.warning("Please upload a dataset to analyze.")

elif section == "Contextual Analysis":
    st.header("Contextual Analysis")
    st.write("Examine fraud based on contextual factors like merchant category.")
    if uploaded_file is not None:
        st.write(f"Contextual Analysis Section")
    else:
        st.warning("Please upload a dataset to analyze.")
