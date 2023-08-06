from typing import Any, Dict

from helpscout.endpoints.endpoint import Endpoint


class Thread(Endpoint):
    """Conversation's thread endpoint."""

    def list(self, conversation_id: int) -> Dict:
        """List all threads.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/list/
        """
        response = self.base_get_request(f"{self.base_url}/{conversation_id}/threads")

        return self.process_get_result(response)

    def update(
        self, conversation_id: int, thread_id: int, op: str, path: str, value: Any
    ) -> int:
        """Update thread.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/update/
        """
        response = self.base_patch_request(
            f"{self.base_url}/{conversation_id}/threads/{thread_id}",
            op=op,
            path=path,
            value=value,
        )

        return self.process_result_with_status_code(response, 204)

    def create_reply_thread(self, conversation_id: int, **kwargs) -> int:
        """Create reply thread.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/reply/
        """
        response = self.base_post_request(
            f"{self.base_url}/{conversation_id}/reply", **kwargs
        )

        return self.process_result_with_status_code(response, 201)

    def create_phone_thread(self, conversation_id: int, **kwargs) -> int:
        """Create phone thread.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/phone/
        """
        response = self.base_post_request(
            f"{self.base_url}/{conversation_id}/phones", **kwargs
        )

        return self.process_result_with_status_code(response, 201)

    def create_note(self, conversation_id: int, **kwargs) -> int:
        """Create note.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/note/
        """
        response = self.base_post_request(
            f"{self.base_url}/{conversation_id}/notes", **kwargs
        )

        return self.process_result_with_status_code(response, 201)

    def create_customer_thread(self, conversation_id: int, **kwargs) -> int:
        """Create customer thread.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/customer/
        """
        response = self.base_post_request(
            f"{self.base_url}/{conversation_id}/customer", **kwargs
        )

        return self.process_result_with_status_code(response, 201)

    def create_chat_thread(self, conversation_id: int, **kwargs) -> int:
        """Create chat thread.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/chat/
        """
        response = self.base_post_request(
            f"{self.base_url}/{conversation_id}/chats", **kwargs
        )

        return self.process_result_with_status_code(response, 201)
