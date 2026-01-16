# Entity Relationship Diagram Documentation

## Extended Database Schema for Review and Q&A System

### Design Process
First, to implement a fully thought-out review system, I had to consider the highest-level relationships between different entities and how they would all interact with each other. The key ones identified immediately were the seller, the products from the existing table, the review system, the rating system and the comment system. Once I defined these as the main entities, it was time for establishing the attributes and keys.

For the attributes I focused on simplicity, and researched simple yet robust reviews systems like Amazon for example, and from there it was easy to establish key attributes for each entity, and for the keys, I had the knowledge of this table being developed as an extension of an existing one, so I focused on overlapping existing keys into this new system to make the implementation as flawless as possible.

From there onwards, table names, column names and data types were established in accordance to the type of attribute each was representing.

### Integration with Existing Database
All of the tables feature on the top make part of the existing shopping database, while the 5 at the bottom are the ones that I've designed. When it comes to integration, 3 tables are the most crucial in establishing a connection, seller_review, shopper_comments, and reviews. The review table includes a foreign key from the products table, which together share a one-to-many connections, as the shops features many products, the seller_reviews established contact with the sellers table containing all of the sellers' information for reviewing products, and the shopper_comments links with the shopper table, giving it access to the shoppers' information so they can leave comments or comment anonymously.

## Visual Documentation

### Table Design Overview
![alt text](../screenshots\image-14.png)

### Complete ER Diagram
![alt text](../screenshots\image-15.png)

## New Table Structures

### 1. Seller Reviews Table

seller_reviews
├── review_id (PRIMARY KEY, AUTOINCREMENT)
├── shopper_id (FOREIGN KEY → shoppers.shopper_id)
├── seller_id (FOREIGN KEY → sellers.seller_id)
├── rating (INTEGER, 1-5 representing ★ to ★★★★★)
├── comment (TEXT, shopper's review text)
└── review_date (TIMESTAMP, auto-generated)


**Purpose:** Allows shoppers to rate and review sellers based on their service quality, independent of products sold.

### 2. Product Reviews Table

product_reviews
├── review_id (PRIMARY KEY, AUTOINCREMENT)
├── shopper_id (FOREIGN KEY → shoppers.shopper_id)
├── product_id (FOREIGN KEY → products.product_id)
├── rating (INTEGER, 1-5 representing ★ to ★★★★★)
├── comment (TEXT, shopper's review text)
└── review_date (TIMESTAMP, auto-generated)


**Purpose:** Enables shoppers to rate and review specific products they have purchased.

### 3. Product Questions Table

product_questions
├── question_id (PRIMARY KEY, AUTOINCREMENT)
├── product_id (FOREIGN KEY → products.product_id)
├── question_text (TEXT, NOT NULL)
├── asked_date (TIMESTAMP, auto-generated)
└── is_anonymous (BOOLEAN, DEFAULT TRUE)


**Purpose:** Allows shoppers to ask questions about products anonymously.

### 4. Question Answers Table

question_answers
├── answer_id (PRIMARY KEY, AUTOINCREMENT)
├── question_id (FOREIGN KEY → product_questions.question_id)
├── answer_text (TEXT, NOT NULL)
├── answered_by_shopper_id (FOREIGN KEY → shoppers.shopper_id, NULLABLE)
├── answered_by_seller_id (FOREIGN KEY → sellers.seller_id, NULLABLE)
└── answer_date (TIMESTAMP, auto-generated)


**Purpose:** Stores answers to product questions from either shoppers or sellers.

## Key Design Decisions

### 1. Separate Review Tables
**Decision:** Created separate `seller_reviews` and `product_reviews` tables instead of a single reviews table.

**Reason:** Maintains data integrity by avoiding NULL values in a combined table and allows for different review criteria for sellers vs. products.

### 2. Star Rating System
**Decision:** Implemented a 1-5 integer rating system with textual representation:
- 1 = ★ (Poor)
- 2 = ★★ (Fair) 
- 3 = ★★★ (Good)
- 4 = ★★★★ (Very Good)
- 5 = ★★★★★ (Excellent)

**Reason:** Standard industry practice that users are familiar with from platforms like Amazon and eBay.

### 3. Anonymous Questions
**Decision:** Added `is_anonymous` flag to product questions table.

**Reason:** Encourages more questions by allowing shoppers to ask without revealing their identity, increasing product information available to all customers.

### 4. Dual Answer System
**Decision:** Allows answers from both shoppers (based on experience) and sellers (official/product knowledge).

**Reason:** Creates a community-driven knowledge base while maintaining official product information from sellers.

## Relationships Diagram

### Existing Database Relationships

shoppers (1) ─── (M) shopper_orders (1) ─── (M) ordered_products (M) ─── (1) products
│
└── (M) ─── (1) sellers


### New Relationships Added

shoppers (1) ─── (M) seller_reviews (M) ─── (1) sellers
shoppers (1) ─── (M) product_reviews (M) ─── (1) products
products (1) ─── (M) product_questions (1) ─── (M) question_answers
│
├── (M) ─── (1) shoppers
└── (M) ─── (1) sellers


## Data Integrity Constraints

### Primary Keys
- All new tables use `INTEGER PRIMARY KEY AUTOINCREMENT` for unique identification
- Ensures each record can be uniquely identified and referenced

### Foreign Key Constraints
```sql
-- Example foreign key constraint
FOREIGN KEY (shopper_id) REFERENCES shoppers(shopper_id)
FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
FOREIGN KEY (product_id) REFERENCES products(product_id)
FOREIGN KEY (question_id) REFERENCES product_questions(question_id)
```

### Check Constraints
```sql
-- Rating must be between 1 and 5
CHECK (rating BETWEEN 1 AND 5)

-- Answer must be from either a shopper OR a seller, not both
CHECK (
    (answered_by_shopper_id IS NOT NULL AND answered_by_seller_id IS NULL) OR
    (answered_by_shopper_id IS NULL AND answered_by_seller_id IS NOT NULL)
)
```
### Default Values
```sql
-- Auto-generated timestamps
review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
asked_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
answer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

-- Anonymous by default for privacy
is_anonymous BOOLEAN DEFAULT 1
```
## Performance Considerations

### Recommended Indexes
```sql
-- For quick retrieval of seller reviews
CREATE INDEX idx_seller_reviews_seller ON seller_reviews(seller_id, review_date DESC);

-- For product review queries
CREATE INDEX idx_product_reviews_product ON product_reviews(product_id, rating DESC);

-- For recent questions display
CREATE INDEX idx_product_questions_product ON product_questions(product_id, asked_date DESC);

-- For chronological answer display
CREATE INDEX idx_question_answers_question ON question_answers(question_id, answer_date);
```

### Views for Simplified Access
```sql
-- Seller performance summary
CREATE VIEW seller_performance_summary AS
SELECT s.seller_id, s.seller_name,
       COUNT(sr.review_id) AS total_reviews,
       AVG(sr.rating) AS average_rating
FROM sellers s
LEFT JOIN seller_reviews sr ON s.seller_id = sr.seller_id
GROUP BY s.seller_id, s.seller_name;

-- Product review summary
CREATE VIEW product_review_summary AS
SELECT p.product_id, p.product_description,
       COUNT(pr.review_id) AS review_count,
       AVG(pr.rating) AS average_rating
FROM products p
LEFT JOIN product_reviews pr ON p.product_id = pr.product_id
GROUP BY p.product_id, p.product_description;
```

## Migration and Integration Strategy

### 1. Non-Disruptive Implementation

The design maintains backward compatibility by:
* Not modifying existing table structures
* Using separate tables for new functionality
* Maintaining all existing foreign key relationships

### 2. Gradual Rollout
1. Create new tables with constraints
2. Add views for reporting
3. Implement application layer integration
4. Enable feature for users

### 3. Data Validation
* All foreign keys reference existing records
* Rating values validated before insertion
* Question/answer relationships maintained

## Benefits of This Design

### For Shoppers
* Transparent seller and product reviews
* Anonymous Q&A for product inquiries
* Community-driven product knowledge
* Informed purchasing decisions

### For Sellers
* Performance feedback mechanism
* Official product information channel
* Customer engagement opportunities
* Quality improvement insights

### For Platform
* Increased user engagement
* Valuable product and seller data
* Competitive advantage through transparency
* Data for recommendation algorithms

---

This ER diagram and database design extends the Orinoco Electronics shopping platform to include comprehensive review and Q&A functionality while maintaining data integrity and system performance.