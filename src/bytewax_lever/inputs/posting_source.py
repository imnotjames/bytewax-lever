from datetime import datetime, timedelta, UTC
from typing import Iterable, List, Optional

from bytewax.inputs import StatefulSourcePartition, FixedPartitionedSource

from ..lever_client import LeverClient
from ..types import (
    Posting,
)


class PostingSourcePartition(StatefulSourcePartition[Posting, float]):
    def __init__(
        self,
        *,
        client: LeverClient,
        from_timestamp: float = 0,
        interval: float = 30,
    ):
        self._client = client
        self._from_timestamp = from_timestamp
        self._has_at_least_one_request = False
        self._interval = interval

    def snapshot(self) -> float:
        return self._from_timestamp or 0

    def next_awake(self) -> Optional[datetime]:
        # If we have never hit the API before we should be awake immediately
        if not self._has_at_least_one_request:
            return None

        return datetime.now(UTC) + timedelta(seconds=self._interval)

    def next_batch(self) -> Iterable[Posting]:
        self._has_at_least_one_request = True

        postings = self._client.get_postings(updated_at_start=self._from_timestamp + 1)

        for posting in postings:
            self._from_timestamp = max(
                self._from_timestamp, posting.updated_at.timestamp()
            )

            yield posting


class PostingSource(FixedPartitionedSource[Posting, float]):
    def __init__(self, *, api_key: str, base_url: str | None = None):
        self._api_key = api_key
        self._base_url = base_url

    def build_part(
        self, step_id: str, for_part: str, resume_state: Optional[float]
    ) -> PostingSourcePartition:
        lever_client = LeverClient(
            self._api_key,
            self._base_url,
        )

        return PostingSourcePartition(
            client=lever_client,
            from_timestamp=resume_state or 0,
        )

    def list_parts(self) -> List[str]:
        return ["partition_0"]


__all__ = ("PostingSource", "PostingSourcePartition")
