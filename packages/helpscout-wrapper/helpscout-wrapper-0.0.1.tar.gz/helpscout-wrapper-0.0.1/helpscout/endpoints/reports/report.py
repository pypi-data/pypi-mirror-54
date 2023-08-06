from typing import Dict

from helpscout.endpoints.endpoint import Endpoint
from helpscout.endpoints.reports.company import Company
from helpscout.endpoints.reports.conversation import Conversation
from helpscout.endpoints.reports.doc import Doc
from helpscout.endpoints.reports.happiness import Happiness
from helpscout.endpoints.reports.productivity import Productivity
from helpscout.endpoints.reports.user import User


class Report(Endpoint):
    """Report endpoint."""

    def chat_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get chat report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/chat/
        """
        response = self.base_get_request(
            f"{self.base_url}/chat", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def email_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get email report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/email/
        """
        response = self.base_get_request(
            f"{self.base_url}/email", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    def phone_report(self, start: str, end: str, **kwargs) -> Dict:
        """Get phone report.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/reports/phone/
        """
        response = self.base_get_request(
            f"{self.base_url}/phone", start=start, end=end, **kwargs
        )

        return self.process_get_result(response)

    @property
    def company(self) -> Company:
        """Company report endpoint."""
        return Company(client=self.client, base_url=self.base_url)

    @property
    def conversation(self) -> Conversation:
        """Conversation report endpoint."""
        return Conversation(client=self.client, base_url=self.base_url)

    @property
    def doc(self) -> Doc:
        """Doc report endpoint."""
        return Doc(client=self.client, base_url=self.base_url)

    @property
    def happiness(self) -> Happiness:
        """Happiness report endpoint."""
        return Happiness(client=self.client, base_url=self.base_url)

    @property
    def productivity(self) -> Productivity:
        """Productivity report endpoint."""
        return Productivity(client=self.client, base_url=self.base_url)

    @property
    def user(self) -> User:
        """User report endpoint."""
        return User(client=self.client, base_url=self.base_url)
