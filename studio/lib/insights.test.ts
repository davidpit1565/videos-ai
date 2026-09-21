import { test } from "node:test";
import assert from "node:assert/strict";
import {
  statusFromErrorBody,
  metricsChanged,
  shouldSnapshot,
  rate,
  computeCalculatedMetrics,
  type SnapshotMetrics,
} from "./insights.ts";

const M = (over: Partial<SnapshotMetrics> = {}): SnapshotMetrics => ({
  views: 100,
  reach: 80,
  likes: 5,
  comments: 1,
  saves: 2,
  shares: 0,
  watchAvgSeconds: null,
  watchTotalSeconds: null,
  watchReplays: null,
  ...over,
});

test("statusFromErrorBody: names permission errors specifically", () => {
  assert.equal(
    statusFromErrorBody("(#10) ... requires the 'pages_read_engagement' permission"),
    "PERMISSION_REQUIRED",
  );
  assert.equal(statusFromErrorBody("(#100) Unsupported get request"), "NOT_AVAILABLE");
});

test("metricsChanged: zero vs null are never treated as equal", () => {
  assert.equal(metricsChanged(M({ shares: 0 }), M({ shares: null })), true);
  assert.equal(metricsChanged(M({ shares: 0 }), M({ shares: 0 })), false);
});

test("metricsChanged: a real change on any field is detected", () => {
  assert.equal(metricsChanged(M({ views: 100 }), M({ views: 101 })), true);
  assert.equal(metricsChanged(M(), M()), false);
});

test("shouldSnapshot: always true with no prior snapshot", () => {
  assert.equal(shouldSnapshot(undefined, M(), 360, new Date().toISOString()), true);
});

test("shouldSnapshot: true immediately when a metric changed, regardless of window", () => {
  const now = new Date();
  const last = { collectedAt: now.toISOString(), ...M({ views: 100 }) };
  const oneMinuteLater = new Date(now.getTime() + 60_000).toISOString();
  assert.equal(shouldSnapshot(last, M({ views: 101 }), 360, oneMinuteLater), true);
});

test("shouldSnapshot: false when nothing changed and the dedupe window hasn't elapsed", () => {
  const now = new Date();
  const last = { collectedAt: now.toISOString(), ...M() };
  const soon = new Date(now.getTime() + 5 * 60_000).toISOString();
  assert.equal(shouldSnapshot(last, M(), 360, soon), false);
});

test("shouldSnapshot: true once the dedupe window has elapsed, even with no change", () => {
  const now = new Date();
  const last = { collectedAt: now.toISOString(), ...M() };
  const muchLater = new Date(now.getTime() + 400 * 60_000).toISOString();
  assert.equal(shouldSnapshot(last, M(), 360, muchLater), true);
});

test("rate: null when the denominator is missing or zero, never a fabricated 0", () => {
  assert.equal(rate(5, null), null);
  assert.equal(rate(5, undefined), null);
  assert.equal(rate(5, 0), null);
  assert.equal(rate(0, 100), 0); // a genuine zero numerator is a real, valid rate
});

test("rate: null when the numerator is missing, even with a real denominator", () => {
  assert.equal(rate(null, 100), null);
});

test("computeCalculatedMetrics: reach-based rates use reach, never views", () => {
  const m = computeCalculatedMetrics({
    views: 500, reach: 300, likes: 10, comments: 2, saves: 3, shares: 1,
  });
  assert.equal(m.engagementRateByReach.value, (10 + 2 + 3 + 1) / 300);
  assert.equal(m.engagementRateByViews.value, (10 + 2 + 3 + 1) / 500);
  assert.notEqual(m.engagementRateByReach.value, m.engagementRateByViews.value);
});

test("computeCalculatedMetrics: null reach propagates to null, not a views fallback", () => {
  const m = computeCalculatedMetrics({
    views: 500, reach: null, likes: 10, comments: 0, saves: 0, shares: 0,
  });
  assert.equal(m.engagementRateByReach.value, null);
  assert.equal(m.likeRateByReach.value, null);
  // views-based legacy metric must still work even though reach is unavailable
  assert.equal(m.engagementRateByViews.value, 10 / 500);
});

test("computeCalculatedMetrics: nonFollowerReachRate only computed from the real breakdown, never inferred", () => {
  const withBreakdown = computeCalculatedMetrics({
    views: 100, reach: 80, likes: 1, comments: 0, saves: 0, shares: 0,
    reachByFollowerType: { followers: 50, nonFollowers: 30 },
  });
  assert.equal(withBreakdown.nonFollowerReachRate.value, 30 / 80);

  const withoutBreakdown = computeCalculatedMetrics({
    views: 100, reach: 80, likes: 1, comments: 0, saves: 0, shares: 0,
  });
  assert.equal(withoutBreakdown.nonFollowerReachRate.value, null);
});

test("computeCalculatedMetrics: watchPercentage only when both watch time and duration are real", () => {
  const m = computeCalculatedMetrics({
    views: 100, reach: 80, likes: 0, comments: 0, saves: 0, shares: 0,
    watchAvgSeconds: 20, durationSeconds: 40,
  });
  assert.equal(m.watchPercentage.value, 0.5);

  const missingDuration = computeCalculatedMetrics({
    views: 100, reach: 80, likes: 0, comments: 0, saves: 0, shares: 0,
    watchAvgSeconds: 20,
  });
  assert.equal(missingDuration.watchPercentage.value, null);
});

test("computeCalculatedMetrics: every metric carries its formula and source fields", () => {
  const m = computeCalculatedMetrics({
    views: 100, reach: 80, likes: 1, comments: 1, saves: 1, shares: 1,
  });
  for (const key of Object.keys(m)) {
    assert.ok(m[key].formula.length > 0, `${key} missing a formula`);
    assert.ok(m[key].sourceFields.length > 0, `${key} missing sourceFields`);
  }
});
