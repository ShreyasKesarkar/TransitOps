const ROLE_NAMES = {
  1: 'Admin',
  2: 'Fleet Manager',
  3: 'Driver',
  4: 'Safety Officer',
  5: 'Financial Analyst',
};

const VEHICLE_TYPE_NAMES = {
  1: 'Truck',
  2: 'Van',
  3: 'Bus',
  4: 'Bike',
  5: 'Car',
};

function decodeBase64Url(value) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
  const padded = normalized + '='.repeat((4 - (normalized.length % 4)) % 4);
  return atob(padded);
}

export function decodeJwtPayload(token) {
  if (!token || !token.includes('.')) {
    return null;
  }

  try {
    const [, payload] = token.split('.');
    return JSON.parse(decodeBase64Url(payload));
  } catch {
    return null;
  }
}

export function normalizeAuthUser(apiUser, token) {
  const payload = decodeJwtPayload(token) || {};
  const organizationId = apiUser?.organization_id ?? payload.organization_id ?? null;
  const roleId = apiUser?.role_id ?? payload.role_id ?? null;

  return {
    userId: apiUser?.user_id ?? Number(payload.sub) ?? null,
    fullName: apiUser?.full_name ?? apiUser?.email ?? 'Current User',
    email: apiUser?.email ?? '',
    roleId,
    roleName: payload.role_name ?? ROLE_NAMES[roleId] ?? 'User',
    organizationId,
    organizationName: organizationId ? `Organization ${organizationId}` : 'Organization',
    mustChangePassword: Boolean(apiUser?.must_change_password),
    token,
  };
}

export function normalizeUser(user) {
  const roleId = user.role_id ?? null;

  return {
    id: user.user_id,
    userId: user.user_id,
    organizationId: user.organization_id,
    roleId,
    roleName: ROLE_NAMES[roleId] ?? `Role ${roleId ?? ''}`.trim(),
    employeeCode: user.employee_code,
    fullName: user.full_name,
    email: user.email,
    phone: user.phone,
    employmentStatus: user.employment_status,
    mustChangePassword: user.must_change_password,
    createdBy: user.created_by,
    updatedBy: user.updated_by,
    createdAt: user.created_at,
    updatedAt: user.updated_at,
  };
}

export function serializeUser(values, organizationId) {
  return {
    organization_id: organizationId,
    role_id: Number(values.roleId),
    employee_code: values.employeeCode || null,
    full_name: values.fullName,
    email: values.email,
    phone: values.phone || null,
    password: values.password,
  };
}

export function serializeUserUpdate(values) {
  return {
    role_id: values.roleId ? Number(values.roleId) : undefined,
    employee_code: values.employeeCode || undefined,
    full_name: values.fullName || undefined,
    email: values.email || undefined,
    phone: values.phone || undefined,
    employment_status: values.employmentStatus || undefined,
  };
}

export function normalizeDriver(driver, usersById = {}) {
  const linkedUser = usersById[driver.user_id] || {};

  return {
    id: driver.driver_id,
    driverId: driver.driver_id,
    userId: driver.user_id,
    fullName: linkedUser.fullName ?? linkedUser.full_name ?? `User ${driver.user_id}`,
    email: linkedUser.email ?? '',
    licenseNumber: driver.license_number,
    licenseCategory: driver.license_category,
    licenseExpiry: driver.license_expiry,
    safetyScore: driver.safety_score,
    driverStatus: driver.driver_status,
    createdBy: driver.created_by,
    updatedBy: driver.updated_by,
    createdAt: driver.created_at,
    updatedAt: driver.updated_at,
  };
}

export function serializeDriver(values) {
  return {
    user_id: Number(values.userId),
    license_number: values.licenseNumber,
    license_category: values.licenseCategory || null,
    license_expiry: values.licenseExpiry,
  };
}

export function serializeDriverUpdate(values) {
  return {
    license_number: values.licenseNumber || undefined,
    license_category: values.licenseCategory || undefined,
    license_expiry: values.licenseExpiry || undefined,
    safety_score: values.safetyScore === '' || values.safetyScore === null ? undefined : Number(values.safetyScore),
    driver_status: values.driverStatus || undefined,
  };
}

export function normalizeVehicle(vehicle) {
  return {
    id: vehicle.vehicle_id,
    vehicleId: vehicle.vehicle_id,
    organizationId: vehicle.organization_id,
    vehicleTypeId: vehicle.vehicle_type_id,
    vehicleType: VEHICLE_TYPE_NAMES[vehicle.vehicle_type_id] ?? `Type ${vehicle.vehicle_type_id}`,
    vehicleCode: vehicle.vehicle_code,
    registrationNumber: vehicle.registration_number,
    manufacturer: vehicle.manufacturer,
    model: vehicle.model,
    manufacturingYear: vehicle.manufacturing_year,
    capacity: vehicle.maximum_load_capacity,
    odometer: vehicle.odometer,
    acquisitionCost: vehicle.acquisition_cost,
    vehicleStatus: vehicle.vehicle_status,
    createdBy: vehicle.created_by,
    updatedBy: vehicle.updated_by,
    createdAt: vehicle.created_at,
    updatedAt: vehicle.updated_at,
  };
}

export function serializeVehicle(values, organizationId) {
  return {
    organization_id: organizationId,
    vehicle_type_id: Number(values.vehicleTypeId),
    vehicle_code: values.vehicleCode || null,
    registration_number: values.registrationNumber,
    manufacturer: values.manufacturer,
    model: values.model,
    manufacturing_year: values.manufacturingYear === '' || values.manufacturingYear == null ? undefined : Number(values.manufacturingYear),
    maximum_load_capacity: values.maximumLoadCapacity === '' || values.maximumLoadCapacity == null ? undefined : Number(values.maximumLoadCapacity),
    acquisition_cost: values.acquisitionCost === '' || values.acquisitionCost == null ? undefined : Number(values.acquisitionCost),
    odometer: values.odometer === '' || values.odometer == null ? undefined : Number(values.odometer),
  };
}

export function serializeVehicleUpdate(values) {
  return {
    vehicle_type_id: values.vehicleTypeId ? Number(values.vehicleTypeId) : undefined,
    vehicle_code: values.vehicleCode || undefined,
    manufacturer: values.manufacturer || undefined,
    model: values.model || undefined,
    manufacturing_year: values.manufacturingYear === '' || values.manufacturingYear == null ? undefined : Number(values.manufacturingYear),
    maximum_load_capacity: values.maximumLoadCapacity === '' || values.maximumLoadCapacity == null ? undefined : Number(values.maximumLoadCapacity),
    odometer: values.odometer === '' || values.odometer == null ? undefined : Number(values.odometer),
    acquisition_cost: values.acquisitionCost === '' || values.acquisitionCost == null ? undefined : Number(values.acquisitionCost),
    vehicle_status: values.vehicleStatus || undefined,
  };
}

export function normalizeTrip(trip, driversById = {}, vehiclesById = {}, usersById = {}) {
  const driverUser = usersById[driversById[trip.driver_id]?.userId] || usersById[trip.driver?.user_id] || {};
  const driver = driversById[trip.driver_id] || {};
  const vehicle = vehiclesById[trip.vehicle_id] || {};

  return {
    id: trip.trip_id,
    tripId: trip.trip_id,
    tripCode: trip.trip_code,
    organizationId: trip.organization_id,
    vehicleId: trip.vehicle_id,
    vehicle: vehicle.vehicleCode ?? trip.vehicle?.registration_number ?? `Vehicle ${trip.vehicle_id}`,
    driverId: trip.driver_id,
    driver: driverUser.fullName ?? driver.fullName ?? `Driver ${trip.driver_id}`,
    source: trip.source,
    destination: trip.destination,
    cargoWeight: trip.cargo_weight,
    plannedDistance: trip.planned_distance,
    actualDistance: trip.actual_distance,
    startTime: trip.start_time,
    endTime: trip.end_time,
    tripStatus: trip.trip_status,
    createdBy: trip.created_by,
    updatedBy: trip.updated_by,
    createdAt: trip.created_at,
    updatedAt: trip.updated_at,
  };
}

export function serializeTrip(values, organizationId) {
  return {
    organization_id: organizationId,
    vehicle_id: Number(values.vehicleId),
    driver_id: Number(values.driverId),
    trip_code: values.tripCode || null,
    source: values.source,
    destination: values.destination,
    cargo_weight: values.cargoWeight === '' || values.cargoWeight == null ? undefined : Number(values.cargoWeight),
    planned_distance: values.plannedDistance === '' || values.plannedDistance == null ? undefined : Number(values.plannedDistance),
  };
}

export function serializeTripUpdate(values) {
  return {
    vehicle_id: values.vehicleId ? Number(values.vehicleId) : undefined,
    driver_id: values.driverId ? Number(values.driverId) : undefined,
    source: values.source || undefined,
    destination: values.destination || undefined,
    cargo_weight: values.cargoWeight === '' || values.cargoWeight == null ? undefined : Number(values.cargoWeight),
    planned_distance: values.plannedDistance === '' || values.plannedDistance == null ? undefined : Number(values.plannedDistance),
    actual_distance: values.actualDistance === '' || values.actualDistance == null ? undefined : Number(values.actualDistance),
    start_time: values.startTime || undefined,
    end_time: values.endTime || undefined,
    trip_status: values.tripStatus || undefined,
  };
}

export function normalizeDashboardSummary(summary) {
  return {
    kpis: [
      { label: 'Active Trips', value: summary.active_trips, trend: 'In progress' },
      { label: 'Trips Today', value: summary.completed_trips_today, trend: 'Completed today' },
      { label: 'Planned Trips', value: summary.planned_trips, trend: 'Awaiting dispatch' },
      { label: 'Delayed Trips', value: summary.delayed_trips, trend: 'Running late' },
      { label: 'Total Vehicles', value: summary.total_vehicles, trend: 'Fleet size' },
      { label: 'Available Drivers', value: summary.available_drivers, trend: 'Ready to assign' },
    ],
    vehicleStatus: summary.vehicle_status_breakdown.map((item) => ({
      label: item.status,
      value: item.count,
    })),
    tripStatus: summary.trip_status_breakdown.map((item) => ({
      label: item.status,
      value: item.count,
    })),
    driverStatus: summary.driver_status_breakdown.map((item) => ({
      label: item.status,
      value: item.count,
    })),
    fleetUtilization: summary.fleet_utilization,
    alerts: summary.alerts || [],
  };
}