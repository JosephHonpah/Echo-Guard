---
inclusion: fileMatch
fileMatchPattern: 'frontend/src/**/*.{js,jsx}'
---

# React Standards for EchoGuard Frontend

When developing the React frontend for EchoGuard:

## Code Organization
- Use functional components with hooks
- Organize components by feature/domain
- Keep components small and focused
- Use proper file naming conventions (PascalCase for components)

## State Management
- Use React Context for global state
- Leverage useState for component-level state
- Use useReducer for complex state logic
- Implement proper loading/error states

## Performance
- Use React.memo for expensive renders
- Implement proper dependency arrays in useEffect
- Use lazy loading for route components
- Avoid unnecessary re-renders

## AWS Amplify Usage
- Use Amplify hooks for authentication
- Implement proper error handling for API calls
- Use Storage module for S3 interactions
- Follow Amplify best practices for configuration

## Accessibility
- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation works
- Test with screen readers
- Maintain proper color contrast

## Testing
- Write unit tests for components
- Test custom hooks separately
- Use React Testing Library
- Implement integration tests for critical flows