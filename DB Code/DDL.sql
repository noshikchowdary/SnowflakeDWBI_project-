-- =====================================================
-- E-Commerce Analytics Platform - Database Schema
-- Enhanced with modern features for production use
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- =====================================================
-- DIMENSION TABLES
-- =====================================================

-- Enhanced Date Dimension with Business Intelligence
CREATE TABLE DimDate (
    DateID INT PRIMARY KEY,
    Date DATE NOT NULL UNIQUE,
    DayOfWeek VARCHAR(10),
    DayOfWeekNum INT,
    DayOfMonth INT,
    DayOfYear INT,
    WeekOfYear INT,
    Month VARCHAR(10),
    MonthNum INT,
    Quarter INT,
    QuarterName VARCHAR(10),
    Year INT,
    FiscalYear INT,
    FiscalQuarter INT,
    IsWeekend BOOLEAN,
    IsHoliday BOOLEAN DEFAULT FALSE,
    IsBusinessDay BOOLEAN,
    Season VARCHAR(20),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced Customer Dimension with Behavioral Scoring
CREATE TABLE DimCustomer (
    CustomerID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    CustomerUUID UUID DEFAULT uuid_generate_v4(),
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    FullName VARCHAR(101) GENERATED ALWAYS AS (FirstName || ' ' || LastName) STORED,
    Gender VARCHAR(10),
    DateOfBirth DATE,
    Age INT GENERATED ALWAYS AS (EXTRACT(YEAR FROM AGE(CURRENT_DATE, DateOfBirth))) STORED,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(20),
    Address VARCHAR(255),
    City VARCHAR(50),
    State VARCHAR(50),
    ZipCode VARCHAR(10),
    Country VARCHAR(50) DEFAULT 'USA',
    Latitude DECIMAL(10, 8),
    Longitude DECIMAL(11, 8),
    CustomerSegment VARCHAR(50),
    LifetimeValue DECIMAL(12, 2) DEFAULT 0,
    AcquisitionChannel VARCHAR(50),
    AcquisitionDate DATE,
    LoyaltyProgramID INT,
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced Product Dimension with Category Hierarchy
CREATE TABLE DimProduct (
    ProductID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ProductUUID UUID DEFAULT uuid_generate_v4(),
    ProductName VARCHAR(100) NOT NULL,
    ProductSKU VARCHAR(50) UNIQUE,
    Category VARCHAR(50),
    SubCategory VARCHAR(50),
    Brand VARCHAR(50),
    UnitPrice DECIMAL(10, 2),
    CostPrice DECIMAL(10, 2),
    Margin DECIMAL(5, 2) GENERATED ALWAYS AS (
        CASE 
            WHEN UnitPrice > 0 THEN ((UnitPrice - CostPrice) / UnitPrice) * 100
            ELSE 0 
        END
    ) STORED,
    Weight DECIMAL(8, 3),
    Dimensions VARCHAR(50),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced Store Dimension with Geographic Clustering
CREATE TABLE DimStore (
    StoreID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    StoreUUID UUID DEFAULT uuid_generate_v4(),
    StoreName VARCHAR(100) NOT NULL,
    StoreCode VARCHAR(20) UNIQUE,
    StoreType VARCHAR(50),
    StoreTier VARCHAR(20),
    StoreOpeningDate DATE,
    Address VARCHAR(255),
    City VARCHAR(50),
    State VARCHAR(50),
    ZipCode VARCHAR(10),
    Country VARCHAR(50) DEFAULT 'USA',
    Latitude DECIMAL(10, 8),
    Longitude DECIMAL(11, 8),
    ManagerName VARCHAR(100),
    ManagerEmail VARCHAR(100),
    StoreSize DECIMAL(10, 2), -- in square feet
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced Loyalty Program Dimension
CREATE TABLE DimLoyaltyProgram (
    LoyaltyProgramID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ProgramName VARCHAR(100) NOT NULL,
    ProgramTier VARCHAR(50),
    PointsAccrued INT DEFAULT 0,
    PointsRedeemed INT DEFAULT 0,
    CurrentBalance INT GENERATED ALWAYS AS (PointsAccrued - PointsRedeemed) STORED,
    TierLevel VARCHAR(20),
    DiscountPercentage DECIMAL(5, 2),
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- New: Inventory Dimension for Stock Management
CREATE TABLE DimInventory (
    InventoryID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ProductID INT REFERENCES DimProduct(ProductID),
    StoreID INT REFERENCES DimStore(StoreID),
    CurrentStock INT DEFAULT 0,
    ReorderPoint INT DEFAULT 10,
    MaxStock INT DEFAULT 1000,
    LastRestockDate DATE,
    SupplierID INT,
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ProductID, StoreID)
);

-- =====================================================
-- FACT TABLES
-- =====================================================

-- Enhanced Orders Fact Table with Partitioning
CREATE TABLE FactOrders (
    OrderID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    OrderUUID UUID DEFAULT uuid_generate_v4(),
    DateID INT REFERENCES DimDate(DateID),
    CustomerID INT REFERENCES DimCustomer(CustomerID),
    ProductID INT REFERENCES DimProduct(ProductID),
    StoreID INT REFERENCES DimStore(StoreID),
    QuantityOrdered INT NOT NULL,
    UnitPrice DECIMAL(10, 2),
    OrderAmount DECIMAL(10, 2),
    DiscountAmount DECIMAL(10, 2),
    ShippingCost DECIMAL(10, 2),
    TaxAmount DECIMAL(10, 2),
    TotalAmount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    OrderStatus VARCHAR(20),
    FulfillmentTime INT, -- in hours
    ReturnFlag BOOLEAN DEFAULT FALSE,
    ReturnReason VARCHAR(100),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (DateID);

-- Create partitions for FactOrders (example for 2024)
CREATE TABLE FactOrders_2024_01 PARTITION OF FactOrders
    FOR VALUES FROM (20240101) TO (20240201);
CREATE TABLE FactOrders_2024_02 PARTITION OF FactOrders
    FOR VALUES FROM (20240201) TO (20240301);
-- Add more partitions as needed

-- New: Customer Behavior Fact Table
CREATE TABLE FactCustomerBehavior (
    BehaviorID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    DateID INT REFERENCES DimDate(DateID),
    CustomerID INT REFERENCES DimCustomer(CustomerID),
    StoreID INT REFERENCES DimStore(StoreID),
    SessionDuration INT, -- in minutes
    PageViews INT,
    ProductsViewed INT,
    CartAdditions INT,
    WishlistAdditions INT,
    ReviewsSubmitted INT,
    Rating DECIMAL(3, 2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- New: Inventory Transactions Fact Table
CREATE TABLE FactInventoryTransactions (
    TransactionID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    DateID INT REFERENCES DimDate(DateID),
    ProductID INT REFERENCES DimProduct(ProductID),
    StoreID INT REFERENCES DimStore(StoreID),
    TransactionType VARCHAR(20), -- 'IN', 'OUT', 'ADJUSTMENT', 'RETURN'
    Quantity INT,
    UnitCost DECIMAL(10, 2),
    TotalCost DECIMAL(10, 2),
    Reason VARCHAR(100),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Date dimension indexes
CREATE INDEX idx_dimdate_date ON DimDate(Date);
CREATE INDEX idx_dimdate_year_month ON DimDate(Year, MonthNum);

-- Customer dimension indexes
CREATE INDEX idx_dimcustomer_email ON DimCustomer(Email);
CREATE INDEX idx_dimcustomer_segment ON DimCustomer(CustomerSegment);
CREATE INDEX idx_dimcustomer_location ON DimCustomer(City, State);

-- Product dimension indexes
CREATE INDEX idx_dimproduct_sku ON DimProduct(ProductSKU);
CREATE INDEX idx_dimproduct_category ON DimProduct(Category, SubCategory);
CREATE INDEX idx_dimproduct_brand ON DimProduct(Brand);

-- Store dimension indexes
CREATE INDEX idx_dimstore_location ON DimStore(City, State);
CREATE INDEX idx_dimstore_type ON DimStore(StoreType, StoreTier);

-- Fact table indexes
CREATE INDEX idx_factorders_date ON FactOrders(DateID);
CREATE INDEX idx_factorders_customer ON FactOrders(CustomerID);
CREATE INDEX idx_factorders_product ON FactOrders(ProductID);
CREATE INDEX idx_factorders_store ON FactOrders(StoreID);
CREATE INDEX idx_factorders_status ON FactOrders(OrderStatus);

-- Composite indexes for common queries
CREATE INDEX idx_factorders_date_store ON FactOrders(DateID, StoreID);
CREATE INDEX idx_factorders_date_product ON FactOrders(DateID, ProductID);
CREATE INDEX idx_factorders_customer_date ON FactOrders(CustomerID, DateID);

-- =====================================================
-- CONSTRAINTS AND VALIDATIONS
-- =====================================================

-- Check constraints for data quality
ALTER TABLE DimCustomer ADD CONSTRAINT chk_customer_age 
    CHECK (Age >= 0 AND Age <= 120);

ALTER TABLE DimProduct ADD CONSTRAINT chk_product_price 
    CHECK (UnitPrice >= 0);

ALTER TABLE DimStore ADD CONSTRAINT chk_store_size 
    CHECK (StoreSize > 0);

ALTER TABLE FactOrders ADD CONSTRAINT chk_order_amounts 
    CHECK (OrderAmount >= 0 AND TotalAmount >= 0);

ALTER TABLE FactOrders ADD CONSTRAINT chk_quantity 
    CHECK (QuantityOrdered > 0);

-- =====================================================
-- TRIGGERS FOR AUDIT TRAIL
-- =====================================================

-- Function to update UpdatedAt timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.UpdatedAt = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables with UpdatedAt
CREATE TRIGGER update_dimdate_updated_at BEFORE UPDATE ON DimDate
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dimcustomer_updated_at BEFORE UPDATE ON DimCustomer
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dimproduct_updated_at BEFORE UPDATE ON DimProduct
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dimstore_updated_at BEFORE UPDATE ON DimStore
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dimloyalty_updated_at BEFORE UPDATE ON DimLoyaltyProgram
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_diminventory_updated_at BEFORE UPDATE ON DimInventory
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_factorders_updated_at BEFORE UPDATE ON FactOrders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================

-- =====================================================

-- Daily Sales Summary View
CREATE VIEW vw_daily_sales_summary AS
SELECT 
    d.Date,
    d.DayOfWeek,
    d.Month,
    d.Year,
    COUNT(DISTINCT fo.OrderID) as TotalOrders,
    COUNT(DISTINCT fo.CustomerID) as UniqueCustomers,
    SUM(fo.QuantityOrdered) as TotalQuantity,
    SUM(fo.TotalAmount) as TotalRevenue,
    AVG(fo.TotalAmount) as AverageOrderValue,
    SUM(fo.DiscountAmount) as TotalDiscounts
FROM DimDate d
LEFT JOIN FactOrders fo ON d.DateID = fo.DateID
GROUP BY d.Date, d.DayOfWeek, d.Month, d.Year
ORDER BY d.Date DESC;

-- Customer Lifetime Value View
CREATE VIEW vw_customer_lifetime_value AS
SELECT 
    c.CustomerID,
    c.FullName,
    c.CustomerSegment,
    COUNT(DISTINCT fo.OrderID) as TotalOrders,
    SUM(fo.TotalAmount) as LifetimeValue,
    AVG(fo.TotalAmount) as AverageOrderValue,
    MIN(fo.CreatedAt) as FirstOrderDate,
    MAX(fo.CreatedAt) as LastOrderDate,
    EXTRACT(DAYS FROM (MAX(fo.CreatedAt) - MIN(fo.CreatedAt))) as CustomerLifespan
FROM DimCustomer c
LEFT JOIN FactOrders fo ON c.CustomerID = fo.CustomerID
GROUP BY c.CustomerID, c.FullName, c.CustomerSegment
ORDER BY LifetimeValue DESC;

-- Store Performance View
CREATE VIEW vw_store_performance AS
SELECT 
    s.StoreID,
    s.StoreName,
    s.StoreType,
    s.City,
    s.State,
    COUNT(DISTINCT fo.OrderID) as TotalOrders,
    COUNT(DISTINCT fo.CustomerID) as UniqueCustomers,
    SUM(fo.TotalAmount) as TotalRevenue,
    AVG(fo.TotalAmount) as AverageOrderValue,
    SUM(fo.QuantityOrdered) as TotalQuantity
FROM DimStore s
LEFT JOIN FactOrders fo ON s.StoreID = fo.StoreID
GROUP BY s.StoreID, s.StoreName, s.StoreType, s.City, s.State
ORDER BY TotalRevenue DESC;

-- =====================================================
--
-- =====================================================

COMMENT ON TABLE DimDate IS 'Enhanced date dimension with business intelligence features including fiscal periods and holiday indicators';
COMMENT ON TABLE DimCustomer IS 'Customer dimension with behavioral scoring and geographic clustering';
COMMENT ON TABLE DimProduct IS 'Product catalog with category hierarchies and margin calculations';
COMMENT ON TABLE DimStore IS 'Store locations with performance tiers and geographic data';
COMMENT ON TABLE FactOrders IS 'Transaction-level order data with partitioning for performance';
COMMENT ON TABLE FactCustomerBehavior IS 'Customer interaction and engagement metrics';
COMMENT ON TABLE FactInventoryTransactions IS 'Inventory movement tracking for stock management';

COMMENT ON COLUMN DimCustomer.LifetimeValue IS 'Calculated customer lifetime value based on historical purchases';
COMMENT ON COLUMN DimProduct.Margin IS 'Calculated profit margin percentage';
COMMENT ON COLUMN FactOrders.FulfillmentTime IS 'Time from order to fulfillment in hours';