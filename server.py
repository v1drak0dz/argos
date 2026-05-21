import asyncio
import json
import os
import uuid

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from services.scrapers.scraper_service import ScraperService

storage_file = "job_history.json"

tasks: dict = {}

tasks_lock = asyncio.Lock()

background_tasks = set()

if os.path.exists(storage_file):
    with open(
        storage_file,
        "r",
        encoding="utf-8",
    ) as r:
        try:
            tasks = json.load(r)

        except json.JSONDecodeError:
            tasks = {}


def save_tasks():

    with open(
        storage_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            tasks,
            f,
            ensure_ascii=False,
            indent=4,
        )


app = FastAPI()

jobs_routes = APIRouter(prefix="/jobs")

status_routes = APIRouter(prefix="/status")


class JobRequest(BaseModel):
    title: str
    sites: list[str]


async def persist_tasks():
    await asyncio.to_thread(save_tasks)


async def run_job(
    title: str,
    sites: list[str],
    job: dict,
):

    async with tasks_lock:
        job["status"] = "processing"

        await persist_tasks()

    scraper_service = ScraperService()

    try:
        data = await asyncio.to_thread(
            scraper_service.process_scraper,
            title,
            sites,
        )

        async with tasks_lock:
            job["status"] = "completed"

            job["data"] = data

            await persist_tasks()

        return data

    except Exception as ex:
        async with tasks_lock:
            job["status"] = "failed"

            job["error"] = str(ex)

            await persist_tasks()

        raise


@jobs_routes.post("/")
async def create_job(
    job: JobRequest,
):

    job_hash = str(uuid.uuid4())

    async with tasks_lock:
        job_id = (
            max(
                [t["id"] for t in tasks.values()],
                default=0,
            )
            + 1
        )

        tasks[job_hash] = {
            "status": "created",
            "parameters": {
                "sites": job.sites,
            },
            "title": job.title,
            "id": job_id,
            "job_hash": job_hash,
            "data": [],
        }

        await persist_tasks()

    task = asyncio.create_task(
        run_job(
            job.title,
            job.sites,
            tasks[job_hash],
        )
    )

    background_tasks.add(task)

    task.add_done_callback(background_tasks.discard)

    return {
        "status": "created",
        "job_id": job_hash,
        "id": job_id,
        "data": [],
    }


@jobs_routes.get("/{id}")
async def get_job(id: str):

    job = tasks.get(id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job


@status_routes.get("/{id}")
async def get_job_status(
    id: str,
):

    job = tasks.get(id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "status": job["status"],
        "title": job["title"],
    }


@status_routes.get("/completed/{id}")
async def is_job_done(
    id: str,
):

    job = tasks.get(id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {"completed": (job["status"] == "completed")}


app.include_router(status_routes)

app.include_router(jobs_routes)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=8000,
        reload=True,
    )
