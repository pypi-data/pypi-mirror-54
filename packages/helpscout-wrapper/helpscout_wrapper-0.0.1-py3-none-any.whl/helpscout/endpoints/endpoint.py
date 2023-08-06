from typing import Dict

import requests

import helpscout.exceptions as exc


class Endpoint:
    """Base endpoint class."""

    def __init__(self, client, base_url: str):
        """
        Params:
            client: helpscout client with credentials
            base_url: url for endpoint
        """
        self.client = client
        self.base_url = base_url

    def process_get_result(self, response: requests.Response) -> Dict:
        """Process response with coresponding status code."""
        if response.status_code == 400:
            raise exc.BadRequestException
        elif response.status_code == 401:
            raise exc.NotAuthorizedException
        elif response.status_code == 404:
            return {}

        return response.json()

    def process_result_with_status_code(self, response: requests.Response, status_code):
        """Process result with given status code.

        Raise exception if response status code does't match provided one
        """
        if response.status_code != status_code:
            raise exc.BadRequestException

        return response.status_code

    def base_get_request(self, base_url: str, **kwargs) -> requests.Response:
        """Base get request."""
        return requests.get(
            base_url,
            headers={"Authorization": f"Bearer {self.client.access_token}"},
            params={**kwargs},
        )

    def base_put_request(self, base_url: str, **kwargs) -> requests.Response:
        """Base put request."""
        return requests.put(
            base_url,
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
                "Content-Type": "application/json; charset=UTF-8",
            },
            json={**kwargs},
        )

    def base_patch_request(self, base_url: str, **kwargs) -> requests.Response:
        """Base patch request."""
        return requests.patch(
            base_url,
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
                "Content-Type": "application/json; charset=UTF-8",
            },
            json={**kwargs},
        )

    def base_post_request(self, base_url: str, **kwargs) -> requests.Response:
        """Base post request."""
        return requests.post(
            base_url,
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
                "Content-Type": "application/json; charset=UTF-8",
            },
            json={**kwargs},
        )

    def base_delete_request(self, base_url: str, **kwargs) -> requests.Response:
        """Base delete request."""
        return requests.delete(
            base_url, headers={"Authorization": f"Bearer {self.client.access_token}"}
        )
