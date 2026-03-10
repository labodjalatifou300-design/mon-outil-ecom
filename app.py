import streamlit as st
import io
import re
import json
from PIL import Image
import base64
from datetime import datetime

# ── INIT SESSION STATE (avant tout) ──────────────────────────────────────────
if "history"         not in st.session_state: st.session_state["history"]         = []
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

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0e1117 !important;
    color: #F0F0F0 !important;
  }
  .main { background-color: #0e1117 !important; }
  .block-container { padding-top: 1.5rem !important; max-width: 1100px !important; padding-left: 1rem !important; padding-right: 1rem !important; }
  section[data-testid="stSidebar"] { background-color: #0a0d12 !important; border-right: 1px solid #1e2530 !important; }

  .hero-banner {
    background: linear-gradient(135deg, #0e0000 0%, #1a0000 40%, #0e0000 100%);
    border: 1px solid #D90429; border-radius: 20px;
    padding: 2rem; margin-bottom: 1.5rem; text-align: center;
    box-shadow: 0 0 50px rgba(217,4,41,0.15);
    animation: fadeInDown 0.7s ease both;
  }
  .hero-banner h1 { font-size: clamp(1.6rem,5vw,2.6rem); font-weight: 900; color: #FFF; margin: 0; letter-spacing: -1px; }
  .hero-banner h1 span { color: #D90429; }
  .hero-banner .slogan { color: #888; margin: 0.4rem 0 0; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; }
  .hero-banner .sub { color: #D90429; font-size: 0.75rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-top: 0.2rem; }

  @keyframes fadeInDown { from { opacity:0; transform:translateY(-25px); } to { opacity:1; transform:translateY(0); } }
  @keyframes fadeInUp   { from { opacity:0; transform:translateY(20px);  } to { opacity:1; transform:translateY(0); } }
  @keyframes fadeInLeft { from { opacity:0; transform:translateX(-20px); } to { opacity:1; transform:translateX(0); } }
  @keyframes pulse { 0%,100% { box-shadow:0 0 0 0 rgba(217,4,41,0.4); } 50% { box-shadow:0 0 0 14px rgba(217,4,41,0); } }
  @keyframes glow  { 0%,100% { box-shadow:0 0 20px rgba(217,4,41,0.25); } 50% { box-shadow:0 0 45px rgba(217,4,41,0.65); } }
  @keyframes shimmer { 0% { opacity:0.7; } 50% { opacity:1; } 100% { opacity:0.7; } }

  .stTextInput input, .stNumberInput input {
    background-color: #161b22 !important; color: #FFF !important;
    border: 1px solid #2a3140 !important; border-radius: 10px !important;
    transition: all 0.3s ease !important;
  }
  .stTextInput input:focus, .stNumberInput input:focus {
    border-color: #D90429 !important; box-shadow: 0 0 0 3px rgba(217,4,41,0.2) !important;
  }

  .stButton > button {
    background: linear-gradient(135deg, #D90429 0%, #a80220 50%, #D90429 100%) !important;
    background-size: 200% auto !important; color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 800 !important; font-size: 1rem !important;
    padding: 0.8rem 2rem !important; width: 100% !important; letter-spacing: 1px !important;
    transition: all 0.3s ease !important; animation: pulse 2.5s infinite;
  }
  .stButton > button:hover { transform: translateY(-3px) !important; box-shadow: 0 12px 35px rgba(217,4,41,0.5) !important; }

  /* Boutons sidebar historique — style discret */
  section[data-testid="stSidebar"] .stButton > button {
    background: #161b22 !important; color: #CCC !important;
    border: 1px solid #2a3140 !important; font-weight: 600 !important;
    font-size: 0.8rem !important; padding: 0.45rem 0.75rem !important;
    animation: none !important; letter-spacing: 0 !important;
    border-radius: 8px !important;
  }
  section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #D90429 !important; color: #FFF !important;
    background: #1a0000 !important; transform: none !important;
    box-shadow: none !important;
  }

  .stTabs [data-baseweb="tab-list"] {
    background: #161b22; border-radius: 14px; padding: 5px; gap: 3px;
    border: 1px solid #2a3140; flex-wrap: wrap;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #666 !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: clamp(0.65rem,2vw,0.82rem) !important;
    padding: 0.4rem 0.6rem !important; transition: all 0.25s ease !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#D90429,#a80220) !important;
    color: white !important; box-shadow: 0 4px 15px rgba(217,4,41,0.4) !important;
  }

  .result-card {
    background: #161b22; border: 1px solid #2a3140; border-radius: 14px;
    padding: 1.4rem; margin-bottom: 1rem;
    animation: fadeInUp 0.5s ease both;
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  }
  .result-card:hover { transform: translateY(-3px); box-shadow: 0 10px 35px rgba(217,4,41,0.1); border-color: #3a2030; }

  .card-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #2a3140;
  }
  .card-title { color: #D90429; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin: 0; }

  /* BOUTON COPIER */
  .copy-btn {
    background: #1a1a2a; color: #888; border: 1px solid #2a3140;
    border-radius: 8px; padding: 5px 14px; font-size: 0.78rem;
    font-weight: 600; cursor: pointer; transition: all 0.2s ease;
    font-family: Inter, sans-serif; white-space: nowrap;
    display: inline-flex; align-items: center; gap: 4px;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
  }
  .copy-btn:hover { border-color: #D90429; color: #FFF; background: #2a0010; }
  .copy-btn:active { transform: scale(0.96); }
  .copy-area { margin: 0.5rem 0 0.8rem; }

  .score-wrap { text-align: center; padding: 1rem 0; animation: fadeInUp 0.6s ease both; }
  .score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 100px; height: 100px; border-radius: 50%;
    border: 4px solid #D90429; font-size: 2.2rem; font-weight: 900;
    color: #FFF; background: radial-gradient(circle,#2d0000,#0e1117);
    margin: 0 auto 0.75rem; animation: glow 2.5s infinite;
  }
  .wow-badge { display:inline-block; background:linear-gradient(135deg,#ff5500,#D90429); color:white; font-weight:800; font-size:0.75rem; padding:4px 14px; border-radius:20px; letter-spacing:1.5px; text-transform:uppercase; animation: fadeInUp 0.7s ease both; }
  .ps-badge  { display:inline-block; background:linear-gradient(135deg,#0055bb,#003a8c); color:white; font-weight:800; font-size:0.75rem; padding:4px 14px; border-radius:20px; letter-spacing:1.5px; text-transform:uppercase; animation: fadeInUp 0.7s ease both; }

  .price-box {
    background: linear-gradient(135deg,#0e0000,#1a0505); border:1px solid #D90429;
    border-radius:14px; padding:1.1rem; text-align:center; margin-bottom:1rem;
    transition: transform 0.2s, box-shadow 0.2s;
    animation: fadeInUp 0.5s ease both;
  }
  .price-box:hover { transform:scale(1.05); box-shadow:0 8px 25px rgba(217,4,41,0.25); }
  .price-box .label { color:#666; font-size:0.68rem; text-transform:uppercase; letter-spacing:1px; }
  .price-box .value { color:#FFF; font-size:clamp(1rem,4vw,1.4rem); font-weight:900; margin-top:3px; }
  .price-box .currency { color:#D90429; font-size:0.72rem; }

  .amelioration-card {
    background:linear-gradient(135deg,#120f00,#1a1500); border:1px solid #cc7700;
    border-radius:14px; padding:1.25rem; margin-bottom:1rem;
    animation: fadeInLeft 0.5s ease both;
  }

  .metric-item {
    background:#161b22; border:1px solid #2a3140; border-radius:12px;
    padding:0.75rem; text-align:center; flex:1; min-width:85px;
    transition: all 0.2s; animation: fadeInUp 0.5s ease both;
  }
  .metric-item:hover { border-color:#D90429; transform:translateY(-3px); box-shadow:0 6px 20px rgba(217,4,41,0.15); }
  .metric-item .m-label { color:#555; font-size:0.6rem; text-transform:uppercase; letter-spacing:0.8px; }
  .metric-item .m-value { color:#FFF; font-size:clamp(0.82rem,3vw,1rem); font-weight:700; margin-top:2px; }
  .metric-item .m-value.red { color:#D90429; }

  /* TABLEAU RENTABILITÉ */
  .gains-table { width:100%; border-collapse:collapse; margin-top:0.5rem; font-size:clamp(0.7rem,2vw,0.83rem); }
  .gains-table th { background:#D90429; color:white; padding:8px 10px; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.8px; text-align:center; }
  .gains-table td { background:#0e1117; color:#CCC; padding:9px 10px; text-align:center; border-bottom:1px solid #1e2530; transition: background 0.2s; }
  .gains-table tr:hover td { background:#161b22; color:#FFF; }
  .gains-table .pos { color:#44dd88; font-weight:700; }
  .gains-table .neg { color:#ff4444; font-weight:700; }
  .gains-table .highlight td { background:#0e0000 !important; border-left:3px solid #D90429; }
  .pub-badge { display:inline-block; background:#1a0800; border:1px solid #cc5500; color:#ff9944; font-size:0.68rem; font-weight:700; padding:2px 8px; border-radius:10px; }

  /* TITRES SHOPIFY */
  .titre-option {
    background:#0e1117; border:1px solid #2a3140; border-radius:12px;
    padding:0.9rem 1.1rem; margin-bottom:0.6rem;
    transition: all 0.25s ease; animation: fadeInLeft 0.5s ease both;
  }
  .titre-option:hover { border-color:#D90429; transform:translateX(6px); background:#0e0000; }
  .titre-option .num { color:#D90429; font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.25rem; }
  .titre-option .texte { color:#FFF; font-size:1rem; font-weight:700; line-height:1.4; }

  /* PARAGRAPHES SHOPIFY */
  .para-card {
    background:#0e1117; border-left:4px solid #D90429; border-radius:0 12px 12px 0;
    padding:1rem 1.2rem; margin-bottom:0.75rem;
    transition: all 0.25s ease; animation: fadeInUp 0.5s ease both;
  }
  .para-card:hover { background:#0e0000; transform:translateX(5px); box-shadow:0 4px 20px rgba(217,4,41,0.1); }
  .para-card .para-titre { color:#D90429; font-weight:800; font-size:0.92rem; margin-bottom:0.5rem; }
  .para-card .para-texte { color:#CCC; font-size:0.88rem; line-height:1.75; }

  /* FACEBOOK ADS */
  .ad-block {
    background:#161b22; border:1px solid #2a3140; border-radius:12px;
    padding:1.2rem; margin-bottom:0.75rem;
    transition: all 0.25s ease; animation: fadeInUp 0.5s ease both;
  }
  .ad-block:hover { border-color:#D90429; box-shadow:0 6px 25px rgba(217,4,41,0.12); transform:translateY(-2px); }
  .ad-accroche { color:#ff9944; font-weight:800; font-size:1rem; margin-bottom:0.5rem; }
  .ad-texte { color:#CCC; font-size:0.9rem; line-height:1.9; white-space:pre-wrap; }

  /* SCRIPTS */
  .script-block {
    background:#161b22; border:1px solid #2a3140; border-radius:12px;
    padding:1.4rem; margin-bottom:1rem;
    transition: all 0.25s ease; animation: fadeInUp 0.5s ease both;
  }
  .script-block:hover { border-color:#D90429; box-shadow:0 6px 25px rgba(217,4,41,0.1); }
  .script-label { color:#D90429; font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.6rem; padding-bottom:0.4rem; border-bottom:1px solid #2a3140; }
  .script-texte { color:#CCC; font-size:0.92rem; line-height:2; white-space:pre-wrap; }

  /* OFFRES */
  .offre-card {
    background:linear-gradient(135deg,#050f00,#0a1800); border:1px solid #336600;
    border-radius:14px; padding:1.2rem; margin-bottom:0.7rem;
    transition: all 0.25s ease; animation: fadeInUp 0.5s ease both;
  }
  .offre-card:hover { transform:translateY(-4px); box-shadow:0 10px 30px rgba(51,102,0,0.25); border-color:#55aa00; }
  .offre-card .offre-titre { color:#77dd22; font-weight:900; font-size:0.92rem; margin-bottom:0.35rem; }
  .offre-card .offre-desc { color:#BBB; font-size:0.85rem; line-height:1.7; }
  .offre-card .offre-prix { color:#55dd88; font-weight:700; font-size:0.78rem; margin-top:0.4rem; }

  .golden-rule { background:linear-gradient(135deg,#0e0000,#1a0800); border:1px solid #cc5500; border-radius:12px; padding:0.9rem 1.1rem; margin-bottom:1rem; }
  .golden-rule p { color:#ffaa55; font-size:0.8rem; margin:0; line-height:1.8; }

  .export-section { background:linear-gradient(135deg,#0a0000,#150000); border:2px solid #D90429; border-radius:16px; padding:1.4rem; margin-top:2rem; text-align:center; animation: fadeInUp 0.6s ease both; }

  /* ZONES DE COPIE (st.text_area) */
  .stTextArea textarea {
    background-color: #0a0d12 !important;
    color: #44dd88 !important;
    border: 1px dashed #2a3140 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', 'Courier New', monospace !important;
    font-size: 0.78rem !important;
    line-height: 1.6 !important;
    resize: none !important;
  }
  .stTextArea textarea:focus {
    border-color: #44dd88 !important;
    box-shadow: 0 0 0 2px rgba(68,221,136,0.15) !important;
  }
  .stTextArea label {
    color: #555 !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
  }

  #MainMenu, footer, header { visibility:hidden; }
  label { color:#AAAAAA !important; font-weight:600 !important; font-size:0.83rem !important; }

  @media (max-width:768px) {
    .block-container { padding-left:0.4rem !important; padding-right:0.4rem !important; }
    .hero-banner { padding:1.2rem 0.75rem; }
    .stTabs [data-baseweb="tab"] { padding:0.3rem 0.35rem !important; font-size:0.58rem !important; }
    .gains-table th, .gains-table td { padding:6px 4px; font-size:0.65rem; }
  }
</style>

<script>
// Copier universel — PC, iPhone, Android
function copyText(text, btnId) {
  var btn = document.getElementById(btnId);
  function success() {
    if (btn) {
      btn.innerHTML = '✅ Copié !';
      btn.style.color = '#44dd88';
      btn.style.borderColor = '#44dd88';
      btn.style.background = '#001a00';
      setTimeout(function() {
        btn.innerHTML = '📋 Copier';
        btn.style.color = '#888';
        btn.style.borderColor = '#2a3140';
        btn.style.background = '#1a1a2a';
      }, 2500);
    }
  }
  // Méthode 1 : Clipboard API moderne
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(success).catch(fallback);
  } else {
    fallback();
  }
  // Méthode 2 : fallback textarea (iOS Safari, Android WebView)
  function fallback() {
    try {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;top:0;left:0;width:2em;height:2em;opacity:0;';
      document.body.appendChild(ta);
      if (navigator.userAgent.match(/ipad|iphone/i)) {
        var range = document.createRange();
        range.selectNodeContents(ta);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        ta.setSelectionRange(0, 999999);
      } else {
        ta.select();
      }
      document.execCommand('copy');
      document.body.removeChild(ta);
      success();
    } catch(e) {
      if (btn) { btn.innerHTML = '⚠️ Manuel'; }
    }
  }
}
</script>
""", unsafe_allow_html=True)

# ── UTILITAIRES ───────────────────────────────────────────────────────────────

def section_header(title):
    """Entête de carte — le bouton copier est remplacé par st.code() natif."""
    return (f'<div class="card-header">'
            f'<span class="card-title">{title}</span>'
            f'</div>')

def copy_block(text: str, label: str = "📋 Copier"):
    """
    Zone de texte sélectionnable — 100% fiable PC, iPhone, Android.
    Ctrl+A ou appui long -> Tout sélectionner -> Copier.
    """
    lines  = max(2, min(6, text.count("\n") + 1))
    height = lines * 26 + 16
    st.text_area(
        label,
        value=text,
        height=height,
        key=f"copy_{hash(text) & 0xFFFFFF}_{label[:10]}",
        help="Clic dans la zone → Ctrl+A (PC) ou appui long (mobile) → Copier"
    )

def save_to_history(name, score, data, prix_achat):
    entry = {
        "name": name, "score": score, "data": data,
        "prix_achat": prix_achat, "ts": datetime.now().strftime("%H:%M")
    }
    existing = [h for h in st.session_state["history"] if h["name"] != name]
    st.session_state["history"] = [entry] + existing[:7]

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

    history = st.session_state["history"]   # lecture directe — stable
    if not history:
        st.markdown(
            '<p style="color:#333;font-size:0.8rem;font-style:italic;">Aucune analyse</p>',
            unsafe_allow_html=True
        )
    else:
        for i, h in enumerate(history):
            short = h["name"][:16] + ("…" if len(h["name"]) > 16 else "")
            label = f"{'⭐' if i == 0 else '📦'} {short}"
            help_txt = f"Score {h['score']}/10 · {h.get('ts','')}"
            if st.button(label, key=f"hist_{i}_{h['name']}", help=help_txt):
                # Chargement sécurisé sans reset de l'historique
                st.session_state["result"]         = h["data"]
                st.session_state["analyzed"]       = True
                st.session_state["active_product"] = h["name"]
                st.session_state["active_price"]   = h["prix_achat"]
                st.rerun()

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
        cols_img = st.columns(len(uploaded_files[:3]))
        for i, f in enumerate(uploaded_files[:3]):
            with cols_img[i]:
                st.image(f, use_column_width=True)

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

③ SCRIPTS VOIX-OFF — 3 scripts, ENVIRON 130 MOTS CHACUN (30 secondes à 1 minute) :
   • Texte fluide et naturel, SANS balises techniques (pas de "Hook:", "CTA:", "Act 1:", etc.).
   • Si type WOW   → Hook visuel choc → Problème rapide (1-2 phrases) → Solution visuelle → Preuve sociale locale (ex: "M. Kofi de Lomé a testé et validé...") → CTA urgent.
   • Si type P-S   → Hook douleur/frustration → Amplification frustration → Ta Solution précise → Témoignage local (ex: "Mme Aminata d'Abidjan ne jure que par ça...") → CTA.
   • Exemple de ton attendu : "Tu veux vraiment arrêter la cigarette ou tu attends qu'elle détruise ton souffle ? Chaque cigarette t'enchaîne un peu plus. Reprends le contrôle avec le patch Anti-Smoke..."

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
    {{"angle": "Script Émotionnel",      "texte_complet": "Texte fluide ENVIRON 130 MOTS, sans aucune balise, naturel et humain, adapté marché africain"}},
    {{"angle": "Script Bénéfice Direct", "texte_complet": "Texte fluide ENVIRON 130 MOTS, angle différent, preuve sociale africaine"}},
    {{"angle": "Script Urgence & Statut","texte_complet": "Texte fluide ENVIRON 130 MOTS, joue sur statut social et urgence africaine"}}
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
                    "shopify","facebook_ads","scripts"]:
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
    <div style="background:#161b22;border:1px solid #2a3140;border-radius:10px;
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

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Stratégie", "🎁 Offres", "🛍️ Shopify", "📣 Facebook Ads", "🎙️ Voix-Off"
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
            st.markdown(f"""<div class="result-card">
              {section_header("💡 Verdict IA")}
              <p style="line-height:1.75;font-size:0.88rem;color:#CCC;">{verdict}</p>
            </div>""", unsafe_allow_html=True)
            copy_block(verdict, "📋 Copier le verdict")

        if score < 9:
            amelios = data.get("ameliorations", [])
            amelios_txt = "\n".join([f"- {a}" for a in amelios])
            st.markdown(f"""<div class="amelioration-card">
              {section_header("⚠️ Comment Booster ce Produit ?")}
              {"".join([f'<p style="margin:0.3rem 0;font-size:0.86rem;color:#CCC;">🔧 {a}</p>' for a in amelios])}
            </div>""", unsafe_allow_html=True)
            copy_block(amelios_txt, "📋 Copier les conseils")

        st.markdown(f"""<div style="display:flex;gap:0.45rem;flex-wrap:wrap;margin-bottom:1rem;">
          <div class="metric-item"><div class="m-label">Budget Pub</div><div class="m-value red">{get_pub_budget(aventes)}</div></div>
          <div class="metric-item"><div class="m-label">Frais/vente</div><div class="m-value">5 000 F</div></div>
          <div class="metric-item"><div class="m-label">Marge brute</div><div class="m-value">8K–12K F</div></div>
          <div class="metric-item"><div class="m-label">Type</div><div class="m-value red">{"⚡ WOW" if type_produit=="wow" else "🎯 P-S"}</div></div>
        </div>""", unsafe_allow_html=True)

        # ── TABLEAU RENTABILITÉ LABO ──────────────────────────────────────────
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
              <td>{ca:,.0f} F</td>
              <td>{cout_global:,.0f} F</td>
              <td class="{cls}">{sign}{bn:,.0f} F</td>
            </tr>"""

        st.markdown(f"""<div class="result-card">
          <div class="card-header">
            <span class="card-title">💰 Calculateur de Rentabilité LABO</span>
          </div>
          <div style="overflow-x:auto;">
          <table class="gains-table">
            <thead>
              <tr>
                <th>Ventes</th><th>Budget Pub</th><th>CA</th>
                <th>Coût Global</th><th>Bénéfice Net</th>
              </tr>
            </thead>
            <tbody>{rows_html}</tbody>
          </table></div>
          <p style="color:#333;font-size:0.68rem;margin-top:0.5rem;">
            * Frais fixes = 5 000 FCFA/vente (2 000 livraison + 2 000 pub + 1 000 closing) · Prix moyen {apmoy:,.0f} FCFA
          </p>
        </div>""", unsafe_allow_html=True)

        cp_col, cd_col = st.columns(2, gap="medium")
        with cp_col:
            peurs     = data.get("peurs", [])
            peurs_txt = "\n".join(peurs)
            st.markdown(f"""<div class="result-card">
              {section_header("😰 Peurs du Client")}
              {"".join([f'<p style="margin:0.3rem 0;font-size:0.86rem;">🔴 {p}</p>' for p in peurs])}
            </div>""", unsafe_allow_html=True)
            copy_block(peurs_txt, "📋 Copier les peurs")
        with cd_col:
            desirs     = data.get("desirs", [])
            desirs_txt = "\n".join(desirs)
            st.markdown(f"""<div class="result-card">
              {section_header("✨ Désirs du Client")}
              {"".join([f'<p style="margin:0.3rem 0;font-size:0.86rem;">💚 {d}</p>' for d in desirs])}
            </div>""", unsafe_allow_html=True)
            copy_block(desirs_txt, "📋 Copier les désirs")

        public = data.get("public_cible", "")
        st.markdown(f"""<div class="result-card">
          {section_header("🎯 Public Cible")}
          <p style="line-height:1.8;font-size:0.88rem;color:#CCC;">{public}</p>
        </div>""", unsafe_allow_html=True)
        copy_block(public, "📋 Copier le public cible")

        mots = data.get("mots_cles", [])
        if mots:
            badges = "".join([
                f'<span style="background:#1a0000;border:1px solid #D90429;color:#FFF;'
                f'padding:3px 11px;border-radius:20px;font-size:0.75rem;margin:3px;display:inline-block;">{m}</span>'
                for m in mots
            ])
            st.markdown(f"""<div class="result-card">
              {section_header("🔍 Mots-Clés")}
              <div>{badges}</div>
            </div>""", unsafe_allow_html=True)
            copy_block(" · ".join(mots), "📋 Copier les mots-clés")

    # ── TAB 2 : OFFRES ───────────────────────────────────────────────────────
    with tab2:
        st.markdown("""<div style="background:#050f00;border:1px solid #336600;border-radius:12px;
          padding:0.75rem 1rem;margin-bottom:1rem;animation:fadeInDown 0.5s ease both;">
          <p style="color:#77dd22;font-weight:700;margin:0;font-size:0.85rem;">
            🎁 Offres conçues pour booster tes ventes — Marché Africain Francophone
          </p></div>""", unsafe_allow_html=True)

        offres_list = data.get("offres", [])
        if not offres_list:
            st.warning("⚠️ Aucune offre générée. Relance une analyse.")
        for i, o in enumerate(offres_list):
            offre_txt = f"{o.get('nom','')}\n{o.get('description','')}\nPrix : {o.get('prix_suggere','')}"
            st.markdown(f"""<div class="offre-card">
              <div class="offre-titre">🎁 {o.get('nom','')}</div>
              <div class="offre-desc">{o.get('description','')}</div>
              <div class="offre-prix">💰 {o.get('prix_suggere','')} · {o.get('argument','')}</div>
            </div>""", unsafe_allow_html=True)
            copy_block(offre_txt, f"📋 Copier Offre {i+1}")

    # ── TAB 3 : SHOPIFY ──────────────────────────────────────────────────────
    with tab3:
        shopify = data.get("shopify", {})

        # 3 TITRES
        titres_txt = "\n".join([t.get("titre", "") for t in shopify.get("titres", [])])
        st.markdown(f"""<div class="result-card">
          {section_header("🏷️ 3 Titres Magnétiques")}
        """, unsafe_allow_html=True)
        for i, t in enumerate(shopify.get("titres", [])):
            st.markdown(f"""<div class="titre-option">
              <div class="num">Option {i+1} — {t.get("angle","")}</div>
              <div class="texte">{t.get("titre","")}</div>
            </div>""", unsafe_allow_html=True)
            copy_block(t.get("titre",""), f"📋 Copier Titre {i+1}")
        st.markdown('</div>', unsafe_allow_html=True)
        copy_block(titres_txt, "📋 Copier les 3 titres")

        # 6 PARAGRAPHES
        all_paras_txt = "\n\n".join([
            f"{p.get('titre','')}\n{p.get('texte','')}"
            for p in shopify.get("paragraphes", [])
        ])
        st.markdown(f"""<div class="result-card">
          {section_header("📝 Fiche Produit — 6 Paragraphes")}
        """, unsafe_allow_html=True)
        for j, para in enumerate(shopify.get("paragraphes", [])):
            para_txt   = f"{para.get('titre','')}\n{para.get('texte','')}"
            texte_html = para.get("texte","").replace("\n", "<br>")
            st.markdown(f"""<div class="para-card">
              <div class="para-titre">{para.get("titre","")}</div>
              <div class="para-texte">{texte_html}</div>
            </div>""", unsafe_allow_html=True)
            copy_block(para_txt, f"📋 Copier §{j+1}")
        st.markdown('</div>', unsafe_allow_html=True)
        copy_block(all_paras_txt, "📋 Copier les 6 paragraphes complets")

    # ── TAB 4 : FACEBOOK ADS ─────────────────────────────────────────────────
    with tab4:
        st.markdown("""<div style="background:#0e0000;border:1px solid #330000;border-radius:10px;
          padding:0.65rem 1rem;margin-bottom:1rem;animation:fadeInDown 0.5s ease both;">
          <p style="color:#888;font-size:0.78rem;margin:0;">
            💡 3 variantes · 1 titre choc + texte max 5 lignes · Prêtes pour Facebook Ads Manager
          </p></div>""", unsafe_allow_html=True)

        fb_ads = data.get("facebook_ads", [])

        # ── Diagnostic si vide ──────────────────────────────────────────────
        if not fb_ads:
            st.error("⚠️ Les Facebook Ads n'ont pas été générées (JSON tronqué ou clé manquante).")
            st.info("💡 Relance l'analyse — le modèle a parfois besoin d'une seconde tentative.")
            # Affiche le contenu brut pour debug
            with st.expander("🔍 Debug — contenu reçu de l'IA"):
                st.json(data)
        else:
            for i, ad in enumerate(fb_ads):
                accroche   = ad.get("accroche", ad.get("titre", ad.get("headline", "")))
                texte      = ad.get("texte", ad.get("text", ad.get("body", ad.get("contenu", ""))))
                angle      = ad.get("angle", f"Variante {i+1}")
                full       = f"{accroche}\n\n{texte}"
                texte_html = texte.replace("\n", "<br>")
                st.markdown(f"""<div class="ad-block">
                  <div style="margin-bottom:0.5rem;">
                    <span style="color:#D90429;font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;">
                      📣 Variante {i+1} — {angle}
                    </span>
                  </div>
                  <div class="ad-accroche">{accroche}</div>
                  <div class="ad-texte">{texte_html}</div>
                </div>""", unsafe_allow_html=True)
                copy_block(full, f"📋 Copier Variante {i+1}")

    # ── TAB 5 : VOIX-OFF ─────────────────────────────────────────────────────
    with tab5:
        type_label = "⚡ PRODUIT WOW" if type_produit == "wow" else "🎯 PROBLÈME-SOLUTION"
        st.markdown(f"""<div style="background:#0e0000;border:1px solid #330000;border-radius:10px;
          padding:0.65rem 1rem;margin-bottom:1rem;animation:fadeInDown 0.5s ease both;">
          <p style="color:#D90429;font-weight:700;margin:0;font-size:0.82rem;">
            Type : {type_label} · ~130 mots · Bloc fluide prêt à lire en voix-off
          </p></div>""", unsafe_allow_html=True)

        scripts = data.get("scripts", [])
        if not scripts:
            st.warning("⚠️ Scripts non générés. Relance l'analyse.")
        for i, script in enumerate(scripts):
            texte_script = script.get("texte_complet", script.get("texte", ""))
            word_count   = len(texte_script.split())
            st.markdown(f"""<div class="script-block">
              <div style="display:flex;justify-content:space-between;align-items:center;
                          margin-bottom:0.6rem;padding-bottom:0.4rem;border-bottom:1px solid #2a3140;">
                <span class="script-label" style="margin:0;border:none;padding:0;">
                  🎙️ {script.get("angle",f"Script {i+1}")}
                </span>
                <span style="color:#444;font-size:0.65rem;">{word_count} mots</span>
              </div>
              <div class="script-texte">{texte_script}</div>
            </div>""", unsafe_allow_html=True)
            copy_block(texte_script, f"📋 Copier Script {i+1}")

    # ── EXPORT ───────────────────────────────────────────────────────────────
    st.markdown("---")
    export_txt = build_export(aname, aprice, apmin, apmax, data)
    st.markdown("""<div class="export-section">
      <p style="color:#D90429;font-weight:800;font-size:1rem;margin:0 0 0.25rem;">📦 Pack Marketing Complet</p>
      <p style="color:#444;font-size:0.8rem;margin:0 0 1rem;">Toute l'analyse exportée en fichier .txt prêt à l'emploi</p>
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
