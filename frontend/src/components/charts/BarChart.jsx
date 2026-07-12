export default function BarChart({ title, series = [], labels = [] }) {
  const max = Math.max(...series, 1);

  return (
    <div className="surface-panel p-5">
      <div className="flex items-center justify-between gap-4">
        <h3 className="text-base font-semibold text-white">{title}</h3>
      </div>
      <div className="mt-6 flex h-64 items-end gap-3">
        {series.map((value, index) => (
          <div key={`${title}-${index}`} className="flex flex-1 flex-col items-center gap-3">
            <div className="flex w-full items-end justify-center rounded-t-2xl bg-white/5 px-2 py-2">
              <div className="w-full rounded-t-2xl bg-gradient-to-t from-brand-700 to-brand-400" style={{ height: `${(value / max) * 100}%`, minHeight: 12 }} />
            </div>
            <div className="text-xs text-slate-400">{labels[index] || index + 1}</div>
          </div>
        ))}
      </div>
    </div>
  );
}