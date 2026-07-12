import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="surface-panel max-w-xl px-8 py-10 text-center">
        <p className="text-sm uppercase tracking-[0.3em] text-brand-200">404</p>
        <h1 className="mt-4 text-4xl font-semibold text-white">Page not found</h1>
        <p className="mt-3 text-sm text-slate-300">The route you requested does not exist or has been moved.</p>
        <Link to="/dashboard" className="mt-6 inline-flex rounded-xl bg-brand-500 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-400">
          Back to dashboard
        </Link>
      </div>
    </div>
  );
}