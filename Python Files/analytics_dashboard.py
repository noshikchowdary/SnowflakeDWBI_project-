#!/usr/bin/env python3
"""
E-Commerce Analytics Dashboard Generator

This script creates comprehensive analytics dashboards with:
- Real-time KPI calculations
- Advanced visualizations
- Customer behavior analysis
- Product performance insights
- Store performance metrics
- Predictive analytics
- Interactive reports

Author: Built for portfolio demonstration
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import logging
import json
from pathlib import Path
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/analytics_dashboard.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ECommerceAnalytics:
    """Advanced e-commerce analytics and dashboard generator."""
    
    def __init__(self, data_dir: str = "data/processed"):
        """Initialize analytics with data directory."""
        self.data_dir = Path(data_dir)
        self.sales_data = None
        self.customers_data = None
        self.products_data = None
        self.stores_data = None
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        logger.info("ECommerceAnalytics initialized successfully")
    
    def load_data(self):
        """Load all data files."""
        logger.info("Loading data files...")
        
        try:
            # Load sales data
            sales_path = self.data_dir / "historical_sales.csv"
            if sales_path.exists():
                self.sales_data = pd.read_csv(sales_path)
                self.sales_data['CreatedAt'] = pd.to_datetime(self.sales_data['CreatedAt'])
                logger.info(f"Loaded {len(self.sales_data):,} sales records")
            
            # Load customer data
            customers_path = self.data_dir / "customers.csv"
            if customers_path.exists():
                self.customers_data = pd.read_csv(customers_path)
                logger.info(f"Loaded {len(self.customers_data):,} customer records")
            
            # Load product data
            products_path = self.data_dir / "products.csv"
            if products_path.exists():
                self.products_data = pd.read_csv(products_path)
                logger.info(f"Loaded {len(self.products_data):,} product records")
            
            # Load store data
            stores_path = self.data_dir / "stores.csv"
            if stores_path.exists():
                self.stores_data = pd.read_csv(stores_path)
                logger.info(f"Loaded {len(self.stores_data):,} store records")
                
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def calculate_kpis(self) -> Dict:
        """Calculate key performance indicators."""
        logger.info("Calculating KPIs...")
        
        if self.sales_data is None:
            logger.warning("No sales data available for KPI calculation")
            return {}
        
        # Basic sales KPIs
        total_revenue = self.sales_data['TotalAmount'].sum()
        total_orders = len(self.sales_data)
        avg_order_value = self.sales_data['TotalAmount'].mean()
        unique_customers = self.sales_data['CustomerID'].nunique()
        
        # Time-based KPIs
        self.sales_data['Date'] = pd.to_datetime(self.sales_data['CreatedAt']).dt.date
        daily_sales = self.sales_data.groupby('Date')['TotalAmount'].sum()
        
        # Growth metrics
        if len(daily_sales) > 30:
            current_month = daily_sales.tail(30).sum()
            previous_month = daily_sales.tail(60).head(30).sum()
            month_over_month_growth = ((current_month - previous_month) / previous_month) * 100
        else:
            month_over_month_growth = 0
        
        # Customer metrics
        customer_lifetime_value = self.sales_data.groupby('CustomerID')['TotalAmount'].sum().mean()
        
        # Product metrics
        top_product = self.sales_data.groupby('ProductID')['QuantityOrdered'].sum().idxmax()
        top_product_quantity = self.sales_data.groupby('ProductID')['QuantityOrdered'].sum().max()
        
        # Store metrics
        top_store = self.sales_data.groupby('StoreID')['TotalAmount'].sum().idxmax()
        top_store_revenue = self.sales_data.groupby('StoreID')['TotalAmount'].sum().max()
        
        # Return rate
        return_rate = self.sales_data['ReturnFlag'].mean() * 100
        
        kpis = {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'avg_order_value': avg_order_value,
            'unique_customers': unique_customers,
            'customer_lifetime_value': customer_lifetime_value,
            'month_over_month_growth': month_over_month_growth,
            'return_rate': return_rate,
            'top_product_id': top_product,
            'top_product_quantity': top_product_quantity,
            'top_store_id': top_store,
            'top_store_revenue': top_store_revenue
        }
        
        logger.info("KPIs calculated successfully")
        return kpis
    
    def create_sales_trends_dashboard(self, output_path: str = "reports/sales_trends.html"):
        """Create comprehensive sales trends dashboard."""
        logger.info("Creating sales trends dashboard...")
        
        if self.sales_data is None:
            logger.warning("No sales data available for dashboard")
            return
        
        # Prepare data
        sales_df = self.sales_data.copy()
        sales_df['Date'] = pd.to_datetime(sales_df['CreatedAt']).dt.date
        sales_df['Month'] = pd.to_datetime(sales_df['CreatedAt']).dt.to_period('M')
        sales_df['DayOfWeek'] = pd.to_datetime(sales_df['CreatedAt']).dt.day_name()
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Daily Sales Trend', 'Monthly Revenue',
                'Sales by Day of Week', 'Order Status Distribution',
                'Payment Method Distribution', 'Return Rate Trend'
            ),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Daily Sales Trend
        daily_sales = sales_df.groupby('Date')['TotalAmount'].sum().reset_index()
        fig.add_trace(
            go.Scatter(x=daily_sales['Date'], y=daily_sales['TotalAmount'],
                      mode='lines', name='Daily Sales', line=dict(color='blue')),
            row=1, col=1
        )
        
        # 2. Monthly Revenue
        monthly_revenue = sales_df.groupby('Month')['TotalAmount'].sum().reset_index()
        monthly_revenue['Month'] = monthly_revenue['Month'].astype(str)
        fig.add_trace(
            go.Bar(x=monthly_revenue['Month'], y=monthly_revenue['TotalAmount'],
                   name='Monthly Revenue', marker_color='green'),
            row=1, col=2
        )
        
        # 3. Sales by Day of Week
        day_sales = sales_df.groupby('DayOfWeek')['TotalAmount'].sum().reset_index()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_sales['DayOfWeek'] = pd.Categorical(day_sales['DayOfWeek'], categories=day_order, ordered=True)
        day_sales = day_sales.sort_values('DayOfWeek')
        
        fig.add_trace(
            go.Bar(x=day_sales['DayOfWeek'], y=day_sales['TotalAmount'],
                   name='Sales by Day', marker_color='orange'),
            row=2, col=1
        )
        
        # 4. Order Status Distribution
        status_dist = sales_df['OrderStatus'].value_counts()
        fig.add_trace(
            go.Pie(labels=status_dist.index, values=status_dist.values,
                   name='Order Status', hole=0.3),
            row=2, col=2
        )
        
        # 5. Payment Method Distribution
        payment_dist = sales_df['PaymentMethod'].value_counts()
        fig.add_trace(
            go.Bar(x=payment_dist.index, y=payment_dist.values,
                   name='Payment Methods', marker_color='purple'),
            row=3, col=1
        )
        
        # 6. Return Rate Trend
        returns_trend = sales_df.groupby('Date')['ReturnFlag'].mean().reset_index()
        fig.add_trace(
            go.Scatter(x=returns_trend['Date'], y=returns_trend['ReturnFlag'] * 100,
                      mode='lines', name='Return Rate %', line=dict(color='red')),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="E-Commerce Sales Analytics Dashboard",
            showlegend=False,
            height=1200,
            width=1200
        )
        
        # Save dashboard
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_path)
        logger.info(f"Sales trends dashboard saved to {output_path}")
    
    def create_customer_analytics_dashboard(self, output_path: str = "reports/customer_analytics.html"):
        """Create customer analytics dashboard."""
        logger.info("Creating customer analytics dashboard...")
        
        if self.sales_data is None or self.customers_data is None:
            logger.warning("Customer or sales data not available")
            return
        
        # Merge sales and customer data
        customer_sales = self.sales_data.merge(
            self.customers_data[['CustomerID', 'CustomerSegment', 'City', 'State']],
            on='CustomerID', how='left'
        )
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Customer Segment Distribution', 'Revenue by Customer Segment',
                'Geographic Revenue Distribution', 'Customer Lifetime Value by Segment'
            )
        )
        
        # 1. Customer Segment Distribution
        segment_dist = customer_sales['CustomerSegment'].value_counts()
        fig.add_trace(
            go.Pie(labels=segment_dist.index, values=segment_dist.values,
                   name='Customer Segments', hole=0.3),
            row=1, col=1
        )
        
        # 2. Revenue by Customer Segment
        segment_revenue = customer_sales.groupby('CustomerSegment')['TotalAmount'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=segment_revenue['CustomerSegment'], y=segment_revenue['TotalAmount'],
                   name='Revenue by Segment', marker_color='lightblue'),
            row=1, col=2
        )
        
        # 3. Geographic Revenue Distribution
        state_revenue = customer_sales.groupby('State')['TotalAmount'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(x=state_revenue['State'], y=state_revenue['TotalAmount'],
                   name='Revenue by State', marker_color='lightgreen'),
            row=2, col=1
        )
        
        # 4. Customer Lifetime Value by Segment
        clv_by_segment = customer_sales.groupby('CustomerSegment')['TotalAmount'].mean().reset_index()
        fig.add_trace(
            go.Bar(x=clv_by_segment['CustomerSegment'], y=clv_by_segment['TotalAmount'],
                   name='CLV by Segment', marker_color='lightcoral'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Customer Analytics Dashboard",
            showlegend=False,
            height=800,
            width=1000
        )
        
        # Save dashboard
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_path)
        logger.info(f"Customer analytics dashboard saved to {output_path}")
    
    def create_product_performance_dashboard(self, output_path: str = "reports/product_performance.html"):
        """Create product performance dashboard."""
        logger.info("Creating product performance dashboard...")
        
        if self.sales_data is None or self.products_data is None:
            logger.warning("Product or sales data not available")
            return
        
        # Merge sales and product data
        product_sales = self.sales_data.merge(
            self.products_data[['ProductID', 'ProductName', 'Category', 'Brand', 'UnitPrice']],
            on='ProductID', how='left'
        )
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Top Products by Revenue', 'Category Performance',
                'Brand Performance', 'Price vs Quantity Analysis'
            )
        )
        
        # 1. Top Products by Revenue
        top_products = product_sales.groupby('ProductName')['TotalAmount'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(x=top_products['TotalAmount'], y=top_products['ProductName'],
                   orientation='h', name='Top Products', marker_color='skyblue'),
            row=1, col=1
        )
        
        # 2. Category Performance
        category_performance = product_sales.groupby('Category')['TotalAmount'].sum().reset_index()
        fig.add_trace(
            go.Pie(labels=category_performance['Category'], values=category_performance['TotalAmount'],
                   name='Category Performance'),
            row=1, col=2
        )
        
        # 3. Brand Performance
        brand_performance = product_sales.groupby('Brand')['TotalAmount'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(x=brand_performance['Brand'], y=brand_performance['TotalAmount'],
                   name='Brand Performance', marker_color='lightgreen'),
            row=2, col=1
        )
        
        # 4. Price vs Quantity Analysis
        price_quantity = product_sales.groupby('ProductID').agg({
            'UnitPrice': 'mean',
            'QuantityOrdered': 'sum'
        }).reset_index()
        
        fig.add_trace(
            go.Scatter(x=price_quantity['UnitPrice'], y=price_quantity['QuantityOrdered'],
                      mode='markers', name='Price vs Quantity',
                      marker=dict(size=8, color='red', opacity=0.6)),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Product Performance Dashboard",
            showlegend=False,
            height=800,
            width=1000
        )
        
        # Save dashboard
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_path)
        logger.info(f"Product performance dashboard saved to {output_path}")
    
    def create_store_analytics_dashboard(self, output_path: str = "reports/store_analytics.html"):
        """Create store analytics dashboard."""
        logger.info("Creating store analytics dashboard...")
        
        if self.sales_data is None or self.stores_data is None:
            logger.warning("Store or sales data not available")
            return
        
        # Merge sales and store data
        store_sales = self.sales_data.merge(
            self.stores_data[['StoreID', 'StoreName', 'City', 'State', 'StoreType']],
            on='StoreID', how='left'
        )
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Top Performing Stores', 'Store Type Performance',
                'Geographic Store Performance', 'Store Efficiency Analysis'
            )
        )
        
        # 1. Top Performing Stores
        top_stores = store_sales.groupby('StoreName')['TotalAmount'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(x=top_stores['TotalAmount'], y=top_stores['StoreName'],
                   orientation='h', name='Top Stores', marker_color='gold'),
            row=1, col=1
        )
        
        # 2. Store Type Performance
        type_performance = store_sales.groupby('StoreType')['TotalAmount'].sum().reset_index()
        fig.add_trace(
            go.Pie(labels=type_performance['StoreType'], values=type_performance['TotalAmount'],
                   name='Store Type Performance'),
            row=1, col=2
        )
        
        # 3. Geographic Store Performance
        geo_performance = store_sales.groupby('State')['TotalAmount'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(x=geo_performance['State'], y=geo_performance['TotalAmount'],
                   name='Geographic Performance', marker_color='lightcoral'),
            row=2, col=1
        )
        
        # 4. Store Efficiency (Revenue per Order)
        store_efficiency = store_sales.groupby('StoreName').agg({
            'TotalAmount': 'sum',
            'OrderID': 'count'
        }).reset_index()
        store_efficiency['RevenuePerOrder'] = store_efficiency['TotalAmount'] / store_efficiency['OrderID']
        
        fig.add_trace(
            go.Bar(x=store_efficiency['StoreName'], y=store_efficiency['RevenuePerOrder'],
                   name='Revenue per Order', marker_color='lightblue'),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Store Analytics Dashboard",
            showlegend=False,
            height=800,
            width=1000
        )
        
        # Save dashboard
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_path)
        logger.info(f"Store analytics dashboard saved to {output_path}")
    
    def generate_executive_summary(self, output_path: str = "reports/executive_summary.html"):
        """Generate executive summary report."""
        logger.info("Generating executive summary...")
        
        kpis = self.calculate_kpis()
        
        # Create executive summary
        fig = go.Figure()
        
        # Add KPI cards
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=kpis.get('total_revenue', 0),
            delta={'reference': kpis.get('total_revenue', 0) * 0.9},
            title={'text': "Total Revenue ($)"},
            domain={'x': [0, 0.5], 'y': [0.5, 1]}
        ))
        
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=kpis.get('total_orders', 0),
            delta={'reference': kpis.get('total_orders', 0) * 0.9},
            title={'text': "Total Orders"},
            domain={'x': [0.5, 1], 'y': [0.5, 1]}
        ))
        
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=kpis.get('avg_order_value', 0),
            delta={'reference': kpis.get('avg_order_value', 0) * 0.9},
            title={'text': "Average Order Value ($)"},
            domain={'x': [0, 0.5], 'y': [0, 0.5]}
        ))
        
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=kpis.get('unique_customers', 0),
            delta={'reference': kpis.get('unique_customers', 0) * 0.9},
            title={'text': "Unique Customers"},
            domain={'x': [0.5, 1], 'y': [0, 0.5]}
        ))
        
        fig.update_layout(
            title_text="E-Commerce Executive Summary",
            height=600,
            width=800
        )
        
        # Save summary
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_path)
        logger.info(f"Executive summary saved to {output_path}")
    
    def generate_all_reports(self):
        """Generate all analytics reports."""
        logger.info("Generating all analytics reports...")
        
        try:
            # Load data first
            self.load_data()
            
            # Generate all dashboards
            self.create_sales_trends_dashboard()
            self.create_customer_analytics_dashboard()
            self.create_product_performance_dashboard()
            self.create_store_analytics_dashboard()
            self.generate_executive_summary()
            
            logger.info("All reports generated successfully!")
            
        except Exception as e:
            logger.error(f"Error generating reports: {str(e)}")
            raise

def main():
    """Main execution function."""
    try:
        logger.info("Starting E-Commerce Analytics Dashboard Generation")
        
        # Initialize analytics
        analytics = ECommerceAnalytics()
        
        # Generate all reports
        analytics.generate_all_reports()
        
        logger.info("Analytics dashboard generation completed successfully!")
        
        print("\n📊 Analytics Dashboards Generated:")
        print("   📈 Sales Trends Dashboard: reports/sales_trends.html")
        print("   👥 Customer Analytics: reports/customer_analytics.html")
        print("   📦 Product Performance: reports/product_performance.html")
        print("   🏪 Store Analytics: reports/store_analytics.html")
        print("   📋 Executive Summary: reports/executive_summary.html")
        
    except Exception as e:
        logger.error(f"Error in analytics generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 