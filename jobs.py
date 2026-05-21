from models.job import Job
from services.file_store import save_data
from services.scrapers.scraper_service import ScraperService

scraper_service = ScraperService()


async def run_job(payload: Job, job_id: str):
    data = scraper_service.process_scraper(
        payload.title, payload.parameters.get("sites", "")
    )

    save_data(data, job_id, payload.title)
