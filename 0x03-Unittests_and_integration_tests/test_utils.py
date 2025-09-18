#!/usr/bin/env python3
"""Unit tests for utils.py module."""

import unittest
from unittest.mock import patch
from utils import memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Tests for utils.access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct result."""
        from utils import access_nested_map
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError properly."""
        from utils import access_nested_map
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches results and only calls method once."""

        class TestClass:
            """Simple class to test memoization."""

            def a_method(self):
                """Return a constant integer value."""
                return 42

            @memoize
            def a_property(self):
                """Call a_method once and cache its result."""
                return self.a_method()

        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            test_instance = TestClass()

            # Call the memoized property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Verify results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was only called once (memoization worked)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
