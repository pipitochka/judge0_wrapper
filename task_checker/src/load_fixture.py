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
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)

    for task in data:
        t_model = models.Task(
            title=task["title"],
            content=task["description"],
            type=models.TaskType.Algorithm
        )
        for tc in task["hidden_testcases"]:
            t_model.test_cases.append(models.TestCase(
                stdin=tc["input"],
                expected=tc["output"],
                memory_limit=task.get("memory_limit", 32) * 1024,
                time_limit=task.get("time_limit", 2),
                is_hidden=True
            ))
        for tc in task["open_testcases"]:
            t_model.test_cases.append(models.TestCase(
                stdin=tc["input"],
                expected=tc["output"],
                memory_limit=task.get("memory_limit", 32) * 1024,
                time_limit=task.get("time_limit", 2),
                is_hidden=False
            ))

        session.add(t_model)
    await session.commit()


async def main():
    db = Database(db_url)
    await db.check_and_create_tables()

    async with db.session() as s:
        await load_batch(root_dir / "fixtures" / "dump1.json", s)
        await load_batch(root_dir / "fixtures" / "dump2.json", s)
        print(f"Fixtures loaded")


asyncio.run(main())
