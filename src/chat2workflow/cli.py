from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional, Sequence, Union

from .miner import bundle_to_dict, build_corpus_stats, mine_workflows
from .parser import parse_wechat_file
from .report import render_markdown_report
from .templates import WORKFLOW_TEMPLATES


def _load(path: Union[str, Path]):
    return parse_wechat_file(path)


def _write_output(path: Optional[str], text: str) -> None:
    if path:
        Path(path).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chat2workflow")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser(
        "analyze",
        help="Parse a chat export and render a summary report.",
    )
    analyze.add_argument("input", help="Path to the WeChat text export.")
    analyze.add_argument("--out", help="Write the report to a file instead of stdout.")
    analyze.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Report format.",
    )
    analyze.add_argument(
        "--min-hits",
        type=int,
        default=1,
        help="Minimum matched messages required for a workflow card.",
    )
    analyze.add_argument(
        "--raw-senders",
        action="store_true",
        help="Keep real sender names in the corpus summary.",
    )

    export = subparsers.add_parser(
        "export-workflows",
        help="Export workflow cards as JSON.",
    )
    export.add_argument("input", help="Path to the WeChat text export.")
    export.add_argument("--out", required=True, help="Where to write the JSON bundle.")
    export.add_argument(
        "--min-hits",
        type=int,
        default=1,
        help="Minimum matched messages required for a workflow card.",
    )

    return parser


def run_analyze(args: argparse.Namespace) -> int:
    messages = _load(args.input)
    stats = build_corpus_stats(messages, WORKFLOW_TEMPLATES, anonymize=not args.raw_senders)
    cards = mine_workflows(messages, WORKFLOW_TEMPLATES, min_hits=args.min_hits)

    if args.format == "json":
        output = json.dumps(bundle_to_dict(stats, cards), ensure_ascii=False, indent=2)
    else:
        output = render_markdown_report(stats, cards)
    _write_output(args.out, output)
    return 0


def run_export_workflows(args: argparse.Namespace) -> int:
    messages = _load(args.input)
    stats = build_corpus_stats(messages, WORKFLOW_TEMPLATES, anonymize=True)
    cards = mine_workflows(messages, WORKFLOW_TEMPLATES, min_hits=args.min_hits)
    bundle = bundle_to_dict(stats, cards)
    Path(args.out).write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        return run_analyze(args)
    if args.command == "export-workflows":
        return run_export_workflows(args)
    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
