from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Tag(Endpoint):
    """Tag endpoint."""

    def list(self, **kwargs) -> Dict:
        """Get all tags.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/tags/list/
        """
        response = self.base_get_request(self.base_url, **kwargs)

        return self.process_get_result(response)
