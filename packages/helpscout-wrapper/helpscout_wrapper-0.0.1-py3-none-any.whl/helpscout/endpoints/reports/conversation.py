from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Conversation(Endpoint):
    """Conversation report endpoint."""

    def overall_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get conversation overall report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-overall/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def volumes_by_channel(self, start: str, end: str, **kwargs) -> Dict:
        """Get conversation volumes by channel.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-volume-by-channel/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations/volume-by-channel",
            start=start,
            end=end,
            **kwargs,
        )

        return self.process_get_result(response)

    def busiest_time_of_day(self, start: str, end: str, **kwargs) -> Dict:
        """Get conversation busiest time of day.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-busy-times/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations/busy-times", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def drilldown(self, start: str, end: str, **kwargs) -> Dict:
        """Get conversation drilldown.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-drilldown/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations/drilldown", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def drilldown_by_field(
        self, start: str, end: str, field: str, fieldid: int, **kwargs
    ) -> Dict:
        """Get conversation drilldown by field.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-field-drilldown/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations/fields-drilldown",
            start=start,
            end=end,
            field=field,
            fieldid=fieldid,
            **kwargs,
        )

        return self.process_get_result(response)

    def new(self, start: str, end: str, **kwargs) -> Dict:
        """Get new conversations.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-new/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations/new", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def new_drilldown(self, start: str, end: str, **kwargs) -> Dict:
        """Get new conversations drilldown.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-new-drilldown/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations/new-drilldown",
            start=start,
            end=end,
            **kwargs,
        )

        return self.process_get_result(response)

    def received_messages(self, start: str, end: str, **kwargs) -> Dict:
        """Get conversation received messages statistics.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/conversations/reports-conversations-received-messages/
        """
        response = self.base_get_request(
            f"{self.base_url}/conversations/received-messages",
            start=start,
            end=end,
            **kwargs,
        )

        return self.process_get_result(response)
