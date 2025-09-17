# 0x03. Unittests and Integration Tests

This project covers writing **unit tests** and **integration tests** in Python.  
It is part of the **ALX Backend Python** specialization.

## Learning Objectives
- Understand the difference between unit tests and integration tests
- Use the `unittest` framework effectively
- Apply `unittest.mock` to mock objects and functions
- Use parameterization to simplify tests
- Write integration tests for end-to-end validation

## Requirements
- Python 3.7
- Ubuntu 18.04 LTS
- All files executable and PEP8 compliant
- All modules, classes, and functions must have docstrings
- Functions and coroutines must be type-annotated

## Project Structure
├── client.py          # code to test (GithubOrgClient)
├── fixtures.py        # test fixtures (JSON for integration tests)
├── test_utils.py      # unit tests for utils.py
├── utils.py           # functions to test (access_nested_map, get_json, memoize)
└── README.md


## Tasks Overview
0. Parameterize a unit test

Write a test for utils.access_nested_map using @parameterized.expand.

Check different nested dictionary/path combinations.

1. Exceptions

Write tests for cases where access_nested_map raises a KeyError.

2. Mock HTTP calls

Write unit tests for utils.get_json by mocking HTTP responses.

3. Parameterize and patch

Write tests for memoization functions with @patch.

4. Test a class with mocks

Test methods in client.GithubOrgClient by mocking calls to external APIs.

5. Parameterize integration tests

Write integration tests for client.GithubOrgClient methods using fixtures.

## Running Tests
To run a specific test file:
```bash
python3 -m unittest test_utils.py
