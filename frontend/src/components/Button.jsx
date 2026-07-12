export default function Button({ children, className = '', ...props }) {
  return (
    <button
      className={`rounded-xl bg-brand-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-brand-700 ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
