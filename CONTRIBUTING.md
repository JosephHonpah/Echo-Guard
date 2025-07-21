# Contributing to EchoGuard

Thank you for your interest in contributing to EchoGuard! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to foster an open and welcoming environment.

## How to Contribute

### Reporting Bugs

If you find a bug in the project:

1. Check if the bug has already been reported in the [Issues](https://github.com/JosephHonpah/Echo-Guard/issues) section.
2. If not, create a new issue with a clear title and description.
3. Include steps to reproduce the bug, expected behavior, and actual behavior.
4. Add screenshots or error logs if applicable.
5. Use the "bug" label for the issue.

### Suggesting Enhancements

If you have ideas for enhancements:

1. Check if the enhancement has already been suggested in the [Issues](https://github.com/JosephHonpah/Echo-Guard/issues) section.
2. If not, create a new issue with a clear title and description.
3. Explain why this enhancement would be useful to most users.
4. Use the "enhancement" label for the issue.

### Pull Requests

1. Fork the repository.
2. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name` or `git checkout -b fix/your-bugfix-name`.
3. Make your changes.
4. Run tests to ensure your changes don't break existing functionality.
5. Commit your changes with clear, descriptive commit messages.
6. Push to your fork: `git push origin feature/your-feature-name`.
7. Submit a pull request to the `main` branch of the original repository.
8. Describe what your pull request does and reference any related issues.

## Development Setup

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Node.js and npm installed
- Python 3.11 installed
- Git installed

### Local Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/JosephHonpah/Echo-Guard.git
   cd Echo-Guard
   ```

2. Set up the backend:
   ```bash
   cd backend
   # Install dependencies if needed
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Run the frontend locally:
   ```bash
   npm start
   ```

### Testing

Before submitting a pull request, please ensure:

1. All existing tests pass.
2. You've added tests for new functionality.
3. Your code follows the project's style guidelines.

## Style Guidelines

### JavaScript

- Use ES6+ features when appropriate.
- Follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
- Use meaningful variable and function names.
- Add comments for complex logic.

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
- Use docstrings for functions and classes.
- Use type hints when appropriate.

### HTML/CSS

- Use semantic HTML elements.
- Follow BEM methodology for CSS class naming.
- Ensure responsive design works on various screen sizes.

## Commit Guidelines

- Use clear, descriptive commit messages.
- Start with a verb in the present tense (e.g., "Add feature" not "Added feature").
- Reference issue numbers when applicable.
- Keep commits focused on a single logical change.

## Documentation

- Update documentation when changing functionality.
- Use clear language and provide examples when appropriate.
- Check for spelling and grammar errors.

## License

By contributing to EchoGuard, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).