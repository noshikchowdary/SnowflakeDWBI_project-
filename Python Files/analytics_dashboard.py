#!/usr/bin/env python3
"""
E-Commerce Analytics Platform - Analytics Dashboard
Comprehensive business intelligence and reporting system
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import argparse
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EcommerceAnalytics:
    """Comprehensive e-commerce analytics engine"""
    
    def __init__(self, data_dir: str = "data/processed"):
        self.data_dir = Path(data_dir)
        self.sales_data = None
        self.customer_data = None
        
        # Set style for visualizations
        plt.style.use('default')
        sns.set_palette("husl")
    
    def load_data(self) -> None:
        """Load all data sources"""
        logger.info("Loading data sources...")
        
        try:
            # Load sales data
            sales_files = list(self.data_dir.glob("*sales_data*.csv"))
            if sales_files:
                self.sales_data = pd.read_csv(sales_files[-1])  # Latest file
                logger.info(f"Loaded sales data: {len(self.sales_data)} records")
            
            # Load customer data
            customer_files = list(self.data_dir.glob("*customer_data*.csv"))
            if customer_files:
                self.customer_data = pd.read_csv(customer_files[-1])
                logger.info(f"Loaded customer data: {len(self.customer_data)} records")
                
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def preprocess_data(self) -> None:
        """Preprocess and clean data for analysis"""
        logger.info("Preprocessing data...")
        
        if self.sales_data is not None:
            # Convert DateID to datetime
            self.sales_data['Date'] = pd.to_datetime(self.sales_data['DateID'], format='%Y%m%d')
            self.sales_data['Year'] = self.sales_data['Date'].dt.year
            self.sales_data['Month'] = self.sales_data['Date'].dt.month
            self.sales_data['Quarter'] = self.sales_data['Date'].dt.quarter
            self.sales_data['DayOfWeek'] = self.sales_data['Date'].dt.day_name()
            
            # Calculate additional metrics
            self.sales_data['Profit'] = self.sales_data['TotalAmount'] - self.sales_data['DiscountAmount']
            self.sales_data['ProfitMargin'] = (self.sales_data['Profit'] / self.sales_data['TotalAmount']) * 100
        
        if self.customer_data is not None:
            # Convert date columns
            date_columns = ['DateOfBirth', 'AcquisitionDate']
            for col in date_columns:
                if col in self.customer_data.columns:
                    self.customer_data[col] = pd.to_datetime(self.customer_data[col])
    
    def calculate_kpis(self) -> Dict[str, float]:
        """Calculate key performance indicators"""
        logger.info("Calculating KPIs...")
        
        kpis = {}
        
        if self.sales_data is not None:
            # Revenue metrics
            kpis['total_revenue'] = self.sales_data['TotalAmount'].sum()
            kpis['avg_order_value'] = self.sales_data['TotalAmount'].mean()
            kpis['total_orders'] = len(self.sales_data)
            kpis['total_quantity'] = self.sales_data['QuantityOrdered'].sum()
            
            # Customer metrics
            kpis['unique_customers'] = self.sales_data['CustomerID'].nunique()
            kpis['unique_stores'] = self.sales_data['StoreID'].nunique()
            kpis['unique_products'] = self.sales_data['ProductID'].nunique()
            
            # Profitability metrics
            kpis['total_profit'] = self.sales_data['Profit'].sum()
            kpis['avg_profit_margin'] = self.sales_data['ProfitMargin'].mean()
            kpis['total_discounts'] = self.sales_data['DiscountAmount'].sum()
            
            # Time-based metrics
            date_range = self.sales_data['Date'].max() - self.sales_data['Date'].min()
            kpis['days_analyzed'] = date_range.days
            kpis['avg_daily_revenue'] = kpis['total_revenue'] / kpis['days_analyzed']
            kpis['avg_daily_orders'] = kpis['total_orders'] / kpis['days_analyzed']
        
        if self.customer_data is not None:
            # Customer metrics
            kpis['total_customers'] = len(self.customer_data)
            kpis['active_customers'] = self.customer_data['IsActive'].sum() if 'IsActive' in self.customer_data.columns else 0
            kpis['avg_customer_score'] = self.customer_data['CustomerScore'].mean() if 'CustomerScore' in self.customer_data.columns else 0
            kpis['avg_lifetime_value'] = self.customer_data['LifetimeValue'].mean() if 'LifetimeValue' in self.customer_data.columns else 0
        
        return kpis
    
    def create_visualizations(self, output_dir: str = "reports") -> None:
        """Create comprehensive visualizations"""
        logger.info("Creating visualizations...")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 1. Revenue Trend Analysis
        if self.sales_data is not None:
            self._create_revenue_trend_chart(output_path)
            self._create_daily_sales_pattern(output_path)
            self._create_store_performance_chart(output_path)
            self._create_product_performance_chart(output_path)
        
        # 2. Customer Analysis
        if self.customer_data is not None:
            self._create_customer_demographics(output_path)
            self._create_geographic_distribution(output_path)
            self._create_customer_segmentation(output_path)
    
    def _create_revenue_trend_chart(self, output_path: Path) -> None:
        """Create revenue trend visualization"""
        monthly_sales = self.sales_data.groupby(['Year', 'Month']).agg({
            'TotalAmount': 'sum',
            'OrderID': 'count'
        }).reset_index()
        monthly_sales['Date'] = pd.to_datetime(monthly_sales[['Year', 'Month']].assign(day=1))
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Revenue trend
        ax1.plot(monthly_sales['Date'], monthly_sales['TotalAmount'], marker='o', linewidth=2)
        ax1.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Revenue ($)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Order count trend
        ax2.plot(monthly_sales['Date'], monthly_sales['OrderID'], marker='s', color='orange', linewidth=2)
        ax2.set_title('Monthly Order Count Trend', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Orders', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / 'revenue_trend_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_daily_sales_pattern(self, output_path: Path) -> None:
        """Create daily sales pattern visualization"""
        daily_sales = self.sales_data.groupby('DayOfWeek').agg({
            'TotalAmount': 'sum',
            'OrderID': 'count'
        }).reset_index()
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_sales['DayOfWeek'] = pd.Categorical(daily_sales['DayOfWeek'], categories=day_order, ordered=True)
        daily_sales = daily_sales.sort_values('DayOfWeek')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Revenue by day
        ax1.bar(daily_sales['DayOfWeek'], daily_sales['TotalAmount'], color='skyblue', alpha=0.7)
        ax1.set_title('Revenue by Day of Week', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Revenue ($)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Orders by day
        ax2.bar(daily_sales['DayOfWeek'], daily_sales['OrderID'], color='lightcoral', alpha=0.7)
        ax2.set_title('Orders by Day of Week', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Orders', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_path / 'daily_sales_pattern.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_store_performance_chart(self, output_path: Path) -> None:
        """Create store performance visualization"""
        store_performance = self.sales_data.groupby('StoreID').agg({
            'TotalAmount': 'sum',
            'OrderID': 'count',
            'CustomerID': 'nunique'
        }).reset_index()
        store_performance['AvgOrderValue'] = store_performance['TotalAmount'] / store_performance['OrderID']
        
        # Top 10 stores by revenue
        top_stores = store_performance.nlargest(10, 'TotalAmount')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Revenue by store
        ax1.barh(range(len(top_stores)), top_stores['TotalAmount'], color='lightgreen', alpha=0.7)
        ax1.set_yticks(range(len(top_stores)))
        ax1.set_yticklabels([f'Store {id}' for id in top_stores['StoreID']])
        ax1.set_title('Top 10 Stores by Revenue', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Revenue ($)', fontsize=12)
        
        # Average order value by store
        ax2.barh(range(len(top_stores)), top_stores['AvgOrderValue'], color='gold', alpha=0.7)
        ax2.set_yticks(range(len(top_stores)))
        ax2.set_yticklabels([f'Store {id}' for id in top_stores['StoreID']])
        ax2.set_title('Top 10 Stores by Average Order Value', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Average Order Value ($)', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(output_path / 'store_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_product_performance_chart(self, output_path: Path) -> None:
        """Create product performance visualization"""
        product_performance = self.sales_data.groupby('ProductID').agg({
            'TotalAmount': 'sum',
            'OrderID': 'count',
            'QuantityOrdered': 'sum'
        }).reset_index()
        product_performance['AvgOrderValue'] = product_performance['TotalAmount'] / product_performance['OrderID']
        
        # Top 10 products by revenue
        top_products = product_performance.nlargest(10, 'TotalAmount')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Revenue by product
        ax1.barh(range(len(top_products)), top_products['TotalAmount'], color='lightsteelblue', alpha=0.7)
        ax1.set_yticks(range(len(top_products)))
        ax1.set_yticklabels([f'Product {id}' for id in top_products['ProductID']])
        ax1.set_title('Top 10 Products by Revenue', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Revenue ($)', fontsize=12)
        
        # Quantity sold by product
        ax2.barh(range(len(top_products)), top_products['QuantityOrdered'], color='lightpink', alpha=0.7)
        ax2.set_yticks(range(len(top_products)))
        ax2.set_yticklabels([f'Product {id}' for id in top_products['ProductID']])
        ax2.set_title('Top 10 Products by Quantity Sold', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Quantity Sold', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(output_path / 'product_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_customer_demographics(self, output_path: Path) -> None:
        """Create customer demographics visualization"""
        if self.customer_data is not None and 'Age' in self.customer_data.columns:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Age distribution
            ax1.hist(self.customer_data['Age'], bins=20, color='lightblue', alpha=0.7, edgecolor='black')
            ax1.set_title('Customer Age Distribution', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Age', fontsize=12)
            ax1.set_ylabel('Number of Customers', fontsize=12)
            ax1.grid(True, alpha=0.3)
            
            # Gender distribution
            if 'Gender' in self.customer_data.columns:
                gender_counts = self.customer_data['Gender'].value_counts()
                ax2.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', 
                       colors=['lightcoral', 'lightblue', 'lightgreen'], startangle=90)
                ax2.set_title('Customer Gender Distribution', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(output_path / 'customer_demographics.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def _create_geographic_distribution(self, output_path: Path) -> None:
        """Create geographic distribution visualization"""
        if self.customer_data is not None and 'State' in self.customer_data.columns:
            geographic_analysis = self.customer_data.groupby('State').agg({
                'CustomerID': 'count',
                'LifetimeValue': 'sum'
            }).reset_index()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Customer count by state
            top_states = geographic_analysis.nlargest(10, 'CustomerID')
            ax1.barh(range(len(top_states)), top_states['CustomerID'], color='lightgreen', alpha=0.7)
            ax1.set_yticks(range(len(top_states)))
            ax1.set_yticklabels(top_states['State'])
            ax1.set_title('Top 10 States by Customer Count', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Number of Customers', fontsize=12)
            
            # Lifetime value by state
            top_states_value = geographic_analysis.nlargest(10, 'LifetimeValue')
            ax2.barh(range(len(top_states_value)), top_states_value['LifetimeValue'], color='gold', alpha=0.7)
            ax2.set_yticks(range(len(top_states_value)))
            ax2.set_yticklabels(top_states_value['State'])
            ax2.set_title('Top 10 States by Total Lifetime Value', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Total Lifetime Value ($)', fontsize=12)
            
            plt.tight_layout()
            plt.savefig(output_path / 'geographic_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def _create_customer_segmentation(self, output_path: Path) -> None:
        """Create customer segmentation visualization"""
        if self.customer_data is not None and 'CustomerSegment' in self.customer_data.columns:
            segment_analysis = self.customer_data.groupby('CustomerSegment').agg({
                'CustomerID': 'count',
                'CustomerScore': 'mean',
                'LifetimeValue': 'mean'
            }).reset_index()
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Customer count by segment
            colors = ['gold', 'silver', 'lightblue', 'lightcoral']
            ax1.pie(segment_analysis['CustomerID'], labels=segment_analysis['CustomerSegment'], 
                   autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.set_title('Customer Distribution by Segment', fontsize=14, fontweight='bold')
            
            # Average customer score by segment
            ax2.bar(segment_analysis['CustomerSegment'], segment_analysis['CustomerScore'], 
                   color=colors, alpha=0.7)
            ax2.set_title('Average Customer Score by Segment', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Customer Score', fontsize=12)
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(output_path / 'customer_segmentation.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def generate_report(self, output_dir: str = "reports") -> None:
        """Generate comprehensive analytics report"""
        logger.info("Generating comprehensive analytics report...")
        
        # Load and preprocess data
        self.load_data()
        self.preprocess_data()
        
        # Calculate KPIs
        kpis = self.calculate_kpis()
        
        # Create visualizations
        self.create_visualizations(output_dir)
        
        # Generate report summary
        self._generate_report_summary(kpis, output_dir)
        
        logger.info(f"Analytics report generated successfully in {output_dir}")
    
    def _generate_report_summary(self, kpis: Dict, output_dir: str) -> None:
        """Generate text summary of analytics findings"""
        output_path = Path(output_dir)
        
        summary = {
            'report_generated': datetime.now().isoformat(),
            'kpis': kpis,
            'key_insights': {
                'total_revenue': f"${kpis.get('total_revenue', 0):,.2f}",
                'avg_order_value': f"${kpis.get('avg_order_value', 0):.2f}",
                'total_orders': f"{kpis.get('total_orders', 0):,}",
                'unique_customers': f"{kpis.get('unique_customers', 0):,}",
                'avg_profit_margin': f"{kpis.get('avg_profit_margin', 0):.1f}%"
            },
            'recommendations': [
                "Focus on increasing average order value through cross-selling",
                "Implement customer retention programs for high-value segments",
                "Optimize store performance based on geographic analysis",
                "Develop targeted marketing campaigns for customer segments"
            ]
        }
        
        # Save summary as JSON
        with open(output_path / 'analytics_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Analytics summary saved to {output_path / 'analytics_summary.json'}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Generate e-commerce analytics dashboard')
    parser.add_argument('--data-dir', type=str, default='data/processed', help='Data directory')
    parser.add_argument('--output-dir', type=str, default='reports', help='Output directory')
    
    args = parser.parse_args()
    
    try:
        # Initialize analytics engine
        analytics = EcommerceAnalytics(args.data_dir)
        
        # Generate comprehensive report
        analytics.generate_report(args.output_dir)
        
        print(f"Analytics dashboard generated successfully in {args.output_dir}")
        
    except Exception as e:
        logger.error(f"Error generating analytics dashboard: {str(e)}")
        raise

if __name__ == "__main__":
    main() 