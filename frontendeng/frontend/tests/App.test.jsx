import React from 'react';
import { render, screen, fireEvent, within } from '@testing-library/react';
import { vi } from 'vitest';
import App from './App';

vi.mock('./components/Main', () => {
  const MockMain = () =>
    React.createElement('div', { 'data-testid': 'main' }, 'Main Scene');
  return { __esModule: true, default: MockMain };
});

vi.mock('./components/CosmicFrame', () => {
  const MockCosmic = () =>
    React.createElement('div', { 'data-testid': 'cosmic' }, 'Cosmic Frame');
  return { __esModule: true, default: MockCosmic };
});

const renderHome = () => {
  window.history.pushState({}, '', '/');
  return render(<App />);
};
const renderCosmic = () => {
  window.history.pushState({}, '', '/cosmic');
  return render(<App />);
};

beforeEach(() => {
  window.alert = vi.fn();
  window.history.pushState({}, '', '/');
});

// 1. if the buttons on the home screen load 
test('Home shows primary actions (LOGIN, SIGN UP, EXPLORE)', () => {
  renderHome();

  // normal: exact
  expect(screen.getByRole('button', { name: 'LOGIN' })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'SIGN UP' })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'EXPLORE' })).toBeInTheDocument();

  // edge: ignore capitals and lowercases
  expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /sign\s*up/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /explore/i })).toBeInTheDocument();
});

// 2. if buttons work and EXPLORE brings to next page
test('Primary buttons are enabled and clickable', () => {
  renderHome();

  // normal/edge: LOGIN + SIGN UP
  for (const label of ['LOGIN', 'SIGN UP']) {
    const btn = screen.getByRole('button', { name: label });
    expect(btn).toBeEnabled();
    fireEvent.click(btn);
    expect(window.alert).toHaveBeenCalled(); 
    expect(screen.getByRole('button', { name: label })).toBeInTheDocument();
    window.alert.mockClear();
  }

  // negative/edge: EXPLORE -> /cosmic, button disappears
  const explore = screen.getByRole('button', { name: 'EXPLORE' });
  expect(explore).toBeEnabled();
  fireEvent.click(explore);
  expect(screen.getByTestId('cosmic')).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'EXPLORE' })).toBeNull();
});

// 3. LOGIN and SIGN UP worked, but not EXPLORE. 
test('LOGIN and SIGN UP worked, but not EXPLORE', () => {
  renderHome();

  fireEvent.click(screen.getByRole('button', { name: 'LOGIN' }));
  expect(window.alert).toHaveBeenCalledWith('You clicked login!');

  fireEvent.click(screen.getByRole('button', { name: 'SIGN UP' }));
  expect(window.alert).toHaveBeenCalledWith('You clicked signup!');

  window.alert.mockClear();
  fireEvent.click(screen.getByRole('button', { name: 'EXPLORE' }));
  expect(window.alert).not.toHaveBeenCalled();
});

// 4. EXPLORE -> /cosmic and shows CosmicFrame 
test('EXPLORE -> /cosmic and shows CosmicFrame', () => {
  renderHome();
  fireEvent.click(screen.getByRole('button', { name: 'EXPLORE' }));
  expect(screen.getByTestId('cosmic')).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'LOGIN' })).not.toBeInTheDocument();
  expect(screen.queryByTestId('main')).not.toBeInTheDocument();
});

// 5. DL of /cosmic renders CosmicFrame with routing
test('DL of /cosmic renders CosmicFrame with routing', () => {
  renderCosmic();
  expect(screen.getByTestId('cosmic')).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: 'LOGIN' })).not.toBeInTheDocument();
  expect(screen.queryByTestId('main')).not.toBeInTheDocument();
});

// 6. Main scene and overlay for render 
test('Main scene and overlay for render', () => {
  renderHome();

  const main = screen.getByTestId('main');
  expect(main).toBeInTheDocument();

  const allButtons = screen.getAllByRole('button');
  expect(allButtons).toHaveLength(3);

  expect(within(main).queryByRole('button')).toBeNull();
});

// 7. keys are working 
test('keys are working', () => {
  renderHome();

  const login = screen.getByRole('button', { name: 'LOGIN' });
  login.focus();
  expect(login).toHaveFocus();
  fireEvent.keyDown(login, { key: 'Enter' });
  fireEvent.click(login); 
  expect(window.alert).toHaveBeenCalledWith('You clicked login!');
  window.alert.mockClear();

  const signup = screen.getByRole('button', { name: 'SIGN UP' });
  signup.focus();
  fireEvent.keyDown(signup, { key: ' ' });
  fireEvent.click(signup);
  expect(window.alert).toHaveBeenCalledWith('You clicked signup!');
  window.alert.mockClear();

  const explore = screen.getByRole('button', { name: 'EXPLORE' });
  explore.focus();
  fireEvent.keyDown(explore, { key: 'Enter' });
  fireEvent.click(explore);
  expect(window.alert).not.toHaveBeenCalled();
  expect(screen.getByTestId('cosmic')).toBeInTheDocument();
});

// 8. all 3 buttons work and are named correctly */
test('all 3 buttons work and are named correctly', () => {
  renderHome();
  const btns = screen.getAllByRole('button');
  expect(btns).toHaveLength(3);
  btns.forEach((b) => expect(b).toHaveAccessibleName());
  expect(screen.queryByRole('button', { name: /settings/i })).toBeNull();
});

// snapshot of /, after navigate, and /cosmic. */
test('snapshot of /, after navigate, and /cosmic', () => {
  const { asFragment, rerender } = renderHome();

  const homeSnap = asFragment();
  expect(homeSnap).toMatchSnapshot('home-root');

  fireEvent.click(screen.getByRole('button', { name: 'EXPLORE' }));
  const afterNavSnap = asFragment();
  expect(afterNavSnap).toMatchSnapshot('after-explore');

  rerender(<></>);
  const { asFragment: cosmicFrag } = renderCosmic();
  expect(cosmicFrag()).toMatchSnapshot('cosmic-direct');
});

// 10. ignore whitespace
test('ignore whitespace', () => {
  renderHome();
  expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /sign\s*up/i })).toBeInTheDocument();
  expect(screen.queryByRole('button', { name: /signups/i })).toBeNull();
});
