from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Doc(Endpoint):
    """Doc report endpoint."""

    def overall_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get doc overall report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/docs/reports-docs-overall/
        """
        response = self.base_get_request(
            f"{self.base_url}/docs", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)
