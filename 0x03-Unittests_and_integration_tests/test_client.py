#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: MagicMock) -> None:
        """Test that GithubOrgClient.org returns correct value"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self) -> None:
        """Test _public_repos_url property"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://example.com")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Test public_repos returns list of repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://example.com"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("http://example.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """Test has_license method"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
                          
