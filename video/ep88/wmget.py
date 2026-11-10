import sys,json,urllib.request,urllib.parse,time,re,os
UA={'User-Agent':'actually-works-research/1.0'}
def api(**p):
    p['format']='json'
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)
    for i in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))
        except Exception as e: time.sleep(15)
    return {}
def get(title,width=1600,out=None):
    r=api(action='query',titles='File:'+title,prop='imageinfo',iiprop='url|size|extmetadata|timestamp',iiurlwidth=width)
    pg=list(r['query']['pages'].values())[0]
    if 'imageinfo' not in pg: print('MISSING',title); return None
    ii=pg['imageinfo'][0]; m=ii['extmetadata']
    clean=lambda s: re.sub('<[^>]+>','',s or '').strip()[:80]
    info=dict(title=title,page='https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(title.replace(' ','_')),lic=clean(m.get('LicenseShortName',{}).get('value')),artist=clean(m.get('Artist',{}).get('value')),w=ii['width'],h=ii['height'])
    url=ii.get('thumburl') or ii['url']
    fn=out or re.sub(r'[^A-Za-z0-9._-]','_',title)[:50]
    path='assets7/'+fn
    for i in range(4):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read(); open(path,'wb').write(d); break
        except Exception as e: time.sleep(20)
    info['file']=path; info['bytes']=os.path.getsize(path) if os.path.exists(path) else 0
    print(json.dumps(info)); 
    open('assets7/credits.jsonl','a').write(json.dumps(info)+'\n')
    return info
if __name__=='__main__':
    for t in sys.argv[1:]:
        get(t); time.sleep(4)
