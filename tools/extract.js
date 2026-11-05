const fs=require("fs");const h=fs.readFileSync("/home/claude/rx-english.html","utf8");
const d1=h.split("/*DATA*/")[1].split("/*ENDDATA*/")[0].replace("const UNITS","global.UNITS");
const d2=h.split("/*AREAS*/")[1].split("/*ENDAREAS*/")[0].replace("const AREAS","global.AREAS");
eval(d1);eval(d2);
const PRON={CRA:"C R A",CRO:"C R O",PI:"P I",SIV:"S I V",SDV:"S D V",eCRF:"e C R F",ICF:"I C F",GCP:"G C P",SAE:"S A E",SUSAR:"soosar",IMP:"I M P",TMF:"T M F",SOP:"S O P",EDC:"E D C",IB:"I B",RWE:"R W E",KPI:"K P I",CRM:"C R M",CAPA:"kappa",QALY:"kwaylee",MSLs:"M S L's",US:"U S",GPs:"G P's",IT:"I T"};
function pron(t){let s=t;
 for(const k of Object.keys(PRON))s=s.replace(new RegExp("(^|[^A-Za-z])"+k+"(?![A-Za-z])","g"),(m,p)=>p+PRON[k]);
 s=s.replace(/\bIII\b/g,"three").replace(/(\d)\s?mg\b/g,"$1 milligrams").replace(/(\d)%/g,"$1 percent").replace(/\//g," or ");
 return s}
const out=[],seen=new Set(),unknown=new Set();
function add(uid,text){if(seen.has(text))return;seen.add(text);out.push({uid,text,say:pron(text)});(text.match(/[A-Za-z]*[A-Z]{2,}[A-Za-z]*/g)||[]).forEach(t=>{if(!PRON[t]&&t!=="III")unknown.add(t)})}
for(const u of UNITS){u.words.forEach(w=>{add(u.id,w[0]);add(u.id,w[2])});(u.sent||[]).forEach(s=>add(u.id,s[0]))}
for(const a of AREAS){a.groups.forEach(g=>g[1].forEach(w=>{add(a.id,w[0]);add(a.id,w[2])}))}
fs.writeFileSync("texts.json",JSON.stringify(out));
console.log(out.length,"clips; unknown caps tokens:",[...unknown].join(" "));
const odd=new Set();out.forEach(o=>(o.say.match(/[^A-Za-z0-9 .,'\-?!:;()]/g)||[]).forEach(c=>odd.add(c)));console.log("odd chars:",[...odd].join(" "));
console.log(out.filter(o=>o.say!==o.text).slice(0,8).map(o=>o.text+"  =>  "+o.say).join("\n"));
