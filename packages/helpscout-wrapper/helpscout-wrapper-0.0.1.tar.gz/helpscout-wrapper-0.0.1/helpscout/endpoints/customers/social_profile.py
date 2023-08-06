from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class SocialProfile(Endpoint):
    """Customer's social profile endpoint."""

    def list(self, customer_id: int) -> Dict:
        """Get all customer's social profiles.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/social_profiles/list/
        """
        response = self.base_get_request(
            f"{self.base_url}/{customer_id}/social-profiles"
        )

        return self.process_get_result(response)

    def create(self, customer_id: int, type_: str, value: str) -> int:
        """Create customer's social profile.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/social_profiles/create/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/social-profiles", type=type_, value=value
        )

        return self.process_result_with_status_code(response, 201)

    def update(self, customer_id: int, profile_id: int, type_: str, value: str) -> int:
        """Update customer's social profile.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/social_profiles/update/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/social-profiles/{profile_id}",
            type=type_,
            value=value,
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, customer_id: int, profile_id: int) -> int:
        """Delete customer's social profile.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/social_profiles/delete/
        """
        response = self.base_delete_request(
            f"{self.base_url}/{customer_id}/social-profiles/{profile_id}"
        )

        return self.process_result_with_status_code(response, 204)
