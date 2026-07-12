"""
scripts/seed_data.py

Idempotent-ish demo data seeder. Run once after the DB schema (the SQL
file that creates tables + default roles/vehicle_types) has been applied.

Creates:
  - 1 organization
  - 4 users: 1 Admin, 1 Fleet Manager, 2 Drivers  (password for all: "Passw0rd!")
  - 2 driver profiles (for the 2 driver users)
  - 3 vehicles (using the vehicle_types already seeded by the SQL schema)
  - 3 trips in different statuses (PLANNED, IN_PROGRESS, COMPLETED)

Run with:
    python -m scripts.seed_data
(run from the backend/ directory, with your venv active and DATABASE_URL
pointed at a database that already has the schema.sql applied)
"""

import asyncio
from datetime import datetime, timedelta

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.enums import TripStatus
from app.core.security import hash_password
from app.models.driver import Driver
from app.models.organization import Organization
from app.models.role import Role
from app.models.trip import Trip
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.vehicle_type import VehicleType

DEMO_PASSWORD = "Passw0rd!"


async def get_or_create_organization(db) -> Organization:
    result = await db.execute(
        select(Organization).where(Organization.organization_code == "TRANSITOPS-DEMO")
    )
    org = result.scalar_one_or_none()
    if org is not None:
        print(f"  Organization already exists (id={org.organization_id}), reusing it.")
        return org

    org = Organization(
        organization_code="TRANSITOPS-DEMO",
        organization_name="TransitOps Demo Logistics",
        email="ops@transitops-demo.test",
        phone="9999999999",
        address="123 Fleet Yard Road, Demo City",
    )
    db.add(org)
    await db.flush()
    print(f"  Created organization (id={org.organization_id}).")
    return org


async def get_role_id(db, role_name: str) -> int:
    result = await db.execute(select(Role.role_id).where(Role.role_name == role_name))
    role_id = result.scalar_one_or_none()
    if role_id is None:
        raise RuntimeError(
            f"Role '{role_name}' not found — make sure schema.sql's default INSERT INTO roles ran first."
        )
    return role_id


async def get_vehicle_type_id(db, type_name: str) -> int:
    result = await db.execute(
        select(VehicleType.vehicle_type_id).where(VehicleType.type_name == type_name)
    )
    vt_id = result.scalar_one_or_none()
    if vt_id is None:
        raise RuntimeError(
            f"Vehicle type '{type_name}' not found — make sure schema.sql's default "
            "INSERT INTO vehicle_types ran first."
        )
    return vt_id


async def get_or_create_user(
    db, *, org_id: int, role_id: int, employee_code: str, full_name: str, email: str, phone: str
) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is not None:
        print(f"  User '{email}' already exists (id={user.user_id}), reusing it.")
        return user

    user = User(
        organization_id=org_id,
        role_id=role_id,
        employee_code=employee_code,
        full_name=full_name,
        email=email,
        phone=phone,
        password_hash=hash_password(DEMO_PASSWORD),
        must_change_password=False,
    )
    db.add(user)
    await db.flush()
    print(f"  Created user '{email}' (id={user.user_id}).")
    return user


async def get_or_create_driver(
    db, *, user_id: int, license_number: str, license_category: str, license_expiry
) -> Driver:
    result = await db.execute(select(Driver).where(Driver.user_id == user_id))
    driver = result.scalar_one_or_none()
    if driver is not None:
        print(f"  Driver profile for user_id={user_id} already exists (id={driver.driver_id}).")
        return driver

    driver = Driver(
        user_id=user_id,
        license_number=license_number,
        license_category=license_category,
        license_expiry=license_expiry,
    )
    db.add(driver)
    await db.flush()
    print(f"  Created driver profile for user_id={user_id} (id={driver.driver_id}).")
    return driver


async def get_or_create_vehicle(
    db,
    *,
    org_id: int,
    vehicle_type_id: int,
    vehicle_code: str,
    registration_number: str,
    manufacturer: str,
    model: str,
    manufacturing_year: int,
    maximum_load_capacity,
    acquisition_cost,
) -> Vehicle:
    result = await db.execute(
        select(Vehicle).where(Vehicle.registration_number == registration_number)
    )
    vehicle = result.scalar_one_or_none()
    if vehicle is not None:
        print(f"  Vehicle '{registration_number}' already exists (id={vehicle.vehicle_id}).")
        return vehicle

    vehicle = Vehicle(
        organization_id=org_id,
        vehicle_type_id=vehicle_type_id,
        vehicle_code=vehicle_code,
        registration_number=registration_number,
        manufacturer=manufacturer,
        model=model,
        manufacturing_year=manufacturing_year,
        maximum_load_capacity=maximum_load_capacity,
        acquisition_cost=acquisition_cost,
    )
    db.add(vehicle)
    await db.flush()
    print(f"  Created vehicle '{registration_number}' (id={vehicle.vehicle_id}).")
    return vehicle


async def get_or_create_trip(
    db,
    *,
    trip_code: str,
    org_id: int,
    vehicle_id: int,
    driver_id: int,
    source: str,
    destination: str,
    planned_distance,
    trip_status: TripStatus,
    start_time=None,
    end_time=None,
    actual_distance=None,
) -> Trip:
    result = await db.execute(select(Trip).where(Trip.trip_code == trip_code))
    trip = result.scalar_one_or_none()
    if trip is not None:
        print(f"  Trip '{trip_code}' already exists (id={trip.trip_id}).")
        return trip

    trip = Trip(
        trip_code=trip_code,
        organization_id=org_id,
        vehicle_id=vehicle_id,
        driver_id=driver_id,
        source=source,
        destination=destination,
        planned_distance=planned_distance,
        trip_status=trip_status,
        start_time=start_time,
        end_time=end_time,
        actual_distance=actual_distance,
    )
    db.add(trip)
    await db.flush()
    print(f"  Created trip '{trip_code}' (id={trip.trip_id}).")
    return trip


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        print("Seeding organization...")
        org = await get_or_create_organization(db)

        print("Looking up roles...")
        admin_role_id = await get_role_id(db, "Admin")
        fleet_manager_role_id = await get_role_id(db, "Fleet Manager")
        driver_role_id = await get_role_id(db, "Driver")

        print("Seeding users...")
        admin_user = await get_or_create_user(
            db,
            org_id=org.organization_id,
            role_id=admin_role_id,
            employee_code="EMP-ADMIN-01",
            full_name="Asha Admin",
            email="admin@transitops-demo.test",
            phone="9000000001",
        )
        fleet_manager_user = await get_or_create_user(
            db,
            org_id=org.organization_id,
            role_id=fleet_manager_role_id,
            employee_code="EMP-FM-01",
            full_name="Farhan Fleet",
            email="fleetmanager@transitops-demo.test",
            phone="9000000002",
        )
        driver_user_1 = await get_or_create_user(
            db,
            org_id=org.organization_id,
            role_id=driver_role_id,
            employee_code="EMP-DRV-01",
            full_name="Deepak Driver",
            email="driver1@transitops-demo.test",
            phone="9000000003",
        )
        driver_user_2 = await get_or_create_user(
            db,
            org_id=org.organization_id,
            role_id=driver_role_id,
            employee_code="EMP-DRV-02",
            full_name="Divya Driver",
            email="driver2@transitops-demo.test",
            phone="9000000004",
        )

        print("Seeding driver profiles...")
        driver_1 = await get_or_create_driver(
            db,
            user_id=driver_user_1.user_id,
            license_number="DL-0001-2024",
            license_category="HMV",
            license_expiry=datetime.utcnow().date() + timedelta(days=365 * 3),
        )
        driver_2 = await get_or_create_driver(
            db,
            user_id=driver_user_2.user_id,
            license_number="DL-0002-2024",
            license_category="LMV",
            license_expiry=datetime.utcnow().date() + timedelta(days=365 * 2),
        )

        print("Looking up vehicle types...")
        truck_type_id = await get_vehicle_type_id(db, "Truck")
        van_type_id = await get_vehicle_type_id(db, "Van")
        bus_type_id = await get_vehicle_type_id(db, "Bus")

        print("Seeding vehicles...")
        vehicle_1 = await get_or_create_vehicle(
            db,
            org_id=org.organization_id,
            vehicle_type_id=truck_type_id,
            vehicle_code="VEH-001",
            registration_number="GA-01-AB-1234",
            manufacturer="Tata",
            model="407",
            manufacturing_year=2021,
            maximum_load_capacity=2500.00,
            acquisition_cost=1500000.00,
        )
        vehicle_2 = await get_or_create_vehicle(
            db,
            org_id=org.organization_id,
            vehicle_type_id=van_type_id,
            vehicle_code="VEH-002",
            registration_number="GA-01-CD-5678",
            manufacturer="Mahindra",
            model="Bolero Pickup",
            manufacturing_year=2022,
            maximum_load_capacity=1200.00,
            acquisition_cost=900000.00,
        )
        vehicle_3 = await get_or_create_vehicle(
            db,
            org_id=org.organization_id,
            vehicle_type_id=bus_type_id,
            vehicle_code="VEH-003",
            registration_number="GA-01-EF-9012",
            manufacturer="Ashok Leyland",
            model="Viking",
            manufacturing_year=2020,
            maximum_load_capacity=None,
            acquisition_cost=3200000.00,
        )

        print("Seeding trips...")
        now = datetime.utcnow()
        await get_or_create_trip(
            db,
            trip_code="TRIP-001",
            org_id=org.organization_id,
            vehicle_id=vehicle_1.vehicle_id,
            driver_id=driver_1.driver_id,
            source="Mapusa Warehouse",
            destination="Panaji Depot",
            planned_distance=18.50,
            trip_status=TripStatus.PLANNED,
        )
        await get_or_create_trip(
            db,
            trip_code="TRIP-002",
            org_id=org.organization_id,
            vehicle_id=vehicle_2.vehicle_id,
            driver_id=driver_2.driver_id,
            source="Margao Hub",
            destination="Vasco Port",
            planned_distance=32.00,
            trip_status=TripStatus.IN_PROGRESS,
            start_time=now - timedelta(hours=1, minutes=30),
        )
        await get_or_create_trip(
            db,
            trip_code="TRIP-003",
            org_id=org.organization_id,
            vehicle_id=vehicle_3.vehicle_id,
            driver_id=driver_1.driver_id,
            source="Panaji Depot",
            destination="Calangute Stop",
            planned_distance=14.00,
            actual_distance=14.80,
            trip_status=TripStatus.COMPLETED,
            start_time=now - timedelta(hours=5),
            end_time=now - timedelta(hours=4, minutes=20),
        )

        await db.commit()
        print("\nSeed complete.")
        print(f"  Login as admin:         admin@transitops-demo.test / {DEMO_PASSWORD}")
        print(f"  Login as fleet manager: fleetmanager@transitops-demo.test / {DEMO_PASSWORD}")
        print(f"  Login as driver 1:      driver1@transitops-demo.test / {DEMO_PASSWORD}")
        print(f"  Login as driver 2:      driver2@transitops-demo.test / {DEMO_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(seed())