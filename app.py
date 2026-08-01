import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
<style>

/* Main App */
.stApp{
    background-color:#F4F8FC;
}

/* Reduce top padding */
.block-container{
    padding-top:2rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* KPI Cards */
div[data-testid="stMetric"]{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:16px;
    padding:20px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

div[data-testid="stMetricLabel"]{
    font-weight:600;
    color:#64748B;
}

div[data-testid="stMetricValue"]{
    color:#1E3A8A;
    font-size:32px;
    font-weight:700;
}

/* Headers */
h1{
    color:#1E293B;
}

h2,h3{
    color:#334155;
}

/* Remove unnecessary white gap */
hr{
    margin-top:8px;
    margin-bottom:18px;
}

</style>
""", unsafe_allow_html=True)


sns.set_theme(
    style="whitegrid",
    rc={
        "axes.facecolor":"white",
        "figure.facecolor":"white",
        "grid.color":"#E5E7EB",
        "axes.edgecolor":"#CBD5E1"
    }
)

PRIMARY = "#2563EB"
GREEN = "#16A34A"
ORANGE = "#F59E0B"
PURPLE = "#7C3AED"


@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/Superstore.csv",
        encoding="latin1"
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True
    )

    df["Order Year"] = df["Order Date"].dt.year
    df["Order Month"] = df["Order Date"].dt.month_name()
    df["Month Number"] = df["Order Date"].dt.month

    return df

df = load_data()


st.sidebar.title("📊 Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "📍 Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_category = st.sidebar.multiselect(
    "📦 Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

selected_segment = st.sidebar.multiselect(
    "👥 Customer Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

filtered_df = df[
    (df["Region"].isin(selected_region))
    &
    (df["Category"].isin(selected_category))
    &
    (df["Segment"].isin(selected_segment))
]


st.title("📊 Superstore Sales Dashboard")

st.markdown("""
Analyze sales performance, customer segments, regional trends and
business profitability using an interactive dashboard built with
**Streamlit, Plotly, Matplotlib and Seaborn**.
""")

st.divider()


total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
average_discount = filtered_df["Discount"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}"
    )

with c2:
    st.metric(
        "📈 Total Profit",
        f"${total_profit:,.0f}"
    )

with c3:
    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )

with c4:
    st.metric(
        "🏷 Average Discount",
        f"{average_discount:.1%}"
    )

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Sales Over Time")

    monthly_sales = (
        filtered_df
        .groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=[PRIMARY]
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
        hovertemplate="<b>%{x|%b %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    )

    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="",
        yaxis_title="Sales ($)",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:

    st.subheader("📦 Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(7,4))

    sns.barplot(
        data=category_sales,
        x="Category",
        y="Sales",
        palette=["#2563EB", "#0EA5E9", "#38BDF8"],
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel("Sales ($)")
    ax.set_title("")

    sns.despine()

    plt.tight_layout()

    st.pyplot(fig)


col3, col4 = st.columns(2)


with col3:

    st.subheader("🌍 Sales by Region")

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        height=360,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="",
        yaxis_title="Sales ($)"
    )

    st.plotly_chart(fig, use_container_width=True)


with col4:

    st.subheader("👥 Sales by Customer Segment")

    segment_sales = (
        filtered_df
        .groupby("Segment")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(7,4))

    sns.barplot(
        data=segment_sales,
        x="Segment",
        y="Sales",
        palette=["#16A34A", "#22C55E", "#86EFAC"],
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel("Sales ($)")
    ax.set_title("")

    sns.despine()

    plt.tight_layout()

    st.pyplot(fig)

st.divider()


col5, col6 = st.columns(2)


with col5:

    st.subheader("🏆 Top 10 Products by Sales")

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_white"
    )

    fig.update_layout(
        height=420,
        xaxis_title="Sales ($)",
        yaxis_title="",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)


with col6:

    st.subheader("💸 Discount vs Profit")

    fig = px.scatter(
        filtered_df,
        x="Discount",
        y="Profit",
        size="Sales",
        color="Category",
        hover_name="Product Name",
        template="plotly_white",
        opacity=0.75
    )

    fig.update_layout(
        height=420,
        xaxis_title="Discount",
        yaxis_title="Profit ($)",
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📊 Profit by Sub-Category")

subcategory_profit = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values()
    .reset_index()
)

colors = [
    "#16A34A" if value >= 0 else "#DC2626"
    for value in subcategory_profit["Profit"]
]

fig, ax = plt.subplots(figsize=(10, 7))

ax.barh(
    subcategory_profit["Sub-Category"],
    subcategory_profit["Profit"],
    color=colors
)

ax.set_xlabel("Profit ($)")
ax.set_ylabel("")
ax.set_title("")

sns.despine()

plt.tight_layout()

st.pyplot(fig)

st.divider()

st.subheader("📌 Key Business Insights")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

best_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

most_profitable_subcategory = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .idxmax()
)

highest_discount = filtered_df["Discount"].max()

st.markdown(f"""
- 💰 **Total Sales:** **${total_sales:,.2f}**
- 📈 **Total Profit:** **${total_profit:,.2f}**
- 🌍 **Highest Sales Region:** **{best_region}**
- 📦 **Best Performing Category:** **{best_category}**
- 🏆 **Most Profitable Sub-Category:** **{most_profitable_subcategory}**
- 🏷️ **Maximum Discount Offered:** **{highest_discount:.0%}**
""")

st.divider()


