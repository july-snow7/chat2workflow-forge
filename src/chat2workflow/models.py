from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from typing import Any


@dataclass(frozen=True)
class Message:
    date: Optional[date]
    sender: str
    body: str
    kind: str = "message"

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date.isoformat() if self.date else None,
            "sender": self.sender,
            "body": self.body,
            "kind": self.kind,
        }


@dataclass(frozen=True)
class WorkflowTemplate:
    id: str
    title: str
    description: str
    keywords: tuple[str, ...]
    tools: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    steps: tuple[str, ...]
    evaluation: tuple[str, ...]
    model_fit: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "keywords": list(self.keywords),
            "tools": list(self.tools),
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "steps": list(self.steps),
            "evaluation": list(self.evaluation),
            "model_fit": list(self.model_fit),
        }


@dataclass(frozen=True)
class WorkflowCard:
    template_id: str
    title: str
    summary: str
    matched_messages: int
    confidence: float
    signals: dict[str, int] = field(default_factory=dict)
    tools: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    steps: tuple[str, ...] = ()
    evaluation: tuple[str, ...] = ()
    privacy_notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "template_id": self.template_id,
            "title": self.title,
            "summary": self.summary,
            "matched_messages": self.matched_messages,
            "confidence": self.confidence,
            "signals": dict(self.signals),
            "tools": list(self.tools),
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "steps": list(self.steps),
            "evaluation": list(self.evaluation),
            "privacy_notes": list(self.privacy_notes),
        }


@dataclass(frozen=True)
class CorpusStats:
    message_count: int
    system_message_count: int
    unique_sender_count: int
    active_day_count: int
    first_date: Optional[str]
    last_date: Optional[str]
    span_days: int
    top_senders: list[dict[str, Any]]
    template_hits: list[dict[str, Any]]
    keyword_totals: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_count": self.message_count,
            "system_message_count": self.system_message_count,
            "unique_sender_count": self.unique_sender_count,
            "active_day_count": self.active_day_count,
            "first_date": self.first_date,
            "last_date": self.last_date,
            "span_days": self.span_days,
            "top_senders": list(self.top_senders),
            "template_hits": list(self.template_hits),
            "keyword_totals": dict(self.keyword_totals),
        }
