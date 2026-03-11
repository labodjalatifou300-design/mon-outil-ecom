import streamlit as st
import requests, json, re, base64, urllib.parse

st.set_page_config(page_title="E-Commerce Master Labo Pro", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;}
:root{--ink:#080810;--s1:#0f0f1a;--s2:#16162a;--s3:#1e1e35;--red:#ff2d55;--amber:#ff9f0a;--teal:#32d4a4;--smoke:#9999bb;--white:#f0f0fa;--bord:rgba(255,255,255,.07);}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:var(--ink)!important;color:var(--white)!important;}
#MainMenu,footer,header{visibility:hidden;}
section[data-testid="stSidebar"]{display:none!important;}
.block-container{padding:0 1.2rem 4rem!important;max-width:1400px!important;}

/* ── HERO ── */
.hero{position:relative;overflow:hidden;padding:3.5rem 2rem 2.5rem;text-align:center;
  background:linear-gradient(160deg,#080810 0%,#1a0815 45%,#080810 100%);
  border-bottom:1px solid rgba(255,45,85,.18);margin-bottom:2rem;}
.hero-glow{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse 90% 50% at 50% -5%,rgba(255,45,85,.22) 0%,transparent 65%),
    radial-gradient(ellipse 50% 50% at 10% 90%,rgba(255,159,10,.12) 0%,transparent 55%),
    radial-gradient(ellipse 50% 50% at 90% 90%,rgba(50,212,164,.1) 0%,transparent 55%);
  animation:gp 5s ease-in-out infinite;}
@keyframes gp{0%,100%{opacity:.7}50%{opacity:1}}

/* floating orbs */
.orb{position:absolute;border-radius:50%;filter:blur(55px);pointer-events:none;animation:of linear infinite;}
@keyframes of{0%{transform:translate(0,0)}25%{transform:translate(20px,-25px)}50%{transform:translate(-10px,15px)}75%{transform:translate(15px,10px)}100%{transform:translate(0,0)}}

/* particles */
.pt{position:absolute;border-radius:50%;pointer-events:none;animation:pf linear infinite;}
@keyframes pf{0%{transform:translateY(110%) scale(0);opacity:0}8%{opacity:1;transform:translateY(90%) scale(1)}88%{opacity:.7}100%{transform:translateY(-5%) scale(.3);opacity:0}}

/* title with 3D depth */
.hero-title{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(2.2rem,5.5vw,4.8rem);
  line-height:1.05;letter-spacing:-2px;color:var(--white);position:relative;z-index:2;
  text-shadow:0 0 80px rgba(255,45,85,.3),0 20px 60px rgba(0,0,0,.5);
  animation:ti 1s cubic-bezier(.16,1,.3,1) both;}
@keyframes ti{from{opacity:0;transform:translateY(35px) scale(.97)}to{opacity:1;transform:none}}
.hero-title .r{color:var(--red);display:inline-block;animation:pulse 3s ease-in-out infinite;}
@keyframes pulse{0%,100%{text-shadow:0 0 40px rgba(255,45,85,.4)}50%{text-shadow:0 0 80px rgba(255,45,85,.8),0 0 120px rgba(255,45,85,.3)}}
.hero-title .a{color:var(--amber);display:inline-block;animation:pulse2 3s 1s ease-in-out infinite;}
@keyframes pulse2{0%,100%{text-shadow:0 0 40px rgba(255,159,10,.4)}50%{text-shadow:0 0 80px rgba(255,159,10,.8)}}
.hero-sub{font-size:clamp(.85rem,1.8vw,1.1rem);color:var(--smoke);letter-spacing:4px;text-transform:uppercase;margin-top:.7rem;position:relative;z-index:2;animation:fi .8s .5s both;}
@keyframes fi{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.hero-bar{width:0;height:3px;margin:1.2rem auto 0;background:linear-gradient(90deg,var(--red),var(--amber),var(--teal));border-radius:2px;position:relative;z-index:2;animation:bw .9s .7s cubic-bezier(.16,1,.3,1) forwards;}
@keyframes bw{from{width:0}to{width:100px}}

/* ── PANEL ── */
.panel{background:var(--s1);border:1px solid var(--bord);border-radius:20px;padding:1.8rem;margin-bottom:1.4rem;position:relative;overflow:hidden;transition:border-color .3s;}
.panel::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,45,85,.5),rgba(255,159,10,.4),transparent);}
.panel:hover{border-color:rgba(255,45,85,.2);}
.pt-title{font-family:'Syne',sans-serif;font-weight:700;font-size:.7rem;letter-spacing:3px;text-transform:uppercase;color:var(--red);margin-bottom:1.3rem;display:flex;align-items:center;gap:.6rem;}
.pt-title::after{content:'';flex:1;height:1px;background:var(--bord);}

/* ── METRIC ── */
.metric{background:var(--s2);border:1px solid var(--bord);border-radius:16px;padding:1.2rem;text-align:center;transition:transform .35s cubic-bezier(.34,1.56,.64,1),border-color .3s,box-shadow .3s;cursor:default;}
.metric:hover{transform:perspective(500px) rotateY(-8deg) rotateX(5deg) translateY(-5px);border-color:rgba(255,45,85,.4);box-shadow:20px 20px 60px rgba(0,0,0,.5),0 0 30px rgba(255,45,85,.1);}
.mv{font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;line-height:1;margin-bottom:.3rem;}
.mv-r{color:var(--red);text-shadow:0 0 25px rgba(255,45,85,.5);}
.mv-a{color:var(--amber);text-shadow:0 0 25px rgba(255,159,10,.5);}
.mv-g{color:var(--teal);text-shadow:0 0 25px rgba(50,212,164,.5);}
.ml{font-size:.67rem;color:var(--smoke);letter-spacing:2px;text-transform:uppercase;}

/* ── TABLE ── */
.tbl{width:100%;border-collapse:collapse;font-size:.83rem;}
.tbl th{padding:.6rem .4rem;font-family:'Syne',sans-serif;font-size:.63rem;letter-spacing:2px;text-transform:uppercase;color:var(--smoke);border-bottom:1px solid var(--bord);text-align:center;}
.tbl td{padding:.55rem .4rem;text-align:center;border-bottom:1px solid rgba(255,255,255,.03);}
.tbl tr:hover td{background:rgba(255,45,85,.05);}
.cg{color:var(--teal);font-weight:700}.cr{color:var(--red);font-weight:600}.ca{color:var(--amber);font-weight:600}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{background:var(--s1)!important;border-radius:14px!important;padding:5px!important;gap:3px!important;border:1px solid var(--bord)!important;flex-wrap:wrap!important;margin-bottom:1.5rem!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--smoke)!important;border-radius:10px!important;padding:.45rem .9rem!important;font-family:'Syne',sans-serif!important;font-weight:600!important;font-size:.76rem!important;transition:all .2s!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,var(--red),#c0103a)!important;color:white!important;box-shadow:0 4px 20px rgba(255,45,85,.5)!important;}

/* ── BUTTONS ── */
.stButton>button{background:linear-gradient(135deg,var(--red),#c0103a)!important;color:white!important;border:none!important;border-radius:12px!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:.95rem!important;padding:.65rem 2.5rem!important;transition:all .3s!important;box-shadow:0 4px 24px rgba(255,45,85,.4)!important;}
.stButton>button:hover{transform:translateY(-3px) scale(1.02)!important;box-shadow:0 8px 35px rgba(255,45,85,.65)!important;}

/* ── INPUTS ── */
.stTextInput input,.stNumberInput input,.stTextArea textarea{background:var(--s2)!important;border:1px solid var(--bord)!important;border-radius:10px!important;color:var(--white)!important;}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:rgba(255,45,85,.5)!important;box-shadow:0 0 0 3px rgba(255,45,85,.1)!important;}
label{color:var(--smoke)!important;font-size:.78rem!important;letter-spacing:.5px!important;}

/* ── COPY BLOCK (text + icon RIGHT) ── */
.cblock{display:flex;align-items:flex-start;gap:.5rem;margin:.4rem 0;}
.ctext{flex:1;background:var(--s2);border:1px solid var(--bord);border-radius:10px;padding:.9rem 1rem;font-size:.88rem;line-height:1.75;white-space:pre-wrap;word-break:break-word;}
.cico{flex-shrink:0;width:38px;height:38px;border-radius:9px;background:var(--s2);border:1px solid var(--bord);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:1rem;transition:all .2s;user-select:none;margin-top:1px;}
.cico:hover{background:var(--red);border-color:var(--red);transform:scale(1.1);}

/* ── SCORE ── */
.crit-row{background:var(--s2);border-radius:12px;padding:.85rem 1rem;margin:.35rem 0;border:1px solid var(--bord);transition:all .2s;}
.crit-row:hover{border-color:rgba(255,45,85,.3);transform:translateX(4px);}
.crit-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:.32rem;}
.crit-name{font-family:'Syne',sans-serif;font-weight:700;font-size:.87rem;}
.crit-note{font-family:'Syne',sans-serif;font-weight:800;font-size:.9rem;}
.bar-bg{background:rgba(255,255,255,.07);border-radius:20px;height:6px;overflow:hidden;}
.bar-fill{height:100%;border-radius:20px;}
.crit-why{font-size:.77rem;color:var(--smoke);margin-top:.28rem;line-height:1.5;}

/* ── OFFER ── */
.ocard{background:var(--s2);border:1px solid var(--bord);border-radius:14px;padding:1.1rem;margin:.5rem 0;transition:all .25s;position:relative;overflow:hidden;}
.ocard::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--red),var(--amber));}
.ocard:hover{border-color:rgba(255,159,10,.35);transform:translateX(6px);}
.ocard-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.4rem;margin-bottom:.4rem;}
.ocard-title{font-family:'Syne',sans-serif;font-weight:700;font-size:.98rem;margin-left:.4rem;}
.ocard-badge{font-size:.68rem;padding:.2rem .6rem;border-radius:20px;font-weight:700;letter-spacing:1px;}
.ocard-tip{font-size:.8rem;color:var(--amber);padding:.35rem .7rem;background:rgba(255,159,10,.07);border-left:2px solid var(--amber);border-radius:0 6px 6px 0;margin-top:.4rem;}

/* ── ADCARD ── */
.adcard{background:var(--s2);border-left:3px solid var(--red);border-radius:0 14px 14px 0;padding:1rem 1.2rem;margin:.4rem 0;transition:transform .2s;}
.adcard:hover{transform:translateX(3px);}
.adcard-hook{font-family:'Syne',sans-serif;font-weight:800;font-size:1rem;color:var(--white);margin-bottom:.6rem;}
.adcard-pip{font-size:.87rem;color:var(--smoke);padding:.12rem 0;}
.adcard-pip::before{content:'▸ ';color:var(--red);}

/* ── VOICE ── */
.vscript{background:var(--s2);border:1px solid var(--bord);border-radius:14px;padding:1.2rem;margin:.4rem 0;}
.vhd{display:flex;align-items:center;gap:.6rem;margin-bottom:.8rem;}
.vnum{font-family:'Syne',sans-serif;font-weight:800;font-size:.9rem;color:var(--red);}
.vwords{font-size:.7rem;padding:.15rem .5rem;border-radius:20px;font-weight:700;}
.vtxt{color:var(--smoke);line-height:1.85;font-size:.9rem;white-space:pre-wrap;}

/* TTS links */
.tts-row{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem;}
.tts-link{display:inline-flex;align-items:center;gap:.4rem;padding:.45rem .9rem;border-radius:30px;text-decoration:none;font-family:'Syne',sans-serif;font-weight:700;font-size:.8rem;border:1px solid;transition:all .2s;}
.tts-link:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.35);}

/* ── AVATAR ── */
.av-wrap{background:var(--s2);border:1px solid var(--bord);border-radius:20px;padding:1.6rem;}
.av-head{display:flex;align-items:center;gap:1.2rem;margin-bottom:1.5rem;padding-bottom:1.2rem;border-bottom:1px solid var(--bord);}
.av-orb{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,var(--red),var(--amber));display:flex;align-items:center;justify-content:center;font-size:2.2rem;flex-shrink:0;box-shadow:0 8px 30px rgba(255,45,85,.35);}
.av-name{font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;}
.av-role{font-size:.82rem;color:var(--smoke);margin-top:.15rem;}
.av-sec{background:var(--s3);border-radius:12px;padding:1rem;}
.av-sec-title{font-family:'Syne',sans-serif;font-weight:700;font-size:.68rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:.7rem;}
.av-kv{display:flex;gap:.6rem;margin:.3rem 0;align-items:flex-start;}
.av-k{font-size:.68rem;color:var(--smoke);letter-spacing:1px;text-transform:uppercase;width:85px;flex-shrink:0;padding-top:.12rem;}
.av-v{font-size:.87rem;flex:1;}
.av-pill{display:inline-block;padding:.18rem .5rem;border-radius:20px;font-size:.72rem;margin:.12rem;border:1px solid rgba(255,255,255,.1);}
.av-item{padding:.3rem .65rem;font-size:.84rem;border-radius:6px;margin:.2rem 0;}
.phrase-box{background:linear-gradient(135deg,rgba(255,45,85,.1),rgba(255,159,10,.08));border:1px solid rgba(255,159,10,.28);border-radius:14px;padding:1.3rem;text-align:center;margin-top:1rem;}
.phrase-text{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:600;font-style:italic;line-height:1.65;}

/* ── BUBBLES ── */
.bub-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.6rem;margin-top:.6rem;}
@media(max-width:900px){.bub-grid{grid-template-columns:repeat(3,1fr);}}
@media(max-width:550px){.bub-grid{grid-template-columns:repeat(2,1fr);}}
.bub{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:.85rem .5rem;border-radius:14px;text-decoration:none;text-align:center;transition:all .3s cubic-bezier(.34,1.56,.64,1);border:1px solid rgba(255,255,255,.09);min-height:72px;gap:.32rem;position:relative;overflow:hidden;}
.bub::after{content:'';position:absolute;inset:0;opacity:0;transition:opacity .2s;background:linear-gradient(135deg,rgba(255,255,255,.07),transparent);}
.bub:hover{transform:translateY(-5px) scale(1.06);box-shadow:0 12px 35px rgba(0,0,0,.4);}
.bub:hover::after{opacity:1;}
.bub-ico{font-size:1.4rem;}
.bub-lbl{font-family:'Syne',sans-serif;font-weight:700;font-size:.78rem;letter-spacing:.3px;}

/* ── THUMBNAILS ── */
.thumb-grid{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:.5rem;}
.thumb{display:flex;flex-direction:column;align-items:center;gap:.25rem;}
.thumb img{width:90px;height:90px;object-fit:cover;border-radius:12px;border:1px solid var(--bord);transition:transform .2s,box-shadow .2s;}
.thumb img:hover{transform:scale(1.1);box-shadow:0 8px 24px rgba(0,0,0,.4);}
.thumb a{font-size:.62rem;color:var(--smoke);text-decoration:none;}
.thumb a:hover{color:var(--red);}

/* ── MISC ── */
.fbud{text-align:center;padding:1.2rem;}
.fbud-num{font-family:'Syne',sans-serif;font-size:3.5rem;font-weight:800;line-height:1;}
.fbud-sub{color:var(--smoke);font-size:.82rem;margin-top:.3rem;}
.tip{background:rgba(255,159,10,.07);border:1px solid rgba(255,159,10,.18);border-radius:10px;padding:.8rem 1rem;font-size:.83rem;color:var(--smoke);line-height:1.7;margin-top:.8rem;}
.tip b{color:var(--amber);}
.hdiv{height:1px;background:var(--bord);margin:1.1rem 0;}
.tag{font-size:.68rem;letter-spacing:1.5px;text-transform:uppercase;color:var(--smoke);margin-bottom:.2rem;}

/* welcome */
.welcome{text-align:center;padding:4.5rem 2rem;}
.welcome-icon{font-size:4rem;display:inline-block;animation:bounce 2s ease-in-out infinite;}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.welcome-title{font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:var(--red);margin:.8rem 0;}
.welcome-sub{color:var(--smoke);font-size:.9rem;max-width:500px;margin:0 auto;line-height:1.7;}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;margin-top:2rem;}
@media(max-width:700px){.feat-grid{grid-template-columns:1fr 1fr;}}
.feat{background:var(--s1);border:1px solid var(--bord);border-radius:14px;padding:1.1rem;text-align:center;transition:all .25s;}
.feat:hover{border-color:rgba(255,45,85,.35);transform:translateY(-3px);}
.feat-e{font-size:1.8rem;margin-bottom:.4rem;}
.feat-t{font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem;color:var(--amber);margin-bottom:.25rem;}
.feat-d{font-size:.77rem;color:var(--smoke);line-height:1.5;}

::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:var(--ink)}::-webkit-scrollbar-thumb{background:var(--red);border-radius:2px}
</style>
""", unsafe_allow_html=True)

# ── COPY SCRIPT ─────────────────────────────────────
COPY_JS = """
<script>
function copyText(id){
  var el=document.getElementById(id);
  if(!el)return;
  var txt=el.innerText||el.textContent;
  var btn=document.getElementById('btn_'+id);
  navigator.clipboard.writeText(txt).then(function(){
    btn.innerText='✅';btn.style.background='#32d4a4';btn.style.borderColor='#32d4a4';
    setTimeout(function(){btn.innerText='📋';btn.style.background='';btn.style.borderColor='';},2000);
  }).catch(function(){
    var ta=document.createElement('textarea');ta.value=txt;
    ta.style.position='fixed';ta.style.opacity='0';
    document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy');}catch(e){}
    document.body.removeChild(ta);
    btn.innerText='✅';
    setTimeout(function(){btn.innerText='📋';},2000);
  });
}
</script>
"""
st.markdown(COPY_JS, unsafe_allow_html=True)

_copy_counter = [0]
def copy_block(text, label=""):
    _copy_counter[0] += 1
    uid = f"cb_{_copy_counter[0]}"
    safe = str(text).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    if label:
        st.markdown(f'<div class="tag">{label}</div>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="cblock">
  <div class="ctext" id="{uid}">{safe}</div>
  <div class="cico" id="btn_{uid}" onclick="copyText('{uid}')" title="Copier">📋</div>
</div>""", unsafe_allow_html=True)

def make_bubs(items):
    # items = (label, url, color, bg, icon)
    cells = "".join([
        f'<a href="{url}" target="_blank" class="bub" style="background:{bg};border-color:{clr}33;">'
        f'<span class="bub-ico">{ico}</span>'
        f'<span class="bub-lbl" style="color:{clr};">{lbl}</span></a>'
        for lbl,url,clr,bg,ico in items
    ])
    st.markdown(f'<div class="bub-grid">{cells}</div>', unsafe_allow_html=True)

# ── SESSION ──────────────────────────────────────────
for k,v in {"gen":False,"pname":"","pimages":[],"pcost":0,"ptarget":5,"res":{},"form_open":True}.items():
    if k not in st.session_state: st.session_state[k]=v

GROQ_KEY = st.secrets.get("GROQ_API_KEY","")

PAYS = ["Togo","Mali","Bénin","Guinée","Côte d'Ivoire","Congo","Sénégal","Cameroun","Burkina Faso","Niger","RDC","Madagascar","Rwanda","Gabon"]
CODES = {"Togo":"TG","Mali":"ML","Bénin":"BJ","Guinée":"GN","Côte d'Ivoire":"CI","Congo":"CG","Sénégal":"SN","Cameroun":"CM","Burkina Faso":"BF","Niger":"NE","RDC":"CD","Madagascar":"MG","Rwanda":"RW","Gabon":"GA"}

def groq_call(prompt, system="", tokens=2500):
    if not GROQ_KEY: return '{"error":"Clé GROQ_API_KEY manquante dans Secrets"}'
    try:
        msgs = ([{"role":"system","content":system}] if system else []) + [{"role":"user","content":prompt}]
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"llama-3.3-70b-versatile","messages":msgs,"max_tokens":tokens,"temperature":.82},
            timeout=90)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f'{{"error":"{str(e)[:120]}"}}'

def parse_json(raw):
    if not raw: return {}
    clean = re.sub(r"```json|```","", raw).strip()
    try: return json.loads(clean)
    except:
        # try to find first { ... }
        m = re.search(r'\{.*\}', clean, re.DOTALL)
        if m:
            try: return json.loads(m.group())
            except: pass
        return {}

def calc_price(cost, pub=5000, cl=1000, liv=2000):
    rec = cost + 10000
    return {"min":cost+8000,"max":cost+12000,"rec":rec,"profit":rec-cost-pub-cl-liv,"pub":pub,"cl":cl,"liv":liv}

# ── HERO ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-glow"></div>
  <div class="orb" style="width:350px;height:350px;background:rgba(255,45,85,.07);top:-120px;left:-120px;animation-duration:18s;"></div>
  <div class="orb" style="width:250px;height:250px;background:rgba(255,159,10,.06);bottom:-100px;right:-80px;animation-duration:22s;animation-delay:4s;"></div>
  <div class="orb" style="width:180px;height:180px;background:rgba(50,212,164,.05);top:20%;right:10%;animation-duration:28s;animation-delay:8s;"></div>
  <div class="pt" style="left:5%;width:5px;height:5px;background:#ff2d55;animation-duration:8s;"></div>
  <div class="pt" style="left:18%;width:3px;height:3px;background:#ff9f0a;animation-duration:11s;animation-delay:1.2s;"></div>
  <div class="pt" style="left:33%;width:4px;height:4px;background:#32d4a4;animation-duration:9.5s;animation-delay:2s;"></div>
  <div class="pt" style="left:50%;width:5px;height:5px;background:#ff2d55;animation-duration:7.5s;animation-delay:.5s;"></div>
  <div class="pt" style="left:67%;width:3px;height:3px;background:#ffd60a;animation-duration:13s;animation-delay:1.8s;"></div>
  <div class="pt" style="left:82%;width:4px;height:4px;background:#ff9f0a;animation-duration:10s;animation-delay:3s;"></div>
  <div class="pt" style="left:93%;width:3px;height:3px;background:#32d4a4;animation-duration:8.5s;animation-delay:2.5s;"></div>
  <div class="hero-title">E-Commerce<br><span class="r">Master</span> <span class="a">Labo Pro</span></div>
  <div class="hero-sub">🌍 Tout en un pour réussir votre e-commerce en Afrique</div>
  <div class="hero-bar"></div>
</div>
""", unsafe_allow_html=True)

# ── TOGGLE CENTRÉ ────────────────────────────────────
_, mc, _ = st.columns([1,2,1])
with mc:
    tog_lbl = "🔼 Masquer le formulaire" if st.session_state.form_open else "🔽 Remplir les informations produit"
    if st.button(tog_lbl, key="tog", use_container_width=True):
        st.session_state.form_open = not st.session_state.form_open
        st.rerun()

# ── FORMULAIRE ───────────────────────────────────────
if st.session_state.form_open:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="pt-title">📦 Informations produit</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns([2,1,1])
    with c1: pname = st.text_input("Nom du produit", placeholder="Ex: Pince multifonction 11-en-1", value=st.session_state.pname)
    with c2: pcost = st.number_input("Prix d'achat (FCFA)", min_value=0, step=500, value=int(st.session_state.pcost))
    with c3: ptarget = st.number_input("Objectif ventes/jour", min_value=1, max_value=100, value=int(st.session_state.ptarget))
    c4,c5,c6 = st.columns(3)
    with c4: ppub = st.number_input("Publicité/vente (FCFA)", value=5000, step=500)
    with c5: pcl  = st.number_input("Closing/vente (FCFA)",  value=1000, step=100)
    with c6: pliv = st.number_input("Livraison/vente (FCFA)",value=2000, step=500)

    st.markdown("**Photos du produit** (1 à 10, côte à côte)")
    uploaded = st.file_uploader("", type=["jpg","jpeg","png","webp"], accept_multiple_files=True, label_visibility="collapsed")
    if uploaded:
        if len(uploaded) > 10: uploaded = uploaded[:10]; st.warning("Max 10 images.")
        st.session_state.pimages = uploaded
        st.markdown('<div class="thumb-grid">', unsafe_allow_html=True)
        for img in uploaded:
            img.seek(0)
            b64 = base64.b64encode(img.read()).decode()
            ext = img.name.split(".")[-1]
            st.markdown(f'<div class="thumb"><img src="data:image/{ext};base64,{b64}"><a href="data:image/{ext};base64,{b64}" download="{img.name}">⬇ DL</a></div>', unsafe_allow_html=True)
            img.seek(0)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, bc, _ = st.columns([1,2,1])
    with bc: go = st.button("⚡ LANCER L'ANALYSE COMPLÈTE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if go:
        if not pname:    st.error("❌ Entrez le nom du produit"); st.stop()
        if pcost == 0:   st.error("❌ Entrez le prix d'achat"); st.stop()
        if not GROQ_KEY: st.error("❌ Ajoutez GROQ_API_KEY dans Streamlit → Settings → Secrets"); st.stop()

        st.session_state.pname = pname; st.session_state.pcost = pcost; st.session_state.ptarget = ptarget
        PR = calc_price(pcost, ppub, pcl, pliv); st.session_state.res["pricing"] = PR

        SYS = (f"Tu es expert e-commerce africain et copywriter neuromarketing. "
               f"Produit EXACT: '{pname}'. Achat: {pcost} FCFA. Vente: {PR['rec']} FCFA. "
               f"Marge brute: {PR['profit']} FCFA. Objectif: {ptarget} ventes/jour. "
               f"Contexte: marché africain francophone (Togo, Côte d'Ivoire, Sénégal, Cameroun…). "
               f"Réponds UNIQUEMENT en français. Tous tes textes parlent EXCLUSIVEMENT de '{pname}'.")

        bar = st.progress(0, "⚙️ Analyse en cours…")

        # SCORE
        bar.progress(10, "🎯 Score produit…")
        raw = groq_call(f"""Évalue '{pname}' pour le marché africain. Note STRICTE /10 (sois honnête, pas trop généreux).
Retourne UNIQUEMENT ce JSON (sans texte avant ou après, sans markdown):
{{"score":6.5,"verdict":"Correct","couleur":"amber","criteres":[
  {{"nom":"💰 Rentabilité","note":7,"explication":"La marge de {PR['profit']} FCFA permet... [explication spécifique]"}},
  {{"nom":"📈 Demande en Afrique","note":6,"explication":"[demande réelle de '{pname}' en Afrique francophone]"}},
  {{"nom":"⚔️ Concurrence locale","note":5,"explication":"[concurrence réelle pour '{pname}']"}},
  {{"nom":"📦 Approvisionnement","note":7,"explication":"[facilité de trouver '{pname}' sur AliExpress/Alibaba]"}},
  {{"nom":"🎨 Créatives disponibles","note":6,"explication":"[photos/vidéos disponibles pour '{pname}']"}},
  {{"nom":"🔥 Viral FB/TikTok","note":7,"explication":"[potentiel viral de '{pname}' sur les réseaux africains]"}},
  {{"nom":"🌍 Problème africain résolu","note":8,"explication":"[problème concret résolu par '{pname}' en Afrique]"}},
  {{"nom":"💵 Prix accessible","note":6,"explication":"[{PR['rec']} FCFA vs revenus africains 35k-200k FCFA/mois]"}},
  {{"nom":"🔄 Fidélisation","note":5,"explication":"[les clients rachètent-ils '{pname}' ?]"}},
  {{"nom":"📅 Saisonnalité","note":7,"explication":"[saisonnalité de '{pname}' en Afrique]"}}
],
"forts":["force concrète 1 de {pname}","force 2","force 3"],
"faibles":["faiblesse 1","faiblesse 2"],
"conseil":"3 phrases stratégiques concrètes pour vendre '{pname}' en Afrique.",
"pays":["pays1","pays2","pays3"],
"periode":"Période optimale de vente"}}""", SYS, 1500)
        st.session_state.res["score"] = parse_json(raw)
        if not st.session_state.res["score"]:
            st.session_state.res["score"] = {"score":6.5,"verdict":"Correct","couleur":"amber","criteres":[{"nom":"💰 Rentabilité","note":7,"explication":"Marge correcte pour le marché"}],"forts":["Bonne marge"],"faibles":["Concurrence"],"conseil":"Testez avec 3$/jour sur Facebook.","pays":["Côte d'Ivoire","Sénégal","Cameroun"],"periode":"Toute l'année"}

        # OFFRES
        bar.progress(22, "🎁 Offres…")
        raw = groq_call(f"""Génère 5 offres marketing SPÉCIFIQUES à '{pname}' pour le marché africain.
Retourne UNIQUEMENT ce JSON:
{{"offres":[
  {{"emoji":"🚚","titre":"Nom offre 1 adaptée à {pname}","desc":"Description précise de l'offre pour {pname}","impact":"Élevé","conseil":"Conseil pratique africain"}},
  {{"emoji":"🎁","titre":"Offre 2","desc":"desc","impact":"Fort","conseil":"conseil"}},
  {{"emoji":"💰","titre":"Offre 3","desc":"desc","impact":"Élevé","conseil":"conseil"}},
  {{"emoji":"⭐","titre":"Offre 4","desc":"desc","impact":"Moyen","conseil":"conseil"}},
  {{"emoji":"🏆","titre":"Offre 5","desc":"desc","impact":"Fort","conseil":"conseil"}}
]}}""", SYS, 900)
        st.session_state.res["offres"] = parse_json(raw)
        if not st.session_state.res["offres"]:
            st.session_state.res["offres"] = {"offres":[{"emoji":"🚚","titre":"Livraison gratuite","desc":"Supprime le frein principal à l'achat en Afrique.","impact":"Élevé","conseil":"Intégrez le coût dans votre prix de vente."}]}

        # SHOPIFY
        bar.progress(36, "🛍️ Shopify…")
        raw = groq_call(f"""Crée du contenu Shopify pour '{pname}'.
RÈGLES ABSOLUES:
1. Les titres de paragraphes = PROMESSES DE RÉSULTAT concrètes de '{pname}' (PAS: Présentation, Avantages, Caractéristiques, Description)
2. Chaque texte de paragraphe = 4 phrases maximum, bien séparées par des sauts de ligne
3. Tout parle UNIQUEMENT de '{pname}' et de ses bénéfices réels
Retourne UNIQUEMENT ce JSON:
{{"titres":["Titre SEO 1 promesse de {pname}","Titre SEO 2 résultat de {pname}","Titre SEO 3 transformation de {pname}"],
"paragraphes":[
  {{"titre":"Promesse résultat 1 de {pname}","texte":"Phrase 1 sur le bénéfice de {pname}.\n\nPhrase 2 développant ce bénéfice.\n\nPhrase 3 avec exemple concret.\n\nPhrase 4 appelant à l'action."}},
  {{"titre":"Promesse 2","texte":"Phrase 1.\n\nPhrase 2.\n\nPhrase 3.\n\nPhrase 4."}},
  {{"titre":"Promesse 3","texte":"Phrase 1.\n\nPhrase 2.\n\nPhrase 3.\n\nPhrase 4."}},
  {{"titre":"Promesse 4","texte":"Phrase 1.\n\nPhrase 2.\n\nPhrase 3.\n\nPhrase 4."}},
  {{"titre":"Promesse 5","texte":"Phrase 1.\n\nPhrase 2.\n\nPhrase 3.\n\nPhrase 4."}},
  {{"titre":"Promesse 6","texte":"Phrase 1.\n\nPhrase 2.\n\nPhrase 3.\n\nPhrase 4."}}
]}}""", SYS, 2500)
        st.session_state.res["shopify"] = parse_json(raw)
        if not st.session_state.res["shopify"]:
            st.session_state.res["shopify"] = {"titres":[f"{pname} — La solution","Résultats rapides avec {pname}","Transformez votre quotidien"],"paragraphes":[{"titre":f"Ce que {pname} change dans votre vie","texte":"Ce produit résout un problème réel.\n\nDes milliers de clients satisfaits en Afrique.\n\nRésultats visibles rapidement.\n\nCommandez maintenant."}]}

        # FB ADS
        bar.progress(50, "📢 Facebook Ads…")
        raw = groq_call(f"""3 textes pub Facebook pour '{pname}', marché africain.
Max 70 mots chacun. Structure: ligne 1 = accroche CHOC propre à '{pname}' (surprenante, pas générique), puis 3 bénéfices en tirets spécifiques à '{pname}'.
Retourne UNIQUEMENT ce JSON:
{{"ads":[
  {{"accroche":"ACCROCHE CHOC SPÉCIFIQUE À {pname}","b1":"Bénéfice 1 concret de {pname}","b2":"Bénéfice 2","b3":"Bénéfice 3","mots":45}},
  {{"accroche":"ACCROCHE 2","b1":"b1","b2":"b2","b3":"b3","mots":48}},
  {{"accroche":"ACCROCHE 3","b1":"b1","b2":"b2","b3":"b3","mots":50}}
]}}""", SYS, 900)
        st.session_state.res["fb"] = parse_json(raw)
        if not st.session_state.res["fb"]:
            st.session_state.res["fb"] = {"ads":[{"accroche":f"Ce que {pname} fait en 5 minutes surprend tout le monde","b1":"Résultat immédiat et visible","b2":"Utilisable partout en Afrique","b3":"Satisfait ou remboursé","mots":40}]}

        # VOIX OFF
        bar.progress(63, "🎙️ Voix off…")
        raw = groq_call(f"""3 scripts voix off pour '{pname}', marché africain francophone.
RÈGLE ABSOLUE: chaque script = exactement 120 à 140 mots. Parle UNIQUEMENT de '{pname}'.
Structure obligatoire de chaque script:
[PROBLÈME] 2-3 phrases sur le problème vécu par le client
[SOLUTION] Présente '{pname}' comme la solution
[FONCTIONNEMENT] 2-3 phrases sur comment {pname} agit concrètement
[TÉMOIGNAGE] 2-3 phrases avec prénom africain réaliste (Aminata, Kofi, Fatou, Ibrahim, Moussa, Aïssatou, Seydou, Mariam, Oumar, Binta)
Neuromarketing: émotions fortes, urgence, identification.
Retourne UNIQUEMENT ce JSON:
{{"scripts":[
  {{"texte":"[Script 1 de 120-140 mots ici, spécifique à {pname}]","mots":125}},
  {{"texte":"[Script 2 different du 1er]","mots":132}},
  {{"texte":"[Script 3 different des deux autres]","mots":128}}
]}}""", SYS, 3000)
        st.session_state.res["voix"] = parse_json(raw)
        if not st.session_state.res["voix"]:
            st.session_state.res["voix"] = {"scripts":[{"texte":f"Vous en avez assez de ce problème quotidien ?\n\n{pname} est enfin là pour changer votre vie.\n\nSimple, efficace, livré chez vous.\n\nFatou de Dakar témoigne : 'Ce produit a tout changé pour moi.'","mots":35}]}

        # AVATAR — prompt enrichi et adapté au genre du produit
        bar.progress(80, "👤 Avatar…")
        raw = groq_call(f"""Crée l'avatar client idéal pour '{pname}' en Afrique francophone.
IMPORTANT: adapte le profil AU TYPE DE PRODUIT '{pname}'. Si c'est un outil pour homme, mets un homme. Si cosmétique, femme. Sois logique.
L'avatar doit être UNIQUE et DIFFÉRENT à chaque fois (prénom africain varié, pas toujours Aminata).
Retourne UNIQUEMENT ce JSON:
{{"prenom":"[prénom africain adapté au profil]",
"emoji":"[emoji adapté: homme/femme/etc]",
"sexe":"[Homme ou Femme selon le produit]",
"age":"[tranche d'âge réaliste pour {pname}]",
"situation":"[situation familiale réaliste]",
"revenus":"[revenus mensuels en FCFA réalistes pour l'Afrique, ex: 80 000 – 150 000 FCFA/mois]",
"profession":"[profession réaliste pour quelqu'un qui achète {pname} en Afrique]",
"ville":"[grandes villes africaines adaptées]",
"reseaux":["réseau 1","réseau 2","réseau 3"],
"heure":"[heure active sur les réseaux]",
"peurs":["peur 1 directement liée à {pname}","peur 2","peur 3"],
"frustrations":["frustration 1 liée à {pname}","frustration 2","frustration 3"],
"desirs":["désir 1 lié à {pname}","désir 2","désir 3"],
"motivations":["motivation principale","motivation secondaire"],
"langage":["Expression africaine qu'il/elle utilise 1","Expression 2","Expression 3"],
"phrase_vendeur":"[La phrase que VOUS (le vendeur) dites à ce client pour déclencher l'achat de {pname}]",
"objections":["objection courante 1","objection 2"],
"reponses":["réponse convaincante à l'objection 1","réponse à l'objection 2"],
"pour_qui":"[pour qui achète-t-il/elle {pname}]",
"budget":"[budget max acceptable pour {pname}]",
"livraison":"[préférence livraison]"}}""", SYS, 1400)
        st.session_state.res["avatar"] = parse_json(raw)
        if not st.session_state.res["avatar"]:
            st.session_state.res["avatar"] = {"prenom":"Kofi","emoji":"👨","sexe":"Homme","age":"25-40 ans","situation":"Célibataire ou marié","revenus":"80 000 – 160 000 FCFA/mois","profession":"Technicien / Artisan","ville":"Abidjan, Accra, Lomé","reseaux":["Facebook","WhatsApp"],"heure":"20h-23h","peurs":["Produit de mauvaise qualité"],"frustrations":["Matériel qui casse vite"],"desirs":["Trouver un produit fiable"],"motivations":["Efficacité","Économies"],"langage":["C'est quoi le prix ?","Ça vaut vraiment ?"],"phrase_vendeur":f"Ce {pname} vous fait économiser du temps et de l'argent dès le premier jour.","objections":["C'est trop cher"],"reponses":["Paiement à la livraison disponible"],"pour_qui":"Pour lui-même","budget":"15 000 FCFA","livraison":"À domicile"}

        bar.progress(100, "✅ Terminé !")
        st.session_state.gen = True
        st.session_state.form_open = False
        st.balloons()
        st.rerun()

# ── WELCOME ──────────────────────────────────────────
if not st.session_state.gen:
    if not st.session_state.form_open:
        st.markdown("""<div class="welcome">
          <div class="welcome-icon">⚡</div>
          <div class="welcome-title">Prêt à analyser votre produit ?</div>
          <div class="welcome-sub">Remplissez le formulaire ci-dessus et lancez votre analyse IA complète gratuite.</div>
          <div class="feat-grid">
            <div class="feat"><div class="feat-e">💰</div><div class="feat-t">Prix &amp; Gains</div><div class="feat-d">Tableau rentabilité + budget pub Facebook</div></div>
            <div class="feat"><div class="feat-e">🎯</div><div class="feat-t">Score Produit</div><div class="feat-d">10 critères avec explication détaillée</div></div>
            <div class="feat"><div class="feat-e">🛍️</div><div class="feat-t">Shopify</div><div class="feat-d">3 titres SEO + 6 paragraphes bénéfices</div></div>
            <div class="feat"><div class="feat-e">📢</div><div class="feat-t">Facebook Ads</div><div class="feat-d">3 textes ≤70 mots prêts à copier</div></div>
            <div class="feat"><div class="feat-e">🎙️</div><div class="feat-t">Voix Off</div><div class="feat-d">3 scripts 120-140 mots + liens TTS</div></div>
            <div class="feat"><div class="feat-e">👤</div><div class="feat-t">Avatar Client</div><div class="feat-d">Profil psychologique + phrase vendeur</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════
#  RÉSULTATS
# ══════════════════════════════════════════════════════
R = st.session_state.res
PN = st.session_state.pname
PR = R.get("pricing", {})
Q  = urllib.parse.quote(PN)

tabs = st.tabs(["💰 Prix & Gains","🎯 Score","🎁 Offres","🛍️ Shopify","📢 Facebook Ads","🎙️ Voix Off","👤 Avatar","🖼️ Images","🎬 Vidéos","⚔️ Concurrence"])

# ══ TAB 1 : PRIX ════════════════════════════════════
with tabs[0]:
    sell=PR.get("rec",0); profit=PR.get("profit",0)
    pub=PR.get("pub",5000); cl=PR.get("cl",1000); liv=PR.get("liv",2000)
    cost=st.session_state.pcost; tg=st.session_state.ptarget

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="pt-title">💰 Stratégie de prix — {PN}</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col,lbl,val,cls in [(cols[0],"Prix minimum",PR.get("min",0),"mv-a"),(cols[1],"Prix recommandé",sell,"mv-r"),(cols[2],"Prix maximum",PR.get("max",0),"mv-a"),(cols[3],"Bénéfice net/vente",profit,"mv-g")]:
        with col: st.markdown(f'<div class="metric"><div class="mv {cls}">{val:,} FCFA</div><div class="ml">{lbl}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="pt-title">📊 Charges par vente</div>', unsafe_allow_html=True)
    cols2 = st.columns(4)
    for col,lbl,val,cls in [(cols2[0],"📣 Publicité",pub,"mv-r"),(cols2[1],"📞 Closing",cl,"mv-a"),(cols2[2],"🚚 Livraison",liv,"mv-a"),(cols2[3],"💚 Votre gain NET",profit,"mv-g")]:
        with col: st.markdown(f'<div class="metric"><div class="mv {cls}">{val:,} FCFA</div><div class="ml">{lbl}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="pt-title">📈 Tableau de gains — 1 à 10 ventes/jour</div>', unsafe_allow_html=True)
    rows = ""
    for v in range(1,11):
        ca=v*sell; cp=v*cost; dp=v*pub; dc=v*cl; dl=v*liv; bn=ca-cp-dp-dc-dl; bm=bn*30
        cc = "cg" if bn>0 else "cr"
        rows += f"<tr><td><b>{v}</b></td><td class='ca'>{ca:,}</td><td class='cr'>{cp:,}</td><td class='cr'>{dp:,}</td><td class='cr'>{dc:,}</td><td class='cr'>{dl:,}</td><td class='{cc}'>{bn:,}</td><td class='{cc}'>{bm:,}</td></tr>"
    st.markdown(f'<table class="tbl"><thead><tr><th>Ventes/j</th><th>CA FCFA</th><th>Coût prod.</th><th>Pub</th><th>Closing</th><th>Livraison</th><th>Bénéf./j</th><th>Bénéf./mois</th></tr></thead><tbody>{rows}</tbody></table>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="pt-title">📣 Budget Facebook Ads recommandé</div>', unsafe_allow_html=True)
    if tg<=5:    fb=("3 – 5 $","1 créative","#32d4a4","Idéal pour démarrer et tester")
    elif tg<=10: fb=("5 – 8 $","1-2 créatives","#ff9f0a","Bon compromis budget/résultats")
    elif tg<=20: fb=("10 – 15 $","2-3 créatives","#ff2d55","Budget sérieux pour scaler")
    else:        fb=("15 $+","3+ créatives","#bf5af2","Mode scale avancé")
    st.markdown(f'<div class="fbud"><div class="fbud-num" style="color:{fb[2]};">{fb[0]} <span style="font-size:1.3rem;color:#9999bb;">/ jour</span></div><div class="fbud-sub">{fb[3]} — Objectif : {tg} ventes/jour ({fb[1]})</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tip">💡 <b>Stratégie :</b> Démarrez avec 1 seule créative. Si après 3 jours votre coût par achat (CPA) est inférieur à <b>{profit:,} FCFA</b>, augmentez le budget de 20% tous les 2-3 jours. En Afrique, les publicités fonctionnent mieux entre 18h et 22h heure locale.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 2 : SCORE ════════════════════════════════════
with tabs[1]:
    SD = R.get("score", {})
    sv = float(SD.get("score", 7))
    verdict = SD.get("verdict", "Correct")
    couleur = SD.get("couleur", "amber")
    sc = {"red":"#ff2d55","amber":"#ff9f0a","green":"#32d4a4","orange":"#ff9f0a"}.get(couleur, "#ff9f0a")
    circ = int((sv/10)*251)

    cS, cD = st.columns([1, 2])
    with cS:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align:center;padding:1.2rem 0;">
          <svg width="175" height="175" viewBox="0 0 100 100" style="filter:drop-shadow(0 0 28px {sc}66)">
            <circle cx="50" cy="50" r="40" fill="none" stroke="#1e1e35" stroke-width="10"/>
            <circle cx="50" cy="50" r="40" fill="none" stroke="{sc}" stroke-width="10"
              stroke-dasharray="{circ} {251-circ}" stroke-dashoffset="63" stroke-linecap="round"/>
            <text x="50" y="46" text-anchor="middle" font-family="Syne,sans-serif" font-size="22" font-weight="800" fill="{sc}">{sv}</text>
            <text x="50" y="60" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="8" fill="#9999bb">/ 10</text>
          </svg>
          <div style="font-family:Syne,sans-serif;font-weight:800;font-size:1.4rem;color:{sc};margin-top:.4rem;">{verdict}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:.68rem;letter-spacing:2px;text-transform:uppercase;color:#32d4a4;margin-bottom:.4rem;">✅ Points forts</div>', unsafe_allow_html=True)
        for p in SD.get("forts", []):
            st.markdown(f'<div style="padding:.38rem .7rem;background:rgba(50,212,164,.08);border-left:2px solid #32d4a4;border-radius:0 6px 6px 0;margin:.22rem 0;font-size:.83rem;">✅ {p}</div>', unsafe_allow_html=True)
        st.markdown('<div class="hdiv"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:.68rem;letter-spacing:2px;text-transform:uppercase;color:#ff2d55;margin-bottom:.4rem;">⚠️ À améliorer</div>', unsafe_allow_html=True)
        for p in SD.get("faibles", []):
            st.markdown(f'<div style="padding:.38rem .7rem;background:rgba(255,45,85,.08);border-left:2px solid #ff2d55;border-radius:0 6px 6px 0;margin:.22rem 0;font-size:.83rem;">⚠️ {p}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cD:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="pt-title">📊 Analyse détaillée par critère</div>', unsafe_allow_html=True)
        for c in SD.get("criteres", []):
            v = c.get("note", 7); pct = v*10
            bc = "#32d4a4" if v>=7 else "#ff9f0a" if v>=5 else "#ff2d55"
            st.markdown(f"""<div class="crit-row">
              <div class="crit-top">
                <div class="crit-name">{c.get('nom','')}</div>
                <div class="crit-note" style="color:{bc};">{v}/10</div>
              </div>
              <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{bc};"></div></div>
              <div class="crit-why">💬 {c.get('explication','')}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown(f'<div class="tip" style="margin-top:1rem;"><b>🧭 Recommandation stratégique :</b><br>{SD.get("conseil","")}<br><br>🌍 <b>Marchés prioritaires :</b> {", ".join(SD.get("pays",[]))} &nbsp;|&nbsp; 📅 <b>Période :</b> {SD.get("periode","")}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 3 : OFFRES ═══════════════════════════════════
with tabs[2]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="pt-title">🎁 Offres marketing — {PN}</div>', unsafe_allow_html=True)
    for o in R.get("offres", {}).get("offres", []):
        imp = o.get("impact","Moyen")
        ic = "#32d4a4" if any(x in imp for x in ["Élevé","Fort","Très"]) else "#ff9f0a"
        st.markdown(f"""<div class="ocard">
          <div class="ocard-head">
            <div class="ocard-title">{o.get('emoji','🎯')} {o.get('titre','')}</div>
            <span class="ocard-badge" style="background:{ic}22;color:{ic};border:1px solid {ic}44;">{imp}</span>
          </div>
          <div style="font-size:.86rem;color:var(--smoke);margin-left:.4rem;">{o.get('desc','')}</div>
          <div class="ocard-tip">💡 {o.get('conseil','')}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 4 : SHOPIFY ══════════════════════════════════
with tabs[3]:
    SH = R.get("shopify", {})
    titres = SH.get("titres", [])
    paragraphes = SH.get("paragraphes", [])

    if titres:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="pt-title">🏷️ 3 Titres produit SEO</div>', unsafe_allow_html=True)
        for i, t in enumerate(titres, 1):
            if t and str(t).strip():
                st.markdown(f'<div class="tag">Titre {i}</div>', unsafe_allow_html=True)
                copy_block(str(t).strip())
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Titres non générés — relancez l'analyse.")

    if paragraphes:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="pt-title">📝 6 Paragraphes de description (bénéfices)</div>', unsafe_allow_html=True)
        for i, p in enumerate(paragraphes, 1):
            titre_p = str(p.get("titre","")).strip()
            texte_p = str(p.get("texte","")).strip()
            if titre_p or texte_p:
                if titre_p:
                    st.markdown(f'<div style="font-family:Syne,sans-serif;font-weight:700;font-size:.92rem;color:#ff9f0a;margin-top:1.1rem;margin-bottom:.3rem;">▶ {titre_p}</div>', unsafe_allow_html=True)
                if texte_p:
                    copy_block(texte_p)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Paragraphes non générés — relancez l'analyse.")

# ══ TAB 5 : FACEBOOK ADS ═════════════════════════════
with tabs[4]:
    ads = R.get("fb", {}).get("ads", [])
    if ads:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="pt-title">📢 Facebook Ads — {PN}</div>', unsafe_allow_html=True)
        for i, ad in enumerate(ads, 1):
            accroche = str(ad.get("accroche","")).strip()
            b1 = str(ad.get("b1","")).strip()
            b2 = str(ad.get("b2","")).strip()
            b3 = str(ad.get("b3","")).strip()
            mots = ad.get("mots","~")
            if accroche:
                st.markdown(f'<div class="tag" style="margin-top:.9rem;">Texte #{i} — {mots} mots</div>', unsafe_allow_html=True)
                st.markdown(f"""<div class="adcard">
                  <div class="adcard-hook">🔥 {accroche}</div>
                  {"<div class='adcard-pip'>"+b1+"</div>" if b1 else ""}
                  {"<div class='adcard-pip'>"+b2+"</div>" if b2 else ""}
                  {"<div class='adcard-pip'>"+b3+"</div>" if b3 else ""}
                </div>""", unsafe_allow_html=True)
                full_text = f"{accroche}"
                if b1: full_text += f"\n\n- {b1}"
                if b2: full_text += f"\n- {b2}"
                if b3: full_text += f"\n- {b3}"
                copy_block(full_text, "Copier ce texte")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Textes Facebook non générés — relancez l'analyse.")

# ══ TAB 6 : VOIX OFF ═════════════════════════════════
with tabs[5]:
    scripts = R.get("voix", {}).get("scripts", [])

    # TTS links
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="pt-title">🎧 Générer votre voix off (gratuit)</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.82rem;color:var(--smoke);margin-bottom:.7rem;">Copiez un script ci-dessous, puis collez-le sur l\'un de ces sites pour générer votre voix off :</div>', unsafe_allow_html=True)
    st.markdown("""<div class="tts-row">
      <a href="https://www.minimaxi.com/text-to-speech" target="_blank" class="tts-link" style="color:#ff9f0a;border-color:#ff9f0a44;background:rgba(255,159,10,.08);">🎙️ MiniMax TTS</a>
      <a href="https://elevenlabs.io" target="_blank" class="tts-link" style="color:#32d4a4;border-color:#32d4a444;background:rgba(50,212,164,.08);">🎙️ ElevenLabs</a>
      <a href="https://ttsmaker.com/fr" target="_blank" class="tts-link" style="color:#bf5af2;border-color:#bf5af244;background:rgba(191,90,242,.08);">🎙️ TTS Maker</a>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if scripts:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="pt-title">🎙️ Scripts voix off — {PN}</div>', unsafe_allow_html=True)
        for i, s in enumerate(scripts, 1):
            txt = str(s.get("texte","")).strip()
            mots = s.get("mots", len(txt.split()))
            if txt:
                mc = "#32d4a4" if 120<=mots<=140 else "#ff9f0a"
                st.markdown(f'<div class="vscript"><div class="vhd"><span class="vnum">🎙️ Script #{i}</span><span class="vwords" style="color:{mc};background:{mc}1a;border:1px solid {mc}44;">{mots} mots</span></div><div class="vtxt">{txt}</div></div>', unsafe_allow_html=True)
                copy_block(txt)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Scripts non générés — relancez l'analyse.")

# ══ TAB 7 : AVATAR ═══════════════════════════════════
with tabs[6]:
    AV = R.get("avatar", {})
    st.markdown('<div class="av-wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="av-head"><div class="av-orb">{AV.get("emoji","👤")}</div><div><div class="av-name">{AV.get("prenom","Avatar")} — Avatar Client Idéal</div><div class="av-role">{AV.get("profession","")} · {AV.get("ville","")}</div></div></div>', unsafe_allow_html=True)

    cL, cR = st.columns(2)
    with cL:
        st.markdown('<div class="av-sec">', unsafe_allow_html=True)
        st.markdown('<div class="av-sec-title" style="color:#ff9f0a;">👤 Profil démographique</div>', unsafe_allow_html=True)
        for lbl,key in [("Sexe","sexe"),("Âge","age"),("Situation","situation"),("Revenus","revenus"),("Profession","profession"),("En ligne","heure"),("Budget max","budget"),("Livraison","livraison"),("Achète pour","pour_qui")]:
            v = AV.get(key,"")
            if v: st.markdown(f'<div class="av-kv"><div class="av-k">{lbl}</div><div class="av-v">{v}</div></div>', unsafe_allow_html=True)
        rs = AV.get("reseaux",[])
        if rs:
            pills = "".join([f'<span class="av-pill">{s}</span>' for s in rs])
            st.markdown(f'<div class="av-kv"><div class="av-k">Réseaux</div><div class="av-v">{pills}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cR:
        st.markdown('<div class="av-sec">', unsafe_allow_html=True)
        st.markdown('<div class="av-sec-title" style="color:#ff2d55;">🧠 Profil psychologique</div>', unsafe_allow_html=True)
        for lbl,key,clr in [("😱 Peurs","peurs","#ff2d55"),("😤 Frustrations","frustrations","#ff9f0a"),("💫 Désirs","desirs","#bf5af2"),("⚡ Motivations","motivations","#32d4a4")]:
            items = AV.get(key,[])
            if items:
                st.markdown(f'<div style="font-size:.67rem;letter-spacing:1.5px;text-transform:uppercase;color:{clr};margin:.55rem 0 .22rem;">{lbl}</div>', unsafe_allow_html=True)
                for x in items:
                    st.markdown(f'<div class="av-item" style="background:{clr}11;border-left:2px solid {clr};">▸ {x}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Langage + objections/réponses
    cA, cB, cC = st.columns(3)
    with cA:
        lang = AV.get("langage",[])
        if lang:
            st.markdown('<div class="av-sec" style="margin-top:1rem;"><div class="av-sec-title" style="color:#ffd60a;">💬 Langage utilisé</div>', unsafe_allow_html=True)
            for x in lang: st.markdown(f'<div class="av-item" style="background:rgba(255,214,10,.08);border-left:2px solid #ffd60a;font-style:italic;">"{x}"</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with cB:
        objs = AV.get("objections",[])
        if objs:
            st.markdown('<div class="av-sec" style="margin-top:1rem;"><div class="av-sec-title" style="color:#ff9f0a;">❓ Objections</div>', unsafe_allow_html=True)
            for x in objs: st.markdown(f'<div class="av-item" style="background:rgba(255,159,10,.08);border-left:2px solid #ff9f0a;">▸ {x}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with cC:
        reps = AV.get("reponses",[])
        if reps:
            st.markdown('<div class="av-sec" style="margin-top:1rem;"><div class="av-sec-title" style="color:#32d4a4;">✅ Vos réponses</div>', unsafe_allow_html=True)
            for x in reps: st.markdown(f'<div class="av-item" style="background:rgba(50,212,164,.08);border-left:2px solid #32d4a4;">▸ {x}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    phrase = str(AV.get("phrase_vendeur", AV.get("phrase",""))).strip()
    if phrase:
        st.markdown(f'<div class="phrase-box"><div style="font-size:.67rem;letter-spacing:2px;text-transform:uppercase;color:#ff9f0a;margin-bottom:.5rem;">🎯 Phrase déclenchante (ce que VOUS dites au client)</div><div class="phrase-text">"{phrase}"</div></div>', unsafe_allow_html=True)
        copy_block(phrase)
    st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 8 : IMAGES ═══════════════════════════════════
with tabs[7]:
    if st.session_state.pimages:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="pt-title">📷 Vos photos uploadées</div>', unsafe_allow_html=True)
        st.markdown('<div class="thumb-grid">', unsafe_allow_html=True)
        for img in st.session_state.pimages:
            img.seek(0)
            b64 = base64.b64encode(img.read()).decode()
            ext = img.name.split(".")[-1]
            st.markdown(f'<div class="thumb"><img src="data:image/{ext};base64,{b64}"><a href="data:image/{ext};base64,{b64}" download="{img.name}">⬇ DL</a></div>', unsafe_allow_html=True)
            img.seek(0)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="pt-title">🔍 Rechercher des images de votre produit</div>', unsafe_allow_html=True)
    make_bubs([
        ("AliExpress",   f"https://fr.aliexpress.com/wholesale?SearchText={Q}",      "#ff6010","rgba(255,96,16,.15)","🟠"),
        ("Alibaba",      f"https://www.alibaba.com/trade/search?SearchText={Q}",      "#e6380a","rgba(230,56,10,.15)","🏭"),
        ("Pinterest",    f"https://www.pinterest.com/search/pins/?q={Q}",             "#e60023","rgba(230,0,35,.15)","📌"),
        ("Temu",         f"https://www.temu.com/search_result.html?search_key={Q}",   "#ff9f0a","rgba(255,159,10,.15)","🛒"),
        ("Google Images",f"https://www.google.com/search?q={Q}&tbm=isch",             "#4285f4","rgba(66,133,244,.15)","🔍"),
        ("Amazon",       f"https://www.amazon.fr/s?k={Q}",                            "#ff9900","rgba(255,153,0,.15)","📦"),
        ("Jumia",        f"https://www.jumia.com/catalog/?q={Q}",                     "#f68b1e","rgba(246,139,30,.15)","🛍️"),
        ("Cdiscount",    f"https://www.cdiscount.com/search/10/{Q}.html",             "#e4001b","rgba(228,0,27,.15)","💳"),
        ("Google Shop",  f"https://www.google.com/search?q={Q}&tbm=shop",             "#34a853","rgba(52,168,83,.15)","🛒"),
        ("eBay",         f"https://www.ebay.fr/sch/i.html?_nkw={Q}",                 "#e53238","rgba(229,50,56,.15)","🏷️"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 9 : VIDÉOS ════════════════════════════════════
with tabs[8]:
    plats = [
        ("▶️","YouTube",      "#ff0000","rgba(255,0,0,.15)",    lambda p: f"https://www.youtube.com/results?search_query={Q}+{urllib.parse.quote(p)}"),
        ("🎵","TikTok",       "#69c9d0","rgba(105,201,208,.15)",lambda p: f"https://www.tiktok.com/search?q={Q}+{urllib.parse.quote(p)}"),
        ("📌","Pinterest",    "#e60023","rgba(230,0,35,.15)",    lambda p: f"https://www.pinterest.com/search/pins/?q={Q}+{urllib.parse.quote(p)}"),
        ("🔍","Google Vidéos","#4285f4","rgba(66,133,244,.15)", lambda p: f"https://www.google.com/search?q={Q}+{urllib.parse.quote(p)}&tbm=vid"),
        ("🟠","AliExpress",   "#ff6010","rgba(255,96,16,.15)",  lambda p: f"https://fr.aliexpress.com/wholesale?SearchText={Q}"),
        ("📘","Facebook",     "#1877f2","rgba(24,119,242,.15)", lambda p: f"https://www.facebook.com/search/videos/?q={Q}+{urllib.parse.quote(p)}"),
    ]
    for ico,plat,clr,bg,make in plats:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="pt-title">{ico} {plat}</div>', unsafe_allow_html=True)
        make_bubs([(p, make(p), clr, bg, "🌍") for p in PAYS])
        st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 10 : CONCURRENCE ══════════════════════════════
with tabs[9]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="pt-title">📚 Bibliothèque Publicitaire Facebook — par pays</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.8rem;color:var(--smoke);margin-bottom:.6rem;">Voyez toutes les pubs actives de vos concurrents</div>', unsafe_allow_html=True)
    make_bubs([(p, f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={CODES.get(p,'TG')}&q={Q}&search_type=keyword_unordered", "#1877f2","rgba(24,119,242,.15)","📘") for p in PAYS])
    st.markdown('</div>', unsafe_allow_html=True)

    conc = [
        ("🛒","Boutiques Facebook",  "#1877f2","rgba(24,119,242,.15)", lambda p: f"https://www.facebook.com/search/pages/?q={Q}+boutique+{urllib.parse.quote(p)}"),
        ("🌐","Google Shopping",     "#4285f4","rgba(66,133,244,.15)", lambda p: f"https://www.google.com/search?q={Q}+boutique+{urllib.parse.quote(p)}&tbm=shop"),
        ("🟠","AliExpress vendeurs", "#ff6010","rgba(255,96,16,.15)",  lambda p: f"https://fr.aliexpress.com/wholesale?SearchText={Q}"),
        ("🛍️","Jumia",              "#f68b1e","rgba(246,139,30,.15)", lambda p: f"https://www.jumia.com/catalog/?q={Q}"),
        ("🔵","Glovo / Yango",      "#00a082","rgba(0,160,130,.15)",  lambda p: f"https://www.google.com/search?q={Q}+{urllib.parse.quote(p)}+livraison"),
    ]
    for ico,sname,clr,bg,make in conc:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="pt-title">{ico} {sname}</div>', unsafe_allow_html=True)
        make_bubs([(p, make(p), clr, bg, "🌍") for p in PAYS])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""<div class="tip">
      💡 <b>Lire la concurrence en Afrique :</b> En Afrique francophone, même 5 à 15 publicités actives sur un produit
      indiquent déjà que le marché est validé. Ne cherchez pas 50+ pubs comme en Europe — les marchés africains
      sont moins saturés. 1 à 3 concurrents actifs = bonne opportunité. 0 pub = produit non testé (risque mais opportunité).
    </div>""", unsafe_allow_html=True)
