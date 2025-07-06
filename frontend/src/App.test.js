import { render, screen } from '@testing-library/react';
import App from './App';

test('renders resume parser title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Resume Parser/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders upload form', () => {
  render(<App />);
  const uploadButton = screen.getByText(/Choose PDF file/i);
  expect(uploadButton).toBeInTheDocument();
});

test('renders parse button', () => {
  render(<App />);
  const parseButton = screen.getByText(/Parse Resume/i);
  expect(parseButton).toBeInTheDocument();
}); 