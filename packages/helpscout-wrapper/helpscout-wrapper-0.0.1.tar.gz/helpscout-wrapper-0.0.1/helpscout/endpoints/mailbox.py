from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Mailbox(Endpoint):
    """Mailbox endpoint."""

    def list(self) -> Dict:
        """Get all mailboxes.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/mailboxes/list/
        """
        response = self.base_get_request(self.base_url)

        return self.process_get_result(response)

    def get(self, mailbox_id: int) -> Dict:
        """Get mailbox by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/mailboxes/get/
        """
        response = self.base_get_request(f"{self.base_url}/{mailbox_id}")

        return self.process_get_result(response)

    def mailbox_fields(self, mailbox_id: int) -> Dict:
        """Get mailbox fields by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/mailboxes/mailbox-fields/
        """
        response = self.base_get_request(f"{self.base_url}/{mailbox_id}/fields")

        return self.process_get_result(response)

    def mailbox_folders(self, mailbox_id: int) -> Dict:
        """Get mailbox folders by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/mailboxes/mailbox-folders/
        """
        response = self.base_get_request(f"{self.base_url}/{mailbox_id}/folders")

        return self.process_get_result(response)
