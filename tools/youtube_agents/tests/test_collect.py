import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.youtube_agents import collect


class TestYouTubeAgentCollector(unittest.TestCase):
    @patch("tools.youtube_agents.collect.subprocess.run")
    def test_cookie_file_passed_as_argument_without_value(self, mock):
        mock.return_value.returncode = 0
        mock.return_value.stdout = "ok"
        with tempfile.TemporaryDirectory() as tmp:
            cookie = Path(tmp) / "cookies.txt"
            cookie.write_text("# Netscape HTTP Cookie File\\n")
            with patch.dict(os.environ, {"YTDLP_COOKIE_FILE": str(cookie)}):
                output, error = collect.run_ytdlp(["--list-subs", "https://example.com"], 10)
            self.assertEqual((output, error), ("ok", None))
            args = mock.call_args.args[0]
            self.assertEqual(args[args.index("--cookies") + 1], str(cookie))
            self.assertNotIn("YOUTUBE_COOKIES", " ".join(args))

    def test_missing_cookie_file_fails_closed(self):
        with patch.dict(os.environ, {"YTDLP_COOKIE_FILE": "/not/a/real/cookie.txt"}):
            output, error = collect.run_ytdlp(["--list-subs"], 10)
        self.assertIsNone(output)
        self.assertEqual(error, "configured cookie file unavailable")

    def test_channel_sources(self):
        self.assertEqual(collect.CHANNELS["forn-ai"], "https://www.youtube.com/@fornyapayzeka")
        self.assertEqual(collect.CHANNELS["avenox"], "https://www.youtube.com/@avenoxai")

    def test_relevance(self):
        self.assertEqual(collect.classify("My Agents Are Working Harder Than Me"), "direct")
        self.assertEqual(collect.classify("Kendi Yapay Zeka Ekibimi Kurdum. Ben Kod Yazmıyorum."), "direct")
        self.assertEqual(collect.classify("Sıradan Şarkı Videosu"), None)
        self.assertEqual(collect.classify("Claude Code ile context topluyorum"), "supporting")
        self.assertEqual(collect.classify("Bir Deney", "Paralel agent workflow kullanıyorum"), "direct_description")

    def test_invalid_video_ids_are_rejected(self):
        self.assertIsNone(collect.base_video({"id": "nope"}))
        self.assertIsNone(collect.base_video({"id": "../attack"}))
        self.assertEqual(
            collect.base_video({"id": "aB12345_67X", "title": "X"})["url"],
            "https://www.youtube.com/watch?v=aB12345_67X",
        )

    def test_vtt_cleaner(self):
        original = (
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.000\n<v Speaker>Merhaba</v>\n\n"
            "00:00:01.000 --> 00:00:02.000\nMerhaba\n\n"
            "00:00:02.000 --> 00:00:03.000\nSelam &amp; merhaba\n"
        )
        self.assertEqual(collect.simplify_vtt(original), "Merhaba\nSelam & merhaba")

    @patch("tools.youtube_agents.collect.run_ytdlp")
    def test_catalog_deduplicated(self, mock):
        payload = json.dumps({"entries": [
            {"id": "aB12345_67X", "title": "My agents"},
            {"id": "aB12345_67X", "title": "Duplicate"},
            {"id": "fake"},
        ]})
        mock.return_value = payload, None
        entries, fails = collect.discover("forn-ai", 30, 0)
        self.assertEqual(len(entries), 1)
        self.assertEqual(fails, [])

    @patch("tools.youtube_agents.collect.run_ytdlp")
    def test_no_data_is_failure_not_success(self, mock):
        mock.return_value = None, "yt-dlp exit status 1"
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(collect.main(["--output", tmp]), 2)
            state = json.loads((Path(tmp) / "manifest.json").read_text())
            self.assertEqual(state["totals"]["discovered"], 0)
            self.assertEqual(len(state["channel_failures"]), 4)


if __name__ == "__main__":
    unittest.main()
