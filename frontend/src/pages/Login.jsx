import { useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Input from '../components/common/Input';
import Button from '../components/common/Button';

export default function Login() {
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState('admin@transitops.com');
  const [password, setPassword] = useState('Password123!');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login({ email, password });
      navigate(location.state?.from?.pathname || '/dashboard', { replace: true });
    } catch {
      setError('Unable to sign in. Check your credentials and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm uppercase tracking-[0.3em] text-brand-200">Authentication</p>
        <h2 className="mt-3 text-3xl font-semibold text-white">Sign in to TransitOps</h2>
        <p className="mt-2 text-sm text-slate-300">Use your enterprise credentials to access fleet operations.</p>
      </div>

      <form className="space-y-5" onSubmit={handleSubmit}>
        <Input label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="name@company.com" />
        <Input label="Password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Enter password" />
        {error ? <p className="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">{error}</p> : null}
        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Signing in...' : 'Login'}
        </Button>
      </form>

      <div className="mt-6 flex items-center justify-between text-sm text-slate-400">
        <Link to="/forgot-password" className="transition hover:text-white">
          Forgot password?
        </Link>
        <Link to="/change-password" className="transition hover:text-white">
          Change password
        </Link>
      </div>
    </div>
  );
}