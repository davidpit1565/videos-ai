// Reference driver 1 (ours, not an AI answer): full gas, never brakes,
// steers gently toward the more open side. Expected: hits a wall.
function steer(s) {
  const turn = Math.max(-1, Math.min(1, (s.right - s.left) / 150));
  return { turn, gas: 1 };
}
