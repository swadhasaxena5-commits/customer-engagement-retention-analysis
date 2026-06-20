import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Bank Customer Retention Dashboard",
    page_icon="🏦",
    layout="wide"
)

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("European_Bank.csv")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("🎛 Dashboard Filters")

st.sidebar.success("""
Welcome to the Bank Analytics Dashboard!

Use the filters below to explore customer behavior, churn patterns, and retention insights.
""")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + list(df["Geography"].unique())
)

product_filter = st.sidebar.slider(
    "Minimum Products",
    int(df["NumOfProducts"].min()),
    int(df["NumOfProducts"].max()),
    1
)
balance_filter = st.sidebar.slider(
    "Minimum Balance",
    0,
    int(df["Balance"].max()),
    0
)
if country != "All":
    df = df[df["Geography"] == country]

df = df[df["NumOfProducts"] >= product_filter]
df = df[df["Balance"] >= balance_filter]

df = df[df["NumOfProducts"] >= product_filter]
# ==========================
# TITLE
# ==========================

st.title("🏦 Customer Engagement & Product Utilization Dashboard")


st.markdown("""
### Understanding Customer Retention Through Engagement & Product Usage
""")

# ==========================
# KPI SECTION
# ==========================

total_customers = len(df)
churn_rate = round(df["Exited"].mean() * 100, 2)
avg_balance = round(df["Balance"].mean(), 2)
avg_products = round(df["NumOfProducts"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Customers", total_customers)
col2.metric("📉 Churn Rate", f"{churn_rate}%")
col3.metric("💰 Avg Balance", f"{avg_balance:,.0f}")
col4.metric("🛍 Avg Products", avg_products)

st.divider()

st.info("""
### 📋 Executive Summary

• Overall Churn Rate: 20.37%

• Active customers churn significantly less than inactive customers.

• Customers with 2 products demonstrate the strongest retention.

• Germany records the highest churn rate among all regions.

• High-value inactive customers represent a major retention risk.

• Credit card ownership has limited impact on loyalty.
""")

if churn_rate > 20:
    st.error(
        "⚠️ Churn rate exceeds 20%. Immediate retention strategies recommended."
    )
# ==========================
# KEY INSIGHTS
# ==========================

st.success("""
### 🔍 Key Insights

✅ Active customers churn significantly less.

✅ Customers with 2 products show the highest loyalty.

✅ Germany has the highest churn rate.

✅ Many premium customers are inactive and at risk.
""")

st.divider()

# ==========================
# CHART 1
# ==========================

st.subheader("📊 Customer Activity vs Churn")

activity_churn = (
    df.groupby("IsActiveMember")["Exited"]
    .mean()
    * 100
)

fig1 = px.bar(
    x=["Inactive", "Active"],
    y=activity_churn.values,
    labels={"x": "Customer Activity", "y": "Churn Rate (%)"},
    title="Customer Activity vs Churn Rate"
)

st.plotly_chart(fig1, use_container_width=True)

# ==========================
# CHART 2
# ==========================

st.subheader("📦 Product Utilization vs Churn")

product_churn = (
    df.groupby("NumOfProducts")["Exited"]
    .mean()
    * 100
)

fig2 = px.bar(
    x=product_churn.index,
    y=product_churn.values,
    labels={"x": "Number of Products", "y": "Churn Rate (%)"},
    title="Products Used vs Churn Rate"
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================
# CHART 3
# ==========================

st.subheader("🌍 Geography vs Churn")

geo_churn = (
    df.groupby("Geography")["Exited"]
    .mean()
    * 100
)

fig3 = px.bar(
    x=geo_churn.index,
    y=geo_churn.values,
    labels={"x": "Country", "y": "Churn Rate (%)"},
    title="Country-wise Churn Rate"
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================
# PIE CHART
# ==========================

st.subheader("🥧 Customer Retention Overview")

churn_counts = df["Exited"].value_counts()

fig4 = px.pie(
    values=churn_counts.values,
    names=["Stayed", "Left"],
    title="Customer Retention Distribution"
)

st.plotly_chart(fig4, use_container_width=True)
# ==========================
# SALARY VS BALANCE ANALYSIS
# ==========================

st.subheader("📈 Salary vs Balance Analysis")

fig5 = px.scatter(
    df,
    x="EstimatedSalary",
    y="Balance",
    color="Exited",
    title="Salary vs Balance Relationship",
    hover_data=["Geography", "Age"]
)

st.plotly_chart(fig5, use_container_width=True)

# ==========================
# HIGH VALUE CUSTOMERS
# ==========================

st.subheader("⚠️ High-Value Disengaged Customers")

high_value = df[
    (df["Balance"] > 100000)
    &
    (df["IsActiveMember"] == 0)
]

st.warning(
    f"{len(high_value)} premium customers are inactive and may churn."
)

st.metric(
    "💰 High-Value Disengaged Customers",
    len(high_value)
)

st.dataframe(
    high_value[
        [
            "CustomerId",
            "Surname",
            "Balance",
            "Geography",
            "Exited"
        ]
    ].head(20)
)
# ==========================
# CREDIT CARD STICKINESS SCORE
# ==========================

st.subheader("💳 Credit Card Stickiness Score")

card_churn = (
    df.groupby("HasCrCard")["Exited"]
    .mean()
    * 100
)

credit_card_stickiness = round(
    100 - card_churn[1],
    2
)

st.metric(
    "Credit Card Stickiness Score",
    f"{credit_card_stickiness}%"
)

# ==========================
# RELATIONSHIP STRENGTH
# ==========================

st.subheader("🤝 Relationship Strength Index")

df["RelationshipScore"] = (
    df["NumOfProducts"]
    + df["HasCrCard"]
    + df["IsActiveMember"]
)

avg_score = round(
    df["RelationshipScore"].mean(),
    2
)

st.metric(
    "Relationship Strength Index",
    avg_score
)

# ==========================
# DATASET
# ==========================
st.subheader("⭐ Customer Retention Segments")

high = len(df[df["RelationshipScore"] >= 4])
medium = len(df[(df["RelationshipScore"] >= 2) & (df["RelationshipScore"] < 4)])
low = len(df[df["RelationshipScore"] < 2])

c1, c2, c3 = st.columns(3)

c1.metric("🟢 High Retention", high)
c2.metric("🟡 Medium Retention", medium)
c3.metric("🔴 At Risk", low)

st.subheader("🎯 Retention Recommendations")

st.success("""
1. Increase engagement campaigns for inactive customers.

2. Promote cross-selling to move customers from 1 product to 2 products.

3. Focus retention efforts on Germany due to its high churn rate.

4. Target high-value inactive customers with personalized offers.

5. Strengthen loyalty programs rather than relying solely on credit card ownership.
""")

with st.expander("📄 View Customer Dataset"):
    st.dataframe(df.head(50))
    csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Dataset",
    csv,
    "customer_analysis.csv",
    "text/csv"
)