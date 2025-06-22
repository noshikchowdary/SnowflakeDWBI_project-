#!/usr/bin/env python3
"""
E-Commerce Analytics Platform - Setup Configuration
Modern data warehouse and business intelligence solution
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="ecommerce-analytics-platform",
    version="1.0.0",
    description="A comprehensive data warehouse and business intelligence solution for modern e-commerce operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        "full": [
            "apache-airflow>=2.7.0",
            "celery>=5.3.0",
            "redis>=4.6.0",
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ecommerce-analytics=scripts.main:main",
            "generate-sales-data=Python Files.Historical_Sales_Data:main",
            "generate-customer-data=Python Files.DimCustomerData:main",
            "analytics-dashboard=Python Files.analytics_dashboard:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yml", "*.yaml", "*.json", "*.sql"],
    },
    keywords=[
        "ecommerce",
        "analytics",
        "data-warehouse",
        "business-intelligence",
        "etl",
        "data-pipeline",
        "postgresql",
        "pandas",
        "numpy",
        "visualization",
    ],
) 