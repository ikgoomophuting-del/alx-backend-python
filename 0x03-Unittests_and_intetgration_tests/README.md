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

├── client.py             # Contains GithubOrgClient class 

├── fixtures.py           # Test fixtures with sample payloads 

├── utils.py              # Utility functions such as access_nested_map, get_json, memoize

├── test_utils.py         # Unit tests for utils.py

├── test_client.py        # Unit tests for client.py

├── test_integration.py   # Integration tests for GithubOrgClient

└── README.md             # Project documentation
