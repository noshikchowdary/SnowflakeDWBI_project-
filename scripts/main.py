#!/usr/bin/env python3
"""
E-Commerce Analytics Platform - Main Entry Point
Orchestrates the entire data pipeline and analytics workflow
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
import yaml
import json

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Python_Files.Historical_Sales_Data import SalesConfig, SalesDataGenerator, DataExporter
from Python_Files.DimCustomerData import CustomerConfig, CustomerDataGenerator, CustomerDataExporter
from Python_Files.analytics_dashboard import EcommerceAnalytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ecommerce_analytics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EcommerceAnalyticsPlatform:
    """Main platform orchestrator for e-commerce analytics"""
    
    def __init__(self, config_path: str = "config/config.yml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.project_root = Path(__file__).parent.parent
        
        # Create necessary directories
        self._create_directories()
    
    def _load_config(self) -> dict:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            logger.warning(f"Config file {self.config_path} not found. Using default configuration.")
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            'data_generation': {
                'sales': {
                    'num_orders': 10000,
                    'start_date': '2020-01-01',
                    'end_date': '2024-12-31',
                    'num_stores': 100,
                    'num_products': 1000,
                    'num_customers': 5000
                },
                'customers': {
                    'num_customers': 5000
                }
            },
            'paths': {
                'processed_data': 'data/processed',
                'reports': 'reports'
            }
        }
    
    def _create_directories(self) -> None:
        """Create necessary directories"""
        directories = [
            'data/raw',
            'data/processed', 
            'data/analytics',
            'logs',
            'reports',
            'temp'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        logger.info("Directory structure created")
    
    def generate_sales_data(self, num_orders: int = None) -> None:
        """Generate sales data"""
        logger.info("Starting sales data generation...")
        
        # Get configuration
        sales_config = self.config.get('data_generation', {}).get('sales', {})
        
        # Override with command line arguments if provided
        if num_orders:
            sales_config['num_orders'] = num_orders
        
        # Create configuration object
        config = SalesConfig(
            num_orders=sales_config.get('num_orders', 10000),
            start_date=sales_config.get('start_date', '2020-01-01'),
            end_date=sales_config.get('end_date', '2024-12-31'),
            num_stores=sales_config.get('num_stores', 100),
            num_products=sales_config.get('num_products', 1000),
            num_customers=sales_config.get('num_customers', 5000),
            output_dir=self.config.get('paths', {}).get('processed_data', 'data/processed')
        )
        
        try:
            # Generate data
            generator = SalesDataGenerator(config)
            sales_data = generator.generate_sales_data()
            
            # Export data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_file = f"{config.output_dir}/sales_data_{timestamp}.csv"
            DataExporter.export_to_csv(sales_data, csv_file)
            
            logger.info(f"Sales data generated successfully: {csv_file}")
            
        except Exception as e:
            logger.error(f"Error generating sales data: {str(e)}")
            raise
    
    def generate_customer_data(self, num_customers: int = None) -> None:
        """Generate customer data"""
        logger.info("Starting customer data generation...")
        
        # Get configuration
        customer_config = self.config.get('data_generation', {}).get('customers', {})
        
        # Override with command line arguments if provided
        if num_customers:
            customer_config['num_customers'] = num_customers
        
        # Create configuration object
        config = CustomerConfig(
            num_customers=customer_config.get('num_customers', 5000),
            output_dir=self.config.get('paths', {}).get('processed_data', 'data/processed')
        )
        
        try:
            # Generate data
            generator = CustomerDataGenerator(config)
            customer_data = generator.generate_customer_profiles()
            customer_data = generator.add_derived_fields(customer_data)
            
            # Export data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_file = f"{config.output_dir}/customer_data_{timestamp}.csv"
            CustomerDataExporter.export_to_csv(customer_data, csv_file)
            
            logger.info(f"Customer data generated successfully: {csv_file}")
            
        except Exception as e:
            logger.error(f"Error generating customer data: {str(e)}")
            raise
    
    def generate_analytics_report(self) -> None:
        """Generate comprehensive analytics report"""
        logger.info("Starting analytics report generation...")
        
        try:
            # Initialize analytics engine
            analytics = EcommerceAnalytics(
                data_dir=self.config.get('paths', {}).get('processed_data', 'data/processed')
            )
            
            # Generate report
            output_dir = self.config.get('paths', {}).get('reports', 'reports')
            analytics.generate_report(output_dir)
            
            logger.info(f"Analytics report generated successfully in {output_dir}")
            
        except Exception as e:
            logger.error(f"Error generating analytics report: {str(e)}")
            raise
    
    def run_full_pipeline(self) -> None:
        """Run the complete data pipeline"""
        logger.info("Starting full e-commerce analytics pipeline...")
        
        try:
            # Step 1: Generate customer data
            self.generate_customer_data()
            
            # Step 2: Generate sales data
            self.generate_sales_data()
            
            # Step 3: Generate analytics report
            self.generate_analytics_report()
            
            logger.info("Full pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in full pipeline: {str(e)}")
            raise
    
    def get_status(self) -> dict:
        """Get current platform status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'config_loaded': self.config_path.exists(),
            'directories': {},
            'data_files': {}
        }
        
        # Check directories
        directories = ['data/raw', 'data/processed', 'data/analytics', 'logs', 'reports']
        for directory in directories:
            path = Path(directory)
            status['directories'][directory] = {
                'exists': path.exists(),
                'files_count': len(list(path.glob('*'))) if path.exists() else 0
            }
        
        # Check data files
        processed_dir = Path(self.config.get('paths', {}).get('processed_data', 'data/processed'))
        if processed_dir.exists():
            for file_type in ['sales_data', 'customer_data']:
                files = list(processed_dir.glob(f"*{file_type}*.csv"))
                status['data_files'][file_type] = {
                    'count': len(files),
                    'latest': files[-1].name if files else None
                }
        
        return status

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='E-Commerce Analytics Platform - Complete Data Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline
  python scripts/main.py --full-pipeline
  
  # Generate only sales data
  python scripts/main.py --generate-sales --num-orders 5000
  
  # Generate only customer data
  python scripts/main.py --generate-customers --num-customers 2000
  
  # Generate analytics report
  python scripts/main.py --generate-analytics
  
  # Check platform status
  python scripts/main.py --status
        """
    )
    
    parser.add_argument('--config', type=str, default='config/config.yml',
                       help='Path to configuration file')
    parser.add_argument('--full-pipeline', action='store_true',
                       help='Run the complete data pipeline')
    parser.add_argument('--generate-sales', action='store_true',
                       help='Generate sales data')
    parser.add_argument('--generate-customers', action='store_true',
                       help='Generate customer data')
    parser.add_argument('--generate-analytics', action='store_true',
                       help='Generate analytics report')
    parser.add_argument('--num-orders', type=int,
                       help='Number of orders to generate')
    parser.add_argument('--num-customers', type=int,
                       help='Number of customers to generate')
    parser.add_argument('--status', action='store_true',
                       help='Show platform status')
    
    args = parser.parse_args()
    
    try:
        # Initialize platform
        platform = EcommerceAnalyticsPlatform(args.config)
        
        if args.status:
            # Show status
            status = platform.get_status()
            print(json.dumps(status, indent=2, default=str))
            return
        
        if args.full_pipeline:
            # Run full pipeline
            platform.run_full_pipeline()
        elif args.generate_sales:
            # Generate sales data
            platform.generate_sales_data(args.num_orders)
        elif args.generate_customers:
            # Generate customer data
            platform.generate_customer_data(args.num_customers)
        elif args.generate_analytics:
            # Generate analytics report
            platform.generate_analytics_report()
        else:
            # Show help if no action specified
            parser.print_help()
    
    except Exception as e:
        logger.error(f"Platform error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 