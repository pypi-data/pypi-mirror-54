from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Happiness(Endpoint):
    """Happiness report endpoint."""

    def overall_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get happiness overall report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/happiness/reports-happiness-overall/
        """
        response = self.base_get_request(
            f"{self.base_url}/happiness", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def ratings(self, start: str, end: str, **kwargs) -> Dict:
        """Get happiness ratings report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/happiness/reports-happiness-ratings/
        """
        response = self.base_get_request(
            f"{self.base_url}/happiness/ratings", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)
