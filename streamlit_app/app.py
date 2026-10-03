import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import plotly.express as px
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SaaS GTM Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
}

[data-testid="stSidebar"] {
    background-color: #161B22;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin-bottom: 0px;
}

.sub-title {
    color: #9CA3AF;
    font-size: 18px;
    margin-bottom: 20px;
}

.insight-box {
    background-color: #161B22;
    padding: 18px;
    border-radius: 14px;
    border-left: 5px solid #4C9AFF;
    margin-top: 10px;
    margin-bottom: 10px;
}

[data-testid="stMetric"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    padding: 15px;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #9CA3AF;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=st.secrets["mysql"]["password"],
        database="saasgtm"
    )

    return connection


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=60)
def load_data():

    connection = get_connection()

    customers = pd.read_sql(
        "SELECT * FROM cleaned_customers",
        connection
    )

    events = pd.read_sql(
        "SELECT * FROM cleaned_events",
        connection
    )

    subscriptions = pd.read_sql(
        "SELECT * FROM cleaned_subscriptions",
        connection
    )

    return customers, events, subscriptions


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# 🚀 SaaS GTM")
st.sidebar.markdown("## Intelligence")

st.sidebar.divider()

st.sidebar.markdown("### 🎛️ Dashboard Filters")


# ============================================================
# REFRESH BUTTON
# ============================================================

if st.sidebar.button("🔄 Refresh Dashboard", use_container_width=True):

    st.cache_data.clear()
    st.rerun()


# ============================================================
# LOAD DATABASE
# ============================================================

try:

    customers, events, subscriptions = load_data()

except Exception as e:

    st.error("❌ Unable to connect to MySQL.")
    st.code(str(e))
    st.stop()


# ============================================================
# CLEAN DATA TYPES
# ============================================================

if "event_date" in events.columns:

    events["event_date"] = pd.to_datetime(
        events["event_date"],
        errors="coerce"
    )


if "start_date" in subscriptions.columns:

    subscriptions["start_date"] = pd.to_datetime(
        subscriptions["start_date"],
        errors="coerce"
    )


if "end_date" in subscriptions.columns:

    subscriptions["end_date"] = pd.to_datetime(
        subscriptions["end_date"],
        errors="coerce"
    )


if "monthly_price" in subscriptions.columns:

    subscriptions["monthly_price"] = pd.to_numeric(
        subscriptions["monthly_price"],
        errors="coerce"
    ).fillna(0)

else:

    subscriptions["monthly_price"] = 0


# ============================================================
# CUSTOMER SEGMENT FILTER
# ============================================================

if "segment" in customers.columns:

    segment_options = ["All"] + sorted(
        customers["segment"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_segment = st.sidebar.selectbox(
        "Customer Segment",
        segment_options
    )

else:

    selected_segment = "All"


# ============================================================
# COUNTRY FILTER
# ============================================================

if "country" in customers.columns:

    country_options = ["All"] + sorted(
        customers["country"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_country = st.sidebar.selectbox(
        "Country",
        country_options
    )

else:

    selected_country = "All"


# ============================================================
# ACQUISITION SOURCE FILTER
# ============================================================

if "source" in events.columns:

    source_options = ["All"] + sorted(
        events["source"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_source = st.sidebar.selectbox(
        "Acquisition Source",
        source_options
    )

else:

    selected_source = "All"


st.sidebar.divider()

st.sidebar.success("📌 Live data connection: MySQL")

st.sidebar.caption(
    f"Last refreshed: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_customers = customers.copy()
filtered_events = events.copy()
filtered_subscriptions = subscriptions.copy()


# SEGMENT FILTER

if selected_segment != "All" and "segment" in filtered_customers.columns:

    selected_customer_ids = filtered_customers[
        filtered_customers["segment"].astype(str)
        == selected_segment
    ]["customer_id"].unique()

    filtered_customers = filtered_customers[
        filtered_customers["customer_id"].isin(selected_customer_ids)
    ]

    filtered_events = filtered_events[
        filtered_events["customer_id"].isin(selected_customer_ids)
    ]

    filtered_subscriptions = filtered_subscriptions[
        filtered_subscriptions["customer_id"].isin(selected_customer_ids)
    ]


# COUNTRY FILTER

if selected_country != "All" and "country" in filtered_customers.columns:

    selected_customer_ids = filtered_customers[
        filtered_customers["country"].astype(str)
        == selected_country
    ]["customer_id"].unique()

    filtered_customers = filtered_customers[
        filtered_customers["customer_id"].isin(selected_customer_ids)
    ]

    filtered_events = filtered_events[
        filtered_events["customer_id"].isin(selected_customer_ids)
    ]

    filtered_subscriptions = filtered_subscriptions[
        filtered_subscriptions["customer_id"].isin(selected_customer_ids)
    ]


# SOURCE FILTER

if selected_source != "All" and "source" in filtered_events.columns:

    source_customer_ids = filtered_events[
        filtered_events["source"].astype(str)
        == selected_source
    ]["customer_id"].unique()

    filtered_customers = filtered_customers[
        filtered_customers["customer_id"].isin(source_customer_ids)
    ]

    filtered_events = filtered_events[
        filtered_events["customer_id"].isin(source_customer_ids)
    ]

    filtered_subscriptions = filtered_subscriptions[
        filtered_subscriptions["customer_id"].isin(source_customer_ids)
    ]


# ============================================================
# CORE METRICS
# ============================================================

total_customers = filtered_customers["customer_id"].nunique()

total_subscriptions = len(filtered_subscriptions)


if "status" in filtered_subscriptions.columns:

    active_subscriptions = filtered_subscriptions[
        filtered_subscriptions["status"]
        .astype(str)
        .str.lower()
        == "active"
    ]

    canceled_subscriptions = filtered_subscriptions[
        filtered_subscriptions["status"]
        .astype(str)
        .str.lower()
        == "canceled"
    ]

else:

    active_subscriptions = filtered_subscriptions.copy()
    canceled_subscriptions = pd.DataFrame()


active_customers = active_subscriptions["customer_id"].nunique()

paid_customers = filtered_subscriptions["customer_id"].nunique()

total_mrr = active_subscriptions["monthly_price"].sum()

avg_revenue_per_customer = (
    total_mrr / active_customers
    if active_customers > 0
    else 0
)

churned_customers = canceled_subscriptions["customer_id"].nunique()

churn_rate = (
    churned_customers / paid_customers * 100
    if paid_customers > 0
    else 0
)


# ============================================================
# REVENUE AT RISK
# ============================================================

activated_customer_ids = set()

if "event_type" in filtered_events.columns:

    activated_customer_ids = set(

        filtered_events[
            filtered_events["event_type"]
            .astype(str)
            .str.lower()
            == "activated"
        ]["customer_id"]
        .dropna()
        .unique()

    )


risk_subscriptions = active_subscriptions[
    ~active_subscriptions["customer_id"].isin(
        activated_customer_ids
    )
].copy()


if "monthly_price" in risk_subscriptions.columns:

    revenue_at_risk = pd.to_numeric(
        risk_subscriptions["monthly_price"],
        errors="coerce"
    ).fillna(0).sum()

else:

    revenue_at_risk = 0


at_risk_customers = (
    risk_subscriptions["customer_id"].nunique()
    if not risk_subscriptions.empty
    else 0
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚀 SaaS GTM Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Advanced Go-To-Market, Revenue, Funnel & Customer Analytics'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )


with col2:

    st.metric(
        "💳 Paying Customers",
        f"{paid_customers:,}"
    )


with col3:

    st.metric(
        "💰 Active MRR",
        f"${total_mrr:,.0f}"
    )


with col4:

    st.metric(
        "📊 Churn Rate",
        f"{churn_rate:.1f}%"
    )


with col5:

    st.metric(
        "⚠️ Revenue at Risk",
        f"${revenue_at_risk:,.0f}"
    )


st.divider()


# ============================================================
# CREATE TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([

    "📊 Executive Overview",
    "🔻 Funnel Analysis",
    "💰 Revenue & Churn",
    "📣 Acquisition",
    "⚠️ Data Quality & Risk"

])


# ============================================================
# TAB 1 - EXECUTIVE OVERVIEW
# ============================================================

with tab1:

    st.subheader("📊 Executive Business Overview")

    # --------------------------------------------------------
    # AUTOMATED EXECUTIVE INSIGHTS
    # --------------------------------------------------------

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    # TOP SEGMENT

    top_segment_text = "No segment data"

    if (
        "segment" in filtered_customers.columns
        and not filtered_subscriptions.empty
    ):

        temp_revenue = filtered_subscriptions.merge(

            filtered_customers[
                ["customer_id", "segment"]
            ],

            on="customer_id",
            how="left"

        )

        temp_revenue["segment"] = (
            temp_revenue["segment"]
            .fillna("Not Provided")
        )

        segment_revenue = (
            temp_revenue
            .groupby("segment")["monthly_price"]
            .sum()
        )

        if not segment_revenue.empty:

            top_segment = segment_revenue.idxmax()
            top_segment_value = segment_revenue.max()

            top_segment_text = (
                f"{top_segment} "
                f"(${top_segment_value:,.0f} MRR)"
            )


    # TOP ACQUISITION SOURCE

    top_source_text = "No acquisition data"

    if (
        "source" in filtered_events.columns
        and "event_type" in filtered_events.columns
    ):

        signup_events = filtered_events[
            filtered_events["event_type"]
            .astype(str)
            .str.lower()
            == "signup"
        ]

        if not signup_events.empty:

            source_counts = (
                signup_events
                .groupby("source")["customer_id"]
                .nunique()
            )

            if not source_counts.empty:

                top_source = source_counts.idxmax()
                top_source_value = source_counts.max()

                top_source_text = (
                    f"{top_source} "
                    f"({top_source_value:,} signups)"
                )


    # RISK LEVEL

    if churn_rate > 20:

        risk_level = "🔴 High"

    elif churn_rate > 10:

        risk_level = "🟡 Moderate"

    else:

        risk_level = "🟢 Stable"


    with insight_col1:

        st.markdown(
            f"""
            <div class="insight-box">
            <b>🏆 Top Revenue Segment</b><br>
            {top_segment_text}
            </div>
            """,
            unsafe_allow_html=True
        )


    with insight_col2:

        st.markdown(
            f"""
            <div class="insight-box">
            <b>📣 Best Acquisition Channel</b><br>
            {top_source_text}
            </div>
            """,
            unsafe_allow_html=True
        )


    with insight_col3:

        st.markdown(
            f"""
            <div class="insight-box">
            <b>🛡️ Customer Health</b><br>
            {risk_level} churn risk
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # MRR BY MONTH
    # --------------------------------------------------------

    with col1:

        st.markdown("### 💰 MRR Trend")

        if (
            "start_date" in active_subscriptions.columns
            and not active_subscriptions.empty
        ):

            mrr_data = active_subscriptions.copy()

            mrr_data["month"] = (
                mrr_data["start_date"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly_mrr = (
                mrr_data
                .groupby("month", as_index=False)["monthly_price"]
                .sum()
            )

            fig = px.line(
                monthly_mrr,
                x="month",
                y="monthly_price",
                markers=True,
                labels={
                    "monthly_price": "MRR",
                    "month": "Month"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                height=400,
                margin=dict(l=20, r=20, t=30, b=20)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No subscription date data available.")


    # --------------------------------------------------------
    # CUSTOMER SEGMENT
    # --------------------------------------------------------

    with col2:

        st.markdown("### 👥 Customers by Segment")

        if "segment" in filtered_customers.columns:

            segment_data = (
                filtered_customers["segment"]
                .fillna("Not Provided")
                .value_counts()
                .reset_index()
            )

            segment_data.columns = [
                "Segment",
                "Customers"
            ]

            fig = px.pie(
                segment_data,
                names="Segment",
                values="Customers",
                hole=0.45
            )

            fig.update_layout(
                template="plotly_dark",
                height=400,
                margin=dict(l=20, r=20, t=30, b=20)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # --------------------------------------------------------
    # COUNTRY DISTRIBUTION
    # --------------------------------------------------------

    st.markdown("### 🌍 Customer Distribution by Country")

    if "country" in filtered_customers.columns:

        country_data = (
            filtered_customers["country"]
            .fillna("Not Provided")
            .value_counts()
            .head(10)
            .reset_index()
        )

        country_data.columns = [
            "Country",
            "Customers"
        ]

        fig = px.bar(
            country_data,
            x="Country",
            y="Customers",
            text="Customers"
        )

        fig.update_layout(
            template="plotly_dark",
            height=400,
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TAB 2 - FUNNEL ANALYSIS
# ============================================================

with tab2:

    st.subheader("🔻 Customer Funnel Analysis")

    all_customer_ids = set(
        filtered_customers["customer_id"]
        .dropna()
        .unique()
    )

    signup_count = len(all_customer_ids)

    trial_customer_ids = set()

    if "event_type" in filtered_events.columns:

        trial_customer_ids = set(

            filtered_events[
                filtered_events["event_type"]
                .astype(str)
                .str.lower()
                == "trial_start"
            ]["customer_id"]
            .dropna()
            .unique()

        )


    activated_customer_ids = set()

    if "event_type" in filtered_events.columns:

        activated_customer_ids = set(

            filtered_events[
                filtered_events["event_type"]
                .astype(str)
                .str.lower()
                == "activated"
            ]["customer_id"]
            .dropna()
            .unique()

        )


    paid_customer_ids = set(
        filtered_subscriptions[
            "customer_id"
        ]
        .dropna()
        .unique()
    )


    churned_customer_ids = set(
        canceled_subscriptions[
            "customer_id"
        ]
        .dropna()
        .unique()
    )


    funnel_data = pd.DataFrame({

        "Stage": [
            "Signup",
            "Trial",
            "Activated",
            "Paid",
            "Churned"
        ],

        "Customers": [
            signup_count,
            len(trial_customer_ids),
            len(activated_customer_ids),
            len(paid_customer_ids),
            len(churned_customer_ids)
        ]

    })


    fig = px.funnel(
        funnel_data,
        y="Stage",
        x="Customers",
        text="Customers"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    if len(paid_customer_ids) > len(activated_customer_ids):

        st.warning(
            "⚠️ Data Quality Finding: Paying customers exceed "
            "customers with recorded activation events. "
            "This suggests missing or incomplete activation tracking."
        )


    c1, c2, c3, c4 = st.columns(4)

    trial_rate = (
        len(trial_customer_ids)
        / signup_count * 100
        if signup_count > 0
        else 0
    )

    activation_rate = (
        len(activated_customer_ids)
        / len(trial_customer_ids) * 100
        if len(trial_customer_ids) > 0
        else 0
    )

    paid_rate = (
        len(paid_customer_ids)
        / signup_count * 100
        if signup_count > 0
        else 0
    )


    with c1:
        st.metric(
            "Signup → Trial",
            f"{trial_rate:.1f}%"
        )

    with c2:
        st.metric(
            "Trial → Activated",
            f"{activation_rate:.1f}%"
        )

    with c3:
        st.metric(
            "Signup → Paid",
            f"{paid_rate:.1f}%"
        )

    with c4:
        st.metric(
            "Paid → Churn",
            f"{churn_rate:.1f}%"
        )


# ============================================================
# TAB 3 - REVENUE & CHURN
# ============================================================

with tab3:

    st.subheader("💰 Revenue & Customer Churn")

    col1, col2 = st.columns(2)


    # REVENUE BY SEGMENT

    with col1:

        st.markdown("### Revenue by Customer Segment")

        if (
            "segment" in filtered_customers.columns
            and not filtered_subscriptions.empty
        ):

            revenue_segment = filtered_subscriptions.merge(

                filtered_customers[
                    ["customer_id", "segment"]
                ],

                on="customer_id",
                how="left"

            )

            revenue_segment["segment"] = (
                revenue_segment["segment"]
                .fillna("Not Provided")
            )

            revenue_by_segment = (

                revenue_segment
                .groupby("segment", as_index=False)
                ["monthly_price"]
                .sum()

            )

            fig = px.bar(

                revenue_by_segment,

                x="segment",

                y="monthly_price",

                text="monthly_price",

                labels={

                    "segment": "Customer Segment",

                    "monthly_price": "Monthly Revenue"

                }

            )

            fig.update_layout(

                template="plotly_dark",

                height=400

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )


    # SUBSCRIPTION STATUS

    with col2:

        st.markdown("### Subscription Status")

        if "status" in filtered_subscriptions.columns:

            status_data = (

                filtered_subscriptions["status"]

                .fillna("Unknown")

                .value_counts()

                .reset_index()

            )

            status_data.columns = [

                "Status",

                "Subscriptions"

            ]

            fig = px.pie(

                status_data,

                names="Status",

                values="Subscriptions",

                hole=0.4

            )

            fig.update_layout(

                template="plotly_dark",

                height=400

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )


    st.divider()

    st.markdown("### ⚠️ Revenue at Risk")

    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(

            "At-Risk Customers",

            f"{at_risk_customers:,}"

        )


    with c2:

        st.metric(

            "MRR at Risk",

            f"${revenue_at_risk:,.0f}"

        )


    with c3:

        risk_percentage = (

            revenue_at_risk / total_mrr * 100

            if total_mrr > 0

            else 0

        )

        st.metric(

            "Revenue Exposure",

            f"{risk_percentage:.1f}%"

        )


    if not risk_subscriptions.empty:

        risk_display_columns = [

            col for col in [

                "subscription_id",

                "customer_id",

                "monthly_price",

                "status"

            ]

            if col in risk_subscriptions.columns

        ]

        st.dataframe(

            risk_subscriptions[
                risk_display_columns
            ],

            use_container_width=True,

            height=300

        )


# ============================================================
# TAB 4 - ACQUISITION ANALYSIS
# ============================================================

with tab4:

    st.subheader("📣 Acquisition Channel Performance")

    if (

        "source" in filtered_events.columns

        and "event_type" in filtered_events.columns

    ):

        signup_events = filtered_events[

            filtered_events["event_type"]

            .astype(str)

            .str.lower()

            == "signup"

        ].copy()


        if not signup_events.empty:

            source_data = (

                signup_events

                .groupby("source")["customer_id"]

                .nunique()

                .reset_index()

            )

            source_data.columns = [

                "Source",

                "Signups"

            ]

            source_data = source_data.sort_values(

                "Signups",

                ascending=False

            )


            col1, col2 = st.columns(2)


            with col1:

                fig = px.bar(

                    source_data,

                    x="Source",

                    y="Signups",

                    text="Signups"

                )

                fig.update_layout(

                    template="plotly_dark",

                    height=450

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )


            with col2:

                fig = px.pie(

                    source_data,

                    names="Source",

                    values="Signups",

                    hole=0.45

                )

                fig.update_layout(

                    template="plotly_dark",

                    height=450

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )


            st.markdown("### 📊 Channel Performance Table")

            st.dataframe(

                source_data,

                use_container_width=True

            )

        else:

            st.info(
                "No signup events available for acquisition analysis."
            )

    else:

        st.info(
            "Source or event type data is unavailable."
        )


# ============================================================
# TAB 5 - DATA QUALITY & RISK
# ============================================================

with tab5:

    st.subheader("🚨 Data Quality & Business Insights")

    col1, col2, col3 = st.columns(3)


    # MISSING VALUES

    missing_segment = 0

    if "segment" in customers.columns:

        missing_segment = (
            customers["segment"]
            .isna()
            .sum()
        )


    missing_country = 0

    if "country" in customers.columns:

        missing_country = (
            customers["country"]
            .isna()
            .sum()
        )


    missing_source = 0

    if "source" in events.columns:

        missing_source = (
            events["source"]
            .isna()
            .sum()
        )


    with col1:

        st.metric(
            "Missing Segments",
            f"{missing_segment:,}"
        )


    with col2:

        st.metric(
            "Missing Countries",
            f"{missing_country:,}"
        )


    with col3:

        st.metric(
            "Missing Sources",
            f"{missing_source:,}"
        )


    st.divider()

    st.markdown("### 🔍 Automated Business Insights")


    if paid_customers > len(activated_customer_ids):

        tracking_gap = (
            paid_customers
            - len(activated_customer_ids)
        )

        st.warning(

            f"""
            **Activation Tracking Gap Detected**

            {tracking_gap:,} paying customers do not have a recorded
            activation event.

            This can cause the Activated → Paid funnel conversion
            to exceed 100%.

            **Business Recommendation:** Review event tracking
            implementation and activation instrumentation.
            """

        )


    if churn_rate > 20:

        st.error(

            f"""
            **High Churn Alert**

            Current churn rate is {churn_rate:.1f}%.

            Consider analyzing churn by customer segment,
            acquisition source, and subscription value.
            """

        )

    else:

        st.success(

            f"""
            **Churn Status: Stable**

            Current churn rate is {churn_rate:.1f}%,
            which is currently within an acceptable range
            based on this dataset.
            """

        )


    if revenue_at_risk > 0:

        st.warning(

            f"""
            **Revenue Risk Opportunity**

            ${revenue_at_risk:,.0f} in monthly recurring revenue
            is associated with active paying customers who
            do not have a recorded activation event.

            These customers may require targeted onboarding
            or engagement campaigns.
            """

        )


    st.divider()


    # --------------------------------------------------------
    # DOWNLOAD FILTERED DATA
    # --------------------------------------------------------

    st.markdown("### 📥 Export Filtered Customer Data")

    csv = filtered_customers.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="⬇️ Download Filtered Customers CSV",

        data=csv,

        file_name="saas_gtm_filtered_customers.csv",

        mime="text/csv",

        use_container_width=True

    )


    # --------------------------------------------------------
    # DATABASE SUMMARY
    # --------------------------------------------------------

    st.markdown("### 🗄️ Live Database Summary")

    database_summary = pd.DataFrame({

        "Table": [

            "cleaned_customers",

            "cleaned_events",

            "cleaned_subscriptions"

        ],

        "Records": [

            len(customers),

            len(events),

            len(subscriptions)

        ]

    })


    st.dataframe(

        database_summary,

        use_container_width=True

    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚀 SaaS GTM Intelligence | "
    "MySQL + Python + Streamlit + Power BI | "
    "End-to-End Data Analytics Portfolio Project"
)