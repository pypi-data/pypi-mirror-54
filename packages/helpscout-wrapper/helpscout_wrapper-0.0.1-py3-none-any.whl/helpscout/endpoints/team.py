from typing import Dict

from helpscout.endpoints.endpoint import Endpoint


class Team(Endpoint):
    """Team endpoint."""

    def list(self, **kwargs) -> Dict:
        """Get all teams.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/teams/list-teams/
        """
        response = self.base_get_request(self.base_url, **kwargs)

        return self.process_get_result(response)

    def members(self, team_id: int, **kwargs) -> Dict:
        """Get all team members.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/teams/list-team-members/
        """
        response = self.base_get_request(f"{self.base_url}/{team_id}/members", **kwargs)

        return self.process_get_result(response)
