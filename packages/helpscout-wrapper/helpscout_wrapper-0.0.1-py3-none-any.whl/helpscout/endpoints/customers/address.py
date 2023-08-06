from typing import Dict, List

from helpscout.endpoints.endpoint import Endpoint


class Address(Endpoint):
    """Customer's address endpoint."""

    def get(self, customer_id: int) -> Dict:
        """Get customer's address.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/address/get/
        """
        response = self.base_get_request(f"{self.base_url}/{customer_id}/address")

        return self.process_get_result(response)

    def create(
        self,
        customer_id: int,
        city: str,
        state: str,
        postal_code: str,
        country: str,
        lines: List[str],
    ) -> int:
        """Create customer's address.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/address/create/
        """
        response = self.base_post_request(
            f"{self.base_url}/{customer_id}/address",
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            lines=lines,
        )

        return self.process_result_with_status_code(response, 201)

    def update(
        self,
        customer_id: int,
        city: str,
        state: str,
        postal_code: str,
        country: str,
        lines: List[str],
    ) -> int:
        """Update customer's address.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/address/update/
        """
        response = self.base_put_request(
            f"{self.base_url}/{customer_id}/address",
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            lines=lines,
        )

        return self.process_result_with_status_code(response, 204)

    def delete(self, customer_id: int) -> int:
        """Delete customer's address.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/customers/address/delete/
        """
        response = self.base_delete_request(f"{self.base_url}/{customer_id}/address")

        return self.process_result_with_status_code(response, 204)
