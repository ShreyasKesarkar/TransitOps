import { Bell, UserCircle2 } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import Breadcrumbs from './Breadcrumbs';
import SearchBar from '../common/SearchBar';
import Button from '../common/Button';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-30 border-b border-white/10 bg-surface/90 backdrop-blur-xl">
      <div className="page-shell">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex-1">
            <Breadcrumbs />
            <SearchBar placeholder="Search records, vehicles, drivers..." />
          </div>
          <div className="flex items-center justify-between gap-3 lg:justify-end">
            <Button variant="ghost" className="h-12 w-12 rounded-full px-0">
              <Bell size={18} />
            </Button>
            <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-2.5">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-brand-500/20 text-brand-200">
                <UserCircle2 size={20} />
              </div>
              <div>
                <p className="text-sm font-semibold text-white">{user?.fullName}</p>
                <p className="text-xs text-slate-400">
                  {user?.roleName} · {user?.organizationName}
                </p>
              </div>
            </div>
            <Button variant="secondary" onClick={logout}>
              Logout
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}