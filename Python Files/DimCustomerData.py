#!/usr/bin/env python3
"""
E-Commerce Analytics Platform - Customer Data Generator
Advanced customer profile generation with behavioral scoring and segmentation
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
from faker import Faker
import geopy.distance
from geopy.geocoders import Nominatim

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('customer_data_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class CustomerConfig:
    """Configuration class for customer data generation"""
    num_customers: int = 5000
    output_dir: str = "data/processed"
    seed: int = 42
    
    # Geographic distribution
    primary_states: List[str] = None
    urban_percentage: float = 0.7
    
    # Demographics
    age_range: Tuple[int, int] = (18, 80)
    gender_distribution: Dict[str, float] = None
    
    # Customer segments
    segment_distribution: Dict[str, float] = None
    
    # Loyalty program
    loyalty_tiers: List[str] = None
    
    def __post_init__(self):
        if self.primary_states is None:
            self.primary_states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
        
        if self.gender_distribution is None:
            self.gender_distribution = {'M': 0.48, 'F': 0.50, 'Other': 0.02}
        
        if self.segment_distribution is None:
            self.segment_distribution = {
                'Premium': 0.15,
                'Regular': 0.60,
                'Budget': 0.20,
                'New': 0.05
            }
        
        if self.loyalty_tiers is None:
            self.loyalty_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']

class CustomerSegmentation:
    """Customer segmentation and behavioral scoring"""
    
    @staticmethod
    def calculate_customer_score(age: int, income_level: str, purchase_frequency: int) -> float:
        """Calculate customer value score based on demographics and behavior"""
        base_score = 50.0
        
        # Age factor (peak spending years 25-55)
        if 25 <= age <= 55:
            age_factor = 1.2
        elif 18 <= age <= 24:
            age_factor = 0.8
        else:
            age_factor = 0.9
        
        # Income factor
        income_factors = {
            'Low': 0.7,
            'Medium': 1.0,
            'High': 1.5,
            'Premium': 2.0
        }
        income_factor = income_factors.get(income_level, 1.0)
        
        # Purchase frequency factor
        frequency_factor = min(1.5, 1.0 + (purchase_frequency / 10))
        
        return base_score * age_factor * income_factor * frequency_factor
    
    @staticmethod
    def assign_customer_segment(score: float, age: int, income_level: str) -> str:
        """Assign customer segment based on score and demographics"""
        if score >= 120 and income_level in ['High', 'Premium']:
            return 'Premium'
        elif score >= 80:
            return 'Regular'
        elif age <= 25 or income_level == 'Low':
            return 'Budget'
        else:
            return 'New'

class GeographicDataGenerator:
    """Generate realistic geographic data with clustering"""
    
    def __init__(self, config: CustomerConfig):
        self.config = config
        self.fake = Faker()
        self.geocoder = Nominatim(user_agent="ecommerce_analytics")
        
        # Major city coordinates for realistic clustering
        self.major_cities = {
            'CA': {'Los Angeles': (34.0522, -118.2437), 'San Francisco': (37.7749, -122.4194)},
            'TX': {'Houston': (29.7604, -95.3698), 'Dallas': (32.7767, -96.7970)},
            'NY': {'New York': (40.7128, -74.0060), 'Buffalo': (42.8864, -78.8784)},
            'FL': {'Miami': (25.7617, -80.1918), 'Orlando': (28.5383, -81.3792)},
            'IL': {'Chicago': (41.8781, -87.6298), 'Springfield': (39.7817, -89.6501)},
            'PA': {'Philadelphia': (39.9526, -75.1652), 'Pittsburgh': (40.4406, -79.9959)},
            'OH': {'Columbus': (39.9612, -82.9988), 'Cleveland': (41.4993, -81.6944)},
            'GA': {'Atlanta': (33.7490, -84.3880), 'Savannah': (32.0809, -81.0912)},
            'NC': {'Charlotte': (35.2271, -80.8431), 'Raleigh': (35.7796, -78.6382)},
            'MI': {'Detroit': (42.3314, -83.0458), 'Grand Rapids': (42.9634, -85.6681)}
        }
    
    def generate_location(self, state: str) -> Dict[str, any]:
        """Generate realistic location data for a given state"""
        # Choose between urban and rural
        is_urban = random.random() < self.config.urban_percentage
        
        if is_urban and state in self.major_cities:
            # Generate location near major cities
            city_name = random.choice(list(self.major_cities[state].keys()))
            base_lat, base_lng = self.major_cities[state][city_name]
            
            # Add some variation around the city center
            lat_variation = random.uniform(-0.5, 0.5)
            lng_variation = random.uniform(-0.5, 0.5)
            
            latitude = base_lat + lat_variation
            longitude = base_lng + lng_variation
            
            city = city_name
        else:
            # Generate random location within state
            latitude = random.uniform(25.0, 49.0)  # Continental US latitude range
            longitude = random.uniform(-125.0, -66.0)  # Continental US longitude range
            city = self.fake.city()
        
        return {
            'latitude': round(latitude, 6),
            'longitude': round(longitude, 6),
            'city': city,
            'state': state,
            'zipcode': self.fake.postcode_in_state(state),
            'country': 'USA'
        }

class CustomerDataGenerator:
    """Advanced customer data generator with realistic profiles"""
    
    def __init__(self, config: CustomerConfig):
        self.config = config
        self.fake = Faker()
        Faker.seed(config.seed)
        random.seed(config.seed)
        np.random.seed(config.seed)
        
        self.geo_generator = GeographicDataGenerator(config)
        self.segmentation = CustomerSegmentation()
        
        # Income levels with realistic distribution
        self.income_levels = ['Low', 'Medium', 'High', 'Premium']
        self.income_weights = [0.4, 0.4, 0.15, 0.05]
        
        # Acquisition channels
        self.acquisition_channels = [
            'Organic Search', 'Paid Search', 'Social Media', 'Email Marketing',
            'Referral', 'Direct', 'Affiliate', 'Retargeting'
        ]
        self.channel_weights = [0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]
    
    def generate_customer_profiles(self) -> pd.DataFrame:
        """Generate comprehensive customer profiles"""
        logger.info(f"Generating {self.config.num_customers} customer profiles...")
        
        customers = []
        
        for i in range(self.config.num_customers):
            # Basic demographics
            gender = np.random.choice(list(self.config.gender_distribution.keys()), 
                                    p=list(self.config.gender_distribution.values()))
            
            if gender == 'M':
                first_name = self.fake.first_name_male()
            elif gender == 'F':
                first_name = self.fake.first_name_female()
            else:
                first_name = self.fake.first_name()
            
            last_name = self.fake.last_name()
            age = random.randint(self.config.age_range[0], self.config.age_range[1])
            date_of_birth = datetime.now() - timedelta(days=age*365 + random.randint(0, 365))
            
            # Geographic data
            state = random.choice(self.config.primary_states)
            location = self.geo_generator.generate_location(state)
            
            # Income and behavioral data
            income_level = np.random.choice(self.income_levels, p=self.income_weights)
            purchase_frequency = random.randint(1, 50)
            acquisition_channel = np.random.choice(self.acquisition_channels, p=self.channel_weights)
            acquisition_date = datetime.now() - timedelta(days=random.randint(1, 1000))
            
            # Customer scoring and segmentation
            customer_score = self.segmentation.calculate_customer_score(age, income_level, purchase_frequency)
            customer_segment = self.segmentation.assign_customer_segment(customer_score, age, income_level)
            
            # Loyalty program
            loyalty_tier = random.choice(self.config.loyalty_tiers)
            loyalty_id = random.randint(1, 5)
            
            # Generate realistic email
            email = f"{first_name.lower()}.{last_name.lower()}@{self.fake.free_email_domain()}"
            
            # Phone number
            phone = self.fake.phone_number()
            
            # Address
            address = self.fake.street_address()
            
            customer = {
                'CustomerID': i + 1,
                'FirstName': first_name,
                'LastName': last_name,
                'Gender': gender,
                'DateOfBirth': date_of_birth.date(),
                'Age': age,
                'Email': email,
                'Phone': phone,
                'Address': address,
                'City': location['city'],
                'State': location['state'],
                'ZipCode': location['zipcode'],
                'Country': location['country'],
                'Latitude': location['latitude'],
                'Longitude': location['longitude'],
                'CustomerSegment': customer_segment,
                'CustomerScore': round(customer_score, 2),
                'IncomeLevel': income_level,
                'PurchaseFrequency': purchase_frequency,
                'AcquisitionChannel': acquisition_channel,
                'AcquisitionDate': acquisition_date.date(),
                'LoyaltyProgramID': loyalty_id,
                'LoyaltyTier': loyalty_tier,
                'IsActive': random.choice([True, True, True, False]),  # 75% active
                'CreatedAt': datetime.now(),
                'UpdatedAt': datetime.now()
            }
            
            customers.append(customer)
        
        df = pd.DataFrame(customers)
        logger.info(f"Generated {len(df)} customer profiles successfully")
        return df
    
    def add_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add computed fields and enrich data"""
        # Full name
        df['FullName'] = df['FirstName'] + ' ' + df['LastName']
        
        # Customer lifetime value (simplified calculation)
        df['LifetimeValue'] = df['CustomerScore'] * df['PurchaseFrequency'] * random.uniform(0.5, 2.0)
        
        # Customer status based on activity and score
        df['CustomerStatus'] = df.apply(
            lambda row: 'VIP' if row['CustomerScore'] > 100 and row['IsActive'] 
            else 'Active' if row['IsActive'] 
            else 'Inactive', axis=1
        )
        
        # Geographic region
        df['Region'] = df['State'].map({
            'CA': 'West', 'TX': 'South', 'NY': 'Northeast', 'FL': 'South',
            'IL': 'Midwest', 'PA': 'Northeast', 'OH': 'Midwest', 'GA': 'South',
            'NC': 'South', 'MI': 'Midwest'
        }).fillna('Other')
        
        return df

class DataQualityChecker:
    """Data quality validation for customer data"""
    
    @staticmethod
    def validate_customer_data(df: pd.DataFrame) -> Dict[str, any]:
        """Validate customer data for quality issues"""
        validation_results = {
            'total_records': len(df),
            'null_counts': df.isnull().sum().to_dict(),
            'duplicates': df.duplicated().sum(),
            'invalid_emails': (~df['Email'].str.contains(r'^[^@]+@[^@]+\.[^@]+$')).sum(),
            'invalid_ages': ((df['Age'] < 18) | (df['Age'] > 100)).sum(),
            'invalid_scores': (df['CustomerScore'] < 0).sum(),
            'quality_score': 0.0
        }
        
        # Calculate quality score
        total_issues = sum(validation_results.values()) - validation_results['total_records']
        validation_results['quality_score'] = max(0, 100 - (total_issues / len(df)) * 100)
        
        return validation_results

class CustomerDataExporter:
    """Export customer data with metadata and validation"""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filepath: str, include_metadata: bool = True):
        """Export customer data to CSV with metadata"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Export main data
        df.to_csv(filepath, index=False)
        logger.info(f"Exported customer data to {filepath}")
        
        if include_metadata:
            # Generate metadata
            metadata = {
                'export_timestamp': datetime.now().isoformat(),
                'total_customers': len(df),
                'columns': list(df.columns),
                'data_types': df.dtypes.to_dict(),
                'summary_stats': {
                    'avg_age': float(df['Age'].mean()),
                    'gender_distribution': df['Gender'].value_counts().to_dict(),
                    'segment_distribution': df['CustomerSegment'].value_counts().to_dict(),
                    'state_distribution': df['State'].value_counts().head(10).to_dict(),
                    'avg_customer_score': float(df['CustomerScore'].mean()),
                    'active_customers': int(df['IsActive'].sum()),
                    'total_lifetime_value': float(df['LifetimeValue'].sum())
                }
            }
            
            metadata_file = filepath.replace('.csv', '_metadata.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            logger.info(f"Exported metadata to {metadata_file}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Generate realistic customer data')
    parser.add_argument('--num-customers', type=int, default=5000, help='Number of customers to generate')
    parser.add_argument('--output-dir', type=str, default='data/processed', help='Output directory')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--format', choices=['csv', 'parquet', 'both'], default='both', help='Output format')
    
    args = parser.parse_args()
    
    # Create configuration
    config = CustomerConfig(
        num_customers=args.num_customers,
        output_dir=args.output_dir,
        seed=args.seed
    )
    
    try:
        # Generate customer data
        generator = CustomerDataGenerator(config)
        customer_data = generator.generate_customer_profiles()
        
        # Add derived fields
        customer_data = generator.add_derived_fields(customer_data)
        
        # Validate data quality
        validator = DataQualityChecker()
        quality_results = validator.validate_customer_data(customer_data)
        
        logger.info(f"Customer data quality score: {quality_results['quality_score']:.2f}%")
        
        if quality_results['quality_score'] < 95:
            logger.warning("Data quality score is below 95%. Review the data for issues.")
        
        # Export data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if args.format in ['csv', 'both']:
            csv_file = f"{config.output_dir}/customer_data_{timestamp}.csv"
            CustomerDataExporter.export_to_csv(customer_data, csv_file)
        
        if args.format in ['parquet', 'both']:
            parquet_file = f"{config.output_dir}/customer_data_{timestamp}.parquet"
            customer_data.to_parquet(parquet_file, index=False)
            logger.info(f"Exported customer data to {parquet_file}")
        
        # Generate summary report
        summary = {
            'generation_timestamp': datetime.now().isoformat(),
            'config': vars(config),
            'quality_results': quality_results,
            'data_summary': {
                'total_customers': len(customer_data),
                'avg_age': float(customer_data['Age'].mean()),
                'gender_distribution': customer_data['Gender'].value_counts().to_dict(),
                'segment_distribution': customer_data['CustomerSegment'].value_counts().to_dict(),
                'avg_customer_score': float(customer_data['CustomerScore'].mean()),
                'active_customers': int(customer_data['IsActive'].sum()),
                'total_lifetime_value': float(customer_data['LifetimeValue'].sum())
            }
        }
        
        summary_file = f"{config.output_dir}/customer_generation_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Customer data generation completed successfully. Summary saved to {summary_file}")
        
    except Exception as e:
        logger.error(f"Error during customer data generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 