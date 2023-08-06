from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Phone(Endpoint):
    """Customer's phone endpoint."""

    def list(self, customer_id: int) -> Dict:
        """Get all customer's phones.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/phones/list/
        """
        response = self.base_get_request(f"{self.base_url}/{customer_id}/phones")

        return self.process_get_result(response)

    def create(self, customer_id: int, type_: str, value: str) -> int:
        """Create customer's phone.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/phones/create/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/phones", type=type_, value=value
        )

        return self.process_result_with_status_code(response, 201)

    def update(self, customer_id: int, phone_id: int, type_: str, value: str) -> int:
        """Update customer's phone.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/phones/update/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/phones/{phone_id}", type=type_, value=value
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, customer_id: int, phone_id: int) -> int:
        """Delete customer's phone.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/phones/delete/
        """
        response = self.base_delete_request(
            f"{self.base_url}/{customer_id}/phones/{phone_id}"
        )

        return self.process_result_with_status_code(response, 204)
