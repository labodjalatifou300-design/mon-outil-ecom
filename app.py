import streamlit as st
import io
import re
import json
from PIL import Image
import base64
from datetime import datetime

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
    animation: fadeInDown 0.6s ease;
  }
  .hero-banner h1 { font-size: clamp(1.6rem, 5vw, 2.6rem); font-weight: 900; color: #FFFFFF; margin: 0; letter-spacing: -1px; }
  .hero-banner h1 span { color: #D90429; }
  .hero-banner .slogan { color: #888; margin: 0.4rem 0 0; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; }
  .hero-banner .sub { color: #D90429; font-size: 0.75rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-top: 0.2rem; }

  @keyframes fadeInDown { from { opacity:0; transform:translateY(-20px); } to { opacity:1; transform:translateY(0); } }
  @keyframes fadeInUp { from { opacity:0; transform:translateY(15px); } to { opacity:1; transform:translateY(0); } }
  @keyframes pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(217,4,41,0.35); } 50% { box-shadow: 0 0 0 12px rgba(217,4,41,0); } }
  @keyframes glow { 0%,100% { box-shadow: 0 0 20px rgba(217,4,41,0.2); } 50% { box-shadow: 0 0 40px rgba(217,4,41,0.6); } }

  .stTextInput input, .stNumberInput input {
    background-color: #161b22 !important; color: #FFFFFF !important;
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

  .stTabs [data-baseweb="tab-list"] {
    background: #161b22; border-radius: 14px; padding: 5px; gap: 3px;
    border: 1px solid #2a3140; flex-wrap: wrap;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #666 !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: clamp(0.62rem, 2vw, 0.8rem) !important;
    padding: 0.4rem 0.55rem !important; transition: all 0.25s ease !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #D90429, #a80220) !important;
    color: white !important; box-shadow: 0 4px 15px rgba(217,4,41,0.4) !important;
  }

  .result-card {
    background: #161b22; border: 1px solid #2a3140; border-radius: 14px;
    padding: 1.4rem; margin-bottom: 1rem; animation: fadeInUp 0.4s ease;
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  }
  .result-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(217,4,41,0.08); border-color: #3a2030; }

  .card-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #2a3140;
  }
  .card-header .card-title {
    color: #D90429; font-size: 0.8rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px; margin: 0;
  }
  .inline-copy {
    background: transparent; border: 1px solid #2a3140; color: #555;
    border-radius: 6px; padding: 3px 8px; font-size: 0.72rem; cursor: pointer;
    transition: all 0.2s ease; font-family: Inter, sans-serif; white-space: nowrap;
  }
  .inline-copy:hover { border-color: #D90429; color: #D90429; background: #1a0000; }

  .score-wrap { text-align: center; padding: 1rem 0; }
  .score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 100px; height: 100px; border-radius: 50%;
    border: 4px solid #D90429; font-size: 2.2rem; font-weight: 900;
    color: #FFFFFF; background: radial-gradient(circle, #2d0000, #0e1117);
    margin: 0 auto 0.75rem; animation: glow 2.5s infinite;
  }
  .wow-badge { display:inline-block; background:linear-gradient(135deg,#ff5500,#D90429); color:white; font-weight:800; font-size:0.75rem; padding:4px 14px; border-radius:20px; letter-spacing:1.5px; text-transform:uppercase; }
  .ps-badge { display:inline-block; background:linear-gradient(135deg,#0055bb,#003a8c); color:white; font-weight:800; font-size:0.75rem; padding:4px 14px; border-radius:20px; letter-spacing:1.5px; text-transform:uppercase; }

  .price-box {
    background: linear-gradient(135deg,#0e0000,#1a0505); border:1px solid #D90429;
    border-radius:14px; padding:1.1rem; text-align:center; margin-bottom:1rem;
    transition:transform 0.2s,box-shadow 0.2s;
  }
  .price-box:hover { transform:scale(1.04); box-shadow:0 8px 25px rgba(217,4,41,0.2); }
  .price-box .label { color:#666; font-size:0.68rem; text-transform:uppercase; letter-spacing:1px; }
  .price-box .value { color:#FFFFFF; font-size:clamp(1rem,4vw,1.4rem); font-weight:900; margin-top:3px; }
  .price-box .currency { color:#D90429; font-size:0.72rem; }

  .gains-table { width:100%; border-collapse:collapse; margin-top:0.5rem; font-size:clamp(0.72rem,2vw,0.85rem); }
  .gains-table th { background:#D90429; color:white; padding:8px 10px; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.8px; text-align:center; }
  .gains-table td { background:#0e1117; color:#CCC; padding:9px 10px; text-align:center; border-bottom:1px solid #1e2530; }
  .gains-table tr:hover td { background:#161b22; color:#FFF; }
  .gains-table .pos { color:#44dd88; font-weight:700; }
  .gains-table .neg { color:#ff4444; }

  .pub-badge { display:inline-block; background:#1a0800; border:1px solid #cc5500; color:#ff9944; font-size:0.72rem; font-weight:700; padding:3px 10px; border-radius:12px; }

  .amelioration-card { background:linear-gradient(135deg,#120f00,#1a1500); border:1px solid #cc7700; border-radius:14px; padding:1.25rem; margin-bottom:1rem; }

  .metric-item { background:#161b22; border:1px solid #2a3140; border-radius:12px; padding:0.75rem; text-align:center; flex:1; min-width:85px; transition:all 0.2s; }
  .metric-item:hover { border-color:#D90429; transform:translateY(-2px); }
  .metric-item .m-label { color:#555; font-size:0.6rem; text-transform:uppercase; letter-spacing:0.8px; }
  .metric-item .m-value { color:#FFF; font-size:clamp(0.82rem,3vw,1rem); font-weight:700; margin-top:2px; }
  .metric-item .m-value.red { color:#D90429; }

  .titre-option { background:#0e1117; border:1px solid #2a3140; border-radius:12px; padding:0.9rem 1.1rem; margin-bottom:0.5rem; transition:all 0.2s; }
  .titre-option:hover { border-color:#D90429; transform:translateX(4px); background:#0e0000; }
  .titre-option .num { color:#D90429; font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.2rem; }
  .titre-option .texte { color:#FFFFFF; font-size:0.95rem; font-weight:700; line-height:1.4; }

  .avantage-card { background:#0e1117; border-left:3px solid #D90429; border-radius:0 12px 12px 0; padding:0.85rem 1.1rem; margin-bottom:0.45rem; transition:all 0.2s; }
  .avantage-card:hover { background:#0e0000; transform:translateX(4px); }
  .avantage-card .av-titre { color:#D90429; font-weight:700; font-size:0.82rem; margin-bottom:0.15rem; }
  .avantage-card .av-texte { color:#BBB; font-size:0.85rem; line-height:1.6; }

  .ad-block { background:#161b22; border:1px solid #2a3140; border-radius:12px; padding:1.2rem; margin-bottom:0.5rem; transition:box-shadow 0.2s; }
  .ad-block:hover { box-shadow:0 6px 25px rgba(217,4,41,0.1); }
  .ad-block .angle { color:#D90429; font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem; }
  .ad-texte { color:#CCC; font-size:0.9rem; line-height:1.9; white-space:pre-wrap; }

  .script-block { background:#161b22; border:1px solid #2a3140; border-radius:12px; padding:1.4rem; margin-bottom:1rem; }
  .script-block .s-angle { color:#D90429; font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.7rem; padding-bottom:0.45rem; border-bottom:1px solid #2a3140; }
  .script-texte { color:#CCC; font-size:0.9rem; line-height:2; white-space:pre-wrap; }

  .offre-card { background:linear-gradient(135deg,#050f00,#0a1800); border:1px solid #336600; border-radius:14px; padding:1.2rem; margin-bottom:0.7rem; transition:all 0.2s; }
  .offre-card:hover { transform:translateY(-3px); box-shadow:0 8px 25px rgba(51,102,0,0.2); border-color:#55aa00; }
  .offre-card .offre-titre { color:#77dd22; font-weight:900; font-size:0.92rem; margin-bottom:0.35rem; }
  .offre-card .offre-desc { color:#BBB; font-size:0.85rem; line-height:1.7; }
  .offre-card .offre-prix { color:#55dd88; font-weight:700; font-size:0.78rem; margin-top:0.45rem; }

  .creative-card { background:linear-gradient(135deg,#000a1a,#001025); border:1px solid #0055aa; border-radius:14px; padding:1.3rem; margin-bottom:1rem; }
  .creative-card h4 { color:#3399ff; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.7rem; padding-bottom:0.45rem; border-bottom:1px solid #001a3a; }
  .prompt-box { background:#000d1a; border:1px solid #003366; border-radius:10px; padding:1rem; font-size:0.82rem; color:#aaccee; line-height:1.8; white-space:pre-wrap; }

  .golden-rule { background:linear-gradient(135deg,#0e0000,#1a0800); border:1px solid #cc5500; border-radius:12px; padding:0.9rem 1.1rem; margin-bottom:1rem; }
  .golden-rule p { color:#ffaa55; font-size:0.8rem; margin:0; line-height:1.8; }

  .export-section { background:linear-gradient(135deg,#0a0000,#150000); border:2px solid #D90429; border-radius:16px; padding:1.4rem; margin-top:2rem; text-align:center; }

  #MainMenu, footer, header { visibility:hidden; }
  label { color:#AAAAAA !important; font-weight:600 !important; font-size:0.83rem !important; }

  @media (max-width:768px) {
    .block-container { padding-left:0.4rem !important; padding-right:0.4rem !important; }
    .hero-banner { padding:1.2rem 0.75rem; }
    .stTabs [data-baseweb="tab"] { padding:0.3rem 0.35rem !important; font-size:0.58rem !important; }
    .gains-table th, .gains-table td { padding:6px 5px; font-size:0.68rem; }
  }
</style>
""", unsafe_allow_html=True)

# ── UTILITAIRES ───────────────────────────────────────────────────────────────

def inline_copy(text, uid):
    safe = text.replace("\\","\\\\").replace("`","\\`").replace("${","\\${").replace("\n","\\n")
    return f"""<button onclick="(function(){{
        navigator.clipboard.writeText(`{safe}`).then(()=>{{
          var b=document.getElementById('ic_{uid}');
          b.innerHTML='✅'; b.style.color='#44dd88'; b.style.borderColor='#44dd88';
          setTimeout(()=>{{b.innerHTML='📋';b.style.color='#555';b.style.borderColor='#2a3140';}},2000);
        }});
      }})()" id="ic_{uid}" class="inline-copy" title="Copier">📋</button>"""

def card_with_copy(title, content_html, copy_text, uid):
    return f"""<div class="result-card">
      <div class="card-header">
        <span class="card-title">{title}</span>
        {inline_copy(copy_text, uid)}
      </div>
      {content_html}
    </div>"""

def save_to_history(name, score, data, prix_achat):
    if "history" not in st.session_state:
        st.session_state["history"] = []
    entry = {"name": name, "score": score, "data": data, "prix_achat": prix_achat, "ts": datetime.now().strftime("%H:%M")}
    existing = [h for h in st.session_state["history"] if h["name"] != name]
    st.session_state["history"] = [entry] + existing[:7]

def get_pub_budget(ventes):
    if ventes <= 10: return "5$–7$/jour"
    elif ventes <= 20: return "7$–10$/jour"
    else: return "15$–20$/jour"

def build_export(product_name, purchase_price, price_min, price_max, data):
    lines = []
    sep = "=" * 60
    lines += [sep, "  ECOMASTER LABO PRO — PACK MARKETING COMPLET",
              f"  Créé par LABO · {datetime.now().strftime('%d/%m/%Y %H:%M')}",
              f"  Produit : {product_name}",
              f"  Prix achat : {purchase_price:,} FCFA | Vente : {price_min:,}–{price_max:,} FCFA",
              f"  Score : {data.get('score','?')}/10 | Type : {data.get('type_produit','').upper()}", sep, ""]
    lines += ["\n📊 STRATÉGIE", "-"*40,
              f"Verdict : {data.get('score_justification','')}",
              f"\nPublic cible : {data.get('public_cible','')}",
              "\nPeurs :"] + [f"  - {p}" for p in data.get("peurs",[])]
    lines += ["\nDésirs :"] + [f"  - {d}" for d in data.get("desirs",[])]
    lines += ["\n\n🎁 OFFRES", "-"*40]
    for i, o in enumerate(data.get("offres",[])):
        lines += [f"Offre {i+1} — {o.get('nom','')}",
                  f"  {o.get('description','')}",
                  f"  Prix : {o.get('prix_suggere','')} | {o.get('argument','')}", ""]
    lines += ["\n🛍️ SHOPIFY", "-"*40, "Titres :"]
    for t in data.get("shopify",{}).get("titres",[]):
        lines.append(f"  [{t.get('angle','')}] {t.get('titre','')}")
    lines.append("\nAvantages :")
    for av in data.get("shopify",{}).get("avantages",[]):
        lines.append(f"  ✦ {av.get('titre','')} : {av.get('texte','')}")
    lines += ["\n\n📣 FACEBOOK ADS", "-"*40]
    for i, ad in enumerate(data.get("facebook_ads",[])):
        lines += [f"--- Ad Copy {i+1} — {ad.get('angle','')} ---", ad.get("texte",""), ""]
    lines += ["\n🎙️ SCRIPTS VOIX-OFF", "-"*40]
    for i, s in enumerate(data.get("scripts",[])):
        lines += [f"--- Script {i+1} — {s.get('angle','')} ---", s.get("texte_complet",""), ""]
    lines += ["", sep, "  Généré par EcoMaster Labo Pro — e-com Family Tool by LABO", sep]
    return "\n".join(lines)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="padding:0.5rem 0 0.75rem;">
      <p style="color:#D90429;font-weight:800;font-size:1rem;margin:0;">🚀 EcoMaster Labo Pro</p>
      <p style="color:#333;font-size:0.68rem;margin:0;">by LABO · v4.0 Elite</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""<p style="color:#555;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.6rem;">🕐 Historique</p>""", unsafe_allow_html=True)
    history = st.session_state.get("history", [])
    if not history:
        st.markdown("""<p style="color:#333;font-size:0.8rem;font-style:italic;">Aucune analyse</p>""", unsafe_allow_html=True)
    else:
        for i, h in enumerate(history):
            label = f"{'⭐' if i==0 else '📦'} {h['name'][:15]}{'…' if len(h['name'])>15 else ''}"
            if st.button(label, key=f"hist_{i}", help=f"Score {h['score']}/10 · {h.get('ts','')}"):
                st.session_state["result"] = h["data"]
                st.session_state["analyzed"] = True
                st.session_state["active_product"] = h["name"]
                st.session_state["active_price"] = h["prix_achat"]
                st.rerun()
    st.markdown("---")
    st.markdown("""<div class="golden-rule">
      <p>💡 <b style="color:#ffcc44;">Règle d'or :</b><br>
      Budget test : <b style="color:#ff8844;">4$–7$/jour</b><br>
      sur <b>1 seule créative</b> Facebook.<br><br>
      Prix vente = achat + <b style="color:#ff8844;">8K–12K FCFA</b><br>
      <span style="color:#444;font-size:0.72rem;">(pub+livraison+closing+marge)</span></p>
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
    default_name = st.session_state.get("active_product", "")
    default_price = st.session_state.get("active_price", 5000)
    product_name = st.text_input("📦 Nom du Produit", value=default_name, placeholder="Ex: Pince Multifonction Pro")
    purchase_price = st.number_input("💰 Prix d'Achat (FCFA)", min_value=0, step=500, value=default_price)
    objectif_ventes = st.number_input("🎯 Objectif de ventes par jour", min_value=1, step=1, value=10)
with col2:
    uploaded_files = st.file_uploader("📸 Photos (1 à 3)", type=["jpg","jpeg","png","webp"], accept_multiple_files=True)
    if uploaded_files:
        cols = st.columns(len(uploaded_files[:3]))
        for i, f in enumerate(uploaded_files[:3]):
            with cols[i]:
                st.image(f, use_column_width=True)

price_min = purchase_price + 8000
price_max = purchase_price + 12000
prix_moyen = (price_min + price_max) / 2

st.markdown("<br>", unsafe_allow_html=True)
p1,p2,p3,p4 = st.columns(4, gap="small")
with p1:
    st.markdown(f"""<div class="price-box"><div class="label">💵 Prix Min</div><div class="value">{price_min:,}<span class="currency"> F</span></div></div>""", unsafe_allow_html=True)
with p2:
    st.markdown(f"""<div class="price-box"><div class="label">💵 Prix Max</div><div class="value">{price_max:,}<span class="currency"> F</span></div></div>""", unsafe_allow_html=True)
with p3:
    st.markdown(f"""<div class="price-box"><div class="label">📈 Marge</div><div class="value">8K–12K<span class="currency"> F</span></div></div>""", unsafe_allow_html=True)
with p4:
    pub_badge = get_pub_budget(objectif_ventes)
    st.markdown(f"""<div class="price-box"><div class="label">📣 Budget Pub</div><div class="value" style="color:#ff9944;font-size:1.1rem;">{pub_badge}</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

# ── PROMPT ────────────────────────────────────────────────────────────────────
def build_prompt(name, prix_achat, prix_min, prix_max):
    return f"""Tu es un expert en neuro-marketing et e-commerce pour le marché africain francophone (Côte d'Ivoire, Sénégal, Cameroun, Mali, Burkina Faso, Togo, Bénin).
Langue : français percutant, émotionnel, adapté à Facebook/WhatsApp africain.
Valeurs locales : confiance, statut social, utilité immédiate, peur de manquer.

PRODUIT : {name}
PRIX D'ACHAT : {prix_achat} FCFA
FOURCHETTE DE VENTE : {prix_min}–{prix_max} FCFA

Type : "wow" = effet visuel immédiat / "probleme_solution" = résout un problème

CONTRAINTES STRICTES :
- Shopify : EXACTEMENT 6 paragraphes, chaque paragraphe avec un titre en gras, MAXIMUM 4 phrases par paragraphe
- Facebook Ads : 3 variantes, émotionnel et fun, MAXIMUM 5 lignes, inclure un titre accrocheur (ex: 🔥 PROMO FLASH, ⚠️ STOCK LIMITÉ)
- Scripts voix-off 30s-1min :
  * Si WOW : Hook choc → Problème express → Solution visuelle → Preuve sociale (ex: "M. Kofi a testé...") → CTA urgent
  * Si PROBLÈME-SOLUTION : Hook émotionnel → Frustration → La Solution → Témoignage (ex: "Mme Aminata...") → CTA urgent

Réponds UNIQUEMENT avec un JSON valide, sans texte avant ni après :

{{
  "score": 8,
  "score_justification": "analyse détaillée du potentiel africain",
  "type_produit": "wow",
  "ameliorations": ["conseil africain 1", "conseil 2", "conseil 3"],
  "public_cible": "description très détaillée : âge, sexe, situation, revenus, habitudes africaines, douleurs, rêves",
  "peurs": ["peur africaine précise 1", "peur 2", "peur 3"],
  "desirs": ["désir africain précis 1", "désir 2", "désir 3"],
  "mots_cles": ["mot1", "mot2", "mot3", "mot4", "mot5"],
  "offres": [
    {{"nom": "nom", "description": "contenu précis", "prix_suggere": "XXXX FCFA", "argument": "pourquoi ça marche"}},
    {{"nom": "nom", "description": "contenu", "prix_suggere": "XXXX FCFA", "argument": "argument"}},
    {{"nom": "nom", "description": "contenu", "prix_suggere": "XXXX FCFA", "argument": "argument"}}
  ],
  "shopify": {{
    "titres": [
      {{"angle": "Bénéfice Principal", "titre": "titre 1"}},
      {{"angle": "Curiosité / Wow", "titre": "titre 2"}},
      {{"angle": "Urgence / FOMO", "titre": "titre 3"}}
    ],
    "paragraphes": [
      {{"titre": "**Titre §1**", "texte": "4 phrases max. Accroche émotionnelle."}},
      {{"titre": "**Titre §2**", "texte": "4 phrases max. Présentation produit."}},
      {{"titre": "**Titre §3**", "texte": "4 phrases max. Bénéfice principal."}},
      {{"titre": "**Titre §4**", "texte": "4 phrases max. Preuve sociale."}},
      {{"titre": "**Titre §5**", "texte": "4 phrases max. Utilisation / mode d'emploi."}},
      {{"titre": "**Titre §6**", "texte": "4 phrases max. Urgence + CTA fort."}}
    ]
  }},
  "facebook_ads": [
    {{"angle": "Émotionnel", "accroche": "🔥 TITRE CHOC ICI", "texte": "Ad copy COMPLET max 5 lignes, émotionnel, emojis africains"}},
    {{"angle": "Preuve Sociale", "accroche": "⭐ TITRE TÉMOIGNAGE ICI", "texte": "Ad copy COMPLET max 5 lignes, témoignage africain authentique"}},
    {{"angle": "Urgence", "accroche": "⚠️ STOCK LIMITÉ / PROMO FLASH", "texte": "Ad copy COMPLET max 5 lignes, urgence, offre limitée"}}
  ],
  "scripts": [
    {{"angle": "Script Principal", "texte_complet": "SCRIPT VOIX-OFF COMPLET bloc unique 30-60sec selon type produit avec structure indiquée ci-dessus"}},
    {{"angle": "Script Émotionnel", "texte_complet": "SCRIPT VOIX-OFF COMPLET bloc unique, angle émotionnel différent"}},
    {{"angle": "Script Urgence & Statut", "texte_complet": "SCRIPT VOIX-OFF COMPLET bloc unique, joue sur statut social africain"}}
  ],
  "creative_prompt_en": "Ultra-professional product advertising photo prompt for Midjourney/Leonardo AI in African lifestyle context, studio lighting, hyperrealistic, 4K",
  "creative_prompt_fr": "Prompt image pub professionnel pour Canva AI / Adobe Firefly, contexte africain moderne, éclairage studio, ultra-réaliste 4K"
}}"""

# ── API ────────────────────────────────────────────────────────────────────────
def call_groq(prompt, images):
    from groq import Groq
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
    content = []
    for img_data in images:
        b64 = base64.b64encode(img_data).decode("utf-8")
        content.append({"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}})
    content.append({"type":"text","text":prompt})
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role":"user","content":content}],
        max_tokens=4000,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*","",raw)
    raw = re.sub(r"\s*```$","",raw)
    return json.loads(raw)

# ── ANALYSE ───────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not product_name.strip():
        st.error("⚠️ Entre le nom du produit.")
    elif not uploaded_files:
        st.error("⚠️ Upload au moins une photo.")
    else:
        images_bytes = [f.read() for f in uploaded_files[:3]]
        prompt = build_prompt(product_name, purchase_price, price_min, price_max)
        with st.spinner("🧠 Analyse IA en cours... 15-20 secondes ⏳"):
            try:
                data = call_groq(prompt, images_bytes)
                st.session_state["result"] = data
                st.session_state["analyzed"] = True
                st.session_state["active_product"] = product_name
                st.session_state["active_price"] = purchase_price
                st.session_state["active_ventes"] = objectif_ventes
                save_to_history(product_name, data.get("score","?"), data, purchase_price)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                st.session_state["analyzed"] = False

# ── RÉSULTATS ─────────────────────────────────────────────────────────────────
if st.session_state.get("analyzed") and "result" in st.session_state:
    data = st.session_state["result"]
    type_produit = data.get("type_produit","wow")
    score = int(data.get("score",8))
    active_name = st.session_state.get("active_product", product_name)
    active_price = st.session_state.get("active_price", purchase_price)
    active_ventes = st.session_state.get("active_ventes", objectif_ventes)
    active_price_min = active_price + 8000
    active_price_max = active_price + 12000
    active_prix_moyen = (active_price_min + active_price_max) / 2

    st.markdown(f"""<div style="background:#161b22;border:1px solid #2a3140;border-radius:10px;padding:0.6rem 1rem;margin-bottom:1rem;display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;">
      <span style="color:#D90429;font-size:1.1rem;">📦</span>
      <div style="flex:1;min-width:150px;">
        <p style="color:#FFF;font-weight:700;margin:0;font-size:0.92rem;">{active_name}</p>
        <p style="color:#444;font-size:0.72rem;margin:0;">Achat : {active_price:,} F · Vente : {active_price_min:,}–{active_price_max:,} FCFA</p>
      </div>
      <span style="background:#D90429;color:white;font-weight:900;padding:3px 12px;border-radius:12px;font-size:0.8rem;">{score}/10</span>
    </div>""", unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
        "📊 Stratégie","🎁 Offres","🛍️ Shopify",
        "📣 Facebook Ads","🎙️ Voix-Off","📈 Graphiques","🖼️ Créatives AI"
    ])

    # ── TAB 1 : STRATÉGIE ────────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns([1,2], gap="large")
        with c1:
            st.markdown(f"""<div class="score-wrap">
              <div class="score-badge">{score}/10</div>
              <p style="color:#444;font-size:0.72rem;margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:1px;">Potentiel</p>
              {"<div class='wow-badge'>⚡ WOW</div>" if type_produit=="wow" else "<div class='ps-badge'>🎯 PROB-SOL</div>"}
            </div>""", unsafe_allow_html=True)
        with c2:
            verdict_txt = data.get("score_justification","")
            st.markdown(card_with_copy(
                "💡 Verdict IA",
                f'<p style="line-height:1.75;font-size:0.88rem;color:#CCC;">{verdict_txt}</p>',
                verdict_txt, "verdict"
            ), unsafe_allow_html=True)

        if score < 9:
            st.markdown('<div class="amelioration-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><span class="card-title">⚠️ Comment Booster ce Produit ?</span></div>', unsafe_allow_html=True)
            for a in data.get("ameliorations",[]):
                st.markdown(f"<p style='margin:0.3rem 0;font-size:0.86rem;color:#CCC;'>🔧 {a}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""<div style="display:flex;gap:0.45rem;flex-wrap:wrap;margin-bottom:1rem;">
          <div class="metric-item"><div class="m-label">Budget Pub</div><div class="m-value red">{get_pub_budget(active_ventes)}</div></div>
          <div class="metric-item"><div class="m-label">Marge Min</div><div class="m-value">8K FCFA</div></div>
          <div class="metric-item"><div class="m-label">Marge Max</div><div class="m-value">12K FCFA</div></div>
          <div class="metric-item"><div class="m-label">Type</div><div class="m-value red">{"⚡WOW" if type_produit=="wow" else "🎯P-S"}</div></div>
        </div>""", unsafe_allow_html=True)

        # CALCULATEUR DYNAMIQUE
        st.markdown('<div class="result-card"><div class="card-header"><span class="card-title">💰 Tableau de Prévision — Rentabilité</span></div>', unsafe_allow_html=True)

        def calc_row(v, pm, pa, pub_fcfa=3000):
            ca = v * pm
            cout_prod = v * pa
            livraison = v * 2000
            closing = v * 1000
            pub = pub_fcfa
            total_couts = cout_prod + livraison + closing + pub
            benef = ca - total_couts
            return ca, cout_prod, livraison, closing, pub, benef

        pub_estimates = {range(1,11): 3000, range(11,21): 5000, range(21,200): 12000}
        pub_fcfa = 12000
        for r, val in pub_estimates.items():
            if active_ventes in r:
                pub_fcfa = val
                break

        rows_html = ""
        for v in [5, 10, active_ventes] if active_ventes not in [5,10] else [5, 10, 20]:
            ca, cp, lv, cl, pb, bn = calc_row(v, active_prix_moyen, active_price, pub_fcfa)
            color = "pos" if bn > 0 else "neg"
            sign = "+" if bn > 0 else ""
            rows_html += f"""<tr>
              <td><b>{v} ventes</b></td>
              <td>{ca:,.0f} F</td>
              <td>{cp:,.0f} F</td>
              <td>{lv:,.0f} F</td>
              <td>{cl:,.0f} F</td>
              <td><span class="pub-badge">{get_pub_budget(v)}</span></td>
              <td class="{color}">{sign}{bn:,.0f} F</td>
            </tr>"""

        # Ligne objectif si différent
        if active_ventes not in [5,10,20]:
            ca, cp, lv, cl, pb, bn = calc_row(active_ventes, active_prix_moyen, active_price, pub_fcfa)
            color = "pos" if bn > 0 else "neg"
            sign = "+" if bn > 0 else ""
            rows_html += f"""<tr style="background:#0e0000 !important;">
              <td><b>🎯 {active_ventes} ventes</b></td>
              <td>{ca:,.0f} F</td>
              <td>{cp:,.0f} F</td>
              <td>{lv:,.0f} F</td>
              <td>{cl:,.0f} F</td>
              <td><span class="pub-badge">{get_pub_budget(active_ventes)}</span></td>
              <td class="{color}">{sign}{bn:,.0f} F</td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto;">
        <table class="gains-table">
          <thead><tr>
            <th>Volume</th><th>CA</th><th>Produit</th><th>Livraison</th><th>Closing</th><th>Budget Pub</th><th>Bénéfice Net</th>
          </tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
        </div>
        <p style="color:#333;font-size:0.68rem;margin-top:0.4rem;">* Livraison : 2 000 F/vente · Closing : 1 000 F/vente · Prix moyen : {active_prix_moyen:,.0f} FCFA</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        cp_col, cd_col = st.columns(2, gap="medium")
        with cp_col:
            peurs_txt = "\n".join([f"- {p}" for p in data.get("peurs",[])])
            st.markdown(card_with_copy("😰 Peurs du Client",
                "".join([f"<p style='margin:0.3rem 0;font-size:0.86rem;'>🔴 {p}</p>" for p in data.get("peurs",[])]),
                peurs_txt, "peurs"), unsafe_allow_html=True)
        with cd_col:
            desirs_txt = "\n".join([f"- {d}" for d in data.get("desirs",[])])
            st.markdown(card_with_copy("✨ Désirs du Client",
                "".join([f"<p style='margin:0.3rem 0;font-size:0.86rem;'>💚 {d}</p>" for d in data.get("desirs",[])]),
                desirs_txt, "desirs"), unsafe_allow_html=True)

        public = data.get("public_cible","")
        st.markdown(card_with_copy("🎯 Public Cible Détaillé",
            f'<p style="line-height:1.8;font-size:0.88rem;color:#CCC;">{public}</p>',
            public, "public"), unsafe_allow_html=True)

        mots = data.get("mots_cles",[])
        if mots:
            badges = "".join([f'<span style="background:#1a0000;border:1px solid #D90429;color:#FFF;padding:3px 11px;border-radius:20px;font-size:0.75rem;margin:3px;display:inline-block;">{m}</span>' for m in mots])
            st.markdown(card_with_copy("🔍 Mots-Clés Stratégiques",
                f'<div style="flex-wrap:wrap;margin-top:0.2rem;">{badges}</div>',
                " · ".join(mots), "mots"), unsafe_allow_html=True)

    # ── TAB 2 : OFFRES ───────────────────────────────────────────────────────
    with tab2:
        st.markdown("""<div style="background:#050f00;border:1px solid #336600;border-radius:12px;padding:0.75rem 1rem;margin-bottom:1rem;">
          <p style="color:#77dd22;font-weight:700;margin:0;font-size:0.85rem;">🎁 Offres booster — Marché Africain</p>
        </div>""", unsafe_allow_html=True)
        for i, offre in enumerate(data.get("offres",[])):
            st.markdown(f"""<div class="offre-card">
              <div class="offre-titre">🎁 {offre.get("nom","")}</div>
              <div class="offre-desc">{offre.get("description","")}</div>
              <div class="offre-prix">💰 {offre.get("prix_suggere","")} · {offre.get("argument","")}</div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 3 : SHOPIFY ──────────────────────────────────────────────────────
    with tab3:
        shopify = data.get("shopify",{})
        titres_txt = "\n".join([f"[{t.get('angle','')}] {t.get('titre','')}" for t in shopify.get("titres",[])])
        st.markdown('<div class="result-card"><div class="card-header"><span class="card-title">🏷️ 3 Titres Magnétiques</span>' + inline_copy(titres_txt,"all_titres") + '</div>', unsafe_allow_html=True)
        for i, t in enumerate(shopify.get("titres",[])):
            st.markdown(f"""<div class="titre-option">
              <div class="num">Option {i+1} — {t.get("angle","")}</div>
              <div class="texte">{t.get("titre","")}</div>
            </div>""", unsafe_allow_html=True)
            st.markdown(inline_copy(t.get("titre",""), f"titre_{i}"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="result-card"><div class="card-header"><span class="card-title">📝 Fiche Shopify — 6 Paragraphes</span></div>', unsafe_allow_html=True)
        for j, para in enumerate(shopify.get("paragraphes",[])):
            para_txt = f"{para.get('titre','')}\n{para.get('texte','')}"
            st.markdown(f"""<div class="avantage-card">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <div class="av-titre">{para.get("titre","")}</div>
                {inline_copy(para_txt, f"para_{j}")}
              </div>
              <div class="av-texte">{para.get("texte","")}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 4 : FACEBOOK ADS ─────────────────────────────────────────────────
    with tab4:
        st.markdown("""<div style="background:#0e0000;border:1px solid #330000;border-radius:10px;padding:0.65rem 1rem;margin-bottom:1rem;">
          <p style="color:#888;font-size:0.78rem;margin:0;">💡 Copie chaque texte dans Facebook Ads Manager · Max 5 lignes par variante</p>
        </div>""", unsafe_allow_html=True)
        for i, ad in enumerate(data.get("facebook_ads",[])):
            texte = ad.get("texte","")
            accroche = ad.get("accroche","")
            full_ad = f"{accroche}\n{texte}"
            st.markdown(f"""<div class="ad-block">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                <div class="angle">📣 Ad {i+1} — {ad.get("angle","")}</div>
                {inline_copy(full_ad, f"ad_{i}")}
              </div>
              <p style="color:#ff9944;font-weight:700;font-size:0.88rem;margin:0 0 0.4rem;">{accroche}</p>
              <div class="ad-texte">{texte}</div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 5 : VOIX-OFF ─────────────────────────────────────────────────────
    with tab5:
        type_label = "⚡ PRODUIT WOW" if type_produit=="wow" else "🎯 PROBLÈME-SOLUTION"
        st.markdown(f"""<div style="background:#0e0000;border:1px solid #330000;border-radius:10px;padding:0.65rem 1rem;margin-bottom:1rem;">
          <p style="color:#D90429;font-weight:700;margin:0;font-size:0.82rem;">Type : {type_label} · Scripts prêts à lire (30–60 sec)</p>
        </div>""", unsafe_allow_html=True)
        for i, script in enumerate(data.get("scripts",[])):
            texte_script = script.get("texte_complet","")
            st.markdown(f"""<div class="script-block">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;padding-bottom:0.4rem;border-bottom:1px solid #2a3140;">
                <span class="s-angle" style="margin:0;border:none;padding:0;">🎙️ Script {i+1} — {script.get("angle","")}</span>
                {inline_copy(texte_script, f"script_{i}")}
              </div>
              <div class="script-texte">{texte_script}</div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 6 : GRAPHIQUES ───────────────────────────────────────────────────
    with tab6:
        try:
            import plotly.graph_objects as go
            g1, g2 = st.columns(2, gap="medium")
            with g1:
                fig_d = go.Figure(data=[go.Pie(
                    labels=["Score","Progression"],
                    values=[score, 10-score],
                    hole=0.65,
                    marker=dict(colors=["#D90429","#1a1a2e"]),
                    textinfo="none", hoverinfo="label+value"
                )])
                fig_d.update_layout(
                    paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                    font=dict(color="#FFF",family="Inter"),
                    showlegend=True,
                    legend=dict(font=dict(color="#666",size=9),orientation="h",y=-0.15),
                    annotations=[dict(text=f"<b>{score}/10</b>",x=0.5,y=0.5,font_size=18,font_color="#FFF",showarrow=False)],
                    margin=dict(t=10,b=30,l=10,r=10), height=210
                )
                st.markdown("**🎯 Score**")
                st.plotly_chart(fig_d, use_container_width=True)
            with g2:
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=score*10,
                    title={"text":"Potentiel %","font":{"color":"#666","size":11}},
                    gauge={
                        "axis":{"range":[0,100],"tickcolor":"#444","tickfont":{"color":"#444","size":9}},
                        "bar":{"color":"#D90429"}, "bgcolor":"#0e1117",
                        "steps":[{"range":[0,40],"color":"#1a0000"},{"range":[40,70],"color":"#2a0800"},{"range":[70,100],"color":"#1a1000"}],
                        "threshold":{"line":{"color":"#ff6600","width":3},"thickness":0.75,"value":80}
                    },
                    number={"suffix":"%","font":{"color":"#FFF","size":22}}
                ))
                fig_g.update_layout(paper_bgcolor="#161b22",font=dict(color="#FFF",family="Inter"),margin=dict(t=20,b=10,l=15,r=15),height=210)
                st.markdown("**📊 Jauge**")
                st.plotly_chart(fig_g, use_container_width=True)

            ventes_graph = [5,10,15,20,active_ventes] if active_ventes not in [5,10,15,20] else [5,10,15,20,25]
            ventes_graph = sorted(set(ventes_graph))
            benefices_g = [calc_row(v, active_prix_moyen, active_price, pub_fcfa)[5] for v in ventes_graph]
            colors_g = ["#44dd88" if b > 0 else "#ff4444" for b in benefices_g]
            fig_gains = go.Figure(data=[go.Bar(
                x=[f"{v}v/j" for v in ventes_graph], y=benefices_g,
                marker_color=colors_g,
                text=[f"{'+' if b>0 else ''}{b:,.0f}F" for b in benefices_g],
                textposition="outside", textfont=dict(color="#CCC",size=9)
            )])
            fig_gains.update_layout(
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(color="#888",family="Inter",size=9),
                xaxis=dict(tickfont=dict(color="#888"),gridcolor="#1e2530"),
                yaxis=dict(tickfont=dict(color="#555"),gridcolor="#1e2530"),
                margin=dict(t=25,b=10,l=10,r=10), height=200, showlegend=False
            )
            st.markdown("**💰 Bénéfice Net par Volume de Ventes**")
            st.plotly_chart(fig_gains, use_container_width=True)
        except Exception as e:
            st.warning(f"Graphiques indisponibles : {e}")

    # ── TAB 7 : CRÉATIVES AI ─────────────────────────────────────────────────
    with tab7:
        st.markdown("""<div style="background:#000a1a;border:1px solid #003399;border-radius:12px;padding:0.75rem 1rem;margin-bottom:1rem;">
          <p style="color:#3399ff;font-weight:700;margin:0;font-size:0.85rem;">🖼️ Prompts pour générer tes visuels publicitaires avec l'IA</p>
          <p style="color:#444;font-size:0.76rem;margin:0.2rem 0 0;">Copie dans Midjourney · Leonardo AI · Canva AI · Bing Image Creator</p>
        </div>""", unsafe_allow_html=True)

        prompt_en = data.get("creative_prompt_en", f"Professional product advertising photo of {active_name}, African lifestyle, studio lighting, hyperrealistic, 4K commercial")
        prompt_fr = data.get("creative_prompt_fr", f"Photo publicitaire professionnelle de {active_name}, contexte africain moderne, éclairage studio, ultra-réaliste 4K")

        st.markdown(f"""<div class="creative-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;padding-bottom:0.4rem;border-bottom:1px solid #001a3a;">
            <h4 style="margin:0;">🇬🇧 Prompt Anglais — Midjourney / Leonardo / DALL-E</h4>
            {inline_copy(prompt_en,"pen")}
          </div>
          <div class="prompt-box">{prompt_en}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="creative-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;padding-bottom:0.4rem;border-bottom:1px solid #001a3a;">
            <h4 style="margin:0;">🇫🇷 Prompt Français — Canva AI / Adobe Firefly</h4>
            {inline_copy(prompt_fr,"pfr")}
          </div>
          <div class="prompt-box">{prompt_fr}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div style="background:#0a0a0a;border:1px solid #1a1a2a;border-radius:12px;padding:1rem;margin-top:0.5rem;">
          <p style="color:#444;font-size:0.8rem;margin:0;line-height:1.9;">
            🆓 <a href="https://leonardo.ai" target="_blank" style="color:#3399ff;">Leonardo AI</a> — Gratuit, haute qualité &nbsp;·&nbsp;
            🆓 <a href="https://www.canva.com" target="_blank" style="color:#3399ff;">Canva AI</a> — Gratuit, interface FR<br>
            🆓 <a href="https://www.bing.com/images/create" target="_blank" style="color:#3399ff;">Bing Image Creator</a> — Gratuit, DALL-E &nbsp;·&nbsp;
            💎 <a href="https://www.midjourney.com" target="_blank" style="color:#3399ff;">Midjourney</a> — Payant, meilleure qualité
          </p>
        </div>""", unsafe_allow_html=True)

    # ── EXPORT ───────────────────────────────────────────────────────────────
    st.markdown("---")
    export_txt = build_export(active_name, active_price, active_price_min, active_price_max, data)
    st.markdown("""<div class="export-section">
      <p style="color:#D90429;font-weight:800;font-size:1rem;margin:0 0 0.25rem;">📦 Pack Marketing Complet</p>
      <p style="color:#444;font-size:0.8rem;margin:0 0 1rem;">Télécharge toute l'analyse en un fichier .txt prêt à l'emploi</p>
    </div>""", unsafe_allow_html=True)
    st.download_button(
        label="⬇️ TÉLÉCHARGER MON PACK MARKETING (.txt)",
        data=export_txt,
        file_name=f"pack_{active_name.replace(' ','_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════════
# GUIDE CONFIGURATION CLÉ API SUR STREAMLIT CLOUD
# ══════════════════════════════════════════════════════════════════
#
# Pour que l'application fonctionne sur Streamlit Cloud :
#
# ÉTAPE 1 — Va sur share.streamlit.io
# ÉTAPE 2 — Clique sur les 3 points "..." de ton application
# ÉTAPE 3 — Clique sur "Settings"
# ÉTAPE 4 — Clique sur l'onglet "Secrets"
# ÉTAPE 5 — Dans la zone de texte, colle EXACTEMENT ceci :
#
#   GROQ_API_KEY = "gsk_XXXXXXXXXXXXXXXXXXXXXXXX"
#
#   (Remplace par ta vraie clé obtenue sur console.groq.com)
#
# ÉTAPE 6 — Clique "Save"
# ÉTAPE 7 — Clique "Reboot app"
#
# ✅ L'application lira automatiquement la clé via st.secrets["GROQ_API_KEY"]
# ══════════════════════════════════════════════════════════════════
