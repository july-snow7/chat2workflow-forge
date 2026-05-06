"""Chat2Workflow Forge."""

from .miner import build_corpus_stats, mine_workflows
from .parser import parse_wechat_export, parse_wechat_file
from .templates import WORKFLOW_TEMPLATES

__all__ = [
    "WORKFLOW_TEMPLATES",
    "build_corpus_stats",
    "mine_workflows",
    "parse_wechat_export",
    "parse_wechat_file",
]

__version__ = "0.1.0"

