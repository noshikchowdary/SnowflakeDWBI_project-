# 🛍️ sales Data Warehouse ETL Project

Welcome to a hands-on data engineering project that simulates a complete **Sales Data Warehouse pipeline**—from ingesting raw retail data to building a structured star schema ready for business intelligence and analytics.  

This project demonstrates my ability to design, develop, and document a full-stack ETL workflow using **Python, SQL, Excel, and file-based automation techniques**. It reflects real-world practices in data warehousing, data transformation, and schema modeling

---

## 📌 Project Overview

**Business Context**  
A fictional retail business operates multiple store locations and collects daily sales data in CSV files. As a Data Engineer, my role is to:

- Set up a structured **data warehouse**
- Build automated ETL scripts to process raw sales data
- Design a relational model for downstream analytics and reporting
- Deliver clean, enriched, query-ready tables for use by analysts and BI teams

---

## 🗂️ Folder Structure & Functionality

### `1_One_Time_Load/`
📦 **Purpose**: Load foundational data (dimensions and fact table) into the warehouse.  
📄 **Contents**: Subfolders for:
- `FactOrders/`
- `DimCustomer/`
- `DimDate/`
- `DimLoyalty/`
- `DimProduct/`
- `DimStore/`

🔧 **Functionality**:
Each subfolder contains data files or scripts to initialize your database. This is used during the first setup or when reloading the system from scratch.

---

### `2_Landing_Directory/`
📦 **Purpose**: Acts as the raw data staging area.  
📄 **Contents**: CSV files such as `Store_102_20240728.csv`, `Store_205_20240728.csv`, etc.

🔧 **Functionality**:
- Each file contains transactional sales data from different stores and dates.
- The ETL pipeline will monitor this directory to pick up new sales files for processing.

---

### `3_Lookup_Data/`
📦 **Purpose**: Reference tables for data enrichment and standardization.  
📄 **Contents**: `LookupFile.xlsx`

🔧 **Functionality**:
- Contains mappings for things like product categories, loyalty tiers, region codes, etc.
- These lookups are used during transformation to ensure consistency and usability of data.

---

### `4_Python_Files/`
📦 **Purpose**: Core of the ETL logic.  
📄 **Contents**:
- Multiple `.py` scripts
- `factorders.csv` (output of transformed fact table)

🔧 **Functionality**:
- Scripts for loading and transforming each dimension (customer, store, product, etc.)
- Script to combine daily store files into a consolidated **FactOrders** table
- Automation of data cleaning, formatting, and enriching with lookup data

🧠 **Skills Showcased**:
- File handling and automation
- Data transformation using `pandas`
- Error handling, backups, and logging
- Built from scratch: no third-party orchestration or cloud dependencies  
- Realistic simulation of retail sales pipelines  
- Demonstrates automation, schema design, and ETL best practices   
- Easy to extend to PostgreSQL, Snowflake, Airflow, or dbt

---

### `5_Excel/`
📦 **Purpose**: Documentation of data model and schema  
📄 **Contents**: `ER_Diagram.xlsx`

🔧 **Functionality**:
- Visual Entity-Relationship (ER) diagram of the star schema
- Clearly shows the relationship between fact and dimension tables
- Acts as a guide for development and analyst handoff

---

### `6_DB_Code/`
📦 **Purpose**: SQL DDL scripts for setting up the data warehouse schema  
📄 **Contents**: `DDL.sql`

🔧 **Functionality**:
- Creates tables, primary/foreign key relationships, constraints
- Prepares the database environment before loading any data
- Ensures consistency and data integrity

---

## 🚀 How It Works (End-to-End ETL Flow)

1. **Raw Data Staging**
   - Daily store sales files arrive in the `Landing_Directory/`

2. **Schema Setup**
   - SQL DDL scripts (`DDL.sql`) create a star schema with one fact table and five dimensions

3. **Lookup Enrichment**
   - Reference data from `LookupFile.xlsx` is used to map codes to descriptions, clean fields, etc.

4. **ETL Processing**
   - Python scripts:
     - Load and transform dimension tables
     - Burst, clean, and combine store-level sales into `FactOrders`
     - Output cleaned `factorders.csv`

5. **Data Loading**
   - Transformed data is loaded into the database (can be extended to PostgreSQL, MySQL, Snowflake, etc.)

6. **Analytics-Ready**
   - Output: a well-structured warehouse ready for reporting and BI tools like Power BI, Tableau, or Excel

---

## 🧰 Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python** | ETL scripting, data wrangling |
| **pandas** | CSV and Excel data processing |
| **SQL (DDL)** | Schema creation and constraints |
| **Excel** | ER diagram, lookup data |
| **File System** | Simulated real-world data drops |

---

---

## 📊 Star Schema Design

- **Fact Table**: `FactOrders`
- **Dimensions**:
  - `DimCustomer`
  - `DimStore`
  - `DimProduct`
  - `DimDate`
  - `DimLoyalty`

Each fact record is enriched with descriptive dimension data, enabling deep sales analytics like customer segmentation, store performance, and product trends.

---

## 👨‍💻 Author

**Noshik Chirumamilla**  
Aspiring Data Engineer | Cloud & ETL Enthusiast  

---


