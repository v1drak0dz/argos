import asyncio
import json
import os
import uuid
from dataclasses import asdict
from typing import Any

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.job import JobRequest, JobResponse
from services.scrapers.scraper_service import ScraperService

storage_file = "job_history.json"
tasks: dict[str, dict[str, Any]] = {}
tasks_lock = asyncio.Lock()
background_tasks: set[asyncio.Task] = set()
job_semaphore = asyncio.Semaphore(2)
scraper_service = ScraperService()


def load_tasks():
    global tasks

    if not os.path.exists(storage_file):
        tasks = {}
        return

    try:
        with open(
            storage_file,
            "r",
            encoding="utf-8",
        ) as f:
            tasks = json.load(f)

    except (
        json.JSONDecodeError,
        OSError,
    ):
        tasks = {}


def save_tasks_snapshot(
    snapshot: dict,
):
    temp_file = f"{storage_file}.tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            snapshot,
            f,
            ensure_ascii=False,
            indent=4,
        )

    os.replace(
        temp_file,
        storage_file,
    )


async def persist_tasks():
    async with tasks_lock:
        snapshot = dict(tasks)

    await asyncio.to_thread(
        save_tasks_snapshot,
        snapshot,
    )


load_tasks()

app = FastAPI()

jobs_routes = APIRouter(prefix="/jobs")

status_routes = APIRouter(prefix="/status")

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):
    return templates.TemplateResponse(
        request,
        name="index.html",
    )


async def update_job(
    job: dict,
    **kwargs,
):
    async with tasks_lock:
        job.update(kwargs)

    await persist_tasks()


async def run_job(
    title: str,
    sites: list[str],
    profundidade: int,
    job: dict,
):
    async with job_semaphore:
        try:
            await update_job(
                job,
                status="processing",
            )

            data = await asyncio.to_thread(
                scraper_service.process_scraper, title, sites, profundidade
            )

            serialized_data = [asdict(item) for item in data]

            await update_job(
                job,
                status="completed",
                data=serialized_data,
            )

            return serialized_data

        except Exception as ex:
            await update_job(
                job,
                status="failed",
                error=str(ex),
            )

            raise


@jobs_routes.post(
    "/",
)
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
            "title": job.title,
            "status": "created",
            "parameters": {"sites": job.sites, "profundidade": job.profundidade},
            "id": job_id,
            "job_hash": job_hash,
            "data": [],
            "error": None,
        }

        created_job = tasks[job_hash]

    await persist_tasks()

    task = asyncio.create_task(
        run_job(
            job.title,
            job.sites,
            job.profundidade,
            created_job,
        )
    )

    background_tasks.add(task)

    task.add_done_callback(
        background_tasks.discard,
    )

    return {
        "status": "created",
        "job_hash": job_hash,
        "job_id": job_id,
        "data": [],
    }


@jobs_routes.get(
    "/",
    response_model=list[JobResponse],
)
async def get_jobs():
    async with tasks_lock:
        jobs = list(tasks.values())

    jobs.sort(
        key=lambda x: x["id"],
        reverse=True,
    )

    return jobs


@jobs_routes.get(
    "/{id}",
    response_model=JobResponse,
)
async def get_job(
    id: str,
):
    async with tasks_lock:
        job = tasks.get(id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job





app.include_router(status_routes)

app.include_router(jobs_routes)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=8000,
        reload=True,
    )
