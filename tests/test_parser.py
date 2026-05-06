from __future__ import annotations

import unittest

from chat2workflow.miner import build_corpus_stats, mine_workflows
from chat2workflow.parser import anonymize_sender, parse_wechat_text
from chat2workflow.templates import WORKFLOW_TEMPLATES


SAMPLE = """********************2024-01-01********************
2024-01-01 09:00:00 system notice
t__;:我要投简历
继续补一句
21会计2郑思语:这个论文怎么写
********************2024-01-02********************
2024-01-02 10:00:00 another system notice
"""


class ParserTest(unittest.TestCase):
    def test_parse_wechat_text(self) -> None:
        messages = parse_wechat_text(SAMPLE)
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0].kind, "system")
        self.assertEqual(messages[1].sender, "t__;")
        self.assertIn("继续补一句", messages[1].body)
        self.assertEqual(messages[2].sender, "21会计2郑思语")
        self.assertEqual(messages[3].kind, "system")

    def test_anonymize_sender_is_stable(self) -> None:
        self.assertEqual(anonymize_sender("alice"), anonymize_sender("alice"))
        self.assertNotEqual(anonymize_sender("alice"), anonymize_sender("bob"))

    def test_mining_finds_workflows(self) -> None:
        messages = parse_wechat_text(SAMPLE)
        cards = mine_workflows(messages, WORKFLOW_TEMPLATES, min_hits=1)
        titles = [card.title for card in cards]
        self.assertIn("Career and Interview Prep", titles)
        self.assertIn("Academic Workflows", titles)

    def test_stats_include_counts(self) -> None:
        messages = parse_wechat_text(SAMPLE)
        stats = build_corpus_stats(messages, WORKFLOW_TEMPLATES)
        self.assertEqual(stats.message_count, 2)
        self.assertEqual(stats.system_message_count, 2)
        self.assertEqual(stats.active_day_count, 2)


if __name__ == "__main__":
    unittest.main()
