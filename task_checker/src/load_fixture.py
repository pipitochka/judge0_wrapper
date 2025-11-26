import asyncio
import json
import sys
import os
from pathlib import Path

from dotenv import load_dotenv

from persistent import Database
import persistent.models as models

num_batches = int(sys.argv[1]) if len(sys.argv) > 1 else 1

root_dir = Path(__file__).parent
load_dotenv(root_dir.parent.parent / ".env")

debug = os.environ.get("TASK_CHECKER_DEBUG", "false").lower() in ("1", "t", "true", "y")
# db_host = os.environ.get()
# db_port = os.environ.get()
# db_user = os.environ.get()
# db_pwd = os.environ.get()
db_name = os.environ.get("DB_NAME")

if debug:
    db_url = f"sqlite+aiosqlite:///./{db_name}.db"
else:
    db_url = ""


async def load_batch(path: Path, session):
    with open(path, "r") as f:
        data = json.load(f)

    for task in data:
        t_model = models.Task(
            title=task["id"],
            content=task["description"],
            type=models.TaskType.Algorithm
        )
        for tc in task["test_cases"]:
            t_model.test_cases.append(models.TestCase(stdin=tc["stdin"], expected=tc["expected"]))
        session.add(t_model)
    await session.commit()


async def main():
    db = Database(db_url)
    await db.check_and_create_tables()

    for i in range(num_batches):
        async with db.session() as s:
            await load_batch(root_dir / "fixtures" / f"problems_batch_{i + 1}.json", s)
            print(f"Fixture {i + 1} loaded")


asyncio.run(main())
