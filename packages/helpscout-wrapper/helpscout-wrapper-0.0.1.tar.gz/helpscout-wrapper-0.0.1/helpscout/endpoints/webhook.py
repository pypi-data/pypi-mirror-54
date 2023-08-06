from typing import Dict, List

from helpscout.endpoints.endpoint import Endpoint


class Webhook(Endpoint):
    """Webhook endpoint."""

    def list(self) -> Dict:
        """Get all webhooks.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/webhooks/list/
        """
        response = self.base_get_request(self.base_url)

        return self.process_get_result(response)

    def get(self, webhook_id: int) -> Dict:
        """Get webhook by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/webhooks/get/
        """
        response = self.base_get_request(f"{self.base_url}/{webhook_id}")

        return self.process_get_result(response)

    def create(
        self, url: str, events: List[str], secret: str, notification: bool = False
    ) -> int:
        """Create new webhook.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/webhooks/create/
        """
        response = self.base_post_request(
            f"{self.base_url}",
            url=url,
            events=events,
            notification=notification,
            secret=secret,
        )

        return self.process_result_with_status_code(response, 201)

    def update(
        self,
        webhook_id: int,
        url: str,
        events: List[str],
        secret: str,
        notification: bool = False,
    ) -> int:
        """Update webhook.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/webhooks/update/
        """
        response = self.base_put_request(
            f"{self.base_url}/{webhook_id}",
            url=url,
            events=events,
            notification=notification,
            secret=secret,
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, webhook_id: int) -> int:
        """Delete webhook.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/webhooks/delete/
        """
        response = self.base_delete_request(f"{self.base_url}/{webhook_id}")

        return self.process_result_with_status_code(response, 204)
