# File: /python-poetry-project/python-poetry-project/README.md

# Python Poetry Project

This project is a Python application managed with Poetry for dependency management and Poe for task management.

## Project Structure

```
python-poetry-project
├── src
│   └── project
│       ├── __init__.py
│       └── main.py
├── tests
│   ├── __init__.py
│   └── test_main.py
├── .gitignore
├── pyproject.toml
├── poetry.lock
├── poe.toml
└── README.md
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd python-poetry-project
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Run the application:**
   ```bash
   poetry run python src/project/main.py
   ```

## Running Tests

To run the tests, use the following command:

```bash
poetry run pytest
```

## Task Management

To manage tasks, you can use Poe. For a list of available tasks, run:

```bash
poe
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.