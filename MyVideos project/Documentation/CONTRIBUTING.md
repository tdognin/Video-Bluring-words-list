# Contributing to Video Text Blur Tool

Thank you for your interest in contributing to the Video Text Blur Tool! This document provides guidelines and instructions for contributing to the project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)
9. [Issue Guidelines](#issue-guidelines)
10. [Community](#community)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race
- Ethnicity
- Age
- Religion
- Nationality

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.8 or higher
- Git
- FFmpeg
- Basic understanding of:
  - Python programming
  - Video processing concepts
  - OCR technology (helpful but not required)

### First-Time Contributors

If you're new to open source, here are some good first issues:

- Documentation improvements
- Bug fixes with clear reproduction steps
- Adding examples to `example_usage.py`
- Improving error messages
- Adding unit tests

Look for issues labeled:
- `good first issue`
- `documentation`
- `help wanted`
- `beginner-friendly`

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/video-text-blur.git
cd video-text-blur

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/video-text-blur.git
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # If available

# Or install common dev tools
pip install pytest pytest-cov black flake8 mypy
```

### 4. Verify Installation

```bash
# Run the tool to ensure everything works
python blur_text_video.py --help

# Run tests (if available)
pytest
```

### 5. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

---

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 1. Bug Reports

Found a bug? Please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- System information (OS, Python version, etc.)
- Error messages or logs

#### 2. Feature Requests

Have an idea? Create an issue with:
- Clear description of the feature
- Use case and benefits
- Proposed implementation (if you have ideas)
- Examples of similar features in other tools

#### 3. Code Contributions

- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test coverage improvements

#### 4. Documentation

- README improvements
- API documentation
- Code comments
- Usage examples
- Tutorial creation
- Translation to other languages

#### 5. Testing

- Writing unit tests
- Integration tests
- Performance benchmarks
- Testing on different platforms

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

#### Code Formatting

```python
# Use 4 spaces for indentation (no tabs)
def process_video(input_path, output_path):
    """Process video with proper indentation."""
    pass

# Maximum line length: 100 characters (not 79)
long_variable_name = some_function_call(
    parameter1, parameter2, parameter3
)

# Use double quotes for strings
message = "Hello, world!"

# Use single quotes for dict keys when appropriate
config = {'key': 'value'}
```

#### Naming Conventions

```python
# Classes: PascalCase
class VideoTextBlur:
    pass

# Functions and methods: snake_case
def detect_text_regions(frame):
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_BLUR_STRENGTH = 51
MAX_CONFIDENCE = 1.0

# Private methods: _leading_underscore
def _internal_helper(self):
    pass

# Variables: snake_case
frame_count = 0
blur_strength = 51
```

#### Type Hints

Use type hints for function signatures:

```python
from typing import List, Tuple, Optional
import numpy as np

def detect_text_regions(
    self,
    frame: np.ndarray
) -> List[Tuple[int, int, int, int, str]]:
    """Detect text regions with type hints."""
    pass

def process_video(
    self,
    input_path: str,
    output_path: str,
    sample_rate: int = 1,
    padding: int = 10
) -> None:
    """Process video with type hints."""
    pass
```

#### Docstrings

Use Google-style docstrings:

```python
def blur_regions(self, frame, boxes, padding=10):
    """
    Apply blur to specified regions in the frame.
    
    Args:
        frame: Input frame as numpy array
        boxes: List of tuples (x1, y1, x2, y2, text) to blur
        padding: Extra pixels around detected text (default: 10)
    
    Returns:
        Frame with blurred regions as numpy array
    
    Raises:
        ValueError: If frame dimensions are invalid
    
    Example:
        >>> processor = VideoTextBlur()
        >>> frame = cv2.imread('frame.png')
        >>> boxes = [(100, 100, 200, 150, 'text')]
        >>> blurred = processor.blur_regions(frame, boxes)
    """
    pass
```

### Code Quality Tools

#### Black (Code Formatter)

```bash
# Format all Python files
black .

# Check without modifying
black --check .

# Format specific file
black blur_text_video.py
```

#### Flake8 (Linter)

```bash
# Run linter
flake8 .

# With specific configuration
flake8 --max-line-length=100 --ignore=E203,W503 .
```

#### MyPy (Type Checker)

```bash
# Run type checker
mypy blur_text_video.py

# With strict mode
mypy --strict blur_text_video.py
```

### Git Commit Messages

Follow these guidelines for commit messages:

```
# Format
<type>(<scope>): <subject>

<body>

<footer>

# Types
feat: New feature
fix: Bug fix
docs: Documentation changes
style: Code style changes (formatting, etc.)
refactor: Code refactoring
test: Adding or updating tests
chore: Maintenance tasks

# Examples
feat(ocr): Add support for Arabic language detection

fix(blur): Correct padding calculation for edge cases
- Fixed issue where padding exceeded frame boundaries
- Added boundary checks before applying blur
- Closes #123

docs(readme): Update installation instructions for Windows

test(blur): Add unit tests for blur_regions method
```

### Code Review Checklist

Before submitting, ensure:

- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] Type hints are included
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Error handling is appropriate
- [ ] Code is DRY (Don't Repeat Yourself)
- [ ] Variable names are descriptive
- [ ] Complex logic has comments
- [ ] Tests pass (if applicable)

---

## Testing Guidelines

### Writing Tests

```python
# tests/test_blur_text_video.py
import pytest
import numpy as np
from blur_text_video import VideoTextBlur

class TestVideoTextBlur:
    """Test suite for VideoTextBlur class."""
    
    def test_initialization(self):
        """Test proper initialization."""
        processor = VideoTextBlur(languages=['en'])
        assert processor.blur_strength == 51
        assert processor.confidence_threshold == 0.5
    
    def test_should_blur_text_with_target_words(self):
        """Test text matching logic."""
        processor = VideoTextBlur(target_words=['password'])
        assert processor.should_blur_text('Password123') is True
        assert processor.should_blur_text('hello world') is False
    
    def test_blur_regions(self):
        """Test blur application."""
        processor = VideoTextBlur()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        boxes = [(100, 100, 200, 150, 'test')]
        result = processor.blur_regions(frame, boxes)
        assert result.shape == frame.shape
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=blur_text_video --cov-report=html

# Run specific test file
pytest tests/test_blur_text_video.py

# Run specific test
pytest tests/test_blur_text_video.py::TestVideoTextBlur::test_initialization

# Run with verbose output
pytest -v
```

### Test Coverage

Aim for:
- **Minimum**: 70% code coverage
- **Target**: 80% code coverage
- **Ideal**: 90%+ code coverage

---

## Documentation

### Documentation Standards

#### Code Comments

```python
# Good: Explain WHY, not WHAT
# Use sample rate to reduce OCR calls and improve performance
if frame_count % sample_rate == 0:
    boxes = self.detect_text_regions(frame)

# Bad: Obvious comment
# Increment frame count
frame_count += 1
```

#### README Updates

When adding features, update:
- Feature list
- Usage examples
- Command-line options
- Troubleshooting section

#### API Documentation

Update `API_REFERENCE.md` when:
- Adding new methods
- Changing method signatures
- Adding new parameters
- Modifying return values

#### Architecture Documentation

Update `ARCHITECTURE.md` when:
- Adding new components
- Changing data flow
- Modifying processing pipeline
- Adding dependencies

---

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   pytest
   flake8 .
   black --check .
   ```

3. **Update documentation**
   - Update README if needed
   - Add docstrings to new functions
   - Update CHANGELOG.md

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add new feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

### Creating the Pull Request

1. Go to GitHub and create a Pull Request
2. Fill out the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
```

3. Link related issues: `Closes #123`

### Review Process

1. **Automated Checks**: CI/CD runs tests and linters
2. **Code Review**: Maintainers review your code
3. **Feedback**: Address review comments
4. **Approval**: Once approved, maintainers will merge

### After Merge

1. **Delete your branch**
   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

2. **Update your fork**
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

---

## Issue Guidelines

### Creating Issues

#### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
1. Run command: `python blur_text_video.py ...`
2. See error

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**System Information**
- OS: [e.g., macOS 12.0]
- Python version: [e.g., 3.10.0]
- FFmpeg version: [e.g., 4.4.0]

**Error messages**
```
Paste error messages here
```

**Additional context**
Any other relevant information
```

#### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired feature

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Examples, mockups, or references
```

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested
- `wontfix`: This will not be worked on
- `duplicate`: This issue already exists

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions and reviews

### Getting Help

If you need help:

1. Check existing documentation
2. Search closed issues
3. Ask in GitHub Discussions
4. Create a new issue with the `question` label

### Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project README

---

## Development Workflow

### Typical Workflow

```bash
# 1. Sync with upstream
git checkout main
git pull upstream main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes
# ... edit files ...

# 4. Test changes
pytest
flake8 .
black .

# 5. Commit changes
git add .
git commit -m "feat: Add my feature"

# 6. Push to fork
git push origin feature/my-feature

# 7. Create Pull Request on GitHub

# 8. Address review feedback
# ... make changes ...
git add .
git commit -m "fix: Address review comments"
git push origin feature/my-feature

# 9. After merge, cleanup
git checkout main
git pull upstream main
git branch -d feature/my-feature
```

### Branch Naming

- `feature/description`: New features
- `fix/description`: Bug fixes
- `docs/description`: Documentation
- `refactor/description`: Code refactoring
- `test/description`: Test additions

---

## Release Process

### Version Numbers

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Checklist

For maintainers:

1. Update version in `blur_text_video.py`
2. Update `CHANGELOG.md`
3. Update documentation
4. Create release branch
5. Run full test suite
6. Create GitHub release
7. Tag release: `git tag v1.0.0`
8. Push tags: `git push --tags`

---

## Additional Resources

### Learning Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)

### Tools

- [Black](https://black.readthedocs.io/): Code formatter
- [Flake8](https://flake8.pycqa.org/): Linter
- [MyPy](http://mypy-lang.org/): Type checker
- [Pytest](https://pytest.org/): Testing framework

---

## Questions?

If you have questions about contributing:

1. Check this guide
2. Search existing issues
3. Ask in GitHub Discussions
4. Contact maintainers

---

## Thank You!

Thank you for contributing to the Video Text Blur Tool! Your contributions help make this project better for everyone.

---

**Document Version**: 1.0.0  
**Last Updated**: February 22, 2026

---

**End of Contributing Guidelines**