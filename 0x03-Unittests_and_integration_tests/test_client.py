#!/usr/bin/env python3
"""
Unittests for client module.
"""
import unittest
from unittest.mock import patch, Mock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, org_payload, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = org_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, org_payload)
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch("client.get_json")
    def test_public_repos_url(self, org_name, org_payload, mock_get_json):
        """Test that the _public_repos_url property returns correct URL."""
        mock_get_json.return_value = org_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client._public_repos_url, org_payload["repos_url"])
        mock_get_json.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that the public_repos method returns the correct list of repos."""
        org_name = "google"
        repos_payload = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        expected_repos = ["repo1", "repo2", "repo3"]

        mock_get_json.side_effect = [
            {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"},
            repos_payload,
        ]

        client = GithubOrgClient(org_name)
        self.assertEqual(client.public_repos(), expected_repos)
        self.assertEqual(client.public_repos(license="my_license"), ["repo1"])
        self.assertEqual(client.public_repos(license="apache-2.0"), ["repo2"])
        self.assertEqual(client.public_repos(license="gpl"), [])
        self.assertEqual(mock_get_json.call_count, 2)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "apache-2.0"}}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean value."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get before tests."""
        cls.get_patcher = patch("requests.get", side_effect=cls.side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop mock after tests."""
        cls.get_patcher.stop()

    @classmethod
    def side_effect(cls, url, *args, **kwargs):
        """Side effect for requests.get mock."""
        if url == "https://api.github.com/orgs/google":
            return Mock(status_code=200,
                        json=MagicMock(return_value=cls.org_payload))
        if url == "https://api.github.com/orgs/google/repos":
            return Mock(status_code=200,
                        json=MagicMock(return_value=cls.repos_payload))
        raise ValueError(f"Unmocked url: {url}")

    def test_public_repos(self):
        """Test that public_repos returns expected repos list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by license."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)
