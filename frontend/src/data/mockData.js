export const mockAuthUser = {
  id: 1,
  fullName: 'Aanya Verma',
  email: 'admin@transitops.com',
  roleName: 'Admin',
  organizationName: 'TransitOps Logistics',
  avatar: 'AV',
};

export const dashboardSummary = {
  kpis: [
    { label: 'Active Vehicles', value: 48, trend: '+6.2%' },
    { label: 'Active Drivers', value: 26, trend: '+2.4%' },
    { label: 'Trips Today', value: 17, trend: '+11.8%' },
    { label: 'Fuel Cost', value: '$12.8K', trend: '-3.1%' },
    { label: 'Maintenance Pending', value: 8, trend: '+1' },
    { label: 'Total Expenses', value: '$42.4K', trend: '+4.5%' },
  ],
  vehicleStatus: [
    { label: 'Available', value: 20 },
    { label: 'On Trip', value: 15 },
    { label: 'Maintenance', value: 8 },
    { label: 'Retired', value: 5 },
  ],
  fuelCostSeries: [18, 24, 20, 31, 28, 35, 40],
  expenseSeries: [12, 18, 14, 22, 19, 25, 30],
  recentTrips: [
    { id: 1, tripCode: 'TRP-1024', source: 'Lagos Hub', destination: 'Ibadan Depot', vehicle: 'TRK-08', driver: 'John Ade', status: 'IN_PROGRESS' },
    { id: 2, tripCode: 'TRP-1025', source: 'Abuja Yard', destination: 'Kaduna Terminal', vehicle: 'BUS-03', driver: 'Mariam Bello', status: 'PLANNED' },
    { id: 3, tripCode: 'TRP-1026', source: 'Port Harcourt', destination: 'Owerri Center', vehicle: 'VAN-11', driver: 'Ifeanyi Obi', status: 'COMPLETED' },
  ],
};

export const users = [
  { id: 1, employeeCode: 'EMP-001', fullName: 'Aanya Verma', email: 'admin@transitops.com', roleName: 'Admin', employmentStatus: 'ACTIVE' },
  { id: 2, employeeCode: 'EMP-015', fullName: 'Mariam Bello', email: 'mariam@transitops.com', roleName: 'Fleet Manager', employmentStatus: 'ACTIVE' },
  { id: 3, employeeCode: 'EMP-024', fullName: 'John Ade', email: 'john@transitops.com', roleName: 'Driver', employmentStatus: 'ACTIVE' },
];

export const drivers = [
  { id: 1, fullName: 'John Ade', licenseNumber: 'LIC-88451', licenseCategory: 'HMV', licenseExpiry: '2027-06-12', safetyScore: 96, driverStatus: 'AVAILABLE' },
  { id: 2, fullName: 'Ifeanyi Obi', licenseNumber: 'LIC-70214', licenseCategory: 'LMV', licenseExpiry: '2026-11-30', safetyScore: 92, driverStatus: 'ON_TRIP' },
  { id: 3, fullName: 'Mariam Bello', licenseNumber: 'LIC-50922', licenseCategory: 'TRANS', licenseExpiry: '2028-01-15', safetyScore: 98, driverStatus: 'OFF_DUTY' },
];

export const vehicles = [
  { id: 1, vehicleCode: 'TRK-08', registrationNumber: 'LAG-739-TRK', vehicleType: 'Truck', manufacturer: 'Mercedes', model: 'Actros', manufacturingYear: 2022, capacity: '25 Tons', vehicleStatus: 'AVAILABLE' },
  { id: 2, vehicleCode: 'BUS-03', registrationNumber: 'ABJ-221-BUS', vehicleType: 'Bus', manufacturer: 'Toyota', model: 'Coaster', manufacturingYear: 2021, capacity: '30 Seats', vehicleStatus: 'ON_TRIP' },
  { id: 3, vehicleCode: 'VAN-11', registrationNumber: 'PHC-118-VAN', vehicleType: 'Van', manufacturer: 'Ford', model: 'Transit', manufacturingYear: 2023, capacity: '2.5 Tons', vehicleStatus: 'IN_MAINTENANCE' },
];

export const trips = [
  { id: 1, tripCode: 'TRP-1024', vehicle: 'TRK-08', driver: 'John Ade', source: 'Lagos Hub', destination: 'Ibadan Depot', plannedDistance: 128, actualDistance: 72, tripStatus: 'IN_PROGRESS' },
  { id: 2, tripCode: 'TRP-1025', vehicle: 'BUS-03', driver: 'Mariam Bello', source: 'Abuja Yard', destination: 'Kaduna Terminal', plannedDistance: 190, actualDistance: 0, tripStatus: 'PLANNED' },
  { id: 3, tripCode: 'TRP-1026', vehicle: 'VAN-11', driver: 'Ifeanyi Obi', source: 'Port Harcourt', destination: 'Owerri Center', plannedDistance: 102, actualDistance: 102, tripStatus: 'COMPLETED' },
];

export const maintenanceRequests = [
  { id: 1, maintenanceCode: 'MNT-2201', vehicle: 'VAN-11', issueTitle: 'Brake pad wear', priority: 'HIGH', maintenanceStatus: 'PENDING' },
  { id: 2, maintenanceCode: 'MNT-2202', vehicle: 'TRK-08', issueTitle: 'Oil leakage inspection', priority: 'MEDIUM', maintenanceStatus: 'APPROVED' },
];

export const fuelLogs = [
  { id: 1, fuelCode: 'FUEL-9001', trip: 'TRP-1024', vehicle: 'TRK-08', fuelStation: 'NNPC Lagos', fuelType: 'DIESEL', liters: 120, cost: 162000, odometerReading: 44210, fuelDate: '2026-07-12' },
  { id: 2, fuelCode: 'FUEL-9002', trip: 'TRP-1025', vehicle: 'BUS-03', fuelStation: 'Total Abuja', fuelType: 'DIESEL', liters: 85, cost: 106000, odometerReading: 35080, fuelDate: '2026-07-11' },
];

export const expenses = [
  { id: 1, expenseCode: 'EXP-3001', expenseType: 'Fuel', trip: 'TRP-1024', vehicle: 'TRK-08', amount: 162000, description: 'Trip refuel' },
  { id: 2, expenseCode: 'EXP-3002', expenseType: 'Toll', trip: 'TRP-1026', vehicle: 'VAN-11', amount: 4800, description: 'Expressway toll' },
];

export const analytics = {
  fuelCost: [15, 21, 18, 27, 24, 32, 29],
  tripCount: [10, 12, 16, 14, 18, 22, 21],
  expenseCount: [8, 11, 10, 13, 15, 16, 19],
  vehicleUtilization: [
    { label: 'Truck', value: 44 },
    { label: 'Bus', value: 32 },
    { label: 'Van', value: 24 },
  ],
  driverPerformance: [
    { label: 'John Ade', value: 96 },
    { label: 'Mariam Bello', value: 93 },
    { label: 'Ifeanyi Obi', value: 88 },
  ],
};