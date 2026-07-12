export default function Card({ title, value, helper, icon, className = '' }) {
  return (
    <div className={`surface-panel p-5 ${className}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm text-slate-400">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-white">{value}</p>
          {helper ? <p className="mt-2 text-sm text-slate-300">{helper}</p> : null}
        </div>
        {icon ? <div className="rounded-2xl bg-brand-500/20 p-3 text-brand-200">{icon}</div> : null}
      </div>
    </div>
  );
}