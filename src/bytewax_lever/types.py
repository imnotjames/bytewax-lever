from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Sequence


class PostingState(Enum):
    PUBLISHED = "published"
    INTERNAL = "internal"
    CLOSED = "closed"
    DRAFT = "draft"
    PENDING = "pending"
    REJECTED = "rejected"


class WorkplaceType(Enum):
    UNSPECIFIED = "unspecified"
    ONSITE = "on-site"
    REMOTE = "remote"
    HYBRID = "hybrid"


@dataclass
class RichTextContent:
    text: str

    html: str


class SalaryInterval(Enum):
    PER_YEAR = "per-year-salary"
    PER_MONTH = "per-month-salary"
    SEMI_MONTH = "semi-month-salary"
    BI_MONTH = "bi-month-salary"
    BI_WEEK = "bi-week-salary"
    PER_WEEK = "per-week-salary"
    PER_DAY = "per-day-wage"
    PER_HOUR = "per-hour-wage"
    ONE_TIME = "one-time"


@dataclass
class Salary:
    minimum: int
    maximum: int
    currency: str
    interval: SalaryInterval


@dataclass
class Posting:
    id: str
    created_at: datetime
    updated_at: datetime
    state: PostingState
    distribution_channels: list[str]
    tags: list[str]
    country: str
    location: str
    commitment: str
    workplace_type: WorkplaceType
    apply_url: str | None
    posting_url: str | None
    department: str | None
    team: str
    title: str
    description: RichTextContent
    lists: Sequence[RichTextContent]
    closing: RichTextContent
    salary: Salary | None
