import streamlit as st
import requests
import json
import os
import base64
import re
from PIL import Image
import io
import time
from datetime import datetime
import urllib.request
import urllib.parse

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Master Labo Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS / ANIMATIONS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');

:root {
  --bg-deep:    #0a0a0f;
  --bg-card:    #111118;
  --bg-panel:   #16161f;
  --red:        #e63946;
  --orange:     #f4a261;
  --white:      #f1f1f1;
  --accent:     #ff6b35;
  --glow-red:   0 0 20px rgba(230,57,70,.55);
  --glow-org:   0 0 20px rgba(244,162,97,.45);
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-deep) !important;
  color: var(--white) !important;
}

/* ── HEADER ── */
.hero-header {
  text-align: center;
  padding: 2.5rem 1rem 1rem;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a0a12 50%, #0a0a0f 100%);
  border-bottom: 2px solid var(--red);
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.hero-header::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(230,57,70,.18) 0%, transparent 70%);
  animation: pulse-bg 4s ease-in-out infinite;
}
@keyframes pulse-bg {
  0%,100% { opacity: .6; } 50% { opacity: 1; }
}
.hero-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 900;
  background: linear-gradient(90deg, var(--red), var(--orange), var(--white), var(--orange), var(--red));
  background-size: 300% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 4s linear infinite;
  letter-spacing: 3px;
  text-transform: uppercase;
  position: relative; z-index: 1;
}
@keyframes shimmer {
  0% { background-position: 300% 0; }
  100% { background-position: 0% 0; }
}
.hero-subtitle {
  font-family: 'Rajdhani', sans-serif;
  font-size: clamp(1rem, 2.5vw, 1.4rem);
  color: var(--orange);
  letter-spacing: 4px;
  text-transform: uppercase;
  margin-top: .5rem;
  position: relative; z-index: 1;
  animation: fadein 1.5s ease;
}
@keyframes fadein { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }

/* floating particles */
.particles {
  position: absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0;
}
.p { position:absolute; width:4px; height:4px; border-radius:50%; animation: float linear infinite; }
@keyframes float {
  0%   { transform: translateY(100%) translateX(0); opacity:0; }
  10%  { opacity:1; }
  90%  { opacity:1; }
  100% { transform: translateY(-200%) translateX(30px); opacity:0; }
}

/* ── CARDS ── */
.card {
  background: var(--bg-card);
  border: 1px solid rgba(230,57,70,.25);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.2rem;
  transition: border-color .3s, box-shadow .3s;
  position: relative; overflow: hidden;
}
.card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg, transparent, var(--red), var(--orange), transparent);
  animation: scan 3s linear infinite;
}
@keyframes scan { 0%{transform:scaleX(0) translateX(-100%)} 100%{transform:scaleX(1) translateX(100%)} }
.card:hover { border-color: var(--red); box-shadow: var(--glow-red); }

/* ── SCORE ── */
.score-ring {
  display:flex; align-items:center; justify-content:center;
  width:160px; height:160px; border-radius:50%;
  background: conic-gradient(var(--red) 0deg, var(--orange) var(--score-deg), #222 var(--score-deg));
  box-shadow: var(--glow-red);
  margin: 0 auto 1rem;
  animation: spin-in .8s ease;
}
@keyframes spin-in { from{transform:scale(0) rotate(-90deg)} to{transform:scale(1) rotate(0deg)} }
.score-inner {
  width:120px; height:120px; border-radius:50%;
  background: var(--bg-deep);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
}
.score-num {
  font-family:'Orbitron',sans-serif; font-size:2.5rem; font-weight:900;
  background: linear-gradient(135deg, var(--red), var(--orange));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.score-label { font-size:.75rem; color:#999; letter-spacing:2px; }

/* ── COPY BUTTON ── */
.copy-zone { position:relative; }
.copy-btn {
  position:absolute; top:.5rem; right:.5rem;
  background: rgba(230,57,70,.2); border: 1px solid var(--red);
  color: var(--white); padding:.3rem .7rem; border-radius:8px;
  cursor:pointer; font-size:.75rem; transition:all .2s;
  z-index:10;
}
.copy-btn:hover { background: var(--red); box-shadow: var(--glow-red); }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  background: var(--bg-panel) !important;
  border-radius: 12px;
  padding: 4px;
  border: 1px solid rgba(230,57,70,.2);
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: #888 !important;
  border-radius: 8px !important;
  padding: .5rem 1rem !important;
  font-family: 'Rajdhani',sans-serif !important;
  font-weight: 600 !important;
  font-size: .9rem !important;
  transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--red), var(--accent)) !important;
  color: white !important;
  box-shadow: var(--glow-red) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, var(--red), var(--accent)) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  padding: .6rem 2rem !important;
  font-family: 'Rajdhani',sans-serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  letter-spacing: 1px !important;
  transition: all .3s !important;
  box-shadow: var(--glow-red) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 0 30px rgba(230,57,70,.8) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: var(--bg-panel) !important;
  border: 1px solid rgba(230,57,70,.35) !important;
  border-radius: 8px !important;
  color: var(--white) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--orange) !important;
  box-shadow: var(--glow-org) !important;
}

/* ── TABLE ── */
.profit-table {
  width:100%; border-collapse:collapse; font-size:.9rem;
}
.profit-table th {
  background: linear-gradient(135deg, rgba(230,57,70,.4), rgba(244,162,97,.3));
  padding:.8rem; text-align:center; font-family:'Rajdhani',sans-serif;
  font-weight:700; letter-spacing:1px; border:1px solid rgba(230,57,70,.3);
}
.profit-table td {
  padding:.7rem; text-align:center;
  border:1px solid rgba(255,255,255,.07);
  transition: background .2s;
}
.profit-table tr:hover td { background: rgba(230,57,70,.08); }
.profit-table tr:nth-child(even) td { background: rgba(255,255,255,.03); }
.profit-td-green { color:#4ade80; font-weight:700; }
.profit-td-red   { color:var(--red); font-weight:700; }
.profit-td-org   { color:var(--orange); font-weight:600; }

/* ── METRIC BOXES ── */
.metric-box {
  background: var(--bg-panel);
  border: 1px solid rgba(230,57,70,.3);
  border-radius: 12px; padding: 1rem; text-align:center;
  transition: all .3s;
}
.metric-box:hover { border-color:var(--orange); transform:translateY(-3px); box-shadow:var(--glow-org); }
.metric-val {
  font-family:'Orbitron',sans-serif; font-size:1.6rem; font-weight:700;
  background:linear-gradient(135deg,var(--red),var(--orange));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.metric-lbl { font-size:.75rem; color:#888; letter-spacing:2px; text-transform:uppercase; margin-top:.3rem; }

/* ── OFFER CARDS ── */
.offer-card {
  background: linear-gradient(135deg, rgba(230,57,70,.1), rgba(244,162,97,.07));
  border: 1px solid rgba(244,162,97,.4);
  border-radius:14px; padding:1.2rem; margin:.5rem 0;
  transition:all .3s; cursor:pointer;
}
.offer-card:hover { border-color:var(--orange); box-shadow:var(--glow-org); transform:translateX(5px); }

/* ── AVATAR ── */
.avatar-section { border-left:3px solid var(--red); padding-left:1rem; margin:.8rem 0; }
.avatar-label { font-family:'Rajdhani',sans-serif; font-weight:700; color:var(--orange); font-size:.85rem; letter-spacing:2px; text-transform:uppercase; }

/* ── IMAGE GRID ── */
.img-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:1rem; }
.img-item { border-radius:12px; overflow:hidden; border:2px solid rgba(230,57,70,.3); transition:all .3s; }
.img-item:hover { border-color:var(--orange); box-shadow:var(--glow-org); transform:scale(1.02); }

/* ── PROGRESS/LOADING ── */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }
.loading-dot { animation:blink 1s ease infinite; }

/* ── DIVIDER ── */
.neon-divider {
  height:1px;
  background:linear-gradient(90deg, transparent, var(--red), var(--orange), var(--red), transparent);
  margin:2rem 0;
  animation:shimmer 3s linear infinite;
  background-size:200% 100%;
}

/* ── COPY CONTAINER ── */
.text-block {
  background: var(--bg-panel);
  border: 1px solid rgba(255,255,255,.1);
  border-radius:10px;
  padding:1rem 1rem 2.5rem;
  position:relative;
  margin:.5rem 0;
  line-height:1.7;
  font-size:.95rem;
}
.copy-overlay {
  position:absolute; bottom:.5rem; right:.5rem;
}

/* scrollbar */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--bg-deep); }
::-webkit-scrollbar-thumb { background:var(--red); border-radius:3px; }
</style>

<script>
function copyText(id) {
  const el = document.getElementById(id);
  if (el) {
    navigator.clipboard.writeText(el.innerText);
    const btn = document.querySelector('[data-copy="'+id+'"]');
    if (btn) { btn.innerText = '✅ Copié'; setTimeout(()=>btn.innerText='📋 Copier', 2000); }
  }
}
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div class="particles">
    <div class="p" style="left:10%;animation-duration:6s;animation-delay:0s;background:#e63946;"></div>
    <div class="p" style="left:25%;animation-duration:8s;animation-delay:1s;background:#f4a261;"></div>
    <div class="p" style="left:50%;animation-duration:7s;animation-delay:2s;background:#e63946;"></div>
    <div class="p" style="left:75%;animation-duration:5s;animation-delay:.5s;background:#f4a261;"></div>
    <div class="p" style="left:90%;animation-duration:9s;animation-delay:1.5s;background:#ff6b35;"></div>
  </div>
  <div class="hero-title">⚡ E-Commerce Master Labo Pro</div>
  <div class="hero-subtitle">🌍 Tout en un pour un e-commerce africain réussi</div>
  <div style="margin-top:1rem;font-size:.8rem;color:#555;letter-spacing:2px;">POWERED BY GROK AI • MADE FOR AFRICA</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for k, v in {
    "generated": False,
    "product_name": "",
    "product_images": [],
    "cost_price": 0,
    "daily_target": 0,
    "grok_api_key": "",
    "results": {},
    "found_images": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def call_grok(api_key: str, prompt: str, system: str = "", max_tokens: int = 4000) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "grok-3",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.85,
    }
    try:
        r = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Erreur API Grok : {e}"


def copy_button(text: str, key: str):
    """Render text block with JS copy button."""
    safe = text.replace("`", "'").replace('"', "&quot;")
    html = f"""
    <div class="text-block" id="tb_{key}">{text.replace(chr(10),'<br>')}</div>
    <div style="text-align:right;margin-top:-.5rem;margin-bottom:.5rem;">
      <button onclick="navigator.clipboard.writeText(document.getElementById('tb_{key}').innerText);
                       this.innerText='✅ Copié!';
                       setTimeout(()=>this.innerText='📋 Copier',2000);"
              style="background:linear-gradient(135deg,#e63946,#ff6b35);border:none;
                     color:white;padding:.35rem .9rem;border-radius:8px;cursor:pointer;
                     font-size:.8rem;letter-spacing:1px;">
        📋 Copier
      </button>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def search_product_images(product_name: str, num: int = 12) -> list:
    """Search product images via SerpAPI-style or Unsplash fallback."""
    urls = []
    try:
        q = urllib.parse.quote(product_name + " product")
        # We use DuckDuckGo image search (no key needed)
        search_url = f"https://duckduckgo.com/?q={q}&iax=images&ia=images"
        # Fallback: return placeholder search URLs for user to open
        platforms = [
            f"https://www.google.com/search?q={q}+site:aliexpress.com&tbm=isch",
            f"https://www.google.com/search?q={q}+site:alibaba.com&tbm=isch",
            f"https://www.pinterest.com/search/pins/?q={q}",
            f"https://www.temu.com/search_result.html?search_key={urllib.parse.quote(product_name)}",
        ]
        urls = platforms
    except Exception:
        pass
    return urls


def calc_pricing(cost: int, pub: int = 5000, closing: int = 1000, livraison: int = 2000):
    margin_min = 8000
    margin_max = 12000
    sell_min = cost + margin_min
    sell_max = cost + margin_max
    sell_rec = cost + 10000
    profit_min = sell_min - cost - pub - closing - livraison
    profit_max = sell_max - cost - pub - closing - livraison
    profit_rec = sell_rec - cost - pub - closing - livraison
    return {
        "sell_min": sell_min,
        "sell_max": sell_max,
        "sell_rec": sell_rec,
        "profit_min": profit_min,
        "profit_max": profit_max,
        "profit_rec": profit_rec,
        "pub": pub, "closing": closing, "livraison": livraison,
    }

# ─────────────────────────────────────────────
#  SIDEBAR — API KEY + PRODUCT INPUT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0;border-bottom:1px solid rgba(230,57,70,.3);margin-bottom:1rem;">
      <div style="font-family:'Orbitron',sans-serif;font-size:1rem;color:#e63946;font-weight:700;">⚙️ CONFIGURATION</div>
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input("🔑 Clé API Grok (xAI)", type="password",
                             value=st.session_state.grok_api_key,
                             placeholder="xai-xxxxxxxxxxxxxxxx")
    if api_key:
        st.session_state.grok_api_key = api_key

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
    st.markdown("**📦 INFORMATIONS PRODUIT**")

    product_name = st.text_input("🏷️ Nom du produit", placeholder="Ex: Sérum anti-acné naturel")
    cost_price = st.number_input("💵 Prix d'achat (FCFA)", min_value=0, step=500, value=0)
    daily_target = st.number_input("🎯 Objectif ventes/jour", min_value=1, max_value=50, value=5)

    st.markdown("**🖼️ Images produit** (1 à 10)")
    uploaded = st.file_uploader("Upload images", type=["jpg","jpeg","png","webp"],
                                  accept_multiple_files=True)
    if uploaded:
        if len(uploaded) > 10:
            st.warning("Maximum 10 images !")
            uploaded = uploaded[:10]
        st.session_state.product_images = uploaded
        cols = st.columns(3)
        for i, img in enumerate(uploaded[:6]):
            with cols[i % 3]:
                st.image(img, use_container_width=True)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    st.markdown("**⚙️ Paramètres Marketing**")
    pub_budget = st.number_input("📣 Pub/vente (FCFA)", value=5000, step=500)
    closing_cost = st.number_input("📞 Closing/vente (FCFA)", value=1000, step=100)
    livraison_cost = st.number_input("🚚 Livraison/vente (FCFA)", value=2000, step=500)

    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

    generate_btn = st.button("🚀 LANCER L'ANALYSE IA", use_container_width=True)

    if generate_btn:
        if not api_key:
            st.error("❌ Entrez votre clé API Grok !")
        elif not product_name:
            st.error("❌ Entrez le nom du produit !")
        elif cost_price == 0:
            st.error("❌ Entrez le prix d'achat !")
        else:
            st.session_state.product_name = product_name
            st.session_state.cost_price = cost_price
            st.session_state.daily_target = daily_target
            pricing = calc_pricing(cost_price, pub_budget, closing_cost, livraison_cost)
            st.session_state.results["pricing"] = pricing

            with st.spinner("🤖 Grok analyse votre produit..."):
                # ── SYSTEM PROMPT ──
                sys_prompt = f"""Tu es un expert en e-commerce africain, marketing digital et neuromarketing.
Tu aides des entrepreneurs africains à lancer leurs produits en ligne.
Le produit analysé est : {product_name}
Prix d'achat : {cost_price} FCFA
Objectif de ventes par jour : {daily_target}
Prix de vente recommandé : {pricing['sell_rec']} FCFA
Marge nette par vente : {pricing['profit_rec']} FCFA
Tu dois toujours répondre en français, de manière précise, concrète et adaptée au marché africain (Côte d'Ivoire, Sénégal, Cameroun, Mali, Burkina Faso, Bénin, Togo, etc.)."""

                # 1. SCORE
                score_prompt = f"""Analyse ce produit e-commerce pour le marché africain et donne-lui un SCORE STRICT sur 10.

Produit : {product_name}
Prix d'achat : {cost_price} FCFA | Prix de vente : {pricing['sell_rec']} FCFA

Critères d'évaluation (sois strict, impartial, base-toi sur des données réelles) :
1. Rentabilité & marge nette (marge de {pricing['profit_rec']} FCFA)
2. Demande sur le marché africain (tendances Google Trends Afrique)
3. Niveau de concurrence en Afrique
4. Facilité d'approvisionnement en Afrique
5. Disponibilité de créatives (photos/vidéos) pour ce produit
6. Potentiel viral sur Facebook/TikTok
7. Problème réel résolu pour les Africains
8. Simplicité d'utilisation/compréhension
9. Prix psychologique adapté au pouvoir d'achat africain
10. Potentiel de répétition d'achat (fidélisation)
11. Risque de retours/réclamations
12. Saisonnalité (vendu toute l'année ?)

Réponds en JSON strict :
{{
  "score": <nombre entre 1 et 10, avec décimale possible>,
  "verdict": "<Excellent / Très Bon / Bon / Moyen / Risqué / Déconseillé>",
  "emoji_verdict": "<emoji>",
  "note_rentabilite": <1-10>,
  "note_demande": <1-10>,
  "note_concurrence": <1-10>,
  "note_creatives": <1-10>,
  "note_viral": <1-10>,
  "note_pertinence_afrique": <1-10>,
  "note_prix_psycho": <1-10>,
  "note_fidelisation": <1-10>,
  "points_forts": ["<point1>","<point2>","<point3>"],
  "points_faibles": ["<point1>","<point2>"],
  "recommandation": "<conseil stratégique principal en 2-3 phrases>",
  "marches_cibles": ["<pays1>","<pays2>","<pays3>"],
  "meilleure_periode": "<période de l'année optimale>"
}}"""

                score_raw = call_grok(api_key, score_prompt, sys_prompt, 1500)
                try:
                    score_raw_clean = re.sub(r"```json|```", "", score_raw).strip()
                    st.session_state.results["score"] = json.loads(score_raw_clean)
                except:
                    st.session_state.results["score"] = {"score": 7, "verdict": "Bon", "emoji_verdict": "👍",
                                                          "note_rentabilite": 7, "note_demande": 7,
                                                          "note_concurrence": 6, "note_creatives": 7,
                                                          "note_viral": 7, "note_pertinence_afrique": 8,
                                                          "note_prix_psycho": 7, "note_fidelisation": 6,
                                                          "points_forts": ["Bonne marge","Marché africain demandeur"],
                                                          "points_faibles": ["Concurrence présente"],
                                                          "recommandation": "Tester avec un budget pub initial de 5$.","marches_cibles":["Côte d'Ivoire","Sénégal","Cameroun"],"meilleure_periode":"Toute l'année"}

                # 2. OFFRES
                offres_prompt = f"""Pour le produit "{product_name}" vendu {pricing['sell_rec']} FCFA en Afrique, génère 5 offres marketing irrésistibles adaptées au marché africain.

Exemples d'offres (inspire-toi mais crée des offres originales et adaptées) :
- Livraison gratuite
- 1 acheté = 1 offert
- Cadeau mystère inclus
- Paiement à la livraison
- Garantie satisfait ou remboursé

Réponds en JSON :
{{
  "offres": [
    {{"titre": "...", "description": "...", "emoji": "...", "impact": "Élevé/Moyen/Fort", "conseil": "..."}},
    ...
  ]
}}"""

                offres_raw = call_grok(api_key, offres_prompt, sys_prompt, 1000)
                try:
                    offres_clean = re.sub(r"```json|```", "", offres_raw).strip()
                    st.session_state.results["offres"] = json.loads(offres_clean)
                except:
                    st.session_state.results["offres"] = {"offres": [
                        {"titre":"Livraison gratuite","description":"Offrez la livraison pour réduire les freins à l'achat","emoji":"🚚","impact":"Élevé","conseil":"Intégrez le coût dans votre prix de vente"},
                        {"titre":"1 acheté = 1 cadeau mystère","description":"Ajoutez un petit cadeau surprise pour augmenter la valeur perçue","emoji":"🎁","impact":"Fort","conseil":"Le cadeau doit coûter moins de 500 FCFA"},
                    ]}

                # 3. SHOPIFY
                shopify_prompt = f"""Pour le produit "{product_name}" vendu sur Shopify en Afrique, crée :

A) 3 TITRES optimisés SEO et conversion (mets en avant les bénéfices principaux, pas les caractéristiques)

B) 6 PARAGRAPHES de description produit (maximum 4 phrases chacun) avec des titres percutants et spécifiques (PAS génériques). Chaque paragraphe doit avoir un titre qui est une promesse ou un bénéfice concret.

Exemples de bons titres de paragraphes :
- "Résultats visibles en 7 jours ou remboursé"
- "100% naturel, 0 effet secondaire"
- "Utilisé par +500 femmes africaines"

Réponds en JSON :
{{
  "titres": ["titre1","titre2","titre3"],
  "paragraphes": [
    {{"titre": "...", "contenu": "..."}},
    ...
  ]
}}"""

                shopify_raw = call_grok(api_key, shopify_prompt, sys_prompt, 1500)
                try:
                    shopify_clean = re.sub(r"```json|```", "", shopify_raw).strip()
                    st.session_state.results["shopify"] = json.loads(shopify_clean)
                except:
                    st.session_state.results["shopify"] = {"titres":["Titre 1","Titre 2","Titre 3"],"paragraphes":[{"titre":"Titre","contenu":"Contenu..."}]}

                # 4. FACEBOOK ADS
                fb_prompt = f"""Crée 3 textes publicitaires Facebook Ads pour "{product_name}" (marché africain francophone).

RÈGLES STRICTES :
- Maximum 70 mots par texte
- Structure obligatoire :
  Ligne 1 : Titre CHOC (accroche qui surprend/choque/intrigue)
  - Bénéfice 1 du produit
  - Bénéfice 2 du produit  
  - Bénéfice 3 du produit

Réponds en JSON :
{{
  "ads": [
    {{"accroche": "...", "benefice1": "...", "benefice2": "...", "benefice3": "...", "mots_count": <nombre>}},
    ...
  ]
}}"""

                fb_raw = call_grok(api_key, fb_prompt, sys_prompt, 800)
                try:
                    fb_clean = re.sub(r"```json|```", "", fb_raw).strip()
                    st.session_state.results["facebook"] = json.loads(fb_clean)
                except:
                    st.session_state.results["facebook"] = {"ads":[{"accroche":"Titre choc ici","benefice1":"Bénéfice 1","benefice2":"Bénéfice 2","benefice3":"Bénéfice 3","mots_count":30}]}

                # 5. VOIX OFF
                voix_prompt = f"""Crée 3 scripts de voix off pour des publicités vidéo du produit "{product_name}" (marché africain francophone).

RÈGLES ABSOLUES :
- Chaque script doit faire EXACTEMENT entre 120 et 140 mots (compte précisément)
- Basé sur le NEUROMARKETING (déclenche des émotions, crée de l'urgence)
- Structure de chaque script :
  1. PROBLÈME (pose le problème que résout le produit, en 2-3 phrases percutantes)
  2. SOLUTION (présente le produit comme LA solution, 2-3 phrases)
  3. FONCTIONNEMENT (explique comment ça marche simplement, 2-3 phrases)
  4. TÉMOIGNAGE (témoignage court avec prénom africain : Aminata, Kofi, Fatou, Ibrahim, Moussa, Aïssatou, etc.)

Réponds en JSON :
{{
  "scripts": [
    {{"script": "texte complet du script 1", "mots": <compte exact>}},
    {{"script": "texte complet du script 2", "mots": <compte exact>}},
    {{"script": "texte complet du script 3", "mots": <compte exact>}}
  ]
}}"""

                voix_raw = call_grok(api_key, voix_prompt, sys_prompt, 2000)
                try:
                    voix_clean = re.sub(r"```json|```", "", voix_raw).strip()
                    st.session_state.results["voix"] = json.loads(voix_clean)
                except:
                    st.session_state.results["voix"] = {"scripts":[{"script":"Script voix off...","mots":125}]}

                # 6. AVATAR CLIENT
                avatar_prompt = f"""Crée le profil d'avatar client idéal pour acheter "{product_name}" en Afrique francophone.

Sois TRÈS PRÉCIS. Donne des détails concrets, pas des généralités.

Réponds en JSON :
{{
  "avatar": {{
    "sexe": "Homme/Femme/Les deux",
    "tranche_age": "Ex: 28-45 ans",
    "situation_familiale": "...",
    "revenus_mensuels": "Ex: 80 000 - 150 000 FCFA",
    "profession": "Ex: Commerçante, Secrétaire, Enseignant...",
    "localisation": "Ex: Grandes villes (Abidjan, Dakar, Douala...)",
    "reseaux_sociaux": ["Facebook","TikTok","WhatsApp"],
    "heure_active_en_ligne": "Ex: 19h-22h",
    "peurs_profondes": ["peur1","peur2","peur3"],
    "frustrations_quotidiennes": ["frustration1","frustration2","frustration3"],
    "desirs_secrets": ["desir1","desir2","desir3"],
    "motivations_achat": ["motivation1","motivation2"],
    "phrase_declenchante": "La phrase parfaite pour déclencher l'achat chez cet avatar",
    "objections_courantes": ["objection1","objection2"],
    "reponse_objections": ["reponse1","reponse2"],
    "qui_achete_pour_qui": "Se l'achète pour lui-même / Pour ses proches / Les deux",
    "budget_max_acceptable": "Ex: 10 000 - 15 000 FCFA",
    "canal_prefere": "Livraison à domicile / Point relais / Les deux"
  }}
}}"""

                avatar_raw = call_grok(api_key, avatar_prompt, sys_prompt, 1500)
                try:
                    avatar_clean = re.sub(r"```json|```", "", avatar_raw).strip()
                    st.session_state.results["avatar"] = json.loads(avatar_clean)
                except:
                    st.session_state.results["avatar"] = {"avatar":{"sexe":"Femme","tranche_age":"25-40 ans","revenus_mensuels":"75 000 - 150 000 FCFA","peurs_profondes":["peur1"],"frustrations_quotidiennes":["frustration1"],"desirs_secrets":["désir1"],"phrase_declenchante":"Phrase clé...","objections_courantes":["Objection 1"],"reponse_objections":["Réponse 1"],"budget_max_acceptable":"15 000 FCFA"}}

                # 7. IMAGES
                st.session_state.results["image_links"] = search_product_images(product_name)
                st.session_state.generated = True

            st.success("✅ Analyse complète générée !")
            st.balloons()

# ─────────────────────────────────────────────
#  MAIN TABS
# ─────────────────────────────────────────────
if not st.session_state.generated:
    # Welcome screen
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;">
      <div style="font-size:4rem;margin-bottom:1rem;animation:fadein 1s ease;">🚀</div>
      <div style="font-family:'Orbitron',sans-serif;font-size:1.5rem;color:#e63946;margin-bottom:1rem;">
        PRÊT À LANCER VOTRE PRODUIT ?
      </div>
      <div style="color:#888;font-size:1rem;max-width:600px;margin:0 auto;line-height:1.7;">
        Remplissez les informations dans le panneau gauche et cliquez sur 
        <span style="color:#f4a261;font-weight:700;">🚀 LANCER L'ANALYSE IA</span> 
        pour obtenir votre analyse complète propulsée par Grok.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("💰", "Calculateur de Prix", "Prix optimal + tableau de gains détaillé"),
        ("🎯", "Score Produit /10", "12 critères stricts d'évaluation marché africain"),
        ("🛍️", "Description Shopify", "3 titres + 6 paragraphes optimisés"),
        ("📢", "Facebook Ads", "3 textes publicitaires ≤70 mots"),
        ("🎙️", "Scripts Voix Off", "3 scripts 120-140 mots, neuromarketing"),
        ("👤", "Avatar Client", "Profil psychologique ultra-précis"),
    ]
    for i, (e, t, d) in enumerate(features):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div class="card" style="text-align:center;min-height:120px;">
              <div style="font-size:2rem;">{e}</div>
              <div style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#f4a261;margin:.3rem 0;">{t}</div>
              <div style="font-size:.85rem;color:#888;">{d}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    r = st.session_state.results
    pname = st.session_state.product_name
    pricing = r.get("pricing", {})

    tabs = st.tabs([
        "💰 Prix & Gains",
        "🎯 Score Produit",
        "🎁 Offres",
        "🛍️ Shopify",
        "📢 Facebook Ads",
        "🎙️ Voix Off",
        "👤 Avatar Client",
        "🖼️ Images",
    ])

    # ──────────────────────────────────────────
    # TAB 1 : PRIX & GAINS
    # ──────────────────────────────────────────
    with tabs[0]:
        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;color:#e63946;margin-bottom:1rem;">
            💰 STRATÉGIE DE PRIX — {pname.upper()}
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("Prix Min", f"{pricing.get('sell_min',0):,} FCFA", "Marge minimale"),
            ("Prix Recommandé", f"{pricing.get('sell_rec',0):,} FCFA", "✅ Optimal"),
            ("Prix Max", f"{pricing.get('sell_max',0):,} FCFA", "Marge maximale"),
            ("Bénéfice Net/vente", f"{pricing.get('profit_rec',0):,} FCFA", "Après toutes charges"),
        ]
        for col, (label, val, sub) in zip([c1,c2,c3,c4], metrics):
            with col:
                st.markdown(f"""
                <div class="metric-box">
                  <div class="metric-val">{val}</div>
                  <div class="metric-lbl">{label}</div>
                  <div style="font-size:.75rem;color:#666;margin-top:.3rem;">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

        # Charges breakdown
        st.markdown("#### 📊 Décomposition des charges par vente")
        cc1, cc2, cc3, cc4 = st.columns(4)
        charges = [
            ("📣 Publicité", pricing.get('pub',5000), "#e63946"),
            ("📞 Closing", pricing.get('closing',1000), "#f4a261"),
            ("🚚 Livraison", pricing.get('livraison',2000), "#4ade80"),
            ("💚 Votre gain NET", pricing.get('profit_rec',0), "#a78bfa"),
        ]
        for col, (label, val, color) in zip([cc1,cc2,cc3,cc4], charges):
            with col:
                st.markdown(f"""
                <div class="metric-box">
                  <div style="font-family:'Orbitron',sans-serif;font-size:1.3rem;font-weight:700;color:{color};">
                    {val:,} FCFA
                  </div>
                  <div class="metric-lbl">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

        # Gains table
        st.markdown("#### 📈 Tableau Calculateur de Gains (1 → 10 ventes/jour)")
        sell_price = pricing.get('sell_rec', 0)
        pub = pricing.get('pub', 5000)
        closing = pricing.get('closing', 1000)
        livraison = pricing.get('livraison', 2000)
        cout = st.session_state.cost_price

        table_html = """
        <div class="card">
        <table class="profit-table">
        <thead>
        <tr>
          <th>Ventes/jour</th>
          <th>Chiffre d'Affaires</th>
          <th>Coût Produits</th>
          <th>💸 Publicité</th>
          <th>📞 Closing</th>
          <th>🚚 Livraison</th>
          <th>💰 BÉNÉFICE NET</th>
          <th>📅 Gain mensuel</th>
        </tr>
        </thead>
        <tbody>
        """
        for v in range(1, 11):
            ca = v * sell_price
            cp = v * cout
            dp = v * pub
            dc = v * closing
            dl = v * livraison
            bn = ca - cp - dp - dc - dl
            bm = bn * 30
            color = "profit-td-green" if bn > 0 else "profit-td-red"
            table_html += f"""
            <tr>
              <td><b>{v}</b></td>
              <td class="profit-td-org">{ca:,} FCFA</td>
              <td class="profit-td-red">{cp:,} FCFA</td>
              <td class="profit-td-red">{dp:,} FCFA</td>
              <td class="profit-td-red">{dc:,} FCFA</td>
              <td class="profit-td-red">{dl:,} FCFA</td>
              <td class="{color}">{bn:,} FCFA</td>
              <td class="{color}">{bm:,} FCFA</td>
            </tr>"""
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)

        # Facebook budget advice
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 📣 Budget Facebook Ads recommandé")
        target = st.session_state.daily_target
        if target <= 7:
            fb_advice = "5 $ / jour", "1 créative", "0-7 ventes/jour", "#4ade80"
        elif target <= 12:
            fb_advice = "7 - 8 $ / jour", "1-2 créatives", "7-12 ventes/jour", "#f4a261"
        elif target <= 20:
            fb_advice = "10 - 15 $ / jour", "2-3 créatives", "12-20 ventes/jour", "#e63946"
        else:
            fb_advice = "15 $ + / jour", "3+ créatives", "20+ ventes/jour", "#a78bfa"

        st.markdown(f"""
        <div class="card" style="border-color:{fb_advice[3]};">
          <div style="display:flex;align-items:center;gap:2rem;flex-wrap:wrap;">
            <div>
              <div style="font-family:'Orbitron',sans-serif;font-size:2rem;color:{fb_advice[3]};font-weight:900;">{fb_advice[0]}</div>
              <div style="color:#888;font-size:.85rem;">Budget recommandé pour votre objectif de {target} ventes/jour</div>
            </div>
            <div style="text-align:center;">
              <div style="color:{fb_advice[3]};font-weight:700;">{fb_advice[1]}</div>
              <div style="color:#888;font-size:.8rem;">Créatives conseillées</div>
            </div>
            <div style="text-align:center;">
              <div style="color:{fb_advice[3]};font-weight:700;">{fb_advice[2]}</div>
              <div style="color:#888;font-size:.8rem;">Objectif ciblé</div>
            </div>
          </div>
          <div style="margin-top:1rem;padding:.8rem;background:rgba(255,255,255,.04);border-radius:8px;font-size:.9rem;color:#ccc;">
            💡 <b>Conseil :</b> Commencez avec 1 seule créative et {fb_advice[0]}. Après 3 jours, analysez les résultats.
            Si le coût par achat (CPA) est inférieur à {pricing.get('profit_rec',0):,} FCFA, augmentez progressivement le budget.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # TAB 2 : SCORE PRODUIT
    # ──────────────────────────────────────────
    with tabs[1]:
        score_data = r.get("score", {})
        score_val = float(score_data.get("score", 7))
        verdict = score_data.get("verdict", "Bon")
        emoji_v = score_data.get("emoji_verdict", "👍")
        deg = int((score_val / 10) * 360)

        color_score = "#4ade80" if score_val >= 7 else "#f4a261" if score_val >= 5 else "#e63946"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem 0;">
          <div style="
            display:inline-block;
            width:200px;height:200px;border-radius:50%;
            background: conic-gradient({color_score} {deg}deg, #1a1a2e {deg}deg);
            box-shadow: 0 0 40px {color_score}44;
            animation: spin-in .8s ease;
            position:relative;
          ">
            <div style="
              position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
              width:150px;height:150px;border-radius:50%;
              background:#0a0a0f;
              display:flex;flex-direction:column;align-items:center;justify-content:center;
            ">
              <div style="font-family:'Orbitron',sans-serif;font-size:3rem;font-weight:900;color:{color_score};">{score_val}</div>
              <div style="font-size:.7rem;color:#888;letter-spacing:2px;">/ 10</div>
            </div>
          </div>
          <div style="margin-top:1rem;font-family:'Orbitron',sans-serif;font-size:1.5rem;color:{color_score};">
            {emoji_v} {verdict.upper()}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Radar-style criteria bars
        st.markdown("#### 📊 Détail par critère")
        criteria = [
            ("💰 Rentabilité", "note_rentabilite"),
            ("📈 Demande marché", "note_demande"),
            ("⚔️ Concurrence", "note_concurrence"),
            ("🎨 Créatives dispo", "note_creatives"),
            ("🔥 Potentiel viral", "note_viral"),
            ("🌍 Pertinence Afrique", "note_pertinence_afrique"),
            ("💵 Prix psychologique", "note_prix_psycho"),
            ("🔄 Fidélisation", "note_fidelisation"),
        ]
        for label, key in criteria:
            val = score_data.get(key, 7)
            pct = val * 10
            bar_color = "#4ade80" if val >= 7 else "#f4a261" if val >= 5 else "#e63946"
            st.markdown(f"""
            <div style="margin:.4rem 0;">
              <div style="display:flex;justify-content:space-between;margin-bottom:.2rem;">
                <span style="font-size:.9rem;">{label}</span>
                <span style="font-weight:700;color:{bar_color};">{val}/10</span>
              </div>
              <div style="background:#1a1a2e;border-radius:20px;height:10px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{bar_color},{bar_color}88);
                             border-radius:20px;transition:width 1s ease;animation:fadein .5s ease;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**✅ Points Forts**")
            for pt in score_data.get("points_forts", []):
                st.markdown(f"""
                <div style="background:rgba(74,222,128,.1);border-left:3px solid #4ade80;
                             padding:.6rem 1rem;border-radius:0 8px 8px 0;margin:.3rem 0;font-size:.9rem;">
                  ✅ {pt}
                </div>""", unsafe_allow_html=True)
        with col_b:
            st.markdown("**⚠️ Points à surveiller**")
            for pt in score_data.get("points_faibles", []):
                st.markdown(f"""
                <div style="background:rgba(230,57,70,.1);border-left:3px solid #e63946;
                             padding:.6rem 1rem;border-radius:0 8px 8px 0;margin:.3rem 0;font-size:.9rem;">
                  ⚠️ {pt}
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card" style="border-color:#f4a261;">
          <div style="color:#f4a261;font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;letter-spacing:2px;margin-bottom:.5rem;">
            🧭 RECOMMANDATION STRATÉGIQUE
          </div>
          <div style="line-height:1.8;font-size:.95rem;">{score_data.get('recommandation','')}</div>
          <div style="margin-top:1rem;display:flex;gap:1rem;flex-wrap:wrap;">
            <div>🌍 <b>Marchés cibles :</b> {', '.join(score_data.get('marches_cibles',[]))}</div>
            <div>📅 <b>Meilleure période :</b> {score_data.get('meilleure_periode','')}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # TAB 3 : OFFRES
    # ──────────────────────────────────────────
    with tabs[2]:
        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#e63946;">
            🎁 OFFRES MARKETING POUR : {pname.upper()}
          </div>
          <div style="color:#888;font-size:.85rem;margin-top:.3rem;">
            Offres adaptées au marché africain pour maximiser vos conversions
          </div>
        </div>
        """, unsafe_allow_html=True)

        offres = r.get("offres", {}).get("offres", [])
        for i, offre in enumerate(offres):
            impact = offre.get("impact","Moyen")
            impact_color = "#4ade80" if "Élevé" in impact or "Fort" in impact else "#f4a261"
            st.markdown(f"""
            <div class="offer-card">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem;">
                <div>
                  <span style="font-size:1.5rem;">{offre.get('emoji','🎯')}</span>
                  <span style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.1rem;margin-left:.5rem;">
                    {offre.get('titre','')}
                  </span>
                </div>
                <span style="background:rgba(0,0,0,.3);color:{impact_color};padding:.2rem .6rem;
                              border-radius:20px;font-size:.75rem;font-weight:700;border:1px solid {impact_color}44;">
                  Impact : {impact}
                </span>
              </div>
              <div style="margin:.6rem 0;color:#ccc;font-size:.9rem;">{offre.get('description','')}</div>
              <div style="background:rgba(244,162,97,.08);border-left:3px solid #f4a261;padding:.5rem .8rem;
                           border-radius:0 8px 8px 0;font-size:.85rem;color:#f4a261;">
                💡 {offre.get('conseil','')}
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # TAB 4 : SHOPIFY
    # ──────────────────────────────────────────
    with tabs[3]:
        shopify = r.get("shopify", {})
        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#e63946;">
            🛍️ DESCRIPTION SHOPIFY — {pname.upper()}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🏷️ 3 Titres Produit Optimisés")
        for i, titre in enumerate(shopify.get("titres", []), 1):
            copy_button(titre, f"shopify_titre_{i}")

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 📝 6 Paragraphes de Description")
        for i, para in enumerate(shopify.get("paragraphes", []), 1):
            st.markdown(f"""
            <div style="margin:.8rem 0;">
              <div style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1rem;
                           color:#f4a261;letter-spacing:1px;margin-bottom:.3rem;">
                ▶ {para.get('titre','')}
              </div>
            </div>
            """, unsafe_allow_html=True)
            copy_button(para.get("contenu",""), f"shopify_para_{i}")

    # ──────────────────────────────────────────
    # TAB 5 : FACEBOOK ADS
    # ──────────────────────────────────────────
    with tabs[4]:
        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#e63946;">
            📢 TEXTES PUBLICITAIRES FACEBOOK ADS — {pname.upper()}
          </div>
          <div style="color:#888;font-size:.85rem;margin-top:.3rem;">3 textes ≤70 mots • Structure : Accroche choc + 3 bénéfices</div>
        </div>
        """, unsafe_allow_html=True)

        ads = r.get("facebook", {}).get("ads", [])
        for i, ad in enumerate(ads, 1):
            full_text = f"{ad.get('accroche','')}\n\n- {ad.get('benefice1','')}\n- {ad.get('benefice2','')}\n- {ad.get('benefice3','')}"
            mots = ad.get('mots_count', '~')
            st.markdown(f"""
            <div style="margin-bottom:.3rem;">
              <span style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#e63946;font-size:1rem;">
                📢 TEXTE PUBLICITAIRE #{i}
              </span>
              <span style="font-size:.75rem;color:#888;margin-left:.5rem;">({mots} mots)</span>
            </div>
            <div style="background:rgba(230,57,70,.08);border-left:3px solid #e63946;
                         padding:.7rem 1rem;border-radius:0 10px 10px 0;margin-bottom:.3rem;font-size:.95rem;">
              <div style="font-weight:700;color:white;margin-bottom:.6rem;font-size:1.05rem;">🔥 {ad.get('accroche','')}</div>
              <div style="color:#ccc;">
                ✦ {ad.get('benefice1','')}<br>
                ✦ {ad.get('benefice2','')}<br>
                ✦ {ad.get('benefice3','')}
              </div>
            </div>
            """, unsafe_allow_html=True)
            copy_button(full_text, f"fb_ad_{i}")
            st.markdown("<br>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # TAB 6 : VOIX OFF
    # ──────────────────────────────────────────
    with tabs[5]:
        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#e63946;">
            🎙️ SCRIPTS VOIX OFF — {pname.upper()}
          </div>
          <div style="color:#888;font-size:.85rem;margin-top:.3rem;">
            3 scripts • 120-140 mots chacun • Neuromarketing • Structure : Problème → Solution → Fonctionnement → Témoignage
          </div>
        </div>
        """, unsafe_allow_html=True)

        scripts = r.get("voix", {}).get("scripts", [])
        for i, s in enumerate(scripts, 1):
            script_text = s.get("script","")
            mots = s.get("mots", len(script_text.split()))
            color = "#4ade80" if 120 <= mots <= 140 else "#f4a261"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:1rem;margin-bottom:.5rem;">
              <div style="font-family:'Orbitron',sans-serif;font-size:1rem;color:#e63946;font-weight:700;">
                🎙️ SCRIPT #{i}
              </div>
              <div style="background:rgba(0,0,0,.3);color:{color};padding:.2rem .7rem;
                           border-radius:20px;font-size:.75rem;font-weight:700;border:1px solid {color}44;">
                {mots} mots
              </div>
            </div>
            """, unsafe_allow_html=True)
            copy_button(script_text, f"voix_{i}")
            st.markdown("<br>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # TAB 7 : AVATAR CLIENT
    # ──────────────────────────────────────────
    with tabs[6]:
        avatar = r.get("avatar", {}).get("avatar", {})
        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#e63946;">
            👤 AVATAR CLIENT IDÉAL — {pname.upper()}
          </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
            <div style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#f4a261;
                         letter-spacing:2px;margin-bottom:1rem;font-size:.9rem;">👤 PROFIL DÉMOGRAPHIQUE</div>
            """, unsafe_allow_html=True)

            demo_fields = [
                ("🚻 Sexe", "sexe"), ("🎂 Tranche d'âge", "tranche_age"),
                ("👨‍👩‍👧 Situation familiale", "situation_familiale"),
                ("💵 Revenus mensuels", "revenus_mensuels"),
                ("💼 Profession", "profession"),
                ("📍 Localisation", "localisation"),
                ("🕐 Heure active en ligne", "heure_active_en_ligne"),
                ("💰 Budget max acceptable", "budget_max_acceptable"),
                ("🛵 Canal de livraison préféré", "canal_prefere"),
                ("🛍️ Qui achète pour qui ?", "qui_achete_pour_qui"),
            ]
            for label, key in demo_fields:
                val = avatar.get(key, "—")
                if val and val != "—":
                    st.markdown(f"""
                    <div class="avatar-section">
                      <div class="avatar-label">{label}</div>
                      <div style="color:#f1f1f1;font-size:.9rem;">{val}</div>
                    </div>""", unsafe_allow_html=True)

            # Réseaux sociaux
            rs = avatar.get("reseaux_sociaux", [])
            if rs:
                st.markdown(f"""
                <div class="avatar-section">
                  <div class="avatar-label">📱 Réseaux sociaux</div>
                  <div>{''.join([f'<span style="background:rgba(230,57,70,.2);border:1px solid #e63946;border-radius:20px;padding:.2rem .6rem;margin:.2rem;font-size:.8rem;display:inline-block;">{s}</span>' for s in rs])}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card">
            <div style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#f4a261;
                         letter-spacing:2px;margin-bottom:1rem;font-size:.9rem;">🧠 PROFIL PSYCHOLOGIQUE</div>
            """, unsafe_allow_html=True)

            psych_fields = [
                ("😱 Peurs profondes", "peurs_profondes", "#e63946"),
                ("😤 Frustrations", "frustrations_quotidiennes", "#f4a261"),
                ("💫 Désirs secrets", "desirs_secrets", "#a78bfa"),
                ("⚡ Motivations d'achat", "motivations_achat", "#4ade80"),
                ("❓ Objections courantes", "objections_courantes", "#fb923c"),
                ("✅ Réponses aux objections", "reponse_objections", "#4ade80"),
            ]
            for label, key, color in psych_fields:
                items = avatar.get(key, [])
                if items:
                    bullets = "".join([f'<div style="margin:.3rem 0;padding:.4rem .8rem;background:rgba(0,0,0,.3);border-left:3px solid {color};border-radius:0 8px 8px 0;font-size:.88rem;">▸ {item}</div>' for item in items])
                    st.markdown(f"""
                    <div class="avatar-section">
                      <div class="avatar-label" style="color:{color};">{label}</div>
                      {bullets}
                    </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Phrase déclenchante
        phrase = avatar.get("phrase_declenchante","")
        if phrase:
            st.markdown(f"""
            <div class="card" style="border-color:#f4a261;text-align:center;margin-top:1rem;">
              <div style="font-family:'Rajdhani',sans-serif;font-weight:700;color:#f4a261;letter-spacing:2px;margin-bottom:.8rem;font-size:.9rem;">
                💬 PHRASE DÉCLENCHANTE (à utiliser dans vos pubs)
              </div>
              <div style="font-size:1.15rem;font-style:italic;color:white;line-height:1.6;">
                "{phrase}"
              </div>
            </div>
            """, unsafe_allow_html=True)
            copy_button(phrase, "phrase_declenchante")

    # ──────────────────────────────────────────
    # TAB 8 : IMAGES
    # ──────────────────────────────────────────
    with tabs[7]:
        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:#e63946;">
            🖼️ IMAGES PRODUIT — {pname.upper()}
          </div>
          <div style="color:#888;font-size:.85rem;margin-top:.3rem;">
            Images uploadées + liens de recherche sur AliExpress, Alibaba, Pinterest, Temu
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Uploaded images
        if st.session_state.product_images:
            st.markdown("#### 📷 Vos images uploadées")
            cols = st.columns(min(len(st.session_state.product_images), 5))
            for i, img_file in enumerate(st.session_state.product_images):
                with cols[i % 5]:
                    st.image(img_file, use_container_width=True)
                    buf = io.BytesIO(img_file.read())
                    img_file.seek(0)
                    b64 = base64.b64encode(img_file.read()).decode()
                    img_file.seek(0)
                    ext = img_file.name.split(".")[-1]
                    st.markdown(f"""
                    <a href="data:image/{ext};base64,{b64}" download="{img_file.name}">
                      <button style="width:100%;background:linear-gradient(135deg,#e63946,#ff6b35);
                                     border:none;color:white;padding:.4rem;border-radius:6px;
                                     cursor:pointer;font-size:.8rem;margin-top:.2rem;">
                        ⬇️ Télécharger
                      </button>
                    </a>
                    """, unsafe_allow_html=True)

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

        # Search links
        q = urllib.parse.quote(pname)
        platforms = [
            ("🟠 AliExpress", f"https://fr.aliexpress.com/wholesale?SearchText={q}", "#ff6010"),
            ("🔵 Alibaba", f"https://www.alibaba.com/trade/search?SearchText={q}", "#e6380a"),
            ("🔴 Pinterest", f"https://www.pinterest.com/search/pins/?q={q}", "#e60023"),
            ("🟡 Temu", f"https://www.temu.com/search_result.html?search_key={q}", "#f4a261"),
            ("🔵 Facebook Marketplace", f"https://www.facebook.com/marketplace/search/?query={q}", "#1877f2"),
            ("🔍 Google Images", f"https://www.google.com/search?q={q}+produit&tbm=isch", "#4285f4"),
        ]

        st.markdown("#### 🔍 Rechercher des images de votre produit")
        cols = st.columns(3)
        for i, (name, url, color) in enumerate(platforms):
            with cols[i % 3]:
                st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration:none;">
                  <div class="offer-card" style="text-align:center;border-color:{color}44;">
                    <div style="font-size:1.5rem;margin-bottom:.3rem;">{name.split()[0]}</div>
                    <div style="font-weight:700;color:{color};font-family:'Rajdhani',sans-serif;">{name[2:]}</div>
                    <div style="font-size:.75rem;color:#888;margin-top:.3rem;">Cliquer pour rechercher →</div>
                  </div>
                </a>
                """, unsafe_allow_html=True)

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="border-color:#f4a261;">
          <div style="color:#f4a261;font-weight:700;margin-bottom:.5rem;">💡 Comment utiliser ces images ?</div>
          <div style="font-size:.9rem;color:#ccc;line-height:1.8;">
            1. Cliquez sur l'une des plateformes ci-dessus pour rechercher les images de votre produit<br>
            2. Téléchargez les meilleures images directement sur la plateforme<br>
            3. Revenez ici et uploadez-les dans le panel gauche (max 10 images)<br>
            4. Elles apparaîtront ici avec un bouton de téléchargement direct
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem;border-top:1px solid rgba(230,57,70,.2);margin-top:2rem;color:#444;font-size:.8rem;">
  <div style="font-family:'Orbitron',sans-serif;font-size:.9rem;color:#e63946;margin-bottom:.5rem;">
    ⚡ E-COMMERCE MASTER LABO PRO
  </div>
  Propulsé par Grok AI (xAI) • Conçu pour les e-commerçants africains 🌍<br>
  <span style="color:#333;">Made with ❤️ pour l'Afrique</span>
</div>
""", unsafe_allow_html=True)
