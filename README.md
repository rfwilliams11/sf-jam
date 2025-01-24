# SF Jam 🎸🌉

## Overview
SF Jam is a Streamlit web application aggregating upcoming concerts from San Francisco venues.

## Setup
```bash
# Install Poetry (if not already installed)
pip install poetry

# Clone the repository
git clone https://github.com/rfwilliams/sf-jam.git
cd sf-jam

# Install dependencies
poetry install
```

## Development Tasks
- `poe format`: Format code with Black and isort
- `poe lint`: Run flake8 linter
- `poe test`: Run pytest
- `poe check`: Run all checks (format, lint, test)
- `poe app`: Launch Streamlit application