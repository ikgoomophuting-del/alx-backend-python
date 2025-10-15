#!/usr/bin/env python3
"""
Mock HTTP calls
"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        # Define the mock payload
        payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        # Mock get_json return value
        mock_get_json.return_value = payload

        # Mock the _public_repos_url property
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=unittest.mock.PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            # Create instance and call the method
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Assertions
            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)

            # Verify mocks
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()
