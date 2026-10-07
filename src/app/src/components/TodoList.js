export function TodoList({ todos, loading, error }) {
  if (loading) {
    return <p role="status">Loading to-dos…</p>;
  }

  if (error) {
    return <p className="todo-error" role="alert">{error}</p>;
  }

  if (todos.length === 0) {
    return <p>No to-dos yet. Add one above.</p>;
  }

  return (
    <ul className="todo-list">
      {todos.map((todo) => (
        <li key={todo.id}>{todo.description}</li>
      ))}
    </ul>
  );
}
