from pydantic import BaseModel


class JobRequest(BaseModel):
    title: str
    description: str
    tags: str
    sites: list[str]
    profundidade: int = 3


class JobResponse(BaseModel):
    title: str
    description: str
    tags: str
    date: str
    status: str
    parameters: dict
    job_id: int
    job_hash: str
    data: list
    error: str | None = None
