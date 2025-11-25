from .base import BaseRepository


class SubmissionRepository(BaseRepository):
    async def create_submission(self, user_id: int, task_id: int, judge0_submission_id: str):
        ...
