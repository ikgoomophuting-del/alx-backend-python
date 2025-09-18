#!/usr/bin/env python3
"""Unit tests for client.py (GithubOrgClient)."""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected repo URL."""
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            client = GithubOrgClient("testorg")

            result = client._public_repos_url

            self.assertEqual(
                result,
                "https://api.github.com/orgs/testorg/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos."""
        # Mock payload returned by get_json
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        # Patch the _public_repos_url property
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/testorg/repos"
            )

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Expected repo names from test_payload
            expected = ["repo1", "repo2", "repo3"]

            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )


if __name__ == "__main__":
    unittest.main()
