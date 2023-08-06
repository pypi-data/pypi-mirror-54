from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class User(Endpoint):
    """User endpoint."""

    def list(self, **kwargs) -> Dict:
        """Get all users.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/users/list/
        """
        response = self.base_get_request(self.base_url, **kwargs)

        return self.process_get_result(response)

    def user(self, user_id: int) -> Dict:
        """Get user by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/users/get/
        """
        response = self.base_get_request(f"{self.base_url}/{user_id}")

        return self.process_get_result(response)

    def resource_owner(self) -> Dict:
        """Get resource owner.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/users/me/
        """
        response = self.base_get_request(f"{self.base_url}/me")

        return self.process_get_result(response)
