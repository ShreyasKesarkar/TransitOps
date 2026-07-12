const stats = [
  { label: 'Active Vehicles', value: '128', change: '+6.2%' },
  { label: 'On-time Trips', value: '94.8%', change: '+2.1%' },
  { label: 'Open Maintenance', value: '14', change: '-3' },
  { label: 'Fuel Cost', value: '$18.4k', change: '+1.4%' },
];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((item) => (
          <div key={item.label} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5">
            <p className="text-sm text-slate-400">{item.label}</p>
            <div className="mt-3 flex items-end justify-between">
              <h3 className="text-3xl font-semibold">{item.value}</h3>
              <span className="text-sm text-emerald-400">{item.change}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[2fr_1fr]">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
          <h3 className="mb-4 text-lg font-semibold">Operations Snapshot</h3>
          <div className="h-56 rounded-xl bg-gradient-to-br from-brand-600/20 to-slate-800 p-6">
            <p className="text-sm text-slate-400">Charts and analytics will integrate with FastAPI endpoints.</p>
          </div>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6">
          <h3 className="mb-4 text-lg font-semibold">Recent Alerts</h3>
          <ul className="space-y-3 text-sm text-slate-300">
            <li className="rounded-lg bg-slate-800/70 p-3">Vehicle V-104 requires inspection.</li>
            <li className="rounded-lg bg-slate-800/70 p-3">Fuel threshold exceeded for Route 12.</li>
            <li className="rounded-lg bg-slate-800/70 p-3">2 new driver assignments pending.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
