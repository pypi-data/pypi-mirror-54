from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Company(Endpoint):
    """Company report endpoint."""

    def overall_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get company overall report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/company/reports-company-overall/
        """
        response = self.base_get_request(
            f"{self.base_url}/company", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def customers_helped(self, start: str, end: str, **kwargs) -> Dict:
        """Get company customers helped.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/company/reports-company-customers-helped/
        """
        response = self.base_get_request(
            f"{self.base_url}/company/customers-helped", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def drilldown(self, start: str, end: str, range_: str, **kwargs) -> Dict:
        """Get company drilldown.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/company/reports-company-drilldown/
        """
        response = self.base_get_request(
            f"{self.base_url}/company/drilldown",
            start=start,
            end=end,
            range=range_,
            **kwargs,
        )

        return self.process_get_result(response)
