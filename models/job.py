from pydantic import BaseModel


class Job(BaseModel):
    title: str
    description: str
    tags: list[str]
    parameters: dict[str, any]
    status: str
