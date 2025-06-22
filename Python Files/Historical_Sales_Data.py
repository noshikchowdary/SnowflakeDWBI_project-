#!/usr/bin/env python3
"""
E-Commerce Analytics Platform - Sales Data Generator
Enhanced ETL pipeline for generating realistic sales data with advanced features
"""

import pandas as pd
import numpy as np
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import argparse
from dataclasses import dataclass
import random
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sales_data_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class SalesConfig:
    """Configuration class for sales data generation"""
    start_date: str = "2020-01-01"
    end_date: str = "2024-12-31"
    num_orders: int = 10000
    num_stores: int = 100
    num_products: int = 1000
    num_customers: int = 5000
    output_dir: str = "data/processed"
    seed: int = 42
    
    # Business rules
    min_order_amount: float = 10.0
    max_order_amount: float = 2000.0
    min_quantity: int = 1
    max_quantity: int = 50
    discount_range: Tuple[float, float] = (0.02, 0.25)
    shipping_range: Tuple[float, float] = (0.05, 0.15)
    tax_rate: float = 0.08

class DataQualityChecker:
    """Data quality validation and monitoring"""
    
    @staticmethod
    def validate_sales_data(df: pd.DataFrame) -> Dict[str, any]:
        """Validate generated sales data for quality issues"""
        validation_results = {
            'total_records': len(df),
            'null_counts': df.isnull().sum().to_dict(),
            'duplicates': df.duplicated().sum(),
            'negative_amounts': (df['TotalAmount'] < 0).sum(),
            'zero_amounts': (df['TotalAmount'] == 0).sum(),
            'invalid_dates': (df['DateID'] < 20200101).sum(),
            'quality_score': 0.0
        }
        
        # Calculate quality score
        total_issues = sum(validation_results.values()) - validation_results['total_records']
        validation_results['quality_score'] = max(0, 100 - (total_issues / len(df)) * 100)
        
        return validation_results

class SalesDataGenerator:
    """Advanced sales data generator with realistic business patterns"""
    
    def __init__(self, config: SalesConfig):
        self.config = config
        np.random.seed(config.seed)
        random.seed(config.seed)
        
        # Business patterns
        self.weekend_multiplier = 1.3
        self.holiday_multiplier = 1.5
        self.seasonal_patterns = self._generate_seasonal_patterns()
        self.store_performance = self._generate_store_performance()
        
    def _generate_seasonal_patterns(self) -> Dict[str, float]:
        """Generate realistic seasonal sales patterns"""
        return {
            'Q1': 0.8,  # Winter - lower sales
            'Q2': 1.0,  # Spring - normal sales
            'Q3': 1.1,  # Summer - slightly higher
            'Q4': 1.4   # Holiday season - highest sales
        }
    
    def _generate_store_performance(self) -> Dict[int, float]:
        """Generate store performance multipliers"""
        return {i: np.random.lognormal(0, 0.3) for i in range(1, self.config.num_stores + 1)}
    
    def _generate_realistic_dates(self) -> np.ndarray:
        """Generate dates with realistic business patterns"""
        start = pd.to_datetime(self.config.start_date)
        end = pd.to_datetime(self.config.end_date)
        
        # Generate more dates on weekdays and during peak seasons
        all_dates = pd.date_range(start, end, freq='D')
        
        # Weight dates based on business patterns
        weights = []
        for date in all_dates:
            weight = 1.0
            
            # Weekend effect
            if date.weekday() >= 5:  # Saturday/Sunday
                weight *= self.weekend_multiplier
            
            # Seasonal effect
            quarter = f"Q{(date.month - 1) // 3 + 1}"
            weight *= self.seasonal_patterns[quarter]
            
            # Holiday effect (simplified)
            if date.month == 12:  # December
                weight *= self.holiday_multiplier
            
            weights.append(weight)
        
        weights = np.array(weights)
        weights = weights / weights.sum()
        
        return np.random.choice(all_dates, size=self.config.num_orders, p=weights)
    
    def _generate_order_amounts(self) -> np.ndarray:
        """Generate realistic order amounts with business patterns"""
        # Use log-normal distribution for realistic order amounts
        base_amounts = np.random.lognormal(4.5, 0.8, self.config.num_orders)
        
        # Apply business constraints
        base_amounts = np.clip(base_amounts, 
                              self.config.min_order_amount, 
                              self.config.max_order_amount)
        
        return base_amounts
    
    def _calculate_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived fields like discounts, shipping, taxes, and totals"""
        # Discount calculation (higher discounts for larger orders)
        discount_percentages = np.random.uniform(
            self.config.discount_range[0], 
            self.config.discount_range[1], 
            len(df)
        )
        # Higher discounts for larger orders
        discount_percentages *= (df['OrderAmount'] / self.config.max_order_amount)
        df['DiscountAmount'] = df['OrderAmount'] * discount_percentages
        
        # Shipping calculation
        shipping_percentages = np.random.uniform(
            self.config.shipping_range[0], 
            self.config.shipping_range[1], 
            len(df)
        )
        df['ShippingCost'] = df['OrderAmount'] * shipping_percentages
        
        # Tax calculation
        df['TaxAmount'] = (df['OrderAmount'] - df['DiscountAmount']) * self.config.tax_rate
        
        # Total calculation
        df['TotalAmount'] = (df['OrderAmount'] - df['DiscountAmount'] + 
                           df['ShippingCost'] + df['TaxAmount'])
        
        return df
    
    def generate_sales_data(self) -> pd.DataFrame:
        """Generate comprehensive sales data with business intelligence"""
        logger.info(f"Generating {self.config.num_orders} sales records...")
        
        # Generate realistic dates
        dates = self._generate_realistic_dates()
        date_ids = pd.to_datetime(dates).strftime('%Y%m%d').astype(int)
        
        # Generate order amounts
        order_amounts = self._generate_order_amounts()
        
        # Generate other fields
        data = {
            'DateID': date_ids,
            'ProductID': np.random.randint(1, self.config.num_products + 1, size=self.config.num_orders),
            'StoreID': np.random.randint(1, self.config.num_stores + 1, size=self.config.num_orders),
            'CustomerID': np.random.randint(1, self.config.num_customers + 1, size=self.config.num_orders),
            'QuantityOrdered': np.random.randint(self.config.min_quantity, self.config.max_quantity + 1, size=self.config.num_orders),
            'OrderAmount': order_amounts,
            'PaymentMethod': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], size=self.config.num_orders),
            'OrderStatus': np.random.choice(['Completed', 'Processing', 'Shipped', 'Delivered'], size=self.config.num_orders, p=[0.8, 0.1, 0.05, 0.05])
        }
        
        df = pd.DataFrame(data)
        
        # Calculate derived fields
        df = self._calculate_derived_fields(df)
        
        # Add business intelligence fields
        df['FulfillmentTime'] = np.random.exponential(24, size=len(df))  # Hours
        df['ReturnFlag'] = np.random.choice([True, False], size=len(df), p=[0.05, 0.95])
        df['ReturnReason'] = np.where(df['ReturnFlag'], 
                                    np.random.choice(['Defective', 'Wrong Size', 'Not as Expected', 'Changed Mind'], size=len(df)), 
                                    None)
        
        # Apply store performance adjustments
        for store_id in df['StoreID'].unique():
            mask = df['StoreID'] == store_id
            df.loc[mask, 'TotalAmount'] *= self.store_performance[store_id]
        
        logger.info(f"Generated {len(df)} sales records successfully")
        return df

class DataExporter:
    """Data export functionality with multiple formats and validation"""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filepath: str, include_metadata: bool = True):
        """Export data to CSV with optional metadata"""
        # Create directory if it doesn't exist
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Export main data
        df.to_csv(filepath, index=False)
        logger.info(f"Exported data to {filepath}")
        
        if include_metadata:
            # Export metadata
            metadata = {
                'export_timestamp': datetime.now().isoformat(),
                'total_records': len(df),
                'columns': list(df.columns),
                'data_types': df.dtypes.to_dict(),
                'summary_stats': {
                    'total_revenue': df['TotalAmount'].sum(),
                    'avg_order_value': df['TotalAmount'].mean(),
                    'total_orders': len(df),
                    'unique_customers': df['CustomerID'].nunique(),
                    'unique_stores': df['StoreID'].nunique(),
                    'unique_products': df['ProductID'].nunique()
                }
            }
            
            metadata_file = filepath.replace('.csv', '_metadata.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            logger.info(f"Exported metadata to {metadata_file}")
    
    @staticmethod
    def export_to_parquet(df: pd.DataFrame, filepath: str):
        """Export data to Parquet format for better performance"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(filepath, index=False)
        logger.info(f"Exported data to {filepath}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Generate realistic e-commerce sales data')
    parser.add_argument('--num-orders', type=int, default=10000, help='Number of orders to generate')
    parser.add_argument('--start-date', type=str, default='2020-01-01', help='Start date for data generation')
    parser.add_argument('--end-date', type=str, default='2024-12-31', help='End date for data generation')
    parser.add_argument('--output-dir', type=str, default='data/processed', help='Output directory')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--format', choices=['csv', 'parquet', 'both'], default='both', help='Output format')
    
    args = parser.parse_args()
    
    # Create configuration
    config = SalesConfig(
        start_date=args.start_date,
        end_date=args.end_date,
        num_orders=args.num_orders,
        output_dir=args.output_dir,
        seed=args.seed
    )
    
    try:
        # Generate data
        generator = SalesDataGenerator(config)
        sales_data = generator.generate_sales_data()
        
        # Validate data quality
        validator = DataQualityChecker()
        quality_results = validator.validate_sales_data(sales_data)
        
        logger.info(f"Data quality score: {quality_results['quality_score']:.2f}%")
        
        if quality_results['quality_score'] < 95:
            logger.warning("Data quality score is below 95%. Review the data for issues.")
        
        # Export data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if args.format in ['csv', 'both']:
            csv_file = f"{config.output_dir}/sales_data_{timestamp}.csv"
            DataExporter.export_to_csv(sales_data, csv_file)
        
        if args.format in ['parquet', 'both']:
            parquet_file = f"{config.output_dir}/sales_data_{timestamp}.parquet"
            DataExporter.export_to_parquet(sales_data, parquet_file)
        
        # Generate summary report
        summary = {
            'generation_timestamp': datetime.now().isoformat(),
            'config': vars(config),
            'quality_results': quality_results,
            'data_summary': {
                'total_revenue': float(sales_data['TotalAmount'].sum()),
                'avg_order_value': float(sales_data['TotalAmount'].mean()),
                'total_orders': len(sales_data),
                'date_range': f"{sales_data['DateID'].min()} to {sales_data['DateID'].max()}",
                'unique_customers': sales_data['CustomerID'].nunique(),
                'unique_stores': sales_data['StoreID'].nunique(),
                'unique_products': sales_data['ProductID'].nunique()
            }
        }
        
        summary_file = f"{config.output_dir}/generation_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Data generation completed successfully. Summary saved to {summary_file}")
        
    except Exception as e:
        logger.error(f"Error during data generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()

