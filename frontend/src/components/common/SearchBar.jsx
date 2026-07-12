import { Search } from 'lucide-react';

export default function SearchBar({ value, onChange, placeholder = 'Search...' }) {
  return (
    <label className="flex min-w-0 items-center gap-3 rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-slate-300">
      <Search size={18} className="shrink-0" />
      <input
        value={value}
        onChange={(event) => onChange?.(event.target.value)}
        placeholder={placeholder}
        className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
      />
    </label>
  );
}