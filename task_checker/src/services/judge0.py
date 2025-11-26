import httpx

from repositories import TaskRepository, TestCaseRepository, SubmissionRepository
from schemas import SubmissionJudge0Schema, CreateSubmissionSchema, Judge0SubmissionSchema, SubmissionGeneralSchema


class Judge0Service:
    def __init__(
            self,
            testcases_repo: TestCaseRepository,
            submission_repo: SubmissionRepository,
            url: str, header: str, token: str
    ):
        if url[-1] == "/":
            url = url[:-1]
        self._url = url
        self._client = httpx.AsyncClient(headers={header: token})
        self._tc_repo = testcases_repo
        self._sm_repo = submission_repo

    async def get_system_information(self) -> dict:
        resp = await self._client.get(f"{self._url}/system_info")
        return resp.json()

    async def get_available_languages(self) -> list[dict]:
        resp = await self._client.get(f"{self._url}/languages")
        return resp.json()

    async def create_submission(self, submission: CreateSubmissionSchema, open_tests: bool) -> SubmissionGeneralSchema:
        test_cases = await self._tc_repo.get_testcases(submission.task_id, open_tests)

        submissions = [
            dict(Judge0SubmissionSchema.from_testcase(tc, submission))
            for tc in test_cases
        ]
        resp = await self._client.post(
            f"{self._url}/submissions/batch",
            json={
                "submissions": submissions
            }
        )
        submission = await self._sm_repo.create_submission("0", submission.task_id, submission.answer)
        tokens = resp.json()

        await self._sm_repo.create_empty_submission_results(
            submission.id,
            [tc.id for tc in test_cases],
            [entry["token"] for entry in tokens]
        )
        return submission

    async def create_test_submission(self, submission: CreateSubmissionSchema) -> SubmissionGeneralSchema:
        resp = await self._client.post(
            f"{self._url}/submissions",
            json=dict(Judge0SubmissionSchema.from_submission_schema(submission))
        )

        token = resp.json()["token"]

        submission = await self._sm_repo.create_submission("0", 0, submission.answer)
        await self._sm_repo.create_empty_submission_results(submission.id, [0], [token])

        return submission
