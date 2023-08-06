from typing import List

from helpscout.endpoints.endpoint import Endpoint


class Tag(Endpoint):
    """Conversation's tag endpoint."""

    def update(self, conversation_id: int, tags: List[str]) -> int:
        """Update tags.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/tags/update/
        """
        response = self.base_put_request(
            f"{self.base_url}/{conversation_id}/tags", tags=tags
        )

        return self.process_result_with_status_code(response, 204)
