export default function StatusBadge({ status }) {
  const styles = {
    active: 'bg-emerald-500/15 text-emerald-400',
    pending: 'bg-amber-500/15 text-amber-400',
    inactive: 'bg-rose-500/15 text-rose-400',
  };

  return <span className={`rounded-full px-3 py-1 text-xs font-medium ${styles[status] || styles.pending}`}>{status}</span>;
}
