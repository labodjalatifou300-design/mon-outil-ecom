import streamlit as st
import requests, json, re, base64, urllib.parse

st.set_page_config(page_title="E-Commerce Master Labo Pro", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');
*,*::before,*::after{box-sizing:border-box;}
:root{--ink:#080810;--s1:#0f0f1a;--s2:#16162a;--s3:#1e1e35;--red:#ff2d55;--amber:#ff9f0a;--teal:#32d4a4;--smoke:#8888aa;--white:#f0f0fa;--border:rgba(255,255,255,.06);}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background:var(--ink)!important;color:var(--white)!important;}
#MainMenu,footer,header{visibility:hidden;}
section[data-testid="stSidebar"]{display:none!important;}
.block-container{padding:0 1.5rem 4rem!important;max-width:1400px!important;}

/* HERO */
.hero{position:relative;overflow:hidden;padding:3.5rem 2rem 2.5rem;text-align:center;
  background:linear-gradient(160deg,#080810 0%,#1a0815 45%,#080810 100%);
  border-bottom:1px solid rgba(255,45,85,.15);margin-bottom:2rem;}
.hero-glow{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse 90% 50% at 50% -5%,rgba(255,45,85,.2) 0%,transparent 65%),
    radial-gradient(ellipse 50% 50% at 15% 90%,rgba(255,159,10,.1) 0%,transparent 55%),
    radial-gradient(ellipse 50% 50% at 85% 90%,rgba(50,212,164,.08) 0%,transparent 55%);
  animation:glowp 5s ease-in-out infinite;}
@keyframes glowp{0%,100%{opacity:.7}50%{opacity:1}}
.orb{position:absolute;border-radius:50%;filter:blur(60px);animation:orbf linear infinite;pointer-events:none;}
@keyframes orbf{0%{transform:translateY(0) translateX(0)}33%{transform:translateY(-30px) translateX(20px)}66%{transform:translateY(15px) translateX(-15px)}100%{transform:translateY(0) translateX(0)}}
.p{position:absolute;border-radius:50%;animation:pfloat linear infinite;}
@keyframes pfloat{0%{transform:translateY(110%) scale(0);opacity:0}10%{opacity:.8;transform:translateY(90%) scale(1)}90%{opacity:.8}100%{transform:translateY(-10%) scale(.5) translateX(30px);opacity:0}}
.hero-title{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(2rem,6vw,4.5rem);
  line-height:1.05;letter-spacing:-2px;color:var(--white);position:relative;z-index:2;
  animation:titlein 1s cubic-bezier(.16,1,.3,1) both;
  text-shadow:0 20px 60px rgba(255,45,85,.3);}
@keyframes titlein{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:none}}
.hero-title .r{color:var(--red)}.hero-title .a{color:var(--amber)}
.hero-sub{font-size:clamp(.85rem,1.8vw,1.1rem);color:var(--smoke);letter-spacing:4px;
  text-transform:uppercase;margin-top:.7rem;position:relative;z-index:2;animation:fadein .8s .4s both;}
@keyframes fadein{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.hero-bar{width:80px;height:3px;margin:1.2rem auto 0;
  background:linear-gradient(90deg,var(--red),var(--amber),var(--teal));
  border-radius:2px;position:relative;z-index:2;}

/* PANEL */
.panel{background:var(--s1);border:1px solid var(--border);border-radius:20px;padding:1.8rem;margin-bottom:1.5rem;position:relative;overflow:hidden;transition:border-color .3s;}
.panel::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,45,85,.4),rgba(255,159,10,.4),transparent);}
.panel:hover{border-color:rgba(255,45,85,.2);}
.panel-title{font-family:'Syne',sans-serif;font-weight:700;font-size:.72rem;letter-spacing:3px;text-transform:uppercase;color:var(--red);margin-bottom:1.3rem;display:flex;align-items:center;gap:.6rem;}
.panel-title::after{content:'';flex:1;height:1px;background:var(--border);}

/* METRIC */
.metric{background:var(--s2);border:1px solid var(--border);border-radius:16px;padding:1.2rem;text-align:center;transition:transform .3s,border-color .3s,box-shadow .3s;cursor:default;}
.metric:hover{transform:perspective(400px) rotateY(-6deg) rotateX(4deg) translateY(-4px);border-color:rgba(255,45,85,.35);box-shadow:20px 20px 60px rgba(0,0,0,.5);}
.metric-val{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;line-height:1;margin-bottom:.3rem;}
.mv-r{color:var(--red);text-shadow:0 0 30px rgba(255,45,85,.4);}
.mv-a{color:var(--amber);text-shadow:0 0 30px rgba(255,159,10,.4);}
.mv-g{color:var(--teal);text-shadow:0 0 30px rgba(50,212,164,.4);}
.metric-lbl{font-size:.68rem;color:var(--smoke);letter-spacing:2px;text-transform:uppercase;}

/* TABLE */
.tbl{width:100%;border-collapse:collapse;font-size:.84rem;}
.tbl th{padding:.6rem .4rem;font-family:'Syne',sans-serif;font-size:.65rem;letter-spacing:2px;text-transform:uppercase;color:var(--smoke);border-bottom:1px solid var(--border);text-align:center;}
.tbl td{padding:.55rem .4rem;text-align:center;border-bottom:1px solid rgba(255,255,255,.03);transition:background .15s;}
.tbl tr:hover td{background:rgba(255,45,85,.05);}
.cg{color:var(--teal);font-weight:700}.cr{color:var(--red);font-weight:600}.ca{color:var(--amber);font-weight:600}

/* TABS */
.stTabs [data-baseweb="tab-list"]{background:var(--s1)!important;border-radius:14px!important;padding:5px!important;gap:3px!important;border:1px solid var(--border)!important;flex-wrap:wrap!important;margin-bottom:1.5rem!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--smoke)!important;border-radius:10px!important;padding:.5rem 1rem!important;font-family:'Syne',sans-serif!important;font-weight:600!important;font-size:.78rem!important;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,var(--red),#c0103a)!important;color:white!important;box-shadow:0 4px 20px rgba(255,45,85,.45)!important;}

/* BUTTONS */
.stButton>button{background:linear-gradient(135deg,var(--red),#c0103a)!important;color:white!important;border:none!important;border-radius:12px!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:.95rem!important;padding:.65rem 2.5rem!important;transition:all .25s!important;box-shadow:0 4px 24px rgba(255,45,85,.4)!important;}
.stButton>button:hover{transform:translateY(-3px) scale(1.02)!important;box-shadow:0 8px 35px rgba(255,45,85,.6)!important;}

/* INPUTS */
.stTextInput input,.stNumberInput input,.stTextArea textarea{background:var(--s2)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--white)!important;}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:rgba(255,45,85,.5)!important;box-shadow:0 0 0 3px rgba(255,45,85,.12)!important;}
label{color:var(--smoke)!important;font-size:.8rem!important;letter-spacing:.5px!important;}

/* SCORE */
.crit-row{background:var(--s2);border-radius:12px;padding:.9rem 1rem;margin:.4rem 0;border:1px solid var(--border);transition:border-color .2s,transform .2s;}
.crit-row:hover{border-color:rgba(255,45,85,.3);transform:translateX(4px);}
.crit-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:.35rem;}
.crit-name{font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem;}
.crit-note{font-family:'Syne',sans-serif;font-weight:800;font-size:.9rem;}
.bar-bg{background:rgba(255,255,255,.07);border-radius:20px;height:6px;overflow:hidden;}
.bar-fill{height:100%;border-radius:20px;}
.crit-why{font-size:.78rem;color:var(--smoke);margin-top:.3rem;line-height:1.5;}

/* OFFER */
.ocard{background:var(--s2);border:1px solid var(--border);border-radius:14px;padding:1.1rem;margin:.5rem 0;transition:all .25s;position:relative;overflow:hidden;}
.ocard::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--red),var(--amber));}
.ocard:hover{border-color:rgba(255,159,10,.35);transform:translateX(6px);box-shadow:0 8px 30px rgba(0,0,0,.3);}
.ocard-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.4rem;margin-bottom:.4rem;}
.ocard-title{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;margin-left:.4rem;}
.ocard-badge{font-size:.68rem;padding:.2rem .6rem;border-radius:20px;font-weight:700;letter-spacing:1px;}
.ocard-tip{font-size:.8rem;color:var(--amber);padding:.35rem .7rem;background:rgba(255,159,10,.07);border-left:2px solid var(--amber);border-radius:0 6px 6px 0;margin-top:.4rem;}

/* AD CARD */
.adcard{background:var(--s2);border-left:3px solid var(--red);border-radius:0 14px 14px 0;padding:1rem 1.2rem;margin:.5rem 0;transition:transform .2s;}
.adcard:hover{transform:translateX(3px);}
.adcard-hook{font-family:'Syne',sans-serif;font-weight:800;font-size:1rem;color:var(--white);margin-bottom:.6rem;}
.adcard-pip{font-size:.87rem;color:var(--smoke);padding:.12rem 0;}
.adcard-pip::before{content:'▸ ';color:var(--red);}

/* VOICE */
.vscript{background:var(--s2);border:1px solid var(--border);border-radius:14px;padding:1.2rem;margin:.5rem 0;}
.vscript-hd{display:flex;align-items:center;gap:.6rem;margin-bottom:.8rem;}
.script-num{font-family:'Syne',sans-serif;font-weight:800;font-size:.9rem;color:var(--red);}
.word-badge{font-size:.7rem;padding:.15rem .5rem;border-radius:20px;font-weight:700;}

/* AVATAR */
.av-wrap{background:var(--s2);border:1px solid var(--border);border-radius:20px;padding:1.6rem;}
.av-hero-row{display:flex;align-items:center;gap:1.2rem;margin-bottom:1.5rem;padding-bottom:1.2rem;border-bottom:1px solid var(--border);}
.av-orb{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,var(--red),var(--amber));display:flex;align-items:center;justify-content:center;font-size:2.2rem;flex-shrink:0;box-shadow:0 8px 30px rgba(255,45,85,.35);}
.av-name{font-family:'Syne',sans-serif;font-weight:800;font-size:1.4rem;}
.av-role{font-size:.82rem;color:var(--smoke);margin-top:.15rem;}
.av-sec{background:var(--s3);border-radius:12px;padding:1rem;height:100%;}
.av-sec-title{font-family:'Syne',sans-serif;font-weight:700;font-size:.68rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:.7rem;}
.av-kv{display:flex;gap:.6rem;margin:.3rem 0;align-items:flex-start;}
.av-k{font-size:.7rem;color:var(--smoke);letter-spacing:1px;text-transform:uppercase;width:90px;flex-shrink:0;padding-top:.1rem;}
.av-v{font-size:.87rem;flex:1;}
.av-pill{display:inline-block;padding:.2rem .55rem;border-radius:20px;font-size:.73rem;margin:.15rem;border:1px solid rgba(255,255,255,.1);}
.av-item{padding:.3rem .6rem;font-size:.84rem;border-radius:6px;margin:.2rem 0;}
.phrase-box{background:linear-gradient(135deg,rgba(255,45,85,.1),rgba(255,159,10,.07));border:1px solid rgba(255,159,10,.25);border-radius:14px;padding:1.3rem;text-align:center;margin-top:1rem;}
.phrase-text{font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:600;font-style:italic;line-height:1.65;}

/* BUBBLE GRID */
.bub-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.5rem;margin-top:.5rem;}
@media(max-width:768px){.bub-grid{grid-template-columns:repeat(3,1fr);}}
@media(max-width:480px){.bub-grid{grid-template-columns:repeat(2,1fr);}}
.bub{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:.7rem .4rem;border-radius:14px;text-decoration:none;text-align:center;transition:all .25s;border:1px solid rgba(255,255,255,.07);min-height:62px;gap:.25rem;}
.bub:hover{transform:translateY(-4px) scale(1.04);box-shadow:0 10px 28px rgba(0,0,0,.4);}
.bub-ico{font-size:1.25rem;}
.bub-lbl{font-family:'Syne',sans-serif;font-weight:700;font-size:.7rem;letter-spacing:.5px;}

/* THUMB */
.thumb-row{display:flex;flex-wrap:wrap;gap:.6rem;}
.thumb{display:flex;flex-direction:column;align-items:center;gap:.2rem;}
.thumb img{width:76px;height:76px;object-fit:cover;border-radius:10px;border:1px solid var(--border);transition:transform .2s;}
.thumb img:hover{transform:scale(1.1);}
.thumb a{font-size:.62rem;color:var(--smoke);text-decoration:none;}
.thumb a:hover{color:var(--red);}

/* FB BUDGET */
.fbud{text-align:center;padding:1.2rem;}
.fbud-num{font-family:'Syne',sans-serif;font-size:3.5rem;font-weight:800;line-height:1;}
.fbud-sub{color:var(--smoke);font-size:.82rem;margin-top:.3rem;}

/* TIP */
.tip{background:rgba(255,159,10,.07);border:1px solid rgba(255,159,10,.18);border-radius:10px;padding:.8rem 1rem;font-size:.84rem;color:var(--smoke);line-height:1.7;margin-top:.8rem;}
.tip b{color:var(--amber);}
.div{height:1px;background:var(--border);margin:1.2rem 0;}

/* WELCOME */
.welcome{text-align:center;padding:5rem 2rem;}
.welcome-icon{font-size:4rem;animation:bounce 2s ease-in-out infinite;}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.welcome-title{font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:var(--red);margin:.8rem 0;}
.welcome-sub{color:var(--smoke);font-size:.9rem;max-width:500px;margin:0 auto;line-height:1.7;}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;margin-top:2rem;}
@media(max-width:700px){.feat-grid{grid-template-columns:1fr 1fr;}}
.feat{background:var(--s1);border:1px solid var(--border);border-radius:14px;padding:1.1rem;text-align:center;transition:all .2s;}
.feat:hover{border-color:rgba(255,45,85,.3);transform:translateY(-3px);}
.feat-e{font-size:1.8rem;margin-bottom:.4rem;}
.feat-t{font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem;color:var(--amber);margin-bottom:.25rem;}
.feat-d{font-size:.78rem;color:var(--smoke);line-height:1.5;}

/* st.code styling */
.stCodeBlock{border-radius:10px!important;}
pre{background:var(--s3)!important;border:1px solid var(--border)!important;border-radius:10px!important;}

::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:var(--ink)}::-webkit-scrollbar-thumb{background:var(--red);border-radius:2px}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── SESSION ──────────────────────────────────────────
for k,v in {"gen":False,"pname":"","pimages":[],"pcost":0,"ptarget":5,"res":{},"form_open":True}.items():
    if k not in st.session_state: st.session_state[k]=v

GROQ_KEY = st.secrets.get("GROQ_API_KEY","")
PAYS = ["Togo","Mali","Bénin","Guinée","Côte d'Ivoire","Congo"]
CODES= {"Togo":"TG","Mali":"ML","Bénin":"BJ","Guinée":"GN","Côte d'Ivoire":"CI","Congo":"CG"}

# ── HELPERS ──────────────────────────────────────────
def groq(prompt, system="", tokens=2500):
    if not GROQ_KEY: return '{"error":"Clé manquante"}'
    try:
        msgs=([{"role":"system","content":system}] if system else [])+[{"role":"user","content":prompt}]
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"llama-3.3-70b-versatile","messages":msgs,"max_tokens":tokens,"temperature":.85},timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e: return f'{{"error":"{e}"}}'

def pj(raw):
    try: return json.loads(re.sub(r"```json|```","",raw).strip())
    except: return {}

def calc(cost,pub=5000,cl=1000,liv=2000):
    rec=cost+10000
    return {"min":cost+8000,"max":cost+12000,"rec":rec,"profit":rec-cost-pub-cl-liv,"pub":pub,"cl":cl,"liv":liv}

def copy_field(label, text):
    if label:
        st.markdown(f'<div style="font-size:.7rem;letter-spacing:1.5px;text-transform:uppercase;color:#8888aa;margin-bottom:.2rem;">{label}</div>', unsafe_allow_html=True)
    st.code(text, language=None)

def make_bub_grid(items):
    # items = list of (label, url, color, bg, icon)
    cells = "".join([
        f'<a href="{url}" target="_blank" class="bub" style="background:{bg};border-color:{clr}22;">'
        f'<span class="bub-ico">{ico}</span>'
        f'<span class="bub-lbl" style="color:{clr};">{lbl}</span></a>'
        for lbl,url,clr,bg,ico in items
    ])
    st.markdown(f'<div class="bub-grid">{cells}</div>', unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-glow"></div>
  <div class="orb" style="width:300px;height:300px;background:rgba(255,45,85,.06);top:-100px;left:-100px;animation-duration:20s;"></div>
  <div class="orb" style="width:200px;height:200px;background:rgba(255,159,10,.05);bottom:-80px;right:-60px;animation-duration:25s;animation-delay:5s;"></div>
  <div class="p" style="left:5%;width:5px;height:5px;background:#ff2d55;animation-duration:8s;animation-delay:0s;"></div>
  <div class="p" style="left:20%;width:3px;height:3px;background:#ff9f0a;animation-duration:11s;animation-delay:1s;"></div>
  <div class="p" style="left:40%;width:4px;height:4px;background:#32d4a4;animation-duration:9s;animation-delay:2s;"></div>
  <div class="p" style="left:60%;width:5px;height:5px;background:#ff2d55;animation-duration:7s;animation-delay:.5s;"></div>
  <div class="p" style="left:75%;width:3px;height:3px;background:#ffd60a;animation-duration:12s;animation-delay:1.5s;"></div>
  <div class="p" style="left:90%;width:4px;height:4px;background:#ff9f0a;animation-duration:10s;animation-delay:3s;"></div>
  <div class="hero-title">E-Commerce<br><span class="r">Master</span> <span class="a">Labo Pro</span></div>
  <div class="hero-sub">🌍 Tout en un pour un e-commerce africain réussi</div>
  <div class="hero-bar"></div>
</div>
""", unsafe_allow_html=True)

# ── TOGGLE BUTTON (centré) ───────────────────────────
_, mc, _ = st.columns([1,2,1])
with mc:
    lbl = "🔼 Masquer le formulaire" if st.session_state.form_open else "🔽 Remplir les informations produit"
    if st.button(lbl, key="tog", use_container_width=True):
        st.session_state.form_open = not st.session_state.form_open
        st.rerun()

# ── FORMULAIRE ───────────────────────────────────────
if st.session_state.form_open:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📦 Informations produit</div>', unsafe_allow_html=True)

    c1,c2,c3=st.columns([2,1,1])
    with c1: pname=st.text_input("Nom du produit",placeholder="Ex: Mini vélo de rééducation",value=st.session_state.pname)
    with c2: pcost=st.number_input("Prix d'achat (FCFA)",min_value=0,step=500,value=int(st.session_state.pcost))
    with c3: ptarget=st.number_input("Objectif ventes/jour",min_value=1,max_value=50,value=int(st.session_state.ptarget))

    c4,c5,c6=st.columns(3)
    with c4: ppub=st.number_input("Publicité/vente (FCFA)",value=5000,step=500)
    with c5: pcl =st.number_input("Closing/vente (FCFA)",value=1000,step=100)
    with c6: pliv=st.number_input("Livraison/vente (FCFA)",value=2000,step=500)

    st.markdown("**Images du produit** (1 à 10 photos)")
    uploaded=st.file_uploader("",type=["jpg","jpeg","png","webp"],accept_multiple_files=True,label_visibility="collapsed")
    if uploaded:
        if len(uploaded)>10: uploaded=uploaded[:10]; st.warning("Maximum 10 images.")
        st.session_state.pimages=uploaded
        st.markdown('<div class="thumb-row">', unsafe_allow_html=True)
        for img in uploaded:
            img.seek(0); b64=base64.b64encode(img.read()).decode(); ext=img.name.split(".")[-1]
            st.markdown(f'<div class="thumb"><img src="data:image/{ext};base64,{b64}"><a href="data:image/{ext};base64,{b64}" download="{img.name}">⬇ DL</a></div>', unsafe_allow_html=True)
            img.seek(0)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _,bc2,_=st.columns([1,2,1])
    with bc2: go=st.button("⚡ LANCER L'ANALYSE COMPLÈTE",use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if go:
        if not pname:    st.error("❌ Entrez le nom du produit"); st.stop()
        if pcost==0:     st.error("❌ Entrez le prix d'achat"); st.stop()
        if not GROQ_KEY: st.error("❌ Ajoutez GROQ_API_KEY dans Streamlit → Settings → Secrets"); st.stop()

        st.session_state.pname=pname; st.session_state.pcost=pcost; st.session_state.ptarget=ptarget
        pricing=calc(pcost,ppub,pcl,pliv); st.session_state.res["pricing"]=pricing
        SYS=(f"Tu es expert e-commerce africain et neuromarketing. "
             f"Produit EXACT: '{pname}'. Prix achat: {pcost} FCFA. Vente: {pricing['rec']} FCFA. "
             f"Marge: {pricing['profit']} FCFA. Objectif: {ptarget}/jour. "
             f"Tous tes textes parlent UNIQUEMENT de '{pname}'. Réponds en français, marché africain francophone.")

        bar=st.progress(0,"⚙️ Analyse IA en cours…")

        bar.progress(10,"🎯 Score produit…")
        raw=groq(f"""Évalue '{pname}' sur le marché africain. Score STRICT /10 (sois rigoureux, pas systématiquement 7-8).
JSON UNIQUEMENT:
{{"score":6.5,"verdict":"Moyen","couleur":"amber",
"criteres":[
  {{"nom":"💰 Rentabilité","note":7,"explication":"Explication précise de la rentabilité de ce produit avec marge {pricing['profit']} FCFA"}},
  {{"nom":"📈 Demande marché Afrique","note":6,"explication":"Demande réelle pour '{pname}' en Afrique francophone"}},
  {{"nom":"⚔️ Niveau de concurrence","note":5,"explication":"Concurrence sur '{pname}' en Afrique"}},
  {{"nom":"📦 Facilité approvisionnement","note":7,"explication":"Facilité à trouver '{pname}' sur AliExpress/Alibaba"}},
  {{"nom":"🎨 Créatives disponibles","note":6,"explication":"Photos/vidéos disponibles pour '{pname}'"}},
  {{"nom":"🔥 Potentiel viral FB/TikTok","note":7,"explication":"Potentiel viral de '{pname}' sur les réseaux"}},
  {{"nom":"🌍 Pertinence problème africain","note":8,"explication":"Problème africain résolu par '{pname}'"}},
  {{"nom":"💵 Prix vs pouvoir d'achat","note":6,"explication":"Prix {pricing['rec']} FCFA vs SMIC africain 35k-200k FCFA"}},
  {{"nom":"🔄 Potentiel fidélisation","note":5,"explication":"Les clients rachètent-ils '{pname}' ?"}},
  {{"nom":"📅 Saisonnalité","note":7,"explication":"Vente de '{pname}' toute l'année ou saisonnière ?"}}
],
"forts":["point fort concret 1 spécifique à {pname}","point fort 2","point fort 3"],
"faibles":["point faible concret 1","point faible 2"],
"conseil":"3 phrases stratégiques CONCRÈTES sur comment vendre '{pname}' en Afrique.",
"pays":["pays1","pays2","pays3"],
"periode":"Période optimale"}}""",SYS,1400)
        st.session_state.res["score"]=pj(raw) or {"score":6.5,"verdict":"Moyen","couleur":"amber","criteres":[{"nom":"💰 Rentabilité","note":7,"explication":"Marge correcte"}],"forts":["Bonne marge"],"faibles":["Concurrence"],"conseil":"Testez.","pays":["Côte d'Ivoire"],"periode":"Toute l'année"}

        bar.progress(22,"🎁 Offres…")
        raw=groq(f"""5 offres marketing irrésistibles SPÉCIFIQUES à '{pname}' pour le marché africain.
JSON UNIQUEMENT:
{{"offres":[
  {{"emoji":"🚚","titre":"offre 1 pour {pname}","desc":"description spécifique à {pname}","impact":"Élevé","conseil":"conseil pratique"}},
  {{"emoji":"🎁","titre":"offre 2","desc":"desc","impact":"Fort","conseil":"conseil"}},
  {{"emoji":"💰","titre":"offre 3","desc":"desc","impact":"Élevé","conseil":"conseil"}},
  {{"emoji":"⭐","titre":"offre 4","desc":"desc","impact":"Moyen","conseil":"conseil"}},
  {{"emoji":"🏆","titre":"offre 5","desc":"desc","impact":"Fort","conseil":"conseil"}}
]}}""",SYS,800)
        st.session_state.res["offres"]=pj(raw) or {"offres":[{"emoji":"🚚","titre":"Livraison gratuite","desc":"Lève les freins","impact":"Élevé","conseil":"Intégrez dans le prix"}]}

        bar.progress(36,"🛍️ Shopify…")
        raw=groq(f"""Contenu Shopify UNIQUEMENT pour '{pname}'.
RÈGLES: titres de paragraphes = PROMESSES DE RÉSULTAT concrètes liées à '{pname}' (PAS: Présentation, Avantages, Caractéristiques).
Exemples bons titres: "Retrouvez votre mobilité en 3 semaines", "Utilisable partout sans équipement".
JSON UNIQUEMENT:
{{"titres":["Titre SEO 1 bénéfice de {pname}","Titre SEO 2 résultat de {pname}","Titre SEO 3 transformation {pname}"],
"paragraphes":[
  {{"titre":"Promesse résultat concrète 1 de {pname}","texte":"4 phrases max sur CE bénéfice précis de {pname}."}},
  {{"titre":"Promesse 2","texte":"4 phrases."}},
  {{"titre":"Promesse 3","texte":"4 phrases."}},
  {{"titre":"Promesse 4","texte":"4 phrases."}},
  {{"titre":"Promesse 5","texte":"4 phrases."}},
  {{"titre":"Promesse 6","texte":"4 phrases."}}
]}}""",SYS,2200)
        st.session_state.res["shopify"]=pj(raw) or {"titres":["Titre 1","Titre 2","Titre 3"],"paragraphes":[{"titre":"Para","texte":"Texte."}]}

        bar.progress(50,"📢 Facebook Ads…")
        raw=groq(f"""3 textes pub Facebook POUR '{pname}', marché africain.
Max 70 mots. Structure: accroche CHOC spécifique à '{pname}' + 3 bénéfices spécifiques à '{pname}'.
JSON UNIQUEMENT:
{{"ads":[
  {{"accroche":"accroche choc spécifique à {pname}","b1":"bénéfice 1 de {pname}","b2":"bénéfice 2","b3":"bénéfice 3","mots":45}},
  {{"accroche":"accroche 2","b1":"b1","b2":"b2","b3":"b3","mots":48}},
  {{"accroche":"accroche 3","b1":"b1","b2":"b2","b3":"b3","mots":50}}
]}}""",SYS,800)
        st.session_state.res["fb"]=pj(raw) or {"ads":[{"accroche":"Accroche","b1":"B1","b2":"B2","b3":"B3","mots":40}]}

        bar.progress(63,"🎙️ Voix off…")
        raw=groq(f"""3 scripts voix off pour '{pname}', marché africain francophone.
RÈGLE ABSOLUE: chaque script = EXACTEMENT 120 à 140 mots. Parle UNIQUEMENT de '{pname}'.
Structure: [PROBLÈME 2-3 phrases percutantes] [SOLUTION: '{pname}' est la solution] [FONCTIONNEMENT 2-3 phrases] [TÉMOIGNAGE africain: Aminata, Kofi, Fatou, Ibrahim, Moussa, Aïssatou]
Neuromarketing: émotions, urgence, identification.
JSON UNIQUEMENT:
{{"scripts":[
  {{"texte":"script 1 de 120-140 mots sur {pname}","mots":125}},
  {{"texte":"script 2","mots":132}},
  {{"texte":"script 3","mots":128}}
]}}""",SYS,2800)
        st.session_state.res["voix"]=pj(raw) or {"scripts":[{"texte":"Script...","mots":0}]}

        bar.progress(80,"👤 Avatar…")
        raw=groq(f"""Avatar client idéal pour '{pname}' en Afrique francophone.
JSON UNIQUEMENT:
{{"prenom":"Aminata","emoji":"👩","sexe":"Femme","age":"35-50 ans","situation":"Mariée, 2 enfants",
"revenus":"100 000 – 180 000 FCFA/mois","profession":"Profession typique acheteur de {pname}",
"ville":"Grandes villes (Abidjan, Dakar, Douala)","reseaux":["Facebook","WhatsApp","TikTok"],"heure":"19h – 22h",
"peurs":["peur 1 liée à {pname}","peur 2","peur 3"],
"frustrations":["frustration 1 liée à {pname}","frustration 2","frustration 3"],
"desirs":["désir 1 lié à {pname}","désir 2","désir 3"],
"motivations":["motivation 1","motivation 2"],
"phrase":"Phrase EXACTE qui déclenche l'achat de {pname}",
"objections":["objection 1 pour {pname}","objection 2"],
"reponses":["réponse 1","réponse 2"],
"pour_qui":"Pour qui","budget":"Budget acceptable","livraison":"Préférence livraison"}}""",SYS,1200)
        st.session_state.res["avatar"]=pj(raw) or {"prenom":"Aminata","emoji":"👩","sexe":"Femme","age":"30-45 ans","revenus":"80 000 – 150 000 FCFA/mois","profession":"Commerçante","ville":"Abidjan, Dakar","reseaux":["Facebook","WhatsApp"],"heure":"19h-22h","peurs":["peur"],"frustrations":["frustration"],"desirs":["désir"],"motivations":["Santé"],"phrase":"Ce produit va changer votre vie.","objections":["Prix"],"reponses":["Paiement livraison"],"pour_qui":"Elle-même","budget":"15 000 FCFA","livraison":"Domicile"}

        bar.progress(100,"✅ Terminé !")
        st.session_state.gen=True; st.session_state.form_open=False
        st.balloons(); st.rerun()

# ── WELCOME ──────────────────────────────────────────
if not st.session_state.gen:
    if not st.session_state.form_open:
        st.markdown("""<div class="welcome">
          <div class="welcome-icon">⚡</div>
          <div class="welcome-title">Prêt à analyser votre produit ?</div>
          <div class="welcome-sub">Ouvrez le formulaire ci-dessus et lancez l'analyse IA complète.</div>
          <div class="feat-grid">
            <div class="feat"><div class="feat-e">💰</div><div class="feat-t">Prix &amp; Gains</div><div class="feat-d">Tableau rentabilité + budget Facebook Ads</div></div>
            <div class="feat"><div class="feat-e">🎯</div><div class="feat-t">Score Produit</div><div class="feat-d">10 critères avec explication de chaque note</div></div>
            <div class="feat"><div class="feat-e">🛍️</div><div class="feat-t">Shopify</div><div class="feat-d">3 titres SEO + 6 paragraphes bénéfices réels</div></div>
            <div class="feat"><div class="feat-e">📢</div><div class="feat-t">Facebook Ads</div><div class="feat-d">3 textes ≤70 mots, accroche choc</div></div>
            <div class="feat"><div class="feat-e">🎙️</div><div class="feat-t">Voix Off</div><div class="feat-d">3 scripts 120-140 mots, neuromarketing</div></div>
            <div class="feat"><div class="feat-e">👤</div><div class="feat-t">Avatar Client</div><div class="feat-d">Profil psychologique complet Afrique</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# ── RÉSULTATS ─────────────────────────────────────────
R=st.session_state.res; PN=st.session_state.pname; PR=R.get("pricing",{})
tabs=st.tabs(["💰 Prix & Gains","🎯 Score","🎁 Offres","🛍️ Shopify","📢 Facebook Ads","🎙️ Voix Off","👤 Avatar","🖼️ Images","🎬 Vidéos","⚔️ Concurrence"])

# ══ TAB 1 ══════════════════════════════════════════════
with tabs[0]:
    sell=PR.get("rec",0); profit=PR.get("profit",0)
    pub=PR.get("pub",5000); cl=PR.get("cl",1000); liv=PR.get("liv",2000)
    cost=st.session_state.pcost; tg=st.session_state.ptarget

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">💰 Stratégie de prix — {PN}</div>', unsafe_allow_html=True)
    m1,m2,m3,m4=st.columns(4)
    for col,lbl,val,cls in[(m1,"Prix minimum",PR.get("min",0),"mv-a"),(m2,"Prix recommandé",sell,"mv-r"),(m3,"Prix maximum",PR.get("max",0),"mv-a"),(m4,"Bénéfice net/vente",profit,"mv-g")]:
        with col: st.markdown(f'<div class="metric"><div class="metric-val {cls}">{val:,} FCFA</div><div class="metric-lbl">{lbl}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📊 Charges par vente</div>', unsafe_allow_html=True)
    d1,d2,d3,d4=st.columns(4)
    for col,lbl,val,cls in[(d1,"📣 Publicité",pub,"mv-r"),(d2,"📞 Closing",cl,"mv-a"),(d3,"🚚 Livraison",liv,"mv-a"),(d4,"💚 Votre gain NET",profit,"mv-g")]:
        with col: st.markdown(f'<div class="metric"><div class="metric-val {cls}">{val:,} FCFA</div><div class="metric-lbl">{lbl}</div></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📈 Tableau de gains — 1 à 10 ventes/jour</div>', unsafe_allow_html=True)
    rows=""
    for v in range(1,11):
        ca=v*sell;cp=v*cost;dp=v*pub;dc=v*cl;dl=v*liv;bn=ca-cp-dp-dc-dl;bm=bn*30
        cc="cg" if bn>0 else "cr"
        rows+=f"<tr><td><b>{v}</b></td><td class='ca'>{ca:,}</td><td class='cr'>{cp:,}</td><td class='cr'>{dp:,}</td><td class='cr'>{dc:,}</td><td class='cr'>{dl:,}</td><td class='{cc}'>{bn:,}</td><td class='{cc}'>{bm:,}</td></tr>"
    st.markdown(f"""<table class="tbl"><thead><tr><th>Ventes/j</th><th>CA FCFA</th><th>Coût prod.</th><th>Pub</th><th>Closing</th><th>Livraison</th><th>Bénéf./j</th><th>Bénéf./mois</th></tr></thead><tbody>{rows}</tbody></table>""",unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📣 Budget Facebook Ads recommandé</div>', unsafe_allow_html=True)
    if tg<=7:    fb=("5 $","1 créative","#32d4a4")
    elif tg<=12: fb=("7 – 8 $","1-2 créatives","#ff9f0a")
    elif tg<=20: fb=("10 – 15 $","2-3 créatives","#ff2d55")
    else:        fb=("15 $+","3+ créatives","#bf5af2")
    st.markdown(f'<div class="fbud"><div class="fbud-num" style="color:{fb[2]};">{fb[0]} <span style="font-size:1.4rem;color:#8888aa;">/ jour</span></div><div class="fbud-sub">Objectif : {tg} ventes/jour — {fb[1]}</div></div><div class="tip">💡 <b>Conseil :</b> 1 créative + {fb[0]}/jour. Si CPA &lt; <b>{profit:,} FCFA</b> après 3 jours → augmentez progressivement.</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 2 ══════════════════════════════════════════════
with tabs[1]:
    SD=R.get("score",{}); sv=float(SD.get("score",7))
    verdict=SD.get("verdict","Bon"); couleur=SD.get("couleur","amber")
    sc={"red":"#ff2d55","amber":"#ff9f0a","green":"#32d4a4","orange":"#ff9f0a"}.get(couleur,"#ff9f0a")
    circ=int((sv/10)*251)

    cS,cD=st.columns([1,2])
    with cS:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align:center;padding:1.2rem 0;">
          <svg width="170" height="170" viewBox="0 0 100 100" style="filter:drop-shadow(0 0 25px {sc}55)">
            <circle cx="50" cy="50" r="40" fill="none" stroke="#1e1e35" stroke-width="10"/>
            <circle cx="50" cy="50" r="40" fill="none" stroke="{sc}" stroke-width="10"
              stroke-dasharray="{circ} {251-circ}" stroke-dashoffset="63" stroke-linecap="round"/>
            <text x="50" y="46" text-anchor="middle" font-family="Syne,sans-serif" font-size="22" font-weight="800" fill="{sc}">{sv}</text>
            <text x="50" y="60" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="8" fill="#8888aa">/ 10</text>
          </svg>
          <div style="font-family:Syne,sans-serif;font-weight:800;font-size:1.4rem;color:{sc};margin-top:.4rem;">{verdict}</div>
        </div>""",unsafe_allow_html=True)
        st.markdown('<div class="div"></div>',unsafe_allow_html=True)
        st.markdown('<div style="font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:#32d4a4;margin-bottom:.5rem;">✅ Points forts</div>',unsafe_allow_html=True)
        for p in SD.get("forts",[]):
            st.markdown(f'<div style="padding:.4rem .7rem;background:rgba(50,212,164,.08);border-left:2px solid #32d4a4;border-radius:0 6px 6px 0;margin:.25rem 0;font-size:.84rem;">✅ {p}</div>',unsafe_allow_html=True)
        st.markdown('<div class="div"></div>',unsafe_allow_html=True)
        st.markdown('<div style="font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:#ff2d55;margin-bottom:.5rem;">⚠️ À surveiller</div>',unsafe_allow_html=True)
        for p in SD.get("faibles",[]):
            st.markdown(f'<div style="padding:.4rem .7rem;background:rgba(255,45,85,.08);border-left:2px solid #ff2d55;border-radius:0 6px 6px 0;margin:.25rem 0;font-size:.84rem;">⚠️ {p}</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with cD:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📊 Détail de chaque critère</div>', unsafe_allow_html=True)
        for c in SD.get("criteres",[]):
            v=c.get("note",7); pct=v*10
            bc="#32d4a4" if v>=7 else "#ff9f0a" if v>=5 else "#ff2d55"
            st.markdown(f"""<div class="crit-row">
              <div class="crit-top">
                <div class="crit-name">{c.get('nom','')}</div>
                <div class="crit-note" style="color:{bc};">{v}/10</div>
              </div>
              <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{bc};"></div></div>
              <div class="crit-why">💬 {c.get('explication','')}</div>
            </div>""",unsafe_allow_html=True)
        st.markdown(f'<div class="tip"><b>🧭 Recommandation :</b> {SD.get("conseil","")}<br><br>🌍 <b>Marchés :</b> {", ".join(SD.get("pays",[]))} &nbsp;|&nbsp; 📅 <b>Période :</b> {SD.get("periode","")}</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 3 ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🎁 Offres marketing — {PN}</div>', unsafe_allow_html=True)
    for o in R.get("offres",{}).get("offres",[]):
        imp=o.get("impact","Moyen"); ic="#32d4a4" if "Élevé" in imp or "Fort" in imp else "#ff9f0a"
        st.markdown(f"""<div class="ocard">
          <div class="ocard-head">
            <div class="ocard-title">{o.get('emoji','🎯')} {o.get('titre','')}</div>
            <span class="ocard-badge" style="background:{ic}22;color:{ic};border:1px solid {ic}33;">{imp}</span>
          </div>
          <div style="font-size:.86rem;color:var(--smoke);">{o.get('desc','')}</div>
          <div class="ocard-tip">💡 {o.get('conseil','')}</div>
        </div>""",unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 4 ══════════════════════════════════════════════
with tabs[3]:
    SH=R.get("shopify",{})
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🏷️ 3 Titres produit optimisés SEO</div>', unsafe_allow_html=True)
    for i,t in enumerate(SH.get("titres",[]),1):
        copy_field(f"Titre {i}", t)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📝 6 Paragraphes de description (bénéfices produit)</div>', unsafe_allow_html=True)
    for i,p in enumerate(SH.get("paragraphes",[]),1):
        st.markdown(f'<div style="font-family:Syne,sans-serif;font-weight:700;font-size:.92rem;color:#ff9f0a;margin-top:1rem;margin-bottom:.3rem;">▶ {p.get("titre","")}</div>',unsafe_allow_html=True)
        copy_field("", p.get("texte",""))
    st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 5 ══════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">📢 Facebook Ads — {PN}</div>', unsafe_allow_html=True)
    for i,ad in enumerate(R.get("fb",{}).get("ads",[]),1):
        full=f"{ad.get('accroche','')}\n\n- {ad.get('b1','')}\n- {ad.get('b2','')}\n- {ad.get('b3','')}"
        st.markdown(f'<div style="font-size:.68rem;letter-spacing:1.5px;text-transform:uppercase;color:#8888aa;margin-top:1rem;margin-bottom:.3rem;">Texte #{i} — {ad.get("mots","~")} mots</div>',unsafe_allow_html=True)
        st.markdown(f"""<div class="adcard">
          <div class="adcard-hook">🔥 {ad.get('accroche','')}</div>
          <div class="adcard-pip">{ad.get('b1','')}</div>
          <div class="adcard-pip">{ad.get('b2','')}</div>
          <div class="adcard-pip">{ad.get('b3','')}</div>
        </div>""",unsafe_allow_html=True)
        copy_field("Copier le texte complet", full)
    st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 6 ══════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🎙️ Scripts voix off — {PN}</div>', unsafe_allow_html=True)
    for i,s in enumerate(R.get("voix",{}).get("scripts",[]),1):
        txt=s.get("texte",""); mots=s.get("mots",len(txt.split()))
        mc="#32d4a4" if 120<=mots<=140 else "#ff9f0a"
        st.markdown(f'<div class="vscript"><div class="vscript-hd"><span class="script-num">🎙️ Script #{i}</span><span class="word-badge" style="color:{mc};background:{mc}18;border:1px solid {mc}33;">{mots} mots</span></div><div style="color:var(--smoke);line-height:1.8;font-size:.9rem;">{txt.replace(chr(10),"<br>")}</div></div>',unsafe_allow_html=True)
        copy_field("", txt)
    st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 7 ══════════════════════════════════════════════
with tabs[6]:
    AV=R.get("avatar",{})
    st.markdown('<div class="av-wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="av-hero-row"><div class="av-orb">{AV.get("emoji","👤")}</div><div><div class="av-name">{AV.get("prenom","Avatar")} — Avatar Client Idéal</div><div class="av-role">{AV.get("profession","")} · {AV.get("ville","")}</div></div></div>',unsafe_allow_html=True)

    cL,cR=st.columns(2)
    with cL:
        st.markdown('<div class="av-sec">', unsafe_allow_html=True)
        st.markdown('<div class="av-sec-title" style="color:#ff9f0a;">👤 Profil démographique</div>', unsafe_allow_html=True)
        for lbl,key in [("Sexe","sexe"),("Âge","age"),("Situation","situation"),("Revenus","revenus"),("En ligne","heure"),("Budget max","budget"),("Livraison","livraison"),("Achète pour","pour_qui")]:
            v=AV.get(key,"")
            if v: st.markdown(f'<div class="av-kv"><div class="av-k">{lbl}</div><div class="av-v">{v}</div></div>',unsafe_allow_html=True)
        rs=AV.get("reseaux",[])
        if rs:
            pills="".join([f'<span class="av-pill">{s}</span>' for s in rs])
            st.markdown(f'<div class="av-kv"><div class="av-k">Réseaux</div><div class="av-v">{pills}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cR:
        st.markdown('<div class="av-sec">', unsafe_allow_html=True)
        st.markdown('<div class="av-sec-title" style="color:#ff2d55;">🧠 Profil psychologique</div>', unsafe_allow_html=True)
        for lbl,key,clr in [("😱 Peurs","peurs","#ff2d55"),("😤 Frustrations","frustrations","#ff9f0a"),("💫 Désirs","desirs","#bf5af2"),("⚡ Motivations","motivations","#32d4a4")]:
            items=AV.get(key,[])
            if items:
                st.markdown(f'<div style="font-size:.68rem;letter-spacing:1.5px;text-transform:uppercase;color:{clr};margin:.6rem 0 .25rem;">{lbl}</div>',unsafe_allow_html=True)
                for x in items: st.markdown(f'<div class="av-item" style="background:{clr}11;border-left:2px solid {clr};">▸ {x}</div>',unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3,c4=st.columns(2)
    for col,lbl,key,clr in [(c3,"❓ Objections","objections","#ff9f0a"),(c4,"✅ Réponses","reponses","#32d4a4")]:
        with col:
            items=AV.get(key,[])
            st.markdown(f'<div class="av-sec" style="margin-top:1rem;"><div class="av-sec-title" style="color:{clr};">{lbl}</div>',unsafe_allow_html=True)
            for x in items: st.markdown(f'<div class="av-item" style="background:{clr}11;border-left:2px solid {clr};">▸ {x}</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

    phrase=AV.get("phrase","")
    if phrase:
        st.markdown(f'<div class="phrase-box"><div style="font-size:.68rem;letter-spacing:2px;text-transform:uppercase;color:#ff9f0a;margin-bottom:.5rem;">💬 Phrase déclenchante</div><div class="phrase-text">"{phrase}"</div></div>',unsafe_allow_html=True)
        copy_field("", phrase)
    st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 8 ══════════════════════════════════════════════
with tabs[7]:
    q=urllib.parse.quote(PN)
    if st.session_state.pimages:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📷 Vos images uploadées</div>', unsafe_allow_html=True)
        st.markdown('<div class="thumb-row">', unsafe_allow_html=True)
        for img in st.session_state.pimages:
            img.seek(0); b64=base64.b64encode(img.read()).decode(); ext=img.name.split(".")[-1]
            st.markdown(f'<div class="thumb"><img src="data:image/{ext};base64,{b64}"><a href="data:image/{ext};base64,{b64}" download="{img.name}">⬇ DL</a></div>',unsafe_allow_html=True)
            img.seek(0)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🔍 Rechercher des images de votre produit</div>', unsafe_allow_html=True)
    make_bub_grid([
        ("AliExpress",f"https://fr.aliexpress.com/wholesale?SearchText={q}","#ff6010","rgba(255,96,16,.12)","🟠"),
        ("Alibaba",f"https://www.alibaba.com/trade/search?SearchText={q}","#e6380a","rgba(230,56,10,.12)","🔵"),
        ("Pinterest",f"https://www.pinterest.com/search/pins/?q={q}","#e60023","rgba(230,0,35,.12)","📌"),
        ("Temu",f"https://www.temu.com/search_result.html?search_key={q}","#ff9f0a","rgba(255,159,10,.12)","🟡"),
        ("Google Images",f"https://www.google.com/search?q={q}&tbm=isch","#4285f4","rgba(66,133,244,.12)","🔍"),
        ("Amazon",f"https://www.amazon.fr/s?k={q}","#ff9900","rgba(255,153,0,.12)","🛒"),
        ("Jumia",f"https://www.jumia.com/catalog/?q={q}","#f68b1e","rgba(246,139,30,.12)","🛍️"),
        ("Cdiscount",f"https://www.cdiscount.com/search/10/{q}.html","#e4001b","rgba(228,0,27,.12)","🏪"),
    ])
    st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 9 ══════════════════════════════════════════════
with tabs[8]:
    q=urllib.parse.quote(PN)
    for ico,pname_v,clr,bg,make in [
        ("▶️","YouTube","#ff0000","rgba(255,0,0,.12)",   lambda p:f"https://www.youtube.com/results?search_query={q}+{urllib.parse.quote(p)}"),
        ("🎵","TikTok", "#69c9d0","rgba(105,201,208,.12)",lambda p:f"https://www.tiktok.com/search?q={q}+{urllib.parse.quote(p)}"),
        ("📌","Pinterest","#e60023","rgba(230,0,35,.12)", lambda p:f"https://www.pinterest.com/search/pins/?q={q}+{urllib.parse.quote(p)}"),
        ("🔍","Google Vidéos","#4285f4","rgba(66,133,244,.12)",lambda p:f"https://www.google.com/search?q={q}+{urllib.parse.quote(p)}&tbm=vid"),
        ("🟠","AliExpress","#ff6010","rgba(255,96,16,.12)",lambda p:f"https://fr.aliexpress.com/wholesale?SearchText={q}"),
    ]:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-title">{ico} {pname_v}</div>', unsafe_allow_html=True)
        make_bub_grid([(p,make(p),clr,bg,"🌍") for p in PAYS])
        st.markdown('</div>', unsafe_allow_html=True)

# ══ TAB 10 ═════════════════════════════════════════════
with tabs[9]:
    q=urllib.parse.quote(PN)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📚 Bibliothèque Publicitaire Facebook</div>', unsafe_allow_html=True)
    make_bub_grid([(p,f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={CODES.get(p,'')}&q={q}&search_type=keyword_unordered","#1877f2","rgba(24,119,242,.12)","🌍") for p in PAYS])
    st.markdown('</div>', unsafe_allow_html=True)

    for ico,sname,clr,bg,make in [
        ("🛒","Boutiques Facebook","#1877f2","rgba(24,119,242,.12)",lambda p:f"https://www.facebook.com/search/pages/?q={q}+boutique+{urllib.parse.quote(p)}"),
        ("🌐","Google Shopping","#4285f4","rgba(66,133,244,.12)",   lambda p:f"https://www.google.com/search?q={q}+boutique+{urllib.parse.quote(p)}&tbm=shop"),
        ("🟠","AliExpress","#ff6010","rgba(255,96,16,.12)",          lambda p:f"https://fr.aliexpress.com/wholesale?SearchText={q}"),
        ("🔵","Jumia","#f68b1e","rgba(246,139,30,.12)",              lambda p:f"https://www.jumia.com/catalog/?q={q}"),
    ]:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-title">{ico} {sname}</div>', unsafe_allow_html=True)
        make_bub_grid([(p,make(p),clr,bg,"🌍") for p in PAYS])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="tip">💡 <b>Comment analyser :</b> +50 pubs actives = marché validé ✅ (concurrence forte) &nbsp;|&nbsp; 0-10 pubs = non validé ⚠️ &nbsp;|&nbsp; Inspirez-vous des meilleures accroches.</div>',unsafe_allow_html=True)
