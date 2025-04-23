# Contributing to Waselni

We love your input! We want to make contributing to Waselni as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use Github to host code, to track issues and feature requests, as well as accept pull requests.

## Development Process
We use Github Flow, so all code changes happen through pull requests:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License
When you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report bugs using Github's [issue tracker]
We use GitHub issues to track public bugs. Report a bug by [opening a new issue]().

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)

## License
By contributing, you agree that your contributions will be licensed under its MIT License.

## References
This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/master/CONTRIBUTING.md).

## AI Development Guidelines

When contributing to AI components:

1. **Model Training**
   - Use standardized datasets
   - Document training parameters
   - Include evaluation metrics

2. **Code Quality**
   - Follow PEP 8 style guide
   - Include docstrings
   - Write unit tests

3. **AI Features**
   - Sentiment analysis improvements
   - Voice recognition enhancements
   - Route optimization algorithms
   - Safety monitoring systems

## Getting Started

1. **Setup Development Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

2. **Run Tests**
```bash
python manage.py test
```

3. **Code Style**
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Questions?
If you have any questions about the project or need assistance, please reach out to:

- **Project Maintainer**: Selim Manai
- **Email**: slimmenei20@gmail.com
- **LinkedIn**: [Selim Manai](https://www.linkedin.com/in/selim-manai-186a4932a/)
- **GitHub**: [slimgithub04](https://github.com/slimgithub04)

You can also open an issue in the repository for technical discussions or feature requests.