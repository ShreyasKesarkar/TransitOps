export default function Select({ label, error, className = '', id, options = [], ...props }) {
  return (
    <label className={`flex flex-col gap-1.5 ${className}`} htmlFor={id}>
      {label ? <span className="text-sm font-medium text-slate-200">{label}</span> : null}
      <select
        id={id}
        className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none transition focus:border-brand-400 focus:bg-white/10"
        {...props}
      >
        <option value="">Select...</option>
        {options.map((option) => (
          <option key={option.value} value={option.value} className="bg-surface text-white">
            {option.label}
          </option>
        ))}
      </select>
      {error ? <span className="text-xs text-rose-300">{error}</span> : null}
    </label>
  );
}