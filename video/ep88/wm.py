import sys,json,urllib.request,urllib.parse,time
UA={'User-Agent':'actually-works-research/1.0 (asset search; contact none)'}
def api(**p):
    p['format']='json'
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p)
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
        except Exception as e:
            time.sleep(15)
    return {}
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 12
r=api(action='query',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=n,prop='imageinfo',iiprop='url|size|extmetadata',iiurlwidth=300)
for pg in (r.get('query',{}).get('pages',{}) or {}).values():
    ii=pg['imageinfo'][0]; m=ii.get('extmetadata',{})
    print(pg['title'],'|',ii['width'],'x',ii['height'],'|',m.get('LicenseShortName',{}).get('value'),'|',(m.get('Artist',{}).get('value','') or '')[:40].replace('\n',' '))
