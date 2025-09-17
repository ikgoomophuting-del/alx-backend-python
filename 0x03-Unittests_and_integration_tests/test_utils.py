#!/usr/bin/env python3
"""
Unit tests for utils.py module.
"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from utils import get_json, access_nested_map, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for utils.access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns expected result.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        Test that access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unit tests for utils.get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str,
                      test_payload: dict,
                      mock_get: MagicMock) -> None:
        """
        Test that get_json returns expected result with mocked requests.get.
        """
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for utils.memoize."""

    def test_memoize(self):
        """
        Test that a_property calls a_method only once
        due to memoization.
        """

        class TestClass:
            """Simple test class with a memoized property."""

            def a_method(self):
                """Dummy method that returns 42."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        test_instance = TestClass()

        self.assertEqual(
    mocked_method.call_args,
    ((expected_argument, another_argument),)
        )
        
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # First call executes a_method
            result1 = test_instance.a_property
            # Second call uses cached result
            result2 = test_instance.a_property

            # Check results
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was only called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
