import asyncio
import datetime
import uuid

from fastapi import APIRouter, HTTPException

from core.state import background_tasks, tasks, tasks_lock
from models.job import JobRequest, JobResponse
from services.job_service import persist_tasks, run_job

jobs_routes = APIRouter(prefix="/jobs")


@jobs_routes.post(
    "/",
)
async def create_job(
    job: JobRequest,
):
    job_hash = str(uuid.uuid4())
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

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
            "description": job.description,
            "tags": job.tags,
            "date": now,
            "status": "created",
            "parameters": {"sites": job.sites, "profundidade": job.profundidade},
            "job_id": job_id,
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
        "date": now,
    }


@jobs_routes.get(
    "/",
    response_model=list[JobResponse],
)
async def get_jobs():
    async with tasks_lock:
        jobs = list(tasks.values())

    jobs.sort(
        key=lambda x: x["job_id"],
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


@jobs_routes.get("/{id}/export")
async def get_parameters(id: str):
    async with tasks_lock:
        job = tasks.get(id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"titulo": job["title"], "parameters": job["parameters"]}
