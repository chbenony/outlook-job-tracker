import asyncio
import os

import httpx
from dotenv import load_dotenv

from auth import get_token

load_dotenv()
GRAPH = "https://graph.microsoft.com/v1.0"
JOB_FOLDER_ID = os.environ["JOB_FOLDER_ID"]
MAX_CONCURRENCY = 4


async def list_messages(client: httpx.AsyncClient, top: int = 25) -> list[dict]:
    response = await client.get(
        f"/me/mailFolders/{JOB_FOLDER_ID}/messages",
        params={
            "$select": "id,subject,from,receivedDateTime,bodyPreview",
            "$top": top,
            "$orderby": "receivedDateTime desc",
        },
    )
    response.raise_for_status()
    return response.json()["value"]


async def fetch_job_emails(top: int = 25) -> list[dict]:
    token = await asyncio.to_thread(get_token)
    async with httpx.AsyncClient(
        base_url=GRAPH,
        headers={
            "Authorization": f"Bearer {token}",
            "Prefer": 'outlook.body-content-type="text"',
        },
    ) as client:
        messages = await list_messages(client, top)
        sem = asyncio.Semaphore(MAX_CONCURRENCY)
        tasks = []
        async with asyncio.TaskGroup() as tg:
            for m in messages:
                task = tg.create_task(fetch_body(client, m["id"], sem))
                tasks.append(task)
        for message, task in zip(messages, tasks):
            message["body"] = task.result()

        return messages


async def fetch_body(
    client: httpx.AsyncClient, message_id: str, sem: asyncio.Semaphore
) -> str:
    async with sem:
        response = await client.get(
            f"/me/mailFolders/{JOB_FOLDER_ID}/messages/{message_id}",
            params={
                "$select": "body",
            },
        )
        response.raise_for_status()

    return response.json()["body"]["content"]


if __name__ == "__main__":
    emails = asyncio.run(fetch_job_emails(5))
    for email in emails:
        print(
            f"  {email['receivedDateTime']}"
            + f"  {email['from']['emailAddress']['address']} "
            + f"  {email['subject']}"
            + f"  ({len(email['body'])} chars)"
        )
