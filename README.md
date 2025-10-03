# Test Project (Python + Playwright)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pytest pytest-playwright playwright
python -m playwright install --with-deps
```

## Run tests

```bash
pytest
```

## Project structure

```
.
├── .gitignore
├── README.md
├── pytest.ini
└── tests
    └── test_example.py
```
