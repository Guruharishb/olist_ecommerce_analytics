# Olist E-Commerce Analytics

## Overview

This project is an end-to-end **E-Commerce Data Analytics and ETL Pipeline** built using the public Olist Brazilian E-Commerce dataset.

The project starts with raw CSV datasets and goes through:

```text
Raw CSV Data
     ↓
Data Quality & Validation
     ↓
Data Transformation
     ↓
MySQL Database
     ↓
SQL Analytics
     ↓
Tkinter Desktop Dashboard
```

The main goals of the project are to:

* Understand and validate raw e-commerce data
* Identify missing, duplicate, and inconsistent records
* Transform the datasets into analysis-ready data
* Build a relational MySQL database
* Validate primary-key and foreign-key relationships
* Perform business analysis using SQL
* Build a desktop analytics dashboard using Tkinter
* Package the dashboard as a Windows executable

---

# Dataset

The project uses the public **Olist Brazilian E-Commerce Dataset**.

The datasets used in the project are:

| Dataset                                 | Description                                     |
| --------------------------------------- | ----------------------------------------------- |
| `olist_orders_dataset.csv`              | Order information and order status dates        |
| `olist_customers_dataset.csv`           | Customer information                            |
| `olist_order_items_dataset.csv`         | Products and sellers associated with orders     |
| `olist_products_dataset.csv`            | Product information                             |
| `olist_sellers_dataset.csv`             | Seller information                              |
| `olist_order_payments_dataset.csv`      | Payment information                             |
| `olist_order_reviews_dataset.csv`       | Customer review information                     |
| `olist_geolocation_dataset.csv`         | Brazilian geolocation information               |
| `product_category_name_translation.csv` | Portuguese-English product category translation |

Raw datasets are kept locally under:

```text
data/raw/
```

Large raw datasets are excluded from the Git repository using `.gitignore`.

---

# Project Structure

```text
olist_ecommerce_analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── dashboard.py
│   ├── query.py
│   ├── validation.py
│   └── ...
│
├── sql/
│
├── screenshots/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Technologies Used

* Python
* Pandas
* MySQL
* SQL
* Tkinter
* Matplotlib
* Git
* GitHub
* PyInstaller

---

# 1. Data Quality and Validation

Before loading the data into MySQL, the raw datasets were inspected and validated.

The validation process focuses on:

* Dataset structure
* Missing values
* Duplicate records
* Duplicate identifiers
* Data types
* Date fields
* Referential integrity
* Order status consistency
* Payment data quality
* Primary-key validation
* Composite-key validation

---

## General Dataset Inspection

Each dataset is inspected for:

* Number of rows and columns
* Column names
* Data types
* Missing values
* Duplicate rows
* Unique identifiers
* Sample records

This provides an initial understanding of the datasets before transformation and database loading.

---

# 2. Orders Validation

The orders dataset contains order-level information and timestamps.

### Order Status

The distribution of `order_status` is examined using:

```python
orders["order_status"].value_counts()
```

The dataset contains statuses such as:

* delivered
* shipped
* canceled
* unavailable
* invoiced
* processing
* created
* approved

### Missing Dates

The following date columns are checked:

* `order_purchase_timestamp`
* `order_approved_at`
* `order_delivered_carrier_date`
* `order_delivered_customer_date`
* `order_estimated_delivery_date`

Missing dates are analyzed according to order status because missing delivery-related dates can be expected for orders that were not delivered.

### Date Conversion

Date columns are converted using:

```python
pd.to_datetime(column, errors="coerce")
```

Invalid values are converted to `NaT` instead of stopping the processing pipeline.

### Delivery Time Feature

A new analytical feature was created:

```text
delivery_days
```

It represents the number of days between order purchase and customer delivery.

```python
orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days
```

This feature is later used for delivery analysis.

### Order ID Validation

The following checks are performed:

* Missing `order_id`
* Duplicate `order_id`

The `order_id` behaves as the primary identifier for the orders table.

---

# 3. Customer Validation

The customer dataset is checked for:

* Missing values
* Duplicate rows
* Duplicate `customer_id`
* Missing `customer_id`

## Customer Referential Integrity

Orders are checked against the customer table:

```python
~orders["customer_id"].isin(customers["customer_id"])
```

This validates:

```text
Customers
    │
    │ customer_id
    ↓
Orders
```

No invalid customer references were found during validation.

---

# 4. Order Items Validation

The order items dataset contains products sold within each order.

The dataset is checked for:

* Missing values
* Duplicate rows
* Duplicate order-item combinations
* Invalid product references
* Invalid seller references
* Invalid order references

## Composite Primary Key

`order_id` alone is not unique because an order can contain multiple products.

Therefore, the combination:

```text
order_id + order_item_id
```

is used as the unique identifier.

The composite key was validated for duplicate occurrences.

---

# 5. Product Validation

The products dataset is checked for:

* Missing values
* Duplicate rows
* Duplicate `product_id`
* Missing product categories
* Missing product dimensions
* Missing product weight

Examples:

```python
products["product_category_name"].isna()
```

```python
products["product_weight_g"].isna()
```

Missing product information is retained where appropriate because these values may represent genuinely unavailable source information.

Product information is later used for product and category analysis.

---

# 6. Seller Validation

The sellers dataset is checked for:

* Missing values
* Duplicate rows
* Duplicate `seller_id`
* General data quality

## Seller Referential Integrity

Order items are checked against the seller table:

```python
~order_items["seller_id"].isin(sellers["seller_id"])
```

This validates:

```text
Sellers
    │
    │ seller_id
    ↓
Order Items
```

---

# 7. Payment Validation

The payment dataset is checked for:

* Missing values
* Duplicate records
* Payment types
* Duplicate payment identifiers
* Invalid order references

## Composite Payment Key

An order can have multiple payment records.

Therefore:

```text
order_id + payment_sequential
```

is used as the composite primary key.

The following validation is performed:

```python
payments.duplicated(
    subset=["order_id", "payment_sequential"]
)
```

### Payment Types

Payment methods are analyzed using:

```python
payments["payment_type"].value_counts()
```

The source value `not_defined` was standardized to:

```text
unknown
```

---

# 8. Review Validation

The order reviews dataset was also included in the database pipeline.

The review dataset is checked for:

* Missing values
* Duplicate rows
* Duplicate review identifiers
* Invalid order references
* Review scores
* Review dates

A review is uniquely identified using:

```text
review_id + order_id
```

because `review_id` alone is not guaranteed to be unique.

Review comments are allowed to contain NULL values because customers may submit a review score without providing written comments.

---

# 9. Data Transformation

After validation, the datasets were transformed into analysis-ready data.

Major transformations include:

### Date Conversion

Order timestamps were converted to Pandas datetime values.

### Delivery Duration

A `delivery_days` feature was created.

### Payment Standardization

The `not_defined` payment type was standardized to:

```text
unknown
```

### Processed Data

The transformed datasets are stored locally under:

```text
data/processed/
```

The processed datasets were then validated before loading them into MySQL.

---

# 10. Validation Results

The processed datasets were validated for primary keys, composite keys, and foreign-key references.

| Dataset     |    Rows |
| ----------- | ------: |
| Customers   |  99,441 |
| Products    |  32,951 |
| Sellers     |   3,095 |
| Orders      |  99,441 |
| Order Items | 112,650 |
| Payments    | 103,886 |
| Reviews     |  99,224 |

Validation results:

```text
Duplicate order IDs: 0
Duplicate customer IDs: 0
Duplicate product IDs: 0
Duplicate seller IDs: 0
Duplicate order item keys: 0
Duplicate payment keys: 0
Duplicate review keys: 0
```

Referential-integrity checks:

```text
Orders with missing customers: 0
Order items with missing orders: 0
Order items with missing products: 0
Order items with missing sellers: 0
Payments with missing orders: 0
Reviews with missing orders: 0
```

These checks provide confidence that the processed datasets can be loaded into the relational database.

---

# 11. MySQL Database

The processed data was loaded into a MySQL database:

```text
olist_analytics
```

The database contains the following tables:

```text
customers
products
sellers
orders
order_items
payments
reviews
```

The tables use primary keys, composite primary keys, and foreign keys to maintain relational integrity.

---

# 12. Database Relationships

The main relationships are:

```text
Customers
    │
    │ customer_id
    ↓
Orders
    │
    ├───────────────┐
    │               │
 order_id        order_id
    ↓               ↓
Order Items      Payments
    │
    ├───────────────┐
    │               │
product_id       seller_id
    ↓               ↓
Products         Sellers

Orders
    │
    │ order_id
    ↓
Reviews
```

### Relationships

```text
Customers 1 ─── N Orders

Orders 1 ─── N Order Items

Products 1 ─── N Order Items

Sellers 1 ─── N Order Items

Orders 1 ─── N Payments

Orders 1 ─── N Reviews
```

---

# 13. SQL Business Analysis

After loading the data into MySQL, SQL was used to perform business analysis.

The analysis includes:

* Total orders
* Delivered orders
* Order status distribution
* Total revenue
* Average order value
* Monthly revenue
* Monthly orders
* Top products
* Top sellers
* Top customers
* Payment distribution
* Cancellation rate
* Average delivery time
* Late deliveries
* Repeat customers
* Review analysis

---

## Total Orders

```sql
select count(*)
from orders;
```

---

## Total Revenue

```sql
select sum(payment_value) as total_revenue
from payments;
```

---

## Average Order Value

Payment records are first aggregated by order:

```sql
select avg(order_total) as average_order_value
from (
    select
        order_id,
        sum(payment_value) as order_total
    from payments
    group by order_id
) as order_payments;
```

---

## Monthly Revenue

```sql
select
    year(o.order_purchase_timestamp) as year,
    month(o.order_purchase_timestamp) as month,
    sum(p.payment_value) as revenue
from orders o
join payments p
    on o.order_id = p.order_id
group by
    year(o.order_purchase_timestamp),
    month(o.order_purchase_timestamp)
order by year, month;
```

---

## Top Products

```sql
select
    product_id,
    count(*) as units_sold
from order_items
group by product_id
order by units_sold desc
limit 10;
```

---

## Top Sellers

```sql
select
    seller_id,
    count(*) as items_sold
from order_items
group by seller_id
order by items_sold desc
limit 10;
```

---

## Payment Distribution

```sql
select
    payment_type,
    count(*) as payment_count
from payments
group by payment_type
order by payment_count desc;
```

---

## Cancellation Rate

```sql
select
    100.0 * sum(
        case
            when order_status = 'canceled' then 1
            else 0
        end
    ) / count(*) as cancellation_rate
from orders;
```

---

## Average Delivery Time

```sql
select
    avg(delivery_days) as average_delivery_days
from orders;
```

---

## Late Deliveries

```sql
select
    count(*) as late_orders
from orders
where order_delivered_customer_date >
      order_estimated_delivery_date;
```

---

# 14. Tkinter Analytics Dashboard

A desktop analytics dashboard was developed using **Tkinter**.

The dashboard connects the Python application to the MySQL database and allows users to execute business-analysis queries through buttons.

Architecture:

```text
Tkinter Dashboard
       ↓
Python Functions
       ↓
SQL Queries
       ↓
MySQL Database
       ↓
Results
       ↓
Tkinter Tables / Charts
```

The dashboard provides sections for:

### Overview

* Total orders
* Total revenue
* Average order value
* Average delivery days
* Cancellation rate

### Sales

* Monthly revenue
* Top products
* Top sellers
* Sales-related analysis

### Customers

* Customer order analysis
* Repeat customer analysis
* Customer-level insights

### Payments

* Payment method distribution
* Payment-related metrics

### Delivery

* Average delivery time
* Late deliveries
* Delivery performance

### Order Status

* Order status distribution
* Status-based analysis

### Reviews

* Review scores
* Review-related analysis

---

# 15. Desktop Application

The Tkinter dashboard can be packaged as a Windows executable using PyInstaller.

Install PyInstaller:

```powershell
pip install pyinstaller
```

Build the application:

```powershell
pyinstaller --onefile --windowed --paths src src\dashboard.py
```

The executable is generated under:

```text
dist/dashboard.exe
```

The executable can be distributed through **GitHub Releases**.

The `dist/` directory is excluded from normal Git tracking, while the final executable can be uploaded as a release asset.

---

# 16. Running the Project

## Clone the Repository

```bash
git clone https://github.com/Guruharishb/olist_ecommerce_analytics.git
```

Move into the project:

```bash
cd olist_ecommerce_analytics
```

## Create Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

## Install Dependencies

```powershell
pip install -r requirements.txt
```

## Configure MySQL

Create the database:

```sql
create database olist_analytics;
```

Then create the required tables and load the processed datasets.

## Run the Dashboard

From the project root:

```powershell
python -m src.dashboard
```

---

# 17. Requirements

The main Python dependencies are:

```text
pandas
mysql-connector-python
pyinstaller
```

Tkinter is included with standard Python installations on Windows and does not need to be installed separately using pip.

---

# 18. Data Quality Summary

| Area                  | Checks                                                          |
| --------------------- | --------------------------------------------------------------- |
| Completeness          | Missing values and missing identifiers                          |
| Uniqueness            | Duplicate rows and duplicate identifiers                        |
| Validity              | Data types and date conversion                                  |
| Consistency           | Order status and date relationships                             |
| Referential Integrity | Customer, order, product, seller, payment and review references |
| Database Integrity    | Primary keys, composite keys and foreign keys                   |
| Analytical Readiness  | Transformation and feature creation                             |

---

# 19. Why This Project Matters

Data analysis is only reliable when the underlying data is reliable.

This project demonstrates the complete workflow from raw data to business insights:

```text
Data Collection
      ↓
Data Profiling
      ↓
Data Quality Checks
      ↓
Data Transformation
      ↓
Data Validation
      ↓
Database Design
      ↓
MySQL Loading
      ↓
SQL Analysis
      ↓
Dashboard
      ↓
Business Insights
```

Examples of problems that data-quality validation helps prevent:

* Duplicate records inflating revenue
* Missing dates affecting delivery calculations
* Invalid customer references affecting customer analysis
* Invalid seller references affecting seller performance
* Missing product information affecting product analysis
* Duplicate payment records affecting revenue calculations
* Invalid order references affecting payment and review analysis

---

# 20. Future Improvements

Possible future improvements include:

1. Add more interactive dashboard filters
2. Add product-category analysis
3. Add geographic analysis using the geolocation dataset
4. Add customer segmentation
5. Add seller performance metrics
6. Add monthly and yearly trend charts
7. Add automated data-quality reports
8. Add scheduled ETL execution
9. Add automated database loading
10. Add more dashboard visualizations
11. Add cloud database connectivity
12. Improve dashboard deployment and distribution

---

# Demo

The Windows desktop application is distributed through GitHub Releases.

**Download the latest dashboard:**

https://github.com/Guruharishb/olist_ecommerce_analytics/releases

---

# Repository

GitHub:

https://github.com/Guruharishb/olist_ecommerce_analytics

---

# Author

**Guruharish B**

B.Tech Information Technology

St. Joseph's Institute of Technology

---

## Project Focus

```text
Python
Pandas
ETL
Data Quality
MySQL
SQL
Database Design
Tkinter
Data Analytics
Data Visualization
Git
GitHub
```
