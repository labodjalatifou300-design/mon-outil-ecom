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
_defaults = [
    ("history",        load_history_file()),
    ("result",         None),
    ("analyzed",       False),
    ("active_product", ""),
    ("active_price",   5000),
    ("active_ventes",  10),
    ("nav_page",       "analyse"),
    ("img_results",    []),
    ("img_query_done", ""),
]
for k, v in _defaults:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="EcoMaster Labo Pro", page_icon="🚀", layout="wide")
st.markdown('<meta name="color-scheme" content="dark"><meta name="theme-color" content="#090c10">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# CSS — DESIGN MINEA AUTHENTIQUE
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ─── VARIABLES ─────────────────────────────────────────── */
:root {
  --bg0:    #090c10;
  --bg1:    #0d1117;
  --bg2:    #13181f;
  --bg3:    #1a2130;
  --bg4:    #1e2535;
  --border: rgba(255,255,255,0.06);
  --border2:rgba(255,255,255,0.11);
  --red:    #e8192c;
  --red2:   rgba(232,25,44,0.12);
  --red3:   rgba(232,25,44,0.25);
  --text:   #e6edf3;
  --muted:  #7d8590;
  --dim:    #3d444d;
  --green:  #2ea043;
  --green2: rgba(46,160,67,0.15);
  --orange: #d29922;
  --blue:   #4493f8;
  --blue2:  rgba(68,147,248,0.12);
}

/* ─── BASE ───────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp, .main, .block-container,
.appview-container, .appview-container > section,
[class*="css"], [data-testid] {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  background-color: var(--bg0) !important;
  color: var(--text) !important;
}
@media (prefers-color-scheme: light) {
  html, body, .stApp, .main, .block-container,
  .appview-container, .appview-container > section,
  [class*="css"], [data-testid] {
    background-color: var(--bg0) !important;
    color: var(--text) !important;
  }
}
.block-container {
  max-width: 100% !important;
  padding: 0 !important;
}

/* ─── SIDEBAR ────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--bg1) !important;
  border-right: 1px solid var(--border) !important;
  min-width: 230px !important;
  max-width: 230px !important;
}
section[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
}

/* ─── LOGO SIDEBAR ───────────────────────────────────────── */
.sb-logo {
  padding: 18px 16px 14px;
  border-bottom: 1px solid var(--border);
}
.sb-logo-title {
  font-size: 0.95rem; font-weight: 800; color: #fff;
  letter-spacing: -0.3px; margin: 0;
}
.sb-logo-title span { color: var(--red); }
.sb-logo-sub {
  font-size: 0.63rem; color: var(--muted);
  margin: 3px 0 0; letter-spacing: 0.2px;
}

/* ─── NAV SECTION LABEL ──────────────────────────────────── */
.sb-section {
  padding: 16px 16px 4px;
  font-size: 0.58rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px;
  color: var(--dim);
}

/* ─── NAV BUTTON (Streamlit override) ───────────────────── */
section[data-testid="stSidebar"] .stButton > button {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  width: calc(100% - 16px) !important;
  margin: 1px 8px !important;
  padding: 8px 10px !important;
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: 7px !important;
  color: var(--muted) !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  text-align: left !important;
  letter-spacing: 0 !important;
  box-shadow: none !important;
  animation: none !important;
  transition: all 0.15s !important;
  justify-content: flex-start !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,0.05) !important;
  color: var(--text) !important;
  border-color: var(--border) !important;
  transform: none !important;
}

/* ─── GOLDEN RULE ────────────────────────────────────────── */
.golden {
  margin: 12px 10px;
  padding: 10px 12px;
  background: rgba(210,153,34,0.06);
  border: 1px solid rgba(210,153,34,0.18);
  border-radius: 8px;
}
.golden p { margin: 0; color: #c9a227; font-size: 0.72rem; line-height: 1.7; }

/* ─── MAIN CONTENT WRAPPER ───────────────────────────────── */
.main-wrap {
  padding: 24px 28px 48px;
  min-height: 100vh;
}

/* ─── PAGE HEADER ────────────────────────────────────────── */
.page-header { margin-bottom: 22px; }
.page-header h1 {
  font-size: 1.35rem; font-weight: 800; color: #fff;
  margin: 0 0 4px; letter-spacing: -0.5px;
}
.page-header p {
  font-size: 0.78rem; color: var(--muted); margin: 0;
}

/* ─── METRIC CARDS ───────────────────────────────────────── */
.mc {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 16px;
  transition: border-color 0.15s;
}
.mc:hover { border-color: var(--border2); }
.mc-label {
  font-size: 0.63rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 1px;
  color: var(--muted); margin: 0 0 6px;
}
.mc-value {
  font-size: 1.45rem; font-weight: 800;
  color: #fff; margin: 0; letter-spacing: -1px;
}
.mc-sub { font-size: 0.67rem; color: var(--muted); margin: 3px 0 0; }

/* ─── ANALYSE CARD ───────────────────────────────────────── */
.product-banner {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 18px;
  display: flex; align-items: center;
  justify-content: space-between;
  flex-wrap: wrap; gap: 10px;
  margin: 16px 0;
}
.pb-left h2 { font-size: 1.1rem; font-weight: 800; color: #fff; margin: 0 0 3px; }
.pb-left p  { font-size: 0.72rem; color: var(--muted); margin: 0; }
.pb-score   { text-align: center; }
.pb-score .score-num {
  font-size: 2.4rem; font-weight: 900; color: #fff;
  line-height: 1; letter-spacing: -2px;
}
.pb-score .score-denom { font-size: 0.68rem; color: var(--muted); }

/* ─── SCORE CIRCLE ───────────────────────────────────────── */
.score-circle {
  width: 100px; height: 100px; border-radius: 50%;
  border: 3px solid var(--red);
  background: var(--bg2);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  box-shadow: 0 0 28px rgba(232,25,44,0.2);
  margin: 0 auto 8px;
}
.score-circle .sn { font-size: 2rem; font-weight: 900; color: #fff; line-height: 1; }
.score-circle .sd { font-size: 0.6rem; color: var(--muted); }

/* ─── CRITERE ROWS ───────────────────────────────────────── */
.crit {
  display: flex; align-items: center; gap: 10px;
  padding: 7px 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.crit-note {
  min-width: 32px; height: 24px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 5px; font-weight: 800; font-size: 0.82rem;
}
.crit-name { font-size: 0.78rem; font-weight: 600; color: var(--text); }
.crit-desc { font-size: 0.67rem; color: var(--muted); }
.crit-poids { font-size: 0.62rem; color: var(--dim); }

/* ─── SECTION DIVIDER ────────────────────────────────────── */
.sdiv {
  display: flex; align-items: center; gap: 10px;
  margin: 20px 0 12px;
}
.sdiv-label {
  font-size: 0.63rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px;
  color: var(--muted); white-space: nowrap;
}
.sdiv-line {
  flex: 1; height: 1px;
  background: var(--border);
}

/* ─── CONTENT CARDS (affichage propre, UNE SEULE FOIS) ───── */
.content-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
  transition: border-color 0.15s;
}
.content-card:hover { border-color: var(--border2); }
.cc-tag {
  font-size: 0.6rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.2px;
  color: var(--muted); margin: 0 0 6px;
}
.cc-title { font-size: 0.9rem; font-weight: 700; color: #fff; margin: 0 0 5px; }
.cc-body  { font-size: 0.83rem; color: #bcc3cd; line-height: 1.75; margin: 0; white-space: pre-wrap; }

/* ─── AD CARD ────────────────────────────────────────────── */
.ad-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--red);
  border-radius: 0 10px 10px 0;
  padding: 14px 16px;
  margin-bottom: 10px;
}
.ad-accroche { font-size: 0.95rem; font-weight: 800; color: #f0883e; margin: 0 0 8px; }
.ad-body     { font-size: 0.84rem; color: #bcc3cd; line-height: 1.8; margin: 0; white-space: pre-wrap; }

/* ─── SCRIPT CARD ────────────────────────────────────────── */
.script-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-top: 2px solid var(--red);
  border-radius: 0 0 10px 10px;
  padding: 14px 16px;
  margin-bottom: 12px;
}
.script-tag   { font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: var(--red); margin: 0 0 8px; }
.script-body  { font-size: 0.85rem; color: #c9d1d9; line-height: 2.0; margin: 0; white-space: pre-wrap; }
.script-wc-ok   { color: #2ea043; font-size: 0.68rem; font-weight: 700; }
.script-wc-warn { color: #f0883e; font-size: 0.68rem; font-weight: 700; }

/* ─── SHOPIFY PARA ────────────────────────────────────────── */
.spara {
  border-left: 3px solid var(--red);
  background: var(--bg2);
  border-radius: 0 10px 10px 0;
  padding: 12px 16px;
  margin-bottom: 8px;
}
.spara-t { color: var(--red); font-weight: 800; font-size: 0.9rem; margin: 0 0 6px; }
.spara-b { color: #bcc3cd; font-size: 0.84rem; line-height: 1.85; margin: 0; white-space: pre-wrap; }

/* ─── OFFRE CARD ─────────────────────────────────────────── */
.offre-card {
  background: var(--bg2);
  border: 1px solid rgba(46,160,67,0.2);
  border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
}
.offre-nom  { color: #3fb950; font-weight: 800; font-size: 0.9rem; margin: 0 0 5px; }
.offre-desc { color: #bcc3cd; font-size: 0.82rem; line-height: 1.7; margin: 0 0 6px; }
.offre-prix { color: #56d364; font-size: 0.75rem; font-weight: 700; margin: 0; }

/* ─── JOUR CARD (plan 7j) ────────────────────────────────── */
.jour-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 16px; margin-bottom: 8px;
}
.jour-num-badge {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: 50%;
  font-weight: 800; font-size: 0.78rem; margin-bottom: 8px;
}
.jour-titre { color: #fff; font-weight: 700; font-size: 0.88rem; margin: 0 0 8px; }
.jour-item  { display: flex; gap: 8px; margin-bottom: 4px; }
.jour-lbl   { color: var(--muted); font-size: 0.68rem; min-width: 64px; flex-shrink: 0; }
.jour-val   { color: var(--text); font-size: 0.78rem; }

/* ─── TEMOIGNAGE ─────────────────────────────────────────── */
.temo-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 16px; margin-bottom: 8px;
}
.temo-head  { display: flex; gap: 12px; align-items: center; margin-bottom: 8px; }
.temo-av    {
  width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg,var(--red),#ff6b35);
  display: flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 1rem; color: #fff;
}
.temo-name  { color: #fff; font-weight: 700; font-size: 0.85rem; margin: 0; }
.temo-ville { color: var(--muted); font-size: 0.68rem; margin: 0; }
.temo-stars { color: #f0883e; font-size: 0.72rem; }
.temo-body  { color: #bcc3cd; font-size: 0.83rem; line-height: 1.75; font-style: italic; margin: 0; }

/* ─── BADGES ─────────────────────────────────────────────── */
.badge {
  display: inline-block; border-radius: 5px;
  padding: 2px 8px; font-size: 0.65rem; font-weight: 700;
}
.badge-red  { background:var(--red2); color:var(--red); border:1px solid var(--red3); }
.badge-grn  { background:var(--green2); color:#3fb950; border:1px solid rgba(46,160,67,0.3); }
.badge-blue { background:var(--blue2); color:var(--blue); border:1px solid rgba(68,147,248,0.25); }
.badge-org  { background:rgba(210,153,34,0.12); color:#d29922; border:1px solid rgba(210,153,34,0.25); }

/* ─── TAGS (mots-clés) ───────────────────────────────────── */
.tag {
  display: inline-block; background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: 20px; padding: 3px 10px;
  font-size: 0.7rem; color: var(--muted);
  margin: 2px;
}

/* ─── COPY BOX (unique, sans doublon) ───────────────────── */
.copy-box {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  font-family: 'SF Mono','Fira Code',monospace;
  font-size: 0.78rem; color: #c9d1d9;
  line-height: 1.7; white-space: pre-wrap;
  max-height: 220px; overflow-y: auto;
  margin: 6px 0 4px;
}

/* ─── INPUTS ─────────────────────────────────────────────── */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
  background: var(--bg2) !important; color: var(--text) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important; font-size: 0.85rem !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
  border-color: var(--red) !important;
  box-shadow: 0 0 0 3px rgba(232,25,44,0.1) !important;
}
.stSelectbox > div > div {
  background: var(--bg2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
}
.stSlider > div { color: var(--text) !important; }

/* ─── BOUTON PRINCIPAL ───────────────────────────────────── */
.main-content .stButton > button {
  background: var(--red) !important;
  color: #fff !important; border: none !important;
  border-radius: 8px !important; font-weight: 700 !important;
  font-size: 0.85rem !important; letter-spacing: 0.3px !important;
  padding: 10px 20px !important;
  box-shadow: 0 2px 12px rgba(232,25,44,0.35) !important;
  transition: all 0.2s !important;
  animation: none !important;
}
.main-content .stButton > button:hover {
  background: #c41224 !important;
  box-shadow: 0 4px 20px rgba(232,25,44,0.5) !important;
  transform: translateY(-1px) !important;
}

/* ─── TABS ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg2); border-radius: 9px; padding: 4px;
  gap: 2px; border: 1px solid var(--border); flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--muted) !important;
  border-radius: 6px !important; font-weight: 600 !important;
  font-size: clamp(0.62rem, 1.6vw, 0.78rem) !important;
  padding: 6px 11px !important; transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--red) !important; color: #fff !important;
  box-shadow: 0 2px 10px rgba(232,25,44,0.35) !important;
}
.stTabs [data-baseweb="tab"]:focus-visible { outline: none !important; }
[data-baseweb="tab-highlight"] { display: none !important; }

/* ─── ST.CODE ────────────────────────────────────────────── */
[data-testid="stCode"] pre, .stCodeBlock pre, pre {
  background: var(--bg3) !important;
  color: #c9d1d9 !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  font-size: 0.78rem !important;
}
[data-testid="stCode"] button {
  background: var(--red) !important; color: #fff !important;
  border-radius: 5px !important; opacity: 1 !important;
}

/* ─── ALERTE RIGUEUR ─────────────────────────────────────── */
.alerte-rigueur {
  background: rgba(232,25,44,0.07);
  border: 1px solid rgba(232,25,44,0.3);
  border-radius: 8px; padding: 8px 12px; margin-top: 8px;
}
.alerte-rigueur p { color: #ff6b6b; font-size: 0.75rem; font-weight: 700; margin: 0; }

/* ─── GAINS TABLE ────────────────────────────────────────── */
.gt { width:100%; border-collapse:collapse; font-size:0.8rem; }
.gt th {
  background: var(--bg3); color: var(--muted);
  padding: 8px 12px; font-size: 0.62rem; text-transform: uppercase;
  letter-spacing: 0.8px; border-bottom: 1px solid var(--border);
  text-align: right;
}
.gt th:first-child { text-align: left; }
.gt td {
  padding: 8px 12px; text-align: right;
  border-bottom: 1px solid rgba(255,255,255,0.03); color: #bcc3cd;
}
.gt td:first-child { text-align: left; color: var(--text); font-weight: 600; }
.gt tr:hover td { background: var(--bg3); }
.gt .pos { color: #3fb950; font-weight: 700; }
.gt .neg { color: #f85149; font-weight: 700; }
.gt .hl td { border-left: 2px solid var(--red); }

/* ─── LISTE PEURS/DESIRS ─────────────────────────────────── */
.list-item {
  padding: 6px 10px 6px 14px;
  border-left: 2px solid;
  margin-bottom: 4px;
  font-size: 0.8rem; color: #bcc3cd;
  background: var(--bg2); border-radius: 0 6px 6px 0;
}

/* ─── PAYS CARD ──────────────────────────────────────────── */
.pays-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 10px;
  text-align: center; cursor: pointer;
  transition: all 0.15s; text-decoration: none;
  display: block;
}
.pays-card:hover {
  border-color: var(--red);
  background: var(--red2);
  transform: translateY(-2px);
}
.pays-flag { font-size: 1.8rem; margin-bottom: 5px; }
.pays-nom  { color: #fff; font-weight: 700; font-size: 0.78rem; margin: 0; }
.pays-sub  { color: var(--muted); font-size: 0.62rem; margin: 2px 0 0; }

/* ─── BUDGET CARD ────────────────────────────────────────── */
.budget-tip {
  background: rgba(68,147,248,0.06);
  border: 1px solid rgba(68,147,248,0.15);
  border-radius: 9px; padding: 12px 14px;
}
.budget-tip p { color: #4493f8; font-size: 0.77rem; margin: 0; line-height: 1.75; }

/* ─── COMPARATEUR BARRE ──────────────────────────────────── */
.comp-bar-wrap { margin-bottom: 8px; }
.comp-bar-header {
  display: flex; justify-content: space-between;
  margin-bottom: 4px;
}
.comp-bar-label { font-size: 0.72rem; color: var(--muted); }
.comp-bar-val   { font-size: 0.72rem; font-weight: 700; }
.comp-bar-track {
  height: 5px; background: var(--bg3);
  border-radius: 3px; overflow: hidden;
}
.comp-bar-fill  { height: 100%; border-radius: 3px; }

/* ─── IMG CARD ───────────────────────────────────────────── */
.img-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 9px; overflow: hidden;
  transition: border-color 0.15s;
}
.img-card:hover { border-color: var(--border2); }
.img-footer { padding: 8px 10px; }
.img-footer p { color: var(--muted); font-size: 0.65rem; margin: 0 0 6px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.img-dl {
  display: block; text-align: center;
  background: var(--red); color: #fff !important;
  border-radius: 6px; padding: 6px 0;
  font-weight: 700; font-size: 0.72rem;
  text-decoration: none !important;
  transition: background 0.15s;
}
.img-dl:hover { background: #c41224; }

/* ─── MISC ───────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
label { color: var(--muted) !important; font-weight: 500 !important; font-size: 0.78rem !important; }
hr { border-color: var(--border) !important; margin: 16px 0 !important; }
.stAlert { border-radius: 8px !important; font-size: 0.82rem !important; }

@media (max-width: 768px) {
  .main-wrap { padding: 14px 12px 40px; }
  .mc-value { font-size: 1.1rem; }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# HELPERS UI — SANS DOUBLONS
# ══════════════════════════════════════════════════════════════════════
def sdiv(label):
    st.markdown(f'<div class="sdiv"><span class="sdiv-label">{label}</span><div class="sdiv-line"></div></div>', unsafe_allow_html=True)

def copy_block(text: str):
    """Affiche le texte UNE SEULE FOIS dans un st.code copiable."""
    st.code(text, language=None)

def content_card(tag, title, body):
    """Carte d'affichage + copy_block en dessous (pas de doublon HTML)."""
    st.markdown(f"""<div class="content-card">
      <p class="cc-tag">{tag}</p>
      <p class="cc-title">{title}</p>
      <p class="cc-body">{body.replace(chr(10),"<br>")}</p>
    </div>""", unsafe_allow_html=True)
    copy_block(body)

def badge(text, cls="badge-red"):
    return f'<span class="badge {cls}">{text}</span>'

# ══════════════════════════════════════════════════════════════════════
# MÉTIER
# ══════════════════════════════════════════════════════════════════════
def get_pub_budget(v):
    if v <= 10:   return "5$–7$/j"
    elif v <= 20: return "7$–10$/j"
    else:         return "15$–20$/j"

def calc_rentabilite(ventes, prix_moyen, prix_achat):
    ca   = ventes * prix_moyen
    cp   = ventes * prix_achat
    ff   = ventes * 5000
    cg   = cp + ff
    bn   = ca - cg
    return ca, cp, ff, cg, bn

def calc_score_produit(prix_achat, prix_vente_moy, data):
    score_ia = int(data.get("score", 5))
    type_p   = data.get("type_produit", "wow")
    categ    = data.get("avatar", {}).get("categorie", "Autre")
    nb_des   = len(data.get("desirs", []))

    # C1 — Prix
    if prix_vente_moy <= 7000:    c1 = 10
    elif prix_vente_moy <= 10000: c1 = 9
    elif prix_vente_moy <= 15000: c1 = 7
    elif prix_vente_moy <= 22000: c1 = 5
    elif prix_vente_moy <= 35000: c1 = 3
    else:                         c1 = 1
    d1 = f"Prix {prix_vente_moy:,.0f} F — {'✅ Impulsif' if c1>=9 else '⚠️ Réfléchi' if c1>=6 else '🔴 Risqué'}"

    # C2 — WOW
    if type_p == "wow":
        c2 = 9; d2 = "WOW — effet visuel immédiat"
    else:
        kw  = " ".join(data.get("peurs",[]) + data.get("desirs",[])).lower()
        sd  = sum(1 for w in ["douleur","fatigue","insomnie","argent","poids","peau","cheveux"] if w in kw)
        c2  = 9 if sd>=3 else 7 if sd>=2 else 5 if sd>=1 else 3
        d2  = f"Problème-solution · {sd} douleurs quotidiennes"

    # C3 — Créatives
    cf = {"Domestique":9,"Beauté & Soins":9,"Santé":8,"Tech":8,"Mode":7,"Alimentation":7}
    c3 = min(10, cf.get(categ,6) + (1 if type_p=="wow" else 0))
    d3 = f"{categ} — {'✅ Facile à filmer' if c3>=8 else '⚠️ Moyen' if c3>=6 else '🔴 Difficile'}"

    # C4 — Rareté
    cr = {"Tech":8,"Santé":7,"Beauté & Soins":7,"Luxe":6,"Mode":4,"Alimentation":3}
    c4 = cr.get(categ,6)
    if score_ia>=8: c4 = min(10,c4+1)
    if score_ia<=4: c4 = max(1,c4-2)
    d4 = f"{'✅ Rare localement' if c4>=7 else '⚠️ Moyen' if c4>=5 else '🔴 Partout en marché'}"

    # C5 — Crédibilité
    c5 = 9 if score_ia>=8 and nb_des>=3 else 7 if score_ia>=7 else 5 if score_ia>=5 else 3
    d5 = f"IA {score_ia}/10 · {nb_des} désirs · {'✅ Crédible' if c5>=7 else '⚠️ Mitigé' if c5>=5 else '🔴 Douteux'}"

    raw    = c1*.30 + c2*.25 + c3*.20 + c4*.15 + c5*.10
    echecs = sum(1 for c in [c1,c2,c3,c4,c5] if c<=4)
    alerte = None
    if echecs >= 2:
        raw    = min(raw, 6.0)
        alerte = f"⚠️ {echecs} critères faibles — score plafonné à 6/10"

    return {
        "score_final": round(max(1.0, min(10.0, raw)), 1),
        "alerte":      alerte,
        "criteres": [
            {"nom":"💰 Prix & Accessibilité",   "note":c1,"desc":d1,"poids":"30%"},
            {"nom":"⚡ Utilité & Effet WOW",     "note":c2,"desc":d2,"poids":"25%"},
            {"nom":"🎬 Potentiel Créatives",     "note":c3,"desc":d3,"poids":"20%"},
            {"nom":"💎 Rareté Locale",           "note":c4,"desc":d4,"poids":"15%"},
            {"nom":"🛡️ Crédibilité",            "note":c5,"desc":d5,"poids":"10%"},
        ]
    }

def calc_budget_pub(obj_ventes, prix_vente, taux_conv_pct=2.0, prix_achat=0):
    cpm       = 0.80
    ctr       = 0.018
    taux_conv = max(taux_conv_pct / 100, 0.001)
    clics     = obj_ventes / taux_conv
    cpc       = cpm / (ctr * 1000)
    budget_j  = clics * cpc
    marge     = prix_vente - prix_achat - 5000
    return {
        "budget_j":  round(budget_j, 2),
        "budget_3j": round(budget_j * 3, 2),
        "budget_5j": round(budget_j * 5, 2),
        "cpc":       round(cpc, 3),
        "clics":     round(clics),
        "marge":     marge,
        "benef_j":   round(marge * obj_ventes - budget_j * 655, 0),
    }

def search_bing_images(query, max_results=10):
    results = []
    try:
        q   = urllib.parse.quote_plus(query)
        url = f"https://www.bing.com/images/search?q={q}&form=HDRSC2&first=1"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "fr-FR,fr;q=0.9",
        })
        html   = urllib.request.urlopen(req, timeout=12).read().decode("utf-8", errors="ignore")
        murls  = re.findall(r'"murl"\s*:\s*"(https?://[^"]+\.(?:jpg|jpeg|png|webp)[^"]*)"', html)
        thurls = re.findall(r'"turl"\s*:\s*"(https?://[^"]+)"', html)
        for i, m in enumerate(murls[:max_results]):
            results.append({"url": m, "thumb": thurls[i] if i < len(thurls) else m, "title": f"#{i+1}"})
    except Exception:
        pass
    return results

# ══════════════════════════════════════════════════════════════════════
# JSON REPAIR
# ══════════════════════════════════════════════════════════════════════
def repair_json(raw):
    raw = re.sub(r"^```(?:json)?\s*","",raw.strip())
    raw = re.sub(r"\s*```$","",raw).strip()
    try: return json.loads(raw)
    except: pass
    stack=[]; last=0; ins=False; esc=False
    for i,c in enumerate(raw):
        if esc: esc=False; continue
        if c=='\\' and ins: esc=True; continue
        if c=='"' and not esc: ins=not ins; continue
        if ins: continue
        if c in ('{','['): stack.append(c)
        elif c in ('}',']'):
            if stack: stack.pop(); last=i+1
    closing="".join('}' if b=='{' else ']' for b in reversed(stack))
    try: return json.loads(raw[:last]+closing)
    except: return {}

# ══════════════════════════════════════════════════════════════════════
# GROQ API
# ══════════════════════════════════════════════════════════════════════
def call_groq(prompt, images):
    from groq import Groq
    client  = Groq(api_key=st.secrets["GROQ_API_KEY"])
    content = []
    for img in images:
        b64 = base64.b64encode(img).decode()
        content.append({"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}})
    content.append({"type":"text","text":prompt})
    r = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role":"user","content":content}],
        max_tokens=8000, temperature=0.7,
    )
    return repair_json(r.choices[0].message.content.strip())

def test_groq():
    try:
        from groq import Groq
        key = st.secrets.get("GROQ_API_KEY","")
        if not key: return {"ok":False,"msg":"GROQ_API_KEY absent"}
        r = Groq(api_key=key).chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role":"user","content":"Réponds juste: OK"}],
            max_tokens=5,
        )
        return {"ok":True,"msg":f"✅ Groq connecté · {r.choices[0].message.content.strip()}"}
    except Exception as e:
        return {"ok":False,"msg":str(e)}

# ══════════════════════════════════════════════════════════════════════
# PROMPT — VERSION BÉTON (scripts 130-170 mots, Shopify 4 phrases)
# ══════════════════════════════════════════════════════════════════════
def build_prompt(name, pa, pmin, pmax):
    return f"""Tu es un expert en neuro-marketing et e-commerce pour l'Afrique Francophone (Togo, Sénégal, Côte d'Ivoire, Bénin).
Tout doit être adapté au contexte africain : Facebook, WhatsApp, argent mobile, noms africains.

PRODUIT : {name}
PRIX ACHAT : {pa:,} FCFA | PRIX DE VENTE : {pmin:,}–{pmax:,} FCFA

══════════════════════════════════
RÈGLES ABSOLUES — VIOLATION = RÉSULTAT NUL
══════════════════════════════════

① SCRIPTS VOIX-OFF — RÈGLE DE FER :
   → CHAQUE script = ENTRE 130 ET 170 MOTS. Compte les mots un par un.
   → 130 mots = environ 12 à 14 lignes de texte naturel.
   → Un script de 40 mots ou 60 mots = INTERDIT. REFUSÉ.
   → MISE EN PAGE : utilise \\n entre chaque phrase courte (1-2 phrases par ligne max).
   → Style : fluide, naturel, oral africain. Utilise des prénoms africains (Kofi, Amina, Moussa, Fatou, Kwame...).
   → STRUCTURE pour chaque script : Hook choc (2 lignes) → Problème/Situation (2-3 lignes) → Présentation produit (2-3 lignes) → Démonstration/Bénéfice (3-4 lignes) → Preuve sociale africaine (2 lignes) → CTA urgent (1-2 lignes).
   → EXEMPLE de longueur correcte (compte : 145 mots) :
     "8 personnes sur 10 se lèvent la nuit dans le noir.\\nEt le plus étonnant, c'est qu'elles pensent que c'est normal.\\nNormal de chercher l'interrupteur,\\nnormal d'avancer à tâtons dans sa propre maison.\\nMaintenant regarde ce qui se passe quand je pose le pied au sol.\\nLa lumière s'allume toute seule.\\nSans rien appuyer. Sans rien dire.\\nC'est la lampe détecteur de mouvement.\\nElle capte ta présence et illumine instantanément.\\nPas besoin de câble. Pas besoin d'électricien.\\nTu la poses, elle fonctionne.\\nKofi à Lomé l'a installée dans son couloir la semaine passée.\\nIl dit que sa femme lui a demandé d'en prendre deux autres.\\nAujourd'hui seulement, tu l'as à 8 000 francs livré chez toi.\\nClique sur le lien et commande maintenant.\\nLes stocks partent vite."

② SHOPIFY — PARAGRAPHES :
   → TITRE de chaque paragraphe = BÉNÉFICE CLIENT DIRECT. INTERDIT : "Découvrez...", "Pourquoi choisir..."
   → CHAQUE paragraphe = EXACTEMENT 4 phrases complètes (ni 2, ni 3, ni 5 — EXACTEMENT 4).
   → Chaque phrase séparée par \\n.

③ FACEBOOK ADS :
   → 3 variantes. Chaque variante = titre choc avec emoji + 5 lignes de texte séparées par \\n.

④ AVATAR : Prénom africain concret (Kofi, Amina...). Ville africaine. Profession réelle.

⑤ PLAN 7 JOURS : Actions concrètes et budgets réalistes pour marché africain.

⑥ TÉMOIGNAGES : 5 avis. Style oral africain authentique. Pas de style "magazine".

Réponds UNIQUEMENT avec du JSON valide. Rien avant, rien après.

{{
  "score": 7,
  "score_justification": "Analyse 2-3 phrases sur le potentiel africain",
  "type_produit": "wow",
  "ameliorations": ["amélioration concrète 1","amélioration 2","amélioration 3"],
  "public_cible": "Description très précise du client africain type",
  "peurs": ["peur africaine précise 1","peur 2","peur 3"],
  "desirs": ["désir africain concret 1","désir 2","désir 3"],
  "mots_cles": ["mot1","mot2","mot3","mot4","mot5"],
  "offres": [
    {{"nom":"Nom offre 1","description":"Contenu précis de l'offre","prix_suggere":"XXXX FCFA","argument":"Pourquoi ça convertit en Afrique"}},
    {{"nom":"Nom offre 2","description":"Contenu","prix_suggere":"XXXX FCFA","argument":"Argument"}},
    {{"nom":"Nom offre 3","description":"Contenu","prix_suggere":"XXXX FCFA","argument":"Argument"}}
  ],
  "facebook_ads": [
    {{"angle":"Émotionnel","accroche":"🔥 TITRE CHOC ICI","texte":"ligne 1 fun africain\\nligne 2 avec emoji\\nligne 3 preuve\\nligne 4 offre\\nligne 5 CTA urgent"}},
    {{"angle":"Preuve Sociale","accroche":"⭐ TITRE TÉMOIGNAGE","texte":"ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5"}},
    {{"angle":"Urgence","accroche":"⚠️ STOCK LIMITÉ","texte":"ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5"}}
  ],
  "shopify": {{
    "titres": [
      {{"angle":"Bénéfice Principal","titre":"Titre page produit magnétique 1"}},
      {{"angle":"Curiosité","titre":"Titre intriguant 2"}},
      {{"angle":"Urgence","titre":"Titre urgent 3"}}
    ],
    "paragraphes": [
      {{"titre":"Titre bénéfice §1 direct","texte":"Phrase 1 percutante.\\nPhrase 2 émotionnelle.\\nPhrase 3 avec preuve.\\nPhrase 4 CTA ou statut."}},
      {{"titre":"Titre bénéfice §2 direct","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §3 direct","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §4 direct","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §5 direct","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre":"Titre bénéfice §6 direct","texte":"Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}}
    ]
  }},
  "scripts": [
    {{"angle":"Script Émotionnel","texte_complet":"ENTRE 130 ET 170 MOTS — Hook\\nProblème\\nSolution\\nDémo\\nPreuve sociale africaine\\nCTA"}},
    {{"angle":"Script Bénéfice Direct","texte_complet":"ENTRE 130 ET 170 MOTS — angle bénéfice direct avec preuve africaine"}},
    {{"angle":"Script Urgence & Statut","texte_complet":"ENTRE 130 ET 170 MOTS — statut social et urgence africaine"}}
  ],
  "angles_marketing": [
    {{"angle":"Peur & Urgence","titre":"Titre court choc","accroche":"Phrase attaque directe africaine"}},
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
    "message_cle":"LA phrase exacte qui convainc immédiatement"
  }},
  "creatives": [
    {{"concept":"Concept 1","scene":"Description précise de la scène à filmer","message":"Message marketing","accroche_type":"WOW"}},
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
    {{"jour":2,"titre":"Premier test pub","action":"Action","budget":"5$","ciblage":"Ciblage","contenu":"Contenu"}},
    {{"jour":3,"titre":"Analyse résultats","action":"Action","budget":"5$","ciblage":"Ciblage affiné","contenu":"Contenu"}},
    {{"jour":4,"titre":"Optimisation","action":"Action","budget":"7$","ciblage":"Ciblage winner","contenu":"Contenu"}},
    {{"jour":5,"titre":"Scale progressif","action":"Action","budget":"10$","ciblage":"Ciblage","contenu":"Contenu"}},
    {{"jour":6,"titre":"Consolidation","action":"Action","budget":"10$","ciblage":"Retargeting","contenu":"Contenu"}},
    {{"jour":7,"titre":"Bilan & Décision","action":"Analyser KPIs et décider scale ou stop","budget":"Budget bilan","ciblage":"Lookalike si positif","contenu":"Contenu bilan"}}
  ],
  "temoignages": [
    {{"prenom":"Amina","ville":"Lomé","produit_utilise":"2 semaines","avis":"Témoignage naturel oral africain, 2-3 phrases concrètes, pas style magazine","note":5}},
    {{"prenom":"Kofi","ville":"Abidjan","produit_utilise":"1 mois","avis":"Témoignage 2","note":5}},
    {{"prenom":"Fatou","ville":"Dakar","produit_utilise":"3 semaines","avis":"Témoignage 3","note":5}},
    {{"prenom":"Moussa","ville":"Cotonou","produit_utilise":"2 mois","avis":"Témoignage 4","note":4}},
    {{"prenom":"Awa","ville":"Conakry","produit_utilise":"1 semaine","avis":"Témoignage 5","note":5}}
  ]
}}"""

def build_export(name, pa, pmin, pmax, data):
    sep = "=" * 55
    ls  = [sep, "  ECOMASTER LABO PRO — PACK MARKETING COMPLET",
           f"  Produit : {name}",
           f"  Prix achat : {pa:,} F | Vente : {pmin:,}–{pmax:,} FCFA",
           f"  Score LABO : {data.get('score','?')}/10 | Type : {data.get('type_produit','').upper()}",
           sep,"",
           "📊 STRATÉGIE", "-"*40,
           data.get("score_justification",""),
           "\nPublic cible :", data.get("public_cible",""),
           "\nPeurs :"] + [f"  - {p}" for p in data.get("peurs",[])] + \
          ["\nDésirs :"] + [f"  - {d}" for d in data.get("desirs",[])] + \
          ["","🎁 OFFRES", "-"*40]
    for i,o in enumerate(data.get("offres",[])):
        ls += [f"Offre {i+1} — {o.get('nom','')}",
               f"  {o.get('description','')} | Prix : {o.get('prix_suggere','')}",""]
    ls += ["","🛍️ SHOPIFY", "-"*40, "TITRES :"]
    for t in data.get("shopify",{}).get("titres",[]):
        ls.append(f"  [{t.get('angle','')}] {t.get('titre','')}")
    ls.append("\nFICHE PRODUIT :")
    for p in data.get("shopify",{}).get("paragraphes",[]):
        ls += [f"\n{p.get('titre','')}", p.get("texte","")]
    ls += ["","📣 FACEBOOK ADS", "-"*40]
    for i,ad in enumerate(data.get("facebook_ads",[])):
        ls += [f"--- Ad {i+1} [{ad.get('angle','')}] ---",
               f"TITRE : {ad.get('accroche','')}",ad.get("texte",""),""]
    ls += ["","🎙️ SCRIPTS VOIX-OFF", "-"*40]
    for i,s in enumerate(data.get("scripts",[])):
        ls += [f"--- Script {i+1} — {s.get('angle','')} ---",s.get("texte_complet",""),""]
    ls += ["","🗓️ PLAN 7 JOURS", "-"*40]
    for j in data.get("plan_7j",[]):
        ls += [f"Jour {j.get('jour','')} : {j.get('titre','')}",
               f"  Action : {j.get('action','')}",
               f"  Budget : {j.get('budget','')} | Ciblage : {j.get('ciblage','')}",
               f"  Contenu : {j.get('contenu','')}",""]
    ls += ["", sep, "  EcoMaster Labo Pro · by LABO", sep]
    return "\n".join(ls)


# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
PAGES = [
    ("analyse",     "🔬", "Analyser un produit"),
    ("images",      "🖼️", "Images Produit"),
    ("spy",         "🕵️", "Spy Concurrents"),
    ("budget",      "💰", "Budget Pub Intelligent"),
    ("comparateur", "⚖️", "Comparateur Produits"),
    ("temoignages", "💬", "Témoignages"),
]

with st.sidebar:
    st.markdown("""<div class="sb-logo">
      <p class="sb-logo-title">🚀 Eco<span>Master</span> Labo</p>
      <p class="sb-logo-sub">E-commerce Afrique Francophone · by LABO</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<p class="sb-section">Menu</p>', unsafe_allow_html=True)

    for pid, icon, label in PAGES:
        active = "✦ " if st.session_state["nav_page"] == pid else ""
        if st.button(f"{icon}  {active}{label}", key=f"nav_{pid}", use_container_width=True):
            st.session_state["nav_page"] = pid
            st.rerun()

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<p class="sb-section">Historique récent</p>', unsafe_allow_html=True)

    history = st.session_state["history"]
    if not history:
        st.markdown('<p style="color:#3d444d;font-size:0.72rem;padding:0 16px;">Aucune analyse</p>', unsafe_allow_html=True)
    else:
        if st.button("🗑️  Effacer l'historique", key="clear_hist", use_container_width=True):
            st.session_state["history"] = []
            write_history_file([])
        for i, h in enumerate(history[:6]):
            short = h["name"][:16] + ("…" if len(h["name"])>16 else "")
            sc    = h.get("score","?")
            if st.button(f"↩  {short} · {sc}/10", key=f"hist_{i}", use_container_width=True):
                st.session_state.update({
                    "result": h["data"], "analyzed": True,
                    "active_product": h["name"],
                    "active_price": h["prix_achat"],
                    "nav_page": "analyse",
                })
                st.rerun()

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown("""<div class="golden">
      <p>💡 <b>Règle d'or LABO</b><br>
      Budget test : <b>4$–7$/jour</b><br>
      Prix vente = achat + <b>8K–12K F</b><br>
      Frais fixes : <b>5 000 F/vente</b><br>
      <span style="color:#7d8590;font-size:0.65rem;">(2K livraison · 2K pub · 1K closing)</span></p>
    </div>""", unsafe_allow_html=True)

    with st.expander("🔌 Tester connexion Groq"):
        if st.button("Tester", key="tg", use_container_width=True):
            r = test_groq()
            (st.success if r["ok"] else st.error)(r["msg"])


# ══════════════════════════════════════════════════════════════════════
# CONTENU PRINCIPAL
# ══════════════════════════════════════════════════════════════════════
page = st.session_state["nav_page"]

with st.container():
    st.markdown('<div class="main-wrap main-content">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PAGE ANALYSE
    # ══════════════════════════════════════════════════════════
    if page == "analyse":
        st.markdown("""<div class="page-header">
          <h1>🔬 Analyser un produit</h1>
          <p>Analyse IA complète — Score LABO, Stratégie, Offres, Shopify, Facebook Ads, Scripts voix-off, Plan 7 jours</p>
        </div>""", unsafe_allow_html=True)

        # Formulaire
        f1, f2 = st.columns([3, 2], gap="large")
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
                tc = st.columns(3)
                for i,f in enumerate(uploaded_files[:3]):
                    with tc[i]: st.image(f, width=90)

        pmin    = purchase_price + 8000
        pmax    = purchase_price + 12000
        pmoy    = (pmin + pmax) / 2
        marge_n = pmin - purchase_price - 5000

        # Metric cards
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4, gap="small")
        with m1:
            st.markdown(f'<div class="mc"><p class="mc-label">Prix Min Conseillé</p><p class="mc-value">{pmin:,} F</p><p class="mc-sub">achat + 8 000 F</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="mc"><p class="mc-label">Prix Max Conseillé</p><p class="mc-value">{pmax:,} F</p><p class="mc-sub">achat + 12 000 F</p></div>', unsafe_allow_html=True)
        with m3:
            c_marge = "color:#2ea043" if marge_n>0 else "color:#f85149"
            st.markdown(f'<div class="mc"><p class="mc-label">Marge Nette Min</p><p class="mc-value" style="{c_marge}">{marge_n:,} F</p><p class="mc-sub">après frais 5 000 F</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="mc"><p class="mc-label">Budget Pub Estimé</p><p class="mc-value" style="color:#d29922;font-size:1.15rem;">{get_pub_budget(objectif_ventes)}</p><p class="mc-sub">pour {objectif_ventes} ventes/jour</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_analyse = st.button("⚡  LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

        if btn_analyse:
            if not product_name.strip():
                st.error("⚠️ Entre le nom du produit.")
            elif not uploaded_files:
                st.error("⚠️ Upload au moins une photo produit.")
            else:
                imgs = [f.read() for f in uploaded_files[:3]]
                with st.spinner("🧠 Analyse en cours… 15–25 secondes"):
                    try:
                        data = call_groq(build_prompt(product_name, purchase_price, pmin, pmax), imgs)
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
                        if "GROQ_API_KEY" in str(e):
                            st.info("🔑 Ajoute ta clé dans Streamlit Secrets : GROQ_API_KEY = \"gsk_...\"")

        # ── RÉSULTATS ──
        if st.session_state.get("analyzed") and st.session_state.get("result"):
            data   = st.session_state["result"]
            aname  = st.session_state.get("active_product","")
            aprice = st.session_state.get("active_price",5000)
            apmin  = aprice + 8000
            apmax  = aprice + 12000
            apmoy  = (apmin + apmax) / 2
            aventes = st.session_state.get("active_ventes",10)
            type_p  = data.get("type_produit","wow")
            sc_data = calc_score_produit(aprice, apmoy, data)

            # Bandeau produit analysé
            b_type = "⚡ WOW" if type_p=="wow" else "🎯 Problème-solution"
            b_cls  = "badge-red" if type_p=="wow" else "badge-blue"
            st.markdown(f"""<div class="product-banner">
              <div class="pb-left">
                <h2>{aname}</h2>
                <p>Achat : {aprice:,} F · Vente : {apmin:,}–{apmax:,} F · Frais fixes : 5 000 F/vente</p>
                <span style="margin-top:4px;display:inline-block;" class="badge {b_cls}">{b_type}</span>
              </div>
              <div class="pb-score">
                <p class="score-num">{sc_data['score_final']}</p>
                <p class="score-denom">/10 Score LABO</p>
              </div>
            </div>""", unsafe_allow_html=True)

            # Tabs
            tabs = st.tabs(["📊 Stratégie","🎁 Offres","🛍️ Shopify","📣 Facebook Ads",
                            "🎙️ Scripts","🎬 Créatives","🎯 Angles","👤 Avatar",
                            "🗓️ Plan 7J","📥 Export"])

            # ── TAB 1 STRATÉGIE ──
            with tabs[0]:
                c1, c2 = st.columns([1, 2], gap="large")
                with c1:
                    sdiv("Score LABO")
                    alerte = sc_data.get("alerte")
                    st.markdown(f'<div class="score-circle"><span class="sn">{sc_data["score_final"]}</span><span class="sd">/10</span></div>', unsafe_allow_html=True)
                    if alerte:
                        st.markdown(f'<div class="alerte-rigueur"><p>{alerte}</p></div>', unsafe_allow_html=True)

                with c2:
                    sdiv("5 Critères détaillés")
                    for cr in sc_data["criteres"]:
                        n = cr["note"]
                        c = "#2ea043" if n>=8 else "#d29922" if n>=6 else "#f85149"
                        st.markdown(f"""<div class="crit">
                          <div class="crit-note" style="background:{c}18;color:{c};">{n}</div>
                          <div style="flex:1">
                            <p class="crit-name">{cr['nom']} <span class="crit-poids">· {cr['poids']}</span></p>
                            <p class="crit-desc">{cr['desc']}</p>
                          </div>
                        </div>""", unsafe_allow_html=True)

                sdiv("Analyse IA — Justification")
                copy_block(data.get("score_justification",""))

                a1, a2 = st.columns(2, gap="medium")
                with a1:
                    sdiv("Public Cible")
                    copy_block(data.get("public_cible",""))
                    sdiv("😨 Peurs du Client")
                    for p in data.get("peurs",[]):
                        st.markdown(f'<div class="list-item" style="border-color:#f85149;">• {p}</div>', unsafe_allow_html=True)
                    copy_block("\n".join(f"• {p}" for p in data.get("peurs",[])))

                with a2:
                    sdiv("✨ Désirs du Client")
                    for d in data.get("desirs",[]):
                        st.markdown(f'<div class="list-item" style="border-color:#2ea043;">• {d}</div>', unsafe_allow_html=True)
                    copy_block("\n".join(f"• {d}" for d in data.get("desirs",[])))
                    sdiv("🔑 Mots-Clés")
                    tags_html = "".join(f'<span class="tag">{m}</span>' for m in data.get("mots_cles",[]))
                    st.markdown(f'<div style="margin-bottom:6px">{tags_html}</div>', unsafe_allow_html=True)
                    copy_block(" · ".join(data.get("mots_cles",[])))

                sdiv("💡 Améliorations Recommandées")
                for i,a in enumerate(data.get("ameliorations",[])):
                    st.markdown(f"""<div class="content-card" style="padding:10px 14px;margin-bottom:6px">
                      <span style="color:var(--red);font-size:0.72rem;font-weight:700">#{i+1} </span>
                      <span style="font-size:0.82rem;color:#bcc3cd">{a}</span>
                    </div>""", unsafe_allow_html=True)

                sdiv("📊 Tableau Rentabilité")
                rows = ""
                for v in [1, 3, 5, 10, 15, 20, 30, 50]:
                    ca,cp,ff,cg,bn = calc_rentabilite(v, apmoy, aprice)
                    cls = "pos" if bn>0 else "neg"
                    hl  = ' class="hl"' if v==aventes else ""
                    rows += f"<tr{hl}><td>{v} ventes</td><td>{ca:,.0f} F</td><td>{cp:,.0f} F</td><td>{ff:,.0f} F</td><td class='{cls}'>{bn:,.0f} F</td></tr>"
                st.markdown(f"""<table class="gt">
                  <tr><th>Ventes/j</th><th>CA</th><th>Produit</th><th>Frais fixes</th><th>Bénéf. net</th></tr>
                  {rows}
                </table>""", unsafe_allow_html=True)

            # ── TAB 2 OFFRES ──
            with tabs[1]:
                sdiv("🎁 3 Offres pour le Marché Africain")
                for i,o in enumerate(data.get("offres",[])):
                    txt = f"Offre {i+1} — {o.get('nom','')}\n{o.get('description','')}\nPrix : {o.get('prix_suggere','')}\nArgument : {o.get('argument','')}"
                    st.markdown(f"""<div class="offre-card">
                      <p class="offre-nom">🎁 Offre {i+1} — {o.get('nom','')}</p>
                      <p class="offre-desc">{o.get('description','')}</p>
                      <p class="offre-prix">💰 {o.get('prix_suggere','')} &nbsp;·&nbsp; {o.get('argument','')}</p>
                    </div>""", unsafe_allow_html=True)
                    copy_block(txt)

            # ── TAB 3 SHOPIFY ──
            with tabs[2]:
                shopify = data.get("shopify",{})
                sdiv("🏷️ 3 Titres Magnétiques de Page Produit")
                for i,t in enumerate(shopify.get("titres",[])):
                    st.markdown(f"""<div class="content-card">
                      <p class="cc-tag">{t.get('angle','')}</p>
                      <p class="cc-title">{t.get('titre','')}</p>
                    </div>""", unsafe_allow_html=True)
                    copy_block(t.get("titre",""))

                st.markdown("<hr>", unsafe_allow_html=True)
                sdiv("📝 Fiche Produit — 6 Paragraphes (Shopify)")
                for j,p in enumerate(shopify.get("paragraphes",[])):
                    txtp = p.get("texte","")
                    nb_phrases = len([l for l in txtp.split('\n') if l.strip()])
                    warn = "" if nb_phrases>=4 else f' <span style="color:#f85149;font-size:0.65rem;">⚠️ {nb_phrases} phrases seulement</span>'
                    st.markdown(f"""<div class="spara">
                      <p class="spara-t">§{j+1} — {p.get('titre','')}{warn}</p>
                      <p class="spara-b">{txtp.replace(chr(10),'<br>')}</p>
                    </div>""", unsafe_allow_html=True)
                    copy_block(f"{p.get('titre','')}\n\n{txtp}")

                sdiv("📦 Fiche complète à copier")
                all_shopify = "\n\n".join(f"{'='*40}\n{p.get('titre','')}\n{'='*40}\n{p.get('texte','')}" for p in shopify.get("paragraphes",[]))
                copy_block(all_shopify)

            # ── TAB 4 FACEBOOK ADS ──
            with tabs[3]:
                sdiv("📣 3 Variantes Facebook Ads")
                for i,ad in enumerate(data.get("facebook_ads",[])):
                    accroche = ad.get("accroche", ad.get("titre",""))
                    texte    = ad.get("texte", ad.get("text",""))
                    angle    = ad.get("angle",f"Variante {i+1}")
                    st.markdown(f"""<div class="ad-card">
                      <p style="color:var(--muted);font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:0 0 4px;">{angle}</p>
                      <p class="ad-accroche">{accroche}</p>
                      <p class="ad-body">{texte.replace(chr(10),'<br>')}</p>
                    </div>""", unsafe_allow_html=True)
                    copy_block(f"{accroche}\n\n{texte}")

            # ── TAB 5 SCRIPTS ──
            with tabs[4]:
                sdiv("🎙️ Scripts Voix-Off — 130 à 170 mots chacun")
                st.markdown('<p style="color:var(--muted);font-size:0.75rem;margin:0 0 14px;">Chaque script doit faire 130–170 mots. Le compteur te l\'indique.</p>', unsafe_allow_html=True)
                scripts = data.get("scripts",[])
                for i,s in enumerate(scripts):
                    txt = s.get("texte_complet", s.get("texte",""))
                    wc  = len(txt.split())
                    wc_ok = 125 <= wc <= 180
                    wc_cls = "script-wc-ok" if wc_ok else "script-wc-warn"
                    wc_msg = f"✅ {wc} mots — OK" if wc_ok else f"⚠️ {wc} mots — devrait être 130–170"
                    st.markdown(f"""<div style="border-top:2px solid var(--red);background:var(--bg2);
                      border-radius:0 0 10px 10px;padding:12px 16px;margin-bottom:12px;">
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <p class="script-tag">Script {i+1} — {s.get('angle','')}</p>
                        <span class="{wc_cls}">{wc_msg}</span>
                      </div>
                      <p class="script-body">{txt.replace(chr(10),'<br>')}</p>
                    </div>""", unsafe_allow_html=True)
                    copy_block(txt)

            # ── TAB 6 CRÉATIVES ──
            with tabs[5]:
                sdiv("🎬 4 Concepts Créatives Publicitaires")
                creatives = data.get("creatives",[])
                cr_icons  = ["🔴","🟠","🟡","🟢"]
                for i,cr in enumerate(creatives):
                    ic  = cr_icons[i] if i<4 else "🎬"
                    txt = f"Concept : {cr.get('concept','')}\nScène : {cr.get('scene','')}\nMessage : {cr.get('message','')}\nType d'accroche : {cr.get('accroche_type','')}"
                    st.markdown(f"""<div class="content-card">
                      <p class="cc-tag">{ic} Créative {i+1}</p>
                      <p class="cc-title">{cr.get('concept','')}</p>
                      <div style="margin-top:6px;display:grid;gap:4px;">
                        <p style="color:var(--muted);font-size:0.72rem;margin:0;">🎬 Scène : <span style="color:var(--text);">{cr.get('scene','')}</span></p>
                        <p style="color:var(--muted);font-size:0.72rem;margin:0;">💬 Message : <span style="color:var(--text);">{cr.get('message','')}</span></p>
                        <span class="badge badge-red" style="margin-top:2px;">{cr.get('accroche_type','')}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)
                    copy_block(txt)

            # ── TAB 7 ANGLES ──
            with tabs[6]:
                sdiv("🎯 5 Angles Marketing — Afrique Francophone")
                angles = data.get("angles_marketing",[])
                a_icons = ["🔴","🟠","🟡","🟢","🔵"]
                for i,ang in enumerate(angles):
                    ic  = a_icons[i] if i<5 else "🎯"
                    txt = f"{ang.get('titre','')}\n\n{ang.get('accroche','')}"
                    st.markdown(f"""<div class="content-card">
                      <p class="cc-tag">{ic} {ang.get('angle','')}</p>
                      <p class="cc-title">{ang.get('titre','')}</p>
                      <p class="cc-body">{ang.get('accroche','')}</p>
                    </div>""", unsafe_allow_html=True)
                    copy_block(txt)

            # ── TAB 8 AVATAR ──
            with tabs[7]:
                av = data.get("avatar",{})
                if av:
                    prenom = av.get("prenom_type","Le client type")
                    sdiv("👤 Persona Client Type")
                    st.markdown(f"""<div class="content-card" style="border-color:var(--red3);">
                      <div style="display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;">
                        <div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--red),#ff6b35);
                          display:flex;align-items:center;justify-content:center;
                          font-size:1.4rem;font-weight:900;color:#fff;flex-shrink:0;">{prenom[0].upper()}</div>
                        <div style="flex:1;">
                          <p style="color:#fff;font-weight:800;font-size:1.1rem;margin:0 0 4px;">{prenom}</p>
                          <p style="color:var(--muted);font-size:0.75rem;margin:0 0 8px;">
                            {av.get('sexe','—')} · {av.get('age','—')} · {av.get('ville','—')}
                          </p>
                          <div style="display:flex;gap:5px;flex-wrap:wrap;">
                            <span class="badge badge-red">{av.get('categorie','—')}</span>
                            <span class="badge badge-blue">{av.get('profession','—')}</span>
                            <span class="badge badge-org">{av.get('revenu','—')}</span>
                            <span class="badge badge-grn">Français {av.get('francais','—')}</span>
                          </div>
                          <p style="color:#bcc3cd;font-size:0.8rem;margin:8px 0 0;line-height:1.7;">{av.get('mode_vie','')}</p>
                        </div>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    av1, av2, av3 = st.columns(3, gap="small")
                    with av1:
                        sdiv("😤 Frustrations")
                        for f in av.get("frustrations",[]):
                            st.markdown(f'<div class="list-item" style="border-color:#f85149">• {f}</div>', unsafe_allow_html=True)
                    with av2:
                        sdiv("✨ Désirs")
                        for d in av.get("desirs",[]):
                            st.markdown(f'<div class="list-item" style="border-color:#2ea043">• {d}</div>', unsafe_allow_html=True)
                    with av3:
                        sdiv("🤔 Objections")
                        for o in av.get("objections",[]):
                            st.markdown(f'<div class="list-item" style="border-color:#d29922">• {o}</div>', unsafe_allow_html=True)

                    sdiv("💬 Message Clé qui Convainc")
                    msg = av.get("message_cle","")
                    st.markdown(f"""<div class="content-card" style="border-color:var(--red3);">
                      <p style="color:#fff;font-size:1rem;font-weight:700;font-style:italic;margin:0;">"{msg}"</p>
                    </div>""", unsafe_allow_html=True)
                    copy_block(msg)

            # ── TAB 9 PLAN 7 JOURS ──
            with tabs[8]:
                sdiv("🗓️ Plan de Lancement 7 Jours")
                plan = data.get("plan_7j",[])
                j_colors = ["#e8192c","#ff6b35","#d29922","#f0d060","#2ea043","#4493f8","#bc8cff"]
                for idx, jour in enumerate(plan):
                    c = j_colors[idx] if idx<7 else "#e8192c"
                    txt = f"Jour {jour.get('jour','')} — {jour.get('titre','')}\n\nAction : {jour.get('action','')}\nBudget pub : {jour.get('budget','')}\nCiblage : {jour.get('ciblage','')}\nContenu : {jour.get('contenu','')}"
                    st.markdown(f"""<div class="jour-card">
                      <div class="jour-num-badge" style="background:{c}18;color:{c};border:1px solid {c}40;">{jour.get('jour','')}</div>
                      <p class="jour-titre">{jour.get('titre','')}</p>
                      <div class="jour-item"><span class="jour-lbl">🎯 Action</span><span class="jour-val">{jour.get('action','')}</span></div>
                      <div class="jour-item"><span class="jour-lbl">💸 Budget</span><span class="jour-val" style="color:{c};font-weight:700;">{jour.get('budget','')}</span></div>
                      <div class="jour-item"><span class="jour-lbl">👥 Ciblage</span><span class="jour-val">{jour.get('ciblage','')}</span></div>
                      <div class="jour-item"><span class="jour-lbl">📝 Contenu</span><span class="jour-val">{jour.get('contenu','')}</span></div>
                    </div>""", unsafe_allow_html=True)
                    copy_block(txt)

            # ── TAB 10 EXPORT ──
            with tabs[9]:
                sdiv("📥 Pack Marketing Complet (.txt)")
                export = build_export(aname, aprice, apmin, apmax, data)
                st.download_button(
                    label="⬇️  TÉLÉCHARGER MON PACK MARKETING",
                    data=export,
                    file_name=f"labo_{aname.replace(' ','_')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)
                copy_block(export[:800] + "\n\n[...] Télécharge pour voir tout le contenu")

    # ══════════════════════════════════════════════════════════
    # PAGE IMAGES
    # ══════════════════════════════════════════════════════════
    elif page == "images":
        aname = st.session_state.get("active_product","")
        st.markdown("""<div class="page-header">
          <h1>🖼️ Images Produit</h1>
          <p>Images réelles affichées directement · Téléchargeables en 1 clic · Recherche multi-plateformes</p>
        </div>""", unsafe_allow_html=True)

        iq, ibtn = st.columns([5, 1], gap="small")
        with iq:
            sq = st.text_input("🔍 Nom du produit", value=aname or "",
                placeholder="Ex: beauty milk serum, solar lamp LED...", key="img_q")
        with ibtn:
            st.markdown("<br>", unsafe_allow_html=True)
            go = st.button("Chercher", use_container_width=True, key="img_go")

        if go and sq.strip():
            with st.spinner("🔍 Recherche d'images…"):
                imgs = search_bing_images(sq.strip(), 10)
                st.session_state["img_results"]    = imgs
                st.session_state["img_query_done"] = sq.strip()

        found = st.session_state.get("img_results",[])
        qdone = st.session_state.get("img_query_done","")

        if found:
            st.markdown(f'<p style="color:#2ea043;font-size:0.75rem;font-weight:700;margin:8px 0 14px;">✅ {len(found)} images trouvées pour « {qdone} »</p>', unsafe_allow_html=True)
            for row in range(0, len(found), 4):
                cols = st.columns(4, gap="small")
                for ci, img in enumerate(found[row:row+4]):
                    with cols[ci]:
                        st.markdown('<div class="img-card">', unsafe_allow_html=True)
                        try:
                            st.image(img["thumb"], use_column_width=True)
                        except:
                            st.image(img["url"], use_column_width=True)
                        st.markdown(f"""<div class="img-footer">
                          <p>{img.get('title','')}</p>
                          <a href="{img['url']}" target="_blank" class="img-dl">⬇️ Télécharger</a>
                        </div></div>""", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            sdiv("Chercher aussi sur ces plateformes")
            qe = urllib.parse.quote_plus(sq if sq else qdone)
            plats = [
                ("🛒 AliExpress",  f"https://fr.aliexpress.com/wholesale?SearchText={qe}"),
                ("🏭 Alibaba",     f"https://www.alibaba.com/trade/search?SearchText={qe}"),
                ("📌 Pinterest",   f"https://www.pinterest.com/search/pins/?q={qe}"),
                ("🛍️ Amazon",     f"https://www.amazon.fr/s?k={qe}"),
                ("🛒 Temu",        f"https://www.temu.com/search_result.html?search_key={qe}"),
            ]
            pc = st.columns(5, gap="small")
            for i,(pn,pu) in enumerate(plats):
                with pc[i]:
                    st.markdown(f'<a href="{pu}" target="_blank" style="display:block;text-align:center;background:var(--bg2);border:1px solid var(--border2);border-radius:8px;padding:10px 6px;color:var(--text);text-decoration:none;font-size:0.75rem;font-weight:600;transition:border-color .15s;">{pn}</a>', unsafe_allow_html=True)
        elif qdone:
            st.warning(f"⚠️ Aucune image pour « {qdone} ». Essaie en anglais.")
        else:
            st.markdown("""<div style="border:1px dashed rgba(255,255,255,0.08);border-radius:12px;
              padding:40px;text-align:center;margin-top:20px;">
              <p style="font-size:2rem;margin:0 0 10px;">🖼️</p>
              <p style="color:#484f58;font-size:0.85rem;margin:0 0 4px;font-weight:600;">Lance une recherche pour voir les images</p>
              <p style="color:#30363d;font-size:0.72rem;margin:0;">Les images s'affichent ici directement</p>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PAGE SPY
    # ══════════════════════════════════════════════════════════
    elif page == "spy":
        aname = st.session_state.get("active_product","")
        st.markdown("""<div class="page-header">
          <h1>🕵️ Spy Concurrents</h1>
          <p>Trouve qui vend déjà ton produit en Afrique — Publicités Facebook, Boutiques, Vidéos</p>
        </div>""", unsafe_allow_html=True)

        spy_q = st.text_input("📦 Produit à espionner", value=aname or "",
            placeholder="Ex: crème éclaircissante, lampe détecteur mouvement...")

        if spy_q.strip():
            qe = urllib.parse.quote_plus(spy_q.strip())

            PAYS = [
                ("🇹🇬","Togo","TG"),
                ("🇸🇳","Sénégal","SN"),
                ("🇨🇮","Côte d'Ivoire","CI"),
                ("🇧🇯","Bénin","BJ"),
                ("🇬🇳","Guinée-Conakry","GN"),
                ("🇨🇬","Congo","CG"),
            ]

            sdiv("📣 Publicités Facebook par Pays — Clique pour voir les pubs")
            pc = st.columns(3, gap="small")
            for i,(flag,nom,code) in enumerate(PAYS):
                with pc[i%3]:
                    fb_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={code}&q={qe}&search_type=keyword_unordered"
                    st.markdown(f"""<a href="{fb_url}" target="_blank" class="pays-card">
                      <p class="pays-flag">{flag}</p>
                      <p class="pays-nom">{nom}</p>
                      <p class="pays-sub">Voir pubs Facebook →</p>
                    </a>""", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            sdiv("🔍 Boutiques Concurrentes en Afrique")

            spy_links = [
                ("🌍 Google — Boutiques Afrique",
                 f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' Afrique acheter livraison')}"),
                ("🛒 Shopify Afrique",
                 f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' site:myshopify.com Afrique')}"),
                ("🇹🇬 Concurrents au Togo",
                 f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' Lomé Togo commander')}"),
                ("🇨🇮 Concurrents en Côte d'Ivoire",
                 f"https://www.google.com/search?q={urllib.parse.quote_plus(spy_q.strip()+' Abidjan commander')}"),
                ("📌 Créatives Pinterest Afrique",
                 f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote_plus(spy_q.strip()+' Afrique')}"),
                ("🎬 Vidéos TikTok",
                 f"https://www.tiktok.com/search?q={qe}"),
            ]
            sl = st.columns(2, gap="medium")
            for i,(label,url) in enumerate(spy_links):
                with sl[i%2]:
                    st.markdown(f"""<a href="{url}" target="_blank" style="text-decoration:none;">
                      <div class="content-card" style="cursor:pointer;margin-bottom:8px;">
                        <p class="cc-title">{label}</p>
                        <p class="cc-body" style="font-size:0.68rem;color:var(--muted);">{url[:55]}…</p>
                      </div>
                    </a>""", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            sdiv("🎬 Vidéos Concurrentes")
            vc = st.columns(2, gap="medium")
            with vc[0]:
                yt = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(spy_q.strip()+' publicité Afrique')}"
                st.markdown(f'<a href="{yt}" target="_blank" style="display:block;background:#FF0000;color:#fff;text-align:center;border-radius:8px;padding:12px;font-weight:700;font-size:0.8rem;text-decoration:none;">▶️ YouTube — Vidéos concurrentes</a>', unsafe_allow_html=True)
            with vc[1]:
                pv = f"https://www.pinterest.com/search/videos/?q={qe}"
                st.markdown(f'<a href="{pv}" target="_blank" style="display:block;background:#E60023;color:#fff;text-align:center;border-radius:8px;padding:12px;font-weight:700;font-size:0.8rem;text-decoration:none;">📌 Pinterest — Vidéos produit</a>', unsafe_allow_html=True)
        else:
            st.markdown("""<div style="border:1px dashed rgba(255,255,255,0.08);border-radius:12px;padding:40px;text-align:center;margin-top:20px;">
              <p style="font-size:2rem;margin:0 0 10px;">🕵️</p>
              <p style="color:#484f58;font-size:0.85rem;margin:0 0 4px;font-weight:600;">Entre un produit pour espionner</p>
              <p style="color:#30363d;font-size:0.72rem;margin:0;">Concurrents · Publicités Facebook · Boutiques · Vidéos</p>
            </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PAGE BUDGET
    # ══════════════════════════════════════════════════════════
    elif page == "budget":
        st.markdown("""<div class="page-header">
          <h1>💰 Calculateur Budget Pub Intelligent</h1>
          <p>Basé sur benchmarks réels Facebook Afrique — CPM 0.80$ · CTR 1.8% · Conversion 1–3%</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="budget-tip" style="margin-bottom:20px;">
          <p>📊 <b>Benchmarks Facebook Afrique Francophone 2024–2025</b><br>
          CPM moyen : <b>0.80$</b> · Coût par clic : <b>~0.044$</b> · Taux conversion e-com : <b>1–3%</b><br>
          Ces chiffres varient selon ton ciblage et ta créative. Utilise ce calculateur comme point de départ.</p>
        </div>""", unsafe_allow_html=True)

        bc1, bc2 = st.columns(2, gap="large")
        with bc1:
            pv_b = st.number_input("💰 Prix de vente (FCFA)", min_value=1000, step=500,
                value=int(st.session_state.get("active_price",5000))+10000)
            pa_b = st.number_input("🏷️ Prix d'achat (FCFA)", min_value=0, step=500,
                value=int(st.session_state.get("active_price",5000)))
        with bc2:
            obj_b = st.number_input("🎯 Objectif ventes/jour", min_value=1, step=1, value=5)
            tc_b  = st.slider("📊 Taux conversion estimé (%)", 0.5, 5.0, 2.0, 0.1,
                help="E-commerce Afrique : 1–3% en moyenne. Bon produit avec bonne créative = 2–3%.")

        res = calc_budget_pub(obj_b, pv_b, tc_b, pa_b)

        sdiv("Résultats")
        r1, r2, r3 = st.columns(3, gap="small")
        with r1:
            st.markdown(f'<div class="mc" style="border-color:var(--red3)"><p class="mc-label">Budget Quotidien</p><p class="mc-value" style="color:var(--red)">{res["budget_j"]:.2f}$</p><p class="mc-sub">≈ {res["budget_j"]*655:,.0f} FCFA</p></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="mc"><p class="mc-label">Budget Test 3 jours</p><p class="mc-value" style="color:#d29922">{res["budget_3j"]:.2f}$</p><p class="mc-sub">≈ {res["budget_3j"]*655:,.0f} FCFA</p></div>', unsafe_allow_html=True)
        with r3:
            st.markdown(f'<div class="mc"><p class="mc-label">Budget Test 5 jours</p><p class="mc-value" style="color:#4493f8">{res["budget_5j"]:.2f}$</p><p class="mc-sub">≈ {res["budget_5j"]*655:,.0f} FCFA</p></div>', unsafe_allow_html=True)

        r4, r5, r6 = st.columns(3, gap="small")
        with r4:
            st.markdown(f'<div class="mc"><p class="mc-label">CPC Estimé</p><p class="mc-value" style="color:#bc8cff">{res["cpc"]:.3f}$</p><p class="mc-sub">coût par clic moyen</p></div>', unsafe_allow_html=True)
        with r5:
            st.markdown(f'<div class="mc"><p class="mc-label">Clics Nécessaires</p><p class="mc-value">{res["clics"]}</p><p class="mc-sub">pour {obj_b} ventes à {tc_b}%</p></div>', unsafe_allow_html=True)
        with r6:
            bc = "#2ea043" if res["benef_j"]>0 else "#f85149"
            st.markdown(f'<div class="mc"><p class="mc-label">Bénéfice Net/Jour estimé</p><p class="mc-value" style="color:{bc}">{res["benef_j"]:,.0f} F</p><p class="mc-sub">CA − achat − frais − pub</p></div>', unsafe_allow_html=True)

        st.markdown("""<div class="budget-tip" style="margin-top:16px;">
          <p>💡 <b>Conseil LABO :</b> Démarre toujours avec le budget minimum 3–5 jours.
          Si tu fais des ventes et ROAS &gt; 2 → double le budget.
          Si 0 vente après 3 jours → change la créative en premier, pas le ciblage.</p>
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PAGE COMPARATEUR
    # ══════════════════════════════════════════════════════════
    elif page == "comparateur":
        st.markdown("""<div class="page-header">
          <h1>⚖️ Comparateur de Produits</h1>
          <p>Compare 2 produits selon les 5 critères LABO · Choisis le gagnant avant d'investir</p>
        </div>""", unsafe_allow_html=True)

        CATS = ["Domestique","Beauté & Soins","Santé","Tech","Mode","Alimentation","Luxe","Agriculture","Élevage","Pêche","Autre"]

        cc1, cc2 = st.columns(2, gap="large")
        with cc1:
            st.markdown('<p style="color:var(--red);font-weight:700;font-size:0.88rem;margin-bottom:8px;">🅰️ Produit 1</p>', unsafe_allow_html=True)
            p1n = st.text_input("Nom", key="p1n", placeholder="Ex: Crème Beauty Milk")
            p1a = st.number_input("Prix achat (FCFA)", min_value=0, step=500, key="p1a", value=5000)
            p1v = st.number_input("Prix vente (FCFA)", min_value=0, step=500, key="p1v", value=15000)
            p1t = st.selectbox("Type", ["wow","probleme_solution"], key="p1t")
            p1c = st.selectbox("Catégorie", CATS, key="p1c")
        with cc2:
            st.markdown('<p style="color:#4493f8;font-weight:700;font-size:0.88rem;margin-bottom:8px;">🅱️ Produit 2</p>', unsafe_allow_html=True)
            p2n = st.text_input("Nom", key="p2n", placeholder="Ex: Lampe solaire LED")
            p2a = st.number_input("Prix achat (FCFA)", min_value=0, step=500, key="p2a", value=3000)
            p2v = st.number_input("Prix vente (FCFA)", min_value=0, step=500, key="p2v", value=12000)
            p2t = st.selectbox("Type", ["wow","probleme_solution"], key="p2t")
            p2c = st.selectbox("Catégorie", CATS, key="p2c")

        if st.button("⚖️  COMPARER LES 2 PRODUITS", use_container_width=True):
            def mk(tp,cat): return {"score":7,"type_produit":tp,"avatar":{"categorie":cat},"peurs":["a","b","c"],"desirs":["a","b","c"]}
            s1 = calc_score_produit(p1a, p1v, mk(p1t,p1c))
            s2 = calc_score_produit(p2a, p2v, mk(p2t,p2c))
            win = "A" if s1["score_final"] >= s2["score_final"] else "B"

            sdiv("⚖️ Résultats de Comparaison")
            rc1, rc2 = st.columns(2, gap="large")
            for col, s, nom, ac, vte, side, col_acc in [
                (rc1, s1, p1n or "Produit 1", p1a, p1v, "A", "#e8192c"),
                (rc2, s2, p2n or "Produit 2", p2a, p2v, "B", "#4493f8"),
            ]:
                with col:
                    is_w = win == side
                    bg   = "border-color:rgba(46,160,67,0.35);background:rgba(46,160,67,0.04);" if is_w else ""
                    st.markdown(f'<div class="content-card" style="{bg}">', unsafe_allow_html=True)
                    if is_w:
                        st.markdown('<span class="badge badge-grn" style="margin-bottom:8px;display:inline-block;">🏆 MEILLEUR CHOIX</span>', unsafe_allow_html=True)
                    st.markdown(f"""<p style="color:{col_acc};font-weight:800;font-size:1.15rem;margin:0 0 4px;">{nom}</p>
                    <p style="color:var(--muted);font-size:0.72rem;margin:0 0 12px;">
                      Achat {ac:,} F · Vente {vte:,} F · Marge {vte-ac-5000:,} F
                    </p>
                    <p style="color:#fff;font-size:2.2rem;font-weight:900;margin:0 0 2px;line-height:1;">{s['score_final']}<span style="font-size:0.9rem;color:var(--muted);font-weight:400;"> /10</span></p>""", unsafe_allow_html=True)

                    for cr in s["criteres"]:
                        n   = cr["note"]
                        c   = "#2ea043" if n>=8 else "#d29922" if n>=6 else "#f85149"
                        pct = int(n/10*100)
                        st.markdown(f"""<div class="comp-bar-wrap">
                          <div class="comp-bar-header">
                            <span class="comp-bar-label">{cr['nom']}</span>
                            <span class="comp-bar-val" style="color:{c}">{n}/10</span>
                          </div>
                          <div class="comp-bar-track">
                            <div class="comp-bar-fill" style="width:{pct}%;background:{c}"></div>
                          </div>
                        </div>""", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PAGE TÉMOIGNAGES
    # ══════════════════════════════════════════════════════════
    elif page == "temoignages":
        st.markdown("""<div class="page-header">
          <h1>💬 Témoignages Clients Africains</h1>
          <p>Générés par l'IA · Style oral africain authentique · Prêts à coller sur ta page Shopify</p>
        </div>""", unsafe_allow_html=True)

        data = st.session_state.get("result")
        if not data:
            st.info("⚠️ Lance d'abord une analyse produit (page 🔬 Analyser) pour générer les témoignages.")
        else:
            aname = st.session_state.get("active_product","le produit")
            temos = data.get("temoignages",[])

            if not temos:
                st.warning("⚠️ Témoignages non générés. Relance une analyse complète.")
            else:
                st.markdown(f'<p style="color:var(--muted);font-size:0.78rem;margin:0 0 16px;">5 témoignages africains pour <b style="color:#fff;">{aname}</b></p>', unsafe_allow_html=True)

                for t in temos:
                    prenom = t.get("prenom","Client")
                    ville  = t.get("ville","Afrique")
                    duree  = t.get("produit_utilise","")
                    avis   = t.get("avis","")
                    note   = int(t.get("note",5))
                    init   = prenom[0].upper() if prenom else "C"
                    stars  = "★"*note + "☆"*(5-note)

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
                    copy_block(f'"{avis}"\n— {prenom}, {ville} ({duree}) {stars}')

                st.markdown("<hr>", unsafe_allow_html=True)
                sdiv("📦 Tous les témoignages à copier")
                all_t = "\n\n---\n\n".join(
                    f'"{t.get("avis","")}" — {t.get("prenom","")}, {t.get("ville","")} ({t.get("produit_utilise","")}) {"★"*int(t.get("note",5))}'
                    for t in temos
                )
                copy_block(all_t)

    st.markdown("</div>", unsafe_allow_html=True)
