#!/bin/bash
# Real run, nothing edited by hand after. Date of run printed at top.
set -u
export GIT_AUTHOR_NAME=David GIT_AUTHOR_EMAIL=d@example.com GIT_COMMITTER_NAME=David GIT_COMMITTER_EMAIL=d@example.com
export GIT_CONFIG_GLOBAL=/dev/null
D=$(cd "$(dirname "$0")" && pwd)
rm -rf "$D/work"; mkdir -p "$D/work"; cd "$D/work"
run(){ echo "\$ $*"; "$@" 2>&1; echo; }
echo "# date: $(date -u +%F) ; $(git --version) ; node $(node --version)"; echo
mkdir tipcalc && cd tipcalc
cat > app.js <<'JS'
// tipcalc: 15% tip on a bill
const bill = Number(process.argv[2]);
const tip = bill * 0.15;
console.log("Bill " + bill + " -> tip " + tip.toFixed(2) + ", total " + (bill + tip).toFixed(2));
JS
run git init -b main
run node app.js 80
run git add app.js
run git commit -m "Tip calculator works"
echo "# --- AI edit #1: 'also split the bill between friends' (NOT committed yet) ---"
cat > app.js <<'JS'
// tipcalc: 15% tip on a bill, split between friends
const bill = Number(process.argv[2]);
const tip = bill * 0.15;
const people = Number(process.argv[3]);
console.log("Each pays " + ((bill + tip) / people.count).toFixed(2));
JS
run node app.js 80
echo "# the app is broken and we do not remember what was there. Ask git:"
run git status --short
run git diff
run git log --oneline
echo "# the fix, said to the AI: 'go back to the last commit that worked'. In git:"
run git restore app.js
run node app.js 80
echo "# --- AI edit #2: this time it WAS committed ---"
cat > app.js <<'JS'
// tipcalc: 15% tip on a bill
const bill = Number(process.argv[2]);
const tip = Math.round(bill * 0.15);
console.log("Bill " + bill + " -> tip " + tip + ", total " + (bill + tip));
JS
run git commit -am "AI: round the tip"
run node app.js 83
run git log --oneline
echo "# undo that commit without erasing history:"
run git revert --no-edit HEAD
run node app.js 83
run git log --oneline
echo "# --- push / clone: local bare folder plays the part of GitHub ---"
cd "$D/work"; git init -q --bare -b main remote.git
cd tipcalc
run git remote add origin ../remote.git
run git push -u origin main
cd "$D/work"
run git clone remote.git friend-copy
cd friend-copy
export GIT_AUTHOR_NAME=Friend GIT_COMMITTER_NAME=Friend
echo "# --- branch + merge ---"
run git switch -c split-bill
cat >> app.js <<'JS'
const people = Number(process.argv[3] || 1);
console.log("Each of " + people + " pays " + ((bill + tip) / people).toFixed(2));
JS
run git commit -am "Split the bill"
run node app.js 80 4
run git switch main
run git merge split-bill
run git tag v1.0
run git push origin main --tags
run git log --oneline --decorate
cd "$D/work/tipcalc"
run git pull
run git tag
