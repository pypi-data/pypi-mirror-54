from typing import Dict

import requests

from helpscout.endpoints import (Conversation, Customer, Mailbox, Report, Tag,
                                 Team, User, Webhook, Workflow)
from helpscout.exceptions import NotAuthorizedException


class Client:
    """Help scout API v2 wrapper."""

    base_api_url = "https://api.helpscout.net/v2"

    def __init__(self, app_id: str, app_secret: str):
        """The app credentials are created on the My App section in your profile.
        More about credentials here:
        https://developer.helpscout.com/mailbox-api/overview/authentication/
        """
        self._app_id = app_id
        self._app_secret = app_secret
        self._auth_params = self._get_authentication_params()
        self._access_token = self._get_access_token()

    @property
    def access_token(self):
        """Get access token."""
        return self._access_token

    @property
    def conversation(self) -> Conversation:
        """Conversation endpoint."""
        return Conversation(client=self, base_url=f"{self.base_api_url}/conversations")

    @property
    def customer(self) -> Customer:
        """Customer endpoint."""
        return Customer(client=self, base_url=f"{self.base_api_url}/customers")

    @property
    def mailbox(self) -> Mailbox:
        """Mailbox endpoint."""
        return Mailbox(client=self, base_url=f"{self.base_api_url}/mailboxes")

    @property
    def report(self) -> Report:
        """Report endpoint."""
        return Report(client=self, base_url=f"{self.base_api_url}/reports")

    @property
    def tag(self) -> Tag:
        """Tag endpoint."""
        return Tag(client=self, base_url=f"{self.base_api_url}/tags")

    @property
    def team(self) -> Team:
        """Team endpoint."""
        return Team(client=self, base_url=f"{self.base_api_url}/teams")

    @property
    def user(self) -> User:
        """User endpoint."""
        return User(client=self, base_url=f"{self.base_api_url}/users")

    @property
    def webhook(self) -> Webhook:
        """Webhook endpoint."""
        return Webhook(client=self, base_url=f"{self.base_api_url}/webhooks")

    @property
    def workflow(self) -> Workflow:
        """Workflow endpoint."""
        return Workflow(client=self, base_url=f"{self.base_api_url}/workflows")

    def _get_authentication_params(self) -> Dict:
        response = requests.post(
            f"{self.base_api_url}/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self._app_id,
                "client_secret": self._app_secret,
            },
        )

        if response.ok:
            return response.json()

        raise NotAuthorizedException()

    def _get_access_token(self) -> str:
        return self._auth_params.get("access_token", "")
