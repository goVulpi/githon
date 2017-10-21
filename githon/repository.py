"""Module that contains all user repository Data Scraping logic."""

import requests
from utils import BaseRequest
from exceptions import InvalidTokenError, ApiError, UsernameNotFoundError, \
    RepositoryIdNotFoundError, RepositoryNameNotFoundError, UserIdNotFoundError

ROOT_API_URL = 'https://api.github.com'


class Repository(BaseRequest):
    """Class that has Repository Data Scraping actions."""

    def __init__(self, default_access_token=None):
        """Constructor.

        Args:
            default_access_token: The default GitHub access_token

        If you don't provide an access_token, your number of requests will be limited to 60 requests per hour, acording with GitHub REST API v3.
        """
        self.default_access_token = default_access_token

    def get_repository_by_id(self, repository_id, access_token=None):
        """Return a repository with given repository_id"""
        url = "{0}/repositories/{1}{2}"

        response = requests.get(
            url.format(
                self.ROOT_API_URL, repository_id, self.get_token(access_token)
            )
        )

        remaining = requests.headers['X-RateLimit-Remaining']
        limit = requests.headers['X-RateLimit-Limit']

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError({'X-RateLimit-Remaining': remaining, 'X-RateLimit-Limit': limit})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': user_token})
        elif response.status_code == requests.codes.not_found:
            raise RepositoryIdNotFoundError({'repository_id': repository_id})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()

    def get_repository_by_username(self, username, repository_name, access_token=None):
        """Return a repository with given repository_name and username"""
        url = "{0}/repos/{1}/{2}{3}"

        response = requests.get(
            url.format(
                self.ROOT_API_URL, username, repository_name, self.get_token(access_token)
            )
        )

        remaining = requests.headers['X-RateLimit-Remaining']
        limit = requests.headers['X-RateLimit-Limit']

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError({'X-RateLimit-Remaining': remaining, 'X-RateLimit-Limit': limit})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code == requests.codes.not_found:
            raise RepositoryNameNotFoundError({'repository_name': repository_name, 'username': username})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()

    def get_repositories_by_username(self, username, access_token=None):
        """Return all repositories from a given username."""
        url = "{0}/users/{1}/repos{2}"

        response = requests.get(
            url.format(
                self.ROOT_API_URL, username,
                self.get_token(access_token)
            )
        )

        remaining = requests.headers['X-RateLimit-Remaining']
        limit = requests.headers['X-RateLimit-Limit']

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError({'X-RateLimit-Remaining': remaining, 'X-RateLimit-Limit': limit})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code == requests.codes.not_found:
            raise UsernameNotFoundError({'username': username})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()

    def get_repositories_by_user_id(self, user_id, access_token=None):
        """Return all repositories from a given user ID."""
        url = "{0}/user/{1}/repos{2}"

        response = requests.get(
            url.format(self.ROOT_API_URL, user_id, self.get_token(access_token))
        )

        remaining = requests.headers['X-RateLimit-Remaining']
        limit = requests.headers['X-RateLimit-Limit']

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError({'X-RateLimit-Remaining': remaining, 'X-RateLimit-Limit': limit})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code == requests.codes.not_found:
            raise UserIdNotFoundError({'user_id': user_id})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()

    def get_all_data(self, repository_id=None, repository_name=None, access_token):
        data = {}

        if repository_id:
            data['branches'] = self.get_branches_by_id(
                repository_id, access_token)
            data['comments'] = self.get_comments_by_id(
                repository_id, access_token)
            data['commits'] = self.get_commits_by_id(
                repository_id, access_token)
            data['contents'] = self.get_contents_by_id(
                repository_id, access_token)
            data['contributors'] = self.get_contributors_by_id(
                repository_id, access_token)
            data['events'] = self.get_events_by_id(
                repository_id, access_token)
            data['issues'] = self.get_issues_by_id(
                repository_id, access_token)
            data['labels'] = self.get_labels_by_id(
                repository_id, access_token)
            data['languages'] = self.get_languages_by_id(
                repository_id, access_token)
            data['pulls'] = self.get_pulls_by_id(
                repository_id, access_token)
            data['subscribers'] = self.get_subscribers_by_id(
                repository_id, access_token)
            data['tags'] = self.get_tags_by_id(
                repository_id, access_token)
        elif repository_name:
            data['branches'] = self.get_branches_by_name(
                repository_id, access_token)
            data['comments'] = self.get_comments_by_name(
                repository_id, access_token)
            data['commits'] = self.get_commits_by_name(
                repository_id, access_token)
            data['contents'] = self.get_contents_by_name(
                repository_id, access_token)
            data['contributors'] = self.get_contributors_by_name(
                repository_id, access_token)
            data['events'] = self.get_events_by_name(
                repository_id, access_token)
            data['issues'] = self.get_issues_by_name(
                repository_id, access_token)
            data['labels'] = self.get_labels_by_name(
                repository_id, access_token)
            data['languages'] = self.get_languages_by_name(
                repository_id, access_token)
            data['pulls'] = self.get_pulls_by_name(
                repository_id, access_token)
            data['subscribers'] = self.get_subscribers_by_name(
                repository_id, access_token)
            data['tags'] = self.get_tags_by_name(
                repository_id, access_token)

        return data

    # Attributes by name

    def get_commits_by_name(self, username, repository_name, access_token):
        """Return repository commits from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "commits", access_token)

    def get_contributors_by_name(self, username, repository_name, access_token):
        """Return repository contributors from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "contributors", access_token)

    def get_issues_by_name(self, username, repository_name, access_token):
        """Return repository issues from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "issues", access_token)

    def get_events_by_name(self, username, repository_name, access_token):
        """Return repository events from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "events", access_token)

    def get_branches_by_name(self, username, repository_name, access_token):
        """Return repository branches from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "branches", access_token)

    def get_tags_by_name(self, username, repository_name, access_token):
        """Return repository tags from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "tags", access_token)

    def get_languages_by_name(self, username, repository_name, access_token):
        """Return repository languages from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "languages", access_token)

    def get_subscribers_by_name(self, username, repository_name, access_token):
        """Return repository subscribers from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "subscribers", access_token)

    def get_comments_by_name(self, username, repository_name, access_token):
        """Return repository comments from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "comments", access_token)

    def get_contents_by_name(self, username, repository_name, access_token):
        """Return repository contents from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "contents", access_token)

    def get_pulls_by_name(self, username, repository_name, access_token):
        """Return repository pulls from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "pulls", access_token)

    def get_labels_by_name(self, username, repository_name, access_token):
        """Return repository labels from a given username.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_name(
            username, repository_name, "labels", access_token)

    # Attributes by ID

    def get_commits_by_id(self, repository_id, access_token=None):
        """Return repository commits from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "commits", access_token)

    def get_contributors_by_id(self, repository_id, access_token=None):
        """Return repository contributors from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(
            repository_id, "contributors", access_token)

    def get_issues_by_id(self, repository_id, access_token=None):
        """Return repository issues from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "issues", access_token)

    def get_events_by_id(self, repository_id, access_token=None):
        """Return repository events from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "events", access_token)

    def get_branches_by_id(self, repository_id, access_token=None):
        """Return repository branches from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "branches", access_token)

    def get_tags_by_id(self, repository_id, access_token=None):
        """Return repository tags from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "tags", access_token)

    def get_languages_by_id(self, repository_id, access_token=None):
        """Return languages tags from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "languages", access_token)

    def get_subscribers_by_id(self, repository_id, access_token=None):
        """Return subscribers tags from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "subscribers", access_token)

    def get_comments_by_id(self, repository_id, access_token=None):
        """Return comments tags from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "comments", access_token)

    def get_contents_by_id(self, repository_id, access_token=None):
        """Return contents tags from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "contents", access_token)

    def get_pulls_by_id(self, repository_id, access_token=None):
        """Return pulls tags from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "pulls", access_token)

    def get_labels_by_id(self, repository_id, access_token=None):
        """Return labels tags from a given username and repository ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        self._complete_request_by_id(repository_id, "labels", access_token)

    def _complete_request_by_name(self, username, repository_name, complement, access_token):
        """Complements an repository data request by name.

        Arguments:
            username -- Github login
            repository_name -- An existent user's repository name
            access_token -- GitHub OAuth2 access token
        """
        url = "{0}/repos/{1}/{2}/{3}{4}"

        response = requests.get(
            url.format(
                self.ROOT_API_URL, username, repository_name, complement,
                self.get_token(access_token)
            )
        )

        remaining = requests.headers['X-RateLimit-Remaining']
        limit = requests.headers['X-RateLimit-Limit']

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError({'X-RateLimit-Remaining': remaining, 'X-RateLimit-Limit': limit})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code == requests.codes.not_found:
            raise RepositoryNameNotFoundError(
                {'repository_name': repository_name, 'username': username})
        elif response.status_code >= 500 and response.status_code <= 599:
            raise ApiError()

        return response.json()

    def _complete_request_by_id(self, repository_id, complement, access_token):
        """Complements an repository data request by ID.

        Arguments:
            username -- Github login
            repository_id -- An existent user's repository ID
            access_token -- GitHub OAuth2 access token
        """
        url = "{0}/repositories/{1}/{2}{3}"

        response = requests.get(
            url.format(
                self.ROOT_API_URL, repository_id, complement,
                self.get_token(access_token)
            )
        )

        remaining = requests.headers['X-RateLimit-Remaining']
        limit = requests.headers['X-RateLimit-Limit']

        if response.status_code == requests.codes.forbidden and remaining == 0:
            raise ApiRateLimitError({'X-RateLimit-Remaining': remaining, 'X-RateLimit-Limit': limit})
        elif response.status_code == requests.codes.unauthorized:
            raise InvalidTokenError({'access_token': access_token})
        elif response.status_code == requests.codes.not_found:
            raise RepositoryIdNotFoundError({'repository_id': repository_id})
        elif response.status_code >= 500 and response.status_code <= 509:
            raise ApiError()

        return response.json()
