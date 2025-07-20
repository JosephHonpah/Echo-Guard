import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the AWS Amplify Auth
jest.mock('aws-amplify', () => ({
  Amplify: {
    configure: jest.fn()
  },
  Auth: {
    currentAuthenticatedUser: jest.fn()
  },
  API: {
    get: jest.fn(),
    post: jest.fn()
  }
}));

// Mock the withAuthenticator HOC
jest.mock('@aws-amplify/ui-react', () => ({
  withAuthenticator: (component) => {
    const WrappedComponent = (props) => {
      const user = {
        attributes: {
          email: 'test@example.com'
        }
      };
      return component({ ...props, user, signOut: jest.fn() });
    };
    return WrappedComponent;
  }
}));

test('renders EchoGuard header', () => {
  render(<App />);
  const headerElement = screen.getByText(/EchoGuard/i);
  expect(headerElement).toBeInTheDocument();
});

test('renders welcome message with user email', () => {
  render(<App />);
  const welcomeElement = screen.getByText(/Welcome, test@example.com/i);
  expect(welcomeElement).toBeInTheDocument();
});

test('renders upload section', () => {
  render(<App />);
  const uploadElement = screen.getByText(/Upload Audio Recording/i);
  expect(uploadElement).toBeInTheDocument();
});

test('renders footer with copyright', () => {
  render(<App />);
  const footerElement = screen.getByText(/AI-powered compliance monitoring/i);
  expect(footerElement).toBeInTheDocument();
});