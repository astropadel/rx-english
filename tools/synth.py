import json,hashlib,os,subprocess,sys,time,wave,io
from piper import PiperVoice
try:
    from piper import SynthesisConfig
    CFG=SynthesisConfig(length_scale=1.05)
except Exception as e:
    CFG=None
v=PiperVoice.load('/home/claude/voice_dl/ex/en-us-lessac-medium.onnx')
os.makedirs('clips',exist_ok=True)
items=json.load(open('texts.json'))
t0=time.time();done=0;new=0
for it in items:
    k=hashlib.sha1(it['say'].encode()).hexdigest()[:16]
    p=f'clips/{k}.mp3'
    if os.path.exists(p) and os.path.getsize(p)>500: continue
    if time.time()-t0>520: break
    buf=io.BytesIO()
    with wave.open(buf,'wb') as w:
        if CFG: v.synthesize_wav(it['say'],w,syn_config=CFG)
        else: v.synthesize_wav(it['say'],w)
    r=subprocess.run(['ffmpeg','-loglevel','error','-y','-f','wav','-i','pipe:0','-af','adelay=60:all=1,apad=pad_dur=0.04','-ac','1','-codec:a','libmp3lame','-b:a','40k','-write_xing','0','-id3v2_version','0','-f','mp3','pipe:1'],input=buf.getvalue(),capture_output=True)
    if r.returncode!=0 or len(r.stdout)<500:
        print('FAIL',it['text'],r.stderr[:200]);continue
    open(p,'wb').write(r.stdout);new+=1
have=sum(1 for it in items if os.path.exists('clips/'+hashlib.sha1(it['say'].encode()).hexdigest()[:16]+'.mp3'))
print('cfg',bool(CFG),'new',new,'have',have,'/',len(items),'secs',round(time.time()-t0))
