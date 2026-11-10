import json,sys,time,urllib.request,datetime
sys.path.insert(0,'.')
from ov import search
UA={'User-Agent':'actually-works-research/1.0'}
W=[("8dd4c6a4","ripped paper piece","rip_lc"),("69245a91","torn paper white background","rip_hole1"),("987ffb20","torn paper white background","rip_hole2"),
("9fc0ccb7","ripped newspaper","rip_news"),("2e4d26b8","torn paper white background","rip_receipts"),("c03bfbc0","torn paper edge texture","pap_red"),
("d0ea59c8","torn paper edge texture","pap_orange"),("323c07ce","torn paper edge texture","pap_blue"),("8201c247","torn paper edge texture","pap_purple"),
("b20e4d77","torn paper edge texture","map_pearl"),("514aeb2a","cat sleeping window","ph_cat"),("5be11030","bicycle leaning wall","ph_bikes"),
("529a4bf1","sunset city skyline","ph_paris"),("c532037e","sunset city skyline","ph_sledders"),("bf1f69a0","dog on couch","ph_dog")]
cache={}
for id8,q,name in W:
    if q not in cache: cache[q]=search(q,8); time.sleep(1)
    r=[x for x in cache[q] if x['id'].startswith(id8)]
    if not r: print('NOTFOUND',name); continue
    r=r[0]; ext=r['url'].split('?')[0].rsplit('.',1)[-1].lower()
    if ext not in('jpg','jpeg','png'): ext='jpg'
    fn=f"assets7/{name}.{ext}"
    ok=False
    for i in range(3):
        try: open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(r['url'],headers=UA),timeout=60).read()); ok=True; break
        except Exception as e: time.sleep(5)
    info=dict(name=name,file=fn,ok=ok,title=r['title'],creator=r.get('creator'),license=r['license'],license_url=r.get('license_url'),page=r.get('foreign_landing_url'),url=r['url'],source=r['source'],retrieved=str(datetime.date.today()))
    open('assets7/credits7.jsonl','a').write(json.dumps(info)+'\n'); print(name,ok,r['license'],r.get('creator'))
