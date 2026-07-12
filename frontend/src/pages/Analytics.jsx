import BarChart from '../components/charts/BarChart';
import DonutChart from '../components/charts/DonutChart';
import { analytics } from '../data/mockData';

export default function Analytics() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-white">Analytics</h1>
        <p className="mt-2 text-sm text-slate-300">Operational analytics across fuel, trips, expenses, and utilization.</p>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <BarChart title="Fuel Cost" series={analytics.fuelCost} labels={['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']} />
        <BarChart title="Trip Count" series={analytics.tripCount} labels={['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']} />
        <DonutChart title="Vehicle Utilization" data={analytics.vehicleUtilization} />
        <DonutChart title="Driver Performance" data={analytics.driverPerformance} />
      </div>
    </div>
  );
}