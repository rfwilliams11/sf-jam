# SF Jam 🌉🎸

SF Jam is a simple Streamlit app aggregating upcoming concerts from Bay Area venues.

Current venue lineup:
- The Chapel
- The Fillmore
- Fox Theatre (Oakland)
- The Warfield
- Greek Theatre (Berkeley)
- The Independent

## Setup
```bash
# Install Poetry
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
- `poe run`: Populate concert data from venue sites
- `poe app`: Launch Streamlit application