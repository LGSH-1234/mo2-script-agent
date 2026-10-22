from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Scene(Contract):
    id: str = Field(min_length=1)
    location: str = Field(min_length=1)
    action: str = Field(min_length=1)
    dialogue: str = ""


class Script(Contract):
    title: str = Field(min_length=1)
    synopsis: str = Field(min_length=1)
    scenes: list[Scene] = Field(min_length=1, max_length=30)


class Shot(Contract):
    id: str = ""
    source_scene: str = Field(min_length=1)
    title: str = Field(min_length=1, max_length=100)
    framing: str = Field(min_length=1)
    camera: str = Field(min_length=1)
    duration: float = Field(ge=1, le=30)
    action: str = Field(min_length=1)
    dialogue: str = ""
    start_state: str = Field(min_length=1)
    end_state: str = Field(min_length=1)
    prompt: str = ""
    reference_ids: list[str] = Field(default_factory=list)


class Board(Contract):
    shots: list[Shot] = Field(min_length=1, max_length=60)


class PromptItem(Contract):
    id: str
    prompt: str = Field(min_length=1)


class PromptResult(Contract):
    prompts: list[PromptItem] = Field(min_length=1)


class NewProject(Contract):
    title: str = "未命名项目"
    brief: str = Field(default="", max_length=50000)
    duration: int = Field(default=30, ge=5, le=300)
    ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    style: str = "写实电影感，克制、自然光"


class VersionRequest(Contract):
    version: int


class SaveScript(VersionRequest):
    script: Script


class SaveBoard(VersionRequest):
    shots: list[Shot] = Field(min_length=1, max_length=60)


class RevisionRequest(VersionRequest):
    shot_id: str
    instruction: str = Field(min_length=1, max_length=4000)


class ApplyRevision(VersionRequest):
    proposal_id: str


class VideoRequest(VersionRequest):
    shot_id: str
    simulate_failure: bool = False


class RetryRequest(Contract):
    pass
