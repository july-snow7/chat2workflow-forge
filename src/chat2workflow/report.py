from __future__ import annotations

from .models import CorpusStats, WorkflowCard


def _table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return ""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def fmt_row(values: list[str]) -> str:
        return "| " + " | ".join(value.ljust(widths[i]) for i, value in enumerate(values)) + " |"

    header_line = fmt_row(headers)
    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    body = "\n".join(fmt_row(row) for row in rows)
    return "\n".join([header_line, separator, body])


def render_markdown_report(stats: CorpusStats, cards: list[WorkflowCard]) -> str:
    lines: list[str] = ["# Chat2Workflow Report", ""]

    lines.extend(
        [
            "## Corpus Overview",
            "",
            _table(
                ["Metric", "Value"],
                [
                    ["Messages", str(stats.message_count)],
                    ["System events", str(stats.system_message_count)],
                    ["Unique senders", str(stats.unique_sender_count)],
                    ["Active dates", str(stats.active_day_count)],
                    ["Date range", f"{stats.first_date or '-'} to {stats.last_date or '-'}"],
                    ["Span days", str(stats.span_days)],
                ],
            ),
            "",
        ]
    )

    if stats.template_hits:
        lines.extend(["## Workflow Families", ""])
        rows = []
        for item in stats.template_hits:
            rows.append(
                [
                    str(item["title"]),
                    str(item["matched_messages"]),
                ]
            )
        lines.append(_table(["Family", "Matched messages"], rows))
        lines.append("")

    if stats.top_senders:
        lines.extend(["## Top Anonymized Senders", ""])
        rows = [[item["sender"], str(item["count"])] for item in stats.top_senders]
        lines.append(_table(["Sender", "Count"], rows))
        lines.append("")

    if cards:
        lines.extend(["## Workflow Cards", ""])
        for card in cards:
            lines.extend(
                [
                    f"### {card.title}",
                    "",
                    card.summary,
                    "",
                    f"- Matched messages: {card.matched_messages}",
                    f"- Confidence: {card.confidence}",
                    f"- Tools: {', '.join(card.tools)}",
                    f"- Inputs: {', '.join(card.inputs)}",
                    f"- Outputs: {', '.join(card.outputs)}",
                    "",
                    "Steps:",
                ]
            )
            for step in card.steps:
                lines.append(f"- {step}")
            lines.append("")
            lines.append("Evaluation:")
            for item in card.evaluation:
                lines.append(f"- {item}")
            lines.append("")
            lines.append("Privacy notes:")
            for note in card.privacy_notes:
                lines.append(f"- {note}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"

