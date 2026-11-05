import json,hashlib,os,io,wave,subprocess,re,sys,time
sys.path.insert(0,'/home/claude/voicegen')
from scenes import SCENES
from piper import PiperVoice
try:
    from piper import SynthesisConfig; CFG=SynthesisConfig(length_scale=1.05)
except Exception: CFG=None
# validate content
for s in SCENES:
    for t in s['turns']:
        assert sorted(o['q'] for o in t['o'])==[0,1,2],(s['id'],t['them'])
PRON={'CRA':'C R A','SAE':'S A E','IMP':'I M P','PI':'P I'}
def pron(t):
    for k,v in PRON.items(): t=re.sub(r'(^|[^A-Za-z])'+k+r'(?![A-Za-z])',lambda m:m.group(1)+v,t)
    return (t.replace('Clínico','Clinico').replace('014','zero one four').replace('022','zero two two')
             .replace('2.0','two point oh').replace('3.0','three point oh').replace('10 a.m.','ten A M').replace('°C',' degrees'))
voices={'them':PiperVoice.load('/home/claude/voice_dl2/ex/en-us-ryan-medium.onnx'),'me':PiperVoice.load('/home/claude/voice_dl/ex/en-us-lessac-medium.onnx')}
items=[]
for s in SCENES:
    for t in s['turns']:
        items.append(('them',t['them']))
        for o in t['o']: items.append(('me',o['t']))
os.makedirs('clips_sc',exist_ok=True)
sprite=bytearray();idx={};t0=time.time()
for who,text in items:
    say=pron(text); k=hashlib.sha1((who+'|'+say).encode()).hexdigest()[:16]; p=f'clips_sc/{k}.mp3'
    if not (os.path.exists(p) and os.path.getsize(p)>500):
        buf=io.BytesIO()
        with wave.open(buf,'wb') as w:
            (voices[who].synthesize_wav(say,w,syn_config=CFG) if CFG else voices[who].synthesize_wav(say,w))
        r=subprocess.run(['ffmpeg','-loglevel','error','-y','-f','wav','-i','pipe:0','-af','adelay=60:all=1,apad=pad_dur=0.04','-ac','1','-codec:a','libmp3lame','-b:a','40k','-write_xing','0','-id3v2_version','0','-f','mp3','pipe:1'],input=buf.getvalue(),capture_output=True)
        assert r.returncode==0 and len(r.stdout)>500,(text,r.stderr[:200])
        open(p,'wb').write(r.stdout)
    b=open(p,'rb').read()
    if text in idx: continue
    idx[text]=['sc',len(sprite),len(b)]; sprite.extend(b)
open('/home/claude/audio/a/sc.mp3','wb').write(sprite)
json.dump(idx,open('aidx_sc.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(SCENES,open('scenes.json','w'),ensure_ascii=False,separators=(',',':'))
print('scenes',len(SCENES),'turns',sum(len(s['turns']) for s in SCENES),'clips',len(idx),'sprite KB',len(sprite)//1000,'secs',round(time.time()-t0))
