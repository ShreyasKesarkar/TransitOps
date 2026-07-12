const badgeMap = {
  ACTIVE: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  AVAILABLE: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  ON_TRIP: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
  OFF_DUTY: 'bg-slate-500/15 text-slate-300 border-slate-500/30',
  IN_MAINTENANCE: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  PENDING: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  APPROVED: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
  IN_PROGRESS: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
  COMPLETED: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  CANCELLED: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
  REJECTED: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
  HIGH: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
  MEDIUM: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  LOW: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  CRITICAL: 'bg-fuchsia-500/15 text-fuchsia-300 border-fuchsia-500/30',
};

export default function StatusBadge({ status }) {
  const key = String(status || '').toUpperCase();
  const classes = badgeMap[key] || 'bg-white/10 text-slate-200 border-white/15';

  return <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide ${classes}`}>{status}</span>;
}