#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient."""

from typing import Any, Dict, List
import unittest
from unittest.mock import patch, PropertyMock, MagicMock

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    def test_public_repos_url(self) -> None:
        """_public_repos_url should return repos_url from org property."""
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
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
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """public_repos returns list of repo names from get_json data."""
        payload: List[Dict[str, Any]] = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = payload

        expected_url = "https://api.github.com/orgs/testorg/repos"
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = expected_url

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
