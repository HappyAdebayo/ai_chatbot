
from pydantic import BaseModel, Field
from typing import Literal, Optional


class Task(BaseModel):
    title: str = Field(description="The title of the task")

    description: Optional[str] = Field(
        None,
        description="A detailed description of the task"
    )

    date: Optional[str] = Field(
        None,
        description="Date in YYYY-MM-DD format"
    )

    time: Optional[str] = Field(
        None,
        description="Time in HH:MM format"
    )

    priority: Literal["low", "medium", "high"] = "medium"

    category: Literal[
        "work",
        "learning",
        "personal",
        "health",
        "other"
    ] = "other"

    status: Literal[
        "pending",
        "in_progress",
        "completed"
    ] = "pending"

class TaskFilters(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None

    category: Optional[
        Literal["work", "learning", "personal", "health", "other"]
    ] = None

    status: Optional[
        Literal["pending", "in_progress", "completed"]
    ] = None

    created_at: Optional[str] = None
  
class TaskUpdate(BaseModel):
    title: str = Field(
        description="Title of the existing task to update"
    )

    new_title: Optional[str] = None

    description: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None

    category: Optional[
        Literal["work", "learning", "personal", "health", "other"]
    ] = None

    status: Optional[
        Literal["pending", "in_progress", "completed"]
    ] = None

class AssistantResponse(BaseModel):
    action: Literal[
        "create_task",
        "update_task",
        "delete_task",
        "delete_all_tasks",
        "list_tasks",
        "chat",
        "clarify",
        "complete_task",
        "complete_all_tasks",
    ]
    confirmation: Optional[Literal[
        "confirmed",
        "cancelled",
        "unclear"
    ]] = None

    task: Optional[Task] = None
    task_update: Optional[TaskUpdate] = None
    filters: Optional[TaskFilters] = None
    message: str
