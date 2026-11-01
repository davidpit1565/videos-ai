"""Tests for outlier.py. Run: python3 -m unittest discover -s scripts -v"""
import csv
import json
import os
import tempfile
import unittest

import outlier

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "..", "fixtures", "oriane-ai-tools-2026-11-01.json")


class OutlierTests(unittest.TestCase):
    def setUp(self):
        self.posts = outlier.load(FIXTURE)

    def test_fixture_loads_all_records(self):
        self.assertEqual(len(self.posts), 50)

    def test_ratio_is_views_over_followers(self):
        ariel = [p for p in self.posts if p["handle"] == "ariel.land"
                 and p["views"] == 4748933][0]
        self.assertAlmostEqual(outlier.score(ariel), 4748933 / 163307, places=3)

    def test_zero_followers_does_not_divide_by_zero(self):
        post = {"views": 50000, "followers": 0}
        self.assertEqual(outlier.score(post), 50000.0)

    def test_min_views_filter_drops_small_posts(self):
        kept = outlier.rank(self.posts, min_views=1_000_000, min_ratio=0)
        self.assertTrue(all(p["views"] >= 1_000_000 for p in kept))
        self.assertTrue(len(kept) > 0)

    def test_min_ratio_filter_drops_big_accounts(self):
        kept = outlier.rank(self.posts, min_views=0, min_ratio=3.0)
        self.assertTrue(all(p["ratio"] >= 3.0 for p in kept))
        # a 5M-follower account with 5M views is not kept
        self.assertFalse(any(p["followers"] > 3_000_000 and p["ratio"] < 3
                             for p in kept))

    def test_ranked_by_ratio_descending(self):
        kept = outlier.rank(self.posts, min_views=0, min_ratio=0)
        ratios = [p["ratio"] for p in kept]
        self.assertEqual(ratios, sorted(ratios, reverse=True))

    def test_comment_bait_detected(self):
        bait = outlier.BAIT.search("Comment “Tools” and I’ll send you my best AI tools")
        self.assertIsNotNone(bait)
        self.assertIsNone(outlier.BAIT.search("Join our Editing for Beginners Workshop"))

    def test_csv_input(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "hand.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["handle", "views", "followers", "published",
                            "format", "caption", "url"])
                w.writerow(["someone", "90000", "10000", "2026-10-01",
                            "reel", "A mistake list", "https://x"])
            posts = outlier.load(path)
            self.assertEqual(posts[0]["views"], 90000)
            self.assertAlmostEqual(outlier.score(posts[0]), 9.0)

    def test_finds_records_inside_firecrawl_envelope(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "envelope.json")
            envelope = {"data": {"alexandria": [{"data": {"data": {
                "results": [{"profileHandle": "a", "viewsCount": 30000,
                             "profileFollowersCount": 1000,
                             "publishedAt": "2026-09-01T00:00:00Z",
                             "format": "video", "caption": "hi"}]}}}]}}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(envelope, f)
            posts = outlier.load(path)
            self.assertEqual(len(posts), 1)
            self.assertEqual(posts[0]["published"], "2026-09-01")


if __name__ == "__main__":
    unittest.main()
