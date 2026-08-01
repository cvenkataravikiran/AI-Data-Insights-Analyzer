# Contributing to InsightLens AI

Thank you for your interest in contributing to **InsightLens AI**! We welcome contributions from the community and appreciate your efforts to make this project better.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful, inclusive, and constructive in all interactions.

**Key Principles:**
- Be respectful and welcoming
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy toward other community members

---

## How to Contribute

There are many ways to contribute to InsightLens AI:

### 1. Report Bugs
Found a bug? Help us fix it by [opening an issue](https://github.com/yourusername/InsightLens-AI/issues/new) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### 2. Suggest Features
Have an idea for improvement? [Open a feature request](https://github.com/yourusername/InsightLens-AI/issues/new) with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Examples or mockups (if applicable)

### 3. Improve Documentation
- Fix typos or unclear instructions
- Add examples and tutorials
- Translate documentation
- Create video guides

### 4. Write Code
- Fix bugs
- Implement new features
- Improve performance
- Add tests
- Refactor code

---

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setup Steps

1. **Fork the Repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/InsightLens-AI.git
   cd InsightLens-AI
   ```

3. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/yourusername/InsightLens-AI.git
   ```

4. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Create Environment File** (Optional)
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

7. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## Coding Standards

### Python Style Guide
We follow **PEP 8** style guidelines. Key points:

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 88 characters (Black formatter standard)
- **Naming Conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
- **Imports**: Organized in three groups (standard library, third-party, local)

### Example
```python
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from services.analyzer import DataAnalyzer
from utils.helpers import create_export_folder


class DataProcessor:
    """Process and analyze data for insights."""
    
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    def __init__(self, df: pd.DataFrame):
        """Initialize processor with dataframe.
        
        Args:
            df: Input pandas DataFrame
        """
        self.df = df.copy()
    
    def process_data(self) -> pd.DataFrame:
        """Clean and process data.
        
        Returns:
            Processed DataFrame
        """
        return self.df.dropna()


def calculate_metrics(data: pd.DataFrame) -> dict:
    """Calculate key metrics from data.
    
    Args:
        data: Input DataFrame
    
    Returns:
        Dictionary of metrics
    """
    return {
        'total': data['sales'].sum(),
        'average': data['sales'].mean()
    }
```

### Type Hints
Use type hints for function parameters and return values:
```python
def analyze_sales(df: pd.DataFrame, period: str = 'monthly') -> dict:
    """Analyze sales data."""
    pass
```

### Docstrings
Use Google-style docstrings:
```python
def complex_function(param1: str, param2: int = 0) -> bool:
    """Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 is empty
    """
    pass
```

### Code Organization
- **Modularity**: Break code into small, reusable functions
- **Single Responsibility**: Each function should do one thing well
- **DRY Principle**: Don't Repeat Yourself
- **Comments**: Explain "why", not "what"

---

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
# Good commits
feat(dashboard): add profit margin visualization
fix(upload): handle CSV encoding errors
docs(readme): update installation instructions
refactor(analyzer): simplify trend calculation logic

# Bad commits
fixed stuff
update
changes
WIP
```

### Commit Best Practices
- Use present tense ("add" not "added")
- Keep subject line under 50 characters
- Capitalize subject line
- Don't end subject with period
- Separate subject from body with blank line
- Wrap body at 72 characters
- Explain what and why, not how

---

## Pull Request Process

### Before Submitting

1. **Sync with Upstream**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write clean, documented code
   - Follow coding standards
   - Add tests if applicable

4. **Test Your Changes**
   ```bash
   # Run the app
   streamlit run app.py
   
   # Test with different datasets
   # Verify all features work
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting PR

1. **Open Pull Request** on GitHub
2. **Fill Out Template** with:
   - Description of changes
   - Related issue numbers
   - Type of change (bug fix, feature, etc.)
   - Testing done
   - Screenshots (if UI changes)

### PR Template
```markdown
## Description
Brief description of changes

## Related Issues
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested with sample dataset
- [ ] All features work as expected
- [ ] No breaking changes

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings/errors
```

### Review Process
1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, PR will be merged
4. Your contribution will be credited!

---

## Reporting Bugs

### Before Reporting
- Check if bug already reported
- Verify it's reproducible
- Test with latest version

### Bug Report Template
```markdown
**Describe the bug**
A clear and concise description

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. Upload '...'
4. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
 - OS: [e.g., Windows 10]
 - Python Version: [e.g., 3.9]
 - Browser: [e.g., Chrome 91]

**Dataset**
- File format: CSV/Excel
- File size: 2MB
- Columns: 10
- Rows: 1000

**Additional context**
Any other relevant information
```

---

## Suggesting Features

### Before Suggesting
- Check if feature already requested
- Ensure it aligns with project goals
- Consider implementation feasibility

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
What you want to happen

**Describe alternatives you've considered**
Alternative solutions or features

**Additional context**
Mockups, examples, or related projects

**Implementation ideas**
Potential approach to implementation
```

---

## Development Guidelines

### Adding New Features

1. **Plan First**
   - Discuss in issue before coding
   - Get feedback on approach
   - Consider edge cases

2. **Implement**
   - Follow coding standards
   - Keep changes focused
   - Add error handling

3. **Document**
   - Update README if needed
   - Add docstrings
   - Include examples

4. **Test**
   - Test with various datasets
   - Test edge cases
   - Verify no regressions

### Project Structure
```
InsightLens-AI/
├── app.py                  # Main application
├── components/             # UI components
│   ├── charts.py
│   ├── dashboard.py
│   └── metrics.py
├── services/              # Business logic
│   ├── analyzer.py
│   ├── cleaner.py
│   ├── forecasting.py
│   └── insights.py
└── utils/                 # Helper functions
    ├── helpers.py
    └── validators.py
```

### Adding New Services
```python
# services/new_service.py
"""
Brief description of service.
"""

import pandas as pd
import numpy as np


class NewService:
    """Service class description."""
    
    def __init__(self, df: pd.DataFrame, config: dict = None):
        """Initialize service.
        
        Args:
            df: Input DataFrame
            config: Configuration dictionary
        """
        self.df = df.copy()
        self.config = config or {}
    
    def process(self) -> dict:
        """Main processing method.
        
        Returns:
            Processing results
        """
        # Implementation
        pass
```

---

## Questions?

- **GitHub Discussions**: [Ask questions](https://github.com/yourusername/InsightLens-AI/discussions)
- **GitHub Issues**: [Report bugs](https://github.com/yourusername/InsightLens-AI/issues)
- **Email**: support@insightlens-ai.com

---

## Recognition

Contributors are recognized in:
- README.md Contributors section
- GitHub Contributors page
- Release notes

Thank you for contributing to InsightLens AI! 🎉

---

<div align="center">

**Made with ❤️ by the InsightLens AI Community**

[Back to README](README.md)

</div>
