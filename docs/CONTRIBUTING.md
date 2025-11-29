# Contributing to GeoConsulta

Thank you for your interest in contributing to GeoConsulta! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/geoconsulta-research.git
   cd geoconsulta-research
   ```
3. **Set up the development environment** following the instructions in the main README
4. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ES6+ features and consistent formatting
- **HTML/CSS**: Use semantic HTML and organized CSS
- **Comments**: Write clear, concise comments for complex logic

### Commit Messages

Use clear and descriptive commit messages:
- `feat: add proximity search functionality`
- `fix: resolve marker clustering issue`
- `docs: update installation instructions`
- `refactor: optimize database queries`

### Testing

- Test your changes thoroughly before submitting
- Ensure the application runs without errors
- Test on different browsers and screen sizes
- Verify database operations work correctly

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Detailed steps to reproduce the bug
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, browser, Python version, etc.
6. **Screenshots**: If applicable

## 💡 Feature Requests

For new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** clearly and concisely
3. **Explain the use case** and why it would be valuable
4. **Provide examples** if possible

## 🔧 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update the README** if you've added new features
5. **Submit the pull request** with a clear description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 📚 Development Setup

### Prerequisites

- Python 3.8+
- PostgreSQL with PostGIS
- Node.js (for development tools)

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database**:
   ```bash
   createdb geoconsulta
   psql -d geoconsulta -f scripts/database/setup.sql
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the application**:
   ```bash
   cd src
   python main.py
   ```

## 🏗️ Project Structure

```
geoconsulta-research/
├── src/                    # Source code
│   ├── main.py            # Flask app entry point
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   └── static/            # Frontend files
├── scripts/               # Utility scripts
├── docs/                  # Documentation
├── paper/                 # Research paper
└── tests/                 # Test files (to be added)
```

## 🎯 Areas for Contribution

We welcome contributions in these areas:

### Backend
- Performance optimizations
- Additional spatial queries
- API improvements
- Error handling enhancements

### Frontend
- UI/UX improvements
- Mobile responsiveness
- Accessibility features
- New visualization options

### Database
- Query optimizations
- Data validation
- Migration scripts
- Backup utilities

### Documentation
- Code documentation
- User guides
- API documentation
- Deployment guides

### Testing
- Unit tests
- Integration tests
- Performance tests
- Browser compatibility tests

## 📞 Getting Help

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Email**: Contact the maintainers for sensitive issues

## 📄 License

By contributing to GeoConsulta, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Academic publications (if applicable)

Thank you for contributing to GeoConsulta! 🎉
