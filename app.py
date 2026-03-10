import streamlit as st
import os, io, re, json, base64, urllib.parse, urllib.request
from PIL import Image
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
    except Exception:
        pass
    return []

def write_history_file(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

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
    ("comp_result",    None),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="EcoMaster Labo Pro", page_icon="🚀", layout="wide")

st.markdown("""
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0d1117">
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# CSS MINEA-STYLE — mêmes couleurs, design professionnel
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
  --red:       #D90429;
  --red2:      #ff1744;
  --red-dim:   rgba(217,4,41,0.12);
  --red-glow:  rgba(217,4,41,0.4);
  --bg:        #0d1117;
  --bg2:       #161b22;
  --bg3:       #1c2333;
  --bg4:       #21262d;
  --border:    rgba(255,255,255,0.07);
  --border2:   rgba(255,255,255,0.12);
  --text:      #e6edf3;
  --muted:     #7d8590;
  --muted2:    #484f58;
  --green:     #3fb950;
  --orange:    #f0883e;
  --blue:      #58a6ff;
  --purple:    #bc8cff;
}

html, body, [class*="css"], [data-testid], .stApp,
.appview-container, .appview-container > section,
.block-container, .main {
  font-family: 'Inter', 'Space Grotesk', sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

@media (prefers-color-scheme: light) {
  html, body, div, section, .stApp, .main, .block-container,
  .appview-container, .appview-container > section,
  [class*="css"], [data-testid] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
  }
}

/* ── LAYOUT ── */
.block-container {
  padding-top: 0 !important;
  max-width: 100% !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
}

/* ── SIDEBAR MINEA ── */
section[data-testid="stSidebar"] {
  background: #0d1117 !important;
  border-right: 1px solid rgba(255,255,255,0.06) !important;
  width: 240px !important;
  min-width: 240px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── NAV ITEMS ── */
.nav-brand {
  padding: 1.2rem 1rem 0.8rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  margin-bottom: 0.5rem;
}
.nav-brand h2 {
  font-size: 1rem; font-weight: 800; color: #fff;
  margin: 0; letter-spacing: -0.3px;
}
.nav-brand h2 span { color: var(--red); }
.nav-brand p { color: var(--muted); font-size: 0.65rem; margin: 0.2rem 0 0; }

.nav-section {
  padding: 0.4rem 0.75rem 0.2rem;
  color: var(--muted2);
  font-size: 0.6rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.nav-item {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 0.55rem 1rem; margin: 1px 0.5rem;
  border-radius: 8px; cursor: pointer;
  color: var(--muted); font-size: 0.82rem; font-weight: 500;
  transition: all 0.15s ease; text-decoration: none;
  border: 1px solid transparent;
}
.nav-item:hover {
  background: rgba(255,255,255,0.05);
  color: var(--text);
}
.nav-item.active {
  background: var(--red-dim);
  color: #fff; font-weight: 700;
  border-color: rgba(217,4,41,0.25);
}
.nav-item .icon { font-size: 1rem; min-width: 20px; text-align: center; }

/* ── TOPBAR ── */
.topbar {
  background: var(--bg);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  padding: 0.75rem 1.5rem;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 100;
}
.topbar-title { color: #fff; font-weight: 700; font-size: 1rem; margin: 0; }
.topbar-badge {
  background: var(--red-dim); color: var(--red);
  border: 1px solid rgba(217,4,41,0.3);
  border-radius: 20px; padding: 3px 10px;
  font-size: 0.68rem; font-weight: 700;
}

/* ── STATS CARDS (Minea-style) ── */
.stat-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px; padding: 1.1rem 1.2rem;
  transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover { border-color: var(--border2); transform: translateY(-2px); }
.stat-card .s-label {
  color: var(--muted); font-size: 0.68rem;
  text-transform: uppercase; letter-spacing: 1px; margin: 0 0 0.4rem;
  display: flex; align-items: center; gap: 0.3rem;
}
.stat-card .s-value {
  color: #fff; font-size: 1.5rem; font-weight: 800;
  margin: 0; letter-spacing: -1px;
}
.stat-card .s-sub { color: var(--muted); font-size: 0.7rem; margin: 0.2rem 0 0; }

/* ── SCORE RING ── */
.score-ring-wrap {
  text-align: center; padding: 1.5rem 0;
}
.score-ring {
  width: 120px; height: 120px; border-radius: 50%;
  border: 4px solid var(--red);
  display: inline-flex; align-items: center; justify-content: center;
  flex-direction: column;
  box-shadow: 0 0 40px rgba(217,4,41,0.25), inset 0 0 30px rgba(217,4,41,0.05);
  background: var(--bg2);
}
.score-ring .sr-val {
  font-size: 2.2rem; font-weight: 900; color: #fff;
  line-height: 1; letter-spacing: -2px;
}
.score-ring .sr-max { font-size: 0.7rem; color: var(--muted); }

/* ── BADGES ── */
.badge {
  display: inline-block; border-radius: 6px; padding: 2px 8px;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.3px;
}
.badge-red    { background: rgba(217,4,41,0.15);  color: var(--red);    border: 1px solid rgba(217,4,41,0.3); }
.badge-green  { background: rgba(63,185,80,0.12); color: var(--green);  border: 1px solid rgba(63,185,80,0.3); }
.badge-orange { background: rgba(240,136,62,0.12);color: var(--orange); border: 1px solid rgba(240,136,62,0.3); }
.badge-blue   { background: rgba(88,166,255,0.12);color: var(--blue);   border: 1px solid rgba(88,166,255,0.3); }
.badge-wow    { background: rgba(217,4,41,0.15);  color: #ff6b6b;       border: 1px solid rgba(255,107,107,0.3); }

/* ── CARDS UNIVERSELLES ── */
.labo-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px; padding: 1.2rem;
  margin-bottom: 0.8rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.labo-card:hover { border-color: var(--border2); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.labo-card .lc-label {
  color: var(--muted); font-size: 0.65rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 1px; margin: 0 0 0.5rem;
}
.labo-card .lc-title { color: #fff; font-weight: 700; font-size: 0.95rem; margin: 0 0 0.4rem; }
.labo-card .lc-text  { color: var(--muted); font-size: 0.83rem; line-height: 1.7; margin: 0; }

/* ── CRITERES SCORE ── */
.critere-row {
  display: flex; align-items: center; gap: 0.8rem;
  padding: 0.55rem 0; border-bottom: 1px solid rgba(255,255,255,0.04);
}
.critere-note {
  min-width: 36px; text-align: center;
  font-weight: 800; font-size: 0.9rem; border-radius: 6px; padding: 2px 6px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg2); border-radius: 10px; padding: 4px;
  gap: 2px; border: 1px solid var(--border);
  flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--muted) !important;
  border-radius: 8px !important; font-weight: 600 !important;
  font-size: clamp(0.65rem, 1.8vw, 0.8rem) !important;
  padding: 0.4rem 0.65rem !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--red) !important;
  color: #fff !important;
  box-shadow: 0 2px 12px rgba(217,4,41,0.4) !important;
}
.stTabs [data-baseweb="tab"]:focus-visible { outline: none !important; }

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input, .stSelectbox select,
.stTextArea textarea {
  background-color: var(--bg3) !important; color: var(--text) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important; font-size: 0.88rem !important;
  transition: border-color 0.2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
  border-color: var(--red) !important;
  box-shadow: 0 0 0 3px rgba(217,4,41,0.12) !important;
}

/* ── BOUTON PRINCIPAL ── */
.stButton > button {
  background: linear-gradient(135deg, #D90429, #ff1744, #D90429) !important;
  background-size: 200% auto !important;
  color: #fff !important; border: none !important;
  border-radius: 10px !important; font-weight: 700 !important;
  font-size: 0.88rem !important; letter-spacing: 0.5px !important;
  padding: 0.7rem 1.5rem !important;
  transition: all 0.3s !important;
  box-shadow: 0 4px 15px rgba(217,4,41,0.3) !important;
}
.stButton > button:hover {
  background-position: right center !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(217,4,41,0.5) !important;
}

/* Boutons sidebar discrets */
section[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  color: var(--muted) !important;
  border: 1px solid var(--border2) !important;
  font-weight: 500 !important; font-size: 0.75rem !important;
  padding: 0.35rem 0.7rem !important;
  box-shadow: none !important; letter-spacing: 0 !important;
  animation: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  border-color: var(--red) !important; color: #fff !important;
  background: rgba(217,4,41,0.08) !important;
  transform: none !important; box-shadow: none !important;
}

/* ── ADS & SCRIPTS ── */
.ad-card {
  background: var(--bg3); border: 1px solid var(--border);
  border-left: 3px solid var(--red);
  border-radius: 0 10px 10px 0; padding: 1rem 1.2rem;
  margin-bottom: 0.8rem; transition: border-color 0.2s;
}
.ad-card:hover { border-left-color: var(--red2); background: var(--bg4); }
.ad-accroche { color: var(--orange); font-weight: 800; font-size: 0.95rem; margin: 0 0 0.5rem; }
.ad-texte    { color: #ccc; font-size: 0.86rem; line-height: 1.9; white-space: pre-wrap; margin: 0; }

.script-card {
  background: var(--bg3); border: 1px solid var(--border);
  border-top: 2px solid var(--red);
  border-radius: 0 0 10px 10px; padding: 1.2rem;
  margin-bottom: 1rem;
}
.script-label { color: var(--red); font-size: 0.65rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px; margin: 0 0 0.5rem; }
.script-text  { color: #ccc; font-size: 0.88rem; line-height: 2; white-space: pre-wrap; margin: 0; }

/* ── SHOPIFY PARA ── */
.para-bloc {
  border-left: 3px solid var(--red); background: var(--bg3);
  border-radius: 0 10px 10px 0; padding: 1rem 1.2rem;
  margin-bottom: 0.7rem; transition: background 0.2s;
}
.para-bloc:hover { background: var(--bg4); }
.para-titre { color: var(--red); font-weight: 800; font-size: 0.92rem; margin: 0 0 0.4rem; }
.para-texte { color: #bbb; font-size: 0.86rem; line-height: 1.85; white-space: pre-wrap; margin: 0; }

/* ── OFFRES ── */
.offre-bloc {
  background: linear-gradient(135deg, rgba(5,15,0,0.8), rgba(10,24,0,0.7));
  border: 1px solid rgba(63,185,80,0.2); border-radius: 10px;
  padding: 1.1rem; margin-bottom: 0.7rem; transition: border-color 0.2s;
}
.offre-bloc:hover { border-color: rgba(63,185,80,0.4); }
.offre-nom  { color: #3fb950; font-weight: 800; font-size: 0.92rem; margin: 0 0 0.3rem; }
.offre-desc { color: #aaa; font-size: 0.83rem; line-height: 1.7; margin: 0 0 0.4rem; }
.offre-prix { color: #56d364; font-size: 0.78rem; font-weight: 700; margin: 0; }

/* ── PLAN 7J ── */
.jour-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem 1.1rem; margin-bottom: 0.7rem;
  transition: border-color 0.2s;
}
.jour-card:hover { border-color: var(--border2); }
.jour-num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--red-dim); border: 1px solid rgba(217,4,41,0.3);
  color: var(--red); font-weight: 800; font-size: 0.82rem;
  margin-bottom: 0.6rem;
}
.jour-titre { color: #fff; font-weight: 700; font-size: 0.88rem; margin: 0 0 0.5rem; }
.jour-row   { display: flex; gap: 0.5rem; margin-bottom: 0.3rem; flex-wrap: wrap; }
.jour-label { color: var(--muted); font-size: 0.68rem; min-width: 60px; }
.jour-val   { color: var(--text); font-size: 0.8rem; flex: 1; }

/* ── TEMOIGNAGES ── */
.temoignage-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.1rem; margin-bottom: 0.7rem;
  transition: border-color 0.2s;
}
.temoignage-card:hover { border-color: var(--border2); }
.temo-header { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 0.6rem; }
.temo-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--red), #ff6b35);
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 1rem; color: #fff; flex-shrink: 0;
}
.temo-name  { color: #fff; font-weight: 700; font-size: 0.88rem; margin: 0; }
.temo-ville { color: var(--muted); font-size: 0.72rem; margin: 0; }
.temo-stars { color: #f0883e; font-size: 0.75rem; margin: 0; }
.temo-text  { color: #bbb; font-size: 0.84rem; line-height: 1.75; font-style: italic; margin: 0; }

/* ── IMAGES GRID ── */
.img-result-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
  margin-bottom: 0.8rem;
}
.img-result-card:hover { border-color: var(--border2); transform: translateY(-2px); }
.img-result-card img { width: 100%; height: 160px; object-fit: cover; display: block; }
.img-footer { padding: 0.5rem 0.7rem; }
.img-footer p { color: var(--muted); font-size: 0.68rem; margin: 0 0 0.4rem; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap; }

/* ── SPY PAYS ── */
.pays-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 1rem; text-align: center;
  cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem;
}
.pays-card:hover { border-color: var(--red); background: var(--red-dim); }
.pays-flag { font-size: 2rem; margin-bottom: 0.3rem; }
.pays-nom  { color: #fff; font-weight: 700; font-size: 0.82rem; margin: 0; }

/* ── BUDGET CALC ── */
.budget-result {
  background: linear-gradient(135deg, rgba(14,0,0,0.9), rgba(26,0,0,0.9));
  border: 1px solid rgba(217,4,41,0.3); border-radius: 12px;
  padding: 1.3rem; margin-top: 1rem; text-align: center;
}
.budget-val { font-size: 2rem; font-weight: 900; color: var(--red); margin: 0; }
.budget-sub { color: var(--muted); font-size: 0.78rem; margin: 0.2rem 0 0; }

/* ── ST.CODE ── */
.stCodeBlock, pre, code,
[data-testid="stCode"] > div,
[data-testid="stCode"] pre {
  background-color: #0a0e15 !important;
  color: #e0e0e0 !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  border-radius: 8px !important;
  font-size: 0.83rem !important;
}
[data-testid="stCode"] button,
[data-testid="stCode"] button:hover {
  background: var(--red) !important; color: white !important;
  border-radius: 5px !important; opacity: 1 !important;
}

/* ── GOLDEN RULE ── */
.golden-rule {
  background: rgba(240,136,62,0.05);
  border: 1px solid rgba(240,136,62,0.2);
  border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0;
}
.golden-rule p { color: #f0883e; font-size: 0.75rem; margin: 0; line-height: 1.8; }

/* ── SECTION LABEL ── */
.slabel {
  color: var(--muted); font-size: 0.65rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px;
  display: flex; align-items: center; gap: 8px;
  margin: 1.2rem 0 0.6rem;
}
.slabel::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, rgba(255,255,255,0.1), transparent);
}

/* ── DOWNLOAD BTN ── */
.dl-btn {
  display: block; text-align: center;
  background: var(--red); color: #fff !important;
  border: none; border-radius: 8px; padding: 8px 0;
  font-weight: 700; font-size: 0.78rem; cursor: pointer;
  text-decoration: none; transition: background 0.2s;
  width: 100%;
}
.dl-btn:hover { background: var(--red2); }

/* ── GAINS TABLE ── */
.gtable { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
.gtable th {
  background: var(--bg3); color: var(--muted);
  padding: 8px 10px; font-size: 0.65rem;
  text-transform: uppercase; letter-spacing: 1px;
  border-bottom: 1px solid var(--border);
}
.gtable td { color: #ccc; padding: 9px 10px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.03); }
.gtable tr:hover td { background: var(--bg3); color: #fff; }
.gtable .pos { color: var(--green); font-weight: 700; }
.gtable .neg { color: #f85149; font-weight: 700; }
.gtable .hl  { border-left: 2px solid var(--red); }

/* ── MISC ── */
#MainMenu, footer, header { visibility: hidden; }
label { color: var(--muted) !important; font-weight: 500 !important; font-size: 0.8rem !important; }
.stAlert { border-radius: 8px !important; }
hr { border-color: var(--border) !important; }

@media (max-width: 768px) {
  .block-container { padding: 0 !important; }
  .stat-card .s-value { font-size: 1.2rem; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ══════════════════════════════════════════════════════════════════════
def slabel(t):
    st.markdown(f'<div class="slabel">{t}</div>', unsafe_allow_html=True)

def labo_card(label, title, text, extra=""):
    st.markdown(f"""<div class="labo-card">
      <div class="lc-label">{label}</div>
      <div class="lc-title">{title}</div>
      <div class="lc-text">{text}</div>
      {extra}
    </div>""", unsafe_allow_html=True)

def get_pub_budget(v):
    if v <= 10:   return "5$–7$/j"
    elif v <= 20: return "7$–10$/j"
    else:          return "15$–20$/j"

def calc_rentabilite(ventes, prix_moyen, prix_achat):
    ca           = ventes * prix_moyen
    cout_produit = ventes * prix_achat
    frais_fixes  = ventes * 5000
    cout_global  = cout_produit + frais_fixes
    benef_net    = ca - cout_global
    return ca, cout_produit, frais_fixes, cout_global, benef_net

def calc_score_produit(prix_achat, prix_vente_moy, data):
    score_ia = int(data.get("score", 5))
    type_p   = data.get("type_produit", "wow")
    categ    = data.get("avatar", {}).get("categorie", "Autre")
    nb_peurs = len(data.get("peurs",  []))
    nb_des   = len(data.get("desirs", []))

    if prix_vente_moy <= 7000:    c1 = 10
    elif prix_vente_moy <= 10000: c1 = 9
    elif prix_vente_moy <= 15000: c1 = 7
    elif prix_vente_moy <= 22000: c1 = 5
    elif prix_vente_moy <= 35000: c1 = 3
    else:                         c1 = 1
    desc1 = f"Prix {prix_vente_moy:,.0f} FCFA — {'✅ Achat impulsif' if c1>=9 else '⚠️ Réfléchi' if c1>=6 else '🔴 Trop cher'}"

    if type_p == "wow":
        c2 = 9; desc2 = "Produit WOW — bénéfice visible en 1 seconde"
    else:
        douleurs = ["douleur","fatigue","insomnie","sécurité","argent","poids","peau","cheveux","digestion"]
        txt = " ".join(data.get("peurs",[]) + data.get("desirs",[])).lower()
        sd  = sum(1 for d in douleurs if d in txt)
        c2  = 9 if sd>=3 else 7 if sd>=2 else 5 if sd>=1 else 3
        desc2 = f"Problème-solution · {sd} douleurs quotidiennes"

    categ_f = {"Domestique":9,"Beauté & Soins":9,"Santé":8,"Tech":8,"Mode":7,"Alimentation":7}
    categ_d = {"Agriculture":5,"Élevage":4,"Pêche":4,"Luxe":6}
    c3 = min(10, categ_f.get(categ, categ_d.get(categ, 6)) + (1 if type_p=="wow" else 0))
    desc3 = f"Catégorie {categ} — {'✅ Facile à filmer' if c3>=8 else '⚠️ Moyen' if c3>=6 else '🔴 Difficile'}"

    cats = {"Tech":8,"Santé":7,"Beauté & Soins":7,"Luxe":6,"Mode":4,"Alimentation":3}
    c4 = cats.get(categ, 6)
    if score_ia>=8: c4 = min(10, c4+1)
    if score_ia<=4: c4 = max(1, c4-2)
    desc4 = f"{'✅ Rare localement' if c4>=7 else '⚠️ Moyennement disponible' if c4>=5 else '🔴 Partout en marché'}"

    c5 = 9 if score_ia>=8 and nb_des>=3 else 7 if score_ia>=7 else 5 if score_ia>=5 else 3 if score_ia>=3 else 2
    desc5 = f"IA {score_ia}/10 · {nb_des} désirs · {'✅ Crédible' if c5>=7 else '⚠️ Mitigé' if c5>=5 else '🔴 Douteux'}"

    score_brut = c1*.30 + c2*.25 + c3*.20 + c4*.15 + c5*.10
    echecs     = sum(1 for c in [c1,c2,c3,c4,c5] if c<=4)
    alerte     = None
    if echecs >= 2:
        score_brut = min(score_brut, 6.0)
        alerte = f"⚠️ {echecs} critères faibles — score plafonné à 6/10"

    return {
        "score_final":    round(max(1.0, min(10.0, score_brut)), 1),
        "alerte_rigueur": alerte,
        "criteres": [
            {"nom":"💰 Attractivité du Prix",     "note":c1,"desc":desc1,"poids":"30%"},
            {"nom":"⚡ Utilité Immédiate & WOW",  "note":c2,"desc":desc2,"poids":"25%"},
            {"nom":"🎬 Potentiel Créatives",       "note":c3,"desc":desc3,"poids":"20%"},
            {"nom":"💎 Rareté & Exclusivité",      "note":c4,"desc":desc4,"poids":"15%"},
            {"nom":"🛡️ Crédibilité",              "note":c5,"desc":desc5,"poids":"10%"},
        ]
    }

def calc_budget_pub(objectif_ventes, prix_vente, taux_conv_pct=2.0):
    """
    Calcul basé sur benchmarks réels Facebook Afrique :
    CPM moyen : 0.80$ | CTR moyen : 1.8% | Taux conv : 1-3%
    """
    cpm       = 0.80    # $ pour 1000 impressions
    ctr       = 0.018   # taux de clic moyen
    taux_conv = taux_conv_pct / 100

    # Nombre de clics nécessaires pour objectif_ventes
    clics_necessaires = objectif_ventes / taux_conv if taux_conv > 0 else 9999
    # CPC = CPM / (CTR * 1000)
    cpc = cpm / (ctr * 1000)
    budget_jour = clics_necessaires * cpc

    # Période test recommandée : 3-5 jours
    budget_test_3j = budget_jour * 3
    budget_test_5j = budget_jour * 5

    roas_min = (objectif_ventes * prix_vente * 0.4) / max(budget_jour, 0.01)

    return {
        "budget_jour":    round(budget_jour, 2),
        "budget_3j":      round(budget_test_3j, 2),
        "budget_5j":      round(budget_test_5j, 2),
        "cpc_estime":     round(cpc, 3),
        "clics_besoin":   round(clics_necessaires),
        "roas_min":       round(roas_min, 1),
    }

# ══════════════════════════════════════════════════════════════════════
# RECHERCHE IMAGES BING (sans API key)
# ══════════════════════════════════════════════════════════════════════
def search_bing_images(query: str, max_results: int = 10) -> list:
    """
    Recherche d'images via Bing Image Search.
    Parse les URLs d'images depuis la réponse HTML.
    """
    results = []
    try:
        q_enc = urllib.parse.quote_plus(query)
        url   = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1&tsc=ImageBasicHover"
        req   = urllib.request.Request(url, headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        })
        html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8", errors="ignore")

        # Extraire les URLs d'images depuis les attributs murl (media url)
        murls = re.findall(r'"murl"\s*:\s*"(https?://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"', html)
        thurls = re.findall(r'"turl"\s*:\s*"(https?://[^"]+)"', html)

        for i, murl in enumerate(murls[:max_results]):
            thumb = thurls[i] if i < len(thurls) else murl
            results.append({
                "url":   murl,
                "thumb": thumb,
                "title": f"{query} #{i+1}",
            })
    except Exception as e:
        pass
    return results

# ══════════════════════════════════════════════════════════════════════
# API GROQ + JSON REPAIR
# ══════════════════════════════════════════════════════════════════════
def repair_json(raw: str) -> dict:
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    stack = []; last_valid_pos = 0; in_string = False; escape_next = False
    for idx, ch in enumerate(raw):
        if escape_next: escape_next = False; continue
        if ch == '\\' and in_string: escape_next = True; continue
        if ch == '"' and not escape_next: in_string = not in_string; continue
        if in_string: continue
        if ch in ('{','['): stack.append(ch)
        elif ch in ('}',']'):
            if stack: stack.pop(); last_valid_pos = idx + 1
    closing = "".join('}' if b=='{' else ']' for b in reversed(stack))
    try:
        return json.loads(raw[:last_valid_pos] + closing)
    except:
        pass
    partial = {}
    for key in ["score","score_justification","type_produit","ameliorations",
                "public_cible","peurs","desirs","mots_cles","offres",
                "shopify","facebook_ads","scripts","angles_marketing","avatar",
                "creatives","images_produit","plan_7j","temoignages"]:
        m = re.search(rf'"{key}"\s*:\s*', raw)
        if m:
            start = m.end(); ch0 = raw[start:start+1]
            if ch0 in ('"','{','['):
                depth=0; in_s=False
                for j, c in enumerate(raw[start:], start):
                    if c=='"' and raw[j-1:j]!='\\': in_s = not in_s
                    if not in_s:
                        if c in ('{','['): depth+=1
                        elif c in ('}',']'): depth-=1
                        if depth==0:
                            try: partial[key]=json.loads(raw[start:j+1])
                            except: pass
                            break
    return partial if partial else {}

def call_groq(prompt: str, images: list) -> dict:
    from groq import Groq
    client  = Groq(api_key=st.secrets["GROQ_API_KEY"])
    content = []
    for img_data in images:
        b64 = base64.b64encode(img_data).decode("utf-8")
        content.append({"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}})
    content.append({"type":"text","text":prompt})
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role":"user","content":content}],
        max_tokens=8000, temperature=0.7,
    )
    return repair_json(response.choices[0].message.content.strip())

def test_groq():
    try:
        from groq import Groq
        key = st.secrets.get("GROQ_API_KEY","")
        if not key: return {"ok":False,"msg":"GROQ_API_KEY absent des Secrets"}
        client = Groq(api_key=key)
        r = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role":"user","content":"Réponds juste OK"}],
            max_tokens=5,
        )
        return {"ok":True,"msg":f"✅ Groq OK — {r.choices[0].message.content.strip()}"}
    except Exception as e:
        return {"ok":False,"msg":str(e)}

# ══════════════════════════════════════════════════════════════════════
# PROMPT IA (avec plan_7j et temoignages)
# ══════════════════════════════════════════════════════════════════════
def build_prompt(name, pa, pmin, pmax):
    return f"""Tu es un expert en neuro-marketing et e-commerce pour l'Afrique Francophone.
Adapte TOUT au contexte africain : Facebook, WhatsApp, statut social, utilité immédiate.

PRODUIT : {name}
PRIX ACHAT : {pa:,} FCFA | PRIX DE VENTE : {pmin:,}–{pmax:,} FCFA

━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ABSOLUES :
━━━━━━━━━━━━━━━━━━━━━━━━━━━

① SHOPIFY : 3 titres magnétiques + 6 paragraphes.
   TITRE DE PARAGRAPHE = BÉNÉFICE CLIENT DIRECT.
   ❌ INTERDIT : "Découvrez...", "Pourquoi choisir...", "Les avantages de..."
   ✅ OBLIGATOIRE : "Peau éclatante en 2 semaines", "Douleurs soulagées dès le 1er jour"
   Chaque para = titre bénéfice + 3-4 phrases courtes.

② FACEBOOK ADS : 3 variantes. Emojis. Ton fun et émotionnel. \\n entre chaque ligne. 5 lignes max.

③ SCRIPTS VOIX-OFF : 3 scripts de 130 à 170 MOTS CHACUN. \\n entre phrases courtes. Noms africains.

④ AVATAR : Persona ultra-détaillé. Prénom africain. Ville africaine. Frustrations, désirs, objections.

⑤ CRÉATIVES : 4 concepts Facebook/TikTok avec scène, message, type d'accroche.

⑥ PLAN 7 JOURS : Actions concrètes jour par jour pour lancer et scaler. Budget pub réaliste.

⑦ TÉMOIGNAGES : 5 avis clients africains authentiques. Style oral africain. Prénoms et villes africaines.

Réponds UNIQUEMENT avec du JSON valide. Aucun texte avant ni après.

{{
  "score": 7,
  "score_justification": "Analyse détaillée 2-3 phrases",
  "type_produit": "wow",
  "ameliorations": ["conseil 1", "conseil 2", "conseil 3"],
  "public_cible": "Description précise africaine",
  "peurs": ["peur 1", "peur 2", "peur 3"],
  "desirs": ["désir 1", "désir 2", "désir 3"],
  "mots_cles": ["mot1","mot2","mot3","mot4","mot5"],
  "offres": [
    {{"nom":"Nom offre","description":"Contenu","prix_suggere":"XXXX FCFA","argument":"Argument africain"}},
    {{"nom":"Offre 2","description":"Contenu","prix_suggere":"XXXX FCFA","argument":"Argument"}},
    {{"nom":"Offre 3","description":"Contenu","prix_suggere":"XXXX FCFA","argument":"Argument"}}
  ],
  "facebook_ads": [
    {{"angle":"Émotionnel","accroche":"🔥 TITRE CHOC","texte":"ligne1\\nligne2\\nligne3\\nligne4\\nligne5"}},
    {{"angle":"Preuve Sociale","accroche":"⭐ TITRE TÉMOIGNAGE","texte":"ligne1\\nligne2\\nligne3\\nligne4\\nligne5"}},
    {{"angle":"Urgence","accroche":"⚠️ STOCK LIMITÉ","texte":"ligne1\\nligne2\\nligne3\\nligne4\\nligne5"}}
  ],
  "shopify": {{
    "titres": [
      {{"angle":"Bénéfice","titre":"Titre 1 magnétique"}},
      {{"angle":"Curiosité","titre":"Titre 2 intriguant"}},
      {{"angle":"Urgence","titre":"Titre 3 urgent"}}
    ],
    "paragraphes": [
      {{"titre":"Titre bénéfice §1","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §2","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §3","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §4","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §5","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §6","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}}
    ]
  }},
  "scripts": [
    {{"angle":"Émotionnel","texte_complet":"130 à 170 mots. Fluide. Noms africains. \\n entre phrases."}},
    {{"angle":"Bénéfice Direct","texte_complet":"130 à 170 mots. Preuve sociale africaine."}},
    {{"angle":"Urgence & Statut","texte_complet":"130 à 170 mots. Statut social et urgence."}}
  ],
  "angles_marketing": [
    {{"angle":"Peur & Urgence","titre":"Titre court","accroche":"Phrase d'attaque directe africaine"}},
    {{"angle":"Désir & Aspiration","titre":"Titre court","accroche":"Phrase qui fait rêver"}},
    {{"angle":"Preuve Sociale","titre":"Titre court","accroche":"Témoignage ou chiffre africain"}},
    {{"angle":"Curiosité","titre":"Titre court","accroche":"Question intrigante"}},
    {{"angle":"Transformation","titre":"Titre court","accroche":"Avant/après concret"}}
  ],
  "avatar": {{
    "sexe":"homme / femme / les deux",
    "age":"25–40 ans",
    "francais":"familier",
    "categorie":"Domestique",
    "prenom_type":"Kofi, Amina ou prénom africain",
    "ville":"Lomé, Abidjan ou similaire",
    "profession":"Profession africaine précise",
    "revenu":"80 000–120 000 FCFA/mois",
    "mode_vie":"Quotidien africain en 2 phrases",
    "frustrations":["frustration 1","frustration 2","frustration 3"],
    "desirs":["désir 1","désir 2","désir 3"],
    "objections":["objection 1","objection 2","objection 3"],
    "message_cle":"Phrase exacte qui convainc immédiatement"
  }},
  "creatives": [
    {{"concept":"Concept 1","scene":"Scène précise","message":"Message principal","accroche_type":"WOW"}},
    {{"concept":"Concept 2","scene":"Scène 2","message":"Message 2","accroche_type":"Problème"}},
    {{"concept":"Concept 3","scene":"Scène 3","message":"Message 3","accroche_type":"Témoignage"}},
    {{"concept":"Concept 4","scene":"Scène 4","message":"Message 4","accroche_type":"Statistique"}}
  ],
  "images_produit": [
    {{"type":"Démonstration","description":"Visuel démonstration précis"}},
    {{"type":"Utilisation","description":"Personne utilisant le produit, contexte africain"}},
    {{"type":"Lifestyle","description":"Lifestyle africain réel"}},
    {{"type":"Avantage Clé","description":"Avantage principal mis en avant"}},
    {{"type":"Gros Plan","description":"Détails et finition du produit"}}
  ],
  "plan_7j": [
    {{"jour":1,"titre":"Mise en place","action":"Action précise","budget":"5$","ciblage":"Ciblage Facebook précis","contenu":"Ce qu'il faut publier exactement"}},
    {{"jour":2,"titre":"Premier test","action":"Action","budget":"5$","ciblage":"Ciblage","contenu":"Contenu"}},
    {{"jour":3,"titre":"Analyse","action":"Action","budget":"7$","ciblage":"Ciblage","contenu":"Contenu"}},
    {{"jour":4,"titre":"Optimisation","action":"Action","budget":"7$","ciblage":"Ciblage optimisé","contenu":"Contenu"}},
    {{"jour":5,"titre":"Scale","action":"Action","budget":"10$","ciblage":"Ciblage winner","contenu":"Contenu"}},
    {{"jour":6,"titre":"Consolidation","action":"Action","budget":"10$","ciblage":"Ciblage","contenu":"Contenu"}},
    {{"jour":7,"titre":"Bilan & Décision","action":"Analyser et décider scale ou stop","budget":"Budget bilan","ciblage":"Retargeting","contenu":"Contenu bilan"}}
  ],
  "temoignages": [
    {{"prenom":"Amina","ville":"Lomé","produit_utilise":"2 semaines","avis":"Témoignage naturel africain 2-3 phrases","note":5}},
    {{"prenom":"Kofi","ville":"Abidjan","produit_utilise":"1 mois","avis":"Témoignage 2","note":5}},
    {{"prenom":"Fatou","ville":"Dakar","produit_utilise":"3 semaines","avis":"Témoignage 3","note":5}},
    {{"prenom":"Moussa","ville":"Cotonou","produit_utilise":"2 mois","avis":"Témoignage 4","note":4}},
    {{"prenom":"Awa","ville":"Conakry","produit_utilise":"1 semaine","avis":"Témoignage 5","note":5}}
  ]
}}"""

def build_export(name, pa, pmin, pmax, data):
    sep   = "=" * 55
    lines = [sep, "  ECOMASTER LABO PRO — PACK MARKETING",
             f"  Produit : {name}",
             f"  Prix achat : {pa:,} FCFA | Vente : {pmin:,}–{pmax:,} FCFA",
             f"  Score LABO : {data.get('score','?')}/10 | Type : {data.get('type_produit','').upper()}",
             sep, "",
             "📊 STRATÉGIE", "-"*40,
             data.get("score_justification",""),
             "\nPublic cible :", data.get("public_cible",""),
             "\nPeurs :"] + [f"  - {p}" for p in data.get("peurs",[])] + \
            ["\nDésirs :"] + [f"  - {d}" for d in data.get("desirs",[])] + \
            ["", "🎁 OFFRES", "-"*40]
    for i,o in enumerate(data.get("offres",[])):
        lines += [f"Offre {i+1} — {o.get('nom','')}",
                  f"  {o.get('description','')} | Prix : {o.get('prix_suggere','')}",""]
    lines += ["", "🛍️ SHOPIFY", "-"*40, "TITRES :"]
    for t in data.get("shopify",{}).get("titres",[]):
        lines.append(f"  [{t.get('angle','')}] {t.get('titre','')}")
    lines.append("\nFICHE PRODUIT :")
    for p in data.get("shopify",{}).get("paragraphes",[]):
        lines += [f"\n{p.get('titre','')}", p.get("texte","")]
    lines += ["","📣 FACEBOOK ADS", "-"*40]
    for i,ad in enumerate(data.get("facebook_ads",[])):
        lines += [f"--- Ad {i+1} [{ad.get('angle','')}] ---",
                  f"TITRE : {ad.get('accroche','')}", ad.get("texte",""), ""]
    lines += ["","🎙️ SCRIPTS VOIX-OFF", "-"*40]
    for i,s in enumerate(data.get("scripts",[])):
        lines += [f"--- {s.get('angle','')} ---", s.get("texte_complet",""), ""]
    lines += ["", sep, "  EcoMaster Labo Pro — by LABO", sep]
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION MINEA-STYLE
# ══════════════════════════════════════════════════════════════════════
PAGES = [
    ("analyse",     "🔬", "Analyser un produit"),
    ("images",      "🖼️", "Images Produit"),
    ("spy",         "🕵️", "Spy Concurrents"),
    ("budget",      "💰", "Budget Pub IA"),
    ("comparateur", "⚖️", "Comparateur"),
    ("temoignages", "💬", "Témoignages"),
]

with st.sidebar:
    st.markdown("""<div class="nav-brand">
      <h2>🚀 Eco<span>Master</span> Labo</h2>
      <p>by LABO · E-commerce Afrique</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)

    for page_id, icon, label in PAGES:
        is_active = st.session_state["nav_page"] == page_id
        cls = "nav-item active" if is_active else "nav-item"
        if st.button(f"{icon}  {label}", key=f"nav_{page_id}",
                     use_container_width=True):
            st.session_state["nav_page"] = page_id
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="nav-section">Historique</div>', unsafe_allow_html=True)

    history = st.session_state["history"]
    if not history:
        st.markdown('<p style="color:#484f58;font-size:0.75rem;padding:0 1rem;">Aucune analyse</p>',
                    unsafe_allow_html=True)
    else:
        if st.button("🗑️ Effacer", key="clear_hist"):
            st.session_state["history"] = []
            write_history_file([])

        for i, h in enumerate(history[:8]):
            short = h["name"][:16] + ("…" if len(h["name"])>16 else "")
            if st.button(f"↩ {short} · {h.get('score','?')}/10", key=f"hist_{i}"):
                st.session_state.update({
                    "result": h["data"], "analyzed": True,
                    "active_product": h["name"],
                    "active_price": h["prix_achat"],
                    "nav_page": "analyse",
                })
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""<div class="golden-rule">
      <p>💡 <b style="color:#f0883e;">Règle d'or LABO</b><br>
      Budget test : <b>4$–7$/jour</b><br>
      Prix = achat + <b>8K–12K FCFA</b><br>
      <span style="color:#484f58;">Frais fixes : 5 000 F/vente</span></p>
    </div>""", unsafe_allow_html=True)

    with st.expander("🔌 Tester Groq"):
        if st.button("Tester la clé", key="test_groq"):
            r = test_groq()
            st.success(r["msg"]) if r["ok"] else st.error(r["msg"])

# ══════════════════════════════════════════════════════════════════════
# CONTENU PRINCIPAL — selon nav_page
# ══════════════════════════════════════════════════════════════════════
page = st.session_state["nav_page"]

# ── PADDING MAIN ──
st.markdown('<div style="padding:1.2rem 1.5rem 2rem;">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 1 : ANALYSE
# ════════════════════════════════════════════════════════════
if page == "analyse":

    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h1 style="font-size:1.5rem;font-weight:800;color:#fff;margin:0 0 0.3rem;">
        🔬 Analyser un produit
      </h1>
      <p style="color:#7d8590;font-size:0.82rem;margin:0;">
        Analyse IA complète — Score, Stratégie, Offres, Scripts, Facebook Ads, Shopify, Plan 7 jours
      </p>
    </div>""", unsafe_allow_html=True)

    # ── FORMULAIRE ──
    col_form, col_upload = st.columns([3, 2], gap="large")

    with col_form:
        product_name = st.text_input("📦 Nom du Produit",
            value=st.session_state.get("active_product",""),
            placeholder="Ex: Crème Beauty Milk, Lampe solaire...")
        purchase_price = st.number_input("💰 Prix d'Achat (FCFA)",
            min_value=0, step=500, value=int(st.session_state.get("active_price",5000)))
        objectif_ventes = st.number_input("🎯 Objectif ventes/jour",
            min_value=1, step=1, value=int(st.session_state.get("active_ventes",10)))

    with col_upload:
        uploaded_files = st.file_uploader("📸 Photos produit (1–3)",
            type=["jpg","jpeg","png","webp"], accept_multiple_files=True)
        if uploaded_files:
            cols_t = st.columns(3)
            for i, f in enumerate(uploaded_files[:3]):
                with cols_t[i]: st.image(f, width=85)

    price_min  = purchase_price + 8000
    price_max  = purchase_price + 12000
    prix_moyen = (price_min + price_max) / 2

    # ── STATS RAPIDES ──
    st.markdown("<br>", unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4, gap="small")
    with sc1:
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">💵 Prix Min</p>
          <p class="s-value">{price_min:,}<span style="font-size:.9rem;color:var(--muted)"> F</span></p>
          <p class="s-sub">Prix conseillé minimum</p>
        </div>""", unsafe_allow_html=True)
    with sc2:
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">💵 Prix Max</p>
          <p class="s-value">{price_max:,}<span style="font-size:.9rem;color:var(--muted)"> F</span></p>
          <p class="s-sub">Prix conseillé maximum</p>
        </div>""", unsafe_allow_html=True)
    with sc3:
        marge = price_min - purchase_price - 5000
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">📈 Marge Nette Min</p>
          <p class="s-value" style="color:{'var(--green)' if marge>0 else '#f85149'};">
            {marge:,}<span style="font-size:.9rem;color:var(--muted)"> F</span></p>
          <p class="s-sub">Après frais fixes 5 000 F</p>
        </div>""", unsafe_allow_html=True)
    with sc4:
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">📣 Budget Pub</p>
          <p class="s-value" style="color:var(--orange);font-size:1.2rem;">{get_pub_budget(objectif_ventes)}</p>
          <p class="s-sub">Pour {objectif_ventes} ventes/jour</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

    # ── LANCEMENT ──
    if analyze_clicked:
        if not product_name.strip():
            st.error("⚠️ Entre le nom du produit.")
        elif not uploaded_files:
            st.error("⚠️ Upload au moins une photo.")
        else:
            images_bytes = [f.read() for f in uploaded_files[:3]]
            with st.spinner("🧠 Groq analyse ton produit… 15–25 secondes ⏳"):
                try:
                    data = call_groq(build_prompt(product_name, purchase_price, price_min, price_max), images_bytes)
                    st.session_state.update({
                        "result":         data,
                        "analyzed":       True,
                        "active_product": product_name,
                        "active_price":   purchase_price,
                        "active_ventes":  objectif_ventes,
                    })
                    save_to_history(product_name, data.get("score","?"), data, purchase_price)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur Groq : {e}")
                    if "GROQ_API_KEY" in str(e) or "api_key" in str(e).lower():
                        st.info("🔑 console.groq.com → API Keys → Create Key → colle dans Streamlit Secrets : `GROQ_API_KEY = \"gsk_...\"`")

    # ── RÉSULTATS ──
    if st.session_state.get("analyzed") and st.session_state.get("result"):
        data         = st.session_state["result"]
        type_produit = data.get("type_produit","wow")
        aname        = st.session_state.get("active_product", product_name)
        aprice       = st.session_state.get("active_price", purchase_price)
        apmin        = aprice + 8000
        apmax        = aprice + 12000
        apmoy        = (apmin + apmax) / 2
        aventes      = st.session_state.get("active_ventes", objectif_ventes)

        # Bandeau produit en cours
        score_data  = calc_score_produit(aprice, apmoy, data)
        score_final = score_data["score_final"]
        badge_type  = "⚡ PRODUIT WOW" if type_produit=="wow" else "🎯 PROBLÈME-SOLUTION"
        badge_cls   = "badge-wow" if type_produit=="wow" else "badge-blue"

        st.markdown(f"""<div style="background:var(--bg2);border:1px solid var(--border);
          border-radius:12px;padding:1rem 1.3rem;margin:1rem 0;
          display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
          <div>
            <p style="color:var(--muted);font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;margin:0 0 0.2rem;">Produit analysé</p>
            <p style="color:#fff;font-weight:800;font-size:1.1rem;margin:0;">{aname}</p>
            <p style="color:var(--muted);font-size:0.75rem;margin:0.2rem 0 0;">
              Achat : {aprice:,} F · Vente : {apmin:,}–{apmax:,} FCFA · Frais fixes : 5 000 F/vente
            </p>
          </div>
          <div style="display:flex;align-items:center;gap:0.8rem;">
            <span class="badge {badge_cls}">{badge_type}</span>
            <div style="text-align:center;">
              <p style="color:#fff;font-weight:900;font-size:2rem;margin:0;line-height:1;">{score_final}</p>
              <p style="color:var(--muted);font-size:0.6rem;margin:0;">/10 LABO</p>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── TABS RÉSULTATS ──
        tabs = st.tabs(["📊 Stratégie","🎁 Offres","🛍️ Shopify","📣 Facebook Ads",
                        "🎙️ Scripts & Créatives","🎯 Angles","👤 Avatar",
                        "🗓️ Plan 7 Jours","📥 Export"])

        # TAB 1 — STRATÉGIE
        with tabs[0]:
            col_s1, col_s2 = st.columns([1, 2], gap="large")
            with col_s1:
                slabel("Score LABO")
                st.markdown(f"""<div class="score-ring-wrap">
                  <div class="score-ring">
                    <span class="sr-val">{score_final}</span>
                    <span class="sr-max">/10</span>
                  </div>
                </div>""", unsafe_allow_html=True)

                alerte = score_data.get("alerte_rigueur")
                if alerte:
                    st.markdown(f"""<div style="border:1px solid #f85149;border-radius:8px;
                      padding:0.6rem 0.8rem;background:rgba(248,81,73,0.08);margin-top:0.5rem;">
                      <p style="color:#f85149;font-weight:700;font-size:0.78rem;margin:0;">{alerte}</p>
                    </div>""", unsafe_allow_html=True)

            with col_s2:
                slabel("Détail des 5 Critères")
                for cr in score_data["criteres"]:
                    n   = cr["note"]
                    col = "#3fb950" if n>=8 else "#f0883e" if n>=6 else "#f85149"
                    st.markdown(f"""<div class="critere-row">
                      <div class="critere-note" style="background:{col}22;color:{col};">{n}</div>
                      <div style="flex:1;">
                        <p style="color:#fff;font-weight:700;font-size:0.82rem;margin:0;">{cr['nom']}
                          <span style="color:var(--muted);font-size:0.65rem;font-weight:400;"> · {cr['poids']}</span>
                        </p>
                        <p style="color:var(--muted);font-size:0.7rem;margin:0;">{cr['desc']}</p>
                      </div>
                    </div>""", unsafe_allow_html=True)

            slabel("Analyse IA")
            st.code(data.get("score_justification",""), language=None)

            col_a1, col_a2 = st.columns(2, gap="medium")
            with col_a1:
                slabel("Public Cible")
                st.code(data.get("public_cible",""), language=None)

                slabel("😨 Peurs du Client")
                peurs = data.get("peurs",[])
                for p in peurs:
                    st.markdown(f'<div style="border-left:2px solid #f85149;padding:0.3rem 0.7rem;margin-bottom:0.3rem;color:#ccc;font-size:0.82rem;">{p}</div>', unsafe_allow_html=True)
                st.code("\n".join(f"• {p}" for p in peurs), language=None)

            with col_a2:
                slabel("✨ Désirs du Client")
                desirs = data.get("desirs",[])
                for d in desirs:
                    st.markdown(f'<div style="border-left:2px solid var(--green);padding:0.3rem 0.7rem;margin-bottom:0.3rem;color:#ccc;font-size:0.82rem;">{d}</div>', unsafe_allow_html=True)
                st.code("\n".join(f"• {d}" for d in desirs), language=None)

                slabel("🔑 Mots-Clés")
                mots = data.get("mots_cles",[])
                badges_html = "".join(f'<span style="border:1px solid rgba(217,4,41,0.4);color:#ccc;padding:3px 10px;border-radius:20px;font-size:0.72rem;margin:2px;display:inline-block;">{m}</span>' for m in mots)
                st.markdown(f'<div style="margin-bottom:0.4rem;">{badges_html}</div>', unsafe_allow_html=True)
                st.code(" · ".join(mots), language=None)

            slabel("💡 Améliorations Recommandées")
            amelios = data.get("ameliorations",[])
            for i, am in enumerate(amelios):
                st.markdown(f"""<div class="labo-card" style="padding:0.8rem 1rem;margin-bottom:0.5rem;">
                  <span style="color:var(--red);font-weight:700;font-size:0.75rem;">#{i+1}</span>
                  <span style="color:#ddd;font-size:0.83rem;margin-left:0.5rem;">{am}</span>
                </div>""", unsafe_allow_html=True)

            slabel("📊 Tableau Rentabilité")
            rows = ""
            for v in [1,5,10,15,20,30,50]:
                ca, cp, ff, cg, bn = calc_rentabilite(v, apmoy, aprice)
                cls_bn = "pos" if bn > 0 else "neg"
                hl = ' class="hl"' if v == 10 else ""
                rows += f'<tr{hl}><td{hl}>{v}</td><td>{ca:,.0f}</td><td>{cp:,.0f}</td><td>{ff:,.0f}</td><td class="{cls_bn}">{bn:,.0f}</td></tr>'
            st.markdown(f"""<table class="gtable">
              <tr><th>Ventes</th><th>CA (F)</th><th>Produit</th><th>Frais fixes</th><th>Bénéf net (F)</th></tr>
              {rows}
            </table>""", unsafe_allow_html=True)

        # TAB 2 — OFFRES
        with tabs[1]:
            slabel("🎁 Offres Commerciales — Marché Africain")
            for i, o in enumerate(data.get("offres",[])):
                st.markdown(f"""<div class="offre-bloc">
                  <p class="offre-nom">🎁 Offre {i+1} — {o.get('nom','')}</p>
                  <p class="offre-desc">{o.get('description','')}</p>
                  <p class="offre-prix">💰 {o.get('prix_suggere','')} · {o.get('argument','')}</p>
                </div>""", unsafe_allow_html=True)
                st.code(f"{o.get('nom','')}\n{o.get('description','')}\nPrix : {o.get('prix_suggere','')}\nArgument : {o.get('argument','')}", language=None)

        # TAB 3 — SHOPIFY
        with tabs[2]:
            shopify = data.get("shopify",{})
            slabel("🏷️ 3 Titres Magnétiques")
            for i, t in enumerate(shopify.get("titres",[])):
                st.markdown(f"""<div style="background:var(--bg3);border:1px solid var(--border);
                  border-left:3px solid var(--red);border-radius:0 10px 10px 0;
                  padding:0.9rem 1.2rem;margin-bottom:0.6rem;">
                  <span style="color:var(--red);font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;">{t.get('angle','')}</span>
                  <p style="color:#fff;font-weight:800;font-size:1rem;margin:0.3rem 0 0;">{t.get('titre','')}</p>
                </div>""", unsafe_allow_html=True)
                st.code(t.get('titre',''), language=None)

            st.markdown("<hr>", unsafe_allow_html=True)
            slabel("📝 Fiche Produit — 6 Paragraphes")
            paras = shopify.get("paragraphes",[])
            for j, p in enumerate(paras):
                st.markdown(f"""<div class="para-bloc">
                  <p class="para-titre">{p.get('titre','')}</p>
                  <p class="para-texte">{p.get('texte','').replace(chr(10),'<br>')}</p>
                </div>""", unsafe_allow_html=True)
                st.code(f"{p.get('titre','')}\n\n{p.get('texte','')}", language=None)

            slabel("📦 Copier la fiche complète")
            all_p = "\n\n".join(f"{p.get('titre','')}\n{p.get('texte','')}" for p in paras)
            st.code(all_p, language=None)

        # TAB 4 — FACEBOOK ADS
        with tabs[3]:
            slabel("📣 3 Variantes Facebook Ads")
            st.markdown('<p style="color:var(--muted);font-size:0.75rem;margin:0 0 1rem;">Copie → colle dans Facebook Ads Manager</p>', unsafe_allow_html=True)
            for i, ad in enumerate(data.get("facebook_ads",[])):
                accroche = ad.get("accroche", ad.get("titre",""))
                texte    = ad.get("texte",    ad.get("text", ""))
                angle    = ad.get("angle",    f"Variante {i+1}")
                st.markdown(f"""<div class="ad-card">
                  <p class="ad-accroche">{accroche}</p>
                  <p class="ad-texte">{texte.replace(chr(10),'<br>')}</p>
                </div>""", unsafe_allow_html=True)
                st.code(f"{accroche}\n\n{texte}", language=None)

        # TAB 5 — SCRIPTS & CRÉATIVES
        with tabs[4]:
            slabel("🎙️ Scripts Voix-Off (130–170 mots chacun)")
            scripts = data.get("scripts",[])
            for i, s in enumerate(scripts):
                txt = s.get("texte_complet", s.get("texte",""))
                wc  = len(txt.split())
                wc_col = "#3fb950" if 125<=wc<=175 else "#f0883e"
                st.markdown(f"""<div class="script-card">
                  <p class="script-label">Script {i+1} — {s.get('angle','')}
                    <span style="color:{wc_col};margin-left:0.5rem;">· {wc} mots</span>
                  </p>
                  <p class="script-text">{txt.replace(chr(10),'<br>')}</p>
                </div>""", unsafe_allow_html=True)
                st.code(txt, language=None)

            st.markdown("<hr>", unsafe_allow_html=True)
            slabel("🎬 Concepts Créatives Publicitaires")
            creatives = data.get("creatives",[])
            icons_cr  = ["🔴","🟠","🟡","🟢"]
            for i, cr in enumerate(creatives):
                ic = icons_cr[i] if i < 4 else "🎬"
                full = f"Concept : {cr.get('concept','')}\nScène : {cr.get('scene','')}\nMessage : {cr.get('message','')}\nType d'accroche : {cr.get('accroche_type','')}"
                st.markdown(f"""<div class="labo-card">
                  <p class="lc-label">{ic} Créative {i+1}</p>
                  <p class="lc-title">{cr.get('concept','')}</p>
                  <div style="display:grid;gap:0.4rem;margin-top:0.5rem;">
                    <p style="color:var(--muted);font-size:0.72rem;margin:0;">🎬 Scène : <span style="color:#ddd;">{cr.get('scene','')}</span></p>
                    <p style="color:var(--muted);font-size:0.72rem;margin:0;">💬 Message : <span style="color:#ddd;">{cr.get('message','')}</span></p>
                    <span class="badge badge-red">{cr.get('accroche_type','')}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
                st.code(full, language=None)

        # TAB 6 — ANGLES
        with tabs[5]:
            slabel("🎯 5 Angles Marketing — Marché Africain Francophone")
            angles = data.get("angles_marketing",[])
            icons_a = ["🔴","🟠","🟡","🟢","🔵"]
            for i, ang in enumerate(angles):
                ic = icons_a[i] if i<5 else "🎯"
                st.markdown(f"""<div class="labo-card">
                  <p class="lc-label">{ic} Angle {i+1} — {ang.get('angle','')}</p>
                  <p class="lc-title">{ang.get('titre','')}</p>
                  <p class="lc-text">{ang.get('accroche','')}</p>
                </div>""", unsafe_allow_html=True)
                st.code(f"{ang.get('titre','')}\n\n{ang.get('accroche','')}", language=None)

        # TAB 7 — AVATAR
        with tabs[6]:
            av = data.get("avatar",{})
            if av:
                prenom   = av.get("prenom_type","Le client type")
                sexe     = av.get("sexe","—")
                age      = av.get("age","—")
                categ    = av.get("categorie","—")
                ville    = av.get("ville","—")
                prof     = av.get("profession","—")
                revenu   = av.get("revenu","—")
                mode_vie = av.get("mode_vie","—")
                fr_niv   = av.get("francais","—")
                frusts   = av.get("frustrations",[])
                desirs_a = av.get("desirs",[])
                objecs   = av.get("objections",[])
                msg_cle  = av.get("message_cle","—")

                st.markdown(f"""<div class="labo-card" style="border-color:rgba(217,4,41,0.25);">
                  <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
                    <div style="font-size:3rem;">👤</div>
                    <div>
                      <p style="color:#fff;font-weight:900;font-size:1.3rem;margin:0;">{prenom}</p>
                      <p style="color:var(--muted);font-size:0.78rem;margin:0.2rem 0 0;">{sexe} · {age} · {ville}</p>
                      <span class="badge badge-red" style="margin-top:0.3rem;display:inline-block;">{categ}</span>
                    </div>
                  </div>
                  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.8rem;">
                    <span class="badge badge-blue">{prof}</span>
                    <span class="badge badge-orange">{revenu}</span>
                    <span class="badge badge-blue">Français {fr_niv}</span>
                  </div>
                  <p style="color:#bbb;font-size:0.83rem;margin-top:0.7rem;line-height:1.7;">{mode_vie}</p>
                </div>""", unsafe_allow_html=True)

                ca1, ca2, ca3 = st.columns(3, gap="small")
                with ca1:
                    slabel("😤 Frustrations")
                    for f in frusts:
                        st.markdown(f'<div style="border-left:2px solid #f85149;padding:0.35rem 0.7rem;margin-bottom:0.3rem;color:#ccc;font-size:0.8rem;">{f}</div>', unsafe_allow_html=True)
                with ca2:
                    slabel("✨ Désirs")
                    for d in desirs_a:
                        st.markdown(f'<div style="border-left:2px solid var(--green);padding:0.35rem 0.7rem;margin-bottom:0.3rem;color:#ccc;font-size:0.8rem;">{d}</div>', unsafe_allow_html=True)
                with ca3:
                    slabel("🤔 Objections")
                    for o in objecs:
                        st.markdown(f'<div style="border-left:2px solid var(--orange);padding:0.35rem 0.7rem;margin-bottom:0.3rem;color:#ccc;font-size:0.8rem;">{o}</div>', unsafe_allow_html=True)

                slabel("💬 Message Clé qui Convainc")
                st.markdown(f"""<div style="border:1px solid rgba(217,4,41,0.3);border-radius:10px;
                  padding:1.1rem 1.3rem;margin-top:0.5rem;background:var(--bg3);">
                  <p style="color:#fff;font-size:1rem;font-weight:700;line-height:1.8;margin:0;font-style:italic;">"{msg_cle}"</p>
                </div>""", unsafe_allow_html=True)
                st.code(msg_cle, language=None)

        # TAB 8 — PLAN 7 JOURS
        with tabs[7]:
            slabel("🗓️ Plan de Lancement 7 Jours")
            st.markdown('<p style="color:var(--muted);font-size:0.78rem;margin:0 0 1rem;">Actions concrètes jour par jour pour lancer et scaler ton produit</p>', unsafe_allow_html=True)
            plan = data.get("plan_7j",[])
            jour_colors = ["#D90429","#ff6b35","#f0883e","#ffd700","#3fb950","#58a6ff","#bc8cff"]
            for j, jour in enumerate(plan):
                col = jour_colors[j] if j < 7 else "#D90429"
                all_txt = f"Jour {jour.get('jour','')}: {jour.get('titre','')}\nAction: {jour.get('action','')}\nBudget pub: {jour.get('budget','')}\nCiblage: {jour.get('ciblage','')}\nContenu: {jour.get('contenu','')}"
                st.markdown(f"""<div class="jour-card">
                  <div class="jour-num" style="background:{col}22;border-color:{col}44;color:{col};">{jour.get('jour','')}</div>
                  <p class="jour-titre">{jour.get('titre','')}</p>
                  <div class="jour-row">
                    <span class="jour-label">🎯 Action</span>
                    <span class="jour-val">{jour.get('action','')}</span>
                  </div>
                  <div class="jour-row">
                    <span class="jour-label">💰 Budget</span>
                    <span class="jour-val" style="color:{col};">{jour.get('budget','')}</span>
                  </div>
                  <div class="jour-row">
                    <span class="jour-label">👥 Ciblage</span>
                    <span class="jour-val">{jour.get('ciblage','')}</span>
                  </div>
                  <div class="jour-row">
                    <span class="jour-label">📝 Contenu</span>
                    <span class="jour-val">{jour.get('contenu','')}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
                st.code(all_txt, language=None)

        # TAB 9 — EXPORT
        with tabs[8]:
            slabel("📥 Pack Marketing Complet")
            st.markdown('<p style="color:var(--muted);font-size:0.78rem;margin:0 0 1rem;">Toute l\'analyse exportée en fichier .txt</p>', unsafe_allow_html=True)
            export_txt = build_export(aname, aprice, apmin, apmax, data)
            st.download_button(
                label="⬇️ TÉLÉCHARGER MON PACK MARKETING (.txt)",
                data=export_txt,
                file_name=f"pack_{aname.replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.code(export_txt[:1000] + "\n\n[...] Télécharge pour voir la suite", language=None)

# ════════════════════════════════════════════════════════════
# PAGE 2 : IMAGES PRODUIT (Bing Search — images dans l'app)
# ════════════════════════════════════════════════════════════
elif page == "images":
    aname = st.session_state.get("active_product","")

    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h1 style="font-size:1.5rem;font-weight:800;color:#fff;margin:0 0 0.3rem;">
        🖼️ Images Produit
      </h1>
      <p style="color:#7d8590;font-size:0.82rem;margin:0;">
        Recherche d'images réelles · Affichées directement · Téléchargeables en un clic
      </p>
    </div>""", unsafe_allow_html=True)

    col_q, col_btn = st.columns([4, 1], gap="small")
    with col_q:
        search_q = st.text_input("🔍 Nom du produit à chercher",
            value=aname if aname else "",
            placeholder="Ex: Beauty Milk serum, lampe solaire...",
            key="img_search_q")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Chercher", use_container_width=True, key="btn_img")

    if search_btn and search_q.strip():
        with st.spinner("🔍 Recherche d'images en cours..."):
            imgs = search_bing_images(search_q.strip() + " product", max_results=10)
            st.session_state["img_results"]    = imgs
            st.session_state["img_query_done"] = search_q.strip()

    imgs_found = st.session_state.get("img_results",[])
    q_done     = st.session_state.get("img_query_done","")

    if imgs_found:
        st.markdown(f'<p style="color:var(--green);font-size:0.78rem;font-weight:700;margin:0.5rem 0 1rem;">✅ {len(imgs_found)} images trouvées pour « {q_done} »</p>',
                    unsafe_allow_html=True)

        # Grille 3 colonnes
        for row_start in range(0, len(imgs_found), 3):
            row_imgs = imgs_found[row_start:row_start+3]
            gcols    = st.columns(len(row_imgs), gap="small")
            for ci, (gcol, img) in enumerate(zip(gcols, row_imgs)):
                with gcol:
                    idx   = row_start + ci
                    url   = img["url"]
                    thumb = img.get("thumb", url)
                    title = img.get("title","")[:50]

                    st.markdown('<div class="img-result-card">', unsafe_allow_html=True)
                    try:
                        st.image(thumb, use_column_width=True)
                    except Exception:
                        st.markdown(f'<img src="{thumb}" style="width:100%;height:160px;object-fit:cover;display:block;" />', unsafe_allow_html=True)
                    st.markdown(f"""<div class="img-footer">
                      <p>#{idx+1} {title}</p>
                      <a href="{url}" target="_blank" class="dl-btn">⬇️ Télécharger</a>
                    </div></div>""", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        slabel("Chercher aussi sur ces plateformes")
        q_enc = urllib.parse.quote_plus(search_q if search_q else q_done)
        platforms = [
            ("🛒 AliExpress", f"https://fr.aliexpress.com/wholesale?SearchText={q_enc}"),
            ("🛍️ Amazon",    f"https://www.amazon.fr/s?k={q_enc}"),
            ("📌 Pinterest",  f"https://www.pinterest.com/search/pins/?q={q_enc}"),
            ("🛒 Temu",       f"https://www.temu.com/search_result.html?search_key={q_enc}"),
            ("🏭 Alibaba",    f"https://www.alibaba.com/trade/search?SearchText={q_enc}"),
        ]
        pc = st.columns(5, gap="small")
        for i, (pname, purl) in enumerate(platforms):
            with pc[i]:
                st.markdown(f'<a href="{purl}" target="_blank" class="dl-btn" style="background:var(--bg3);color:var(--text);border:1px solid var(--border2);border-radius:8px;padding:10px;display:block;text-align:center;font-size:0.78rem;font-weight:600;text-decoration:none;">{pname}</a>', unsafe_allow_html=True)

    elif q_done:
        st.warning(f"⚠️ Aucune image trouvée pour « {q_done} ». Essaie en anglais.")
    else:
        st.markdown("""<div style="border:1px dashed rgba(255,255,255,0.1);border-radius:12px;
          padding:3rem;text-align:center;margin-top:1rem;">
          <p style="font-size:2.5rem;margin:0 0 0.7rem;">🖼️</p>
          <p style="color:#484f58;font-size:0.88rem;margin:0 0 0.3rem;font-weight:600;">Lance une recherche</p>
          <p style="color:#30363d;font-size:0.75rem;margin:0;">Les images s'affichent directement ici</p>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 3 : SPY CONCURRENTS
# ════════════════════════════════════════════════════════════
elif page == "spy":
    aname = st.session_state.get("active_product","")

    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h1 style="font-size:1.5rem;font-weight:800;color:#fff;margin:0 0 0.3rem;">
        🕵️ Spy Concurrents
      </h1>
      <p style="color:#7d8590;font-size:0.82rem;margin:0;">
        Trouver les concurrents qui vendent déjà ton produit en Afrique Francophone
      </p>
    </div>""", unsafe_allow_html=True)

    spy_q = st.text_input("📦 Produit à espionner",
        value=aname if aname else "",
        placeholder="Ex: crème éclaircissante, lampe détecteur...")

    if spy_q.strip():
        q_enc = urllib.parse.quote_plus(spy_q.strip())

        PAYS = [
            {"nom":"🇹🇬 Togo",           "code":"TG", "flag":"🇹🇬", "adlib":"TG", "fb_region":"TG"},
            {"nom":"🇸🇳 Sénégal",        "code":"SN", "flag":"🇸🇳", "adlib":"SN", "fb_region":"SN"},
            {"nom":"🇨🇮 Côte d'Ivoire",  "code":"CI", "flag":"🇨🇮", "adlib":"CI", "fb_region":"CI"},
            {"nom":"🇧🇯 Bénin",          "code":"BJ", "flag":"🇧🇯", "adlib":"BJ", "fb_region":"BJ"},
            {"nom":"🇬🇳 Guinée-Conakry", "code":"GN", "flag":"🇬🇳", "adlib":"GN", "fb_region":"GN"},
            {"nom":"🇨🇬 Congo",          "code":"CG", "flag":"🇨🇬", "adlib":"CG", "fb_region":"CG"},
        ]

        st.markdown("<br>", unsafe_allow_html=True)
        slabel("📣 Publicités Facebook par Pays")
        st.markdown('<p style="color:var(--muted);font-size:0.75rem;margin:0 0 1rem;">Clique sur un pays → Facebook Ad Library filtrée sur ce pays + ton produit</p>', unsafe_allow_html=True)

        cols_p = st.columns(3, gap="small")
        for i, p in enumerate(PAYS):
            with cols_p[i % 3]:
                fb_url = (
                    f"https://www.facebook.com/ads/library/"
                    f"?active_status=all&ad_type=all&country={p['adlib']}"
                    f"&q={q_enc}&search_type=keyword_unordered"
                )
                st.markdown(f"""<a href="{fb_url}" target="_blank" style="text-decoration:none;">
                  <div class="pays-card">
                    <p class="pays-flag">{p['flag']}</p>
                    <p class="pays-nom">{p['nom']}</p>
                    <p style="color:var(--muted);font-size:0.68rem;margin:0.3rem 0 0;">Voir pubs Facebook →</p>
                  </div>
                </a>""", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        slabel("🔍 Boutiques Concurrentes")
        st.markdown('<p style="color:var(--muted);font-size:0.75rem;margin:0 0 1rem;">Trouver les boutiques qui vendent déjà ce produit en Afrique</p>', unsafe_allow_html=True)

        q_africa = urllib.parse.quote_plus(spy_q.strip() + " Afrique acheter livraison")
        q_shopify = urllib.parse.quote_plus(spy_q.strip() + " site:myshopify.com OR site:shopify.com Afrique")
        q_togo    = urllib.parse.quote_plus(spy_q.strip() + " Lomé Togo commander livraison")
        q_ci      = urllib.parse.quote_plus(spy_q.strip() + " Abidjan Côte d'Ivoire commander")

        spy_links = [
            ("🌍 Google — Boutiques Afrique",
             f"https://www.google.com/search?q={q_africa}"),
            ("🛒 Google — Boutiques Shopify Afrique",
             f"https://www.google.com/search?q={q_shopify}"),
            ("🇹🇬 Concurrents au Togo",
             f"https://www.google.com/search?q={q_togo}"),
            ("🇨🇮 Concurrents en Côte d'Ivoire",
             f"https://www.google.com/search?q={q_ci}"),
            ("📌 Créatives Pinterest — Afrique",
             f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote_plus(spy_q.strip()+' Afrique')}"),
            ("🎬 Vidéos créatives TikTok",
             f"https://www.tiktok.com/search?q={q_enc}"),
        ]

        sl_cols = st.columns(2, gap="medium")
        for i, (label, url) in enumerate(spy_links):
            with sl_cols[i % 2]:
                st.markdown(f"""<a href="{url}" target="_blank" style="text-decoration:none;">
                  <div class="labo-card" style="cursor:pointer;margin-bottom:0.6rem;">
                    <p class="lc-title">{label}</p>
                    <p class="lc-text" style="font-size:0.7rem;">{url[:60]}...</p>
                  </div>
                </a>""", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        slabel("🎬 Créatives Vidéo Concurrentes")
        st.markdown('<p style="color:var(--muted);font-size:0.75rem;margin:0 0 1rem;">Vidéos de produits similaires sur YouTube et TikTok</p>', unsafe_allow_html=True)

        yt_url  = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(spy_q.strip()+' produit Afrique publicité')}"
        pin_vid = f"https://www.pinterest.com/search/videos/?q={q_enc}"

        vc = st.columns(2, gap="medium")
        with vc[0]:
            st.markdown(f'<a href="{yt_url}" target="_blank" class="dl-btn" style="background:#FF0000;margin-bottom:0.5rem;display:block;border-radius:8px;padding:12px;text-align:center;color:#fff;font-weight:700;text-decoration:none;">▶️ YouTube — Vidéos concurrentes</a>', unsafe_allow_html=True)
        with vc[1]:
            st.markdown(f'<a href="{pin_vid}" target="_blank" class="dl-btn" style="background:#E60023;margin-bottom:0.5rem;display:block;border-radius:8px;padding:12px;text-align:center;color:#fff;font-weight:700;text-decoration:none;">📌 Pinterest — Vidéos produit</a>', unsafe_allow_html=True)

    else:
        st.markdown("""<div style="border:1px dashed rgba(255,255,255,0.1);border-radius:12px;
          padding:3rem;text-align:center;margin-top:1rem;">
          <p style="font-size:2.5rem;margin:0 0 0.7rem;">🕵️</p>
          <p style="color:#484f58;font-size:0.88rem;margin:0 0 0.3rem;font-weight:600;">Entre un nom de produit pour espionner</p>
          <p style="color:#30363d;font-size:0.75rem;margin:0;">Concurrents · Publicités · Vidéos · Boutiques</p>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 4 : CALCULATEUR BUDGET PUB INTELLIGENT
# ════════════════════════════════════════════════════════════
elif page == "budget":
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h1 style="font-size:1.5rem;font-weight:800;color:#fff;margin:0 0 0.3rem;">
        💰 Calculateur Budget Pub Intelligent
      </h1>
      <p style="color:#7d8590;font-size:0.82rem;margin:0;">
        Basé sur les benchmarks réels Facebook Afrique — CPM, CTR, taux de conversion
      </p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(240,136,62,0.08);border:1px solid rgba(240,136,62,0.2);
      border-radius:10px;padding:0.8rem 1rem;margin-bottom:1.5rem;">
      <p style="color:#f0883e;font-size:0.78rem;margin:0;line-height:1.8;">
        📊 <b>Benchmarks Facebook Afrique Francophone (2024)</b><br>
        CPM moyen : <b>0.80$</b> · CTR moyen : <b>1.8%</b> · Taux de conversion e-com : <b>1–3%</b>
      </p>
    </div>""", unsafe_allow_html=True)

    bc1, bc2 = st.columns(2, gap="large")
    with bc1:
        prix_vente_b = st.number_input("💰 Prix de vente (FCFA)", min_value=1000, step=500,
            value=int(st.session_state.get("active_price",5000))+10000)
        objectif_b   = st.number_input("🎯 Objectif ventes/jour", min_value=1, step=1, value=5)
    with bc2:
        taux_conv    = st.slider("📊 Taux de conversion estimé (%)", 0.5, 5.0, 2.0, 0.1)
        prix_achat_b = st.number_input("🏷️ Prix d'achat (FCFA)", min_value=0, step=500,
            value=int(st.session_state.get("active_price",5000)))

    res = calc_budget_pub(objectif_b, prix_vente_b, taux_conv)
    marge_nette_vente = prix_vente_b - prix_achat_b - 5000

    st.markdown("<br>", unsafe_allow_html=True)
    slabel("Résultats du Calculateur")

    br1, br2, br3 = st.columns(3, gap="medium")
    with br1:
        st.markdown(f"""<div class="stat-card" style="border-color:rgba(217,4,41,0.3);">
          <p class="s-label">💸 Budget Quotidien</p>
          <p class="s-value" style="color:var(--red);">{res['budget_jour']:.2f}$</p>
          <p class="s-sub">Pour {objectif_b} ventes/jour</p>
        </div>""", unsafe_allow_html=True)
    with br2:
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">📅 Budget Test 3 jours</p>
          <p class="s-value" style="color:var(--orange);">{res['budget_3j']:.2f}$</p>
          <p class="s-sub">{res['budget_3j']*655:.0f} FCFA environ</p>
        </div>""", unsafe_allow_html=True)
    with br3:
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">📅 Budget Test 5 jours</p>
          <p class="s-value" style="color:var(--blue);">{res['budget_5j']:.2f}$</p>
          <p class="s-sub">{res['budget_5j']*655:.0f} FCFA environ</p>
        </div>""", unsafe_allow_html=True)

    br4, br5, br6 = st.columns(3, gap="medium")
    with br4:
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">🖱️ CPC Estimé</p>
          <p class="s-value" style="color:var(--purple);">{res['cpc_estime']:.3f}$</p>
          <p class="s-sub">Coût par clic moyen Afrique</p>
        </div>""", unsafe_allow_html=True)
    with br5:
        st.markdown(f"""<div class="stat-card">
          <p class="s-label">👥 Clics Nécessaires</p>
          <p class="s-value">{res['clics_besoin']}</p>
          <p class="s-sub">Pour {objectif_b} ventes à {taux_conv}% conv.</p>
        </div>""", unsafe_allow_html=True)
    with br6:
        st.markdown(f"""<div class="stat-card" style="border-color:rgba(63,185,80,0.3);">
          <p class="s-label">💰 Marge Nette/Vente</p>
          <p class="s-value" style="color:{'var(--green)' if marge_nette_vente>0 else '#f85149'};">
            {marge_nette_vente:,.0f} F</p>
          <p class="s-sub">Après achat + frais fixes 5 000 F</p>
        </div>""", unsafe_allow_html=True)

    benefice_jour = marge_nette_vente * objectif_b
    depense_pub   = res['budget_jour'] * 655

    st.markdown(f"""<div style="background:var(--bg2);border:1px solid var(--border);
      border-radius:12px;padding:1.3rem;margin-top:1rem;">
      <p style="color:var(--muted);font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;margin:0 0 1rem;">📊 Résumé quotidien estimé</p>
      <div style="display:flex;gap:1.5rem;flex-wrap:wrap;">
        <div>
          <p style="color:var(--muted);font-size:0.7rem;margin:0;">Revenus</p>
          <p style="color:#fff;font-weight:700;font-size:1.1rem;margin:0;">{objectif_b*prix_vente_b:,.0f} F</p>
        </div>
        <div>
          <p style="color:var(--muted);font-size:0.7rem;margin:0;">Budget pub</p>
          <p style="color:#f85149;font-weight:700;font-size:1.1rem;margin:0;">−{depense_pub:,.0f} F</p>
        </div>
        <div>
          <p style="color:var(--muted);font-size:0.7rem;margin:0;">Frais fixes</p>
          <p style="color:#f0883e;font-weight:700;font-size:1.1rem;margin:0;">−{objectif_b*5000:,.0f} F</p>
        </div>
        <div>
          <p style="color:var(--muted);font-size:0.7rem;margin:0;">Achat produit</p>
          <p style="color:#f0883e;font-weight:700;font-size:1.1rem;margin:0;">−{objectif_b*prix_achat_b:,.0f} F</p>
        </div>
        <div>
          <p style="color:var(--muted);font-size:0.7rem;margin:0;">🏆 Bénéfice net</p>
          <p style="color:{'var(--green)' if benefice_jour-depense_pub>0 else '#f85149'};font-weight:900;font-size:1.3rem;margin:0;">
            {benefice_jour-depense_pub:,.0f} F
          </p>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="margin-top:1rem;background:rgba(88,166,255,0.06);border:1px solid rgba(88,166,255,0.15);
      border-radius:10px;padding:0.8rem 1rem;">
      <p style="color:#58a6ff;font-size:0.78rem;margin:0;line-height:1.8;">
        💡 <b>Conseil LABO :</b> Commence toujours avec le budget minimum 3-5 jours.
        Si ROAS > 2 (tu gagnes 2F pour 1F dépensé), tu peux doubler le budget.
        Si pas de ventes après 3 jours → change la créative avant de changer le ciblage.
      </p>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 5 : COMPARATEUR DE PRODUITS
# ════════════════════════════════════════════════════════════
elif page == "comparateur":
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h1 style="font-size:1.5rem;font-weight:800;color:#fff;margin:0 0 0.3rem;">
        ⚖️ Comparateur de Produits
      </h1>
      <p style="color:#7d8590;font-size:0.82rem;margin:0;">
        Compare 2 produits selon les 5 critères LABO et choisis le meilleur
      </p>
    </div>""", unsafe_allow_html=True)

    cc1, cc2 = st.columns(2, gap="large")

    CATS = ["Domestique","Beauté & Soins","Santé","Tech","Mode","Alimentation","Luxe","Agriculture","Élevage","Pêche","Autre"]

    with cc1:
        st.markdown('<p style="color:var(--red);font-weight:700;margin-bottom:0.5rem;">🅰️ Produit 1</p>', unsafe_allow_html=True)
        p1_nom    = st.text_input("Nom", key="p1_nom", placeholder="Ex: Crème Beauty Milk")
        p1_achat  = st.number_input("Prix achat (FCFA)", min_value=0, step=500, key="p1_achat", value=5000)
        p1_vente  = st.number_input("Prix vente (FCFA)", min_value=0, step=500, key="p1_vente", value=15000)
        p1_type   = st.selectbox("Type", ["wow","probleme_solution"], key="p1_type")
        p1_cat    = st.selectbox("Catégorie", CATS, key="p1_cat")

    with cc2:
        st.markdown('<p style="color:var(--blue);font-weight:700;margin-bottom:0.5rem;">🅱️ Produit 2</p>', unsafe_allow_html=True)
        p2_nom    = st.text_input("Nom", key="p2_nom", placeholder="Ex: Lampe solaire LED")
        p2_achat  = st.number_input("Prix achat (FCFA)", min_value=0, step=500, key="p2_achat", value=3000)
        p2_vente  = st.number_input("Prix vente (FCFA)", min_value=0, step=500, key="p2_vente", value=12000)
        p2_type   = st.selectbox("Type", ["wow","probleme_solution"], key="p2_type")
        p2_cat    = st.selectbox("Catégorie", CATS, key="p2_cat")

    if st.button("⚖️ COMPARER LES 2 PRODUITS", use_container_width=True):
        # Construire données mock pour calc_score_produit
        def mock_data(type_p, cat, vente):
            return {
                "score": 7, "type_produit": type_p,
                "avatar": {"categorie": cat},
                "peurs": ["peur1","peur2","peur3"],
                "desirs": ["désir1","désir2","désir3"],
            }

        d1 = mock_data(p1_type, p1_cat, p1_vente)
        d2 = mock_data(p2_type, p2_cat, p2_vente)
        s1 = calc_score_produit(p1_achat, p1_vente, d1)
        s2 = calc_score_produit(p2_achat, p2_vente, d2)

        slabel("⚖️ Résultats de la Comparaison")

        r1, r2 = st.columns(2, gap="large")
        winner = "A" if s1["score_final"] >= s2["score_final"] else "B"
        for col, s, pnom, pachat, pvente, col_accent, side in [
            (r1, s1, p1_nom or "Produit 1", p1_achat, p1_vente, "#D90429", "A"),
            (r2, s2, p2_nom or "Produit 2", p2_achat, p2_vente, "#58a6ff", "B"),
        ]:
            with col:
                is_w = winner == side
                st.markdown(f"""<div class="labo-card" style="border-color:{'rgba(63,185,80,0.4)' if is_w else 'var(--border)'};
                  {'background:rgba(63,185,80,0.04)' if is_w else ''}">
                  {'<p style="color:var(--green);font-weight:700;font-size:0.78rem;margin:0 0 0.5rem;">🏆 MEILLEUR CHOIX</p>' if is_w else ''}
                  <p style="color:{col_accent};font-weight:800;font-size:1.2rem;margin:0 0 0.3rem;">{pnom}</p>
                  <p style="color:var(--muted);font-size:0.72rem;margin:0 0 0.8rem;">
                    Achat {pachat:,} F · Vente {pvente:,} F · Marge {pvente-pachat-5000:,} F
                  </p>
                  <div style="text-align:center;margin-bottom:1rem;">
                    <p style="color:#fff;font-size:2.5rem;font-weight:900;margin:0;line-height:1;">{s['score_final']}</p>
                    <p style="color:var(--muted);font-size:0.65rem;margin:0;">/10 Score LABO</p>
                  </div>
                """, unsafe_allow_html=True)
                for cr in s["criteres"]:
                    n   = cr["note"]
                    c   = "#3fb950" if n>=8 else "#f0883e" if n>=6 else "#f85149"
                    bar = int((n/10)*100)
                    st.markdown(f"""<div style="margin-bottom:0.5rem;">
                      <div style="display:flex;justify-content:space-between;margin-bottom:0.2rem;">
                        <span style="color:var(--muted);font-size:0.7rem;">{cr['nom']}</span>
                        <span style="color:{c};font-weight:700;font-size:0.7rem;">{n}/10</span>
                      </div>
                      <div style="background:var(--bg3);border-radius:4px;height:5px;">
                        <div style="width:{bar}%;background:{c};border-radius:4px;height:5px;"></div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 6 : TÉMOIGNAGES
# ════════════════════════════════════════════════════════════
elif page == "temoignages":
    st.markdown("""<div style="margin-bottom:1.5rem;">
      <h1 style="font-size:1.5rem;font-weight:800;color:#fff;margin:0 0 0.3rem;">
        💬 Témoignages & Avis Clients
      </h1>
      <p style="color:#7d8590;font-size:0.82rem;margin:0;">
        Avis clients africains générés par l'IA · Prêts à copier sur ta page Shopify
      </p>
    </div>""", unsafe_allow_html=True)

    data = st.session_state.get("result")
    if not data:
        st.info("⚠️ Lance d'abord une analyse produit pour générer les témoignages.")
    else:
        aname  = st.session_state.get("active_product","le produit")
        temos  = data.get("temoignages",[])

        if not temos:
            st.warning("⚠️ Témoignages non générés. Relance une analyse.")
        else:
            st.markdown(f'<p style="color:var(--muted);font-size:0.78rem;margin:0 0 1.2rem;">5 témoignages africains authentiques pour <b style="color:#fff;">{aname}</b></p>', unsafe_allow_html=True)

            for i, t in enumerate(temos):
                prenom   = t.get("prenom","Client")
                ville    = t.get("ville","Afrique")
                duree    = t.get("produit_utilise","")
                avis     = t.get("avis","")
                note     = int(t.get("note",5))
                initiale = prenom[0].upper() if prenom else "C"
                stars    = "⭐" * note + "☆" * (5-note)

                full_temo = f'"{avis}"\n— {prenom}, {ville} ({duree})\n{"★"*note}'
                st.markdown(f"""<div class="temoignage-card">
                  <div class="temo-header">
                    <div class="temo-avatar">{initiale}</div>
                    <div>
                      <p class="temo-name">{prenom}</p>
                      <p class="temo-ville">📍 {ville} · {duree}</p>
                      <p class="temo-stars">{stars}</p>
                    </div>
                  </div>
                  <p class="temo-text">"{avis}"</p>
                </div>""", unsafe_allow_html=True)
                st.code(full_temo, language=None)

            st.markdown("<hr>", unsafe_allow_html=True)
            slabel("📦 Copier tous les témoignages")
            all_temos = "\n\n".join(
                f'"{t.get("avis","")}" — {t.get("prenom","")}, {t.get("ville","")} ({t.get("produit_utilise","")}) {"★"*int(t.get("note",5))}'
                for t in temos
            )
            st.code(all_temos, language=None)

st.markdown("</div>", unsafe_allow_html=True)
