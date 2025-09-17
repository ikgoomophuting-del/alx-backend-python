#!/usr/bin/env python3
"""
Integration tests for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {"org_payload": TEST_PAYLOAD[0],
     "repos_payload": TEST_PAYLOAD[1],
     "expected_repos": ["episodes.py", "git-consortium"],
     "apache2_repos": ["episodes.py"]},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls) -> None:
        """Start patcher for requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Configure side effect for mocked requests.get
        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: cls.org_payload),
            unittest.mock.Mock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patcher for requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns expected repo list"""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test that public_repos filters repos by license"""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
