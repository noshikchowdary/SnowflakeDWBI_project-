# Quick Start Guide - E-Commerce Analytics Platform

Get up and running with the E-Commerce Analytics Platform in minutes!

## 🚀 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher (optional, for database operations)
- Git

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ecommerce-analytics-platform
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Configuration
```bash
cp config/config.example.yml config/config.yml
# Edit config/config.yml with your settings
```

## 🎯 Quick Start Examples

### Option 1: Run Complete Pipeline
Generate all data and analytics in one command:
```bash
python scripts/main.py --full-pipeline
```

### Option 2: Step-by-Step Generation

#### Generate Customer Data
```bash
python scripts/main.py --generate-customers --num-customers 2000
```

#### Generate Sales Data
```bash
python scripts/main.py --generate-sales --num-orders 5000
```

#### Generate Analytics Report
```bash
python scripts/main.py --generate-analytics
```

### Option 3: Individual Scripts

#### Generate Sales Data
```bash
python "Python Files/Historical_Sales_Data.py" --num-orders 10000 --start-date 2020-01-01 --end-date 2024-12-31
```

#### Generate Customer Data
```bash
python "Python Files/DimCustomerData.py" --num-customers 5000
```

#### Generate Analytics Dashboard
```bash
python "Python Files/analytics_dashboard.py" --data-dir data/processed --output-dir reports
```

## 📊 What You'll Get

After running the pipeline, you'll have:

### Data Files (in `data/processed/`)
- `sales_data_YYYYMMDD_HHMMSS.csv` - Comprehensive sales transactions
- `customer_data_YYYYMMDD_HHMMSS.csv` - Customer profiles with segmentation
- Metadata files with data quality scores

### Analytics Reports (in `reports/`)
- Revenue trend analysis charts
- Daily sales pattern visualizations
- Store performance comparisons
- Product performance analysis
- Customer demographics and segmentation
- Geographic distribution analysis
- `analytics_summary.json` - Key metrics and insights

### Logs (in `logs/`)
- Detailed execution logs
- Data quality validation results
- Performance metrics

## 🔍 Check Platform Status

Monitor your platform:
```bash
python scripts/main.py --status
```

This will show:
- Configuration status
- Directory structure
- Data file counts
- Latest generated files

## 📈 Sample Output

### Analytics Summary
```json
{
  "key_insights": {
    "total_revenue": "$1,234,567.89",
    "avg_order_value": "$123.45",
    "total_orders": "10,000",
    "unique_customers": "5,000",
    "avg_profit_margin": "15.2%"
  },
  "recommendations": [
    "Focus on increasing average order value through cross-selling",
    "Implement customer retention programs for high-value segments",
    "Optimize store performance based on geographic analysis"
  ]
}
```

### Generated Visualizations
- Revenue trend over time
- Sales patterns by day of week
- Top-performing stores and products
- Customer segmentation analysis
- Geographic distribution maps

## 🛠️ Customization

### Modify Data Generation Parameters
Edit `config/config.yml`:
```yaml
data_generation:
  sales:
    num_orders: 20000
    start_date: "2022-01-01"
    end_date: "2024-12-31"
  customers:
    num_customers: 10000
```

### Add Custom Business Rules
Modify the Python scripts in `Python Files/` to:
- Adjust pricing strategies
- Change customer segmentation logic
- Add new product categories
- Implement custom KPIs

### Extend Analytics
Enhance `Python Files/analytics_dashboard.py` to:
- Add new visualization types
- Create custom business metrics
- Implement predictive analytics
- Generate executive dashboards

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Make sure you're in the project root directory
cd ecommerce-analytics-platform
# Activate virtual environment
source venv/bin/activate
```

#### 2. Missing Dependencies
```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade
```

#### 3. Configuration Issues
```bash
# Check if config file exists
ls config/config.yml
# Copy example if missing
cp config/config.example.yml config/config.yml
```

#### 4. Permission Issues
```bash
# Make scripts executable
chmod +x scripts/main.py
chmod +x "Python Files/"*.py
```

### Getting Help

1. Check the logs in `logs/` directory
2. Review the README.md for detailed documentation
3. Check the `docs/` directory for technical specifications
4. Open an issue for bugs or feature requests

## 🚀 Next Steps

### For Data Scientists
- Extend the analytics with machine learning models
- Add predictive analytics for sales forecasting
- Implement customer lifetime value predictions
- Create A/B testing frameworks

### For Developers
- Integrate with real e-commerce platforms
- Add real-time data streaming
- Implement API endpoints for data access
- Create web-based dashboards

### For Business Users
- Customize KPIs for your business needs
- Add industry-specific metrics
- Integrate with existing BI tools
- Set up automated reporting schedules

## 📚 Additional Resources

- [Full Documentation](docs/)
- [API Reference](docs/api/)
- [User Guides](docs/user-guides/)
- [Technical Specifications](docs/technical/)

---

**Ready to start? Run `python scripts/main.py --full-pipeline` and explore your e-commerce analytics!** 