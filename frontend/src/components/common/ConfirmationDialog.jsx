import Button from './Button';
import Modal from './Modal';

export default function ConfirmationDialog({ open, title, description, confirmLabel = 'Confirm', onCancel, onConfirm }) {
  return (
    <Modal open={open} title={title} onClose={onCancel} size="md">
      <p className="text-sm text-slate-300">{description}</p>
      <div className="mt-6 flex items-center justify-end gap-3">
        <Button variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
        <Button variant="danger" onClick={onConfirm}>
          {confirmLabel}
        </Button>
      </div>
    </Modal>
  );
}