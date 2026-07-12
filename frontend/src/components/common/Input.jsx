export default function Input({ label, error, className = '', id, type = 'text', as = 'input', ...props }) {
  const Component = as;

  return (
    <label className={`flex flex-col gap-1.5 ${className}`} htmlFor={id}>
      {label ? <span className="text-sm font-medium text-slate-200">{label}</span> : null}
      <Component
        id={id}
        type={type}
        className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-brand-400 focus:bg-white/10"
        {...props}
      />
      {error ? <span className="text-xs text-rose-300">{error}</span> : null}
    </label>
  );
}