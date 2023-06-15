#!/usr/bin/env python3
"""
Customer Data Generator for E-Commerce Analytics Platform

This script generates realistic customer data with advanced features:
- Geographic clustering and distribution
- Customer segmentation and behavioral patterns
- Loyalty program integration
- Data quality and validation
- Comprehensive logging and error handling

Author: Built for portfolio demonstration
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
import logging
import json
from pathlib import Path
import sys
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/customer_data_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CustomerDataGenerator:
    """Advanced customer data generator with realistic patterns."""
    
    def __init__(self, config_path: str = "config/config.yml"):
        """Initialize the generator with configuration."""
        self.config = self._load_config(config_path)
        self.fake = Faker(['en_US'])
        Faker.seed(42)  # For reproducible results
        
        # Customer segments and their characteristics
        self.customer_segments = self._define_customer_segments()
        self.geographic_clusters = self._define_geographic_clusters()
        self.acquisition_channels = self._define_acquisition_channels()
        
        logger.info("CustomerDataGenerator initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            import yaml
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {
                'num_customers': 10000,
                'data_quality': {
                    'missing_rate': 0.02,
                    'duplicate_rate': 0.001,
                    'invalid_email_rate': 0.01
                }
            }
    
    def _define_customer_segments(self) -> Dict:
        """Define customer segments with their characteristics."""
        return {
            'Premium': {
                'weight': 0.1,
                'avg_age': 45,
                'income_range': (80000, 200000),
                'loyalty_tier': 'Gold',
                'acquisition_channels': ['Direct', 'Referral', 'Organic Search'],
                'geographic_preference': ['Urban', 'Suburban']
            },
            'Regular': {
                'weight': 0.5,
                'avg_age': 35,
                'income_range': (40000, 80000),
                'loyalty_tier': 'Silver',
                'acquisition_channels': ['Organic Search', 'Social Media', 'Email'],
                'geographic_preference': ['Suburban', 'Urban']
            },
            'Occasional': {
                'weight': 0.3,
                'avg_age': 28,
                'income_range': (25000, 50000),
                'loyalty_tier': 'Bronze',
                'acquisition_channels': ['Social Media', 'Paid Ads', 'Email'],
                'geographic_preference': ['Urban', 'Rural']
            },
            'New': {
                'weight': 0.1,
                'avg_age': 25,
                'income_range': (20000, 40000),
                'loyalty_tier': 'Bronze',
                'acquisition_channels': ['Paid Ads', 'Social Media', 'Organic Search'],
                'geographic_preference': ['Urban', 'Suburban']
            }
        }
    
    def _define_geographic_clusters(self) -> Dict:
        """Define geographic clusters for realistic distribution."""
        return {
            'Urban': {
                'cities': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
                'states': ['NY', 'CA', 'IL', 'TX', 'AZ'],
                'weight': 0.4
            },
            'Suburban': {
                'cities': ['San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville'],
                'states': ['CA', 'TX', 'CA', 'TX', 'FL'],
                'weight': 0.4
            },
            'Rural': {
                'cities': ['Fresno', 'Sacramento', 'Mesa', 'Atlanta', 'Raleigh'],
                'states': ['CA', 'CA', 'AZ', 'GA', 'NC'],
                'weight': 0.2
            }
        }
    
    def _define_acquisition_channels(self) -> Dict:
        """Define customer acquisition channels with effectiveness."""
        return {
            'Organic Search': {'weight': 0.3, 'effectiveness': 0.8},
            'Paid Ads': {'weight': 0.2, 'effectiveness': 0.6},
            'Social Media': {'weight': 0.2, 'effectiveness': 0.7},
            'Email': {'weight': 0.15, 'effectiveness': 0.5},
            'Direct': {'weight': 0.1, 'effectiveness': 0.9},
            'Referral': {'weight': 0.05, 'effectiveness': 0.9}
        }
    
    def _generate_customer_segment(self) -> str:
        """Generate customer segment based on weights."""
        segments = list(self.customer_segments.keys())
        weights = [self.customer_segments[seg]['weight'] for seg in segments]
        return random.choices(segments, weights=weights)[0]
    
    def _generate_geographic_location(self, segment: str) -> Tuple[str, str, str]:
        """Generate geographic location based on segment preferences."""
        segment_prefs = self.customer_segments[segment]['geographic_preference']
        location_type = random.choice(segment_prefs)
        
        cluster = self.geographic_clusters[location_type]
        city_idx = random.randint(0, len(cluster['cities']) - 1)
        
        city = cluster['cities'][city_idx]
        state = cluster['states'][city_idx]
        
        # Generate realistic zip code
        zip_code = f"{random.randint(10000, 99999)}"
        
        return city, state, zip_code
    
    def _generate_customer_profile(self, customer_id: int) -> Dict:
        """Generate a complete customer profile."""
        # Determine segment first
        segment = self._generate_customer_segment()
        segment_config = self.customer_segments[segment]
        
        # Generate geographic location
        city, state, zip_code = self._generate_geographic_location(segment)
        
        # Generate personal information
        gender = random.choice(['Male', 'Female', 'Other'])
        first_name = self.fake.first_name_male() if gender == 'Male' else self.fake.first_name_female()
        last_name = self.fake.last_name()
        
        # Generate age based on segment
        avg_age = segment_config['avg_age']
        age = max(18, min(80, int(random.normalvariate(avg_age, 10))))
        birth_year = datetime.now().year - age
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Safe for all months
        date_of_birth = datetime(birth_year, birth_month, birth_day).date()
        
        # Generate contact information
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{self.fake.free_email_domain()}"
        phone = self.fake.phone_number()
        
        # Generate address
        address = self.fake.street_address()
        
        # Generate coordinates (approximate for the city)
        latitude = random.uniform(25.0, 49.0)  # Continental US
        longitude = random.uniform(-125.0, -66.0)  # Continental US
        
        # Generate acquisition information
        acquisition_channel = random.choice(segment_config['acquisition_channels'])
        acquisition_date = self.fake.date_between(start_date='-2y', end_date='today')
        
        # Generate loyalty program information
        loyalty_tier = segment_config['loyalty_tier']
        points_accrued = random.randint(0, 50000) if loyalty_tier != 'Bronze' else random.randint(0, 5000)
        points_redeemed = random.randint(0, points_accrued // 2)
        
        # Calculate lifetime value based on segment
        base_lifetime_value = random.uniform(*segment_config['income_range']) * 0.1
        lifetime_value = base_lifetime_value * random.uniform(0.5, 2.0)
        
        # Generate customer record
        customer_record = {
            'CustomerID': customer_id,
            'FirstName': first_name,
            'LastName': last_name,
            'Gender': gender,
            'DateOfBirth': date_of_birth,
            'Email': email,
            'Phone': phone,
            'Address': address,
            'City': city,
            'State': state,
            'ZipCode': zip_code,
            'Country': 'USA',
            'Latitude': round(latitude, 6),
            'Longitude': round(longitude, 6),
            'CustomerSegment': segment,
            'LifetimeValue': round(lifetime_value, 2),
            'AcquisitionChannel': acquisition_channel,
            'AcquisitionDate': acquisition_date,
            'LoyaltyProgramID': customer_id,
            'IsActive': random.random() > 0.05,  # 95% active customers
            'CreatedAt': datetime.now(),
            'UpdatedAt': datetime.now()
        }
        
        return customer_record
    
    def _generate_loyalty_program_data(self, customer_id: int, segment: str) -> Dict:
        """Generate loyalty program data for customer."""
        segment_config = self.customer_segments[segment]
        loyalty_tier = segment_config['loyalty_tier']
        
        # Define tier-specific benefits
        tier_benefits = {
            'Bronze': {'discount': 5.0, 'points_multiplier': 1.0},
            'Silver': {'discount': 10.0, 'points_multiplier': 1.5},
            'Gold': {'discount': 15.0, 'points_multiplier': 2.0}
        }
        
        benefits = tier_benefits[loyalty_tier]
        points_accrued = random.randint(0, 50000) if loyalty_tier != 'Bronze' else random.randint(0, 5000)
        points_redeemed = random.randint(0, points_accrued // 2)
        
        return {
            'LoyaltyProgramID': customer_id,
            'ProgramName': f'{loyalty_tier} Rewards Program',
            'ProgramTier': loyalty_tier,
            'PointsAccrued': points_accrued,
            'PointsRedeemed': points_redeemed,
            'TierLevel': loyalty_tier,
            'DiscountPercentage': benefits['discount'],
            'IsActive': True,
            'CreatedAt': datetime.now(),
            'UpdatedAt': datetime.now()
        }
    
    def generate_customer_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Generate comprehensive customer and loyalty program data."""
        logger.info("Starting customer data generation...")
        
        customer_records = []
        loyalty_records = []
        
        for customer_id in range(1, self.config['num_customers'] + 1):
            if customer_id % 1000 == 0:
                logger.info(f"Generated {customer_id} customers...")
            
            # Generate customer profile
            customer_record = self._generate_customer_profile(customer_id)
            customer_records.append(customer_record)
            
            # Generate loyalty program data
            loyalty_record = self._generate_loyalty_program_data(
                customer_id, 
                customer_record['CustomerSegment']
            )
            loyalty_records.append(loyalty_record)
        
        # Convert to DataFrames
        customers_df = pd.DataFrame(customer_records)
        loyalty_df = pd.DataFrame(loyalty_records)
        
        # Apply data quality controls
        customers_df = self._apply_data_quality_controls(customers_df)
        
        logger.info(f"Generated {len(customers_df)} customer records")
        return customers_df, loyalty_df
    
    def _apply_data_quality_controls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply data quality controls and validations."""
        logger.info("Applying data quality controls...")
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['Email'])
        logger.info(f"Removed {initial_count - len(df)} duplicate email records")
        
        # Validate email format
        df['Email'] = df['Email'].apply(self._validate_email)
        
        # Ensure age is reasonable
        df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'])
        current_date = pd.Timestamp.now()
        df['Age'] = (current_date - df['DateOfBirth']).dt.days // 365
        df = df[df['Age'].between(18, 100)]
        
        # Validate phone numbers
        df['Phone'] = df['Phone'].apply(self._clean_phone_number)
        
        # Ensure coordinates are within reasonable bounds
        df = df[
            (df['Latitude'].between(25, 49)) & 
            (df['Longitude'].between(-125, -66))
        ]
        
        return df
    
    def _validate_email(self, email: str) -> str:
        """Validate and clean email address."""
        if pd.isna(email) or '@' not in str(email):
            return f"invalid{random.randint(1000, 9999)}@example.com"
        return str(email).lower()
    
    def _clean_phone_number(self, phone: str) -> str:
        """Clean and format phone number."""
        if pd.isna(phone):
            return self.fake.phone_number()
        
        # Remove non-numeric characters
        cleaned = ''.join(filter(str.isdigit, str(phone)))
        
        # Ensure it's a valid US phone number
        if len(cleaned) == 10:
            return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
        elif len(cleaned) == 11 and cleaned[0] == '1':
            return f"({cleaned[1:4]}) {cleaned[4:7]}-{cleaned[7:]}"
        else:
            return self.fake.phone_number()
    
    def save_data(self, customers_df: pd.DataFrame, loyalty_df: pd.DataFrame, 
                  output_dir: str = "data/processed"):
        """Save the generated data to files."""
        # Ensure directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Save customer data
        customers_path = f"{output_dir}/customers.csv"
        customers_df.to_csv(customers_path, index=False)
        logger.info(f"Customer data saved to {customers_path}")
        
        # Save loyalty program data
        loyalty_path = f"{output_dir}/loyalty_programs.csv"
        loyalty_df.to_csv(loyalty_path, index=False)
        logger.info(f"Loyalty program data saved to {loyalty_path}")
        
        # Generate summary statistics
        self._generate_summary_stats(customers_df, loyalty_df, output_dir)
    
    def _generate_summary_stats(self, customers_df: pd.DataFrame, 
                               loyalty_df: pd.DataFrame, output_dir: str):
        """Generate and save summary statistics."""
        summary = {
            'total_customers': len(customers_df),
            'customer_segments': customers_df['CustomerSegment'].value_counts().to_dict(),
            'geographic_distribution': {
                'states': customers_df['State'].value_counts().head(10).to_dict(),
                'cities': customers_df['City'].value_counts().head(10).to_dict()
            },
            'acquisition_channels': customers_df['AcquisitionChannel'].value_counts().to_dict(),
            'loyalty_tiers': loyalty_df['TierLevel'].value_counts().to_dict(),
            'average_lifetime_value': float(customers_df['LifetimeValue'].mean()),
            'total_lifetime_value': float(customers_df['LifetimeValue'].sum()),
            'active_customers': int(customers_df['IsActive'].sum()),
            'total_points_accrued': int(loyalty_df['PointsAccrued'].sum()),
            'total_points_redeemed': int(loyalty_df['PointsRedeemed'].sum())
        }
        
        summary_path = f"{output_dir}/customer_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary statistics saved to {summary_path}")

def main():
    """Main execution function."""
    try:
        logger.info("Starting Customer Data Generation")
        
        # Initialize generator
        generator = CustomerDataGenerator()
        
        # Generate data
        customers_df, loyalty_df = generator.generate_customer_data()
        
        # Save data
        generator.save_data(customers_df, loyalty_df)
        
        logger.info("Customer data generation completed successfully!")
        
        # Print summary
        print(f"\n👥 Generated {len(customers_df):,} customer records")
        print(f"🎯 Customer Segments:")
        for segment, count in customers_df['CustomerSegment'].value_counts().items():
            print(f"   {segment}: {count:,} ({count/len(customers_df)*100:.1f}%)")
        print(f"💰 Average Lifetime Value: ${customers_df['LifetimeValue'].mean():.2f}")
        print(f"🏆 Loyalty Tiers:")
        for tier, count in loyalty_df['TierLevel'].value_counts().items():
            print(f"   {tier}: {count:,}")
        print(f"📍 Top States: {', '.join(customers_df['State'].value_counts().head(3).index.tolist())}")
        
    except Exception as e:
        logger.error(f"Error in customer data generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 