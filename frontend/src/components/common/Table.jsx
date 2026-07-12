export default function Table({ columns, data, rowKey = 'id', actions }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-white/10">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-white/10">
          <thead className="bg-white/5 text-left text-xs uppercase tracking-[0.2em] text-slate-400">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="px-5 py-4 font-medium">
                  {column.label}
                </th>
              ))}
              {actions ? <th className="px-5 py-4 font-medium">Actions</th> : null}
            </tr>
          </thead>
          <tbody className="divide-y divide-white/10 bg-white/5 text-sm text-slate-200">
            {data.map((row) => (
              <tr key={row[rowKey]} className="transition hover:bg-white/5">
                {columns.map((column) => (
                  <td key={column.key} className="px-5 py-4 align-top">
                    {column.render ? column.render(row[column.key], row) : row[column.key]}
                  </td>
                ))}
                {actions ? <td className="px-5 py-4">{actions(row)}</td> : null}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}