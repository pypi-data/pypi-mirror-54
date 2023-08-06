from typing import Any, Dict

from helpscout.endpoints.conversations.attachment import Attachment
from helpscout.endpoints.conversations.custom_field import CustomField
from helpscout.endpoints.conversations.tag import Tag
from helpscout.endpoints.conversations.thread import Thread
from helpscout.endpoints.endpoint import Endpoint


class Conversation(Endpoint):
    """Conversation endpoint."""

    def list(self, **kwargs) -> Dict:
        """List all conversations.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/list/
        """
        response = self.base_get_request(self.base_url, **kwargs)

        return self.process_get_result(response)

    def get(self, conversation_id: int, **kwargs) -> Dict:
        """Get conversation by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/get/
        """
        response = self.base_get_request(f"{self.base_url}/{conversation_id}", **kwargs)

        return self.process_get_result(response)

    def update(
        self, conversation_id: int, op: str, path: str, value: Any = None
    ) -> int:
        """Update conversation by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/update/
        """
        response = self.base_patch_request(
            f"{self.base_url}/{conversation_id}", op=op, path=path, value=value
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, conversation_id: int) -> int:
        """Delete conversation by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/delete/
        """
        response = self.base_delete_request(f"{self.base_url}/{conversation_id}")

        return self.process_result_with_status_code(response, 204)

    def create(self, **kwargs) -> int:
        """Create new conversation.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/delete/
        """
        response = self.base_post_request(self.base_url, **kwargs)

        return self.process_result_with_status_code(response, 201)

    @property
    def attachment(self) -> Attachment:
        """Conversation's attachement endpoint."""
        return Attachment(client=self.client, base_url=self.base_url)

    @property
    def custom_field(self) -> CustomField:
        """Conversation's custom field endpoint."""
        return CustomField(client=self.client, base_url=self.base_url)

    @property
    def tag(self) -> Tag:
        """Conversation's tag endpoint."""
        return Tag(client=self.client, base_url=self.base_url)

    @property
    def thread(self) -> Thread:
        """Conversation's thread endpoint."""
        return Thread(client=self.client, base_url=self.base_url)
