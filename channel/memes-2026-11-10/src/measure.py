import subprocess,sys,re
R="/root/.cache/hyperframes/chrome/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
D="/tmp/claude-0/-home-user-videos-ai/6fd8d102-d852-578a-aa0a-796b7f4d4fb2/scratchpad/memes"
for n in "AB":
    h=open(f"{D}/build/{n}.html").read()
    h+="<script>document.fonts.ready.then(()=>{let o=[];document.querySelectorAll('.t').forEach(e=>{let r=e.getBoundingClientRect();o.push(e.innerText.replace(/\\n/g,'/')+' '+[r.left,r.top,r.right,r.bottom].map(Math.round))});document.title=o.join(' || ')})</script>"
    open(f"{D}/build/m{n}.html","w").write(h)
    out=subprocess.run([R,"--no-sandbox","--disable-gpu","--virtual-time-budget=3000","--dump-dom",f"file://{D}/build/m{n}.html"],capture_output=True,text=True).stdout
    print(n,re.search(r"<title>(.*?)</title>",out,re.S).group(1))
