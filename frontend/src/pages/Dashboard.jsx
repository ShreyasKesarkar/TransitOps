import { useEffect, useState } from 'react';
import DashboardSummary from '../components/pages/DashboardSummary';
import BarChart from '../components/charts/BarChart';
import DonutChart from '../components/charts/DonutChart';
import Loader from '../components/common/Loader';
import { fetchDashboardSummary } from '../services/dashboardService';

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
        <BarChart title="Trip Status" series={summary.tripStatus.map((item) => item.value)} labels={summary.tripStatus.map((item) => item.label)} />
        <DonutChart title="Vehicle Status" data={summary.vehicleStatus} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <DonutChart title="Driver Status" data={summary.driverStatus} />
        <div className="surface-panel p-5">
          <h3 className="text-lg font-semibold text-white">Alerts</h3>
          <div className="mt-4 space-y-3">
            {summary.alerts.length ? summary.alerts.map((alert) => (
              <div key={alert} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
                {alert}
              </div>
            )) : (
              <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
                No active alerts.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}