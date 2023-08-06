from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Productivity(Endpoint):
    """Productivity report endpoint."""

    def overall_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get productivity overall report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/productivity/reports-productivity-overall/
        """
        response = self.base_get_request(
            f"{self.base_url}/productivity", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def first_response_time(self, start: str, end: str, **kwargs) -> Dict:
        """Get productivity first response time.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/productivity/reports-productivity-first-response-time/
        """
        response = self.base_get_request(
            f"{self.base_url}/productivity/first-response-time",
            start=start,
            end=end,
            **kwargs,
        )

        return self.process_get_result(response)

    def replies_sent(self, start: str, end: str, **kwargs) -> Dict:
        """Get productivity replies sent.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/productivity/reports-productivity-replies-sent/
        """
        response = self.base_get_request(
            f"{self.base_url}/productivity/replies-sent", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def resolution_time(self, start: str, end: str, **kwargs) -> Dict:
        """Get productivity resolution time.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/productivity/reports-productivity-resolution-time/
        """
        response = self.base_get_request(
            f"{self.base_url}/productivity/resolution-time",
            start=start,
            end=end,
            **kwargs,
        )

        return self.process_get_result(response)

    def resolved(self, start: str, end: str, **kwargs) -> Dict:
        """Get productivity resolved.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/productivity/reports-productivity-resolved/
        """
        response = self.base_get_request(
            f"{self.base_url}/productivity/resolved", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def response_time(self, start: str, end: str, **kwargs) -> Dict:
        """Get productivity response time.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/productivity/reports-productivity-respose-time/
        """
        response = self.base_get_request(
            f"{self.base_url}/productivity/response-time",
            start=start,
            end=end,
            **kwargs,
        )

        return self.process_get_result(response)
