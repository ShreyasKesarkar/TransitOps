import { useState } from 'react';
import { Link } from 'react-router-dom';
import { requestPasswordReset } from '../services/authService';
import Input from '../components/common/Input';
import Button from '../components/common/Button';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await requestPasswordReset({ email });
    setMessage(response.message);
  };

  return (
    <div>
      <h2 className="text-3xl font-semibold text-white">Forgot password</h2>
      <p className="mt-2 text-sm text-slate-300">Send a reset link to the registered email address.</p>
      <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
        <Input label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="name@company.com" />
        <Button type="submit" className="w-full">
          Send reset link
        </Button>
      </form>
      {message ? <p className="mt-4 text-sm text-emerald-300">{message}</p> : null}
      <Link to="/login" className="mt-5 inline-block text-sm text-slate-400 transition hover:text-white">
        Back to login
      </Link>
    </div>
  );
}