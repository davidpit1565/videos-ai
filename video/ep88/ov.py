import sys,json,urllib.request,urllib.parse,time
UA={'User-Agent':'actually-works-research/1.0'}
def search(q,n=8,lic='cc0,pdm',extra=''):
    u='https://api.openverse.org/v1/images/?'+urllib.parse.urlencode(dict(q=q,license=lic,page_size=n))+extra
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))['results']
        except Exception as e: time.sleep(8)
    return []
if __name__=='__main__':
    for q in sys.argv[1:]:
        print('##',q)
        for r in search(q,8):
            print(r['id'][:8],'|',(r['title'] or '')[:50],'|',r.get('creator'),'|',r['license'],'|',r.get('width'),'x',r.get('height'),'|',r['source'],'|',r['url'][:90])
