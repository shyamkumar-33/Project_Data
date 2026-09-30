# ============================================================
# CART2INSIGHTS - QUERIES.PY
# ============================================================


# ============================================================
# DATABASE CONNECTION TEST
# ============================================================

SHOW_TABLES = """
SHOW TABLES;
"""


# ============================================================
# 1. BUSINESS OVERVIEW
# ============================================================

BUSINESS_OVERVIEW = """
SELECT

    (
        SELECT COUNT(*)
        FROM customers
    ) AS total_customers,

    (
        SELECT COUNT(*)
        FROM orders
    ) AS total_orders,

    (
        SELECT COUNT(*)
        FROM products
    ) AS total_products,

    (
        SELECT COUNT(*)
        FROM sellers
    ) AS total_sellers,

    (
        SELECT ROUND(SUM(payment_value), 2)
        FROM order_payments
    ) AS total_revenue,

    (
        SELECT ROUND(
            SUM(payment_value) /
            COUNT(DISTINCT order_id),
            2
        )
        FROM order_payments
    ) AS average_order_value;
"""


# ============================================================
# 2. SALES ANALYSIS
# ============================================================

ORDERS_BY_STATUS = """
SELECT
    order_status,
    COUNT(*) AS total_orders

FROM orders

GROUP BY order_status

ORDER BY total_orders DESC;
"""


REVENUE_BY_PAYMENT = """
SELECT
    payment_type,
    ROUND(
        SUM(payment_value),
        2
    ) AS revenue

FROM order_payments

GROUP BY payment_type

ORDER BY revenue DESC;
"""


# IMPORTANT:
# %% is used instead of % because PyMySQL processes
# the SQL string before sending it to MySQL.

MONTHLY_REVENUE = """
SELECT

    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%%Y-%%m'
    ) AS month,

    ROUND(
        SUM(p.payment_value),
        2
    ) AS revenue

FROM orders o

JOIN order_payments p
    ON o.order_id = p.order_id

GROUP BY month

ORDER BY month;
"""


MONTHLY_ORDERS = """
SELECT

    DATE_FORMAT(
        order_purchase_timestamp,
        '%%Y-%%m'
    ) AS month,

    COUNT(*) AS total_orders

FROM orders

GROUP BY month

ORDER BY month;
"""


# ============================================================
# 3. CUSTOMER ANALYSIS
# ============================================================

CUSTOMERS_BY_STATE = """
SELECT

    customer_state,

    COUNT(*) AS total_customers

FROM customers

GROUP BY customer_state

ORDER BY total_customers DESC;
"""


TOP_CUSTOMER_CITIES = """
SELECT

    customer_city,

    customer_state,

    COUNT(*) AS total_customers

FROM customers

GROUP BY
    customer_city,
    customer_state

ORDER BY total_customers DESC

LIMIT 10;
"""


CUSTOMERS_BY_STATE_REVENUE = """
SELECT

    c.customer_state,

    ROUND(
        SUM(p.payment_value),
        2
    ) AS revenue

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_payments p
    ON o.order_id = p.order_id

GROUP BY c.customer_state

ORDER BY revenue DESC;
"""


# ============================================================
# 4. PRODUCT ANALYSIS
# ============================================================

TOP_PRODUCT_CATEGORIES = """
SELECT

    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,

    COUNT(*) AS items_sold

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN product_category_name_translation t
    ON p.product_category_name =
       t.product_category_name

GROUP BY category

ORDER BY items_sold DESC

LIMIT 10;
"""


CATEGORY_REVENUE = """
SELECT

    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,

    ROUND(
        SUM(oi.price),
        2
    ) AS revenue

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN product_category_name_translation t
    ON p.product_category_name =
       t.product_category_name

GROUP BY category

ORDER BY revenue DESC

LIMIT 10;
"""


PRODUCT_PHYSICAL_STATS = """
SELECT

    ROUND(
        AVG(product_weight_g),
        2
    ) AS average_weight_g,

    ROUND(
        AVG(product_length_cm),
        2
    ) AS average_length_cm,

    ROUND(
        AVG(product_height_cm),
        2
    ) AS average_height_cm,

    ROUND(
        AVG(product_width_cm),
        2
    ) AS average_width_cm

FROM products;
"""


# ============================================================
# 5. SELLER ANALYSIS
# ============================================================

TOP_SELLERS = """
SELECT

    seller_id,

    COUNT(*) AS items_sold

FROM order_items

GROUP BY seller_id

ORDER BY items_sold DESC

LIMIT 10;
"""


SELLER_REVENUE = """
SELECT

    seller_id,

    ROUND(
        SUM(price),
        2
    ) AS revenue

FROM order_items

GROUP BY seller_id

ORDER BY revenue DESC

LIMIT 10;
"""


# ============================================================
# 6. DELIVERY ANALYSIS
# ============================================================

AVERAGE_DELIVERY = """
SELECT

    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS average_delivery_days

FROM orders

WHERE
    order_delivered_customer_date IS NOT NULL;
"""


DELIVERY_PERFORMANCE = """
SELECT

    CASE

        WHEN order_delivered_customer_date >
             order_estimated_delivery_date

        THEN 'Late'

        ELSE 'On Time'

    END AS delivery_status,

    COUNT(*) AS total_orders

FROM orders

WHERE
    order_delivered_customer_date IS NOT NULL

    AND order_estimated_delivery_date IS NOT NULL

GROUP BY delivery_status;
"""


DELIVERY_BY_STATE = """
SELECT

    c.customer_state,

    ROUND(
        AVG(
            DATEDIFF(
                o.order_delivered_customer_date,
                o.order_purchase_timestamp
            )
        ),
        2
    ) AS average_delivery_days

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

WHERE
    o.order_delivered_customer_date IS NOT NULL

GROUP BY c.customer_state

ORDER BY average_delivery_days DESC;
"""


# ============================================================
# 7. CUSTOMER EXPERIENCE
# ============================================================

REVIEW_SCORES = """
SELECT

    review_score,

    COUNT(*) AS total_reviews

FROM order_reviews

GROUP BY review_score

ORDER BY review_score;
"""


AVERAGE_REVIEW = """
SELECT

    ROUND(
        AVG(review_score),
        2
    ) AS average_review_score

FROM order_reviews;
"""


REVIEW_SCORE_BY_DELIVERY = """
SELECT

    r.review_score,

    COUNT(*) AS total_reviews

FROM order_reviews r

GROUP BY r.review_score

ORDER BY r.review_score;
"""


# ============================================================
# 8. PAYMENT ANALYSIS
# ============================================================

PAYMENT_TYPE_COUNTS = """
SELECT

    payment_type,

    COUNT(*) AS total_payments

FROM order_payments

GROUP BY payment_type

ORDER BY total_payments DESC;
"""


PAYMENT_INSTALLMENTS = """
SELECT

    payment_installments,

    COUNT(*) AS total_orders

FROM order_payments

GROUP BY payment_installments

ORDER BY payment_installments;
"""
