import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Customer Churn Analytics", layout="wide")

# --- MOCK DATA GENERATOR ---
@st.cache_data
def load_data():
    # Creating dummy data for demonstration
    np.random.seed(42)
    data = pd.DataFrame({
        'CustomerID': range(1001, 1201),
        'Tenure': np.random.randint(1, 72, 200),
        'MonthlyCharges': np.random.uniform(20, 120, 200),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], 200),
        'Churn_Prob': np.random.uniform(0, 1, 200),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 200)
    })
    data['Is_Churn'] = data['Churn_Prob'] > 0.7
    return data

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
region_filter = st.sidebar.multiselect("Select Region:", options=df['Region'].unique(), default=df['Region'].unique())
contract_filter = st.sidebar.multiselect("Contract Type:", options=df['Contract'].unique(), default=df['Contract'].unique())

filtered_df = df[(df['Region'].isin(region_filter)) & (df['Contract'].isin(contract_filter))]

# --- MAIN HEADER ---
st.title("📊 Customer Churn Analysis Dashboard")
st.markdown("Monitor customer retention metrics and identify high-risk segments in real-time.")

# --- TOP LEVEL METRICS ---
col1, col2, col3, col4 = st.columns(4)
total_cust = len(filtered_df)
churned_cust = filtered_df['Is_Churn'].sum()
churn_rate = (churned_cust / total_cust) * 100

col1.metric("Total Customers", total_cust)
col2.metric("Churned Customers", churned_cust, delta_color="inverse")
col3.metric("Churn Rate", f"{churn_rate:.1f}%")
col4.metric("Avg Monthly Revenue", f"${filtered_df['MonthlyCharges'].mean():.2f}")

st.divider()

# --- VISUALIZATIONS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Churn Probability vs Monthly Charges")
    fig_scatter = px.scatter(filtered_df, x="MonthlyCharges", y="Churn_Prob", 
                 color="Contract", hover_data=['CustomerID'],
                 title="Risk Analysis by Spending")
    st.plotly_chart(fig_scatter, use_container_width=True)

with c2:
    st.subheader("Churn Distribution by Contract")
    fig_bar = px.histogram(filtered_df, x="Contract", color="Is_Churn", barmode="group",
                           title="Churn Count by Contract Type")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- DATA TABLE ---
st.subheader("🔍 High Risk Customer Watchlist")
high_risk = filtered_df[filtered_df['Churn_Prob'] > 0.8].sort_values(by="Churn_Prob", ascending=False)
st.dataframe(high_risk, use_container_width=True)

# --- EXPORT FEATURE ---
st.sidebar.download_button(
    label="Download Analysis as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='churn_analysis.csv',
    mime='text/csv'
)
