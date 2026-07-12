export default function DonutChart({ title, data = [] }) {
  const total = data.reduce((sum, item) => sum + item.value, 0) || 1;

  return (
    <div className="surface-panel p-5">
      <h3 className="text-base font-semibold text-white">{title}</h3>
      <div className="mt-6 grid gap-4 sm:grid-cols-[220px_1fr] sm:items-center">
        <div className="mx-auto flex h-56 w-56 items-center justify-center rounded-full border border-white/10 bg-[radial-gradient(circle,_rgba(47,110,255,0.35)_0%,_rgba(47,110,255,0.15)_38%,_transparent_39%)]">
          <div className="text-center">
            <p className="text-3xl font-semibold text-white">{total}</p>
            <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Total</p>
          </div>
        </div>
        <div className="space-y-3">
          {data.map((item) => (
            <div key={item.label} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <div className="flex items-center justify-between gap-4 text-sm text-slate-200">
                <span>{item.label}</span>
                <span>{item.value}</span>
              </div>
              <div className="mt-3 h-2 rounded-full bg-white/10">
                <div className="h-2 rounded-full bg-brand-500" style={{ width: `${(item.value / total) * 100}%` }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}