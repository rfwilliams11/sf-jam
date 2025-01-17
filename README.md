# My Project

A simple Python project

## Features

- Dependency management with Poetry
- Task automation with poethepoet (poe)
- Code formatting with Black and isort
- Linting with flake8
- Testing with pytest

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/my_project.git
cd my_project
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate
# OR activate on Unix/MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install poetry poethepoet
poetry install
```

## Usage

The project includes several pre-configured tasks that can be run using `poe`:

```bash
# Run the application
poe run

# Format code
poe format

# Run linting
poe lint

# Run tests
poe test

# Run all checks (format, lint, test)
poe check
```