-- ============================================
-- PART 2: DATABASE DESIGN & EXTENSIONS
-- Review and Q&A System Implementation
-- ============================================

-- New Tables for Review System
CREATE TABLE IF NOT EXISTS seller_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shopper_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shopper_id) REFERENCES shoppers(shopper_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

CREATE TABLE IF NOT EXISTS product_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shopper_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shopper_id) REFERENCES shoppers(shopper_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS product_questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    asked_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_anonymous BOOLEAN DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS question_answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    answered_by_shopper_id INTEGER,
    answered_by_seller_id INTEGER,
    answer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES product_questions(question_id),
    FOREIGN KEY (answered_by_shopper_id) REFERENCES shoppers(shopper_id),
    FOREIGN KEY (answered_by_seller_id) REFERENCES sellers(seller_id),
    CHECK (
        (answered_by_shopper_id IS NOT NULL AND answered_by_seller_id IS NULL) OR
        (answered_by_shopper_id IS NULL AND answered_by_seller_id IS NOT NULL)
    )
);

-- Create Views for Simplified Access
CREATE VIEW IF NOT EXISTS seller_performance AS
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(sr.review_id) as total_reviews,
    AVG(sr.rating) as average_rating,
    COUNT(DISTINCT sr.shopper_id) as unique_reviewers
FROM sellers s
LEFT JOIN seller_reviews sr ON s.seller_id = sr.seller_id
GROUP BY s.seller_id, s.seller_name;

CREATE VIEW IF NOT EXISTS product_review_summary AS
SELECT 
    p.product_id,
    p.product_description,
    COUNT(pr.review_id) as review_count,
    AVG(pr.rating) as average_rating,
    COUNT(pq.question_id) as question_count
FROM products p
LEFT JOIN product_reviews pr ON p.product_id = pr.product_id
LEFT JOIN product_questions pq ON p.product_id = pq.product_id
GROUP BY p.product_id, p.product_description;