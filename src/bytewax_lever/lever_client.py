from datetime import datetime
import html
from typing import Any, Sequence
from urllib.parse import urljoin
from logging import getLogger

import requests

from .html_to_text import html_to_text
from .types import (
    Posting,
    RichTextContent,
    SalaryInterval,
    Salary,
    WorkplaceType,
    PostingState,
)


logger = getLogger(__name__)


DEFAULT_BASE_URL = "https://api.lever.co/v1/"


class LeverClient:
    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
    ):
        self._api_key = api_key
        self._base_url = base_url or DEFAULT_BASE_URL

    def _get(self, path: str, params: dict[str, Any] | None = None):
        response = requests.get(
            urljoin(self._base_url, path),
            auth=(self._api_key, ""),
            params=params,
        )

        if not response.ok:
            raise ValueError("something went wrong")

        return response.json()

    @staticmethod
    def _parse_lever_list(data: dict) -> RichTextContent:
        """Try to interpret lever lists as Rich Text Content"""

        title = data["text"]
        content_html = data["content"]

        content_text = html_to_text(content_html.replace("</li>", "</li>\n")).strip()

        return RichTextContent(
            f"{title}\n\n{content_text}",
            f"<h2>{html.escape(title)}</h2><ul>{content_html}</ul>",
        )

    @staticmethod
    def _parse_lever_posting(data) -> Posting:
        urls = data["urls"]

        if "salaryRange" in data:
            salary = Salary(
                int(data["salaryRange"]["min"]),
                int(data["salaryRange"]["max"]),
                data["salaryRange"]["currency"],
                SalaryInterval(data["salaryRange"]["interval"]),
            )
        else:
            salary = None

        description = RichTextContent(
            data["content"]["description"], data["content"]["descriptionHtml"]
        )

        closing = RichTextContent(
            data["content"]["closing"], data["content"]["closingHtml"]
        )

        lists = [
            LeverClient._parse_lever_list(list_item)
            for list_item in data["content"]["lists"]
        ]

        return Posting(
            id=data["id"],
            created_at=datetime.fromtimestamp(data["createdAt"] / 1000),
            updated_at=datetime.fromtimestamp(data["updatedAt"] / 1000),
            state=PostingState(data["state"]),
            distribution_channels=data["distributionChannels"],
            tags=data["tags"],
            country=data["country"],
            location=data["categories"]["location"],
            commitment=data["categories"]["commitment"],
            workplace_type=WorkplaceType(data["workplaceType"]),
            apply_url=urls["apply"] if urls is not None else None,
            posting_url=urls["show"] if urls is not None else None,
            department=data["categories"]["department"],
            team=data["categories"]["team"],
            title=data["text"],
            description=description,
            lists=lists,
            closing=closing,
            salary=salary,
        )

    def get_postings(
        self,
        *,
        updated_at_start: float | None = None,
    ) -> Sequence[Posting]:
        data = self._get(
            "postings",
            {
                "updated_at_start": updated_at_start,
            },
        )

        postings = data["data"]

        return [self._parse_lever_posting(posting) for posting in postings]


__all__ = ("LeverClient",)
