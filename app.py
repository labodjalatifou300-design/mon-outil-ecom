import streamlit as st
import os
import io
import re
import json
from PIL import Image
import base64
from datetime import datetime

# ── INIT SESSION STATE (avant tout) ──────────────────────────────────────────
# ── HISTORIQUE PERSISTANT — fichier JSON sur disque ──────────────
HISTORY_FILE = "/tmp/labo_history.json"  # /tmp = toujours accessible sur Streamlit Cloud

def load_history_file():
    """Charge l'historique depuis le fichier JSON (survit aux rechargements)."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def write_history_file(history):
    """Sauvegarde l'historique dans le fichier JSON."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

if "history"         not in st.session_state:
    st.session_state["history"]         = load_history_file()  # ← chargé depuis disque
if "result"          not in st.session_state: st.session_state["result"]          = None
if "analyzed"        not in st.session_state: st.session_state["analyzed"]        = False
if "active_product"  not in st.session_state: st.session_state["active_product"]  = ""
if "active_price"    not in st.session_state: st.session_state["active_price"]    = 5000
if "active_ventes"   not in st.session_state: st.session_state["active_ventes"]   = 10
if "load_history"    not in st.session_state: st.session_state["load_history"]    = None

st.set_page_config(
    page_title="EcoMaster Labo Pro",
    page_icon="🚀",
    layout="wide",
)

# ── INJECTION META DARK MODE (mobile Safari + Chrome) ──────────────
st.markdown("""
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0d1117">
""", unsafe_allow_html=True)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

  /* ══════ DARK MODE FORCÉ — TOUS APPAREILS ══════ */
  :root {
    color-scheme: dark !important;
    --red:      #D90429;
    --red-dim:  rgba(217,4,41,0.15);
    --red-glow: rgba(217,4,41,0.5);
    --bg:       #0d1117;
    --bg2:      #161b22;
    --bg3:      #1c2333;
    --border:   rgba(255,255,255,0.07);
    --text:     #F0F0F0;
    --muted:    #6e7681;
  }
  html, body, [class*="css"], [data-testid], .stApp,
  .appview-container, .appview-container > section,
  .block-container, .main {
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
  }
  @media (prefers-color-scheme: light) {
    html, body, div, section, header, footer, aside,
    .stApp, .main, .block-container, .appview-container,
    .appview-container > section, [class*="css"], [data-testid],
    [data-testid="stAppViewContainer"], [data-testid="stHeader"],
    [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
      background-color: #0d1117 !important;
      color: #F0F0F0 !important;
    }
  }

  /* ══════ ANIMATIONS PREMIUM ══════ */
  @keyframes fadeInDown  { from{opacity:0;transform:translateY(-30px) scale(0.97)} to{opacity:1;transform:translateY(0) scale(1)} }
  @keyframes fadeInUp    { from{opacity:0;transform:translateY(24px)}  to{opacity:1;transform:translateY(0)} }
  @keyframes fadeInLeft  { from{opacity:0;transform:translateX(-24px)} to{opacity:1;transform:translateX(0)} }
  @keyframes fadeInRight { from{opacity:0;transform:translateX(24px)}  to{opacity:1;transform:translateX(0)} }
  @keyframes scaleIn     { from{opacity:0;transform:scale(0.88)} to{opacity:1;transform:scale(1)} }

  @keyframes pulse3d {
    0%,100% { box-shadow: 0 0 0 0 rgba(217,4,41,0.5), 0 0 30px rgba(217,4,41,0.1); transform: translateY(0); }
    50%      { box-shadow: 0 0 0 16px rgba(217,4,41,0), 0 8px 40px rgba(217,4,41,0.35); transform: translateY(-2px); }
  }
  @keyframes glowPulse {
    0%,100% { box-shadow: 0 0 15px rgba(217,4,41,0.3), inset 0 0 15px rgba(217,4,41,0.05); }
    50%      { box-shadow: 0 0 50px rgba(217,4,41,0.7), inset 0 0 30px rgba(217,4,41,0.12); }
  }
  @keyframes scanLine {
    0%   { background-position: 0 -100%; }
    100% { background-position: 0 200%; }
  }
  @keyframes borderRun {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  @keyframes float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-6px); }
  }
  @keyframes shimmerMove {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }

  /* ══════ LAYOUT ══════ */
  .main  { background-color: var(--bg) !important; }
  .block-container {
    padding-top: 1.5rem !important; max-width: 1100px !important;
    padding-left: 1rem !important; padding-right: 1rem !important;
  }
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b0f 0%, #0d1117 100%) !important;
    border-right: 2px solid rgba(217,4,41,0.2) !important;
  }

  /* ══════ HERO BANNER — épuré, pas de fond rouge ══════ */
  .hero-banner {
    position: relative; overflow: hidden;
    background: transparent;
    border: 3px solid var(--red);
    border-radius: 24px;
    padding: 2.5rem 2rem; margin-bottom: 2rem; text-align: center;
    box-shadow: 0 0 60px rgba(217,4,41,0.2), 0 0 120px rgba(217,4,41,0.06);
    animation: fadeInDown 0.8s cubic-bezier(0.16,1,0.3,1) both;
  }
  /* Ligne lumineuse qui traverse le hero */
  .hero-banner::before {
    content: '';
    position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(217,4,41,0.06), transparent);
    animation: shimmerMove 3s ease-in-out infinite;
    pointer-events: none;
  }
  /* Coin décoratif */
  .hero-banner::after {
    content: '';
    position: absolute; top: -1px; left: -1px; right: -1px; bottom: -1px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(217,4,41,0.15) 0%, transparent 40%, transparent 60%, rgba(217,4,41,0.08) 100%);
    pointer-events: none;
  }
  .hero-banner h1 {
    font-size: clamp(1.8rem,5vw,3rem); font-weight: 900;
    color: #FFF; margin: 0; letter-spacing: -1.5px;
    text-shadow: 0 0 40px rgba(217,4,41,0.3);
  }
  .hero-banner h1 span { color: var(--red); }
  .hero-banner .slogan {
    color: var(--muted); margin: 0.6rem 0 0; font-size: 0.85rem;
    letter-spacing: 3px; text-transform: uppercase;
  }
  .hero-banner .sub {
    color: var(--red); font-size: 0.72rem; font-weight: 700;
    letter-spacing: 4px; text-transform: uppercase; margin-top: 0.3rem;
  }

  /* ══════ INPUTS ══════ */
  .stTextInput input, .stNumberInput input {
    background-color: var(--bg2) !important; color: #FFF !important;
    border: 2px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    font-size: 0.9rem !important;
  }
  .stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 4px rgba(217,4,41,0.15), 0 0 20px rgba(217,4,41,0.1) !important;
  }

  /* ══════ BOUTON PRINCIPAL — propre, sans fond noir sur le texte ══════ */
  .stButton > button {
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #D90429, #ff1744, #D90429) !important;
    background-size: 200% auto !important;
    color: #fff !important; border: none !important;
    border-radius: 14px !important; font-weight: 900 !important;
    font-size: 1rem !important; letter-spacing: 2px !important;
    padding: 0.9rem 2rem !important; width: 100% !important;
    transition: background-position 0.4s ease, transform 0.3s ease, box-shadow 0.3s ease !important;
    animation: pulse3d 2.5s infinite;
  }
  .stButton > button:hover {
    background-position: right center !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 16px 45px rgba(217,4,41,0.55) !important;
  }

  /* Boutons sidebar — discrets */
  section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important; color: #aaa !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    font-weight: 600 !important; font-size: 0.78rem !important;
    padding: 0.4rem 0.7rem !important; animation: none !important;
    letter-spacing: 0 !important; border-radius: 8px !important;
    text-shadow: none !important;
  }
  section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--red) !important; color: #FFF !important;
    background: rgba(217,4,41,0.08) !important;
    transform: none !important; box-shadow: none !important;
  }

  /* ══════ TABS ══════ */
  .stTabs [data-baseweb="tab-list"] {
    background: var(--bg2); border-radius: 14px; padding: 5px; gap: 4px;
    border: 2px solid rgba(255,255,255,0.06); flex-wrap: wrap;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; color: var(--muted) !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: clamp(0.65rem,2vw,0.82rem) !important;
    padding: 0.45rem 0.7rem !important;
    transition: all 0.25s ease !important; letter-spacing: 0.3px !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #D90429, #c0021f) !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(217,4,41,0.4) !important;
    border: none !important;
    outline: none !important;
  }
  /* Supprime tout fond parasite sur les tabs */
  .stTabs [data-baseweb="tab"]:focus,
  .stTabs [data-baseweb="tab"]:focus-visible,
  .stTabs [data-baseweb="tab"][aria-selected="true"] > div {
    background: transparent !important;
    box-shadow: none !important;
    outline: none !important;
  }

  /* ══════ CARTES RÉSULTATS ══════ */
  .result-card {
    background: var(--bg2);
    border: 2px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 1.4rem; margin-bottom: 1rem;
    animation: fadeInUp 0.5s ease both;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative; overflow: hidden;
  }
  .result-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    opacity: 0; transition: opacity 0.3s;
  }
  .result-card:hover { transform: translateY(-4px); border-color: rgba(217,4,41,0.3); }
  .result-card:hover::before { opacity: 1; }
  .result-card:hover { box-shadow: 0 12px 40px rgba(217,4,41,0.12); }

  .card-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }
  .card-title {
    color: var(--red); font-size: 0.75rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px; margin: 0;
  }

  /* ══════ SCORE BADGE ══════ */
  .score-wrap { text-align: center; padding: 1rem 0; animation: scaleIn 0.6s ease both; }
  .score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 110px; height: 110px; border-radius: 50%;
    border: 3px solid var(--red);
    font-size: 2.4rem; font-weight: 900; color: #FFF;
    background: radial-gradient(circle at 30% 30%, #2d0000, var(--bg));
    margin: 0 auto 0.75rem;
    animation: glowPulse 2.5s ease-in-out infinite;
    position: relative;
  }
  .score-badge::after {
    content: ''; position: absolute; inset: -8px;
    border-radius: 50%; border: 1px solid rgba(217,4,41,0.2);
    animation: float 3s ease-in-out infinite;
  }
  .wow-badge {
    display: inline-block;
    background: linear-gradient(135deg, #ff5500, #D90429);
    color: white; font-weight: 800; font-size: 0.72rem;
    padding: 5px 16px; border-radius: 20px;
    letter-spacing: 2px; text-transform: uppercase;
    animation: fadeInUp 0.7s ease both;
    box-shadow: 0 4px 15px rgba(217,4,41,0.4);
  }
  .ps-badge {
    display: inline-block;
    background: linear-gradient(135deg, #0055bb, #003a8c);
    color: white; font-weight: 800; font-size: 0.72rem;
    padding: 5px 16px; border-radius: 20px;
    letter-spacing: 2px; text-transform: uppercase;
    animation: fadeInUp 0.7s ease both;
    box-shadow: 0 4px 15px rgba(0,85,187,0.4);
  }

  /* ══════ PRICE BOXES ══════ */
  .price-box {
    background: var(--bg2);
    border: 2px solid var(--red);
    border-radius: 16px; padding: 1.1rem;
    text-align: center; margin-bottom: 1rem;
    transition: all 0.3s ease; animation: fadeInUp 0.5s ease both;
    position: relative; overflow: hidden;
  }
  .price-box::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
  }
  .price-box:hover {
    transform: translateY(-5px) scale(1.03);
    box-shadow: 0 12px 30px rgba(217,4,41,0.3);
  }
  .price-box .label { color: var(--muted); font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.5px; }
  .price-box .value { color: #FFF; font-size: clamp(1rem,4vw,1.5rem); font-weight: 900; margin-top: 4px; }
  .price-box .currency { color: var(--red); font-size: 0.72rem; }

  /* ══════ TABLEAU ══════ */
  .gains-table { width:100%; border-collapse:collapse; margin-top:0.5rem; font-size:clamp(0.7rem,2vw,0.83rem); }
  .gains-table th {
    background: linear-gradient(135deg, #D90429, #a80220);
    color: white; padding: 10px 12px; font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: 1px; text-align: center;
  }
  .gains-table td { background: var(--bg); color: #CCC; padding: 10px 12px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.2s; }
  .gains-table tr:hover td { background: var(--bg2); color: #FFF; }
  .gains-table .pos { color: #44dd88; font-weight: 700; }
  .gains-table .neg { color: #ff4444; font-weight: 700; }
  .gains-table .highlight td { background: rgba(217,4,41,0.06) !important; border-left: 3px solid var(--red); }
  .pub-badge { display:inline-block; background:rgba(204,85,0,0.15); border:1px solid #cc5500; color:#ff9944; font-size:0.68rem; font-weight:700; padding:3px 10px; border-radius:10px; }

  /* ══════ CARDS CONTENU ══════ */
  .amelioration-card {
    background: linear-gradient(135deg, rgba(18,15,0,0.8), rgba(26,21,0,0.8));
    border: 2px solid #cc7700; border-radius: 16px;
    padding: 1.25rem; margin-bottom: 1rem;
    animation: fadeInLeft 0.5s ease both;
  }
  .metric-item {
    background: var(--bg2); border: 2px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 0.85rem; text-align: center; flex: 1; min-width: 85px;
    transition: all 0.25s ease; animation: fadeInUp 0.5s ease both;
  }
  .metric-item:hover {
    border-color: var(--red); transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(217,4,41,0.2);
  }
  .metric-item .m-label { color: var(--muted); font-size: 0.58rem; text-transform: uppercase; letter-spacing: 1px; }
  .metric-item .m-value { color: #FFF; font-size: clamp(0.82rem,3vw,1rem); font-weight: 700; margin-top: 3px; }
  .metric-item .m-value.red { color: var(--red); }

  /* ══════ SHOPIFY ══════ */
  .titre-option {
    background: var(--bg); border: 2px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 0.7rem;
    transition: all 0.3s ease; animation: fadeInLeft 0.5s ease both;
  }
  .titre-option:hover { border-color: var(--red); transform: translateX(8px); background: rgba(217,4,41,0.04); }
  .titre-option .num { color: var(--red); font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.3rem; }
  .titre-option .texte { color: #FFF; font-size: 1rem; font-weight: 700; line-height: 1.4; }

  .para-card {
    background: var(--bg); border-left: 4px solid var(--red);
    border-radius: 0 14px 14px 0; padding: 1rem 1.3rem; margin-bottom: 0.8rem;
    transition: all 0.3s ease; animation: fadeInUp 0.5s ease both;
    position: relative;
  }
  .para-card::before {
    content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 0;
    background: #ff6b6b; transition: height 0.3s ease;
    border-radius: 2px 0 0 2px;
  }
  .para-card:hover { background: rgba(217,4,41,0.03); transform: translateX(6px); }
  .para-card:hover::before { height: 100%; }
  .para-card .para-titre { color: var(--red); font-weight: 800; font-size: 0.92rem; margin-bottom: 0.5rem; }
  .para-card .para-texte { color: #BBB; font-size: 0.88rem; line-height: 1.8; }

  /* ══════ ADS & SCRIPTS ══════ */
  .ad-block {
    background: var(--bg2); border: 2px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 1.3rem; margin-bottom: 0.8rem;
    transition: all 0.3s ease; animation: fadeInUp 0.5s ease both;
    position: relative; overflow: hidden;
  }
  .ad-block::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--red), #ff6b35, var(--red));
    background-size: 200% auto; animation: borderRun 3s linear infinite;
    opacity: 0; transition: opacity 0.3s;
  }
  .ad-block:hover { border-color: rgba(217,4,41,0.35); transform: translateY(-3px); box-shadow: 0 10px 35px rgba(217,4,41,0.15); }
  .ad-block:hover::before { opacity: 1; }
  .ad-accroche { color: #ff9944; font-weight: 800; font-size: 1.05rem; margin-bottom: 0.5rem; }
  .ad-texte { color: #CCC; font-size: 0.9rem; line-height: 1.9; white-space: pre-wrap; }

  .script-block {
    background: var(--bg2); border: 2px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 1.5rem; margin-bottom: 1rem;
    transition: all 0.3s ease; animation: fadeInUp 0.5s ease both;
  }
  .script-block:hover { border-color: rgba(217,4,41,0.3); box-shadow: 0 8px 30px rgba(217,4,41,0.1); }
  .script-label { color: var(--red); font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
  .script-texte { color: #CCC; font-size: 0.92rem; line-height: 2.1; white-space: pre-wrap; }

  /* ══════ OFFRES ══════ */
  .offre-card {
    background: linear-gradient(135deg, rgba(5,15,0,0.9), rgba(10,24,0,0.9));
    border: 2px solid #336600; border-radius: 16px;
    padding: 1.3rem; margin-bottom: 0.8rem;
    transition: all 0.3s ease; animation: fadeInUp 0.5s ease both;
  }
  .offre-card:hover { transform: translateY(-5px); box-shadow: 0 12px 35px rgba(51,102,0,0.3); border-color: #55aa00; }
  .offre-card .offre-titre { color: #77dd22; font-weight: 900; font-size: 0.95rem; margin-bottom: 0.4rem; }
  .offre-card .offre-desc { color: #BBB; font-size: 0.85rem; line-height: 1.7; }
  .offre-card .offre-prix { color: #55dd88; font-weight: 700; font-size: 0.78rem; margin-top: 0.5rem; }

  /* ══════ DIVERS ══════ */
  .golden-rule {
    background: linear-gradient(135deg, rgba(14,0,0,0.8), rgba(26,8,0,0.8));
    border: 2px solid rgba(204,85,0,0.6); border-radius: 14px;
    padding: 1rem 1.2rem; margin-bottom: 1rem;
  }
  .golden-rule p { color: #ffaa55; font-size: 0.8rem; margin: 0; line-height: 1.9; }

  .export-section {
    background: linear-gradient(135deg, rgba(10,0,0,0.9), rgba(21,0,0,0.9));
    border: 3px solid var(--red); border-radius: 18px;
    padding: 1.5rem; margin-top: 2rem; text-align: center;
    animation: fadeInUp 0.6s ease both;
    box-shadow: 0 0 40px rgba(217,4,41,0.15);
  }

  /* ══════ ST.CODE ══════ */
  .stCodeBlock, pre, code,
  [data-testid="stCode"] > div,
  [data-testid="stCode"] pre {
    background-color: #0a0e15 !important;
    color: #e0e0e0 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
  }
  [data-testid="stCode"] button,
  [data-testid="stCode"] button:hover {
    background: var(--red) !important; color: white !important;
    border-radius: 6px !important; opacity: 1 !important;
  }

  /* ══════ TITRE SECTION (card_title) ══════ */
  .section-label {
    color: var(--red); font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px;
    margin: 1.3rem 0 0.4rem; display: flex; align-items: center; gap: 8px;
  }
  .section-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(217,4,41,0.3), transparent);
  }

  #MainMenu, footer, header { visibility: hidden; }
  label { color: #8b949e !important; font-weight: 600 !important; font-size: 0.82rem !important; }

  @media (max-width: 768px) {
    .block-container { padding-left: 0.4rem !important; padding-right: 0.4rem !important; }
    .hero-banner { padding: 1.5rem 1rem; }
    .stTabs [data-baseweb="tab"] { padding: 0.3rem 0.4rem !important; font-size: 0.6rem !important; }
    .gains-table th, .gains-table td { padding: 7px 5px; font-size: 0.66rem; }
  }
</style>

""", unsafe_allow_html=True)

# ── UTILITAIRES ───────────────────────────────────────────────────────────────

def card_title(title: str):
    """Titre rouge premium avec ligne décorative."""
    st.markdown(f'<div class="section-label">{title}</div>', unsafe_allow_html=True)

def content_block(text: str, border_color: str = "#2a3140"):
    """
    Affiche le texte en bloc visuel aéré (multilignes, paragraphes)
    + bouton copier natif Streamlit en dessous.
    Respecte les \n — chaque retour à la ligne est préservé.
    """
    # Convertir \n en <br> pour affichage HTML propre
    html_text = str(text).replace("\n", "<br>")
    st.markdown(
        f'''<div style="border:1px solid {border_color};border-radius:12px;
            padding:1rem 1.2rem;margin-bottom:0.4rem;line-height:1.95;
            color:#DDD;font-size:0.88rem;font-family:'Space Grotesk',sans-serif;">
            {html_text}
        </div>''',
        unsafe_allow_html=True
    )
    # Bouton copier natif (fonctionne PC + mobile)
    st.code(text, language=None)

# section_header gardé pour compatibilité avec le HTML des cartes visuelles (score, tableau, etc.)
def section_header(title: str) -> str:
    return (f'<div class="card-header">'
            f'<span class="card-title">{title}</span>'
            f'</div>')


def save_to_history(name, score, data, prix_achat):
    entry = {
        "name":       name,
        "score":      score,
        "data":       data,
        "prix_achat": prix_achat,
        "ts":         datetime.now().strftime("%d/%m %H:%M")   # date + heure
    }
    existing = [h for h in st.session_state["history"] if h["name"] != name]
    updated  = [entry] + existing[:19]          # garde 20 analyses max
    st.session_state["history"] = updated
    write_history_file(updated)                 # ← sauvegarde sur disque

def get_pub_budget(v):
    if v <= 10:  return "5$–7$/jour"
    elif v <= 20: return "7$–10$/jour"
    else:         return "15$–20$/jour"

def calc_rentabilite(ventes, prix_moyen, prix_achat):
    """
    Frais fixes LABO : 5 000 FCFA/vente
      - Livraison : 2 000 FCFA
      - Publicité  : 2 000 FCFA
      - Closing    : 1 000 FCFA
    """
    ca            = ventes * prix_moyen
    cout_produit  = ventes * prix_achat
    frais_fixes   = ventes * 5000          # 2000+2000+1000
    cout_global   = cout_produit + frais_fixes
    benef_net     = ca - cout_global
    return ca, cout_produit, frais_fixes, cout_global, benef_net

def build_export(name, pa, pmin, pmax, data):
    sep = "=" * 60
    lines = [
        sep,
        "  ECOMASTER LABO PRO — PACK MARKETING",
        f"  Créé par LABO · {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"  Produit : {name}",
        f"  Prix achat : {pa:,} FCFA | Vente : {pmin:,}–{pmax:,} FCFA",
        f"  Score : {data.get('score','?')}/10 | Type : {data.get('type_produit','').upper()}",
        sep, "",
        "📊 STRATÉGIE", "-"*40,
        f"Verdict : {data.get('score_justification','')}",
        f"\nPublic cible : {data.get('public_cible','')}",
        "\nPeurs :",
    ] + [f"  - {p}" for p in data.get("peurs", [])] + \
        ["\nDésirs :"] + [f"  - {d}" for d in data.get("desirs", [])] + \
        ["", "\n🎁 OFFRES", "-"*40]
    for i, o in enumerate(data.get("offres", [])):
        lines += [f"Offre {i+1} — {o.get('nom','')}", f"  {o.get('description','')}", f"  Prix : {o.get('prix_suggere','')}", ""]
    lines += ["", "\n🛍️ SHOPIFY", "-"*40, "Titres :"]
    for t in data.get("shopify", {}).get("titres", []):
        lines.append(f"  [{t.get('angle','')}] {t.get('titre','')}")
    lines.append("\nFiche produit :")
    for p in data.get("shopify", {}).get("paragraphes", []):
        lines += [f"\n{p.get('titre','')}", p.get('texte','')]
    lines += ["", "\n📣 FACEBOOK ADS", "-"*40]
    for i, ad in enumerate(data.get("facebook_ads", [])):
        lines += [f"--- Ad {i+1} ---", f"TITRE : {ad.get('accroche','')}", ad.get("texte",""), ""]
    lines += ["", "\n🎙️ SCRIPTS VOIX-OFF", "-"*40]
    for i, s in enumerate(data.get("scripts", [])):
        lines += [f"--- {s.get('angle','')} ---", s.get("texte_complet",""), ""]
    lines += ["", sep, "  EcoMaster Labo Pro — by LABO", sep]
    return "\n".join(lines)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 0.75rem;">
      <p style="color:#D90429;font-weight:800;font-size:1rem;margin:0;">🚀 EcoMaster Labo Pro</p>
      <p style="color:#777;font-size:0.68rem;margin:0.25rem 0 0;line-height:1.5;">
        Tout-en-un pour un e-commerce réussi<br>
        <span style="color:#D90429;font-weight:700;">créé par LABO</span>
      </p>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        '<p style="color:#555;font-size:0.68rem;text-transform:uppercase;'
        'letter-spacing:1px;margin-bottom:0.6rem;">🕐 Historique</p>',
        unsafe_allow_html=True
    )

    history = st.session_state["history"]   # chargé depuis disque au démarrage

    if not history:
        st.markdown(
            '<p style="color:#444;font-size:0.78rem;font-style:italic;">'
            '📭 Aucune analyse encore.<br>Lance ta première analyse !</p>',
            unsafe_allow_html=True
        )
    else:
        # Bouton "Tout effacer"
        if st.button("🗑️ Effacer l'historique", key="clear_hist"):
            st.session_state["history"] = []
            write_history_file([])

        st.markdown("<br>", unsafe_allow_html=True)

        for i, h in enumerate(history):
            short    = h["name"][:18] + ("…" if len(h["name"]) > 18 else "")
            date_str = h.get("ts", "")
            score_v  = h.get("score", "?")
            icon     = "⭐" if i == 0 else "📦"

            # Carte cliquable pour chaque entrée historique
            st.markdown(
                f'''<div style="border:1px solid rgba(255,255,255,0.08);
                  border-radius:8px;padding:0.5rem 0.75rem;margin-bottom:0.4rem;cursor:pointer;">
                  <p style="color:#FFF;font-weight:700;margin:0;font-size:0.8rem;">{icon} {short}</p>
                  <p style="color:#555;font-size:0.65rem;margin:0.2rem 0 0;">
                    Score {score_v}/10 · {date_str}
                  </p>
                </div>''',
                unsafe_allow_html=True
            )
            if st.button(f"↩️ Recharger", key=f"hist_{i}_{h['name'][:8]}"):
                st.session_state["result"]         = h["data"]
                st.session_state["analyzed"]       = True
                st.session_state["active_product"] = h["name"]
                st.session_state["active_price"]   = h["prix_achat"]

    st.markdown("---")
    st.markdown("""<div class="golden-rule">
      <p>💡 <b style="color:#ffcc44;">Règle d'or LABO :</b><br>
      Budget test : <b style="color:#ff8844;">4$–7$/jour</b><br>
      sur <b>1 seule créative</b> Facebook.<br><br>
      Prix vente = achat + <b style="color:#ff8844;">8K–12K FCFA</b><br>
      <span style="color:#555;font-size:0.72rem;">Frais fixes : 5 000 FCFA/vente</span><br>
      <span style="color:#444;font-size:0.68rem;">(2K livraison · 2K pub · 1K closing)</span></p>
    </div>""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero-banner">
  <h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
  <p class="slogan">Tout-en-un pour un e-commerce réussi</p>
  <p class="sub">créé par LABO</p>
</div>""", unsafe_allow_html=True)

# ── INPUTS ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2], gap="large")
with col1:
    product_name = st.text_input(
        "📦 Nom du Produit",
        value=st.session_state.get("active_product", ""),
        placeholder="Ex: Bracelet Protection Ancestral"
    )
    purchase_price = st.number_input(
        "💰 Prix d'Achat (FCFA)",
        min_value=0, step=500,
        value=int(st.session_state.get("active_price", 5000))
    )
    objectif_ventes = st.number_input(
        "🎯 Objectif de ventes / jour",
        min_value=1, step=1,
        value=int(st.session_state.get("active_ventes", 10))
    )
with col2:
    uploaded_files = st.file_uploader(
        "📸 Photos produit (1 à 3)",
        type=["jpg","jpeg","png","webp"],
        accept_multiple_files=True
    )
    if uploaded_files:
        # Thumbnails petits — 80px de large max
        thumb_cols = st.columns(3)
        for i, f in enumerate(uploaded_files[:3]):
            with thumb_cols[i]:
                st.image(f, width=80)

price_min = purchase_price + 8000
price_max = purchase_price + 12000
prix_moyen = (price_min + price_max) / 2

st.markdown("<br>", unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4, gap="small")
with p1:
    st.markdown(f'<div class="price-box"><div class="label">💵 Prix Min</div><div class="value">{price_min:,}<span class="currency"> F</span></div></div>', unsafe_allow_html=True)
with p2:
    st.markdown(f'<div class="price-box"><div class="label">💵 Prix Max</div><div class="value">{price_max:,}<span class="currency"> F</span></div></div>', unsafe_allow_html=True)
with p3:
    st.markdown(f'<div class="price-box"><div class="label">📈 Marge Nette</div><div class="value">3K–7K<span class="currency"> F</span></div></div>', unsafe_allow_html=True)
with p4:
    st.markdown(f'<div class="price-box"><div class="label">📣 Budget Pub</div><div class="value" style="color:#ff9944;font-size:1rem;">{get_pub_budget(objectif_ventes)}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

# ── PROMPT ────────────────────────────────────────────────────────────────────
def build_prompt(name, pa, pmin, pmax):
    return f"""Tu es un expert en neuro-marketing et e-commerce pour l'Afrique Francophone (Togo, Sénégal, Côte d'Ivoire, Bénin).
Adapte TOUT au contexte africain : Facebook, WhatsApp, statut social, confiance communautaire, utilité immédiate.

PRODUIT : {name}
PRIX ACHAT : {pa:,} FCFA | PRIX DE VENTE CONSEILLÉ : {pmin:,}–{pmax:,} FCFA

CLASSIFICATION DU PRODUIT :
- "wow" = produit à effet visuel immédiat, la photo parle d'elle-même, pas besoin d'explication
- "probleme_solution" = produit qui résout une douleur précise, nécessite argumentation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ABSOLUES DE RÉDACTION :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① SHOPIFY — Fiche produit qui VEND (pas une liste de caractéristiques) :
   • EXACTEMENT 3 titres magnétiques de page produit.
   • EXACTEMENT 6 paragraphes.
   • Chaque paragraphe = 1 titre en gras accrocheur + EXACTEMENT 4 phrases courtes et percutantes.
   • Style direct et émotionnel. Exemple OBLIGATOIRE à imiter :
     "Maison intelligente instantanée : Transforme ta maison en un espace moderne en quelques secondes. Trois lampes s'allument dès qu'elles te détectent. Fini les interrupteurs à chercher dans le noir. Tes invités seront bluffés dès l'entrée."

② FACEBOOK ADS — 3 variantes complètes :
   • Chaque variante = 1 titre d'offre choc avec emoji (ex: 🔥 PROMO FLASH, ⚠️ STOCK LIMITÉ, 💥 OFFRE EXCLUSIVE).
   • Suivi d'un texte publicitaire émotionnel et fun de MAXIMUM 5 lignes.
   • Exemple OBLIGATOIRE à imiter :
     "💡 Rends ta maison intelligente avec moins de 10 000 francs ! Avec seulement 8 000 francs, tu reçois 3 lampes intelligentes qui s'allument automatiquement. Plus besoin de chercher l'interrupteur la nuit. Commande maintenant et fais-toi livrer gratuitement !"

③ SCRIPTS VOIX-OFF — 3 scripts INDÉPENDANTS de 130 à 170 MOTS CHACUN :
   • RÈGLE ABSOLUE : chaque script individuel = entre 130 et 170 mots. PAS 130 mots pour les 3 scripts réunis.
   • MISE EN FORME OBLIGATOIRE : utilise \n pour séparer les phrases courtes. Maximum 1-2 phrases par ligne. Le texte DOIT être aéré, pas un bloc continu.
   • Texte fluide et naturel, SANS balises techniques (pas de "Hook:", "CTA:", "Act 1:", etc.).
   • Utilise des noms africains réalistes : Kofi, Amina, Moussa, Fatou, Kwame, Aminata, Adama…
   • Si type WOW   → Hook visuel choc → Problème rapide → Solution visuelle → Preuve sociale locale → CTA urgent.
   • Si type P-S   → Hook douleur → Amplification → Solution précise → Témoignage local → CTA.
   • EXEMPLE de format attendu avec retours à la ligne :
     "8 personnes sur 10 se lèvent la nuit dans le noir.\nEt le plus étonnant, c'est qu'elles pensent que c'est normal.\nNormal de chercher l'interrupteur,\nnormal d'avancer à tâtons.\nMaintenant regarde ce qui se passe quand je pose le pied au sol.\nLa lumière s'allume toute seule.\nSans réfléchir. Sans rien appuyer.\nKofi à Lomé utilise ce système depuis 3 semaines.\nIl dit qu'il ne pourrait plus s'en passer.\nL'offre est disponible maintenant, mais les stocks sont limités.\nClique sur le lien et commande aujourd'hui."

④ FACEBOOK ADS — 3 variantes complètes :
   • Chaque variante = 1 titre d'offre choc avec emoji.
   • MISE EN FORME : le texte doit utiliser \n entre chaque ligne. Maximum 5 lignes.
   • Utilise des emojis, un ton fun et émotionnel, contexte africain.

⑤ ANGLES MARKETING — 5 angles différents et percutants :
   • Chaque angle = un titre court + une phrase d'accroche directe.
   • Adapté au marché africain francophone.

⑥ AVATAR CLIENT — Persona ultra-détaillé selon la méthode LABO :
   • Sexe, tranche d'âge précise, niveau de français (soutenu / familier / mixte).
   • Catégorie : Luxe / Domestique / Agriculture / Élevage / Pêche / Beauté & Soins / Santé / Tech / Mode / Alimentation / Autre.
   • Situation : profession, revenu mensuel estimé en FCFA, ville type, mode de vie.
   • Frustrations profondes (3), Désirs secrets (3), Objections à l'achat (3).
   • Message clé qui le convainc immédiatement.

⑦ CRÉATIVES PUBLICITAIRES — 4 concepts créatifs :
   • Chaque créative = concept + type de scène/visuel + message principal + type d'accroche.
   • Inspiré des formats qui fonctionnent sur Facebook/TikTok en Afrique.

⑧ IMAGES PRODUIT — 5 types de visuels pour la page de vente :
   • Démonstration du produit en action.
   • Utilisation réelle (mains/personne avec le produit).
   • Lifestyle (produit dans un environnement de vie africain réel).
   • Mise en avant d'un avantage clé.
   • Gros plan sur les détails/qualité du produit.
   • Pour chaque type : description précise du visuel à créer/commander.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Réponds UNIQUEMENT avec du JSON valide. Aucun texte avant ni après. Aucun commentaire.

{{
  "score": 8,
  "score_justification": "Analyse détaillée du potentiel marché africain en 2-3 phrases",
  "type_produit": "wow",
  "ameliorations": ["conseil concret 1", "conseil concret 2", "conseil concret 3"],
  "public_cible": "Description très précise : âge, ville, situation professionnelle, revenus, habitudes d'achat africaines, douleurs quotidiennes, rêves et aspirations",
  "peurs": ["peur précise et africaine 1", "peur 2", "peur 3"],
  "desirs": ["désir concret et africain 1", "désir 2", "désir 3"],
  "mots_cles": ["mot1", "mot2", "mot3", "mot4", "mot5"],
  "offres": [
    {{"nom": "Nom offre attractive", "description": "Contenu précis de l'offre en 1-2 phrases", "prix_suggere": "XXXX FCFA", "argument": "Pourquoi cette offre convertit en Afrique"}},
    {{"nom": "Nom offre 2", "description": "Contenu", "prix_suggere": "XXXX FCFA", "argument": "Argument"}},
    {{"nom": "Nom offre 3", "description": "Contenu", "prix_suggere": "XXXX FCFA", "argument": "Argument"}}
  ],
  "facebook_ads": [
    {{"angle": "Émotionnel",    "accroche": "🔥 TITRE CHOC ÉMOTIONNEL ICI",        "texte": "ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5 — fun, emojis, contexte africain"}},
    {{"angle": "Preuve Sociale","accroche": "⭐ TITRE TÉMOIGNAGE AFRICAIN ICI",    "texte": "ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5 — preuve sociale locale"}},
    {{"angle": "Urgence",       "accroche": "⚠️ STOCK LIMITÉ — COMMANDE VITE",    "texte": "ligne 1\\nligne 2\\nligne 3\\nligne 4\\nligne 5 — urgence et offre limitée"}}
  ],
  "shopify": {{
    "titres": [
      {{"angle": "Bénéfice Principal", "titre": "Titre page produit 1 — accrocheur"}},
      {{"angle": "Curiosité / Wow",    "titre": "Titre page produit 2 — intriguant"}},
      {{"angle": "Urgence / FOMO",     "titre": "Titre page produit 3 — urgent"}}
    ],
    "paragraphes": [
      {{"titre": "Titre §1 accrocheur en gras", "texte": "Phrase 1 qui vend.\\nPhrase 2 qui vend.\\nPhrase 3 qui vend.\\nPhrase 4 qui vend."}},
      {{"titre": "Titre §2 accrocheur en gras", "texte": "Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre": "Titre §3 accrocheur en gras", "texte": "Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre": "Titre §4 accrocheur en gras", "texte": "Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre": "Titre §5 accrocheur en gras", "texte": "Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}},
      {{"titre": "Titre §6 accrocheur en gras", "texte": "Phrase 1.\\nPhrase 2.\\nPhrase 3.\\nPhrase 4."}}
    ]
  }},
  "scripts": [
    {{"angle": "Script Émotionnel",      "texte_complet": "130 MOTS EXACTEMENT — texte fluide sans balise, naturel, humain, marché africain"}},
    {{"angle": "Script Bénéfice Direct", "texte_complet": "130 MOTS EXACTEMENT — angle bénéfice direct, preuve sociale africaine"}},
    {{"angle": "Script Urgence & Statut","texte_complet": "130 MOTS EXACTEMENT — statut social et urgence africaine"}}
  ],
  "angles_marketing": [
    {{"angle": "Peur & Urgence",       "titre": "Titre choc court", "accroche": "Phrase d'attaque directe, contexte africain"}},
    {{"angle": "Désir & Aspiration",   "titre": "Titre choc court", "accroche": "Phrase qui fait rêver, marché africain"}},
    {{"angle": "Preuve Sociale",       "titre": "Titre choc court", "accroche": "Témoignage ou chiffre concret africain"}},
    {{"angle": "Curiosité & Mystère",  "titre": "Titre choc court", "accroche": "Question ou révélation intrigante"}},
    {{"angle": "Transformation",       "titre": "Titre choc court", "accroche": "Avant/après, changement de vie concret"}}
  ],
  "avatar": {{
    "sexe": "homme / femme / les deux",
    "age": "25–40 ans",
    "francais": "familier",
    "categorie": "Domestique",
    "prenom_type": "Kofi, Amina ou autre prénom africain",
    "ville": "Lomé, Abidjan, Dakar ou similaire",
    "profession": "Profession précise avec contexte africain",
    "revenu": "80 000–120 000 FCFA/mois",
    "mode_vie": "Description du quotidien en 2 phrases, contexte africain",
    "frustrations": ["frustration précise 1", "frustration précise 2", "frustration précise 3"],
    "desirs": ["désir concret 1", "désir concret 2", "désir concret 3"],
    "objections": ["objection réelle 1", "objection réelle 2", "objection réelle 3"],
    "message_cle": "La phrase exacte (1 ligne max) qui le/la convainc d'acheter immédiatement"
  }},
  "creatives": [
    {{
      "concept": "Nom court du concept créatif",
      "scene": "Description précise de la scène ou du visuel à filmer/créer",
      "message": "Le message marketing principal de cette créative",
      "accroche_type": "Statistique / Problème / WOW / Témoignage / Interdiction"
    }},
    {{
      "concept": "Concept 2",
      "scene": "Scène 2",
      "message": "Message 2",
      "accroche_type": "Type d'accroche 2"
    }},
    {{
      "concept": "Concept 3",
      "scene": "Scène 3",
      "message": "Message 3",
      "accroche_type": "Type d'accroche 3"
    }},
    {{
      "concept": "Concept 4",
      "scene": "Scène 4",
      "message": "Message 4",
      "accroche_type": "Type d'accroche 4"
    }}
  ],
  "images_produit": [
    {{"type": "Démonstration", "description": "Description précise du visuel démonstration à créer"}},
    {{"type": "Utilisation",   "description": "Description précise : personne utilisant le produit, contexte africain"}},
    {{"type": "Lifestyle",     "description": "Description de la scène lifestyle dans un foyer ou environnement africain réel"}},
    {{"type": "Avantage Clé",  "description": "Visuel mettant en avant l'avantage principal avec texte ou annotation"}},
    {{"type": "Gros Plan",     "description": "Gros plan sur la qualité, les détails ou la finition du produit"}}
  ]
}}"""

# ── API GROQ ──────────────────────────────────────────────────────────────────
def repair_json(raw: str) -> dict:
    """
    Parse JSON robuste :
    1. Tente json.loads direct
    2. Si troncature (JSON incomplet), répare en fermant les structures ouvertes
    """
    # Nettoyage markdown
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    # Tentative directe
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Réparation : trouver la dernière virgule propre et refermer
    # Stratégie : couper après le dernier élément complet, refermer les }] manquants
    # On compte les accolades/crochets ouverts non fermés
    stack = []
    last_valid_pos = 0
    in_string = False
    escape_next = False

    for idx, ch in enumerate(raw):
        if escape_next:
            escape_next = False
            continue
        if ch == '\\' and in_string:
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch in ('{', '['):
            stack.append(ch)
        elif ch in ('}', ']'):
            if stack:
                stack.pop()
                last_valid_pos = idx + 1

    # Fermer ce qui reste ouvert
    closing = ""
    for bracket in reversed(stack):
        closing += '}' if bracket == '{' else ']'

    repaired = raw[:last_valid_pos] + closing
    try:
        return json.loads(repaired)
    except json.JSONDecodeError:
        # Dernier recours : extraire uniquement les champs clés présents
        partial = {}
        for key in ["score","score_justification","type_produit","ameliorations",
                    "public_cible","peurs","desirs","mots_cles","offres",
                    "shopify","facebook_ads","scripts","angles_marketing","avatar","creatives","images_produit"]:
            pattern = rf'"{key}"\s*:\s*'
            m = re.search(pattern, raw)
            if m:
                # Extrait la valeur brute (best-effort)
                start = m.end()
                ch0 = raw[start:start+1]
                if ch0 in ('"', '{', '['):
                    end_map = {'"': '"', '{': '}', '[': ']'}
                    depth = 0
                    in_s  = False
                    for j, c in enumerate(raw[start:], start):
                        if c == '"' and raw[j-1:j] != '\\':
                            in_s = not in_s
                        if not in_s:
                            if c in ('{','['): depth += 1
                            elif c in ('}',']'): depth -= 1
                            if depth == 0:
                                try:
                                    partial[key] = json.loads(raw[start:j+1])
                                except Exception:
                                    pass
                                break
        return partial if partial else {}

def call_groq(prompt, images):
    from groq import Groq
    client  = Groq(api_key=st.secrets["GROQ_API_KEY"])
    content = []
    for img_data in images:
        b64 = base64.b64encode(img_data).decode("utf-8")
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
    content.append({"type": "text", "text": prompt})
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": content}],
        max_tokens=7000,          # ← augmenté pour éviter la troncature du JSON
    )
    raw = response.choices[0].message.content.strip()
    return repair_json(raw)

# ── LANCEMENT ANALYSE ─────────────────────────────────────────────────────────
if analyze_clicked:
    if not product_name.strip():
        st.error("⚠️ Entre le nom du produit.")
    elif not uploaded_files:
        st.error("⚠️ Upload au moins une photo du produit.")
    else:
        images_bytes = [f.read() for f in uploaded_files[:3]]
        with st.spinner("🧠 Analyse IA en cours… 15–20 secondes ⏳"):
            try:
                data = call_groq(
                    build_prompt(product_name, purchase_price, price_min, price_max),
                    images_bytes
                )
                st.session_state["result"]         = data
                st.session_state["analyzed"]       = True
                st.session_state["active_product"] = product_name
                st.session_state["active_price"]   = purchase_price
                st.session_state["active_ventes"]  = objectif_ventes
                save_to_history(product_name, data.get("score", "?"), data, purchase_price)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur IA : {e}")
                st.session_state["analyzed"] = False

# ── AFFICHAGE RÉSULTATS ───────────────────────────────────────────────────────
if st.session_state.get("analyzed") and st.session_state.get("result"):
    data          = st.session_state["result"]
    type_produit  = data.get("type_produit", "wow")
    score         = int(data.get("score", 8))
    aname         = st.session_state.get("active_product", product_name)
    aprice        = st.session_state.get("active_price", purchase_price)
    aventes       = st.session_state.get("active_ventes", objectif_ventes)
    apmin         = aprice + 8000
    apmax         = aprice + 12000
    apmoy         = (apmin + apmax) / 2

    # Barre produit actif
    st.markdown(f"""
    <div style="border:2px solid rgba(217,4,41,0.3);border-radius:10px;
                padding:0.6rem 1rem;margin-bottom:1rem;display:flex;align-items:center;
                gap:0.75rem;flex-wrap:wrap;animation:fadeInDown 0.5s ease both;">
      <span style="color:#D90429;font-size:1.1rem;">📦</span>
      <div style="flex:1;min-width:150px;">
        <p style="color:#FFF;font-weight:700;margin:0;font-size:0.92rem;">{aname}</p>
        <p style="color:#444;font-size:0.72rem;margin:0;">
          Achat : {aprice:,} F · Vente : {apmin:,}–{apmax:,} FCFA · Frais fixes : 5 000 F/vente
        </p>
      </div>
      <span style="background:#D90429;color:white;font-weight:900;padding:3px 12px;border-radius:12px;font-size:0.8rem;">{score}/10</span>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Stratégie", "🎁 Offres", "🛍️ Shopify", "📣 Facebook Ads",
        "🎙️ Voix-Off", "🎯 Angles", "👤 Avatar",
        "🎬 Créatives", "🖼️ Images"
    ])

    # ── TAB 1 : STRATÉGIE ────────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            badge_html = ("<div class='wow-badge'>⚡ PRODUIT WOW</div>"
                          if type_produit == "wow"
                          else "<div class='ps-badge'>🎯 PROBLÈME-SOLUTION</div>")
            st.markdown(f"""<div class="score-wrap">
              <div class="score-badge">{score}/10</div>
              <p style="color:#444;font-size:0.72rem;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:1px;">Potentiel marché</p>
              {badge_html}
            </div>""", unsafe_allow_html=True)
        with c2:
            verdict = data.get("score_justification", "")
            card_title("💡 Verdict IA")
            content_block(verdict)

        if score < 9:
            amelios = data.get("ameliorations", [])
            amelios_txt = "\n".join([f"- {a}" for a in amelios])
            card_title("⚠️ Comment Booster ce Produit ?")
            content_block(amelios_txt)

        st.markdown(f"""<div style="display:flex;gap:0.45rem;flex-wrap:wrap;margin:1rem 0;">
          <div class="metric-item"><div class="m-label">Budget Pub</div><div class="m-value red">{get_pub_budget(aventes)}</div></div>
          <div class="metric-item"><div class="m-label">Frais/vente</div><div class="m-value">5 000 F</div></div>
          <div class="metric-item"><div class="m-label">Marge brute</div><div class="m-value">8K–12K F</div></div>
          <div class="metric-item"><div class="m-label">Type</div><div class="m-value red">{"⚡ WOW" if type_produit=="wow" else "🎯 P-S"}</div></div>
        </div>""", unsafe_allow_html=True)

        # ── TABLEAU RENTABILITÉ ───────────────────────────────────────────────
        volumes = sorted(set([5, 10, 20] + ([aventes] if aventes not in [5, 10, 20] else [])))
        rows_html = ""
        for v in volumes:
            ca, cout_prod, frais_tot, cout_global, bn = calc_rentabilite(v, apmoy, aprice)
            cls  = "pos" if bn >= 0 else "neg"
            sign = "+" if bn >= 0 else ""
            is_target = (v == aventes)
            tr_class  = ' class="highlight"' if is_target else ""
            label_v   = f"🎯 {v}/j" if is_target else f"{v}/jour"
            rows_html += f"""<tr{tr_class}>
              <td><b>{label_v}</b></td>
              <td><span class="pub-badge">{get_pub_budget(v)}</span></td>
              <td>{ca:,.0f} F</td><td>{cout_global:,.0f} F</td>
              <td class="{cls}">{sign}{bn:,.0f} F</td>
            </tr>"""

        st.markdown(f"""<div class="result-card">
          <div class="card-header"><span class="card-title">💰 Calculateur de Rentabilité LABO</span></div>
          <div style="overflow-x:auto;">
          <table class="gains-table">
            <thead><tr><th>Ventes</th><th>Budget Pub</th><th>CA</th><th>Coût Global</th><th>Bénéfice Net</th></tr></thead>
            <tbody>{rows_html}</tbody>
          </table></div>
          <p style="color:#333;font-size:0.68rem;margin-top:0.5rem;">
            * 5 000 FCFA/vente (2K livraison + 2K pub + 1K closing) · Prix moyen {apmoy:,.0f} FCFA
          </p>
        </div>""", unsafe_allow_html=True)

        cp_col, cd_col = st.columns(2, gap="medium")
        with cp_col:
            peurs = data.get("peurs", [])
            card_title("😰 Peurs du Client")
            content_block("\n".join([f"🔴 {p}" for p in peurs]))
        with cd_col:
            desirs = data.get("desirs", [])
            card_title("✨ Désirs du Client")
            content_block("\n".join([f"💚 {d}" for d in desirs]))

        public = data.get("public_cible", "")
        card_title("🎯 Public Cible")
        content_block(public)

        mots = data.get("mots_cles", [])
        if mots:
            badges_html = "".join([
                f'<span style="border:2px solid #D90429;color:#FFF;'
                f'padding:3px 11px;border-radius:20px;font-size:0.75rem;margin:3px;display:inline-block;">{m}</span>'
                for m in mots
            ])
            card_title("🔍 Mots-Clés")
            st.markdown(f'<div style="margin-bottom:0.5rem;">{badges_html}</div>', unsafe_allow_html=True)
            st.code(" · ".join(mots), language=None)  # gardé st.code pour copie one-liner

    # ── TAB 2 : OFFRES ───────────────────────────────────────────────────────
    with tab2:
        st.markdown("""<div style="border-left:3px solid #77dd22;padding:0.4rem 0.8rem;margin-bottom:1rem;">
          <p style="color:#77dd22;font-weight:700;margin:0;font-size:0.85rem;">
            🎁 Offres conçues pour booster tes ventes — Marché Africain Francophone
          </p></div>""", unsafe_allow_html=True)

        offres_list = data.get("offres", [])
        if not offres_list:
            st.warning("⚠️ Aucune offre générée. Relance une analyse.")
        for i, o in enumerate(offres_list):
            offre_txt = f"{o.get('nom','')}\nDescription : {o.get('description','')}\nPrix : {o.get('prix_suggere','')}\nArgument : {o.get('argument','')}"
            card_title(f"🎁 Offre {i+1} — {o.get('nom','')}")
            content_block(offre_txt)

    # ── TAB 3 : SHOPIFY ──────────────────────────────────────────────────────
    with tab3:
        shopify = data.get("shopify", {})
        titres  = shopify.get("titres", [])
        paras   = shopify.get("paragraphes", [])

        card_title("🏷️ 3 Titres Magnétiques — choisissez le meilleur")
        for i, t in enumerate(titres):
            content_block(f"Option {i+1} [{t.get('angle','')}]\n{t.get('titre','')}")

        st.markdown("<hr style='border-color:#2a3140;margin:1.2rem 0;'>", unsafe_allow_html=True)

        card_title("📝 Fiche Produit Shopify — 6 Paragraphes (4 phrases max)")
        for j, para in enumerate(paras):
            bloc = f"{para.get('titre','')}\n\n{para.get('texte','')}"
            content_block(bloc, border_color="#D90429" if j==0 else "#2a3140")

        # Copier tout d'un coup
        all_paras_txt = "\n\n".join([
            f"{p.get('titre','')}\n{p.get('texte','')}" for p in paras
        ])
        card_title("📦 Copier la fiche complète (6 paragraphes)")
        content_block(all_paras_txt)

    # ── TAB 4 : FACEBOOK ADS ─────────────────────────────────────────────────
    with tab4:
        fb_ads = data.get("facebook_ads", [])
        if not fb_ads:
            st.error("⚠️ Facebook Ads vides — JSON tronqué. Relance l'analyse.")
            with st.expander("🔍 Debug JSON reçu"):
                st.json(data)
        else:
            st.markdown("""<div style="border-left:3px solid #D90429;padding:0.4rem 0.8rem;margin-bottom:1rem;">
              <p style="color:#888;font-size:0.78rem;margin:0;">
                💡 3 variantes prêtes · Copie le bloc et colle dans Facebook Ads Manager
              </p></div>""", unsafe_allow_html=True)
            for i, ad in enumerate(fb_ads):
                accroche = ad.get("accroche", ad.get("titre", ad.get("headline", "")))
                texte    = ad.get("texte",    ad.get("text",  ad.get("body",     ad.get("contenu", ""))))
                angle    = ad.get("angle", f"Variante {i+1}")
                full     = f"{accroche}\n\n{texte}"
                card_title(f"📣 Variante {i+1} — {angle}")
                content_block(full)

    # ── TAB 5 : VOIX-OFF ─────────────────────────────────────────────────────
    with tab5:
        type_label = "⚡ PRODUIT WOW" if type_produit == "wow" else "🎯 PROBLÈME-SOLUTION"
        st.markdown(f"""<div style="border-left:3px solid #D90429;padding:0.4rem 0.8rem;margin-bottom:1rem;">
          <p style="color:#D90429;font-weight:700;margin:0;font-size:0.82rem;">
            Type : {type_label} · ~130 mots · Copie le script et enregistre ta voix-off
          </p></div>""", unsafe_allow_html=True)

        scripts = data.get("scripts", [])
        if not scripts:
            st.warning("⚠️ Scripts non générés. Relance l'analyse.")
        for i, script in enumerate(scripts):
            texte_script = script.get("texte_complet", script.get("texte", ""))
            word_count   = len(texte_script.split())
            card_title(f"🎙️ {script.get('angle', f'Script {i+1}')} · {word_count} mots")
            content_block(texte_script)

    # ── TAB 6 : ANGLES MARKETING ─────────────────────────────────────────────
    with tab6:
        st.markdown("""<div style="border-left:3px solid #D90429;padding:0.4rem 0.8rem;margin-bottom:1.2rem;">
          <p style="color:#D90429;font-weight:700;margin:0;font-size:0.82rem;">
            🎯 5 angles marketing prêts à utiliser — Marché Africain Francophone
          </p></div>""", unsafe_allow_html=True)

        angles = data.get("angles_marketing", [])
        if not angles:
            st.warning("⚠️ Angles non générés. Relance l'analyse.")
        else:
            for i, ang in enumerate(angles):
                angle_nom  = ang.get("angle",   f"Angle {i+1}")
                titre      = ang.get("titre",   "")
                accroche   = ang.get("accroche","")
                icons = ["🔴","🟠","🟡","🟢","🔵"]
                ic = icons[i] if i < len(icons) else "🎯"
                card_title(f"{ic} Angle {i+1} — {angle_nom}")
                st.markdown(f"""<div class="ad-block">
                  <p class="ad-accroche">{titre}</p>
                  <p class="ad-texte">{accroche}</p>
                </div>""", unsafe_allow_html=True)
                content_block(f"{titre}\n\n{accroche}")

    # ── TAB 7 : AVATAR CLIENT ─────────────────────────────────────────────────
    with tab7:
        av = data.get("avatar", {})
        if not av:
            st.warning("⚠️ Avatar non généré. Relance l'analyse.")
        else:
            prenom   = av.get("prenom_type", "Le client type")
            sexe     = av.get("sexe", "—")
            age      = av.get("age",  "—")
            fr_niv   = av.get("francais", "—")
            categ    = av.get("categorie", "—")
            ville    = av.get("ville", "—")
            prof     = av.get("profession", "—")
            revenu   = av.get("revenu", "—")
            mode_vie = av.get("mode_vie", "—")
            frusts   = av.get("frustrations", [])
            desirs_a = av.get("desirs", [])
            objecs   = av.get("objections", [])
            msg_cle  = av.get("message_cle", "—")

            # ── Carte identité ──
            st.markdown(f"""<div class="result-card" style="border-color:rgba(217,4,41,0.4);">
              <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
                <div style="font-size:3.5rem;line-height:1;">👤</div>
                <div>
                  <p style="color:#FFF;font-weight:900;font-size:1.4rem;margin:0;">{prenom}</p>
                  <p style="color:#888;font-size:0.8rem;margin:0.2rem 0 0;">{sexe} · {age} · {ville}</p>
                  <p style="color:#D90429;font-size:0.75rem;font-weight:700;margin:0.2rem 0 0;">{categ}</p>
                </div>
              </div>
              <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:1rem;">
                <span style="border:2px solid #D90429;color:#FFF;padding:3px 12px;border-radius:20px;font-size:0.75rem;">{prof}</span>
                <span style="border:2px solid #D90429;color:#FFF;padding:3px 12px;border-radius:20px;font-size:0.75rem;">{revenu}</span>
                <span style="border:2px solid #888;color:#aaa;padding:3px 12px;border-radius:20px;font-size:0.75rem;">Français {fr_niv}</span>
              </div>
              <p style="color:#BBB;font-size:0.85rem;margin-top:0.8rem;line-height:1.7;">{mode_vie}</p>
            </div>""", unsafe_allow_html=True)

            # ── 3 colonnes : Frustrations / Désirs / Objections ──
            ca, cb, cc = st.columns(3, gap="small")
            with ca:
                card_title("😤 Frustrations")
                for f in frusts:
                    st.markdown(f'<div style="border-left:3px solid #ff4444;padding:0.4rem 0.7rem;margin-bottom:0.5rem;color:#CCC;font-size:0.84rem;">{f}</div>', unsafe_allow_html=True)
            with cb:
                card_title("✨ Désirs")
                for d in desirs_a:
                    st.markdown(f'<div style="border-left:3px solid #44dd88;padding:0.4rem 0.7rem;margin-bottom:0.5rem;color:#CCC;font-size:0.84rem;">{d}</div>', unsafe_allow_html=True)
            with cc:
                card_title("🤔 Objections")
                for o in objecs:
                    st.markdown(f'<div style="border-left:3px solid #ff9944;padding:0.4rem 0.7rem;margin-bottom:0.5rem;color:#CCC;font-size:0.84rem;">{o}</div>', unsafe_allow_html=True)

            # ── Message clé ──
            card_title("💬 Message qui convainc")
            st.markdown(f"""<div style="border:2px solid #D90429;border-radius:14px;padding:1.2rem 1.4rem;margin-top:0.5rem;">
              <p style="color:#FFF;font-size:1rem;font-weight:700;line-height:1.8;margin:0;font-style:italic;">"{msg_cle}"</p>
            </div>""", unsafe_allow_html=True)

    # ── TAB 8 : CRÉATIVES PUBLICITAIRES ─────────────────────────────────────
    with tab8:
        st.markdown("""<div style="border-left:3px solid #ff6b35;padding:0.4rem 0.8rem;margin-bottom:1.2rem;">
          <p style="color:#ff6b35;font-weight:700;margin:0;font-size:0.82rem;">
            🎬 4 concepts de créatives prêts à produire — Facebook & TikTok
          </p></div>""", unsafe_allow_html=True)

        creatives = data.get("creatives", [])
        if not creatives:
            st.warning("⚠️ Créatives non générées. Relance l'analyse.")
        else:
            for i, cr in enumerate(creatives):
                concept    = cr.get("concept",      f"Créative {i+1}")
                scene      = cr.get("scene",        "")
                message    = cr.get("message",      "")
                accroche_t = cr.get("accroche_type","")

                icons_cr = ["🔴","🟠","🟡","🟢"]
                ic = icons_cr[i] if i < len(icons_cr) else "🎬"
                card_title(f"{ic} Créative {i+1} — {concept}")

                st.markdown(f"""<div class="result-card">
                  <div style="display:grid;gap:0.7rem;">
                    <div>
                      <p style="color:#ff6b35;font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:0 0 0.25rem;">🎬 Scène / Visuel</p>
                      <p style="color:#FFF;font-size:0.9rem;line-height:1.7;margin:0;">{scene}</p>
                    </div>
                    <div>
                      <p style="color:#ff6b35;font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:0 0 0.25rem;">💬 Message Principal</p>
                      <p style="color:#CCC;font-size:0.88rem;line-height:1.7;margin:0;">{message}</p>
                    </div>
                    <div>
                      <p style="color:#ff6b35;font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin:0 0 0.25rem;">⚡ Type d'Accroche</p>
                      <span style="border:2px solid #ff6b35;color:#ff6b35;padding:3px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;">{accroche_t}</span>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
                full_cr = f"CRÉATIVE {i+1} — {concept}\nScène : {scene}\nMessage : {message}\nType d'accroche : {accroche_t}"
                st.code(full_cr, language=None)

    # ── TAB 9 : IMAGES PRODUIT ────────────────────────────────────────────────
    with tab9:
        st.markdown("""<div style="border-left:3px solid #44aaff;padding:0.4rem 0.8rem;margin-bottom:1.2rem;">
          <p style="color:#44aaff;font-weight:700;margin:0;font-size:0.82rem;">
            🖼️ 5 types de visuels pour construire ta page de vente Shopify
          </p></div>""", unsafe_allow_html=True)

        images = data.get("images_produit", [])
        if not images:
            st.warning("⚠️ Images non générées. Relance l'analyse.")
        else:
            img_icons  = ["🎥","🤝","🏠","⭐","🔍"]
            img_colors = ["#44aaff","#44dd88","#ff9944","#D90429","#aa44ff"]

            for i, img in enumerate(images):
                type_img = img.get("type",        f"Type {i+1}")
                desc     = img.get("description", "")
                ic   = img_icons[i]  if i < len(img_icons)  else "🖼️"
                col  = img_colors[i] if i < len(img_colors) else "#888"

                st.markdown(f"""<div class="result-card" style="border-color:{col}22;">
                  <div style="display:flex;align-items:flex-start;gap:1rem;">
                    <div style="width:44px;height:44px;border-radius:50%;border:2px solid {col};
                         display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">
                      {ic}
                    </div>
                    <div style="flex:1;">
                      <p style="color:{col};font-weight:800;font-size:0.82rem;text-transform:uppercase;
                           letter-spacing:1.5px;margin:0 0 0.4rem;">{type_img}</p>
                      <p style="color:#DDD;font-size:0.88rem;line-height:1.8;margin:0;">{desc}</p>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
                st.code(f"{type_img}\n{desc}", language=None)

    # ── EXPORT ───────────────────────────────────────────────────────────────
    st.markdown("---")
    export_txt = build_export(aname, aprice, apmin, apmax, data)
    st.markdown("""<div class="export-section">
      <p style="color:#D90429;font-weight:800;font-size:1rem;margin:0 0 0.25rem;">📦 Pack Marketing Complet</p>
      <p style="color:#444;font-size:0.8rem;margin:0 0 1rem;">Toute l'analyse en un fichier .txt prêt à l'emploi</p>
    </div>""", unsafe_allow_html=True)
    st.download_button(
        label="⬇️ TÉLÉCHARGER MON PACK MARKETING (.txt)",
        data=export_txt,
        file_name=f"pack_{aname.replace(' ','_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════════
# CONFIG CLÉ API — STREAMLIT CLOUD
# ══════════════════════════════════════════════════════════════════
# 1. share.streamlit.io → "..." sur ton app → Settings → Secrets
# 2. Colle exactement :
#    GROQ_API_KEY = "gsk_XXXXXXXXXXXXXXXXXXXXXXXX"
# 3. Save → Reboot app
# ══════════════════════════════════════════════════════════════════
