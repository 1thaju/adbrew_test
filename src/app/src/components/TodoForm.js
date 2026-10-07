import { useState } from 'react';

export function TodoForm({ submitting, error, onAddTodo }) {
  const [description, setDescription] = useState('');

  async function handleSubmit(event) {
    event.preventDefault();
    const created = await onAddTodo(description);
    if (created) {
      setDescription('');
    }
  }

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <label htmlFor="todo-description">To-do description</label>
      <div className="todo-form__controls">
        <input
          id="todo-description"
          type="text"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          maxLength={200}
          required
          disabled={submitting}
        />
        <button type="submit" disabled={submitting}>
          {submitting ? 'Adding…' : 'Add to-do'}
        </button>
      </div>
      {error && <p className="todo-error" role="alert">{error}</p>}
    </form>
  );
}
