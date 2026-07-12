import Button from '../components/common/Button';
import Input from '../components/common/Input';
import Select from '../components/common/Select';

export default function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-white">Settings</h1>
        <p className="mt-2 text-sm text-slate-300">Organization profile, user profile, theme, and permissions.</p>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="surface-panel p-6">
          <h2 className="text-lg font-semibold text-white">User Profile</h2>
          <div className="mt-5 grid gap-4">
            <Input label="Full Name" placeholder="Enter full name" />
            <Input label="Email" type="email" placeholder="name@company.com" />
            <Select label="Theme" options={[{ label: 'Dark', value: 'dark' }, { label: 'Light', value: 'light' }]} />
            <Button className="w-fit">Save profile</Button>
          </div>
        </div>

        <div className="surface-panel p-6">
          <h2 className="text-lg font-semibold text-white">Role Permissions</h2>
          <p className="mt-2 text-sm text-slate-300">Permissions UI is scaffolded for later backend-driven control.</p>
          <div className="mt-5 grid gap-3 text-sm text-slate-200">
            <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">Admin - Full access</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">Fleet Manager - Operations access</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">Driver - Trip visibility only</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">Safety Officer - Maintenance and safety</div>
            <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">Financial Analyst - Expenses and analytics</div>
          </div>
        </div>
      </div>
    </div>
  );
}