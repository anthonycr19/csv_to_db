from pydantic import BaseModel
from typing import List


class Job(BaseModel):
    marketing_assistant: str


class JobCreate(Job):
    pass


class JobResponse(Job):
    id: int

    class Config:
        from_attributes = True


class BatchJobCreate(BaseModel):
    jobs: List[JobCreate]
