# Contributing to DJ Backup

Thank you for considering contributing to DJ Backup! We value your time and effort to help improve this project. This document outlines the guidelines for contributing to ensure a smooth and collaborative process.

## Getting Started

1. **Fork the Repository**: Create a fork of the [DJ Backup repository](https://github.com/FZl47/dj_backup) on GitHub.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/your-username/dj_backup.git
   ```
3. **Set Up the Development Environment**:
   - Ensure you have Python 3.8+ and Django 3.2+ installed.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     pip install djbackup[all]  # For full features
     ```
   - Set up a Django project and add `dj_backup` to `INSTALLED_APPS`.

4. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Contribution Guidelines

### Code Contributions
- **Follow the Code Style**: Use [Black](https://github.com/psf/black) for code formatting and adhere to PEP 8 guidelines.
- **Write Tests**: Add unit tests for new features or bug fixes using Django’s testing framework. Aim for high test coverage.
- **Document Changes**: Update the [README.md](README.md) or [documentation](https://djbackup.readthedocs.io/) if your changes affect usage or configuration.
- **Keep Commits Clean**: Write clear and concise commit messages. Use the format:
  ```
  [Feature/Bugfix]: Brief description of the change
  ```
  Example:
  ```
  [Feature]: Add support for AWS S3 storage provider
  ```

### Reporting Bugs
- Check the [Issue Tracker](https://github.com/FZl47/dj_backup/issues) to ensure the bug hasn’t been reported.
- Open a new issue with a clear title and description, including:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Environment details (Python/Django versions, OS, etc.)

### Suggesting Features
- Open an issue with the `[Feature Request]` prefix in the title.
- Describe the feature, its use case, and potential implementation ideas.
- Tag it with the `enhancement` label.

## Submitting a Pull Request
1. **Push Your Changes**:
   ```bash
   git push origin feature/your-feature-name
   ```
2. **Create a Pull Request**:
   - Go to the [DJ Backup repository](https://github.com/FZl47/dj_backup) and create a pull request from your branch.
   - Provide a clear description of the changes and reference any related issues.
3. **Code Review**: Respond to feedback from maintainers and make necessary updates.
4. **Merge**: Once approved, your pull request will be merged into the main branch.

## Questions?
If you have questions or need help, open an issue on [GitHub Issues](https://github.com/FZl47/dj_backup/issues) or contact the maintainers.

Thank you for contributing to DJ Backup! 🚀