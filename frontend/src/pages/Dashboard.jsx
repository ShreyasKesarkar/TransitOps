import { useEffect, useState } from 'react';
import DashboardSummary from '../components/pages/DashboardSummary';
import BarChart from '../components/charts/BarChart';
import DonutChart from '../components/charts/DonutChart';
import Loader from '../components/common/Loader';
import { fetchDashboardSummary } from '../services/dashboardService';
import { analytics } from '../data/mockData';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    fetchDashboardSummary().then(setSummary);
  }, []);

  if (!summary) {
    return <Loader label="Loading dashboard..." />;
  }

  return (
    <div className="space-y-6">
      <DashboardSummary summary={summary} />

      <div className="grid gap-6 xl:grid-cols-2">
        <BarChart title="Fuel Cost Trend" series={summary.fuelCostSeries} labels={['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']} />
        <DonutChart title="Vehicle Utilization" data={summary.vehicleStatus} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <BarChart title="Trip Count" series={analytics.tripCount} labels={['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']} />
        <BarChart title="Expenses" series={analytics.expenseCount} labels={['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']} />
      </div>
    </div>
  );
}