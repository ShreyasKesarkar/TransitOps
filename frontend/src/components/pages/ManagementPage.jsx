import { useEffect, useMemo, useState } from 'react';
import { Plus, PenSquare, Trash2, Filter } from 'lucide-react';
import Button from '../common/Button';
import Card from '../common/Card';
import ConfirmationDialog from '../common/ConfirmationDialog';
import EmptyState from '../common/EmptyState';
import Loader from '../common/Loader';
import Pagination from '../common/Pagination';
import SearchBar from '../common/SearchBar';
import StatusBadge from '../common/StatusBadge';
import Table from '../common/Table';
import EntityFormModal from '../forms/EntityFormModal';
import { useToast } from '../../context/ToastContext';

const defaultPageSize = 8;

function filterBySearch(rows, query, searchableKeys) {
  const normalized = query.trim().toLowerCase();
  if (!normalized) {
    return rows;
  }

  return rows.filter((row) => searchableKeys.some((key) => String(row[key] ?? '').toLowerCase().includes(normalized)));
}

export default function ManagementPage({ config }) {
  const { title, description, service, columns, fields, createLabel, searchPlaceholder, summaryCards = [], searchableKeys = [] } = config;
  const { pushToast } = useToast();
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  const reload = async () => {
    setLoading(true);
    const response = await service.list();
    const items = Array.isArray(response) ? response : response.items || [];
    setRecords(items);
    setLoading(false);
  };

  useEffect(() => {
    reload();
  }, []);

  const filteredRecords = useMemo(() => filterBySearch(records, search, searchableKeys.length ? searchableKeys : columns.map((column) => column.key)), [columns, records, searchableKeys, search]);
  const totalPages = Math.max(1, Math.ceil(filteredRecords.length / defaultPageSize));
  const paginatedRecords = filteredRecords.slice((page - 1) * defaultPageSize, page * defaultPageSize);

  const openCreate = () => {
    setSelected(null);
    setModalOpen(true);
  };

  const openEdit = (record) => {
    setSelected(record);
    setModalOpen(true);
  };

  const closeModal = () => {
    setSelected(null);
    setModalOpen(false);
  };

  const handleSubmit = async (values) => {
    const payload = { ...values };
    if (selected) {
      await service.update(selected.id, payload);
      pushToast({ type: 'success', title: `${title} updated`, message: `${title} record saved successfully.` });
    } else {
      await service.create(payload);
      pushToast({ type: 'success', title: `${title} created`, message: `${title} record added successfully.` });
    }
    closeModal();
    await reload();
  };

  const handleDelete = async () => {
    if (!confirmDelete) {
      return;
    }
    await service.remove(confirmDelete.id);
    pushToast({ type: 'info', title: `${title} removed`, message: `${confirmDelete[columns[0].key] || 'Record'} was deleted.` });
    setConfirmDelete(null);
    await reload();
  };

  const actionRenderer = (row) => (
    <div className="flex items-center gap-2">
      <Button variant="secondary" onClick={() => openEdit(row)}>
        <PenSquare size={16} />
        Edit
      </Button>
      <Button variant="danger" onClick={() => setConfirmDelete(row)}>
        <Trash2 size={16} />
        Delete
      </Button>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h1 className="text-3xl font-semibold text-white">{title}</h1>
          <p className="mt-2 max-w-3xl text-sm text-slate-300">{description}</p>
        </div>
        <Button onClick={openCreate}>
          <Plus size={18} />
          {createLabel || `Add ${title}`}
        </Button>
      </div>

      {summaryCards.length ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {summaryCards.map((card) => (
            <Card key={card.title} {...card} />
          ))}
        </div>
      ) : null}

      <div className="surface-panel overflow-hidden">
        <div className="flex flex-col gap-4 border-b border-white/10 p-5 lg:flex-row lg:items-center lg:justify-between">
          <SearchBar value={search} onChange={(value) => { setSearch(value); setPage(1); }} placeholder={searchPlaceholder || `Search ${title.toLowerCase()}...`} />
          <Button variant="secondary">
            <Filter size={16} />
            Filters
          </Button>
        </div>

        {loading ? (
          <Loader />
        ) : paginatedRecords.length ? (
          <Table
            columns={columns.map((column) => ({
              ...column,
              render: column.render || ((value) => (column.key.toLowerCase().includes('status') || column.key.toLowerCase().includes('priority') ? <StatusBadge status={value} /> : value)),
            }))}
            data={paginatedRecords}
            actions={actionRenderer}
          />
        ) : (
          <EmptyState title={`No ${title.toLowerCase()} found`} description={`Use the add button to create your first ${title.toLowerCase()}.`} actionLabel={`Add ${title}`} onAction={openCreate} />
        )}

        <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
      </div>

      <EntityFormModal
        open={modalOpen}
        title={selected ? `Edit ${title}` : `Create ${title}`}
        fields={fields}
        initialValues={selected || {}}
        onCancel={closeModal}
        onSubmit={handleSubmit}
        submitLabel={selected ? 'Update record' : 'Save record'}
      />

      <ConfirmationDialog
        open={Boolean(confirmDelete)}
        title={`Delete ${title}`}
        description={`This will permanently remove the selected ${title.toLowerCase()} from the mock layer or backend endpoint.`}
        confirmLabel="Delete"
        onCancel={() => setConfirmDelete(null)}
        onConfirm={handleDelete}
      />
    </div>
  );
}