from typing import Dict, List

from helpscout.endpoints.endpoint import Endpoint


class Workflow(Endpoint):
    """Workflow endpoint."""

    def list(self, **kwargs) -> Dict:
        """Get all workflows.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/workflows/list/
        """
        response = self.base_get_request(self.base_url, **kwargs)

        return self.process_get_result(response)

    def update_status(self, workflow_id: int, op: str, value: str, path: str) -> int:
        """Update workflow status.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/workflows/update/
        """
        response = self.base_patch_request(
            f"{self.base_url}/{workflow_id}", op=op, value=value, path=path
        )

        return self.process_result_with_status_code(response, 204)

    def run_manual(self, workflow_id: int, conversation_ids: List[int]) -> int:
        """Run manual workflow.

        Doc page: https://developer.helpscout.com/mailbox-api/endpoints/workflows/run/
        """
        response = self.base_post_request(
            f"{self.base_url}/{workflow_id}/run", conversation_ids=conversation_ids
        )

        return self.process_result_with_status_code(response, 204)
