-- ============================================
-- PART 1: ADVANCED SQL QUERIES
-- Orinoco Electronics Database
-- ============================================

-- Query A: Marketing Campaign Targeting
SELECT 
    shopper_first_name AS "Shopper First Name",
    shopper_surname AS "Shopper Surname",
    shopper_email_address AS "Email Address",
    COALESCE(gender, 'Not known') AS "Gender",
    strftime('%d-%m-%Y', date_joined) AS "Date Joined",
    CAST(
        (strftime('%Y', 'now') - strftime('%Y', date_of_birth)) -
        (strftime('%m-%d', 'now') < strftime('%m-%d', date_of_birth))
    AS INTEGER) AS "Current Age"
FROM shoppers
WHERE date_joined >= '2020-01-01' OR gender = 'F'
ORDER BY 
    CASE WHEN gender IS NULL THEN 1 ELSE 0 END,
    gender,
    "Current Age" DESC;

-- Query B: Customer Account History (Parameterized)
-- Usage: Replace ? with shopper_id (e.g., 10000 or 10019)
SELECT 
    s.shopper_first_name AS "Shopper First Name",
    s.shopper_surname AS "Shopper Surname",
    so.order_id AS "Order ID",
    strftime('%d-%m-%Y', so.order_date) AS "Order Date",
    p.product_description AS "Product Description",
    se.seller_name AS "Seller Name",
    op.quantity AS "Qty Ordered",
    printf('£%.2f', op.price) AS "Price",
    op.ordered_product_status AS "Order Status"
FROM shoppers s
JOIN shopper_orders so ON s.shopper_id = so.shopper_id
JOIN ordered_products op ON so.order_id = op.order_id
JOIN products p ON op.product_id = p.product_id
JOIN sellers se ON op.seller_id = se.seller_id
WHERE s.shopper_id = ?
ORDER BY so.order_date DESC, so.order_id, p.product_description;

-- Query C: Sales Summary Report
WITH product_sales AS (
    SELECT 
        op.seller_id,
        op.product_id,
        COUNT(DISTINCT op.order_id) as order_count,
        COALESCE(SUM(op.quantity), 0) as total_quantity,
        COALESCE(SUM(op.quantity * op.price), 0) as total_value
    FROM ordered_products op
    JOIN shopper_orders so ON op.order_id = so.order_id
    WHERE so.order_date >= '2019-06-01'
    GROUP BY op.seller_id, op.product_id
)
SELECT 
    s.seller_account_ref AS "Seller Account Ref",
    s.seller_name AS "Seller Name",
    COALESCE(p.product_code, '0') AS "Product Code",
    COALESCE(p.product_description, 'No Product') AS "Product Description",
    COALESCE(ps.order_count, 0) AS "No. of Orders",
    COALESCE(ps.total_quantity, 0) AS "Total Quantity Sold",
    printf('£%.2f', COALESCE(ps.total_value, 0)) AS "Total Value of Sales"
FROM sellers s
LEFT JOIN product_sellers ps_link ON s.seller_id = ps_link.seller_id
LEFT JOIN products p ON ps_link.product_id = p.product_id
LEFT JOIN product_sales ps ON s.seller_id = ps.seller_id 
    AND p.product_id = ps.product_id
WHERE s.seller_id IS NOT NULL
ORDER BY s.seller_name, p.product_description;