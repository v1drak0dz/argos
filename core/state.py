import asyncio
from typing import Any

from services.scrapers.scraper_service import ScraperService

tasks: dict[str, dict[str, Any]] = {}
tasks_lock = asyncio.Lock()
background_tasks: set[asyncio.Task] = set()
job_semaphore = asyncio.Semaphore(2)
scraper_service = ScraperService()
