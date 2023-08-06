from typing import Dict

from helpscout.endpoints.customers.address import Address
from helpscout.endpoints.customers.chat_handler import ChatHandler
from helpscout.endpoints.customers.email import Email
from helpscout.endpoints.customers.phone import Phone
from helpscout.endpoints.customers.social_profile import SocialProfile
from helpscout.endpoints.customers.website import Website
from helpscout.endpoints.endpoint import Endpoint


class Customer(Endpoint):
    """Customer endpoint."""

    def list(self, **kwargs) -> Dict:
        """List all customers.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/list/
        """
        response = self.base_get_request(self.base_url, **kwargs)

        return self.process_get_result(response)

    def get(self, customer_id: int, **kwargs) -> Dict:
        """Get customer by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/get/
        """
        response = self.base_get_request(f"{self.base_url}/{customer_id}", **kwargs)

        return self.process_get_result(response)

    def create(self, first_name: str, **kwargs) -> int:
        """Create new customer.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/create/
        """
        response = self.base_post_request(self.base_url, firstName=first_name, **kwargs)

        return self.process_result_with_status_code(response, 201)

    def update(self, customer_id: int, first_name: str, **kwargs) -> int:
        """Update customer by id.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/update/
        """
        response = self.base_put_request(
            f"{self.base_url}/{customer_id}", firstName=first_name, **kwargs
        )

        return self.process_result_with_status_code(response, 204)

    @property
    def address(self) -> Address:
        """Customer's address endpoint."""
        return Address(client=self.client, base_url=self.base_url)

    @property
    def chat_handler(self) -> ChatHandler:
        """Customer's chat handler endpoint."""
        return ChatHandler(client=self.client, base_url=self.base_url)

    @property
    def email(self) -> Email:
        """Customer's email endpoint."""
        return Email(client=self.client, base_url=self.base_url)

    @property
    def phone(self) -> Phone:
        """Customer's phone endpoint."""
        return Phone(client=self.client, base_url=self.base_url)

    @property
    def social_profile(self) -> SocialProfile:
        """Customer's social profile endpoint."""
        return SocialProfile(client=self.client, base_url=self.base_url)

    @property
    def website(self) -> Website:
        """Customer's website endpoint."""
        return Website(client=self.client, base_url=self.base_url)
