import { useMemo, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Building2, CarFront, ChevronLeft, CircleGauge, Fuel, LayoutDashboard, LogOut, Menu, Settings, ShieldAlert, Users, Wrench, Route } from 'lucide-react';
import Button from '../common/Button';
import { useAuth } from '../../context/AuthContext';

const navItems = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Users', path: '/users', icon: Users },
  { label: 'Fleet', path: '/vehicles', icon: CarFront },
  { label: 'Drivers', path: '/drivers', icon: Users },
  { label: 'Trips', path: '/trips', icon: Route },
  { label: 'Maintenance', path: '/maintenance', icon: Wrench },
  { label: 'Fuel & Expenses', path: '/fuel-logs', icon: Fuel },
  { label: 'Analytics', path: '/analytics', icon: CircleGauge },
  { label: 'Settings', path: '/settings', icon: Settings },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const { user, logout } = useAuth();

  const filteredItems = useMemo(() => navItems, []);

  return (
    <aside className={`border-r border-white/10 bg-black/20 backdrop-blur-xl transition-all duration-300 ${collapsed ? 'lg:w-24' : 'lg:w-80'}`}>
      <div className="flex h-full flex-col p-4 lg:p-5">
        <div className="mb-6 flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
          <div className={`flex items-center gap-3 ${collapsed ? 'lg:hidden' : ''}`}>
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-500/20 text-brand-200">
              <Building2 size={20} />
            </div>
            <div>
              <p className="font-semibold text-white">TransitOps</p>
              <p className="text-xs text-slate-400">Smart Transport ERP</p>
            </div>
          </div>
          <Button variant="ghost" className="hidden lg:inline-flex" onClick={() => setCollapsed((value) => !value)}>
            {collapsed ? <Menu size={18} /> : <ChevronLeft size={18} />}
          </Button>
        </div>

        <nav className="flex-1 space-y-2">
          {filteredItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition ${isActive ? 'bg-brand-500/20 text-white' : 'text-slate-300 hover:bg-white/5 hover:text-white'}`
                }
              >
                <Icon size={18} className="shrink-0" />
                <span className={collapsed ? 'lg:hidden' : ''}>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="mt-6 rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-500/20 text-brand-200">
              <ShieldAlert size={18} />
            </div>
            <div className={collapsed ? 'lg:hidden' : ''}>
              <p className="text-sm font-semibold text-white">{user?.roleName || 'Role pending'}</p>
              <p className="text-xs text-slate-400">{user?.organizationName || 'Organization pending'}</p>
            </div>
          </div>
        </div>

        <Button variant="secondary" className="mt-4 justify-start" onClick={logout}>
          <LogOut size={18} />
          <span className={collapsed ? 'lg:hidden' : ''}>Logout</span>
        </Button>
      </div>
    </aside>
  );
}