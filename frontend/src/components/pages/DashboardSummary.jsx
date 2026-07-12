import Card from '../common/Card';
import Table from '../common/Table';
import StatusBadge from '../common/StatusBadge';

export default function DashboardSummary({ summary }) {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {summary.kpis.map((item) => (
          <Card key={item.label} title={item.label} value={item.value} helper={item.trend} />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.5fr_0.9fr]">
        <div className="surface-panel overflow-hidden">
          <div className="border-b border-white/10 p-5">
            <h3 className="text-lg font-semibold text-white">Recent Trips</h3>
          </div>
          <Table
            columns={[
              { key: 'tripCode', label: 'Trip Code' },
              { key: 'source', label: 'Source' },
              { key: 'destination', label: 'Destination' },
              { key: 'vehicle', label: 'Vehicle' },
              { key: 'driver', label: 'Driver' },
              { key: 'status', label: 'Status', render: (value) => <StatusBadge status={value} /> },
            ]}
            data={summary.recentTrips}
          />
        </div>

        <div className="surface-panel p-5">
          <h3 className="text-lg font-semibold text-white">Vehicle Status</h3>
          <div className="mt-6 space-y-3">
            {summary.vehicleStatus.map((item) => (
              <div key={item.label} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
                <div className="flex items-center justify-between gap-4 text-sm text-slate-200">
                  <span>{item.label}</span>
                  <span>{item.value}</span>
                </div>
                <div className="mt-3 h-2 rounded-full bg-white/10">
                  <div className="h-2 rounded-full bg-brand-500" style={{ width: `${item.value * 4}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}