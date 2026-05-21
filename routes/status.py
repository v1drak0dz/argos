from fastapi import APIRouter, HTTPException

from core.state import tasks, tasks_lock

status_routes = APIRouter(prefix="/status")


@status_routes.get(
    "/{id}",
)
async def get_job_status(
    id: str,
):
    async with tasks_lock:
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


@status_routes.get(
    "/completed/{id}",
)
async def is_job_done(
    id: str,
):
    async with tasks_lock:
        job = tasks.get(id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {"completed": (job["status"] == "completed")}
