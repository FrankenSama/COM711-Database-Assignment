# 🎓 COM711 Database Assignment - Orinoco Electronics E-commerce System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/SQLite-3.36%2B-green)
![License](https://img.shields.io/badge/License-MIT-orange)
![GitHub](https://img.shields.io/badge/GitHub-Repository-brightgreen)

A comprehensive database management system project for Solent University's COM711 Databases module, showcasing expertise in SQL optimization, database design, and Python application development for an e-commerce platform.

---

## 📊 Project Highlights

| Aspect | Technologies Used | Key Features |
|------|------------------|--------------|
| **Database** | SQLite, SQL | Complex queries, CTEs, joins, transactions |
| **Application** | Python 3.8+ | Modular design, error handling, user interface |
| **Design** | ER Diagrams | Normalization, integrity constraints, views |
| **Testing** | Manual testing | Query validation, edge cases, user flows |

---

## 🎯 Learning Outcomes Demonstrated

### 1. SQL Mastery
- Complex multi-table joins with aggregation  
- Optimized subqueries and CTEs  
- Data integrity via constraints  
- Business intelligence reporting queries  

### 2. Database Design
- Extended e-commerce schema  
- 3NF normalization  
- Foreign keys and CHECK constraints  
- Scalable views  

### 3. Application Development
- Secure Python–SQLite integration  
- Menu-driven user interface  
- ACID-compliant transactions  
- Robust exception handling  

---

## 🛠️ Technical Implementation

### Database Schema
```sql
-- Core tables
shoppers, products, sellers, categories

-- Transaction tables
shopper_orders, ordered_products, basket_contents

-- Support tables
shopper_delivery_addresses, shopper_payment_cards
```

---

## 🧱 Application Architecture
```
main.py (Entry Point)
├── Database Connection Layer
├── Business Logic Layer
│   ├── Order Management
│   ├── Basket Operations
│   └── Checkout Process
└── Presentation Layer
    └── User Interface
```

---

## 📁 Project Structure
```
COM711-Database-Assignment/
├── main.py
├── database/
│   └── README.md
├── sql/
│   ├── part1_queries.sql
│   ├── part2_design.sql
│   └── test_data.sql
├── docs/
│   ├── report.md
│   └── er_diagram.md
├── screenshots/
│   ├── query_results.png
│   ├── python_output.png
│   └── testing.png
├── src/
│   └── __init__.py
├── tests/
│   └── test_main.py
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- SQLite3 (included with Python)

### Installation
```bash
git clone https://github.com/FrankenSama/COM711-Database-Assignment.git
cd COM711-Database-Assignment

# Place assessment_COM711.db in the database/ folder
python main.py
```

---

## 🧪 Sample Shopper IDs
- **10000** – Has order history and saved addresses  
- **10005** – Multiple payment methods  
- **10010** – No order history  
- **10023** – No saved addresses or cards  

---

## 🔍 Key Features

### 1. SQL Query Excellence
```sql
-- Query A: Demographic targeting
SELECT shopper_first_name AS [Shopper First Name]
FROM shoppers
WHERE date_joined >= '2020-01-01'
   OR gender = 'F';

-- Query B: Parameterized order history
SELECT s.shopper_first_name, so.order_id, p.product_description
FROM shoppers s
JOIN shopper_orders so ON s.shopper_id = so.shopper_id
JOIN ordered_products op ON so.order_id = op.order_id
JOIN products p ON op.product_id = p.product_id
WHERE s.shopper_id = ?;
```

---

### 2. Database Design Extension
```sql
CREATE TABLE seller_reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shopper_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE product_questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    answer_text TEXT
);
```

---

### 3. Python Application
```python
def main():
    conn = sqlite3.connect('assessment_COM711.db')
    cursor = conn.cursor()

    shopper_id = input("Enter shopper ID: ")
    cursor.execute(
        "SELECT * FROM shoppers WHERE shopper_id = ?",
        (shopper_id,)
    )

    while True:
        print("1. Display order history")
        print("2. Add item to basket")
        print("3. View basket")
        print("4. Checkout")
        print("5. Exit")

        choice = input("Select option: ")
```

---

## 📸 Screenshots

| Feature | Description |
|-------|------------|
| SQL Query Results | Complex formatted SQL outputs |
| Python Application | Interactive menu system |
| Database Design | Extended ER diagram |
| Testing Evidence | Validation and edge cases |

---

## 🧪 Testing Methodology

### SQL Testing
- Output validation  
- NULL handling  
- Edge-case testing  

### Application Testing
- Input validation  
- Error handling  
- Transaction integrity  

### Integration Testing
- Full checkout workflow  
- Basket persistence  
- Data consistency  

---

## 📚 Academic Context
- **Module:** COM711 – Databases  
- **University:** Solent University  
- **Program:** MSc Computer Engineering  
- **Date:** January 2025  
- **Tutor:** Kenton Wheeler  

---

## 🏆 Skills Demonstrated

### SQL & Database
- Advanced joins, subqueries, CTEs  
- Normalization and constraints  
- Performance optimization  

### Python Development
- SQLite3 integration  
- Modular design  
- Exception handling  

### Software Engineering
- Requirements analysis  
- Testing & documentation  
- Professional project structure  

---

## 📄 License
MIT License — see `LICENSE` file.

---

## 🤝 Connect
**Octavio Silva**  
GitHub: **@FrankenSama**  
Solent University — MSc Computer Engineering  
