from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from datetime import date
from pathlib import Path
from typing import List, Optional, Union

from .models import Message

DATE_HEADER_RE = re.compile(r"^\*{20}(\d{4}-\d{2}-\d{2})\*{20}$")
SENDER_LINE_RE = re.compile(r"^(?P<sender>[^:]{1,60}?):(?P<body>.*)$")
SYSTEM_LINE_RE = re.compile(r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<body>.+)$")


def anonymize_sender(sender: str) -> str:
    digest = hashlib.sha1(sender.encode("utf-8")).hexdigest()[:10]
    return f"contact_{digest}"


def parse_wechat_text(text: str) -> list[Message]:
    messages: List[Message] = []
    current_date: Optional[date] = None
    last_index: Optional[int] = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r")
        stripped = line.strip()
        if not stripped:
            continue

        date_match = DATE_HEADER_RE.match(stripped)
        if date_match:
            current_date = date.fromisoformat(date_match.group(1))
            last_index = None
            continue

        system_match = SYSTEM_LINE_RE.match(stripped)
        if system_match:
            messages.append(
                Message(
                    date=current_date,
                    sender="system",
                    body=system_match.group("body").strip(),
                    kind="system",
                )
            )
            last_index = len(messages) - 1
            continue

        sender_match = SENDER_LINE_RE.match(stripped)
        if sender_match:
            messages.append(
                Message(
                    date=current_date,
                    sender=sender_match.group("sender").strip(),
                    body=sender_match.group("body").lstrip(),
                    kind="message",
                )
            )
            last_index = len(messages) - 1
            continue

        if last_index is not None:
            previous = messages[last_index]
            messages[last_index] = replace(previous, body=f"{previous.body}\n{line.rstrip()}")
        else:
            messages.append(
                Message(
                    date=current_date,
                    sender="system",
                    body=stripped,
                    kind="system",
                )
            )
            last_index = len(messages) - 1

    return messages


def parse_wechat_export(text: str) -> list[Message]:
    """Backward-compatible alias for the public API."""
    return parse_wechat_text(text)


def parse_wechat_file(path: Union[str, Path]) -> list[Message]:
    file_path = Path(path)
    return parse_wechat_text(file_path.read_text(encoding="utf-8-sig"))
