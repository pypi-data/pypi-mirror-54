from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class ChatHandler(Endpoint):
    """Customer's chat handler endpoint."""

    def list(self, customer_id: int) -> Dict:
        """Get all customer's chat handlers.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/chat_handles/list/
        """
        response = self.base_get_request(f"{self.base_url}/{customer_id}/chats")

        return self.process_get_result(response)

    def create(self, customer_id: int, type_: str, value: str) -> int:
        """Create customer's chat handler.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/chat_handles/create/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/chats", type=type_, value=value
        )

        return self.process_result_with_status_code(response, 201)

    def update(self, customer_id: int, chat_id: int, type_: str, value: str) -> int:
        """Update customer's chat handler.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/chat_handles/update/
        """
        response = self.base_put_request(
            f"{self.base_url}/{customer_id}/chats/{chat_id}", type=type_, value=value
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, customer_id: int, chat_id: int) -> int:
        """Delete customer's chat handler.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/chat_handles/delete/
        """
        response = self.base_delete_request(
            f"{self.base_url}/{customer_id}/chats/{chat_id}"
        )

        return self.process_result_with_status_code(response, 204)
