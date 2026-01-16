# Database Assignment Report - COM711

## Project Overview
Implementation of a comprehensive database system for Orinoco Electronics, an online electronics shopping company. This assessment required practical database application development work meeting specified requirements, including SQL queries, database design extension, Python application development, and research.

**Student:** Octavio Silva  
**Module:** Databases (COM711)  
**Tutor:** Kenton Wheeler  
**Date:** 03/01/25  
**University:** Solent University  
**Program:** MSc Computer Engineering

---

## Part 1 - Retrieving Data using SQL

### Question A: Marketing Campaign Targeting

#### SQL Code
```sql
SELECT shopper_first_name AS [Shopper First Name],
shopper_surname AS [Shopper Surname],
shopper_email_address AS [Email Address],
ifnull(gender, 'Not known') AS [Gender],
strftime('%d-%m-%Y', date_joined) AS [Date Joined],
CAST((strftime('%Y', 'now') - strftime('%Y', date_of_birth)) AS INT) -
(strftime('%m-%d', 'now') < strftime('%m-%d', date_of_birth)) AS [Age]
FROM shoppers
WHERE (date_joined >= '2020-01-01') OR gender = 'F'
ORDER BY gender, date_of_birth ASC
```
### Explanation
The SELECT clause highlights the requested columns, in this case, the name of the shoppers, email address, gender, date joined and age. The STRFTIME function changes the default order the time format to any depending on the user and the request, the CAST clause alongside the STRFTIME function in the first line calculates the difference between the current year and the year of birth, and the second line checks if the current date is before the birthdate of the current year for better accuracy. The FROM clause selects an entity containing the attributes present in the SELECT Clause, the WHERE clause filters the table for better accuracy, and ORDER BY organises the table according to the data present in the attribute.

![alt text](../screenshots\image.png)

### Question B: Customer Account History

#### SQL Code
```sql
SELECT s.shopper_first_name AS [Shopper First Name],
s.shopper_surname AS [Shopper Surname],
so.order_id AS [Order ID],
strftime('%d-%m-%Y', order_date) AS [Order Date],
p.product_description AS [Product Descriptions],
se.seller_Name AS [Seller Name],
op.quantity AS [QTY Ordered],
PRINTF('£%.2f', op.price) AS [Price],
op.ordered_product_status AS [Order Status]
FROM shoppers AS s
JOIN shopper_orders AS so
ON s.shopper_id = so.shopper_id
JOIN ordered_products AS op
ON so.order_id = op.order_id
JOIN products AS p
ON op.product_id = p.product_id
JOIN sellers AS se
ON op.seller_id = se.seller_id
WHERE s.shopper_id = 10000 OR s.shopper_id = 10019
ORDER BY order_date DESC
```
### Explanation
The SELECT clause in this instance gathers all attributes from various different entities with a suffix attached at the start of them. These suffixes, as used in the clauses and functions FROM, JOIN, and ON, are used for connecting the tables and link foreign keys for better readability and concise overlap between data. The WHERE Clause filters the specific shoppers the question requests by their IDs, and the ORDER clause sorts these customers by the most recent one.

![alt text](../screenshots\image-1.png)

**Testing**: By adding "SELECT s.shopper_id", the last column showed me all the result relation to the recurring customer.

![alt text](../screenshots\image-2.png)

### Question C: Sales Summary Report

#### SQL Code
```sql
SELECT s.seller_account_ref AS [Seller Account Ref],
s.seller_name AS [Seller Name],
ifnull(p.product_code, '0') AS [Product Code],
ifnull(p.product_description, '0') AS [Product Decription],
COUNT(DISTINCT op.order_id) AS [No. Of Orders],
COALESCE(SUM(op.quantity), 0) AS [Total Quantity Sold],
COALESCE(printf('£%.2f', ROUND(SUM(op.quantity * op.price), 2)),
'£0.00') AS [Total Value of Sales]
FROM sellers AS s
LEFT JOIN product_sellers AS ps
ON s.seller_id = ps.seller_id
LEFT JOIN products AS p
ON ps.product_id = p.product_id
LEFT JOIN ordered_products AS op
ON ps.product_id = op.product_id AND ps.seller_id = op.seller_id
GROUP BY s.seller_account_ref,
s.seller_name,
p.product_code,
p.product_description
ORDER BY s.seller_name,
p.product_description;
```
### Explanation
Similar to Question B, the SELECT gathers all attributes from various entities with a suffix attached at the start of them simplify table linking. The IFFNULL function is to showcase any NULL value to 0 as requested by the question. The COUNT clause calculates the number of a specific column, the COALESCE function is another method of handling NULL values, the FROM clause defines the tables as a single letter for simplicity again, the LEFT JOIN clause joins tables containing all of the data from the left one with matching data from the right one alongside unmatched data, the GROUP BY clause organises the columns in a specific order, and the ORDER BY sorts selected columns by their similarities.

![alt text](../screenshots\image-3.png)

**Testing**: The result at first showed incomplete data, so I added "ifnull(p.product_code, '0')" and "ifnull(p.product_description, '0')" to show NULL values as 0 as requested by the question.

![alt text](../screenshots\image-4.png)
![alt text](../screenshots\image-5.png)

### Question D: Product Performance Analysis

#### SQL Code
```sql
SELECT c.category_description as [Category Description],
p.product_code AS [Product Code],
p.product_description AS [Product Description],
ROUND(COALESCE(pa.avg_quantity, 0), 2) AS [Avg Qty Sold],
ROUND(ca.avg_quantity, 2) AS [Avg Qty Sold for Category]
FROM products AS p
LEFT JOIN categories AS c
ON p.category_id = c.category_id
LEFT JOIN (SELECT product_id,
AVG(quantity) AS avg_quantity
FROM ordered_products
WHERE ordered_product_status <> 'Cancelled'
GROUP BY product_id) AS pa
ON p.product_id = pa.product_id
LEFT JOIN (SELECT c.category_id,
AVG(op.quantity) AS avg_quantity
FROM ordered_products AS op
JOIN products AS p
ON op.product_id = p.product_id
JOIN categories AS c
ON p.category_id = c.category_id
WHERE op.ordered_product_status <> 'Cancelled'
GROUP BY c.category_id) AS ca ON c.category_id = ca.category_id
WHERE COALESCE(pa.avg_quantity, 0) < ca.avg_quantity OR pa.avg_quantity IS NULL
ORDER BY c.category_description,
p.product_description;
```
### Explanation
The SELECT follows a structure similar to question B and C, gathering attributes from multiple entities with a suffix positioned at the start to simplify table linking. Within the LEFT JOINS clause, the FROM, JOIN and ON functions serve for shortening the linking between the entities and attributes. The WHERE clause with the COALESCE function work in tandem to work out the NULL values and determine the average quantity sold that is less than the average quantity sold for the category that the product is in, and finally, the ORDER BY clause is used to sort similarities within the column.

![alt text](../screenshots\image-6.png)

---

## Part 2 - Database Design, Implementation and Integrity

### Question A: Table Design

#### Design Process
First, to implement a fully thought-out review system, I had to consider the highest-level relationships between different entities and how they would all interact with each other. The key ones identified immediately were the seller, the products from the existing table, the review system, the rating system and the comment system. Once I defined these as the main entities, it was time for establishing the attributes and keys.

For the attributes I focused on simplicity, and researched simple yet robust reviews systems like Amazon for example, and from there it was easy to establish key attributes for each entity, and for the keys, I had the knowledge of this table being developed as an extension of an existing one, so I focused on overlapping existing keys into this new system to make the implementation as flawless as possible.

From there onwards, table names, column names and data types were established in accordance to the type of attribute each was representing.

#### Design Assumptions
1. Each review must be star-rated with values 1-5 representing Poor to Excellent
2. Reviews can be left for both sellers and products separately
3. Questions about products can be answered by both shoppers and sellers
4. Questions can have multiple answers from different users
5. All timestamps should be automatically recorded

### Question B: Entity Relationship Diagram
All of the tables featured on the top make part of the existing shopping database, while the new tables are the ones that I've designed. When it comes to integration, 3 tables are the most crucial in establishing a connection, seller_review, shopper_comments, and reviews. The review table includes a foreign key from the products table, which together share a one-to-many connections, as the shops features many products, the seller_reviews established contact with the sellers table containing all of the sellers' information for reviewing products, and the shopper_comments links with the shopper table, giving it access to the shopppers' information so they can leave comments or comment anonymously.

![alt text](../screenshots\image-8.png)

---

## Part 3 - Programming for Databases

### System Architecture
The Python application connects to the SQLite database and provides an interactive shopping interface. The system follows a modular approach with clear separation of concerns between database connectivity, business logic, and user interface layers.

### Core Functionality Implemented
1. **User Authentication**
* Shopper ID validation
* Welcome message with personalized greeting
* Error handling for invalid IDs

2. **Order History Display (Option 1)**
* Complete order history retrieval
* Multi-item order formatting
* "No orders" message for new customers
* Chronological sorting (most recent first)

![alt text](../screenshots\image-9.png)

3. **Shopping Basket Management (Options 2 & 3)**
* Category-based product browsing
* Seller selection with price comparison
* Quantity validation
* Real-time basket calculation
* Persistent basket storage

![alt text](../screenshots\image-10.png)
![alt text](../screenshots\image-11.png)
![alt text](../screenshots\image-12.png)

4. **System Exit (Option 5)**
* Clean program termination
* Database connection closure

![alt text](../screenshots\image-13.png)

### Technical Implementation Details

#### Database Connection
```python
import sqlite3
conn = sqlite3.connect('assessment_COM711.db')
cursor = conn.cursor()
```
#### User Input Processing
The program uses structured input validation and error handling to ensure robust user interaction, preventing crashes from invalid inputs.

#### Transaction Management
Database transactions are properly managed with commit and rollback operations to maintain data integrity.

## Evaluation Report
For the overall assessment, I believe I've done the proper job of analyzing a question, dissect it, and present all that has been request, but at the same time I admit that I've also faced challenges I struggled with throughout the entire assessment.

### SQL Queries Performance
For the SQL Queries, the first 3 questions I was able to complete with relative ease, as I partook in an iterative approach of testing and retesting the code until I reached the desired result, but for the last one I felt its difficulty and even requested the help of a friend how is knowledgeable in SQL to guide me through and explained the process to get to the requested result.

### Database Design Approach
For part 2 of designing a table for the database, I was more throughout in my approach to not disrupt the flow of the existing one, and by using the flow of conceptual, logical and physical design, I believe I created an appropriate table that complemented and further enhanced the existing one.

## Research Report

### Introduction
The increased demand for efficient data handling paired with the rapidly evolving landscape of technological advancements bodes well with the existing robust solutions found for system management, but taking into account how the overall data management shares overlap with emergent technologies, the near future promises paramount access to new discoveries and methods to efficiently perform more complex methods, and some of them are the following.

### Serverless Databases
While not a new concept, it's been surging for quite some time now, and while the name may suggest no servers at all, it instead suggests the methods of giving the responsibility to someone else for handling, maintaining and managing the infrastructure of your own database. This option presents tremendous scalability and efficient cost use depending on the complexity of the service.

### AI and Machine Learning Integration
These past few years, advancements in artificial intelligence and machine learning have been significant, and in the case of database management, many benefits arise from both their inclusion. For example, AI and ML enhance data analysis by employing language and image processing algorithms on various datasets to provide a quicker and detailed responses, data optimisation provides efficient operation, reduced response times and minimal resource conception by optimizing data storage strategies and query execution times, and both together can provide personalised systems for different use cases such as e-commerce, finance, healthcare, education, automation.

### Blockchain integration
For this use case, these sorts of databases can store transactional data by default. This means by default, these databases can be used for data storage and retrieval whenever additional features need to be implemented. In other words, blockchain databases offer a new approach of data safety, as it ensures decentralized methods and eliminates the need of a central authority in command of it.

### Conclusion
As highlighted above, the following advancements provide a new way of interacting with databases and managing its data. It can be as simple as using artificial intelligence and machine learning for more efficient use of data handling, to more expansive and complex systems such as blockchain and processing a decentralized database system amongst the more established services. In the following years there's a tangible opportunity of these main three becoming widely adopted as time passes, and as soon as adopt them, the quicker we will witness further advancements from the ones we've adopted for use.

## References

1. McQuillan, R. (2023). The Future of Databases | 8 Data Management Trends. budibase.com. Available at: https://budibase.com/blog/data/data-management-trends/

2. EMB, T. (2024). Emerging Trends in Database Management Systems. Available at: https://blog.emb.global/emerging-trends-in-database-management-systems/

3. www.redswitches.com. (2023). Emerging Trends In Databases: Multi Model Databases & More. Available at: https://www.redswitches.com/blog/database-trends/

## Learning Outcomes Achieved

This assessment enabled demonstration of the following learning outcomes:

1. **Understand the importance and role of relational databases in modern IT systems**
* Practical implementation of e-commerce database
* Real-world business requirements analysis

2. **Have a good understanding of the SQL language and be able to write a range of SQL queries to meet specific reporting requirements**
* Complex queries with joins, aggregation, and subqueries
* Parameterized queries for dynamic data retrieval
* Data formatting and presentation

3. **Able to design, implement and test relational databases to maintain the integrity of the data**
* Database extension design
* Foreign key relationships
* Data validation constraints

4. **Able to develop applications that securely interact with a backend database**
* Python application with SQLite integration
* User authentication and input validation
* Transaction management and error handling