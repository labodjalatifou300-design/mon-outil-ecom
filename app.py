import streamlit as st
import os, re, json, base64, urllib.parse, urllib.request
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════
# HISTORIQUE
# ══════════════════════════════════════════════════════════════════════
HISTORY_FILE = "/tmp/labo_history.json"

def load_history_file():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except: pass
    return []

def write_history_file(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except: pass

def save_to_history(name, score, data, prix_achat):
    entry = {"name": name, "score": score, "data": data,
             "prix_achat": prix_achat, "ts": datetime.now().strftime("%d/%m %H:%M")}
    existing = [h for h in st.session_state["history"] if h["name"] != name]
    updated  = [entry] + existing[:19]
    st.session_state["history"] = updated
    write_history_file(updated)

# ══════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════
for k, v in [
    ("history",        load_history_file()),
    ("result",         None),
    ("analyzed",       False),
    ("active_product", ""),
    ("active_price",   5000),
    ("active_ventes",  10),
    ("nav_page",       "analyse"),
    ("img_results",    []),
    ("img_query_done", ""),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="EcoMaster Labo Pro", page_icon="🚀", layout="wide")
st.markdown("""
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0d1117">
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# CSS — DESIGN ORIGINAL LABO (restauré + amélioré)
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700;800&display=swap');

/* ══ VARIABLES ══════════════════════════════════════════════ */
:root {
  color-scheme: dark !important;
  --red:      #D90429;
  --red2:     #ff1744;
  --red-dim:  rgba(217,4,41,0.12);
  --red-glow: rgba(217,4,41,0.45);
  --bg:       #0d1117;
  --bg2:      #161b22;
  --bg3:      #1c2333;
  --bg4:      #21262d;
  --border:   rgba(255,255,255,0.07);
  --border2:  rgba(255,255,255,0.13);
  --text:     #F0F0F0;
  --muted:    #6e7681;
  --muted2:   #444c56;
}

/* ══ BASE ═══════════════════════════════════════════════════ */
html, body, [class*="css"], [data-testid], .stApp,
.appview-container, .appview-container > section,
.block-container, .main {
  font-family: 'Space Grotesk','Inter',sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}
@media (prefers-color-scheme: light) {
  html, body, div, section, .stApp, .main, .block-container,
  .appview-container, .appview-container > section,
  [class*="css"], [data-testid] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
  }
}
.block-container {
  padding-top: 1.5rem !important;
  max-width: 1120px !important;
  padding-left: 1rem !important;
  padding-right: 1rem !important;
}

/* ══ ANIMATIONS ═════════════════════════════════════════════ */
@keyframes fadeInDown  { from{opacity:0;transform:translateY(-28px) scale(.97)} to{opacity:1;transform:none} }
@keyframes fadeInUp    { from{opacity:0;transform:translateY(22px)}  to{opacity:1;transform:none} }
@keyframes fadeInLeft  { from{opacity:0;transform:translateX(-22px)} to{opacity:1;transform:none} }
@keyframes fadeInRight { from{opacity:0;transform:translateX(22px)}  to{opacity:1;transform:none} }
@keyframes scaleIn     { from{opacity:0;transform:scale(.88)} to{opacity:1;transform:none} }
@keyframes pulse3d {
  0%,100%{box-shadow:0 0 0 0 rgba(217,4,41,.5),0 0 30px rgba(217,4,41,.1);transform:translateY(0)}
  50%    {box-shadow:0 0 0 14px rgba(217,4,41,0),0 8px 40px rgba(217,4,41,.35);transform:translateY(-2px)}
}
@keyframes glowPulse {
  0%,100%{box-shadow:0 0 18px rgba(217,4,41,.3),inset 0 0 18px rgba(217,4,41,.05)}
  50%    {box-shadow:0 0 55px rgba(217,4,41,.7),inset 0 0 30px rgba(217,4,41,.12)}
}
@keyframes shimmerMove {
  0%  {transform:translateX(-100%)}
  100%{transform:translateX(300%)}
}
@keyframes borderRun {
  0%  {background-position:0% 50%}
  50% {background-position:100% 50%}
  100%{background-position:0% 50%}
}
@keyframes float {
  0%,100%{transform:translateY(0)}
  50%    {transform:translateY(-5px)}
}
@keyframes scanLine {
  from{top:-20%} to{top:120%}
}

/* ══ SIDEBAR ════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#080b0f 0%,var(--bg) 100%) !important;
  border-right: 2px solid rgba(217,4,41,0.18) !important;
}
section[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  color: var(--muted) !important;
  border: 1px solid var(--border2) !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
  padding: 0.42rem 0.75rem !important;
  box-shadow: none !important;
  animation: none !important;
  letter-spacing: 0 !important;
  border-radius: 9px !important;
  text-align: left !important;
  justify-content: flex-start !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  border-color: var(--red) !important;
  color: #fff !important;
  background: rgba(217,4,41,0.08) !important;
  transform: none !important;
}
section[data-testid="stSidebar"] .stButton > button[data-active="true"] {
  border-color: var(--red) !important;
  color: #fff !important;
  background: rgba(217,4,41,0.12) !important;
}

/* ══ HERO BANNER ════════════════════════════════════════════ */
.hero-banner {
  position: relative; overflow: hidden;
  background: transparent;
  border: 3px solid var(--red);
  border-radius: 22px;
  padding: 2.2rem 2rem 2rem;
  margin-bottom: 2rem; text-align: center;
  box-shadow: 0 0 70px rgba(217,4,41,0.18), 0 0 140px rgba(217,4,41,0.05);
  animation: fadeInDown 0.8s cubic-bezier(.16,1,.3,1) both;
}
.hero-banner::before {
  content:'';
  position:absolute;top:0;left:-50%;width:40%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(217,4,41,0.07),transparent);
  animation:shimmerMove 3.5s ease-in-out infinite;
  pointer-events:none;
}
.hero-banner::after {
  content:'';
  position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--red),transparent);
}
.hero-banner h1 {
  font-size:clamp(1.7rem,5vw,2.8rem);
  font-weight:900;color:#fff;
  margin:0;letter-spacing:-1.5px;
  text-shadow:0 0 40px rgba(217,4,41,0.25);
}
.hero-banner h1 span{color:var(--red);}
.hero-banner .slogan{color:var(--muted);margin:.5rem 0 0;font-size:.82rem;letter-spacing:3px;text-transform:uppercase;}
.hero-banner .sub{color:var(--red);font-size:.7rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;margin-top:.25rem;}

/* ══ INPUTS ═════════════════════════════════════════════════ */
.stTextInput input, .stNumberInput input {
  background:var(--bg2) !important; color:#fff !important;
  border:2px solid var(--border2) !important;
  border-radius:12px !important; font-size:.88rem !important;
  transition:all .25s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border-color:var(--red) !important;
  box-shadow:0 0 0 4px rgba(217,4,41,0.12), 0 0 18px rgba(217,4,41,0.08) !important;
}
.stSelectbox > div > div, .stSlider {
  color:var(--text) !important;
}
.stSelectbox > div > div {
  background:var(--bg2) !important;
  border:2px solid var(--border2) !important;
  border-radius:12px !important;
}

/* ══ BOUTON PRINCIPAL ═══════════════════════════════════════ */
.stButton > button {
  position:relative; overflow:hidden;
  background:linear-gradient(135deg,#D90429,#ff1744,#D90429) !important;
  background-size:200% auto !important;
  color:#fff !important; border:none !important;
  border-radius:14px !important; font-weight:900 !important;
  font-size:.95rem !important; letter-spacing:1.5px !important;
  padding:.85rem 2rem !important; width:100% !important;
  transition:all .35s !important;
  animation:pulse3d 2.8s infinite !important;
}
.stButton > button:hover {
  background-position:right center !important;
  transform:translateY(-3px) !important;
  box-shadow:0 14px 40px rgba(217,4,41,0.55) !important;
}

/* ══ TABS ════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background:var(--bg2);border-radius:14px;padding:5px;
  gap:3px;border:2px solid rgba(255,255,255,0.05);flex-wrap:wrap;
}
.stTabs [data-baseweb="tab"] {
  background:transparent !important; color:var(--muted) !important;
  border-radius:10px !important; font-weight:700 !important;
  font-size:clamp(.63rem,1.8vw,.8rem) !important;
  padding:.42rem .65rem !important; transition:all .2s !important;
}
.stTabs [aria-selected="true"] {
  background:linear-gradient(135deg,#D90429,#c0021f) !important;
  color:#fff !important;
  box-shadow:0 4px 18px rgba(217,4,41,0.4) !important;
}
.stTabs [data-baseweb="tab"]:focus-visible,
[data-baseweb="tab-highlight"] { display:none !important; outline:none !important; }

/* ══ PRICE BOXES ═════════════════════════════════════════════ */
.price-box {
  background:var(--bg2);border:2px solid var(--red);
  border-radius:16px;padding:1rem 1.1rem;text-align:center;
  margin-bottom:1rem;transition:all .3s;
  animation:fadeInUp .5s ease both;position:relative;overflow:hidden;
}
.price-box::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--red),transparent);
}
.price-box:hover{transform:translateY(-4px) scale(1.02);box-shadow:0 10px 28px rgba(217,4,41,0.28);}
.price-box .label{color:var(--muted);font-size:.63rem;text-transform:uppercase;letter-spacing:1.5px;}
.price-box .value{color:#fff;font-size:clamp(.95rem,4vw,1.45rem);font-weight:900;margin-top:3px;}
.price-box .currency{color:var(--red);font-size:.7rem;}

/* ══ SCORE BADGE ═════════════════════════════════════════════ */
.score-wrap{text-align:center;padding:.8rem 0;animation:scaleIn .6s ease both;}
.score-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:108px;height:108px;border-radius:50%;
  border:4px solid var(--red);background:var(--bg2);
  box-shadow:0 0 45px rgba(217,4,41,0.3),inset 0 0 30px rgba(217,4,41,0.06);
  animation:glowPulse 3s infinite;
}
.score-badge .sn{font-size:2.1rem;font-weight:900;color:#fff;line-height:1;letter-spacing:-2px;}
.score-badge .sd{font-size:.62rem;color:var(--muted);}

/* ══ RESULT CARD ═════════════════════════════════════════════ */
.result-card {
  background:var(--bg2);border:2px solid var(--border);
  border-radius:16px;padding:1.3rem;margin-bottom:.9rem;
  animation:fadeInUp .5s ease both;
  transition:transform .25s,box-shadow .25s,border-color .25s;
  position:relative;overflow:hidden;
}
.result-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--red),transparent);
  opacity:0;transition:opacity .3s;
}
.result-card:hover{transform:translateY(-3px);border-color:rgba(217,4,41,0.28);}
.result-card:hover::before{opacity:1;}
.result-card:hover{box-shadow:0 10px 35px rgba(217,4,41,0.1);}

/* ══ SECTION LABEL ═══════════════════════════════════════════ */
.slabel {
  color:var(--red);font-size:.7rem;font-weight:700;
  text-transform:uppercase;letter-spacing:2px;
  margin:1.2rem 0 .5rem;display:flex;align-items:center;gap:8px;
}
.slabel::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(217,4,41,0.3),transparent);}

/* ══ CRITÈRE ROW ═════════════════════════════════════════════ */
.crit-row{
  display:flex;align-items:center;gap:10px;
  padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.04);
}
.crit-note{
  min-width:34px;height:26px;
  display:flex;align-items:center;justify-content:center;
  border-radius:7px;font-weight:900;font-size:.85rem;
}
.crit-name{font-size:.8rem;font-weight:700;color:var(--text);}
.crit-desc{font-size:.68rem;color:var(--muted);}
.crit-poids{font-size:.6rem;color:var(--muted2);}

/* ══ AD BLOCK ════════════════════════════════════════════════ */
.ad-block{
  background:var(--bg2);border:2px solid var(--border);
  border-radius:14px;padding:1.2rem;margin-bottom:.8rem;
  transition:all .25s;position:relative;overflow:hidden;
}
.ad-block::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--red),#ff6b35,var(--red));
  background-size:200% auto;animation:borderRun 3s linear infinite;
  opacity:0;transition:opacity .25s;
}
.ad-block:hover{border-color:rgba(217,4,41,0.32);transform:translateY(-2px);box-shadow:0 8px 30px rgba(217,4,41,0.12);}
.ad-block:hover::before{opacity:1;}
.ad-angle{color:var(--muted);font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;margin:0 0 5px;}
.ad-accroche{color:#ff9944;font-weight:900;font-size:1rem;margin:0 0 7px;}
.ad-texte{color:#ccc;font-size:.86rem;line-height:1.9;margin:0;white-space:pre-wrap;}

/* ══ SCRIPT BLOCK ════════════════════════════════════════════ */
.script-block{
  background:var(--bg2);border:2px solid var(--border);
  border-top:3px solid var(--red);
  border-radius:0 0 14px 14px;padding:1.3rem;margin-bottom:1rem;
  transition:all .25s;
}
.script-block:hover{border-color:rgba(217,4,41,0.28);}
.script-label{color:var(--red);font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 8px;}
.script-texte{color:#ccc;font-size:.87rem;line-height:2.05;margin:0;white-space:pre-wrap;}
.wc-ok  {color:#44dd88;font-weight:700;font-size:.68rem;}
.wc-bad {color:#ff9944;font-weight:700;font-size:.68rem;}

/* ══ SHOPIFY PARA ════════════════════════════════════════════ */
.para-card{
  background:var(--bg);border-left:4px solid var(--red);
  border-radius:0 14px 14px 0;padding:1rem 1.3rem;margin-bottom:.75rem;
  transition:all .25s;
}
.para-card:hover{background:rgba(217,4,41,0.025);transform:translateX(5px);}
.para-titre{color:var(--red);font-weight:800;font-size:.9rem;margin:0 0 6px;}
.para-texte{color:#bbb;font-size:.86rem;line-height:1.85;margin:0;white-space:pre-wrap;}

/* ══ TITRE OPTION (Shopify titres) ══════════════════════════ */
.titre-opt{
  background:var(--bg);border:2px solid var(--border2);
  border-radius:14px;padding:.9rem 1.2rem;margin-bottom:.6rem;
  transition:all .25s;
}
.titre-opt:hover{border-color:var(--red);transform:translateX(7px);background:rgba(217,4,41,0.03);}
.titre-num{color:var(--red);font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 4px;}
.titre-texte{color:#fff;font-size:1rem;font-weight:700;line-height:1.4;margin:0;}

/* ══ OFFRE CARD ══════════════════════════════════════════════ */
.offre-card{
  background:linear-gradient(135deg,rgba(5,15,0,.85),rgba(10,24,0,.85));
  border:2px solid rgba(51,102,0,.5);border-radius:16px;
  padding:1.2rem;margin-bottom:.8rem;transition:all .25s;
  animation:fadeInUp .5s ease both;
}
.offre-card:hover{transform:translateY(-4px);box-shadow:0 10px 30px rgba(51,102,0,.25);border-color:#55aa00;}
.offre-nom{color:#77dd22;font-weight:900;font-size:.92rem;margin:0 0 5px;}
.offre-desc{color:#bbb;font-size:.83rem;line-height:1.7;margin:0 0 7px;}
.offre-prix{color:#55dd88;font-weight:700;font-size:.76rem;margin:0;}

/* ══ METRIC ITEM ═════════════════════════════════════════════ */
.metric-item{
  background:var(--bg2);border:2px solid var(--border);
  border-radius:14px;padding:.8rem;text-align:center;
  transition:all .25s;animation:fadeInUp .5s ease both;
}
.metric-item:hover{border-color:var(--red);transform:translateY(-3px);box-shadow:0 7px 22px rgba(217,4,41,0.18);}
.metric-item .ml{color:var(--muted);font-size:.58rem;text-transform:uppercase;letter-spacing:1px;}
.metric-item .mv{color:#fff;font-size:clamp(.8rem,3vw,.95rem);font-weight:900;margin-top:3px;}

/* ══ JOUR CARD (plan 7j) ═════════════════════════════════════ */
.jour-card{
  background:var(--bg2);border:2px solid var(--border);
  border-radius:14px;padding:1.1rem;margin-bottom:.75rem;
  transition:border-color .2s;
}
.jour-card:hover{border-color:rgba(217,4,41,0.28);}
.jour-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:30px;height:30px;border-radius:50%;font-weight:900;
  font-size:.78rem;margin-bottom:7px;
}
.jour-titre{color:#fff;font-weight:800;font-size:.88rem;margin:0 0 8px;}
.jour-row{display:flex;gap:8px;margin-bottom:4px;flex-wrap:wrap;}
.jour-lbl{color:var(--muted);font-size:.66rem;min-width:60px;flex-shrink:0;}
.jour-val{color:var(--text);font-size:.78rem;}

/* ══ TEMOIGNAGE ══════════════════════════════════════════════ */
.temo-card{
  background:var(--bg2);border:2px solid var(--border);
  border-radius:14px;padding:1.1rem;margin-bottom:.75rem;
  transition:border-color .2s;
}
.temo-card:hover{border-color:rgba(217,4,41,0.2);}
.temo-head{display:flex;gap:12px;align-items:center;margin-bottom:8px;}
.temo-av{
  width:40px;height:40px;border-radius:50%;flex-shrink:0;
  background:linear-gradient(135deg,var(--red),#ff6b35);
  display:flex;align-items:center;justify-content:center;
  font-weight:900;font-size:1rem;color:#fff;
}
.temo-name{color:#fff;font-weight:700;font-size:.86rem;margin:0;}
.temo-ville{color:var(--muted);font-size:.68rem;margin:0;}
.temo-stars{color:#ff9944;font-size:.72rem;}
.temo-body{color:#bbb;font-size:.83rem;line-height:1.78;font-style:italic;margin:0;}

/* ══ PAYS CARD ═══════════════════════════════════════════════ */
.pays-card{
  background:var(--bg2);border:2px solid var(--border);
  border-radius:14px;padding:1.2rem .8rem;
  text-align:center;cursor:pointer;transition:all .2s;
  text-decoration:none;display:block;
}
.pays-card:hover{border-color:var(--red);background:rgba(217,4,41,0.07);transform:translateY(-3px);}
.pays-flag{font-size:1.8rem;margin-bottom:5px;}
.pays-nom{color:#fff;font-weight:700;font-size:.78rem;margin:0;}
.pays-sub{color:var(--muted);font-size:.6rem;margin:2px 0 0;}

/* ══ EXPORT SECTION ══════════════════════════════════════════ */
.export-section{
  background:linear-gradient(135deg,rgba(10,0,0,.9),rgba(21,0,0,.9));
  border:3px solid var(--red);border-radius:18px;
  padding:1.5rem;margin-top:1.5rem;text-align:center;
  animation:fadeInUp .6s ease both;
  box-shadow:0 0 40px rgba(217,4,41,0.14);
}

/* ══ GOLDEN RULE ═════════════════════════════════════════════ */
.golden-rule{
  background:linear-gradient(135deg,rgba(14,0,0,.8),rgba(26,8,0,.8));
  border:2px solid rgba(204,85,0,.5);border-radius:13px;
  padding:.9rem 1rem;margin:.5rem 0;
}
.golden-rule p{color:#ffaa55;font-size:.76rem;margin:0;line-height:1.85;}

/* ══ GAINS TABLE ═════════════════════════════════════════════ */
.gt{width:100%;border-collapse:collapse;font-size:.81rem;}
.gt th{
  background:linear-gradient(135deg,#D90429,#a80220);
  color:#fff;padding:9px 11px;font-size:.65rem;
  text-transform:uppercase;letter-spacing:1px;text-align:center;
}
.gt td{background:var(--bg);color:#ccc;padding:9px 11px;text-align:center;border-bottom:1px solid rgba(255,255,255,0.04);}
.gt tr:hover td{background:var(--bg2);color:#fff;}
.gt .pos{color:#44dd88;font-weight:700;}
.gt .neg{color:#ff4444;font-weight:700;}
.gt .hl td{background:rgba(217,4,41,0.05) !important;border-left:3px solid var(--red);}

/* ══ LISTE PEURS/DESIRS ══════════════════════════════════════ */
.list-item{
  padding:5px 10px 5px 13px;border-left:2px solid;
  margin-bottom:4px;font-size:.8rem;color:#ccc;
  background:var(--bg2);border-radius:0 7px 7px 0;
}

/* ══ TAGS ════════════════════════════════════════════════════ */
.tag{
  display:inline-block;background:var(--bg3);
  border:1px solid var(--border2);
  border-radius:20px;padding:3px 10px;
  font-size:.7rem;color:var(--muted);margin:2px;
}

/* ══ IMG CARD ════════════════════════════════════════════════ */
.img-card{
  background:var(--bg2);border:2px solid var(--border);
  border-radius:13px;overflow:hidden;transition:all .2s;
  margin-bottom:.8rem;
}
.img-card:hover{border-color:rgba(217,4,41,0.3);transform:translateY(-2px);}
.img-footer{padding:8px 10px;}
.img-footer p{color:var(--muted);font-size:.65rem;margin:0 0 6px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.img-dl{
  display:block;text-align:center;
  background:var(--red);color:#fff !important;
  border-radius:7px;padding:6px 0;
  font-weight:700;font-size:.72rem;
  text-decoration:none !important;transition:background .15s;
}
.img-dl:hover{background:var(--red2);}

/* ══ COMP BAR ════════════════════════════════════════════════ */
.comp-bar{margin-bottom:7px;}
.comp-bar-hd{display:flex;justify-content:space-between;margin-bottom:3px;}
.comp-bar-lbl{font-size:.7rem;color:var(--muted);}
.comp-bar-val{font-size:.7rem;font-weight:700;}
.comp-bar-track{height:5px;background:var(--bg3);border-radius:3px;overflow:hidden;}
.comp-bar-fill{height:100%;border-radius:3px;}

/* ══ ALERTE ══════════════════════════════════════════════════ */
.alerte-red{
  background:rgba(217,4,41,0.07);
  border:2px solid rgba(217,4,41,0.28);
  border-radius:10px;padding:8px 12px;margin-top:8px;
}
.alerte-red p{color:#ff6b6b;font-weight:700;font-size:.75rem;margin:0;}

/* ══ BUDGET TIP ══════════════════════════════════════════════ */
.budget-tip{
  background:rgba(255,180,0,0.05);
  border:1px solid rgba(255,180,0,0.18);
  border-radius:10px;padding:10px 14px;
}
.budget-tip p{color:#ffcc66;font-size:.77rem;margin:0;line-height:1.75;}

/* ══ ST.CODE ═════════════════════════════════════════════════ */
.stCodeBlock, pre, code,
[data-testid="stCode"] > div,
[data-testid="stCode"] pre {
  background-color:#0a0e15 !important;
  color:#dde !important;
  border:1px solid rgba(255,255,255,0.07) !important;
  border-radius:10px !important;
  font-size:.78rem !important;
}
[data-testid="stCode"] button,
[data-testid="stCode"] button:hover {
  background:var(--red) !important;
  color:#fff !important;
  border-radius:5px !important;
  opacity:1 !important;
}

/* ══ MISC ════════════════════════════════════════════════════ */
#MainMenu, footer, header{visibility:hidden;}
label{color:#8b949e !important;font-weight:600 !important;font-size:.8rem !important;}
hr{border-color:rgba(255,255,255,0.07) !important;margin:14px 0 !important;}

@media(max-width:768px){
  .block-container{padding-left:.4rem !important;padding-right:.4rem !important;}
  .hero-banner{padding:1.4rem .9rem;}
  .stTabs [data-baseweb="tab"]{padding:.3rem .4rem !important;font-size:.6rem !important;}
  .gt th,.gt td{padding:6px 5px;font-size:.65rem;}
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# HELPERS — ZÉRO DOUBLON
# règle : les cartes HTML servent à AFFICHER joliment
#         st.code() sert UNIQUEMENT à copier
#         on n'affiche JAMAIS le même texte dans les deux
# ══════════════════════════════════════════════════════════════════════
def slabel(t):
    st.markdown(f'<div class="slabel">{t}</div>', unsafe_allow_html=True)

def copy_box(text: str):
    """Boîte copiable unique — remplace tout st.code() dans l'app."""
    st.code(text, language=None)

def section_header(title):
    st.markdown(f'<div style="border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:.5rem;margin-bottom:.8rem;"><span style="color:var(--red);font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:2px;">{title}</span></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# MÉTIER
# ══════════════════════════════════════════════════════════════════════
def get_pub_budget(v):
    if v <= 10:   return "5$–7$/j"
    elif v <= 20: return "7$–10$/j"
    else:         return "15$–20$/j"

def calc_rentabilite(ventes, prix_moyen, prix_achat):
    ca  = ventes * prix_moyen
    cp  = ventes * prix_achat
    ff  = ventes * 5000
    bn  = ca - cp - ff
    return ca, cp, ff, cp+ff, bn

def calc_score_produit(prix_achat, prix_vente_moy, data):
    score_ia = int(data.get("score", 5))
    type_p   = data.get("type_produit", "wow")
    categ    = data.get("avatar", {}).get("categorie", "Autre")
    nb_des   = len(data.get("desirs", []))

    if prix_vente_moy<=7000:    c1=10
    elif prix_vente_moy<=10000: c1=9
    elif prix_vente_moy<=15000: c1=7
    elif prix_vente_moy<=22000: c1=5
    elif prix_vente_moy<=35000: c1=3
    else: c1=1
    d1=f"Prix {prix_vente_moy:,.0f} FCFA — {'✅ Impulsif'if c1>=9 else '⚠️ Réfléchi'if c1>=6 else '🔴 Risqué'}"

    if type_p=="wow":
        c2=9; d2="WOW — effet visuel immédiat"
    else:
        kw=" ".join(data.get("peurs",[])+data.get("desirs",[])).lower()
        sd=sum(1 for w in ["douleur","fatigue","insomnie","argent","poids","peau","cheveux"] if w in kw)
        c2=9 if sd>=3 else 7 if sd>=2 else 5 if sd>=1 else 3
        d2=f"Problème-solution · {sd} douleurs quotidiennes"

    cf={"Domestique":9,"Beauté & Soins":9,"Santé":8,"Tech":8,"Mode":7,"Alimentation":7}
    c3=min(10,cf.get(categ,6)+(1 if type_p=="wow" else 0))
    d3=f"{categ} — {'✅ Facile à filmer'if c3>=8 else '⚠️ Moyen'if c3>=6 else '🔴 Difficile'}"

    cr={"Tech":8,"Santé":7,"Beauté & Soins":7,"Luxe":6,"Mode":4,"Alimentation":3}
    c4=cr.get(categ,6)
    if score_ia>=8: c4=min(10,c4+1)
    if score_ia<=4: c4=max(1,c4-2)
    d4=f"{'✅ Rare localement'if c4>=7 else '⚠️ Moyen'if c4>=5 else '🔴 Partout en marché'}"

    c5=9 if score_ia>=8 and nb_des>=3 else 7 if score_ia>=7 else 5 if score_ia>=5 else 3
    d5=f"IA {score_ia}/10 · {nb_des} désirs · {'✅ Crédible'if c5>=7 else '⚠️ Mitigé'if c5>=5 else '🔴 Douteux'}"

    raw=c1*.30+c2*.25+c3*.20+c4*.15+c5*.10
    echecs=sum(1 for c in [c1,c2,c3,c4,c5] if c<=4)
    alerte=None
    if echecs>=2:
        raw=min(raw,6.0)
        alerte=f"⚠️ {echecs} critères faibles — score plafonné à 6/10"

    return {
        "score_final": round(max(1.0,min(10.0,raw)),1),
        "alerte": alerte,
        "criteres":[
            {"nom":"💰 Prix & Accessibilité",  "note":c1,"desc":d1,"poids":"30%"},
            {"nom":"⚡ Utilité & WOW",          "note":c2,"desc":d2,"poids":"25%"},
            {"nom":"🎬 Potentiel Créatives",    "note":c3,"desc":d3,"poids":"20%"},
            {"nom":"💎 Rareté Locale",          "note":c4,"desc":d4,"poids":"15%"},
            {"nom":"🛡️ Crédibilité",           "note":c5,"desc":d5,"poids":"10%"},
        ]
    }

def calc_budget_pub(obj, pv, tc_pct, pa):
    cpm=0.80; ctr=0.018
    tc=max(tc_pct/100, 0.001)
    clics=obj/tc; cpc=cpm/(ctr*1000)
    bj=clics*cpc; marge=pv-pa-5000
    return {"bj":round(bj,2),"b3":round(bj*3,2),"b5":round(bj*5,2),
            "cpc":round(cpc,3),"clics":round(clics),"marge":marge,
            "benef":round(marge*obj - bj*655)}

def search_bing_images(query, n=10):
    results=[]
    try:
        q=urllib.parse.quote_plus(query)
        url=f"https://www.bing.com/images/search?q={q}&form=HDRSC2"
        req=urllib.request.Request(url,headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Accept-Language":"fr-FR,fr;q=0.9",
        })
        html=urllib.request.urlopen(req,timeout=12).read().decode("utf-8",errors="ignore")
        murls=re.findall(r'"murl"\s*:\s*"(https?://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"',html)
        thurls=re.findall(r'"turl"\s*:\s*"(https?://[^"]+)"',html)
        for i,m in enumerate(murls[:n]):
            results.append({"url":m,"thumb":thurls[i] if i<len(thurls) else m,"title":f"#{i+1}"})
    except: pass
    return results

# ══════════════════════════════════════════════════════════════════════
# JSON REPAIR
# ══════════════════════════════════════════════════════════════════════
def repair_json(raw):
    raw=re.sub(r"^```(?:json)?\s*","",raw.strip())
    raw=re.sub(r"\s*```$","",raw).strip()
    try: return json.loads(raw)
    except: pass
    stack=[]; last=0; ins=False; esc=False
    for i,c in enumerate(raw):
        if esc: esc=False; continue
        if c=="\\" and ins: esc=True; continue
        if c=='"' and not esc: ins=not ins; continue
        if ins: continue
        if c in("{","["): stack.append(c)
        elif c in("}","]"):
            if stack: stack.pop(); last=i+1
    closing="".join("}" if b=="{" else "]" for b in reversed(stack))
    try: return json.loads(raw[:last]+closing)
    except: return {}

# ══════════════════════════════════════════════════════════════════════
# GROQ
# ══════════════════════════════════════════════════════════════════════
def call_groq(prompt, images):
    from groq import Groq
    client=Groq(api_key=st.secrets["GROQ_API_KEY"])
    content=[]
    for img in images:
        b64=base64.b64encode(img).decode()
        content.append({"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}})
    content.append({"type":"text","text":prompt})
    r=client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role":"user","content":content}],
        max_tokens=8000,temperature=0.7,
    )
    return repair_json(r.choices[0].message.content.strip())

def test_groq():
    try:
        from groq import Groq
        key=st.secrets.get("GROQ_API_KEY","")
        if not key: return {"ok":False,"msg":"GROQ_API_KEY absent des Secrets"}
        r=Groq(api_key=key).chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role":"user","content":"Réponds juste OK"}],max_tokens=5,
        )
        return {"ok":True,"msg":f"✅ Groq OK · {r.choices[0].message.content.strip()}"}
    except Exception as e:
        return {"ok":False,"msg":str(e)}

# ══════════════════════════════════════════════════════════════════════
# PROMPT BÉTON
# ══════════════════════════════════════════════════════════════════════
def build_prompt(name, pa, pmin, pmax):
    return f"""Tu es un expert neuro-marketing e-commerce Afrique Francophone (Togo, Sénégal, Côte d'Ivoire, Bénin).
Tout doit être 100% adapté au contexte africain.

PRODUIT : {name}
PRIX ACHAT : {pa:,} FCFA | PRIX VENTE : {pmin:,}–{pmax:,} FCFA

══════════════════════════════════
RÈGLES ABSOLUES — VIOLATION = RÉSULTAT INUTILE
══════════════════════════════════

① SCRIPTS VOIX-OFF — RÈGLE DE FER :
   → CHAQUE script = EXACTEMENT entre 130 et 170 MOTS. PAS 40, PAS 60, PAS 90 mots. 130 à 170.
   → STRUCTURE OBLIGATOIRE (14 à 16 lignes aérées) :
     Ligne 1-2   : Hook choc — statistique ou question choc
     Ligne 3-5   : Problème / situation que le client vit
     Ligne 6-8   : Présentation du produit + bénéfice principal
     Ligne 9-11  : Démonstration / ce que ça fait concrètement
     Ligne 12-13 : Preuve sociale africaine (prénom + ville africaine)
     Ligne 14-15 : CTA urgent avec prix et livraison
   → \\n entre chaque phrase courte (1-2 phrases max par ligne).
   → Style : fluide, oral, naturel. Prénoms africains (Kofi, Amina, Fatou, Moussa, Kwame...).
   → INTERDIT : balises techniques (Hook:, CTA:, Act 1:). Texte naturel uniquement.

② SHOPIFY PARAGRAPHES — RÈGLE DE FER :
   → Titre = BÉNÉFICE CLIENT DIRECT. INTERDIT : "Découvrez", "Pourquoi choisir", "Les avantages".
   → CHAQUE paragraphe = EXACTEMENT 4 phrases complètes séparées par \\n.
   → Style émotionnel, contexte africain, phrases courtes et percutantes.

③ FACEBOOK ADS : 3 variantes. Titre emoji choc + 5 lignes séparées par \\n.

④ PLAN 7 JOURS : Actions concrètes, budgets réalistes pour marché africain.

⑤ TÉMOIGNAGES : Style oral africain authentique. Pas de style "catalogue".

Réponds UNIQUEMENT en JSON valide. Rien avant, rien après.

{{
  "score": 7,
  "score_justification": "Analyse 2-3 phrases sur le potentiel marché africain",
  "type_produit": "wow",
  "ameliorations": ["conseil concret 1","conseil 2","conseil 3"],
  "public_cible": "Description précise : âge, ville, revenus FCFA, habitudes africaines",
  "peurs": ["peur africaine précise 1","peur 2","peur 3"],
  "desirs": ["désir africain concret 1","désir 2","désir 3"],
  "mots_cles": ["mot1","mot2","mot3","mot4","mot5"],
  "offres": [
    {{"nom":"Nom offre 1","description":"Contenu précis","prix_suggere":"XXXX FCFA","argument":"Argument africain"}},
    {{"nom":"Offre 2","description":"Contenu","prix_suggere":"XXXX FCFA","argument":"Argument"}},
    {{"nom":"Offre 3","description":"Contenu","prix_suggere":"XXXX FCFA","argument":"Argument"}}
  ],
  "facebook_ads": [
    {{"angle":"Émotionnel","accroche":"🔥 TITRE CHOC AFRICAIN","texte":"ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5 CTA"}},
    {{"angle":"Preuve Sociale","accroche":"⭐ TÉMOIGNAGE AFRICAIN","texte":"ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5"}},
    {{"angle":"Urgence","accroche":"⚠️ STOCK LIMITÉ","texte":"ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5"}}
  ],
  "shopify": {{
    "titres": [
      {{"angle":"Bénéfice Principal","titre":"Titre magnétique 1 — bénéfice direct"}},
      {{"angle":"Curiosité / WOW","titre":"Titre intriguant 2"}},
      {{"angle":"Urgence / FOMO","titre":"Titre urgent 3"}}
    ],
    "paragraphes": [
      {{"titre":"Titre bénéfice direct §1","texte":"Phrase 1 percutante.\\nPhrase 2 émotionnelle.\\nPhrase 3 preuve.\\nPhrase 4 statut ou CTA."}},
      {{"titre":"Titre bénéfice direct §2","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice direct §3","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice direct §4","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice direct §5","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice direct §6","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}}
    ]
  }},
  "scripts": [
    {{"angle":"Émotionnel","texte_complet":"130–170 MOTS OBLIGATOIRE.\\nHook choc 2 lignes.\\nProblème 3 lignes.\\nSolution 3 lignes.\\nDémonstration 3 lignes.\\nPreuve sociale africaine 2 lignes.\\nCTA urgent 2 lignes."}},
    {{"angle":"Bénéfice Direct","texte_complet":"130–170 MOTS OBLIGATOIRE.\\nStructure identique, angle bénéfice."}},
    {{"angle":"Urgence & Statut","texte_complet":"130–170 MOTS OBLIGATOIRE.\\nStructure identique, angle statut social africain."}}
  ],
  "angles_marketing": [
    {{"angle":"Peur & Urgence","titre":"Titre court choc","accroche":"Phrase d'attaque directe africaine"}},
    {{"angle":"Désir & Aspiration","titre":"Titre court","accroche":"Phrase qui fait rêver"}},
    {{"angle":"Preuve Sociale","titre":"Titre court","accroche":"Chiffre ou témoignage africain"}},
    {{"angle":"Curiosité","titre":"Titre court","accroche":"Question intrigante"}},
    {{"angle":"Transformation","titre":"Titre court","accroche":"Avant/après concret"}}
  ],
  "avatar": {{
    "sexe":"homme / femme / les deux",
    "age":"25–40 ans",
    "francais":"familier",
    "categorie":"Domestique",
    "prenom_type":"Kofi ou Amina ou autre prénom africain",
    "ville":"Lomé ou Abidjan ou Dakar",
    "profession":"Profession africaine précise",
    "revenu":"80 000–120 000 FCFA/mois",
    "mode_vie":"Quotidien africain concret en 2 phrases",
    "frustrations":["frustration précise 1","frustration 2","frustration 3"],
    "desirs":["désir concret 1","désir 2","désir 3"],
    "objections":["objection réelle 1","objection 2","objection 3"],
    "message_cle":"La phrase exacte qui convainc immédiatement"
  }},
  "creatives": [
    {{"concept":"Concept 1","scene":"Scène précise à filmer","message":"Message marketing","accroche_type":"WOW"}},
    {{"concept":"Concept 2","scene":"Scène 2","message":"Message 2","accroche_type":"Problème"}},
    {{"concept":"Concept 3","scene":"Scène 3","message":"Message 3","accroche_type":"Témoignage"}},
    {{"concept":"Concept 4","scene":"Scène 4","message":"Message 4","accroche_type":"Statistique"}}
  ],
  "images_produit": [
    {{"type":"Démonstration","description":"Visuel démo précis"}},
    {{"type":"Utilisation","description":"Personne utilisant, contexte africain"}},
    {{"type":"Lifestyle","description":"Lifestyle africain réel"}},
    {{"type":"Avantage Clé","description":"Avantage principal visuel"}},
    {{"type":"Gros Plan","description":"Qualité et finition"}}
  ],
  "plan_7j": [
    {{"jour":1,"titre":"Mise en place","action":"Action précise","budget":"5$","ciblage":"Intérêts Facebook précis","contenu":"Ce qu'il faut publier exactement"}},
    {{"jour":2,"titre":"Premier test pub","action":"Action","budget":"5$","ciblage":"Ciblage","contenu":"Contenu précis"}},
    {{"jour":3,"titre":"Analyse résultats","action":"Action","budget":"5$","ciblage":"Ciblage affiné","contenu":"Contenu"}},
    {{"jour":4,"titre":"Optimisation","action":"Action","budget":"7$","ciblage":"Ciblage winner","contenu":"Contenu"}},
    {{"jour":5,"titre":"Scale progressif","action":"Action","budget":"10$","ciblage":"Ciblage","contenu":"Contenu"}},
    {{"jour":6,"titre":"Consolidation","action":"Action","budget":"10$","ciblage":"Retargeting","contenu":"Contenu"}},
    {{"jour":7,"titre":"Bilan & Décision","action":"Analyser et décider scale ou stop","budget":"Budget bilan","ciblage":"Lookalike","contenu":"Contenu bilan"}}
  ],
  "temoignages": [
    {{"prenom":"Amina","ville":"Lomé","produit_utilise":"2 semaines","avis":"Témoignage naturel oral africain 2-3 phrases concrètes","note":5}},
    {{"prenom":"Kofi","ville":"Abidjan","produit_utilise":"1 mois","avis":"Témoignage 2","note":5}},
    {{"prenom":"Fatou","ville":"Dakar","produit_utilise":"3 semaines","avis":"Témoignage 3","note":5}},
    {{"prenom":"Moussa","ville":"Cotonou","produit_utilise":"2 mois","avis":"Témoignage 4","note":4}},
    {{"prenom":"Awa","ville":"Conakry","produit_utilise":"1 semaine","avis":"Témoignage 5","note":5}}
  ]
}}"""

def build_export(name, pa, pmin, pmax, data):
    sep="="*55
    ls=[sep,"  ECOMASTER LABO PRO — PACK MARKETING COMPLET",
        f"  Produit : {name}",
        f"  Prix achat : {pa:,} F | Vente : {pmin:,}–{pmax:,} FCFA",
        f"  Score LABO : {data.get('score','?')}/10 | Type : {data.get('type_produit','').upper()}",
        sep,"",
        "📊 STRATÉGIE","-"*40,
        data.get("score_justification",""),
        "\nPublic cible :",data.get("public_cible",""),
        "\nPeurs:"]+[f"  - {p}" for p in data.get("peurs",[])]+\
       ["\nDésirs:"]+[f"  - {d}" for d in data.get("desirs",[])]+\
       ["","🎁 OFFRES","-"*40]
    for i,o in enumerate(data.get("offres",[])):
        ls+=[f"Offre {i+1} — {o.get('nom','')}",
             f"  {o.get('description','')} | Prix : {o.get('prix_suggere','')}",""]
    ls+=["","🛍️ SHOPIFY","-"*40,"TITRES :"]
    for t in data.get("shopify",{}).get("titres",[]):
        ls.append(f"  [{t.get('angle','')}] {t.get('titre','')}")
    ls.append("\nFICHE PRODUIT :")
    for p in data.get("shopify",{}).get("paragraphes",[]):
        ls+=[f"\n{p.get('titre','')}", p.get("texte","")]
    ls+=["","📣 FACEBOOK ADS","-"*40]
    for i,ad in enumerate(data.get("facebook_ads",[])):
        ls+=[f"--- Ad {i+1} [{ad.get('angle','')}] ---",
             f"TITRE : {ad.get('accroche','')}",ad.get("texte",""),""]
    ls+=["","🎙️ SCRIPTS VOIX-OFF","-"*40]
    for i,s in enumerate(data.get("scripts",[])):
        ls+=[f"--- Script {i+1} — {s.get('angle','')} ---",s.get("texte_complet",""),""]
    ls+=["","🗓️ PLAN 7 JOURS","-"*40]
    for j in data.get("plan_7j",[]):
        ls+=[f"Jour {j.get('jour','')} : {j.get('titre','')}",
             f"  Action : {j.get('action','')}",
             f"  Budget : {j.get('budget','')} | Ciblage : {j.get('ciblage','')}",
             f"  Contenu : {j.get('contenu','')}",""]
    ls+=["",sep,"  EcoMaster Labo Pro · by LABO",sep]
    return "\n".join(ls)


# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
PAGES=[
    ("analyse","🔬","Analyser un produit"),
    ("images","🖼️","Images Produit"),
    ("spy","🕵️","Spy Concurrents"),
    ("budget","💰","Budget Pub IA"),
    ("comparateur","⚖️","Comparateur"),
    ("temoignages","💬","Témoignages"),
]

with st.sidebar:
    st.markdown("""<div style="padding:.9rem 1rem .7rem;">
      <p style="color:#D90429;font-weight:800;font-size:.98rem;margin:0;letter-spacing:-.3px;">🚀 EcoMaster <span style="color:#fff;">Labo Pro</span></p>
      <p style="color:#444c56;font-size:.63rem;margin:.2rem 0 0;">by LABO · E-commerce Afrique</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<p style="color:#444c56;font-size:.58rem;text-transform:uppercase;letter-spacing:1.5px;padding:.8rem 1rem .3rem;margin:0;">Navigation</p>', unsafe_allow_html=True)

    for pid, icon, label in PAGES:
        active = st.session_state["nav_page"] == pid
        prefix = "▶ " if active else ""
        style  = "border-color:var(--red) !important;color:#fff !important;background:rgba(217,4,41,0.1) !important;" if active else ""
        if st.button(f"{icon}  {prefix}{label}", key=f"nav_{pid}", use_container_width=True):
            st.session_state["nav_page"] = pid
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p style="color:#444c56;font-size:.58rem;text-transform:uppercase;letter-spacing:1.5px;padding:.4rem 1rem .3rem;margin:0;">Historique</p>', unsafe_allow_html=True)

    history = st.session_state["history"]
    if not history:
        st.markdown('<p style="color:#2d333b;font-size:.75rem;font-style:italic;padding:0 1rem;">Aucune analyse</p>', unsafe_allow_html=True)
    else:
        if st.button("🗑️  Effacer l'historique", key="clear_hist", use_container_width=True):
            st.session_state["history"]=[]
            write_history_file([])
        for i, h in enumerate(history[:7]):
            short=h["name"][:16]+("…" if len(h["name"])>16 else "")
            if st.button(f"↩  {short} · {h.get('score','?')}/10", key=f"hist_{i}", use_container_width=True):
                st.session_state.update({
                    "result":h["data"],"analyzed":True,
                    "active_product":h["name"],"active_price":h["prix_achat"],
                    "nav_page":"analyse",
                })
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""<div class="golden-rule">
      <p>💡 <b style="color:#ffcc44;">Règle d'or LABO</b><br>
      Budget test : <b style="color:#ff8844;">4$–7$/jour</b><br>
      Prix = achat + <b style="color:#ff8844;">8K–12K FCFA</b><br>
      <span style="color:#444c56;font-size:.7rem;">Frais fixes : 5 000 FCFA/vente<br>(2K livraison · 2K pub · 1K closing)</span></p>
    </div>""", unsafe_allow_html=True)

    with st.expander("🔌 Tester connexion Groq"):
        if st.button("Tester la clé API", key="tg", use_container_width=True):
            r=test_groq()
            (st.success if r["ok"] else st.error)(r["msg"])


# ══════════════════════════════════════════════════════════════════════
# HERO (affiché uniquement sur la page analyse)
# ══════════════════════════════════════════════════════════════════════
page = st.session_state["nav_page"]

if page == "analyse":
    st.markdown("""<div class="hero-banner">
      <h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
      <p class="slogan">Analyse · Stratégie · Publicité · Ventes</p>
      <p class="sub">créé par LABO · E-commerce Afrique Francophone</p>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE : ANALYSE
# ══════════════════════════════════════════════════════════════════════
if page == "analyse":

    f1, f2 = st.columns([3,2], gap="large")
    with f1:
        product_name = st.text_input("📦 Nom du Produit",
            value=st.session_state.get("active_product",""),
            placeholder="Ex: Crème Beauty Milk, Lampe solaire LED...")
        purchase_price = st.number_input("💰 Prix d'Achat (FCFA)", min_value=0, step=500,
            value=int(st.session_state.get("active_price",5000)))
        objectif_ventes = st.number_input("🎯 Objectif ventes/jour", min_value=1, step=1,
            value=int(st.session_state.get("active_ventes",10)))
    with f2:
        uploaded_files = st.file_uploader("📸 Photos produit (1–3)",
            type=["jpg","jpeg","png","webp"], accept_multiple_files=True)
        if uploaded_files:
            tc=st.columns(3)
            for i,f in enumerate(uploaded_files[:3]):
                with tc[i]: st.image(f, width=88)

    pmin  = purchase_price + 8000
    pmax  = purchase_price + 12000
    pmoy  = (pmin + pmax) / 2
    marge = pmin - purchase_price - 5000

    st.markdown("<br>", unsafe_allow_html=True)
    p1,p2,p3,p4 = st.columns(4, gap="small")
    with p1: st.markdown(f'<div class="price-box"><div class="label">💵 Prix Min</div><div class="value">{pmin:,}<span class="currency"> F</span></div></div>', unsafe_allow_html=True)
    with p2: st.markdown(f'<div class="price-box"><div class="label">💵 Prix Max</div><div class="value">{pmax:,}<span class="currency"> F</span></div></div>', unsafe_allow_html=True)
    with p3: st.markdown(f'<div class="price-box" style="border-color:{"#44dd88" if marge>0 else "#ff4444"}"><div class="label">📈 Marge Nette</div><div class="value" style="color:{"#44dd88" if marge>0 else "#ff4444"}">{marge:,}<span class="currency"> F</span></div></div>', unsafe_allow_html=True)
    with p4: st.markdown(f'<div class="price-box"><div class="label">📣 Budget Pub</div><div class="value" style="color:#ff9944;font-size:1rem;">{get_pub_budget(objectif_ventes)}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    btn = st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

    if btn:
        if not product_name.strip():
            st.error("⚠️ Entre le nom du produit.")
        elif not uploaded_files:
            st.error("⚠️ Upload au moins une photo produit.")
        else:
            imgs=[f.read() for f in uploaded_files[:3]]
            with st.spinner("🧠 Groq analyse ton produit… 15–25 secondes ⏳"):
                try:
                    data=call_groq(build_prompt(product_name,purchase_price,pmin,pmax),imgs)
                    st.session_state.update({
                        "result":data,"analyzed":True,
                        "active_product":product_name,"active_price":purchase_price,
                        "active_ventes":objectif_ventes,
                    })
                    save_to_history(product_name,data.get("score","?"),data,purchase_price)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur Groq : {e}")
                    if "GROQ_API_KEY" in str(e):
                        st.info("🔑 Ajoute ta clé dans Streamlit Secrets : GROQ_API_KEY = \"gsk_...\"")

    # ── RÉSULTATS ─────────────────────────────────────────────────────
    if st.session_state.get("analyzed") and st.session_state.get("result"):
        data   = st.session_state["result"]
        aname  = st.session_state.get("active_product","")
        aprice = st.session_state.get("active_price",5000)
        apmin  = aprice+8000; apmax=aprice+12000; apmoy=(apmin+apmax)/2
        aventes= st.session_state.get("active_ventes",10)
        type_p = data.get("type_produit","wow")
        scd    = calc_score_produit(aprice,apmoy,data)

        # Bandeau produit
        b_type = "⚡ PRODUIT WOW" if type_p=="wow" else "🎯 PROBLÈME-SOLUTION"
        b_col  = "#D90429" if type_p=="wow" else "#4493f8"
        st.markdown(f"""<div class="result-card" style="border-color:rgba(217,4,41,0.25);margin-top:1.5rem;">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
            <div>
              <p style="color:var(--muted);font-size:.6rem;text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;">Produit analysé</p>
              <p style="color:#fff;font-weight:900;font-size:1.15rem;margin:0 0 5px;">{aname}</p>
              <span style="background:{b_col}22;border:1px solid {b_col}55;color:{b_col};border-radius:6px;padding:2px 9px;font-size:.65rem;font-weight:700;">{b_type}</span>
            </div>
            <div style="text-align:center;">
              <p style="color:#fff;font-weight:900;font-size:2.5rem;margin:0;line-height:1;letter-spacing:-2px;">{scd['score_final']}</p>
              <p style="color:var(--muted);font-size:.6rem;margin:0;">/10 Score LABO</p>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        tabs = st.tabs(["📊 Stratégie","🎁 Offres","🛍️ Shopify","📣 Facebook Ads",
                        "🎙️ Scripts","🎬 Créatives","🎯 Angles","👤 Avatar",
                        "🗓️ Plan 7J","📥 Export"])

        # TAB 0 — STRATÉGIE
        with tabs[0]:
            t0c1, t0c2 = st.columns([1,2], gap="large")
            with t0c1:
                slabel("Score LABO")
                st.markdown(f'<div class="score-wrap"><div class="score-badge"><span class="sn">{scd["score_final"]}</span><span class="sd">/10</span></div></div>', unsafe_allow_html=True)
                if scd.get("alerte"):
                    st.markdown(f'<div class="alerte-red"><p>{scd["alerte"]}</p></div>', unsafe_allow_html=True)

            with t0c2:
                slabel("5 Critères LABO")
                for cr in scd["criteres"]:
                    n=cr["note"]; c="#44dd88" if n>=8 else "#ff9944" if n>=6 else "#ff4444"
                    st.markdown(f"""<div class="crit-row">
                      <div class="crit-note" style="background:{c}18;color:{c};">{n}</div>
                      <div style="flex:1">
                        <p class="crit-name">{cr['nom']} <span class="crit-poids">· {cr['poids']}</span></p>
                        <p class="crit-desc">{cr['desc']}</p>
                      </div>
                    </div>""", unsafe_allow_html=True)

            slabel("Analyse IA")
            copy_box(data.get("score_justification",""))

            a1,a2 = st.columns(2,gap="medium")
            with a1:
                slabel("Public Cible")
                copy_box(data.get("public_cible",""))
                slabel("😨 Peurs")
                for p in data.get("peurs",[]):
                    st.markdown(f'<div class="list-item" style="border-color:#ff4444;">• {p}</div>', unsafe_allow_html=True)
                copy_box("\n".join(f"• {p}" for p in data.get("peurs",[])))
            with a2:
                slabel("✨ Désirs")
                for d in data.get("desirs",[]):
                    st.markdown(f'<div class="list-item" style="border-color:#44dd88;">• {d}</div>', unsafe_allow_html=True)
                copy_box("\n".join(f"• {d}" for d in data.get("desirs",[])))
                slabel("🔑 Mots-Clés")
                st.markdown("".join(f'<span class="tag">{m}</span>' for m in data.get("mots_cles",[])), unsafe_allow_html=True)
                copy_box(" · ".join(data.get("mots_cles",[])))

            slabel("💡 Améliorations")
            for i,a in enumerate(data.get("ameliorations",[])):
                st.markdown(f'<div class="result-card" style="padding:.7rem 1rem;margin-bottom:.5rem;"><span style="color:var(--red);font-size:.7rem;font-weight:700;">#{i+1} </span><span style="font-size:.83rem;color:#ccc;">{a}</span></div>', unsafe_allow_html=True)

            slabel("📊 Tableau Rentabilité")
            rows=""
            for v in [1,3,5,10,15,20,30,50]:
                ca,cp,ff,cg,bn=calc_rentabilite(v,apmoy,aprice)
                cls="pos" if bn>0 else "neg"
                hl=' class="hl"' if v==aventes else ""
                rows+=f"<tr{hl}><td>{v}</td><td>{ca:,.0f}</td><td>{cp:,.0f}</td><td>{ff:,.0f}</td><td class='{cls}'>{bn:,.0f}</td></tr>"
            st.markdown(f"""<table class="gt">
              <tr><th>Ventes</th><th>CA (F)</th><th>Produit</th><th>Frais fixes</th><th>Bénéfice net</th></tr>
              {rows}</table>""", unsafe_allow_html=True)

        # TAB 1 — OFFRES
        with tabs[1]:
            slabel("🎁 3 Offres Commerciales")
            for i,o in enumerate(data.get("offres",[])):
                st.markdown(f"""<div class="offre-card">
                  <p class="offre-nom">🎁 Offre {i+1} — {o.get('nom','')}</p>
                  <p class="offre-desc">{o.get('description','')}</p>
                  <p class="offre-prix">💰 {o.get('prix_suggere','')} &nbsp;·&nbsp; {o.get('argument','')}</p>
                </div>""", unsafe_allow_html=True)
                copy_box(f"Offre {i+1} — {o.get('nom','')}\n{o.get('description','')}\nPrix : {o.get('prix_suggere','')}\nArgument : {o.get('argument','')}")

        # TAB 2 — SHOPIFY
        with tabs[2]:
            shopify=data.get("shopify",{})
            slabel("🏷️ 3 Titres Magnétiques")
            for i,t in enumerate(shopify.get("titres",[])):
                st.markdown(f"""<div class="titre-opt">
                  <p class="titre-num">{t.get('angle','')}</p>
                  <p class="titre-texte">{t.get('titre','')}</p>
                </div>""", unsafe_allow_html=True)
                copy_box(t.get("titre",""))

            st.markdown("<hr>", unsafe_allow_html=True)
            slabel("📝 Fiche Produit — 6 Paragraphes")
            paras=shopify.get("paragraphes",[])
            for j,p in enumerate(paras):
                txtp=p.get("texte","")
                nb=len([l for l in txtp.split("\n") if l.strip()])
                warn=f' <span style="color:#ff4444;font-size:.62rem;">⚠️ {nb} phrases seulement</span>' if nb<4 else ""
                st.markdown(f"""<div class="para-card">
                  <p class="para-titre">§{j+1} — {p.get('titre','')}{warn}</p>
                  <p class="para-texte">{txtp.replace(chr(10),'<br>')}</p>
                </div>""", unsafe_allow_html=True)
                copy_box(f"{p.get('titre','')}\n\n{txtp}")

            slabel("📦 Fiche complète")
            copy_box("\n\n".join(f"{p.get('titre','')}\n{p.get('texte','')}" for p in paras))

        # TAB 3 — FACEBOOK ADS
        with tabs[3]:
            slabel("📣 3 Variantes Facebook Ads")
            for i,ad in enumerate(data.get("facebook_ads",[])):
                accroche=ad.get("accroche",ad.get("titre",""))
                texte=ad.get("texte",ad.get("text",""))
                angle=ad.get("angle",f"Variante {i+1}")
                st.markdown(f"""<div class="ad-block">
                  <p class="ad-angle">{angle}</p>
                  <p class="ad-accroche">{accroche}</p>
                  <p class="ad-texte">{texte.replace(chr(10),'<br>')}</p>
                </div>""", unsafe_allow_html=True)
                copy_box(f"{accroche}\n\n{texte}")

        # TAB 4 — SCRIPTS
        with tabs[4]:
            slabel("🎙️ Scripts Voix-Off — 130 à 170 mots chacun")
            for i,s in enumerate(data.get("scripts",[])):
                txt=s.get("texte_complet",s.get("texte",""))
                wc=len(txt.split())
                wc_ok=125<=wc<=180
                wc_cls="wc-ok" if wc_ok else "wc-bad"
                wc_msg=f"✅ {wc} mots" if wc_ok else f"⚠️ {wc} mots (devrait être 130–170)"
                st.markdown(f"""<div class="script-block">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <p class="script-label">Script {i+1} — {s.get('angle','')}</p>
                    <span class="{wc_cls}">{wc_msg}</span>
                  </div>
                  <p class="script-texte">{txt.replace(chr(10),'<br>')}</p>
                </div>""", unsafe_allow_html=True)
                copy_box(txt)

        # TAB 5 — CRÉATIVES
        with tabs[5]:
            slabel("🎬 4 Concepts Créatives")
            cr_icons=["🔴","🟠","🟡","🟢"]
            for i,cr in enumerate(data.get("creatives",[])):
                ic=cr_icons[i] if i<4 else "🎬"
                st.markdown(f"""<div class="result-card">
                  <p style="color:var(--muted);font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:0 0 6px;">{ic} Créative {i+1}</p>
                  <p style="color:#fff;font-weight:800;font-size:.9rem;margin:0 0 8px;">{cr.get('concept','')}</p>
                  <p style="color:var(--muted);font-size:.7rem;margin:0 0 3px;">🎬 Scène : <span style="color:#ccc;">{cr.get('scene','')}</span></p>
                  <p style="color:var(--muted);font-size:.7rem;margin:0 0 6px;">💬 Message : <span style="color:#ccc;">{cr.get('message','')}</span></p>
                  <span style="background:rgba(217,4,41,0.12);border:1px solid rgba(217,4,41,0.3);color:var(--red);border-radius:5px;padding:2px 8px;font-size:.63rem;font-weight:700;">{cr.get('accroche_type','')}</span>
                </div>""", unsafe_allow_html=True)
                copy_box(f"Concept : {cr.get('concept','')}\nScène : {cr.get('scene','')}\nMessage : {cr.get('message','')}\nAccroche : {cr.get('accroche_type','')}")

        # TAB 6 — ANGLES
        with tabs[6]:
            slabel("🎯 5 Angles Marketing")
            a_icons=["🔴","🟠","🟡","🟢","🔵"]
            for i,ang in enumerate(data.get("angles_marketing",[])):
                ic=a_icons[i] if i<5 else "🎯"
                st.markdown(f"""<div class="result-card">
                  <p style="color:var(--muted);font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:0 0 5px;">{ic} {ang.get('angle','')}</p>
                  <p style="color:#fff;font-weight:800;font-size:.95rem;margin:0 0 5px;">{ang.get('titre','')}</p>
                  <p style="color:#bbb;font-size:.84rem;margin:0;">{ang.get('accroche','')}</p>
                </div>""", unsafe_allow_html=True)
                copy_box(f"{ang.get('titre','')}\n\n{ang.get('accroche','')}")

        # TAB 7 — AVATAR
        with tabs[7]:
            av=data.get("avatar",{})
            if av:
                prenom=av.get("prenom_type","Le client type")
                slabel("👤 Persona Client Type")
                st.markdown(f"""<div class="result-card" style="border-color:rgba(217,4,41,0.2);">
                  <div style="display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;">
                    <div style="width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,var(--red),#ff6b35);
                      display:flex;align-items:center;justify-content:center;font-size:1.5rem;font-weight:900;color:#fff;flex-shrink:0;">{prenom[0].upper()}</div>
                    <div style="flex:1;">
                      <p style="color:#fff;font-weight:900;font-size:1.1rem;margin:0 0 3px;">{prenom}</p>
                      <p style="color:var(--muted);font-size:.73rem;margin:0 0 8px;">{av.get('sexe','—')} · {av.get('age','—')} · {av.get('ville','—')}</p>
                      <div style="display:flex;gap:5px;flex-wrap:wrap;">
                        <span style="background:rgba(217,4,41,0.12);border:1px solid rgba(217,4,41,0.28);color:var(--red);border-radius:5px;padding:2px 8px;font-size:.63rem;font-weight:700;">{av.get('categorie','—')}</span>
                        <span style="background:rgba(68,147,248,0.1);border:1px solid rgba(68,147,248,0.25);color:#4493f8;border-radius:5px;padding:2px 8px;font-size:.63rem;font-weight:700;">{av.get('profession','—')}</span>
                        <span style="background:rgba(255,152,0,0.1);border:1px solid rgba(255,152,0,0.25);color:#ff9944;border-radius:5px;padding:2px 8px;font-size:.63rem;font-weight:700;">{av.get('revenu','—')}</span>
                      </div>
                      <p style="color:#bbb;font-size:.8rem;margin:8px 0 0;line-height:1.7;">{av.get('mode_vie','')}</p>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

                av1,av2,av3=st.columns(3,gap="small")
                with av1:
                    slabel("😤 Frustrations")
                    for f in av.get("frustrations",[]):
                        st.markdown(f'<div class="list-item" style="border-color:#ff4444;">• {f}</div>', unsafe_allow_html=True)
                with av2:
                    slabel("✨ Désirs")
                    for d in av.get("desirs",[]):
                        st.markdown(f'<div class="list-item" style="border-color:#44dd88;">• {d}</div>', unsafe_allow_html=True)
                with av3:
                    slabel("🤔 Objections")
                    for o in av.get("objections",[]):
                        st.markdown(f'<div class="list-item" style="border-color:#ff9944;">• {o}</div>', unsafe_allow_html=True)

                slabel("💬 Message Clé")
                msg=av.get("message_cle","")
                st.markdown(f"""<div class="result-card" style="border-color:rgba(217,4,41,0.25);text-align:center;padding:1.2rem;">
                  <p style="color:#fff;font-size:1rem;font-weight:700;font-style:italic;margin:0;">"{msg}"</p>
                </div>""", unsafe_allow_html=True)
                copy_box(msg)

        # TAB 8 — PLAN 7J
        with tabs[8]:
            slabel("🗓️ Plan de Lancement 7 Jours")
            plan=data.get("plan_7j",[])
            jcols=["#D90429","#ff6b35","#ff9944","#ffd700","#44dd88","#4493f8","#bc8cff"]
            for idx,jour in enumerate(plan):
                c=jcols[idx] if idx<7 else "#D90429"
                st.markdown(f"""<div class="jour-card">
                  <div class="jour-badge" style="background:{c}18;color:{c};border:1px solid {c}40;">{jour.get('jour','')}</div>
                  <p class="jour-titre">{jour.get('titre','')}</p>
                  <div class="jour-row"><span class="jour-lbl">🎯 Action</span><span class="jour-val">{jour.get('action','')}</span></div>
                  <div class="jour-row"><span class="jour-lbl">💸 Budget</span><span class="jour-val" style="color:{c};font-weight:700;">{jour.get('budget','')}</span></div>
                  <div class="jour-row"><span class="jour-lbl">👥 Ciblage</span><span class="jour-val">{jour.get('ciblage','')}</span></div>
                  <div class="jour-row"><span class="jour-lbl">📝 Contenu</span><span class="jour-val">{jour.get('contenu','')}</span></div>
                </div>""", unsafe_allow_html=True)
                copy_box(f"Jour {jour.get('jour','')} — {jour.get('titre','')}\nAction : {jour.get('action','')}\nBudget : {jour.get('budget','')}\nCiblage : {jour.get('ciblage','')}\nContenu : {jour.get('contenu','')}")

        # TAB 9 — EXPORT
        with tabs[9]:
            st.markdown("""<div class="export-section">
              <p style="color:var(--red);font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:2px;margin:0 0 .8rem;">📥 Pack Marketing Complet</p>
              <p style="color:#777;font-size:.78rem;margin:0 0 1rem;">Toute l'analyse exportée en fichier .txt prêt à utiliser</p>
            </div>""", unsafe_allow_html=True)
            export=build_export(aname,aprice,apmin,apmax,data)
            st.download_button(
                label="⬇️  TÉLÉCHARGER MON PACK MARKETING (.txt)",
                data=export,
                file_name=f"labo_{aname.replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ══════════════════════════════════════════════════════════════════════
# PAGE : IMAGES
# ══════════════════════════════════════════════════════════════════════
elif page == "images":
    aname=st.session_state.get("active_product","")
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h2 style="font-size:1.35rem;font-weight:900;color:#fff;margin:0 0 .3rem;">🖼️ Images Produit</h2>
      <p style="color:var(--muted);font-size:.8rem;margin:0;">Images réelles · Affichées dans l'app · Téléchargeables en 1 clic</p>
    </div>""", unsafe_allow_html=True)

    iq,ibtn=st.columns([5,1],gap="small")
    with iq:
        sq=st.text_input("🔍 Nom du produit",value=aname or "",placeholder="Ex: beauty milk serum, solar lamp...",key="img_q")
    with ibtn:
        st.markdown("<br>", unsafe_allow_html=True)
        go=st.button("Chercher", use_container_width=True, key="img_go")

    if go and sq.strip():
        with st.spinner("🔍 Recherche images…"):
            imgs=search_bing_images(sq.strip()+" product",10)
            st.session_state["img_results"]=imgs
            st.session_state["img_query_done"]=sq.strip()

    found=st.session_state.get("img_results",[])
    qdone=st.session_state.get("img_query_done","")

    if found:
        st.markdown(f'<p style="color:#44dd88;font-size:.75rem;font-weight:700;margin:6px 0 14px;">✅ {len(found)} images trouvées pour « {qdone} »</p>', unsafe_allow_html=True)
        for row in range(0,len(found),4):
            cols=st.columns(4,gap="small")
            for ci,img in enumerate(found[row:row+4]):
                with cols[ci]:
                    st.markdown('<div class="img-card">', unsafe_allow_html=True)
                    try: st.image(img["thumb"],use_column_width=True)
                    except: st.image(img["url"],use_column_width=True)
                    st.markdown(f'<div class="img-footer"><p>{img.get("title","")}</p><a href="{img["url"]}" target="_blank" class="img-dl">⬇️ Télécharger</a></div></div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        slabel("Chercher aussi sur ces plateformes")
        qe=urllib.parse.quote_plus(sq if sq else qdone)
        plats=[
            ("🛒 AliExpress",  f"https://fr.aliexpress.com/wholesale?SearchText={qe}"),
            ("🏭 Alibaba",     f"https://www.alibaba.com/trade/search?SearchText={qe}"),
            ("📌 Pinterest",   f"https://www.pinterest.com/search/pins/?q={qe}"),
            ("🛍️ Amazon",     f"https://www.amazon.fr/s?k={qe}"),
            ("🛒 Temu",        f"https://www.temu.com/search_result.html?search_key={qe}"),
        ]
        pc=st.columns(5,gap="small")
        for i,(pn,pu) in enumerate(plats):
            with pc[i]:
                st.markdown(f'<a href="{pu}" target="_blank" style="display:block;text-align:center;background:var(--bg2);border:2px solid var(--border2);border-radius:12px;padding:10px 6px;color:var(--text);text-decoration:none;font-size:.75rem;font-weight:700;transition:border-color .2s;">{pn}</a>', unsafe_allow_html=True)
    elif qdone:
        st.warning(f"⚠️ Aucune image pour « {qdone} ». Essaie en anglais.")
    else:
        st.markdown("""<div style="border:2px dashed rgba(217,4,41,0.2);border-radius:18px;padding:3rem;text-align:center;margin-top:1.5rem;">
          <p style="font-size:2.5rem;margin:0 0 .8rem;">🖼️</p>
          <p style="color:var(--muted2);font-size:.88rem;margin:0 0 4px;font-weight:700;">Lance une recherche</p>
          <p style="color:#2d333b;font-size:.73rem;margin:0;">Les images s'affichent ici directement · Bouton télécharger sous chaque image</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE : SPY
# ══════════════════════════════════════════════════════════════════════
elif page == "spy":
    aname=st.session_state.get("active_product","")
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h2 style="font-size:1.35rem;font-weight:900;color:#fff;margin:0 0 .3rem;">🕵️ Spy Concurrents</h2>
      <p style="color:var(--muted);font-size:.8rem;margin:0;">Trouver qui vend déjà ton produit en Afrique Francophone</p>
    </div>""", unsafe_allow_html=True)

    spy_q=st.text_input("📦 Produit à espionner",value=aname or "",placeholder="Ex: crème éclaircissante, lampe détecteur mouvement...")

    if spy_q.strip():
        qe=urllib.parse.quote_plus(spy_q.strip())
        PAYS=[("🇹🇬","Togo","TG"),("🇸🇳","Sénégal","SN"),("🇨🇮","Côte d'Ivoire","CI"),
              ("🇧🇯","Bénin","BJ"),("🇬🇳","Guinée-Conakry","GN"),("🇨🇬","Congo","CG")]

        slabel("📣 Pubs Facebook par Pays — clique pour voir les concurrents")
        pc=st.columns(3,gap="small")
        for i,(flag,nom,code) in enumerate(PAYS):
            with pc[i%3]:
                fb_url=f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={code}&q={qe}&search_type=keyword_unordered"
                st.markdown(f'<a href="{fb_url}" target="_blank" class="pays-card"><p class="pays-flag">{flag}</p><p class="pays-nom">{nom}</p><p class="pays-sub">Voir pubs →</p></a>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        slabel("🔍 Boutiques Concurrentes")
        spy_links=[
            ("🌍 Google Boutiques Afrique",          f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' Afrique acheter livraison')}"),
            ("🛒 Boutiques Shopify Afrique",           f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' site:myshopify.com Afrique')}"),
            ("🇹🇬 Concurrents Togo",                  f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' Lomé Togo commander')}"),
            ("🇨🇮 Concurrents Côte d'Ivoire",         f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' Abidjan commander')}"),
            ("📌 Créatives Pinterest Afrique",         f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote_plus(spy_q.strip()+' Afrique')}"),
            ("🎬 Vidéos TikTok concurrents",           f"https://www.tiktok.com/search?q={qe}"),
        ]
        sl=st.columns(2,gap="medium")
        for i,(label,url) in enumerate(spy_links):
            with sl[i%2]:
                st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none;"><div class="result-card" style="cursor:pointer;padding:.9rem 1.1rem;"><p style="color:#fff;font-weight:700;font-size:.85rem;margin:0 0 3px;">{label}</p><p style="color:var(--muted);font-size:.66rem;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{url[:55]}…</p></div></a>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        slabel("🎬 Vidéos Concurrentes")
        vc=st.columns(2,gap="medium")
        with vc[0]:
            yt=f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(spy_q.strip()+' publicité Afrique')}"
            st.markdown(f'<a href="{yt}" target="_blank" style="display:block;background:#FF0000;color:#fff;text-align:center;border-radius:14px;padding:13px;font-weight:800;font-size:.82rem;text-decoration:none;letter-spacing:.5px;">▶️  YouTube — Vidéos concurrentes</a>', unsafe_allow_html=True)
        with vc[1]:
            pv=f"https://www.pinterest.com/search/videos/?q={qe}"
            st.markdown(f'<a href="{pv}" target="_blank" style="display:block;background:#E60023;color:#fff;text-align:center;border-radius:14px;padding:13px;font-weight:800;font-size:.82rem;text-decoration:none;letter-spacing:.5px;">📌  Pinterest — Vidéos produit</a>', unsafe_allow_html=True)
    else:
        st.markdown("""<div style="border:2px dashed rgba(217,4,41,0.2);border-radius:18px;padding:3rem;text-align:center;margin-top:1.5rem;">
          <p style="font-size:2.5rem;margin:0 0 .8rem;">🕵️</p>
          <p style="color:var(--muted2);font-size:.88rem;margin:0 0 4px;font-weight:700;">Entre un produit pour espionner</p>
          <p style="color:#2d333b;font-size:.73rem;margin:0;">Pubs Facebook · Boutiques Shopify · YouTube · Pinterest</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE : BUDGET
# ══════════════════════════════════════════════════════════════════════
elif page == "budget":
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h2 style="font-size:1.35rem;font-weight:900;color:#fff;margin:0 0 .3rem;">💰 Calculateur Budget Pub Intelligent</h2>
      <p style="color:var(--muted);font-size:.8rem;margin:0;">Benchmarks réels Facebook Afrique · CPM 0.80$ · CTR 1.8% · Conversion 1–3%</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="budget-tip" style="margin-bottom:1.5rem;">
      <p>📊 <b>Benchmarks Facebook Afrique Francophone</b><br>
      CPM moyen : <b>0.80$</b> · Coût par clic estimé : <b>~0.044$</b> · Taux de conversion e-com : <b>1–3%</b><br>
      Ces chiffres varient selon ta créative et ton ciblage. Utilise comme point de départ.</p>
    </div>""", unsafe_allow_html=True)

    bc1,bc2=st.columns(2,gap="large")
    with bc1:
        pv_b=st.number_input("💰 Prix de vente (FCFA)",min_value=1000,step=500,value=int(st.session_state.get("active_price",5000))+10000)
        pa_b=st.number_input("🏷️ Prix d'achat (FCFA)",min_value=0,step=500,value=int(st.session_state.get("active_price",5000)))
    with bc2:
        obj_b=st.number_input("🎯 Objectif ventes/jour",min_value=1,step=1,value=5)
        tc_b=st.slider("📊 Taux de conversion (%)",0.5,5.0,2.0,0.1)

    res=calc_budget_pub(obj_b,pv_b,tc_b,pa_b)

    slabel("Résultats")
    r1,r2,r3=st.columns(3,gap="small")
    with r1: st.markdown(f'<div class="price-box"><div class="label">💸 Budget/Jour</div><div class="value" style="color:var(--red);">{res["bj"]:.2f}$</div><div class="currency">{res["bj"]*655:,.0f} FCFA</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="price-box"><div class="label">📅 Budget 3 jours</div><div class="value" style="color:#ff9944;">{res["b3"]:.2f}$</div><div class="currency">{res["b3"]*655:,.0f} FCFA</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="price-box"><div class="label">📅 Budget 5 jours</div><div class="value" style="color:#4493f8;">{res["b5"]:.2f}$</div><div class="currency">{res["b5"]*655:,.0f} FCFA</div></div>', unsafe_allow_html=True)

    r4,r5,r6=st.columns(3,gap="small")
    with r4: st.markdown(f'<div class="price-box"><div class="label">🖱️ CPC Estimé</div><div class="value" style="color:#bc8cff;">{res["cpc"]:.3f}$</div></div>', unsafe_allow_html=True)
    with r5: st.markdown(f'<div class="price-box"><div class="label">👥 Clics Nécessaires</div><div class="value">{res["clics"]}</div></div>', unsafe_allow_html=True)
    with r6:
        bc_col="#44dd88" if res["benef"]>0 else "#ff4444"
        st.markdown(f'<div class="price-box" style="border-color:{bc_col}"><div class="label">🏆 Bénéfice Net/Jour</div><div class="value" style="color:{bc_col};">{res["benef"]:,.0f} F</div></div>', unsafe_allow_html=True)

    st.markdown("""<div class="budget-tip" style="margin-top:1rem;">
      <p>💡 <b>Conseil LABO :</b> Démarre avec le minimum 3–5 jours.
      Si ROAS &gt; 2 → double le budget progressivement.
      Si 0 vente après 3 jours → change la créative en premier, jamais le ciblage.</p>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE : COMPARATEUR
# ══════════════════════════════════════════════════════════════════════
elif page == "comparateur":
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h2 style="font-size:1.35rem;font-weight:900;color:#fff;margin:0 0 .3rem;">⚖️ Comparateur de Produits</h2>
      <p style="color:var(--muted);font-size:.8rem;margin:0;">Compare 2 produits · Score LABO · Choisis le gagnant avant d'investir</p>
    </div>""", unsafe_allow_html=True)

    CATS=["Domestique","Beauté & Soins","Santé","Tech","Mode","Alimentation","Luxe","Agriculture","Élevage","Pêche","Autre"]
    cc1,cc2=st.columns(2,gap="large")
    with cc1:
        st.markdown('<p style="color:var(--red);font-weight:800;font-size:.88rem;margin-bottom:.5rem;">🅰️ Produit 1</p>', unsafe_allow_html=True)
        p1n=st.text_input("Nom",key="p1n",placeholder="Ex: Crème Beauty Milk")
        p1a=st.number_input("Prix achat (FCFA)",min_value=0,step=500,key="p1a",value=5000)
        p1v=st.number_input("Prix vente (FCFA)",min_value=0,step=500,key="p1v",value=15000)
        p1t=st.selectbox("Type",["wow","probleme_solution"],key="p1t")
        p1c=st.selectbox("Catégorie",CATS,key="p1c")
    with cc2:
        st.markdown('<p style="color:#4493f8;font-weight:800;font-size:.88rem;margin-bottom:.5rem;">🅱️ Produit 2</p>', unsafe_allow_html=True)
        p2n=st.text_input("Nom",key="p2n",placeholder="Ex: Lampe solaire LED")
        p2a=st.number_input("Prix achat (FCFA)",min_value=0,step=500,key="p2a",value=3000)
        p2v=st.number_input("Prix vente (FCFA)",min_value=0,step=500,key="p2v",value=12000)
        p2t=st.selectbox("Type",["wow","probleme_solution"],key="p2t")
        p2c=st.selectbox("Catégorie",CATS,key="p2c")

    if st.button("⚖️  COMPARER LES 2 PRODUITS",use_container_width=True):
        def mk(tp,cat): return {"score":7,"type_produit":tp,"avatar":{"categorie":cat},"peurs":["a","b","c"],"desirs":["a","b","c"]}
        s1=calc_score_produit(p1a,p1v,mk(p1t,p1c))
        s2=calc_score_produit(p2a,p2v,mk(p2t,p2c))
        win="A" if s1["score_final"]>=s2["score_final"] else "B"

        slabel("⚖️ Résultats")
        rc1,rc2=st.columns(2,gap="large")
        for col,s,nom,ac,vte,side,ca in [(rc1,s1,p1n or "Produit 1",p1a,p1v,"A","#D90429"),(rc2,s2,p2n or "Produit 2",p2a,p2v,"B","#4493f8")]:
            with col:
                is_w=win==side
                border="border-color:rgba(68,221,136,0.4) !important;" if is_w else ""
                st.markdown(f'<div class="result-card" style="{border}">', unsafe_allow_html=True)
                if is_w:
                    st.markdown('<span style="background:rgba(68,221,136,0.12);border:1px solid rgba(68,221,136,0.3);color:#44dd88;border-radius:5px;padding:2px 9px;font-size:.65rem;font-weight:700;display:inline-block;margin-bottom:8px;">🏆 MEILLEUR CHOIX</span>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:{ca};font-weight:900;font-size:1.15rem;margin:0 0 3px;">{nom}</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:var(--muted);font-size:.72rem;margin:0 0 10px;">Achat {ac:,} F · Vente {vte:,} F · Marge {vte-ac-5000:,} F</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#fff;font-size:2.2rem;font-weight:900;margin:0 0 12px;line-height:1;">{s["score_final"]}<span style="font-size:.85rem;color:var(--muted);font-weight:400;"> /10</span></p>', unsafe_allow_html=True)
                for cr in s["criteres"]:
                    n=cr["note"]; c="#44dd88" if n>=8 else "#ff9944" if n>=6 else "#ff4444"
                    pct=int(n/10*100)
                    st.markdown(f"""<div class="comp-bar">
                      <div class="comp-bar-hd">
                        <span class="comp-bar-lbl">{cr['nom']}</span>
                        <span class="comp-bar-val" style="color:{c};">{n}/10</span>
                      </div>
                      <div class="comp-bar-track">
                        <div class="comp-bar-fill" style="width:{pct}%;background:{c};"></div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE : TÉMOIGNAGES
# ══════════════════════════════════════════════════════════════════════
elif page == "temoignages":
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h2 style="font-size:1.35rem;font-weight:900;color:#fff;margin:0 0 .3rem;">💬 Témoignages Clients Africains</h2>
      <p style="color:var(--muted);font-size:.8rem;margin:0;">Générés par l'IA · Style oral africain authentique · Prêts pour Shopify</p>
    </div>""", unsafe_allow_html=True)

    data=st.session_state.get("result")
    if not data:
        st.info("⚠️ Lance d'abord une analyse produit (🔬 Analyser) pour générer les témoignages.")
    else:
        aname=st.session_state.get("active_product","le produit")
        temos=data.get("temoignages",[])
        if not temos:
            st.warning("⚠️ Témoignages non générés. Relance une analyse.")
        else:
            st.markdown(f'<p style="color:var(--muted);font-size:.78rem;margin:0 0 1rem;">5 témoignages pour <b style="color:#fff;">{aname}</b></p>', unsafe_allow_html=True)
            for t in temos:
                prenom=t.get("prenom","Client"); ville=t.get("ville","Afrique")
                duree=t.get("produit_utilise",""); avis=t.get("avis","")
                note=int(t.get("note",5)); init=prenom[0].upper()
                stars="★"*note+"☆"*(5-note)
                st.markdown(f"""<div class="temo-card">
                  <div class="temo-head">
                    <div class="temo-av">{init}</div>
                    <div>
                      <p class="temo-name">{prenom}</p>
                      <p class="temo-ville">📍 {ville} · {duree}</p>
                      <p class="temo-stars">{stars}</p>
                    </div>
                  </div>
                  <p class="temo-body">"{avis}"</p>
                </div>""", unsafe_allow_html=True)
                copy_box(f'"{avis}"\n— {prenom}, {ville} ({duree}) {stars}')

            st.markdown("<hr>", unsafe_allow_html=True)
            slabel("📦 Tous les témoignages")
            copy_box("\n\n---\n\n".join(
                f'"{t.get("avis","")}" — {t.get("prenom","")}, {t.get("ville","")} ({t.get("produit_utilise","")}) {"★"*int(t.get("note",5))}'
                for t in temos
            ))
