import { useState } from 'react';
import { Link } from 'react-router-dom';
import { changePassword } from '../services/authService';
import Input from '../components/common/Input';
import Button from '../components/common/Button';

export default function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await changePassword({ currentPassword, newPassword, confirmPassword });
    setMessage(response.message);
  };

  return (
    <div>
      <h2 className="text-3xl font-semibold text-white">Change password</h2>
      <p className="mt-2 text-sm text-slate-300">Update your password from this secure form.</p>
      <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
        <Input label="Current Password" type="password" value={currentPassword} onChange={(event) => setCurrentPassword(event.target.value)} />
        <Input label="New Password" type="password" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} />
        <Input label="Confirm Password" type="password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} />
        <Button type="submit" className="w-full">
          Update password
        </Button>
      </form>
      {message ? <p className="mt-4 text-sm text-emerald-300">{message}</p> : null}
      <Link to="/login" className="mt-5 inline-block text-sm text-slate-400 transition hover:text-white">
        Back to login
      </Link>
    </div>
  );
}