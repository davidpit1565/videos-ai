// Reference driver 2 (ours, not an AI answer): keeps to the middle and
// slows down when the wall ahead is close. Expected: 2 laps in 7-11 s.
function steer(s) {
  const turn = Math.max(-1, Math.min(1, (s.right - s.left) / 60));
  const target = Math.max(3, Math.min(10, s.front / 22));
  const gas = s.speed < target ? 1 : 0;
  return { turn, gas };
}
