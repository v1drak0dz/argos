import asyncio
from dataclasses import asdict

from core.state import job_semaphore, scraper_service, tasks, tasks_lock
from services.task_storage import save_tasks_snapshot


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


async def persist_tasks():
    async with tasks_lock:
        snapshot = dict(tasks)

    await asyncio.to_thread(
        save_tasks_snapshot,
        snapshot,
    )
