from __future__ import annotations

import json
from collections import Counter
from datetime import date
from typing import Iterable

from .models import CorpusStats, Message, WorkflowCard, WorkflowTemplate
from .parser import anonymize_sender
from .templates import WORKFLOW_TEMPLATES


def _keyword_hits(message: Message, template: WorkflowTemplate) -> list[str]:
    body = message.body.lower()
    return [keyword for keyword in template.keywords if keyword.lower() in body]


def build_corpus_stats(
    messages: list[Message],
    templates: Iterable[WorkflowTemplate] = WORKFLOW_TEMPLATES,
    anonymize: bool = True,
) -> CorpusStats:
    message_count = sum(1 for message in messages if message.kind == "message")
    system_message_count = sum(1 for message in messages if message.kind == "system")

    sender_counter = Counter()
    date_values: list[date] = []
    keyword_totals = Counter()
    template_hits: list[dict[str, object]] = []

    for message in messages:
        if message.date is not None:
            date_values.append(message.date)
        if message.kind == "message":
            sender = anonymize_sender(message.sender) if anonymize else message.sender
            sender_counter[sender] += 1

    for template in templates:
        matched_messages = 0
        signal_counter = Counter()
        for message in messages:
            if message.kind != "message":
                continue
            hits = _keyword_hits(message, template)
            if not hits:
                continue
            matched_messages += 1
            signal_counter.update(hits)
        keyword_totals.update(signal_counter)
        template_hits.append(
            {
                "template_id": template.id,
                "title": template.title,
                "matched_messages": matched_messages,
                "keyword_hits": dict(signal_counter),
            }
        )

    template_hits.sort(key=lambda item: (-int(item["matched_messages"]), str(item["title"])))

    active_dates = sorted(set(date_values))
    first_date = active_dates[0].isoformat() if active_dates else None
    last_date = active_dates[-1].isoformat() if active_dates else None
    span_days = (active_dates[-1] - active_dates[0]).days + 1 if len(active_dates) >= 2 else len(active_dates)

    top_senders = [
        {"sender": sender, "count": count}
        for sender, count in sender_counter.most_common(10)
    ]

    return CorpusStats(
        message_count=message_count,
        system_message_count=system_message_count,
        unique_sender_count=len(sender_counter),
        active_day_count=len(active_dates),
        first_date=first_date,
        last_date=last_date,
        span_days=span_days,
        top_senders=top_senders,
        template_hits=template_hits,
        keyword_totals=dict(keyword_totals),
    )


def mine_workflows(
    messages: list[Message],
    templates: Iterable[WorkflowTemplate] = WORKFLOW_TEMPLATES,
    min_hits: int = 1,
) -> list[WorkflowCard]:
    template_list = list(templates)

    hits_by_template: dict[str, tuple[int, Counter[str]]] = {}
    for template in template_list:
        matched_messages = 0
        signal_counter: Counter[str] = Counter()
        for message in messages:
            if message.kind != "message":
                continue
            hits = _keyword_hits(message, template)
            if not hits:
                continue
            matched_messages += 1
            signal_counter.update(hits)
        if matched_messages >= min_hits:
            hits_by_template[template.id] = (matched_messages, signal_counter)

    if not hits_by_template:
        return []

    top_count = max(count for count, _ in hits_by_template.values())
    cards: list[WorkflowCard] = []

    for template in template_list:
        if template.id not in hits_by_template:
            continue
        matched_messages, signal_counter = hits_by_template[template.id]
        confidence = round(matched_messages / top_count, 3) if top_count else 0.0
        summary = (
            f"{template.description} "
            f"Matched {matched_messages} message groups in the corpus."
        )
        cards.append(
            WorkflowCard(
                template_id=template.id,
                title=template.title,
                summary=summary,
                matched_messages=matched_messages,
                confidence=confidence,
                signals=dict(signal_counter),
                tools=template.tools,
                inputs=template.inputs,
                outputs=template.outputs,
                steps=template.steps,
                evaluation=template.evaluation,
                privacy_notes=(
                    "Raw chat logs stay local.",
                    "Sender names are anonymized in reports.",
                    "Workflow output is provider-agnostic.",
                ),
            )
        )

    cards.sort(key=lambda card: (-card.matched_messages, card.title))
    return cards


def bundle_to_dict(stats: CorpusStats, cards: list[WorkflowCard]) -> dict[str, object]:
    return {
        "stats": stats.to_dict(),
        "workflow_cards": [card.to_dict() for card in cards],
    }


def bundle_to_json(stats: CorpusStats, cards: list[WorkflowCard], indent: int = 2) -> str:
    return json.dumps(bundle_to_dict(stats, cards), ensure_ascii=False, indent=indent)
