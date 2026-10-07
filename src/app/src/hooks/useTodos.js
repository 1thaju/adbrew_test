import { useCallback, useEffect, useState } from 'react';
import { createTodo, fetchTodos } from '../api/todos';

export function useTodos() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const results = await fetchTodos();
      setTodos(results);
      return true;
    } catch (requestError) {
      setError(requestError.message || 'Unable to load todos.');
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const addTodo = useCallback(async (description) => {
    setSubmitting(true);
    setError('');

    try {
      await createTodo(description);
      await refresh();
      return true;
    } catch (requestError) {
      setError(requestError.message || 'Unable to create todo.');
      return false;
    } finally {
      setSubmitting(false);
    }
  }, [refresh]);

  return { todos, loading, error, submitting, addTodo, refresh };
}
