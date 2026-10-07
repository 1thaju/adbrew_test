import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import App from './App';

function jsonResponse(body, ok = true, status = 200) {
  return {
    ok,
    status,
    json: async () => body,
  };
}

test('loads todos and refreshes the list after adding one', async () => {
  global.fetch = jest.fn()
    .mockResolvedValueOnce(jsonResponse([
      { id: '1', description: 'Learn Docker' },
    ]))
    .mockResolvedValueOnce(jsonResponse(
      { id: '2', description: 'Learn React' },
      true,
      201
    ))
    .mockResolvedValueOnce(jsonResponse([
      { id: '2', description: 'Learn React' },
      { id: '1', description: 'Learn Docker' },
    ]));

  render(<App />);

  expect(await screen.findByText('Learn Docker')).toBeInTheDocument();

  fireEvent.change(screen.getByLabelText('To-do description'), {
    target: { value: 'Learn React' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Add to-do' }));

  expect(await screen.findByText('Learn React')).toBeInTheDocument();
  await waitFor(() => {
    expect(global.fetch).toHaveBeenCalledTimes(3);
  });
  expect(global.fetch.mock.calls[1][1].method).toBe('POST');
});
