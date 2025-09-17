# 0x03. Unittests and Integration Tests

This project is part of the **ALX Backend Python** curriculum.  
It focuses on writing **unit tests** and **integration tests** in Python using the `unittest` framework, `unittest.mock`, and `parameterized`.  

The goal is to learn how to build robust test suites that validate both **individual functions** in isolation and **end-to-end workflows** involving multiple components.

---

## Learning Objectives

By the end of this project, you should be able to:

1. Explain the difference between **unit tests** and **integration tests** in Python.  
2. Apply **mocking** techniques to replace external dependencies such as HTTP calls or database queries.  
3. Use **parameterization** to run the same test with multiple input values.  
4. Write and use **fixtures** to simplify integration tests.  
5. Ensure that all code, classes, and functions are **fully documented** and **type-annotated**.  

---

## Project Structure

0x03-Unittests_and_integration_tests/

├── client.py                    # Contains GithubOrgClient class 

├── fixtures.py                  # Test fixtures with sample payloads 

├── utils.py                     # Utility functions such as access_nested_map, get_json, memoize

├── test_utils.py                # Unit tests for utils.py

├── test_client.py               # Unit tests for client.py

├── test_integration.py          # Integration tests for GithubOrgClient

└── README.md                    # Project documentation

---

## Types of Tests

### Unit Tests
Unit tests validate **single functions or methods** in isolation.  
Examples in this project include:
- `utils.access_nested_map`: retrieving values from nested dictionaries.  
- `utils.get_json`: mocking HTTP requests so no real network call is made.  
- `utils.memoize`: ensuring repeated calls return cached results.  
- `GithubOrgClient.has_license`: checking license filtering logic.  

The purpose of a unit test is:  
> If everything outside the function works correctly, does this function work as expected?

### Integration Tests
Integration tests validate **end-to-end behavior** of multiple components.  
For example:
- `GithubOrgClient.public_repos`: ensures repository fetching, filtering, and license checks work together.  

Integration tests use **fixtures** (`org_payload`, `repos_payload`) to simulate API responses, and only the lowest-level HTTP request (`requests.get`) is mocked.  

The purpose of an integration test is:  
> Do all parts of the system interact correctly when combined?

---

## Requirements

All files in this project must follow these rules:

- Interpreted/compiled on **Ubuntu 18.04 LTS** using **Python 3.7**.  
- The first line of each file must be exactly:  
  ```bash
  #!/usr/bin/env python3

  Code must follow pycodestyle 2.5.

All files must be executable.

All files must end with a new line.

All modules, classes, and functions must include docstrings that are complete sentences.

All functions and coroutines must be type-annotated.
  
---

## Resources

unittest — https://docs.python.org/3/library/unittest.html

unittest.mock — mock object library

parameterized — parameterized testing for Python

Memoization in Python

---

## Running Tests

To run a specific test file:

python3 -m unittest path/to/test_file.py


Example:

python3 -m unittest test_utils.py
python3 -m unittest test_client.py


To run all tests at once:

python3 -m unittest discover

---

## Key Ideas

Unit tests check correctness of small isolated parts.

Integration tests check correctness of the entire system working together.

Both are necessary to ensure reliable software.

---

## Author

Project completed as part of ALX Backend Python program.

