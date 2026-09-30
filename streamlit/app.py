import streamlit as st
import pandas as pd

from database import get_engine
import queries

from utils import (
    format_number,
    format_currency,
    format_decimal
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cart2Insights",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def load_engine():
    return get_engine()


@st.cache_data(ttl=300)
def run_query(query):
    engine = load_engine()

    return pd.read_sql(
        query,
        engine
    )


# ============================================================
# HEADER
# ============================================================

st.title("🛒 Cart2Insights")

st.subheader(
    "E-Commerce Performance Analytics"
)

st.write(
    "An interactive dashboard for analyzing "
    "sales, customers, products, sellers, "
    "delivery performance and customer experience."
)


# ============================================================
# DATABASE CONNECTION TEST
# ============================================================

try:

    engine = load_engine()

    tables = run_query(
        queries.SHOW_TABLES
    )

    st.success(
        "MySQL database connected successfully!"
    )

except Exception as e:

    st.error(
        "Unable to connect to MySQL database."
    )

    st.error(str(e))

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛒 Cart2Insights")

st.sidebar.markdown(
    "### Dashboard Navigation"
)

page = st.sidebar.radio(
    "Select Section",
    [
        "📊 Business Overview",
        "📈 Sales Analysis",
        "👥 Customer Analysis",
        "📦 Product Analysis",
        "🏪 Seller Analysis",
        "🚚 Delivery Analysis",
        "⭐ Customer Experience"
    ]
)

st.sidebar.markdown("---")

st.sidebar.write(
    "Database: cart2insights"
)

st.sidebar.write(
    "Tables: 9"
)


# ============================================================
# 1. BUSINESS OVERVIEW
# ============================================================

if page == "📊 Business Overview":

    st.header(
        "📊 Business Overview"
    )

    overview = run_query(
        queries.BUSINESS_OVERVIEW
    )

    if overview.empty:

        st.warning(
            "No business overview data available."
        )

    else:

        # ------------------------------
        # KPI ROW 1
        # ------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "👥 Total Customers",
                format_number(
                    overview.loc[
                        0,
                        "total_customers"
                    ]
                )
            )

        with col2:

            st.metric(
                "🛒 Total Orders",
                format_number(
                    overview.loc[
                        0,
                        "total_orders"
                    ]
                )
            )

        with col3:

            st.metric(
                "💰 Total Revenue",
                format_currency(
                    overview.loc[
                        0,
                        "total_revenue"
                    ]
                )
            )

        # ------------------------------
        # KPI ROW 2
        # ------------------------------

        col4, col5, col6 = st.columns(3)

        with col4:

            st.metric(
                "📦 Total Products",
                format_number(
                    overview.loc[
                        0,
                        "total_products"
                    ]
                )
            )

        with col5:

            st.metric(
                "🏪 Total Sellers",
                format_number(
                    overview.loc[
                        0,
                        "total_sellers"
                    ]
                )
            )

        with col6:

            st.metric(
                "💳 Average Order Value",
                format_currency(
                    overview.loc[
                        0,
                        "average_order_value"
                    ]
                )
            )

        st.markdown("---")

        st.info(
            "Use the sidebar to explore detailed "
            "sales, customer, product, seller, "
            "delivery and customer experience analysis."
        )


# ============================================================
# 2. SALES ANALYSIS
# ============================================================

elif page == "📈 Sales Analysis":

    st.header(
        "📈 Sales Analysis"
    )

    orders_status = run_query(
        queries.ORDERS_BY_STATUS
    )

    revenue_payment = run_query(
        queries.REVENUE_BY_PAYMENT
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Orders by Status"
        )

        if not orders_status.empty:

            st.bar_chart(
                orders_status.set_index(
                    "order_status"
                )["total_orders"]
            )

    with col2:

        st.subheader(
            "Revenue by Payment Type"
        )

        if not revenue_payment.empty:

            st.bar_chart(
                revenue_payment.set_index(
                    "payment_type"
                )["revenue"]
            )

    st.markdown("---")

    # Monthly Revenue

    st.subheader(
        "Monthly Revenue Trend"
    )

    monthly_revenue = run_query(
        queries.MONTHLY_REVENUE
    )

    if not monthly_revenue.empty:

        monthly_revenue["month"] = pd.to_datetime(
            monthly_revenue["month"]
        )

        monthly_revenue = monthly_revenue.set_index(
            "month"
        )

        st.line_chart(
            monthly_revenue["revenue"]
        )

    st.markdown("---")

    # Monthly Orders

    st.subheader(
        "Monthly Order Trend"
    )

    monthly_orders = run_query(
        queries.MONTHLY_ORDERS
    )

    if not monthly_orders.empty:

        monthly_orders["month"] = pd.to_datetime(
            monthly_orders["month"]
        )

        monthly_orders = monthly_orders.set_index(
            "month"
        )

        st.line_chart(
            monthly_orders["total_orders"]
        )


# ============================================================
# 3. CUSTOMER ANALYSIS
# ============================================================

elif page == "👥 Customer Analysis":

    st.header(
        "👥 Customer Analysis"
    )

    customers_state = run_query(
        queries.CUSTOMERS_BY_STATE
    )

    st.subheader(
        "Customers by State"
    )

    if not customers_state.empty:

        st.bar_chart(
            customers_state.set_index(
                "customer_state"
            )["total_customers"]
        )

    st.markdown("---")

    customer_cities = run_query(
        queries.TOP_CUSTOMER_CITIES
    )

    st.subheader(
        "Top 10 Customer Cities"
    )

    if not customer_cities.empty:

        st.dataframe(
            customer_cities,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            customer_cities.set_index(
                "customer_city"
            )["total_customers"]
        )

    st.markdown("---")

    state_revenue = run_query(
        queries.CUSTOMERS_BY_STATE_REVENUE
    )

    st.subheader(
        "Revenue by Customer State"
    )

    if not state_revenue.empty:

        st.bar_chart(
            state_revenue.set_index(
                "customer_state"
            )["revenue"]
        )


# ============================================================
# 4. PRODUCT ANALYSIS
# ============================================================

elif page == "📦 Product Analysis":

    st.header(
        "📦 Product Analysis"
    )

    top_categories = run_query(
        queries.TOP_PRODUCT_CATEGORIES
    )

    category_revenue = run_query(
        queries.CATEGORY_REVENUE
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Top Product Categories"
        )

        if not top_categories.empty:

            st.bar_chart(
                top_categories.set_index(
                    "category"
                )["items_sold"]
            )

    with col2:

        st.subheader(
            "Revenue by Product Category"
        )

        if not category_revenue.empty:

            st.bar_chart(
                category_revenue.set_index(
                    "category"
                )["revenue"]
            )

    st.markdown("---")

    physical_stats = run_query(
        queries.PRODUCT_PHYSICAL_STATS
    )

    if not physical_stats.empty:

        st.subheader(
            "Product Physical Statistics"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Average Weight",
                f"{format_decimal(physical_stats.loc[0, 'average_weight_g'])} g"
            )

        with col2:

            st.metric(
                "Average Length",
                f"{format_decimal(physical_stats.loc[0, 'average_length_cm'])} cm"
            )

        with col3:

            st.metric(
                "Average Height",
                f"{format_decimal(physical_stats.loc[0, 'average_height_cm'])} cm"
            )

        with col4:

            st.metric(
                "Average Width",
                f"{format_decimal(physical_stats.loc[0, 'average_width_cm'])} cm"
            )


# ============================================================
# 5. SELLER ANALYSIS
# ============================================================

elif page == "🏪 Seller Analysis":

    st.header(
        "🏪 Seller Analysis"
    )

    top_sellers = run_query(
        queries.TOP_SELLERS
    )

    seller_revenue = run_query(
        queries.SELLER_REVENUE
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Top Sellers by Items Sold"
        )

        if not top_sellers.empty:

            st.bar_chart(
                top_sellers.set_index(
                    "seller_id"
                )["items_sold"]
            )

    with col2:

        st.subheader(
            "Top Sellers by Revenue"
        )

        if not seller_revenue.empty:

            st.bar_chart(
                seller_revenue.set_index(
                    "seller_id"
                )["revenue"]
            )

    st.markdown("---")

    st.subheader(
        "Top Sellers - Items Sold"
    )

    st.dataframe(
        top_sellers,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Top Sellers - Revenue"
    )

    st.dataframe(
        seller_revenue,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 6. DELIVERY ANALYSIS
# ============================================================

elif page == "🚚 Delivery Analysis":

    st.header(
        "🚚 Delivery Analysis"
    )

    average_delivery = run_query(
        queries.AVERAGE_DELIVERY
    )

    if not average_delivery.empty:

        average_days = average_delivery.loc[
            0,
            "average_delivery_days"
        ]

        st.metric(
            "Average Delivery Time",
            f"{format_decimal(average_days)} days"
        )

    st.markdown("---")

    delivery_performance = run_query(
        queries.DELIVERY_PERFORMANCE
    )

    st.subheader(
        "On-Time vs Late Deliveries"
    )

    if not delivery_performance.empty:

        st.bar_chart(
            delivery_performance.set_index(
                "delivery_status"
            )["total_orders"]
        )

        st.dataframe(
            delivery_performance,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    delivery_state = run_query(
        queries.DELIVERY_BY_STATE
    )

    st.subheader(
        "Average Delivery Time by State"
    )

    if not delivery_state.empty:

        st.bar_chart(
            delivery_state.set_index(
                "customer_state"
            )["average_delivery_days"]
        )


# ============================================================
# 7. CUSTOMER EXPERIENCE
# ============================================================

elif page == "⭐ Customer Experience":

    st.header(
        "⭐ Customer Experience"
    )

    average_review = run_query(
        queries.AVERAGE_REVIEW
    )

    if not average_review.empty:

        average_score = average_review.loc[
            0,
            "average_review_score"
        ]

        st.metric(
            "Average Review Score",
            f"{format_decimal(average_score)} / 5"
        )

    st.markdown("---")

    review_scores = run_query(
        queries.REVIEW_SCORES
    )

    st.subheader(
        "Customer Review Score Distribution"
    )

    if not review_scores.empty:

        st.bar_chart(
            review_scores.set_index(
                "review_score"
            )["total_reviews"]
        )

        st.dataframe(
            review_scores,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    payment_counts = run_query(
        queries.PAYMENT_TYPE_COUNTS
    )

    st.subheader(
        "Payment Type Distribution"
    )

    if not payment_counts.empty:

        st.bar_chart(
            payment_counts.set_index(
                "payment_type"
            )["total_payments"]
        )