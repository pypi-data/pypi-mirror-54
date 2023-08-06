from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Website(Endpoint):
    """Customer's website endpoint."""

    def list(self, customer_id: int) -> Dict:
        """List all customer's websites.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/websites/list/
        """
        response = self.base_get_request(f"{self.base_url}/{customer_id}/websites")

        return self.process_get_result(response)

    def create(self, customer_id: int, value: str) -> int:
        """Create customer's website.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/websites/create/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/websites", value=value
        )

        return self.process_result_with_status_code(response, 201)

    def update(self, customer_id: int, website_id: int, value: str) -> int:
        """Update customer's website.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/websites/update/
        """
        response = self.base_put_request(
            f"{self.base_url}/{customer_id}/websites/{website_id}", value=value
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, customer_id: int, website_id: int) -> int:
        """Delete customer's website.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/websites/delete/
        """
        response = self.base_delete_request(
            f"{self.base_url}/{customer_id}/websites/{website_id}"
        )

        return self.process_result_with_status_code(response, 204)
