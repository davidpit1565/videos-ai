// Reference bot 1 (ours, not an AI answer): no memory. Takes the exit when it
// sees it, otherwise the first open way in the order right, down, left, up.
// Expected: walks back and forth and never gets out in 500 steps.
function move(v) {
  var order = ["right", "down", "left", "up"];
  for (var i = 0; i < 4; i++) if (v[order[i]] === "exit") return order[i];
  for (var j = 0; j < 4; j++) if (v[order[j]] === "open") return order[j];
  return "up";
}
