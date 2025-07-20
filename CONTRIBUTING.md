# Contributing to EchoGuard

Thank you for your interest in contributing to EchoGuard! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue with a descriptive title and clear description
3. Include steps to reproduce, expected behavior, and actual behavior
4. Add relevant screenshots or logs if applicable

### Suggesting Features

1. Check if the feature has already been suggested in the Issues section
2. If not, create a new issue with a descriptive title and clear description
3. Explain why this feature would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request to the `main` branch
6. Describe your changes in detail

## Development Setup

### Backend

1. Install dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

2. Local testing:
   ```
   # Use AWS SAM for local Lambda testing
   sam local invoke StartTranscribe --event events/s3-event.json
   ```

### Frontend

1. Install dependencies:
   ```
   cd frontend
   npm install
   ```

2. Start development server:
   ```
   npm start
   ```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use docstrings for functions and classes
- Write unit tests for new functionality

### JavaScript/React

- Follow Airbnb JavaScript Style Guide
- Use functional components with hooks
- Write unit tests for components and utilities

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

## Review Process

1. All code changes require review from at least one maintainer
2. Automated tests must pass
3. Code must follow project style guidelines
4. Documentation must be updated if necessary

Thank you for contributing to EchoGuard!