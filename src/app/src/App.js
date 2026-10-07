import './App.css';
import { TodoForm } from './components/TodoForm';
import { TodoList } from './components/TodoList';
import { useTodos } from './hooks/useTodos';

export function App() {
  const { todos, loading, error, submitting, addTodo } = useTodos();

  return (
    <div className="App">
      <main className="todo-app">
        <h1>To-dos</h1>
        <TodoForm
          submitting={submitting}
          error={error}
          onAddTodo={addTodo}
        />
        <section aria-labelledby="todo-list-heading">
          <h2 id="todo-list-heading">Your list</h2>
          <TodoList todos={todos} loading={loading} error={error} />
        </section>
      </main>
    </div>
  );
}

export default App;
