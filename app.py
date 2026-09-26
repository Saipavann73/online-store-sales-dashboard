import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("🛒 Online Store Sales Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Total Sales'] = df['Price'] * df['Quantity']
    return df

df = load_data()

st.sidebar.header("Filter Options")
region_filter = st.sidebar.multiselect(
    "Select Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[(df["Region"].isin(region_filter)) & (df["Category"].isin(category_filter))]

st.markdown("### Key Metrics")
col1, col2, col3 = st.columns(3)

total_revenue = filtered_df["Total Sales"].sum()
total_units = filtered_df["Quantity"].sum()
avg_order_value = filtered_df["Total Sales"].mean() if not filtered_df.empty else 0

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sales by Category")
    fig_category = px.bar(
        filtered_df, 
        x="Category", 
        y="Total Sales", 
        color="Category", 
        text_auto=True
    )
    st.plotly_chart(fig_category, use_container_width=True)

with chart_col2:
    st.subheader("Revenue by Region")
    fig_region = px.pie(
        filtered_df, 
        names="Region", 
        values="Total Sales", 
        hole=0.4
    )
    st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Raw Sales Data")
st.dataframe(filtered_df, use_container_width=True)