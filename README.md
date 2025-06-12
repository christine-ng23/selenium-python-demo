# Web UI Testing with Selenium

This project contains automated tests for a Web application using **Selenium**, **Pytest**, and **Allure Reports**.

## Setup

```bash
git clone git@github.com:christine-ng23/selenium-python-demo.git
cd selenium-python-demo
pip install -r requirements.txt
```

## Running Tests

Run tests in parallel:

```bash
pytest -n auto --alluredir=reports
allure serve reports
```

## Folder Structure

- core/ - The core libraries layer consists of product independent, widely reusable components such as base page, utilities of logging, report, load data, etc.
- pages/ – Page Object Model for UI components
- tests/ – Web test cases
- config/ – configuration for Browser, URL, downloads directory, etc.

## Dependencies

- Python 3.9+
- pytest
- pytest-xdist
- allure-pytest
- selenium
