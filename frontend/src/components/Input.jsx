export default function Input({ className = '', ...props }) {
  return (
    <input
      className={`w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-100 outline-none focus:border-brand-500 ${className}`}
      {...props}
    />
  );
}
