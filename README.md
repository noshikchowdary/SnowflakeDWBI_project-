# Snowflake Data Warehouse & Business Intelligence Project

A comprehensive data warehouse and business intelligence solution built on Snowflake, featuring automated ETL pipelines, dimensional modeling, and analytics capabilities.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Monitoring & Logging](#monitoring--logging)

## Project Overview

This project implements a complete data warehouse solution using Snowflake as the cloud data platform. It includes:

- **Data Ingestion**: Automated ETL pipelines for customer and sales data
- **Data Modeling**: Dimensional model with customer dimensions and sales facts
- **Data Quality**: Comprehensive validation and monitoring framework
- **Analytics**: Pre-built views for business intelligence and reporting
- **Orchestration**: Python-based ETL orchestration with error handling

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Source Data   │───▶│   Staging Layer │───▶│  Data Warehouse │
│   (CSV, APIs)   │    │   (Raw Data)    │    │  (Dimensional)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Data Quality   │    │   Analytics     │
                       │   Framework     │    │    Views        │
                       └─────────────────┘    └─────────────────┘
```

### Data Flow Architecture

1. **Data Ingestion Layer**
   - Source data extraction from various systems
   - Initial data validation and cleaning
   - Staging table population

2. **Staging Layer**
   - Raw data storage with minimal transformation
   - Data quality checks and validation
   - Incremental loading capabilities

3. **Data Warehouse Layer**
   - Dimensional model implementation
   - Customer dimension with SCD Type 2
   - Sales fact table with proper grain definition
   - Optimized for analytical query performance

4. **Analytics Layer**
   - Pre-built views for common business metrics
   - Aggregated sales performance views
   - Year-over-year growth calculations

5. **Orchestration Layer**
   - Python-based ETL orchestration
   - Dependency management and scheduling
   - Error handling and recovery mechanisms

## Technology Stack

- **Cloud Data Platform**: Snowflake
- **ETL Orchestration**: Python 3.8+
- **Data Quality**: Great Expectations / Custom validation
- **Version Control**: Git
- **Documentation**: Markdown, Jupyter Notebooks
- **Testing**: pytest, SQL validation tests

## Project Structure

```
SnowflakeDWBI_project/
├── config/
│   └── config.example.yml          # Configuration templates
├── sql/
│   ├── etl/
│   │   ├── stage_customers.sql     # Customer staging logic
│   │   └── stage_sales.sql         # Sales staging logic
│   └── warehouse/
│       ├── dim_customers.sql       # Customer dimension
│       ├── fact_sales.sql          # Sales fact table
│       └── analytics_view.sql      # Analytics views
├── scripts/
│   ├── sf_connect.py               # Snowflake connection utility
│   └── run_etl.py                  # Main ETL orchestration
├── notebooks/
│   └── data_quality_checks.ipynb   # Data quality validation
├── tests/
│   ├── test_etl.py                 # ETL pipeline tests
│   └── test_queries.sql            # SQL validation tests
├── docs/                           # Documentation
├── logs/                           # Execution logs
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Snowflake account with appropriate permissions
- Git for version control
- Access to source data systems

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/noshikchowdary/SnowflakeDWBI_project-.git
cd SnowflakeDWBI_project-
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

# ETL Configuration
ETL_BATCH_SIZE=10000
ETL_MAX_RETRIES=3
LOG_LEVEL=INFO
```

### 4. Database Setup

Execute the SQL scripts in the following order:

1. `sql/etl/stage_customers.sql` - Create staging tables
2. `sql/etl/stage_sales.sql` - Create sales staging
3. `sql/warehouse/dim_customers.sql` - Create customer dimension
4. `sql/warehouse/fact_sales.sql` - Create sales fact table
5. `sql/warehouse/analytics_view.sql` - Create analytics views

## Configuration

### Snowflake Connection

The project uses a centralized connection utility (`scripts/sf_connect.py`) that handles:

- Connection pooling for optimal performance
- Environment variable configuration
- Error handling and retry logic
- Multiple warehouse support

### ETL Configuration

ETL processes are configured through:

- Environment variables for runtime settings
- SQL scripts for data transformation logic
- Python orchestration for workflow management

## Usage

### Running the ETL Pipeline

```bash
# Execute the complete ETL pipeline
python scripts/run_etl.py

# Run specific stages
python scripts/run_etl.py --stage staging
python scripts/run_etl.py --stage warehouse
python scripts/run_etl.py --stage analytics
```

### Data Quality Checks

```bash
# Run data quality validation
jupyter notebook notebooks/data_quality_checks.ipynb
```

### Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_etl.py
```

## Testing

The project includes comprehensive testing:

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow validation
- **SQL Tests**: Query validation and performance testing
- **Data Quality Tests**: Automated data validation

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts

# Run specific test file
pytest tests/test_etl.py
```

## Monitoring & Logging

### Logging Configuration

- Logs are stored in the `logs/` directory
- Different log levels for development and production
- Structured logging for easy parsing and analysis

### Monitoring Features

- ETL execution status tracking
- Data quality metrics monitoring
- Performance metrics collection
- Error alerting and notification

---

**Note**: This project is designed for educational and demonstration purposes. Please ensure proper security measures when deploying to production environments.
