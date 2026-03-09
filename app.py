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
    box-shadow: 0 0 50px rgba(217,4,41,0.12);
    animation: fadeInDown 0.6s ease;
  }
  .hero-banner h1 { font-size: clamp(1.5rem, 5vw, 2.4rem); font-weight: 900; color: #FFFFFF; margin: 0; letter-spacing: -1px; }
  .hero-banner h1 span { color: #D90429; }
  .hero-banner p { color: #666; margin: 0.5rem 0 0; font-size: 0.88rem; letter-spacing: 1px; text-transform: uppercase; }

  @keyframes fadeInDown { from { opacity:0; transform:translateY(-20px); } to { opacity:1; transform:translateY(0); } }
  @keyframes fadeInUp { from { opacity:0; transform:translateY(15px); } to { opacity:1; transform:translateY(0); } }
  @keyframes pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(217,4,41,0.35); } 50% { box-shadow: 0 0 0 12px rgba(217,4,41,0); } }
  @keyframes glow { 0%,100% { box-shadow: 0 0 20px rgba(217,4,41,0.2); } 50% { box-shadow: 0 0 35px rgba(217,4,41,0.5); } }

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
    font-size: clamp(0.65rem, 2vw, 0.82rem) !important;
    padding: 0.4rem 0.6rem !important; transition: all 0.25s ease !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #D90429, #a80220) !important;
    color: white !important; box-shadow: 0 4px 15px rgba(217,4,41,0.4) !important;
  }

  .result-card {
    background: #161b22; border: 1px solid #2a3140; border-radius: 14px;
    padding: 1.4rem; margin-bottom: 1rem; animation: fadeInUp 0.4s ease;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  }
  .result-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(217,4,41,0.08); border-color: #3a2030; }
  .result-card h3 {
    color: #D90429; font-size: 0.82rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #2a3140;
  }

  .score-wrap { text-align: center; padding: 1rem 0; }
  .score-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 100px; height: 100px; border-radius: 50%;
    border: 4px solid #D90429; font-size: 2.2rem; font-weight: 900;
    color: #FFFFFF; background: radial-gradient(circle, #2d0000, #0e1117);
    margin: 0 auto 0.75rem; animation: glow 2.5s infinite;
  }
  .wow-badge { display: inline-block; background: linear-gradient(135deg, #ff5500, #D90429); color: white; font-weight: 800; font-size: 0.78rem; padding: 5px 16px; border-radius: 20px; letter-spacing: 1.5px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(217,4,41,0.4); }
  .ps-badge { display: inline-block; background: linear-gradient(135deg, #0055bb, #003a8c); color: white; font-weight: 800; font-size: 0.78rem; padding: 5px 16px; border-radius: 20px; letter-spacing: 1.5px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,85,187,0.4); }

  .price-box {
    background: linear-gradient(135deg, #0e0000, #1a0505); border: 1px solid #D90429;
    border-radius: 14px; padding: 1.2rem; text-align: center; margin-bottom: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease; animation: fadeInUp 0.4s ease;
  }
  .price-box:hover { transform: scale(1.04); box-shadow: 0 8px 25px rgba(217,4,41,0.2); }
  .price-box .label { color: #666; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; }
  .price-box .value { color: #FFFFFF; font-size: clamp(1.1rem, 4vw, 1.5rem); font-weight: 900; margin-top: 4px; }
  .price-box .currency { color: #D90429; font-size: 0.78rem; }

  .amelioration-card { background: linear-gradient(135deg, #120f00, #1a1500); border: 1px solid #cc7700; border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem; animation: fadeInUp 0.4s ease; }
  .amelioration-card h3 { color: #ffaa00 !important; border-bottom-color: #2a2000 !important; }

  .metric-item {
    background: #161b22; border: 1px solid #2a3140; border-radius: 12px;
    padding: 0.8rem; text-align: center; flex: 1; min-width: 90px;
    transition: all 0.2s ease; animation: fadeInUp 0.4s ease;
  }
  .metric-item:hover { border-color: #D90429; transform: translateY(-2px); }
  .metric-item .m-label { color: #555; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.8px; }
  .metric-item .m-value { color: #FFF; font-size: clamp(0.85rem, 3vw, 1.1rem); font-weight: 700; margin-top: 3px; }
  .metric-item .m-value.red { color: #D90429; }
  .metric-item .m-value.green { color: #44dd88; }

  .gains-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
  .gains-table th { background: #D90429; color: white; padding: 8px 12px; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; text-align: center; }
  .gains-table td { background: #0e1117; color: #CCC; padding: 10px 12px; font-size: 0.88rem; text-align: center; border-bottom: 1px solid #2a3140; }
  .gains-table tr:hover td { background: #161b22; color: #FFF; }
  .gains-table .highlight { color: #44dd88; font-weight: 700; }

  .titre-option { background: #0e1117; border: 1px solid #2a3140; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.6rem; transition: all 0.2s ease; }
  .titre-option:hover { border-color: #D90429; transform: translateX(5px); background: #0e0000; }
  .titre-option .num { color: #D90429; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.25rem; }
  .titre-option .texte { color: #FFFFFF; font-size: 1rem; font-weight: 700; line-height: 1.4; }

  .avantage-card { background: #0e1117; border-left: 3px solid #D90429; border-radius: 0 12px 12px 0; padding: 0.9rem 1.2rem; margin-bottom: 0.5rem; transition: all 0.2s ease; }
  .avantage-card:hover { background: #0e0000; transform: translateX(5px); }
  .avantage-card .av-titre { color: #D90429; font-weight: 700; font-size: 0.85rem; margin-bottom: 0.2rem; }
  .avantage-card .av-texte { color: #BBB; font-size: 0.88rem; line-height: 1.6; }

  .ad-block { background: #161b22; border: 1px solid #2a3140; border-radius: 12px; padding: 1.25rem; margin-bottom: 0.5rem; animation: fadeInUp 0.4s ease; transition: box-shadow 0.2s ease; }
  .ad-block:hover { box-shadow: 0 6px 25px rgba(217,4,41,0.1); }
  .ad-block .angle { color: #D90429; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.6rem; }
  .ad-texte { color: #CCC; font-size: 0.92rem; line-height: 1.9; white-space: pre-wrap; }

  .script-block { background: #161b22; border: 1px solid #2a3140; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; animation: fadeInUp 0.4s ease; }
  .script-block .s-angle { color: #D90429; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #2a3140; }
  .script-texte { color: #CCC; font-size: 0.92rem; line-height: 2; white-space: pre-wrap; }

  .offre-card { background: linear-gradient(135deg, #050f00, #0a1800); border: 1px solid #336600; border-radius: 14px; padding: 1.25rem; margin-bottom: 0.75rem; transition: all 0.2s ease; animation: fadeInUp 0.4s ease; }
  .offre-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(51,102,0,0.25); border-color: #55aa00; }
  .offre-card .offre-titre { color: #77dd22; font-weight: 900; font-size: 0.95rem; margin-bottom: 0.4rem; }
  .offre-card .offre-desc { color: #BBB; font-size: 0.88rem; line-height: 1.7; }
  .offre-card .offre-prix { color: #55dd88; font-weight: 700; font-size: 0.82rem; margin-top: 0.5rem; }

  .creative-card { background: linear-gradient(135deg, #000a1a, #001025); border: 1px solid #0055aa; border-radius: 14px; padding: 1.4rem; margin-bottom: 1rem; animation: fadeInUp 0.4s ease; }
  .creative-card h4 { color: #3399ff; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #001a3a; }
  .prompt-box { background: #000d1a; border: 1px solid #003366; border-radius: 10px; padding: 1rem; font-size: 0.85rem; color: #aaccee; line-height: 1.8; white-space: pre-wrap; font-family: 'Inter', monospace; }

  .golden-rule { background: linear-gradient(135deg, #0e0000, #1a0800); border: 1px solid #cc5500; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 1rem; }
  .golden-rule p { color: #ffaa55; font-size: 0.82rem; margin: 0; line-height: 1.8; }

  .copy-wrap { margin: 0.4rem 0 0.9rem; }
  .export-section { background: linear-gradient(135deg, #0a0000, #150000); border: 2px solid #D90429; border-radius: 16px; padding: 1.5rem; margin-top: 2rem; text-align: center; }

  #MainMenu, footer, header { visibility: hidden; }
  label { color: #AAAAAA !important; font-weight: 600 !important; font-size: 0.85rem !important; }

  @media (max-width: 768px) {
    .block-container { padding-left: 0.4rem !important; padding-right: 0.4rem !important; }
    .hero-banner { padding: 1.25rem 0.75rem; }
    .stTabs [data-baseweb="tab"] { padding: 0.3rem 0.4rem !important; font-size: 0.62rem !important; }
  }
</style>
""", unsafe_allow_html=True)

# ── UTILITAIRES ───────────────────────────────────────────────────────────────

def copy_button(text, uid):
    safe = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${").replace("\n", "\\n")
    st.markdown(f"""
    <div class="copy-wrap">
      <button onclick="(function(){{
        navigator.clipboard.writeText(`{safe}`).then(()=>{{
          var b=document.getElementById('cb_{uid}');
          b.innerHTML='✅ Copié !';
          b.style.color='#44dd88'; b.style.borderColor='#44dd88';
          setTimeout(()=>{{b.innerHTML='📋 Copier';b.style.color='#888';b.style.borderColor='#2a3140';}},2500);
        }});
      }})()" id="cb_{uid}" style="
        background:transparent; color:#888; border:1px solid #2a3140;
        border-radius:8px; padding:7px 18px; font-size:0.78rem; font-weight:600;
        cursor:pointer; transition:all 0.2s ease; width:100%; font-family:Inter,sans-serif;
      ">📋 Copier</button>
    </div>""", unsafe_allow_html=True)

def save_to_history(name, score, data, prix_achat):
    if "history" not in st.session_state:
        st.session_state["history"] = []
    entry = {"name": name, "score": score, "data": data, "prix_achat": prix_achat, "ts": datetime.now().strftime("%H:%M")}
    existing = [h for h in st.session_state["history"] if h["name"] != name]
    st.session_state["history"] = [entry] + existing[:7]

def build_export(product_name, purchase_price, price_min, price_max, data):
    lines = []
    lines.append("=" * 60)
    lines.append(f"  ECOMASTER LABO PRO — PACK MARKETING")
    lines.append(f"  Produit : {product_name}")
    lines.append(f"  Prix achat : {purchase_price:,} FCFA | Vente : {price_min:,}–{price_max:,} FCFA")
    lines.append(f"  Score : {data.get('score','?')}/10 | Type : {data.get('type_produit','').upper()}")
    lines.append("=" * 60)

    lines.append("\n📊 STRATÉGIE\n")
    lines.append(f"Verdict : {data.get('score_justification','')}")
    lines.append(f"\nPublic cible : {data.get('public_cible','')}")
    lines.append("\nPeurs :")
    for p in data.get("peurs", []):
        lines.append(f"  - {p}")
    lines.append("\nDésirs :")
    for d in data.get("desirs", []):
        lines.append(f"  - {d}")

    lines.append("\n" + "─" * 60)
    lines.append("\n🎁 OFFRES\n")
    for i, o in enumerate(data.get("offres", [])):
        lines.append(f"Offre {i+1} — {o.get('nom','')}")
        lines.append(f"  {o.get('description','')}")
        lines.append(f"  Prix : {o.get('prix_suggere','')} | {o.get('argument','')}\n")

    lines.append("─" * 60)
    lines.append("\n🛍️ SHOPIFY\n")
    shopify = data.get("shopify", {})
    lines.append("Titres :")
    for t in shopify.get("titres", []):
        lines.append(f"  [{t.get('angle','')}] {t.get('titre','')}")
    lines.append("\nAvantages :")
    for av in shopify.get("avantages", []):
        lines.append(f"  ✦ {av.get('titre','')} : {av.get('texte','')}")

    lines.append("\n" + "─" * 60)
    lines.append("\n📣 FACEBOOK ADS\n")
    for i, ad in enumerate(data.get("facebook_ads", [])):
        lines.append(f"--- Ad Copy {i+1} — {ad.get('angle','')} ---")
        lines.append(ad.get("texte", ""))
        lines.append("")

    lines.append("─" * 60)
    lines.append("\n🎙️ SCRIPTS VOIX-OFF\n")
    for i, s in enumerate(data.get("scripts", [])):
        lines.append(f"--- Script {i+1} — {s.get('angle','')} ---")
        lines.append(s.get("texte_complet", ""))
        lines.append("")

    lines.append("=" * 60)
    lines.append("  Généré par EcoMaster Labo Pro — e-com Family Tool")
    lines.append("=" * 60)
    return "\n".join(lines)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="padding:0.5rem 0 1rem;">
      <p style="color:#D90429; font-weight:800; font-size:1rem; margin:0;">🚀 EcoMaster Labo Pro</p>
      <p style="color:#444; font-size:0.72rem; margin:0;">v3.0 Elite — Afrique Francophone</p>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""<p style="color:#666; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.75rem;">🕐 Historique</p>""", unsafe_allow_html=True)

    history = st.session_state.get("history", [])
    if not history:
        st.markdown("""<p style="color:#333; font-size:0.82rem; font-style:italic;">Aucune analyse encore</p>""", unsafe_allow_html=True)
    else:
        for i, h in enumerate(history):
            label = f"{'⭐' if i==0 else '📦'} {h['name'][:16]}{'...' if len(h['name'])>16 else ''}"
            sublabel = f"Score {h['score']}/10 · {h.get('ts','')}"
            if st.button(label, key=f"hist_btn_{i}", help=sublabel):
                st.session_state["result"] = h["data"]
                st.session_state["analyzed"] = True
                st.session_state["active_product"] = h["name"]
                st.session_state["active_price"] = h["prix_achat"]
                st.rerun()

    st.markdown("---")
    st.markdown("""<div class="golden-rule">
      <p>💡 <b style="color:#ffcc44;">Règle d'or :</b><br>
      Budget pub : <b style="color:#ff8844;">4$–7$/jour</b><br>
      sur <b>1 seule créative</b> pour le testing.<br><br>
      Prix vente = achat + <b style="color:#ff8844;">8 000–12 000 FCFA</b><br>
      <span style="color:#555; font-size:0.75rem;">(pub + livraison + marge inclus)</span></p>
    </div>""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero-banner">
  <h1>🚀 <span>EcoMaster</span> Labo Pro</h1>
  <p>⚡ Intelligence Artificielle · Neuro-Marketing · Afrique Francophone</p>
</div>""", unsafe_allow_html=True)

# ── CHOIX IA ──────────────────────────────────────────────────────────────────
st.markdown("""<div style="background:#161b22; border:1px solid #2a3140; border-radius:14px; padding:1.1rem 1.25rem; margin-bottom:1.25rem;">
  <p style="color:#D90429; font-weight:700; margin:0 0 0.6rem; font-size:0.88rem; text-transform:uppercase; letter-spacing:1px;">🤖 Moteur IA</p>
""", unsafe_allow_html=True)
ai_choice = st.radio("Moteur", ["🟢 Groq — LLaMA 4 (Gratuit)", "🔵 OpenAI — GPT-4o (Payant)"], horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if "Groq" in ai_choice:
    st.markdown("""<div style="background:#050f00; border:1px solid #226600; border-radius:12px; padding:0.9rem 1.25rem; margin-bottom:1.25rem;">
      <p style="color:#55dd22; font-weight:700; margin:0 0 0.2rem; font-size:0.88rem;">🔑 Clé API Groq — Gratuite</p>
      <p style="color:#555; font-size:0.78rem; margin:0;"><a href="https://console.groq.com" target="_blank" style="color:#55dd22;">console.groq.com</a> → API Keys → Create API Key</p>
    </div>""", unsafe_allow_html=True)
    api_key = st.text_input("🔑 Clé Groq", type="password", placeholder="gsk_...")
else:
    st.markdown("""<div style="background:#00050f; border:1px solid #003399; border-radius:12px; padding:0.9rem 1.25rem; margin-bottom:1.25rem;">
      <p style="color:#3399ff; font-weight:700; margin:0 0 0.2rem; font-size:0.88rem;">🔑 Clé API OpenAI</p>
      <p style="color:#555; font-size:0.78rem; margin:0;"><a href="https://platform.openai.com/api-keys" target="_blank" style="color:#3399ff;">platform.openai.com</a> → Create new secret key</p>
    </div>""", unsafe_allow_html=True)
    api_key = st.text_input("🔑 Clé OpenAI", type="password", placeholder="sk-...")

# ── INPUTS ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2], gap="large")
with col1:
    default_name = st.session_state.get("active_product", "")
    default_price = st.session_state.get("active_price", 5000)
    product_name = st.text_input("📦 Nom du Produit", value=default_name, placeholder="Ex: Pince Multifonction Pro")
    purchase_price = st.number_input("💰 Prix d'Achat (FCFA)", min_value=0, step=500, value=default_price)
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
frais_par_vente = 6000

st.markdown("<br>", unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4, gap="small")
with p1:
    st.markdown(f"""<div class="price-box"><div class="label">💵 Prix Min</div><div class="value">{price_min:,}<span class="currency"> FCFA</span></div></div>""", unsafe_allow_html=True)
with p2:
    st.markdown(f"""<div class="price-box"><div class="label">💵 Prix Max</div><div class="value">{price_max:,}<span class="currency"> FCFA</span></div></div>""", unsafe_allow_html=True)
with p3:
    st.markdown(f"""<div class="price-box"><div class="label">📈 Marge</div><div class="value">8K–12K<span class="currency"> FCFA</span></div></div>""", unsafe_allow_html=True)
with p4:
    st.markdown(f"""<div class="price-box"><div class="label">📣 Budget Pub</div><div class="value">4$–7$<span class="currency">/jour</span></div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("⚡ LANCER L'ANALYSE IA COMPLÈTE", use_container_width=True)

# ── PROMPT ────────────────────────────────────────────────────────────────────
def build_prompt(name, prix_achat, prix_min, prix_max):
    return f"""Tu es un expert en neuro-marketing et e-commerce pour le marché africain francophone (Côte d'Ivoire, Sénégal, Cameroun, Mali, Burkina Faso, Togo, Bénin, etc.).
Ton langage doit être percutant, basé sur l'émotion : confiance, utilité immédiate, statut social, peur de manquer.
Adapte tout à la réalité africaine : prix FCFA, Facebook/WhatsApp, habitudes d'achat locales.

PRODUIT : {name}
PRIX D'ACHAT : {prix_achat} FCFA
FOURCHETTE DE VENTE : {prix_min}–{prix_max} FCFA (pub + livraison + marge inclus)
BUDGET PUB : 4$–7$/jour, 1 seule créative pour testing Facebook

Type produit : "wow" = effet visuel immédiat / "probleme_solution" = résout un problème

Réponds UNIQUEMENT avec un JSON valide, sans texte avant ni après :

{{
  "score": 8,
  "score_justification": "analyse du potentiel sur le marché africain",
  "type_produit": "wow",
  "ameliorations": ["conseil 1", "conseil 2", "conseil 3"],
  "public_cible": "description très détaillée : âge, sexe, situation, revenus, habitudes africaines, douleurs, rêves",
  "peurs": ["peur africaine 1", "peur 2", "peur 3"],
  "desirs": ["désir africain 1", "désir 2", "désir 3"],
  "budget_pub_usd": "4$-7$ par jour",
  "mots_cles": ["mot-clé 1", "mot-clé 2", "mot-clé 3", "mot-clé 4", "mot-clé 5"],
  "offres": [
    {{"nom": "nom", "description": "contenu précis", "prix_suggere": "XXXX FCFA", "argument": "pourquoi ça marche en Afrique"}},
    {{"nom": "nom", "description": "contenu", "prix_suggere": "XXXX FCFA", "argument": "argument"}},
    {{"nom": "nom", "description": "contenu", "prix_suggere": "XXXX FCFA", "argument": "argument"}}
  ],
  "shopify": {{
    "titres": [
      {{"angle": "Bénéfice Principal", "titre": "titre 1"}},
      {{"angle": "Curiosité / Wow", "titre": "titre 2"}},
      {{"angle": "Urgence / FOMO", "titre": "titre 3"}}
    ],
    "avantages": [
      {{"titre": "titre", "texte": "max 2 lignes"}},
      {{"titre": "titre", "texte": "max 2 lignes"}},
      {{"titre": "titre", "texte": "max 2 lignes"}},
      {{"titre": "titre", "texte": "max 2 lignes"}},
      {{"titre": "titre", "texte": "max 2 lignes"}},
      {{"titre": "titre", "texte": "max 2 lignes"}}
    ]
  }},
  "facebook_ads": [
    {{"angle": "Émotionnel", "texte": "AD COPY COMPLET bloc unique, emojis, 5-7 lignes, ton africain direct"}},
    {{"angle": "Preuve Sociale", "texte": "AD COPY COMPLET bloc unique, témoignage africain authentique, emojis"}},
    {{"angle": "Urgence / Offre", "texte": "AD COPY COMPLET bloc unique, urgence, offre limitée, emojis"}}
  ],
  "scripts": [
    {{"angle": "Émotionnel", "texte_complet": "SCRIPT VOIX-OFF COMPLET bloc unique fluide 30-45sec. Si wow: effet visuel d'abord. Si probleme_solution: Problème→Solution→Témoignage→Fonctionnement→CTA. Ton africain chaleureux."}},
    {{"angle": "Bénéfice Direct", "texte_complet": "SCRIPT VOIX-OFF COMPLET bloc unique, angle différent."}},
    {{"angle": "Urgence & Statut", "texte_complet": "SCRIPT VOIX-OFF COMPLET bloc unique, joue sur statut social africain."}}
  ],
  "creative_prompt_en": "Ultra-professional product photo prompt in English for Midjourney/Canva AI — describe the product in a lifestyle African context, studio lighting, hyperrealistic, commercial advertising style",
  "creative_prompt_fr": "Prompt image publicitaire en français pour Canva AI / Leonardo AI — décris le produit dans un contexte africain moderne, éclairage studio, ultra-réaliste, style pub professionnelle"
}}"""

def call_groq(key, prompt, images):
    from groq import Groq
    client = Groq(api_key=key)
    content = []
    for img_data in images:
        b64 = base64.b64encode(img_data).decode("utf-8")
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
    content.append({"type": "text", "text": prompt})
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": content}],
        max_tokens=4000,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

def call_openai(key, prompt, images):
    from openai import OpenAI
    client = OpenAI(api_key=key)
    content = []
    for img_data in images:
        b64 = base64.b64encode(img_data).decode("utf-8")
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
    content.append({"type": "text", "text": prompt})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        max_tokens=4000,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

# ── ANALYSE ───────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not api_key:
        st.error("⚠️ Entre ta clé API en haut de la page !")
    elif not product_name.strip():
        st.error("⚠️ Entre le nom du produit.")
    elif not uploaded_files:
        st.error("⚠️ Upload au moins une photo.")
    else:
        images_bytes = [f.read() for f in uploaded_files[:3]]
        prompt = build_prompt(product_name, purchase_price, price_min, price_max)
        with st.spinner("🧠 Analyse IA en cours... 15-20 secondes ⏳"):
            try:
                if "Groq" in ai_choice:
                    data = call_groq(api_key, prompt, images_bytes)
                else:
                    data = call_openai(api_key, prompt, images_bytes)
                st.session_state["result"] = data
                st.session_state["analyzed"] = True
                st.session_state["active_product"] = product_name
                st.session_state["active_price"] = purchase_price
                save_to_history(product_name, data.get("score","?"), data, purchase_price)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                st.session_state["analyzed"] = False

# ── RÉSULTATS ─────────────────────────────────────────────────────────────────
if st.session_state.get("analyzed") and "result" in st.session_state:
    data = st.session_state["result"]
    type_produit = data.get("type_produit", "wow")
    score = int(data.get("score", 8))
    active_name = st.session_state.get("active_product", product_name)
    active_price = st.session_state.get("active_price", purchase_price)
    active_price_min = active_price + 8000
    active_price_max = active_price + 12000
    active_prix_moyen = (active_price_min + active_price_max) / 2

    st.markdown(f"""<div style="background:#161b22; border:1px solid #2a3140; border-radius:10px; padding:0.6rem 1rem; margin-bottom:1rem; display:flex; align-items:center; gap:0.75rem;">
      <span style="color:#D90429; font-size:1.2rem;">📦</span>
      <div>
        <p style="color:#FFF; font-weight:700; margin:0; font-size:0.95rem;">{active_name}</p>
        <p style="color:#555; font-size:0.75rem; margin:0;">Prix achat : {active_price:,} FCFA · Vente : {active_price_min:,}–{active_price_max:,} FCFA</p>
      </div>
      <span style="margin-left:auto; background:#D90429; color:white; font-weight:900; padding:3px 12px; border-radius:12px; font-size:0.82rem;">{score}/10</span>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Stratégie", "🎁 Offres", "🛍️ Shopify",
        "📣 Facebook Ads", "🎙️ Voix-Off", "📈 Graphiques", "🖼️ Créatives AI"
    ])

    # ── TAB 1 : STRATÉGIE ────────────────────────────────────────────────────
    with tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f"""<div class="score-wrap">
              <div class="score-badge">{score}/10</div>
              <p style="color:#555; font-size:0.75rem; margin-bottom:0.6rem; text-transform:uppercase; letter-spacing:1px;">Potentiel</p>
              {"<div class='wow-badge'>⚡ WOW</div>" if type_produit == "wow" else "<div class='ps-badge'>🎯 PROB-SOL</div>"}
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="result-card">
              <h3>💡 Verdict IA</h3>
              <p style="line-height:1.75; font-size:0.9rem; color:#CCC;">{data.get("score_justification","")}</p>
            </div>""", unsafe_allow_html=True)

        if score < 9:
            st.markdown('<div class="amelioration-card"><h3>⚠️ Comment Booster ce Produit ?</h3>', unsafe_allow_html=True)
            for a in data.get("ameliorations", []):
                st.markdown(f"<p style='margin:0.35rem 0; font-size:0.88rem; color:#CCC;'>🔧 {a}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""<div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:1rem;">
          <div class="metric-item"><div class="m-label">Budget Pub</div><div class="m-value red">{data.get("budget_pub_usd","4$-7$")}</div></div>
          <div class="metric-item"><div class="m-label">Marge Min</div><div class="m-value">8 000 F</div></div>
          <div class="metric-item"><div class="m-label">Marge Max</div><div class="m-value">12 000 F</div></div>
          <div class="metric-item"><div class="m-label">Type</div><div class="m-value red">{"⚡WOW" if type_produit=="wow" else "🎯P-S"}</div></div>
        </div>""", unsafe_allow_html=True)

        # CALCULATEUR DE GAINS
        st.markdown('<div class="result-card"><h3>💰 Calculateur de Gains Prévisionnels</h3>', unsafe_allow_html=True)
        gains_rows = ""
        for nb_ventes in [5, 10, 20]:
            ca = nb_ventes * active_prix_moyen
            couts = nb_ventes * (active_price + frais_par_vente)
            benefice = ca - couts
            gains_rows += f"""<tr>
              <td><b>{nb_ventes} ventes/jour</b></td>
              <td>{ca:,.0f} FCFA</td>
              <td>{couts:,.0f} FCFA</td>
              <td class="highlight">+{benefice:,.0f} FCFA</td>
            </tr>"""
        st.markdown(f"""
        <table class="gains-table">
          <thead><tr>
            <th>Volume</th><th>Chiffre d'Affaires</th><th>Coûts Totaux</th><th>Bénéfice Net</th>
          </tr></thead>
          <tbody>{gains_rows}</tbody>
        </table>
        <p style="color:#444; font-size:0.72rem; margin-top:0.5rem;">* Coûts = prix achat + 6 000 FCFA frais (pub+livraison) · Prix vente moyen = {active_prix_moyen:,.0f} FCFA</p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        cp, cd = st.columns(2, gap="medium")
        with cp:
            st.markdown('<div class="result-card"><h3>😰 Peurs du Client</h3>', unsafe_allow_html=True)
            for p in data.get("peurs", []):
                st.markdown(f"<p style='margin:0.3rem 0; font-size:0.88rem;'>🔴 {p}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with cd:
            st.markdown('<div class="result-card"><h3>✨ Désirs du Client</h3>', unsafe_allow_html=True)
            for d in data.get("desirs", []):
                st.markdown(f"<p style='margin:0.3rem 0; font-size:0.88rem;'>💚 {d}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""<div class="result-card">
          <h3>🎯 Public Cible Détaillé</h3>
          <p style="line-height:1.8; font-size:0.9rem; color:#CCC;">{data.get("public_cible","")}</p>
        </div>""", unsafe_allow_html=True)

        mots = data.get("mots_cles", [])
        if mots:
            st.markdown('<div class="result-card"><h3>🔍 Mots-Clés Stratégiques</h3>', unsafe_allow_html=True)
            badges = "".join([f'<span style="background:#1a0000; border:1px solid #D90429; color:#FFF; padding:4px 12px; border-radius:20px; font-size:0.78rem; margin:3px; display:inline-block;">{m}</span>' for m in mots])
            st.markdown(f"<div style='flex-wrap:wrap;'>{badges}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2 : OFFRES ───────────────────────────────────────────────────────
    with tab2:
        st.markdown("""<div style="background:#050f00; border:1px solid #336600; border-radius:12px; padding:0.8rem 1rem; margin-bottom:1rem;">
          <p style="color:#77dd22; font-weight:700; margin:0; font-size:0.88rem;">🎁 Offres pour booster tes ventes en Afrique</p>
        </div>""", unsafe_allow_html=True)
        for i, offre in enumerate(data.get("offres", [])):
            st.markdown(f"""<div class="offre-card">
              <div class="offre-titre">🎁 {offre.get("nom","")}</div>
              <div class="offre-desc">{offre.get("description","")}</div>
              <div class="offre-prix">💰 {offre.get("prix_suggere","")} · {offre.get("argument","")}</div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 3 : SHOPIFY ──────────────────────────────────────────────────────
    with tab3:
        shopify = data.get("shopify", {})
        st.markdown('<div class="result-card"><h3>🏷️ 3 Titres Magnétiques</h3>', unsafe_allow_html=True)
        for i, t in enumerate(shopify.get("titres", [])):
            st.markdown(f"""<div class="titre-option">
              <div class="num">Option {i+1} — {t.get("angle","")}</div>
              <div class="texte">{t.get("titre","")}</div>
            </div>""", unsafe_allow_html=True)
            copy_button(t.get("titre",""), f"titre_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="result-card"><h3>✅ Avantages Produit</h3>', unsafe_allow_html=True)
        for j, av in enumerate(shopify.get("avantages", [])):
            st.markdown(f"""<div class="avantage-card">
              <div class="av-titre">✦ {av.get("titre","")}</div>
              <div class="av-texte">{av.get("texte","")}</div>
            </div>""", unsafe_allow_html=True)
            copy_button(f"{av.get('titre','')}\n{av.get('texte','')}", f"av_{j}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 4 : FACEBOOK ADS ─────────────────────────────────────────────────
    with tab4:
        st.markdown("""<div style="background:#0e0000; border:1px solid #330000; border-radius:10px; padding:0.7rem 1rem; margin-bottom:1rem;">
          <p style="color:#888; font-size:0.8rem; margin:0;">💡 Copie chaque texte directement dans Facebook Ads Manager</p>
        </div>""", unsafe_allow_html=True)
        for i, ad in enumerate(data.get("facebook_ads", [])):
            texte = ad.get("texte", "")
            st.markdown(f"""<div class="ad-block">
              <div class="angle">📣 Ad Copy {i+1} — {ad.get("angle","")}</div>
              <div class="ad-texte">{texte}</div>
            </div>""", unsafe_allow_html=True)
            copy_button(texte, f"ad_{i}")

    # ── TAB 5 : VOIX-OFF ─────────────────────────────────────────────────────
    with tab5:
        type_label = "⚡ PRODUIT WOW" if type_produit == "wow" else "🎯 PROBLÈME-SOLUTION"
        st.markdown(f"""<div style="background:#0e0000; border:1px solid #330000; border-radius:10px; padding:0.7rem 1rem; margin-bottom:1rem;">
          <p style="color:#D90429; font-weight:700; margin:0; font-size:0.85rem;">Type : {type_label} · Scripts prêts à lire (30-45 sec)</p>
        </div>""", unsafe_allow_html=True)
        for i, script in enumerate(data.get("scripts", [])):
            texte_script = script.get("texte_complet", "")
            st.markdown(f"""<div class="script-block">
              <div class="s-angle">🎙️ Script {i+1} — {script.get("angle","")}</div>
              <div class="script-texte">{texte_script}</div>
            </div>""", unsafe_allow_html=True)
            copy_button(texte_script, f"script_{i}")

    # ── TAB 6 : GRAPHIQUES ───────────────────────────────────────────────────
    with tab6:
        try:
            import plotly.graph_objects as go
            g1, g2 = st.columns(2, gap="medium")

            with g1:
                fig_donut = go.Figure(data=[go.Pie(
                    labels=["Score actuel", "Marge possible"],
                    values=[score, 10 - score],
                    hole=0.65,
                    marker=dict(colors=["#D90429", "#1a1a2e"]),
                    textinfo="none", hoverinfo="label+value"
                )])
                fig_donut.update_layout(
                    paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                    font=dict(color="#FFF", family="Inter"),
                    showlegend=True,
                    legend=dict(font=dict(color="#666", size=9), orientation="h", y=-0.15),
                    annotations=[dict(text=f"<b>{score}/10</b>", x=0.5, y=0.5, font_size=18, font_color="#FFF", showarrow=False)],
                    margin=dict(t=10, b=30, l=10, r=10), height=220
                )
                st.markdown("**🎯 Score Potentiel**")
                st.plotly_chart(fig_donut, use_container_width=True)

            with g2:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score * 10,
                    title={"text": "Potentiel %", "font": {"color": "#666", "size": 11}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#444", "tickfont": {"color": "#444", "size": 9}},
                        "bar": {"color": "#D90429"},
                        "bgcolor": "#0e1117",
                        "steps": [
                            {"range": [0, 40], "color": "#1a0000"},
                            {"range": [40, 70], "color": "#2a0800"},
                            {"range": [70, 100], "color": "#1a1000"},
                        ],
                        "threshold": {"line": {"color": "#ff6600", "width": 3}, "thickness": 0.75, "value": 80}
                    },
                    number={"suffix": "%", "font": {"color": "#FFF", "size": 22}}
                ))
                fig_gauge.update_layout(
                    paper_bgcolor="#161b22", font=dict(color="#FFF", family="Inter"),
                    margin=dict(t=20, b=10, l=15, r=15), height=220
                )
                st.markdown("**📊 Jauge Potentiel**")
                st.plotly_chart(fig_gauge, use_container_width=True)

            # Graphique gains prévisionnels
            ventes = [5, 10, 20]
            benefices = [v * active_prix_moyen - v * (active_price + frais_par_vente) for v in ventes]
            fig_gains = go.Figure(data=[go.Bar(
                x=[f"{v} ventes/j" for v in ventes],
                y=benefices,
                marker_color=["#aa0020", "#D90429", "#ff4455"],
                text=[f"+{b:,.0f} F" for b in benefices],
                textposition="outside",
                textfont=dict(color="#FFF", size=10)
            )])
            fig_gains.update_layout(
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(color="#888", family="Inter", size=10),
                xaxis=dict(tickfont=dict(color="#888"), gridcolor="#1e2530"),
                yaxis=dict(tickfont=dict(color="#555"), gridcolor="#1e2530"),
                margin=dict(t=30, b=15, l=15, r=15), height=200,
                showlegend=False
            )
            st.markdown("**💰 Bénéfice Net Prévisionnel**")
            st.plotly_chart(fig_gains, use_container_width=True)

        except Exception as e:
            st.warning(f"Graphiques indisponibles : {e}")

    # ── TAB 7 : CRÉATIVES AI ─────────────────────────────────────────────────
    with tab7:
        st.markdown("""<div style="background:#000a1a; border:1px solid #003399; border-radius:12px; padding:0.8rem 1rem; margin-bottom:1rem;">
          <p style="color:#3399ff; font-weight:700; margin:0; font-size:0.88rem;">🖼️ Générateur de Prompts Créatives Publicitaires</p>
          <p style="color:#555; font-size:0.78rem; margin:0.2rem 0 0;">Copie ces prompts dans Midjourney, Canva AI, Leonardo AI ou DALL-E pour créer tes visuels pub</p>
        </div>""", unsafe_allow_html=True)

        prompt_en = data.get("creative_prompt_en", f"Professional product photography of {active_name}, African lifestyle context, studio lighting, hyperrealistic, commercial advertising, clean background, 4K quality")
        prompt_fr = data.get("creative_prompt_fr", f"Photo publicitaire professionnelle de {active_name}, contexte africain moderne, éclairage studio, ultra-réaliste, style pub commerciale, fond épuré, qualité 4K")

        st.markdown("""<div class="creative-card">
          <h4>🇬🇧 Prompt Anglais — Midjourney / DALL-E / Leonardo AI</h4>""", unsafe_allow_html=True)
        st.markdown(f'<div class="prompt-box">{prompt_en}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        copy_button(prompt_en, "prompt_en")

        st.markdown("""<div class="creative-card">
          <h4>🇫🇷 Prompt Français — Canva AI / Adobe Firefly</h4>""", unsafe_allow_html=True)
        st.markdown(f'<div class="prompt-box">{prompt_fr}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        copy_button(prompt_fr, "prompt_fr")

        st.markdown("""<div style="background:#0a0a0a; border:1px solid #1a1a2a; border-radius:12px; padding:1rem; margin-top:1rem;">
          <p style="color:#555; font-size:0.82rem; margin:0; line-height:1.8;">
            💡 <b style="color:#888;">Outils recommandés :</b><br>
            🆓 <a href="https://www.canva.com" target="_blank" style="color:#3399ff;">Canva AI</a> — Gratuit, interface française<br>
            🆓 <a href="https://leonardo.ai" target="_blank" style="color:#3399ff;">Leonardo AI</a> — Gratuit, très haute qualité<br>
            🆓 <a href="https://www.bing.com/images/create" target="_blank" style="color:#3399ff;">Bing Image Creator</a> — Gratuit, propulsé par DALL-E<br>
            💎 <a href="https://www.midjourney.com" target="_blank" style="color:#3399ff;">Midjourney</a> — Payant, meilleure qualité pro
          </p>
        </div>""", unsafe_allow_html=True)

    # ── EXPORT PACK MARKETING ────────────────────────────────────────────────
    st.markdown("---")
    export_txt = build_export(active_name, active_price, active_price_min, active_price_max, data)
    st.markdown("""<div class="export-section">
      <p style="color:#D90429; font-weight:800; font-size:1rem; margin:0 0 0.3rem;">📦 Exporter le Pack Marketing Complet</p>
      <p style="color:#555; font-size:0.82rem; margin:0 0 1rem;">Télécharge tous les textes générés (Analyse + Shopify + Ads + Scripts) en un seul fichier .txt</p>
    </div>""", unsafe_allow_html=True)
    st.download_button(
        label="⬇️ TÉLÉCHARGER MON PACK MARKETING COMPLET (.txt)",
        data=export_txt,
        file_name=f"pack_marketing_{active_name.replace(' ','_')}.txt",
        mime="text/plain",
        use_container_width=True
    )
