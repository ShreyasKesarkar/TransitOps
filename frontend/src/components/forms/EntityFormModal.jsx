import { useEffect, useMemo, useState } from 'react';
import Modal from '../common/Modal';
import Input from '../common/Input';
import Select from '../common/Select';
import Button from '../common/Button';

const emptyValue = (field) => {
  if (field.type === 'number') {
    return '';
  }
  return field.defaultValue ?? '';
};

export default function EntityFormModal({ open, title, fields = [], initialValues = {}, onCancel, onSubmit, submitLabel = 'Save changes' }) {
  const initialFormValues = useMemo(() => {
    return fields.reduce((accumulator, field) => {
      accumulator[field.name] = initialValues[field.name] ?? emptyValue(field);
      return accumulator;
    }, {});
  }, [fields, initialValues]);

  const [values, setValues] = useState(initialFormValues);

  useEffect(() => {
    setValues(initialFormValues);
  }, [initialFormValues]);

  const updateValue = (name, value) => {
    setValues((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(values);
  };

  return (
    <Modal open={open} title={title} onClose={onCancel} size="xl">
      <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-2">
        {fields.map((field) => {
          const fieldValue = values[field.name] ?? '';

          if (field.type === 'select') {
            return (
              <Select
                key={field.name}
                label={field.label}
                id={field.name}
                value={fieldValue}
                options={typeof field.options === 'function' ? field.options() : field.options || []}
                onChange={(event) => updateValue(field.name, event.target.value)}
                className={field.span === 2 ? 'md:col-span-2' : ''}
              />
            );
          }

          if (field.type === 'textarea') {
            return (
              <Input
                key={field.name}
                as="textarea"
                label={field.label}
                id={field.name}
                rows={field.rows || 4}
                value={fieldValue}
                onChange={(event) => updateValue(field.name, event.target.value)}
                className={field.span === 2 ? 'md:col-span-2' : ''}
              />
            );
          }

          return (
            <Input
              key={field.name}
              label={field.label}
              id={field.name}
              type={field.type || 'text'}
              value={fieldValue}
              onChange={(event) => updateValue(field.name, field.type === 'number' ? event.target.valueAsNumber || '' : event.target.value)}
              className={field.span === 2 ? 'md:col-span-2' : ''}
            />
          );
        })}

        <div className="md:col-span-2 mt-2 flex items-center justify-end gap-3 border-t border-white/10 pt-4">
          <Button variant="secondary" type="button" onClick={onCancel}>
            Cancel
          </Button>
          <Button type="submit">{submitLabel}</Button>
        </div>
      </form>
    </Modal>
  );
}