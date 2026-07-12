import { createContext, useCallback, useContext, useMemo, useState } from 'react';

const ToastContext = createContext(null);

let toastId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const dismiss = useCallback((id) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  const pushToast = useCallback((toast) => {
    const id = ++toastId;
    setToasts((current) => [...current, { id, type: 'info', title: 'Notification', ...toast }]);
    window.setTimeout(() => dismiss(id), toast.duration ?? 3200);
  }, [dismiss]);

  const value = useMemo(() => ({ pushToast, dismiss }), [pushToast, dismiss]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed right-4 top-4 z-50 flex w-full max-w-sm flex-col gap-3">
        {toasts.map((toast) => (
          <div key={toast.id} className="surface-panel border-white/15 px-4 py-3 text-sm text-slate-100">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="font-semibold">{toast.title}</p>
                <p className="mt-1 text-slate-300">{toast.message}</p>
              </div>
              <button type="button" className="text-slate-400 transition hover:text-white" onClick={() => dismiss(toast.id)}>
                ×
              </button>
            </div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
}