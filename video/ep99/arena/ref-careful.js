// Reference bot 2 (ours, not an AI answer): remembers every cell it has been
// in (by v.x, v.y), goes into a new cell when it can (order right, down, left,
// up), walks back the way it came at a dead end, takes the exit when it sees it.
// Expected: gets out within 500 steps.
var seen = {};
var trail = [];
function move(v) {
  var order = ["right", "down", "left", "up"];
  var dx = { right: 1, down: 0, left: -1, up: 0 };
  var dy = { right: 0, down: 1, left: 0, up: -1 };
  var back = { right: "left", down: "up", left: "right", up: "down" };
  seen[v.x + "," + v.y] = true;
  for (var i = 0; i < 4; i++) if (v[order[i]] === "exit") return order[i];
  for (var j = 0; j < 4; j++) {
    var d = order[j];
    if (v[d] === "open" && !seen[(v.x + dx[d]) + "," + (v.y + dy[d])]) {
      trail.push(back[d]);
      return d;
    }
  }
  if (trail.length) return trail.pop();
  return "up";
}
