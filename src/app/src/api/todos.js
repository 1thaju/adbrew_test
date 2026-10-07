const API_BASE_URL = (
  process.env.REACT_APP_API_URL || 'http://localhost:8000'
).replace(/\/+$/, '');

async function getErrorMessage(response) {
  try {
    const body = await response.json();
    if (body && typeof body.error === 'string') {
      return body.error;
    }
  } catch (error) {
    // Fall back to the HTTP status when the response body is not JSON.
  }

  return `Request failed with status ${response.status}.`;
}

async function requestJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }
  return response.json();
}

export function fetchTodos() {
  return requestJson(`${API_BASE_URL}/todos`, {
    headers: { Accept: 'application/json' },
  });
}

export function createTodo(description) {
  return requestJson(`${API_BASE_URL}/todos`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ description }),
  });
}
