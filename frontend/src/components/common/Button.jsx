const variants = {
  primary: 'bg-brand-500 text-white hover:bg-brand-400',
  secondary: 'bg-white/10 text-slate-100 hover:bg-white/15',
  ghost: 'bg-transparent text-slate-200 hover:bg-white/10',
  danger: 'bg-rose-500 text-white hover:bg-rose-400',
};

export default function Button({ children, className = '', variant = 'primary', type = 'button', ...props }) {
  return (
    <button
      type={type}
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-brand-400 focus:ring-offset-2 focus:ring-offset-surface disabled:cursor-not-allowed disabled:opacity-60 ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}