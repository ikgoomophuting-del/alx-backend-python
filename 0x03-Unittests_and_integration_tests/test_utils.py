#!/usr/bin/env python3
"""
Test module for mocking HTTP calls.
"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    def test_public_repos(self):
        """Test public_repos method using mock HTTP calls."""
        # Mock payload to return
        mock_repos = [{"name": "repo1"}, {"name": "repo2"}]

        # Patch get_json and _public_repos_url using context managers
        with patch('client.get_json', return_value=mock_repos) as mock_get_json:
            with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=unittest.mock.PropertyMock
            ) as mock_url:
                mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

                # Create instance and call method
                client = GithubOrgClient("testorg")
                result = client.public_repos()

                # Assertions
                self.assertEqual(result, ["repo1", "repo2"])
                mock_get_json.assert_called_once()
                mock_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()
