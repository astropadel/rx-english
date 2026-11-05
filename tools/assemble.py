import json,hashlib,os,subprocess,random
items=json.load(open('texts.json'))
os.makedirs('/home/claude/audio/a',exist_ok=True)
sp={};idx={}
for it in items:
    k=hashlib.sha1(it['say'].encode()).hexdigest()[:16]
    b=open(f'clips/{k}.mp3','rb').read()
    s=sp.setdefault(it['uid'],bytearray())
    idx[it['text']]=[it['uid'],len(s),len(b)]
    s.extend(b)
tot=0
for uid,b in sp.items():
    open(f'/home/claude/audio/a/{uid}.mp3','wb').write(b);tot+=len(b)
json.dump(idx,open('aidx.json','w'),ensure_ascii=False,separators=(',',':'))
lens=sorted((v[2],t) for t,v in idx.items())
print('sprites',len(sp),'total MB',round(tot/1e6,2),'max sprite KB',max(len(b) for b in sp.values())//1000)
print('shortest',[(l,t) for l,t in lens[:3]]);print('longest',[(l,t[:40]) for l,t in lens[-2:]])
print('index KB',round(os.path.getsize('aidx.json')/1000))
# decode check on random slices + durations
random.seed(1);bad=0
for t,(uid,st,ln) in random.sample(list(idx.items()),40):
    data=open(f'/home/claude/audio/a/{uid}.mp3','rb').read()[st:st+ln]
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','-f','mp3','-i','pipe:0'],input=data,capture_output=True)
    d=float(r.stdout.decode().strip() or 0)
    if d<0.3 or d>14: bad+=1;print('odd duration',t,d)
print('decode check done, odd:',bad)
