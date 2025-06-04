# Web UI Testing with Selenium

This project contains automated tests for a Web application using **Selenium**, **Pytest**, and **Allure Reports**.

## Setup

```bash
git clone https://github.com/your-org/web-tests.git
cd web-tests
pip install -r requirements.txt
```

Make sure the `qa-shared` repo is available either via:
- git submodule: `git submodule update --init --recursive`
- Or as an installed package

## Running Tests

Run tests in parallel:

```bash
pytest -n auto --alluredir=reports
allure serve reports
```

## Folder Structure

- pages/ – Page Object Model for UI components
- tests/ – Web test cases
- config/ – Browser and URL configuration

## Dependencies

- Python 3.9+
- pytest
- pytest-xdist
- allure-pytest
- selenium