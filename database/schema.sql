-- ==========================================================
-- TransitOps Database Schema
-- Author: Team TransitOps
-- Database: PostgreSQL
-- ==========================================================

-- ==========================================================
-- DROP TABLES (Development Only)
-- ==========================================================

DROP TABLE IF EXISTS expenses CASCADE;
DROP TABLE IF EXISTS fuel_logs CASCADE;
DROP TABLE IF EXISTS maintenance_requests CASCADE;
DROP TABLE IF EXISTS trips CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS drivers CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS organizations CASCADE;

-- ==========================================================
-- ENUMS
-- ==========================================================

CREATE TYPE organization_status_enum AS ENUM
(
    'ACTIVE',
    'INACTIVE'
);

CREATE TYPE employment_status_enum AS ENUM
(
    'ACTIVE',
    'INACTIVE',
    'SUSPENDED',
    'RESIGNED'
);

CREATE TYPE driver_status_enum AS ENUM
(
    'AVAILABLE',
    'ON_TRIP',
    'OFF_DUTY',
    'SUSPENDED'
);

CREATE TYPE vehicle_status_enum AS ENUM
(
    'AVAILABLE',
    'ON_TRIP',
    'IN_MAINTENANCE',
    'RETIRED'
);

CREATE TYPE trip_status_enum AS ENUM
(
    'PLANNED',
    'IN_PROGRESS',
    'COMPLETED',
    'CANCELLED'
);

CREATE TYPE maintenance_status_enum AS ENUM
(
    'PENDING',
    'APPROVED',
    'IN_PROGRESS',
    'COMPLETED',
    'REJECTED'
);

CREATE TYPE priority_enum AS ENUM
(
    'LOW',
    'MEDIUM',
    'HIGH',
    'CRITICAL'
);

-- ==========================================================
-- ORGANIZATIONS
-- ==========================================================

CREATE TABLE organizations
(
    organization_id SERIAL PRIMARY KEY,

    organization_code VARCHAR(20) UNIQUE NOT NULL,

    organization_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    phone VARCHAR(15),

    address TEXT,

    organization_status organization_status_enum
        DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN DEFAULT FALSE,

    deleted_at TIMESTAMP
);

-- ==========================================================
-- ROLES
-- ==========================================================

CREATE TABLE roles
(
    role_id SERIAL PRIMARY KEY,

    role_name VARCHAR(50) UNIQUE NOT NULL,

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN DEFAULT FALSE,

    deleted_at TIMESTAMP
);

-- Default Roles

INSERT INTO roles(role_name,description)
VALUES
('Admin','System Administrator'),
('Fleet Manager','Fleet Management'),
('Driver','Vehicle Driver'),
('Safety Officer','Safety Management'),
('Financial Analyst','Finance & Reports');



-- ==========================================================
-- USERS
-- ==========================================================

CREATE TABLE users
(
    user_id SERIAL PRIMARY KEY,

    organization_id INTEGER NOT NULL,

    role_id INTEGER NOT NULL,

    employee_code VARCHAR(20) UNIQUE,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    phone VARCHAR(15),

    password_hash TEXT NOT NULL,

    must_change_password BOOLEAN DEFAULT TRUE,

    employment_status employment_status_enum
        DEFAULT 'ACTIVE',

    created_by INTEGER,

    updated_by INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN DEFAULT FALSE,

    deleted_at TIMESTAMP,

    CONSTRAINT fk_user_organization
        FOREIGN KEY (organization_id)
        REFERENCES organizations(organization_id),

    CONSTRAINT fk_user_role
        FOREIGN KEY (role_id)
        REFERENCES roles(role_id)
);

-- ==========================================================
-- DRIVERS
-- ==========================================================

CREATE TABLE drivers
(
    driver_id SERIAL PRIMARY KEY,

    user_id INTEGER UNIQUE NOT NULL,

    license_number VARCHAR(50) UNIQUE NOT NULL,

    license_category VARCHAR(20)
        CHECK (
            license_category IN
            (
                'LMV',
                'HMV',
                'MCWG',
                'HPMV',
                'TRANS'
            )
        ),

    license_expiry DATE NOT NULL,

    safety_score DECIMAL(5,2)
        DEFAULT 100.00
        CHECK (safety_score >= 0 AND safety_score <= 100),

    driver_status driver_status_enum
        DEFAULT 'AVAILABLE',

    created_by INTEGER,

    updated_by INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN DEFAULT FALSE,

    deleted_at TIMESTAMP,

    CONSTRAINT fk_driver_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

-- ==========================================================
-- SELF REFERENCING FOREIGN KEYS
-- ==========================================================

ALTER TABLE users
ADD CONSTRAINT fk_users_created_by
FOREIGN KEY (created_by)
REFERENCES users(user_id);

ALTER TABLE users
ADD CONSTRAINT fk_users_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(user_id);

ALTER TABLE drivers
ADD CONSTRAINT fk_drivers_created_by
FOREIGN KEY (created_by)
REFERENCES users(user_id);

ALTER TABLE drivers
ADD CONSTRAINT fk_drivers_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(user_id);


-- ==========================================================
-- VEHICLE TYPES
-- ==========================================================

CREATE TABLE vehicle_types
(
    vehicle_type_id SERIAL PRIMARY KEY,

    type_name VARCHAR(50) UNIQUE NOT NULL,

    description TEXT
);

INSERT INTO vehicle_types(type_name, description)
VALUES
('Truck', 'Heavy Goods Vehicle'),
('Van', 'Light Commercial Vehicle'),
('Bus', 'Passenger Transport'),
('Bike', 'Two Wheeler'),
('Car', 'Four Wheeler');

-- ==========================================================
-- VEHICLES
-- ==========================================================

CREATE TABLE vehicles
(
    vehicle_id SERIAL PRIMARY KEY,

    organization_id INTEGER NOT NULL,

    vehicle_type_id INTEGER NOT NULL,

    vehicle_code VARCHAR(20) UNIQUE,

    registration_number VARCHAR(20) UNIQUE NOT NULL,

    manufacturer VARCHAR(100) NOT NULL,

    model VARCHAR(100) NOT NULL,

    manufacturing_year INTEGER
        CHECK (manufacturing_year >= 1980),

    maximum_load_capacity DECIMAL(10,2)
        CHECK (maximum_load_capacity >= 0),

    odometer INTEGER DEFAULT 0
        CHECK (odometer >= 0),

    acquisition_cost DECIMAL(12,2)
        CHECK (acquisition_cost >= 0),

    vehicle_status vehicle_status_enum
        DEFAULT 'AVAILABLE',

    created_by INTEGER,

    updated_by INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN DEFAULT FALSE,

    deleted_at TIMESTAMP,

    CONSTRAINT fk_vehicle_org
        FOREIGN KEY (organization_id)
        REFERENCES organizations(organization_id),

    CONSTRAINT fk_vehicle_type
        FOREIGN KEY (vehicle_type_id)
        REFERENCES vehicle_types(vehicle_type_id)
);

-- ==========================================================
-- TRIPS
-- ==========================================================

CREATE TABLE trips
(
    trip_id SERIAL PRIMARY KEY,

    trip_code VARCHAR(20) UNIQUE,

    organization_id INTEGER NOT NULL,

    vehicle_id INTEGER NOT NULL,

    driver_id INTEGER NOT NULL,

    created_by INTEGER,

    updated_by INTEGER,

    source VARCHAR(150) NOT NULL,

    destination VARCHAR(150) NOT NULL,

    cargo_weight DECIMAL(10,2)
        CHECK (cargo_weight >= 0),

    planned_distance DECIMAL(10,2)
        CHECK (planned_distance >= 0),

    actual_distance DECIMAL(10,2)
        CHECK (actual_distance >= 0),

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    trip_status trip_status_enum
        DEFAULT 'PLANNED',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_trip_org
        FOREIGN KEY (organization_id)
        REFERENCES organizations(organization_id),

    CONSTRAINT fk_trip_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id),

    CONSTRAINT fk_trip_driver
        FOREIGN KEY (driver_id)
        REFERENCES drivers(driver_id)
);

-- ==========================================================
-- MAINTENANCE REQUESTS
-- ==========================================================

CREATE TABLE maintenance_requests
(
    maintenance_request_id SERIAL PRIMARY KEY,

    maintenance_code VARCHAR(20) UNIQUE,

    vehicle_id INTEGER NOT NULL,

    reported_by INTEGER NOT NULL,

    approved_by INTEGER,

    created_by INTEGER,

    updated_by INTEGER,

    issue_title VARCHAR(150) NOT NULL,

    description TEXT,

    priority priority_enum
        DEFAULT 'MEDIUM',

    maintenance_status maintenance_status_enum
        DEFAULT 'PENDING',

    requested_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    approved_date TIMESTAMP,

    completed_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_maintenance_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id),

    CONSTRAINT fk_maintenance_reported
        FOREIGN KEY (reported_by)
        REFERENCES users(user_id),

    CONSTRAINT fk_maintenance_approved
        FOREIGN KEY (approved_by)
        REFERENCES users(user_id)
);

-- ==========================================================
-- SELF REFERENCING FOREIGN KEYS
-- ==========================================================

ALTER TABLE vehicles
ADD CONSTRAINT fk_vehicle_created_by
FOREIGN KEY (created_by)
REFERENCES users(user_id);

ALTER TABLE vehicles
ADD CONSTRAINT fk_vehicle_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(user_id);

ALTER TABLE trips
ADD CONSTRAINT fk_trip_created_by
FOREIGN KEY (created_by)
REFERENCES users(user_id);

ALTER TABLE trips
ADD CONSTRAINT fk_trip_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(user_id);

ALTER TABLE maintenance_requests
ADD CONSTRAINT fk_maintenance_created_by
FOREIGN KEY (created_by)
REFERENCES users(user_id);

ALTER TABLE maintenance_requests
ADD CONSTRAINT fk_maintenance_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(user_id);



-- ==========================================================
-- EXPENSE TYPES
-- ==========================================================

CREATE TABLE expense_types
(
    expense_type_id SERIAL PRIMARY KEY,

    type_name VARCHAR(50) UNIQUE NOT NULL,

    description TEXT
);

INSERT INTO expense_types(type_name, description)
VALUES
('Fuel','Fuel Expense'),
('Toll','Road Toll'),
('Parking','Parking Charges'),
('Repair','Vehicle Repair'),
('Food','Food Allowance'),
('Other','Miscellaneous');

-- ==========================================================
-- FUEL LOGS
-- ==========================================================

CREATE TABLE fuel_logs
(
    fuel_log_id SERIAL PRIMARY KEY,

    fuel_code VARCHAR(20) UNIQUE,

    trip_id INTEGER NOT NULL,

    vehicle_id INTEGER NOT NULL,

    created_by INTEGER,

    updated_by INTEGER,

    fuel_station VARCHAR(100),

    fuel_type VARCHAR(20)
        CHECK (fuel_type IN ('PETROL','DIESEL','CNG','EV')),

    liters DECIMAL(8,2)
        CHECK (liters > 0),

    cost DECIMAL(10,2)
        CHECK (cost >= 0),

    odometer_reading INTEGER
        CHECK (odometer_reading >= 0),

    fuel_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fuel_trip
        FOREIGN KEY (trip_id)
        REFERENCES trips(trip_id),

    CONSTRAINT fk_fuel_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id)
);

-- ==========================================================
-- EXPENSES
-- ==========================================================

CREATE TABLE expenses
(
    expense_id SERIAL PRIMARY KEY,

    expense_code VARCHAR(20) UNIQUE,

    trip_id INTEGER NOT NULL,

    vehicle_id INTEGER NOT NULL,

    expense_type_id INTEGER NOT NULL,

    created_by INTEGER,

    updated_by INTEGER,

    amount DECIMAL(10,2)
        CHECK (amount >= 0),

    description TEXT,

    expense_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_expense_trip
        FOREIGN KEY (trip_id)
        REFERENCES trips(trip_id),

    CONSTRAINT fk_expense_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id),

    CONSTRAINT fk_expense_type
        FOREIGN KEY (expense_type_id)
        REFERENCES expense_types(expense_type_id)
);

-- ==========================================================
-- SELF REFERENCING FOREIGN KEYS
-- ==========================================================

ALTER TABLE fuel_logs
ADD CONSTRAINT fk_fuel_created_by
FOREIGN KEY (created_by)
REFERENCES users(user_id);

ALTER TABLE fuel_logs
ADD CONSTRAINT fk_fuel_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(user_id);

ALTER TABLE expenses
ADD CONSTRAINT fk_expense_created_by
FOREIGN KEY (created_by)
REFERENCES users(user_id);

ALTER TABLE expenses
ADD CONSTRAINT fk_expense_updated_by
FOREIGN KEY (updated_by)
REFERENCES users(user_id);