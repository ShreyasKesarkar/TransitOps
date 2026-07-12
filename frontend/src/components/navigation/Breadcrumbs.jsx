import { Link, useLocation } from 'react-router-dom';

export default function Breadcrumbs() {
  const location = useLocation();
  const segments = location.pathname.split('/').filter(Boolean);

  if (!segments.length) {
    return null;
  }

  return (
    <nav className="mb-4 text-sm text-slate-400">
      <ol className="flex flex-wrap items-center gap-2">
        <li>
          <Link to="/dashboard" className="transition hover:text-white">
            Home
          </Link>
        </li>
        {segments.map((segment, index) => {
          const path = `/${segments.slice(0, index + 1).join('/')}`;
          const label = segment.replace('-', ' ');

          return (
            <li key={path} className="flex items-center gap-2">
              <span>/</span>
              <Link to={path} className={index === segments.length - 1 ? 'capitalize text-white' : 'capitalize transition hover:text-white'}>
                {label}
              </Link>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}