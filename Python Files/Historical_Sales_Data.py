#!/usr/bin/env python3
"""
Historical Sales Data Generator for E-Commerce Analytics Platform

This script generates realistic historical sales data with advanced features:
- Seasonal patterns and trends
- Customer behavior modeling
- Product performance variations
- Store-specific patterns
- Data quality controls
- Comprehensive logging

Author: Built for portfolio demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import logging
import json
from pathlib import Path
import sys
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sales_data_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class SalesDataGenerator:
    """Advanced sales data generator with realistic business patterns."""
    
    def __init__(self, config_path: str = "config/config.yml"):
        """Initialize the generator with configuration."""
        self.config = self._load_config(config_path)
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2024, 12, 31)
        self.date_range = pd.date_range(self.start_date, self.end_date, freq='D')
        
        # Business patterns
        self.seasonal_patterns = self._define_seasonal_patterns()
        self.weekly_patterns = self._define_weekly_patterns()
        self.holiday_effects = self._define_holiday_effects()
        
        logger.info("SalesDataGenerator initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            import yaml
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {
                'num_stores': 100,
                'num_products': 500,
                'num_customers': 10000,
                'avg_orders_per_day': 1500,
                'data_quality': {
                    'missing_rate': 0.01,
                    'duplicate_rate': 0.005,
                    'outlier_rate': 0.02
                }
            }
    
    def _define_seasonal_patterns(self) -> Dict:
        """Define seasonal business patterns."""
        return {
            'spring': {'multiplier': 1.1, 'months': [3, 4, 5]},
            'summer': {'multiplier': 1.3, 'months': [6, 7, 8]},
            'fall': {'multiplier': 1.2, 'months': [9, 10, 11]},
            'winter': {'multiplier': 1.4, 'months': [12, 1, 2]},
            'holiday_season': {'multiplier': 2.0, 'months': [11, 12]},
            'back_to_school': {'multiplier': 1.5, 'months': [8, 9]},
            'black_friday': {'multiplier': 3.0, 'date': '2024-11-29'},
            'cyber_monday': {'multiplier': 2.5, 'date': '2024-12-02'}
        }
    
    def _define_weekly_patterns(self) -> Dict:
        """Define weekly sales patterns."""
        return {
            0: 0.8,  # Monday
            1: 0.9,  # Tuesday
            2: 1.0,  # Wednesday
            3: 1.1,  # Thursday
            4: 1.3,  # Friday
            5: 1.5,  # Saturday
            6: 1.2   # Sunday
        }
    
    def _define_holiday_effects(self) -> Dict:
        """Define holiday effects on sales."""
        return {
            '2024-01-01': {'multiplier': 0.5, 'name': 'New Year'},
            '2024-02-14': {'multiplier': 1.8, 'name': 'Valentine\'s Day'},
            '2024-03-17': {'multiplier': 1.3, 'name': 'St. Patrick\'s Day'},
            '2024-04-01': {'multiplier': 0.9, 'name': 'April Fool\'s Day'},
            '2024-05-05': {'multiplier': 1.2, 'name': 'Cinco de Mayo'},
            '2024-07-04': {'multiplier': 1.4, 'name': 'Independence Day'},
            '2024-09-02': {'multiplier': 1.1, 'name': 'Labor Day'},
            '2024-10-31': {'multiplier': 1.6, 'name': 'Halloween'},
            '2024-11-28': {'multiplier': 0.3, 'name': 'Thanksgiving'},
            '2024-12-25': {'multiplier': 0.2, 'name': 'Christmas'}
        }
    
    def _calculate_daily_multiplier(self, date: datetime) -> float:
        """Calculate daily sales multiplier based on patterns."""
        multiplier = 1.0
        
        # Weekly pattern
        day_of_week = date.weekday()
        multiplier *= self.weekly_patterns.get(day_of_week, 1.0)
        
        # Seasonal pattern
        month = date.month
        for season, pattern in self.seasonal_patterns.items():
            if 'months' in pattern and month in pattern['months']:
                multiplier *= pattern['multiplier']
                break
        
        # Holiday effect
        date_str = date.strftime('%Y-%m-%d')
        if date_str in self.holiday_effects:
            multiplier *= self.holiday_effects[date_str]['multiplier']
        
        # Random variation (±20%)
        multiplier *= random.uniform(0.8, 1.2)
        
        return max(0.1, multiplier)  # Ensure minimum sales
    
    def _generate_store_performance(self) -> Dict[int, float]:
        """Generate store-specific performance multipliers."""
        store_performance = {}
        for store_id in range(1, self.config['num_stores'] + 1):
            # Base performance with some stores being better/worse
            base_performance = random.normalvariate(1.0, 0.3)
            # Add some geographic clustering effect
            if store_id % 10 == 0:  # Every 10th store is in a high-performing area
                base_performance *= 1.5
            store_performance[store_id] = max(0.3, base_performance)
        
        return store_performance
    
    def _generate_product_popularity(self) -> Dict[int, float]:
        """Generate product-specific popularity scores."""
        product_popularity = {}
        for product_id in range(1, self.config['num_products'] + 1):
            # Some products are more popular than others
            popularity = random.betavariate(2, 5)  # Beta distribution for popularity
            # Add seasonal effects for certain product categories
            if product_id % 50 == 0:  # Seasonal products
                popularity *= 1.5
            product_popularity[product_id] = popularity
        
        return product_popularity
    
    def _generate_customer_segments(self) -> Dict[int, str]:
        """Generate customer segments with different buying patterns."""
        segments = ['Premium', 'Regular', 'Occasional', 'New']
        weights = [0.1, 0.5, 0.3, 0.1]  # Distribution of segments
        
        customer_segments = {}
        for customer_id in range(1, self.config['num_customers'] + 1):
            customer_segments[customer_id] = random.choices(segments, weights=weights)[0]
        
        return customer_segments
    
    def generate_sales_data(self) -> pd.DataFrame:
        """Generate comprehensive sales data."""
        logger.info("Starting sales data generation...")
        
        # Initialize performance multipliers
        store_performance = self._generate_store_performance()
        product_popularity = self._generate_product_popularity()
        customer_segments = self._generate_customer_segments()
        
        sales_records = []
        order_id = 1
        
        for date in self.date_range:
            daily_multiplier = self._calculate_daily_multiplier(date)
            base_orders = int(self.config['avg_orders_per_day'] * daily_multiplier)
            
            logger.info(f"Generating {base_orders} orders for {date.strftime('%Y-%m-%d')}")
            
            for _ in range(base_orders):
                # Generate order details
                customer_id = random.randint(1, self.config['num_customers'])
                store_id = random.randint(1, self.config['num_stores'])
                product_id = random.randint(1, self.config['num_products'])
                
                # Calculate order-specific multipliers
                store_mult = store_performance[store_id]
                product_mult = product_popularity[product_id]
                customer_segment = customer_segments[customer_id]
                
                # Segment-specific adjustments
                segment_multipliers = {
                    'Premium': 2.0,
                    'Regular': 1.0,
                    'Occasional': 0.7,
                    'New': 0.5
                }
                customer_mult = segment_multipliers[customer_segment]
                
                # Generate order quantities and amounts
                quantity = max(1, int(random.exponential(2)))
                unit_price = random.uniform(10, 500)
                order_amount = quantity * unit_price
                
                # Apply multipliers
                total_amount = order_amount * store_mult * product_mult * customer_mult
                
                # Add realistic variations
                discount_rate = random.uniform(0, 0.3) if random.random() < 0.3 else 0
                discount_amount = total_amount * discount_rate
                shipping_cost = random.uniform(0, 15) if total_amount < 50 else 0
                tax_rate = random.uniform(0.06, 0.12)
                tax_amount = (total_amount - discount_amount) * tax_rate
                
                final_amount = total_amount - discount_amount + shipping_cost + tax_amount
                
                # Generate order status
                statuses = ['Completed', 'Processing', 'Shipped', 'Delivered']
                status_weights = [0.7, 0.1, 0.1, 0.1]
                order_status = random.choices(statuses, weights=status_weights)[0]
                
                # Generate fulfillment time
                fulfillment_time = random.exponential(24) if order_status in ['Shipped', 'Delivered'] else None
                
                # Generate return information
                return_flag = random.random() < 0.05  # 5% return rate
                return_reason = None
                if return_flag:
                    reasons = ['Defective', 'Wrong Size', 'Not as Described', 'Changed Mind']
                    return_reason = random.choice(reasons)
                
                # Create sales record
                sales_record = {
                    'OrderID': order_id,
                    'DateID': int(date.strftime('%Y%m%d')),
                    'CustomerID': customer_id,
                    'ProductID': product_id,
                    'StoreID': store_id,
                    'QuantityOrdered': quantity,
                    'UnitPrice': round(unit_price, 2),
                    'OrderAmount': round(order_amount, 2),
                    'DiscountAmount': round(discount_amount, 2),
                    'ShippingCost': round(shipping_cost, 2),
                    'TaxAmount': round(tax_amount, 2),
                    'TotalAmount': round(final_amount, 2),
                    'PaymentMethod': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash']),
                    'OrderStatus': order_status,
                    'FulfillmentTime': int(fulfillment_time) if fulfillment_time else None,
                    'ReturnFlag': return_flag,
                    'ReturnReason': return_reason,
                    'CreatedAt': date,
                    'UpdatedAt': date
                }
                
                sales_records.append(sales_record)
                order_id += 1
        
        # Convert to DataFrame
        sales_df = pd.DataFrame(sales_records)
        
        # Apply data quality controls
        sales_df = self._apply_data_quality_controls(sales_df)
        
        logger.info(f"Generated {len(sales_df)} sales records")
        return sales_df
    
    def _apply_data_quality_controls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply data quality controls and validations."""
        logger.info("Applying data quality controls...")
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df)} duplicate records")
        
        # Validate numeric fields
        df['TotalAmount'] = df['TotalAmount'].clip(lower=0)
        df['QuantityOrdered'] = df['QuantityOrdered'].clip(lower=1)
        df['UnitPrice'] = df['UnitPrice'].clip(lower=0.01)
        
        # Add some realistic outliers (but not too many)
        outlier_indices = random.sample(range(len(df)), int(len(df) * 0.01))
        for idx in outlier_indices:
            if random.random() < 0.5:
                df.loc[idx, 'TotalAmount'] *= random.uniform(5, 10)
            else:
                df.loc[idx, 'QuantityOrdered'] *= random.randint(5, 20)
        
        return df
    
    def save_data(self, df: pd.DataFrame, output_path: str = "data/processed/historical_sales.csv"):
        """Save the generated data to file."""
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Sales data saved to {output_path}")
        
        # Generate summary statistics
        self._generate_summary_stats(df, output_path.replace('.csv', '_summary.json'))
    
    def _generate_summary_stats(self, df: pd.DataFrame, output_path: str):
        """Generate and save summary statistics."""
        summary = {
            'total_records': len(df),
            'date_range': {
                'start': df['CreatedAt'].min().strftime('%Y-%m-%d'),
                'end': df['CreatedAt'].max().strftime('%Y-%m-%d')
            },
            'total_revenue': float(df['TotalAmount'].sum()),
            'avg_order_value': float(df['TotalAmount'].mean()),
            'total_orders': df['OrderID'].nunique(),
            'unique_customers': df['CustomerID'].nunique(),
            'unique_products': df['ProductID'].nunique(),
            'unique_stores': df['StoreID'].nunique(),
            'return_rate': float(df['ReturnFlag'].mean()),
            'top_stores': df.groupby('StoreID')['TotalAmount'].sum().nlargest(5).to_dict(),
            'top_products': df.groupby('ProductID')['QuantityOrdered'].sum().nlargest(5).to_dict()
        }
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary statistics saved to {output_path}")

def main():
    """Main execution function."""
    try:
        logger.info("Starting Historical Sales Data Generation")
        
        # Initialize generator
        generator = SalesDataGenerator()
        
        # Generate data
        sales_data = generator.generate_sales_data()
        
        # Save data
        generator.save_data(sales_data)
        
        logger.info("Historical sales data generation completed successfully!")
        
        # Print summary
        print(f"\n📊 Generated {len(sales_data):,} sales records")
        print(f"💰 Total Revenue: ${sales_data['TotalAmount'].sum():,.2f}")
        print(f"📦 Average Order Value: ${sales_data['TotalAmount'].mean():.2f}")
        print(f"👥 Unique Customers: {sales_data['CustomerID'].nunique():,}")
        print(f"🏪 Unique Stores: {sales_data['StoreID'].nunique():,}")
        print(f"📦 Unique Products: {sales_data['ProductID'].nunique():,}")
        
    except Exception as e:
        logger.error(f"Error in sales data generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 