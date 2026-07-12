import { Outlet } from 'react-router-dom';

export default function AuthLayout() {
  return (
    <div className="min-h-screen px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto flex min-h-[calc(100vh-5rem)] w-full max-w-7xl items-center justify-center">
        <div className="grid w-full overflow-hidden rounded-[2rem] border border-white/10 bg-white/5 shadow-panel backdrop-blur-xl lg:grid-cols-[1.1fr_0.9fr]">
          <div className="hidden border-r border-white/10 p-10 lg:block">
            <div className="flex h-full flex-col justify-between rounded-[1.6rem] bg-gradient-to-br from-brand-700/45 via-brand-600/20 to-transparent p-8">
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-brand-200">TransitOps</p>
                <h1 className="mt-4 max-w-xl text-5xl font-semibold leading-tight text-white">
                  Smart transport operations built for enterprise fleets.
                </h1>
                <p className="mt-5 max-w-lg text-sm leading-6 text-slate-300">
                  Manage vehicles, drivers, trips, maintenance, fuel, and expenses from a single ERP-grade control center.
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3 text-sm text-slate-200">
                <div className="rounded-2xl border border-white/10 bg-white/10 p-4">Fleet control</div>
                <div className="rounded-2xl border border-white/10 bg-white/10 p-4">Audit ready</div>
                <div className="rounded-2xl border border-white/10 bg-white/10 p-4">FastAPI ready</div>
              </div>
            </div>
          </div>
          <div className="p-6 sm:p-10">
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
}