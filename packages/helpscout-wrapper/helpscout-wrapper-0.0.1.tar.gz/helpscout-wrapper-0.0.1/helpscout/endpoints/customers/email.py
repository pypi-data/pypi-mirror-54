from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Email(Endpoint):
    """Customer's email endpoint."""

    def list(self, customer_id: int) -> Dict:
        """Get all customer's emails.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/emails/list/
        """
        response = self.base_get_request(f"{self.base_url}/{customer_id}/emails")

        return self.process_get_result(response)

    def create(self, customer_id: int, type_: str, value: str) -> int:
        """Create customer's email.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/emails/create/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/emails", type=type_, value=value
        )

        return self.process_result_with_status_code(response, 201)

    def update(self, customer_id: int, email_id: int, type_: str, value: str) -> int:
        """Update customer's email.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/emails/update/
        """
        response = self.base_pus_request(
            f"{self.base_url}/{customer_id}/emails/{email_id}", type=type_, value=value
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, customer_id: int, email_id: int) -> int:
        """Delete customer's email.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/emails/delete/
        """
        response = self.base_delete_request(
            f"{self.base_url}/{customer_id}/emails/{email_id}"
        )

        return self.process_result_with_status_code(response, 204)
