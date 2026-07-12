import { X } from 'lucide-react';

export default function Modal({ open, title, children, onClose, size = 'lg' }) {
  if (!open) {
    return null;
  }

  const width = size === 'xl' ? 'max-w-5xl' : size === 'md' ? 'max-w-2xl' : 'max-w-3xl';

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-slate-950/70 px-4 py-8 backdrop-blur-sm">
      <div className={`surface-panel w-full ${width} max-h-[90vh] overflow-y-auto`}>
        <div className="flex items-center justify-between border-b border-white/10 px-6 py-4">
          <h3 className="text-lg font-semibold text-white">{title}</h3>
          <button type="button" className="rounded-full p-2 text-slate-400 transition hover:bg-white/10 hover:text-white" onClick={onClose}>
            <X size={18} />
          </button>
        </div>
        <div className="p-6">{children}</div>
      </div>
    </div>
  );
}