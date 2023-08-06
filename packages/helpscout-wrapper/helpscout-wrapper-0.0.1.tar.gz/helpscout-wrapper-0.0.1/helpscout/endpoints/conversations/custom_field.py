from typing import Dict, List, Union

from helpscout.endpoints.endpoint import Endpoint


class CustomField(Endpoint):
    """Conversation's custom field endpoint."""

    def update(
        self, conversation_id: int, fields: List[Dict[str, Union[str, int]]]
    ) -> int:
        """Update custom field

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/custom_fields/update/
        """
        response = self.base_put_request(
            f"{self.base_url}/{conversation_id}/fields", fields=fields
        )

        return self.process_result_with_status_code(response, 204)
