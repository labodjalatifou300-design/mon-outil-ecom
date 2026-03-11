import streamlit as st
import requests, json, re, base64, urllib.parse
from PIL import Image
import io

st.set_page_config(page_title="E-Commerce Master Labo Pro", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════
#  STYLES
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --ink:    #0b0b0f;
  --surface:#111118;
  --lift:   #1c1c28;
  --border: rgba(255,255,255,.07);
  --red:    #ff2d55;
  --amber:  #ff9f0a;
  --gold:   #ffd60a;
  --smoke:  #a0a0b0;
  --white:  #f5f5fa;
}
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  background: var(--ink) !important;
  color: var(--white) !important;
}
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 1.5rem 3rem !important; max-width: 1400px !important; }

/* ── HERO ── */
.hero {
  background: linear-gradient(135deg, #0b0b0f 0%, #18080e 40%, #0b0b0f 100%);
  padding: 3rem 2rem 2rem; text-align: center;
  border-bottom: 1px solid rgba(255,45,85,.2);
  position: relative; overflow: hidden; margin-bottom: 2rem;
}
.hero-bg {
  position: absolute; inset: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 80% 60% at 50% -10%, rgba(255,45,85,.15) 0%, transparent 70%),
    radial-gradient(ellipse 40% 40% at 20% 80%, rgba(255,159,10,.08) 0%, transparent 60%);
}
.hero-title {
  font-family: 'Syne', sans-serif; font-weight: 800;
  font-size: clamp(2rem, 6vw, 4.5rem); line-height: 1.05;
  letter-spacing: -1px; color: var(--white);
  position: relative; z-index: 1;
}
.hero-title span { color: var(--red); }
.hero-sub {
  font-family: 'DM Sans', sans-serif; font-weight: 300;
  font-size: clamp(.9rem, 2vw, 1.15rem); color: var(--smoke);
  margin-top: .6rem; letter-spacing: 3px; text-transform: uppercase;
  position: relative; z-index: 1;
}
.hero-line {
  width: 60px; height: 3px; margin: 1.2rem auto 0;
  background: linear-gradient(90deg, var(--red), var(--amber));
  border-radius: 2px; position: relative; z-index: 1;
}

/* ── PANEL ── */
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 20px; padding: 1.8rem; margin-bottom: 1.5rem;
  position: relative;
}
.panel-title {
  font-family: 'Syne', sans-serif; font-weight: 700; font-size: .7rem;
  letter-spacing: 3px; text-transform: uppercase; color: var(--red);
  margin-bottom: 1.2rem; display: flex; align-items: center; gap: .5rem;
}
.panel-title::after { content:''; flex:1; height:1px; background:var(--border); }

/* ── METRIC ── */
.metric {
  background: var(--lift); border: 1px solid var(--border);
  border-radius: 14px; padding: 1.1rem; text-align: center;
  transition: border-color .25s, transform .25s;
}
.metric:hover { border-color: rgba(255,45,85,.4); transform: translateY(-3px); }
.metric-val {
  font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800;
  color: var(--white); line-height: 1;
}
.metric-val.red { color: var(--red); }
.metric-val.amber { color: var(--amber); }
.metric-val.green { color: #30d158; }
.metric-lbl { font-size: .72rem; color: var(--smoke); letter-spacing: 1.5px; text-transform: uppercase; margin-top: .35rem; }

/* ── TABLE ── */
.tbl { width:100%; border-collapse:collapse; font-size:.85rem; }
.tbl th { padding:.65rem .5rem; font-family:'Syne',sans-serif; font-size:.7rem; letter-spacing:2px; text-transform:uppercase; color:var(--smoke); border-bottom:1px solid var(--border); text-align:center; }
.tbl td { padding:.6rem .5rem; text-align:center; border-bottom:1px solid rgba(255,255,255,.04); }
.tbl tr:hover td { background:rgba(255,45,85,.06); }
.c-g{color:#30d158;font-weight:700} .c-r{color:var(--red);font-weight:600} .c-a{color:var(--amber);font-weight:600}

/* ── COPY ROW ── */
.copy-row {
  display: flex; align-items: flex-start; gap: .6rem; margin: .5rem 0;
}
.copy-text {
  flex: 1; background: var(--lift); border: 1px solid var(--border);
  border-radius: 10px; padding: .9rem 1rem; font-size: .9rem;
  line-height: 1.7; color: var(--white);
}
.copy-icon {
  flex-shrink: 0; width: 36px; height: 36px; border-radius: 8px;
  background: var(--lift); border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; font-size: 1rem; transition: all .2s;
  margin-top: 2px;
}
.copy-icon:hover { background: var(--red); border-color: var(--red); transform: scale(1.1); }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important; border-radius: 14px !important;
  padding: 5px !important; gap: 3px !important;
  border: 1px solid var(--border) !important; flex-wrap: wrap !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--smoke) !important;
  border-radius: 10px !important; padding: .5rem 1rem !important;
  font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
  font-size: .8rem !important; letter-spacing: .5px !important;
}
.stTabs [aria-selected="true"] {
  background: var(--red) !important; color: white !important;
  box-shadow: 0 4px 20px rgba(255,45,85,.4) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: var(--red) !important; color: white !important;
  border: none !important; border-radius: 12px !important;
  font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
  font-size: .95rem !important; letter-spacing: .5px !important;
  padding: .65rem 2rem !important; transition: all .25s !important;
  box-shadow: 0 4px 20px rgba(255,45,85,.35) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(255,45,85,.55) !important; }

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox > div > div {
  background: var(--lift) !important; border: 1px solid var(--border) !important;
  border-radius: 10px !important; color: var(--white) !important; font-family: 'DM Sans',sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: rgba(255,45,85,.5) !important;
  box-shadow: 0 0 0 3px rgba(255,45,85,.12) !important;
}
label, .stTextInput label, .stNumberInput label { color: var(--smoke) !important; font-size:.82rem !important; letter-spacing:.5px !important; }

/* ── SCORE RING ── */
.score-wrap { text-align:center; padding: 1.5rem 0; }
.score-ring-svg { filter: drop-shadow(0 0 30px rgba(255,45,85,.4)); }
.score-verdict { font-family:'Syne',sans-serif; font-weight:800; font-size:1.4rem; margin-top:.6rem; }

/* ── BAR ── */
.bar-row { display:flex; align-items:center; gap:.8rem; margin:.4rem 0; }
.bar-lbl { font-size:.83rem; width:180px; flex-shrink:0; color:var(--smoke); }
.bar-bg { flex:1; background:rgba(255,255,255,.07); border-radius:20px; height:8px; overflow:hidden; }
.bar-fill { height:100%; border-radius:20px; transition: width 1s ease; }
.bar-val { font-family:'Syne',sans-serif; font-size:.8rem; font-weight:700; width:32px; text-align:right; flex-shrink:0; }

/* ── OFFER CARD ── */
.offer { background:var(--lift); border:1px solid var(--border); border-radius:14px; padding:1.1rem; margin:.5rem 0; display:flex; flex-direction:column; gap:.5rem; transition:border-color .2s,transform .2s; }
.offer:hover { border-color:rgba(255,159,10,.4); transform:translateX(4px); }
.offer-head { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:.4rem; }
.offer-name { font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; }
.offer-badge { font-size:.7rem; padding:.2rem .6rem; border-radius:20px; font-weight:700; letter-spacing:1px; }
.offer-tip { font-size:.8rem; color:var(--amber); padding:.4rem .7rem; background:rgba(255,159,10,.07); border-left:2px solid var(--amber); border-radius:0 6px 6px 0; }

/* ── AVATAR CARD ── */
.av-card { background:var(--lift); border:1px solid var(--border); border-radius:16px; padding:1.4rem; }
.av-head { display:flex; align-items:center; gap:1rem; margin-bottom:1.2rem; }
.av-avatar { width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg,var(--red),var(--amber)); display:flex; align-items:center; justify-content:center; font-size:2rem; flex-shrink:0; }
.av-name { font-family:'Syne',sans-serif; font-weight:800; font-size:1.2rem; }
.av-role { font-size:.8rem; color:var(--smoke); margin-top:.15rem; }
.av-row { display:flex; gap:.5rem; margin:.35rem 0; align-items:flex-start; }
.av-key { font-size:.72rem; letter-spacing:1.5px; text-transform:uppercase; color:var(--smoke); width:110px; flex-shrink:0; padding-top:.1rem; }
.av-val { font-size:.88rem; color:var(--white); flex:1; }
.badge { display:inline-block; padding:.2rem .6rem; border-radius:20px; font-size:.75rem; margin:.15rem; border:1px solid var(--border); }

/* ── BUBBLE LINK ── */
.bubble-wrap { display:flex; flex-wrap:wrap; gap:.5rem; margin:.8rem 0; }
.bubble { display:inline-flex; align-items:center; gap:.35rem; padding:.4rem .9rem; border-radius:30px; font-size:.82rem; font-weight:600; text-decoration:none; transition:all .2s; cursor:pointer; }
.bubble:hover { transform:translateY(-2px); box-shadow:0 4px 16px rgba(0,0,0,.4); }

/* ── PHRASE CARD ── */
.phrase-card {
  background:linear-gradient(135deg,rgba(255,45,85,.12),rgba(255,159,10,.08));
  border:1px solid rgba(255,159,10,.3); border-radius:14px; padding:1.4rem;
  text-align:center; margin-top:1rem;
}
.phrase-quote { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:600; line-height:1.6; font-style:italic; }

/* ── PIPS (FB ad) ── */
.ad-card { background:var(--lift); border-left:3px solid var(--red); border-radius:0 12px 12px 0; padding:1rem 1.2rem; margin:.5rem 0; }
.ad-hook { font-family:'Syne',sans-serif; font-weight:800; font-size:1.05rem; color:var(--white); margin-bottom:.6rem; }
.ad-pip { font-size:.88rem; color:var(--smoke); padding:.15rem 0; }
.ad-pip::before { content:'▸ '; color:var(--red); }

/* ── IMG THUMB ── */
.thumb-grid { display:flex; flex-wrap:wrap; gap:.6rem; }
.thumb-item { width:80px; }
.thumb-item img { width:80px; height:80px; object-fit:cover; border-radius:10px; border:1px solid var(--border); transition:transform .2s; }
.thumb-item img:hover { transform:scale(1.08); }
.thumb-dl { display:block; text-align:center; font-size:.65rem; color:var(--smoke); margin-top:.25rem; text-decoration:none; }
.thumb-dl:hover { color:var(--red); }

/* ── FB BUDGET ── */
.budget-hero { text-align:center; padding:1.5rem; }
.budget-num { font-family:'Syne',sans-serif; font-size:3rem; font-weight:800; color:var(--red); line-height:1; }
.budget-sub { color:var(--smoke); font-size:.85rem; margin-top:.3rem; }

/* ── TIP BOX ── */
.tip { background:rgba(255,159,10,.07); border:1px solid rgba(255,159,10,.2); border-radius:10px; padding:.8rem 1rem; font-size:.85rem; color:var(--smoke); line-height:1.7; }
.tip b { color:var(--amber); }

/* ── DIVIDER ── */
.div { height:1px; background:var(--border); margin:1.5rem 0; }

/* scrollbar */
::-webkit-scrollbar{width:4px} ::-webkit-scrollbar-track{background:var(--ink)} ::-webkit-scrollbar-thumb{background:var(--red);border-radius:2px}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  SESSION
# ══════════════════════════════════════════════════════
for k,v in {"gen":False,"pname":"","pimages":[],"pcost":0,"ptarget":5,"res":{},"form_open":True}.items():
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════
GROQ_KEY = st.secrets.get("GROQ_API_KEY","")
PAYS = ["Togo","Mali","Bénin","Guinée","Côte d'Ivoire","Congo"]
CODES = {"Togo":"TG","Mali":"ML","Bénin":"BJ","Guinée":"GN","Côte d'Ivoire":"CI","Congo":"CG"}

# ══════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════
def groq(prompt, system="", tokens=2500):
    if not GROQ_KEY: return '{"error":"Clé API manquante"}'
    try:
        msgs = ([{"role":"system","content":system}] if system else []) + [{"role":"user","content":prompt}]
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {GROQ_KEY}","Content-Type":"application/json"},
            json={"model":"llama-3.3-70b-versatile","messages":msgs,"max_tokens":tokens,"temperature":.85},
            timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e: return f'{{"error":"{e}"}}'

def pjson(raw):
    try: return json.loads(re.sub(r"```json|```","",raw).strip())
    except: return {}

def calc(cost,pub=5000,cl=1000,liv=2000):
    rec=cost+10000
    return {"min":cost+8000,"max":cost+12000,"rec":rec,"profit":rec-cost-pub-cl-liv,"pub":pub,"cl":cl,"liv":liv}

# Copy block: text on left, icon on right — uses Streamlit text_area + button trick
def copy_row(text, uid):
    """Render text with inline copy button on the right."""
    safe = text.replace("\\","\\\\").replace("`","\\`").replace('"','\\"').replace("\n","\\n")
    st.markdown(f"""
    <div class="copy-row">
      <div class="copy-text" id="ct_{uid}">{text.replace(chr(10),'<br>')}</div>
      <button class="copy-icon" title="Copier"
        onclick="
          const el=document.getElementById('ct_{uid}');
          const txt=el.innerText;
          navigator.clipboard.writeText(txt).then(()=>{{
            this.innerText='✅';
            this.style.background='#30d158';
            this.style.borderColor='#30d158';
            setTimeout(()=>{{this.innerText='📋';this.style.background='';this.style.borderColor=''}},1800);
          }}).catch(()=>{{
            const ta=document.createElement('textarea');
            ta.value=txt; document.body.appendChild(ta);
            ta.select(); document.execCommand('copy');
            document.body.removeChild(ta);
            this.innerText='✅';
            setTimeout(()=>this.innerText='📋',1800);
          }});
        ">📋</button>
    </div>""", unsafe_allow_html=True)

def bubble(label, url, color="#ff2d55", bg="rgba(255,45,85,.12)"):
    q=urllib.parse.quote(label)
    return f'<a href="{url}" target="_blank" class="bubble" style="background:{bg};color:{color};border:1px solid {color}44;">🌍 {label}</a>'

# ══════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-bg"></div>
  <div class="hero-title">E-Commerce<br><span>Master Labo Pro</span></div>
  <div class="hero-sub">🌍 Tout en un pour un e-commerce africain réussi</div>
  <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  FORM TOGGLE
# ══════════════════════════════════════════════════════
lbl = "🔼 Masquer le formulaire" if st.session_state.form_open else "🔽 Remplir les informations produit"
if st.button(lbl, key="tog"):
    st.session_state.form_open = not st.session_state.form_open
    st.rerun()

if st.session_state.form_open:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📦 Informations produit</div>', unsafe_allow_html=True)

    c1,c2,c3 = st.columns([2,1,1])
    with c1: pname = st.text_input("Nom du produit", placeholder="Ex: Sérum anti-acné naturel", value=st.session_state.pname)
    with c2: pcost = st.number_input("Prix d'achat (FCFA)", min_value=0, step=500, value=int(st.session_state.pcost))
    with c3: ptarget = st.number_input("Objectif ventes/jour", min_value=1, max_value=50, value=int(st.session_state.ptarget))

    c4,c5,c6 = st.columns(3)
    with c4: ppub = st.number_input("Publicité/vente (FCFA)", value=5000, step=500)
    with c5: pcl  = st.number_input("Closing/vente (FCFA)", value=1000, step=100)
    with c6: pliv = st.number_input("Livraison/vente (FCFA)", value=2000, step=500)

    st.markdown("**Images du produit** — 1 à 10 photos")
    uploaded = st.file_uploader("", type=["jpg","jpeg","png","webp"], accept_multiple_files=True, label_visibility="collapsed")
    if uploaded:
        if len(uploaded)>10: uploaded=uploaded[:10]; st.warning("Maximum 10 images.")
        st.session_state.pimages = uploaded
        # Show thumbnails
        st.markdown('<div class="thumb-grid">', unsafe_allow_html=True)
        for img in uploaded:
            img.seek(0)
            b64=base64.b64encode(img.read()).decode(); ext=img.name.split(".")[-1]
            st.markdown(f'<div class="thumb-item"><img src="data:image/{ext};base64,{b64}"><a class="thumb-dl" href="data:image/{ext};base64,{b64}" download="{img.name}">⬇ DL</a></div>', unsafe_allow_html=True)
            img.seek(0)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    go = st.button("⚡ LANCER L'ANALYSE COMPLÈTE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if go:
        if not pname: st.error("❌ Entrez le nom du produit"); st.stop()
        if pcost==0:  st.error("❌ Entrez le prix d'achat"); st.stop()
        if not GROQ_KEY: st.error("❌ Clé GROQ_API_KEY manquante dans Streamlit Secrets"); st.stop()

        st.session_state.pname=pname; st.session_state.pcost=pcost; st.session_state.ptarget=ptarget
        pricing=calc(pcost,ppub,pcl,pliv); st.session_state.res["pricing"]=pricing

        SYS=f"Tu es expert e-commerce africain. Produit: {pname}. Achat: {pcost} FCFA. Vente: {pricing['rec']} FCFA. Marge: {pricing['profit']} FCFA. Objectif: {ptarget}/jour. Réponds en français, marché africain francophone."

        bar=st.progress(0,"Analyse IA en cours…")

        # SCORE
        bar.progress(10,"🎯 Score produit…")
        raw=groq(f"""Évalue "{pname}" sur le marché africain. Score STRICT sur 10 (avec décimale).
12 critères: rentabilité({pricing['profit']} FCFA net), demande Afrique, concurrence, approvisionnement,
créatives dispo, viral FB/TikTok, problème réel africain, simplicité, prix vs SMIC(35k-200k FCFA), fidélisation, risque retours, saisonnalité.
JSON UNIQUEMENT sans markdown:
{{"score":7.5,"verdict":"Bon","couleur":"orange","note_r":8,"note_d":7,"note_c":5,"note_cr":7,"note_v":8,"note_a":8,"note_p":7,"note_f":6,"forts":["f1","f2","f3"],"faibles":["w1","w2"],"conseil":"2-3 phrases concrètes","pays":["Côte d'Ivoire","Sénégal","Cameroun"],"periode":"Toute l'année"}}""",SYS,900)
        st.session_state.res["score"]=pjson(raw) or {"score":7,"verdict":"Bon","couleur":"amber","note_r":7,"note_d":7,"note_c":6,"note_cr":7,"note_v":7,"note_a":8,"note_p":7,"note_f":6,"forts":["Bonne marge","Marché porteur"],"faibles":["Concurrence existante"],"conseil":"Testez avec 5$/jour sur Facebook.","pays":["Côte d'Ivoire","Sénégal"],"periode":"Toute l'année"}

        # OFFRES
        bar.progress(22,"🎁 Offres…")
        raw=groq(f"""Génère exactement 5 offres marketing pour "{pname}" à {pricing['rec']} FCFA en Afrique francophone.
JSON UNIQUEMENT:
{{"offres":[{{"emoji":"🚚","titre":"Livraison offerte","desc":"Description courte de l'offre et pourquoi elle convertit","impact":"Élevé","conseil":"Conseil pratique"}}]}}""",SYS,700)
        st.session_state.res["offres"]=pjson(raw) or {"offres":[
            {"emoji":"🚚","titre":"Livraison gratuite","desc":"Lève le principal frein à l'achat.","impact":"Élevé","conseil":"Intégrez le coût dans le prix"},
            {"emoji":"🎁","titre":"Cadeau mystère offert","desc":"Augmente la valeur perçue sans coût élevé.","impact":"Fort","conseil":"Coût du cadeau < 500 FCFA"},
            {"emoji":"💰","titre":"Paiement à la livraison","desc":"Réduit le risque perçu.","impact":"Élevé","conseil":"Demandez un acompte si possible"}]}

        # SHOPIFY
        bar.progress(36,"🛍️ Shopify…")
        raw=groq(f"""Pour "{pname}" sur Shopify, génère du contenu de vente pour l'Afrique.
JSON UNIQUEMENT (ne mets RIEN d'autre, pas de texte avant ou après):
{{"titres":["Titre SEO 1 axé bénéfice","Titre SEO 2 axé résultat","Titre SEO 3 axé transformation"],"paragraphes":[{{"titre":"Titre percutant du paragraphe 1","texte":"4 phrases max de description produit convaincante."}},{{"titre":"Titre percutant 2","texte":"4 phrases."}},{{"titre":"Titre 3","texte":"4 phrases."}},{{"titre":"Titre 4","texte":"4 phrases."}},{{"titre":"Titre 5","texte":"4 phrases."}},{{"titre":"Titre 6","texte":"4 phrases."}}]}}""",SYS,2000)
        st.session_state.res["shopify"]=pjson(raw) or {"titres":["Titre 1","Titre 2","Titre 3"],"paragraphes":[{"titre":"Paragraphe","texte":"Contenu."}]*6}

        # FB ADS
        bar.progress(50,"📢 Facebook Ads…")
        raw=groq(f"""Génère 3 textes publicitaires Facebook pour "{pname}", marché africain francophone.
RÈGLES: max 70 mots chacun. Structure: 1 accroche CHOC qui surprend, puis exactement 3 bénéfices en tirets.
JSON UNIQUEMENT:
{{"ads":[{{"accroche":"TITRE CHOC ICI","b1":"Premier bénéfice concret","b2":"Deuxième bénéfice","b3":"Troisième bénéfice","mots":45}},{{"accroche":"TITRE 2","b1":"b1","b2":"b2","b3":"b3","mots":50}},{{"accroche":"TITRE 3","b1":"b1","b2":"b2","b3":"b3","mots":48}}]}}""",SYS,700)
        st.session_state.res["fb"]=pjson(raw) or {"ads":[{"accroche":"Vous ne savez pas encore que ce produit va changer votre quotidien","b1":"Bénéfice 1","b2":"Bénéfice 2","b3":"Bénéfice 3","mots":40}]}

        # VOIX OFF
        bar.progress(63,"🎙️ Voix off…")
        raw=groq(f"""Génère 3 scripts de voix off pour "{pname}", marché africain francophone.
RÈGLE ABSOLUE: chaque script doit faire ENTRE 120 ET 140 MOTS. Compte bien.
Structure de CHAQUE script:
[PROBLÈME] 2-3 phrases percutantes sur le problème que le client vit
[SOLUTION] 2-3 phrases présentant le produit comme la solution
[FONCTIONNEMENT] 2-3 phrases sur comment le produit agit
[TÉMOIGNAGE] 2-3 phrases avec un prénom africain authentique (Aminata, Kofi, Fatou, Ibrahim, Moussa, Aïssatou, Seydou, Mariam...)
Neuromarketing: déclenche émotions, urgence, identification.
JSON UNIQUEMENT:
{{"scripts":[{{"texte":"script complet 120-140 mots ici","mots":125}},{{"texte":"script 2","mots":130}},{{"texte":"script 3","mots":128}}]}}""",SYS,2500)
        st.session_state.res["voix"]=pjson(raw) or {"scripts":[{"texte":"Script en cours de génération...","mots":0}]}

        # AVATAR
        bar.progress(78,"👤 Avatar client…")
        raw=groq(f"""Crée l'avatar client idéal pour "{pname}" en Afrique francophone. Très précis et concret.
JSON UNIQUEMENT:
{{"prenom":"Fatou","emoji":"👩","sexe":"Femme","age":"28-42 ans","situation":"Mariée, 2 enfants","revenus":"80 000 – 150 000 FCFA/mois","profession":"Commerçante / Fonctionnaire","ville":"Abidjan, Dakar, Douala (grandes villes)","reseaux":["Facebook","WhatsApp","TikTok"],"heure":"19h – 22h","peurs":["peur précise 1","peur précise 2","peur précise 3"],"frustrations":["frustration précise 1","frustration précise 2","frustration précise 3"],"desirs":["désir précis 1","désir précis 2","désir précis 3"],"motivations":["motivation 1","motivation 2"],"phrase":"La phrase exacte qui va lui faire acheter immédiatement le produit","objections":["objection 1","objection 2"],"reponses":["réponse 1","réponse 2"],"pour_qui":"Pour elle-même","budget":"10 000 – 15 000 FCFA","livraison":"Livraison à domicile"}}""",SYS,1200)
        st.session_state.res["avatar"]=pjson(raw) or {"prenom":"Fatou","emoji":"👩","sexe":"Femme","age":"28-40 ans","revenus":"75 000 – 150 000 FCFA/mois","profession":"Commerçante","ville":"Abidjan, Dakar","reseaux":["Facebook","WhatsApp"],"heure":"19h-22h","peurs":["Ne pas obtenir de résultats"],"frustrations":["Produits qui ne fonctionnent pas"],"desirs":["Avoir confiance en elle"],"motivations":["Améliorer son quotidien"],"phrase":"Ce produit a changé ma vie, essayez-le aujourd'hui.","objections":["Trop cher"],"reponses":["Paiement à la livraison"],"pour_qui":"Pour elle-même","budget":"15 000 FCFA","livraison":"À domicile"}

        bar.progress(100,"✅ Analyse terminée !")
        st.session_state.gen=True; st.session_state.form_open=False
        st.balloons(); st.rerun()

# ══════════════════════════════════════════════════════
#  RÉSULTATS
# ══════════════════════════════════════════════════════
if not st.session_state.gen:
    if not st.session_state.form_open:
        st.markdown("""<div style="text-align:center;padding:4rem 1rem;">
          <div style="font-size:3.5rem;">⚡</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:#ff2d55;margin:.8rem 0;">Prêt à analyser votre produit ?</div>
          <div style="color:#a0a0b0;font-size:.9rem;">Ouvrez le formulaire ci-dessus et lancez l'analyse.</div>
        </div>""", unsafe_allow_html=True)
    st.stop()

R=st.session_state.res; PN=st.session_state.pname; PR=R.get("pricing",{})

tabs=st.tabs(["💰 Prix & Gains","🎯 Score","🎁 Offres","🛍️ Shopify","📢 Facebook Ads","🎙️ Voix Off","👤 Avatar","🖼️ Images","🎬 Vidéos","⚔️ Concurrence"])

# ─── 1. PRIX & GAINS ─────────────────────────────────
with tabs[0]:
    sell=PR.get("rec",0); profit=PR.get("profit",0); pub=PR.get("pub",5000)
    cl=PR.get("cl",1000); liv=PR.get("liv",2000); cost=st.session_state.pcost; tg=st.session_state.ptarget

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">💰 Stratégie de prix — {PN}</div>', unsafe_allow_html=True)
    m1,m2,m3,m4=st.columns(4)
    for col,lbl,val,cls in [(m1,"Prix minimum",PR.get("min",0),"amber"),(m2,"Prix recommandé",sell,"red"),(m3,"Prix maximum",PR.get("max",0),"amber"),(m4,"Bénéfice net / vente",profit,"green")]:
        with col: st.markdown(f'<div class="metric"><div class="metric-val {cls}">{val:,} FCFA</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📊 Charges par vente</div>', unsafe_allow_html=True)
    d1,d2,d3,d4=st.columns(4)
    for col,lbl,val,cls in [(d1,"📣 Publicité",pub,"red"),(d2,"📞 Closing",cl,"amber"),(d3,"🚚 Livraison",liv,"amber"),(d4,"💚 Votre gain",profit,"green")]:
        with col: st.markdown(f'<div class="metric"><div class="metric-val {cls}">{val:,} FCFA</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📈 Tableau de gains — 1 à 10 ventes / jour</div>', unsafe_allow_html=True)
    rows=""
    for v in range(1,11):
        ca=v*sell;cp=v*cost;dp=v*pub;dc=v*cl;dl=v*liv;bn=ca-cp-dp-dc-dl;bm=bn*30
        cc="c-g" if bn>0 else "c-r"
        rows+=f"<tr><td><b>{v}</b></td><td class='c-a'>{ca:,}</td><td class='c-r'>{cp:,}</td><td class='c-r'>{dp:,}</td><td class='c-r'>{dc:,}</td><td class='c-r'>{dl:,}</td><td class='{cc}'>{bn:,}</td><td class='{cc}'>{bm:,}</td></tr>"
    st.markdown(f"""<table class="tbl"><thead><tr><th>Ventes/j</th><th>CA (FCFA)</th><th>Coût prod.</th><th>Pub</th><th>Closing</th><th>Livraison</th><th>Bénéf./j</th><th>Bénéf./mois</th></tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📣 Budget Facebook Ads recommandé</div>', unsafe_allow_html=True)
    if tg<=7:    fb=("5 $","1 créative","#30d158")
    elif tg<=12: fb=("7 – 8 $","1-2 créatives","#ff9f0a")
    elif tg<=20: fb=("10 – 15 $","2-3 créatives","#ff2d55")
    else:        fb=("15 $+","3+ créatives","#bf5af2")
    st.markdown(f"""<div class="budget-hero">
      <div class="budget-num" style="color:{fb[2]};">{fb[0]} <span style="font-size:1.2rem;color:#a0a0b0;">/ jour</span></div>
      <div class="budget-sub">Pour votre objectif de {tg} ventes/jour — {fb[1]}</div>
    </div>
    <div class="tip">💡 <b>Conseil :</b> Démarrez avec 1 seule créative et {fb[0]}/jour. Après 3 jours, si le coût par achat (CPA) est inférieur à <b>{profit:,} FCFA</b>, augmentez progressivement le budget.</div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 2. SCORE ────────────────────────────────────────
with tabs[1]:
    SD=R.get("score",{}); sv=float(SD.get("score",7))
    verdict=SD.get("verdict","Bon"); couleur=SD.get("couleur","amber")
    sc={"red":"#ff2d55","amber":"#ff9f0a","green":"#30d158","orange":"#ff9f0a"}.get(couleur,"#ff9f0a")
    circ=int((sv/10)*251); anti=251-circ

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f"""<div class="score-wrap">
      <svg class="score-ring-svg" width="200" height="200" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" fill="none" stroke="#1c1c28" stroke-width="10"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="{sc}" stroke-width="10"
          stroke-dasharray="{circ} {anti}" stroke-dashoffset="63" stroke-linecap="round"/>
        <text x="50" y="45" text-anchor="middle" font-family="Syne,sans-serif" font-size="20" font-weight="800" fill="{sc}">{sv}</text>
        <text x="50" y="58" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="8" fill="#606070">/ 10</text>
      </svg>
      <div class="score-verdict" style="color:{sc};">{verdict}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📊 Détail par critère</div>', unsafe_allow_html=True)
    for lbl,key in [("💰 Rentabilité","note_r"),("📈 Demande marché","note_d"),("⚔️ Concurrence","note_c"),("🎨 Créatives dispo","note_cr"),("🔥 Viral FB/TikTok","note_v"),("🌍 Pertinence Afrique","note_a"),("💵 Prix psychologique","note_p"),("🔄 Fidélisation","note_f")]:
        v=SD.get(key,7); pct=v*10; bc="#30d158" if v>=7 else "#ff9f0a" if v>=5 else "#ff2d55"
        st.markdown(f'<div class="bar-row"><div class="bar-lbl">{lbl}</div><div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{bc};"></div></div><div class="bar-val" style="color:{bc};">{v}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    cA,cB=st.columns(2)
    with cA:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">✅ Points forts</div>', unsafe_allow_html=True)
        for p in SD.get("forts",[]):
            st.markdown(f'<div style="padding:.45rem .8rem;background:rgba(48,209,88,.08);border-left:3px solid #30d158;border-radius:0 8px 8px 0;margin:.3rem 0;font-size:.87rem;">✅ {p}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with cB:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">⚠️ Points à surveiller</div>', unsafe_allow_html=True)
        for p in SD.get("faibles",[]):
            st.markdown(f'<div style="padding:.45rem .8rem;background:rgba(255,45,85,.08);border-left:3px solid #ff2d55;border-radius:0 8px 8px 0;margin:.3rem 0;font-size:.87rem;">⚠️ {p}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🧭 Recommandation stratégique</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.92rem;line-height:1.8;margin-bottom:.8rem;">{SD.get("conseil","")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.82rem;color:#a0a0b0;">🌍 <b style="color:#ff9f0a;">Marchés :</b> {", ".join(SD.get("pays",[]))} &nbsp;|&nbsp; 📅 <b style="color:#ff9f0a;">Période :</b> {SD.get("periode","")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 3. OFFRES ───────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🎁 Offres marketing — {PN}</div>', unsafe_allow_html=True)
    for o in R.get("offres",{}).get("offres",[]):
        imp=o.get("impact","Moyen"); ic="#30d158" if "Élevé" in imp or "Fort" in imp else "#ff9f0a"
        st.markdown(f"""<div class="offer">
          <div class="offer-head">
            <div class="offer-name">{o.get('emoji','🎯')} {o.get('titre','')}</div>
            <span class="offer-badge" style="background:{ic}22;color:{ic};border:1px solid {ic}44;">{imp}</span>
          </div>
          <div style="font-size:.87rem;color:#a0a0b0;">{o.get('desc','')}</div>
          <div class="offer-tip">💡 {o.get('conseil','')}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 4. SHOPIFY ──────────────────────────────────────
with tabs[3]:
    SH=R.get("shopify",{})
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🏷️ 3 Titres produit optimisés</div>', unsafe_allow_html=True)
    for i,t in enumerate(SH.get("titres",[]),1):
        st.markdown(f'<div style="font-size:.72rem;letter-spacing:1.5px;text-transform:uppercase;color:#a0a0b0;margin-bottom:.2rem;">Titre {i}</div>', unsafe_allow_html=True)
        copy_row(t, f"sh_t{i}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📝 6 Paragraphes de description</div>', unsafe_allow_html=True)
    for i,p in enumerate(SH.get("paragraphes",[]),1):
        titre=p.get("titre",""); texte=p.get("texte","")
        st.markdown(f'<div style="font-family:Syne,sans-serif;font-weight:700;font-size:.95rem;color:#ff9f0a;margin-top:1rem;margin-bottom:.3rem;">▶ {titre}</div>', unsafe_allow_html=True)
        copy_row(texte, f"sh_p{i}")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 5. FACEBOOK ADS ─────────────────────────────────
with tabs[4]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">📢 Facebook Ads — {PN}</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.78rem;color:#a0a0b0;margin-bottom:1rem;">3 textes ≤ 70 mots • Accroche choc + 3 bénéfices</div>', unsafe_allow_html=True)
    for i,ad in enumerate(R.get("fb",{}).get("ads",[]),1):
        full=f"{ad.get('accroche','')}\n\n- {ad.get('b1','')}\n- {ad.get('b2','')}\n- {ad.get('b3','')}"
        st.markdown(f'<div style="font-size:.72rem;letter-spacing:1.5px;text-transform:uppercase;color:#a0a0b0;margin-bottom:.3rem;margin-top:.8rem;">Texte #{i} — {ad.get("mots","~")} mots</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="ad-card">
          <div class="ad-hook">🔥 {ad.get('accroche','')}</div>
          <div class="ad-pip">{ad.get('b1','')}</div>
          <div class="ad-pip">{ad.get('b2','')}</div>
          <div class="ad-pip">{ad.get('b3','')}</div>
        </div>""", unsafe_allow_html=True)
        copy_row(full, f"fb_{i}")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 6. VOIX OFF ─────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🎙️ Scripts voix off — {PN}</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.78rem;color:#a0a0b0;margin-bottom:1rem;">3 scripts • 120-140 mots chacun • Neuromarketing africain • Problème → Solution → Fonctionnement → Témoignage</div>', unsafe_allow_html=True)
    for i,s in enumerate(R.get("voix",{}).get("scripts",[]),1):
        txt=s.get("texte",""); mots=s.get("mots",len(txt.split()))
        mc="#30d158" if 120<=mots<=140 else "#ff9f0a"
        st.markdown(f"""<div style="display:flex;align-items:center;gap:.6rem;margin-top:1rem;margin-bottom:.3rem;">
          <div style="font-family:Syne,sans-serif;font-weight:700;font-size:.9rem;color:#ff2d55;">Script #{i}</div>
          <span style="font-size:.72rem;color:{mc};border:1px solid {mc}44;padding:.15rem .5rem;border-radius:20px;">{mots} mots</span>
        </div>""", unsafe_allow_html=True)
        copy_row(txt, f"vo_{i}")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 7. AVATAR ───────────────────────────────────────
with tabs[6]:
    AV=R.get("avatar",{})
    st.markdown('<div class="av-card">', unsafe_allow_html=True)
    st.markdown(f"""<div class="av-head">
      <div class="av-avatar">{AV.get('emoji','👤')}</div>
      <div>
        <div class="av-name">{AV.get('prenom','Avatar')}</div>
        <div class="av-role">{AV.get('profession','')} • {AV.get('ville','')}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    cL,cR=st.columns(2)
    with cL:
        for lbl,key in [("🚻 Sexe","sexe"),("🎂 Âge","age"),("👨‍👩‍👧 Situation","situation"),("💵 Revenus","revenus"),("🕐 En ligne","heure"),("💰 Budget max","budget"),("🛵 Livraison","livraison"),("🛍️ Achète pour","pour_qui")]:
            v=AV.get(key,"")
            if v: st.markdown(f'<div class="av-row"><div class="av-key">{lbl}</div><div class="av-val">{v}</div></div>', unsafe_allow_html=True)
        rs=AV.get("reseaux",[])
        if rs:
            badges="".join([f'<span class="badge">{s}</span>' for s in rs])
            st.markdown(f'<div class="av-row"><div class="av-key">📱 Réseaux</div><div class="av-val">{badges}</div></div>', unsafe_allow_html=True)
    with cR:
        for lbl,key,clr in [("😱 Peurs","peurs","#ff2d55"),("😤 Frustrations","frustrations","#ff9f0a"),("💫 Désirs","desirs","#bf5af2"),("⚡ Motivations","motivations","#30d158"),("❓ Objections","objections","#ff9f0a"),("✅ Réponses","reponses","#30d158")]:
            items=AV.get(key,[])
            if items:
                bullets="".join([f'<div style="padding:.3rem .6rem;background:rgba(0,0,0,.3);border-left:2px solid {clr};border-radius:0 6px 6px 0;margin:.2rem 0;font-size:.84rem;">▸ {x}</div>' for x in items])
                st.markdown(f'<div style="margin:.5rem 0;"><div style="font-size:.7rem;letter-spacing:1.5px;text-transform:uppercase;color:{clr};margin-bottom:.3rem;">{lbl}</div>{bullets}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    phrase=AV.get("phrase","")
    if phrase:
        st.markdown(f"""<div class="phrase-card">
          <div style="font-size:.72rem;letter-spacing:2px;text-transform:uppercase;color:#ff9f0a;margin-bottom:.6rem;">💬 Phrase déclenchante</div>
          <div class="phrase-quote">"{phrase}"</div>
        </div>""", unsafe_allow_html=True)
        copy_row(phrase, "phrase_av")

# ─── 8. IMAGES ───────────────────────────────────────
with tabs[7]:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🖼️ Images — {PN}</div>', unsafe_allow_html=True)

    if st.session_state.pimages:
        st.markdown("**Vos images uploadées**")
        st.markdown('<div class="thumb-grid">', unsafe_allow_html=True)
        for img in st.session_state.pimages:
            img.seek(0); b64=base64.b64encode(img.read()).decode(); ext=img.name.split(".")[-1]
            st.markdown(f'<div class="thumb-item"><img src="data:image/{ext};base64,{b64}"><a class="thumb-dl" href="data:image/{ext};base64,{b64}" download="{img.name}">⬇ DL</a></div>', unsafe_allow_html=True)
            img.seek(0)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    st.markdown("**Rechercher des images en ligne**")
    q=urllib.parse.quote(PN)
    st.markdown('<div class="bubble-wrap">', unsafe_allow_html=True)
    for name,url,clr,bg in [
        ("AliExpress",f"https://fr.aliexpress.com/wholesale?SearchText={q}","#ff6010","rgba(255,96,16,.12)"),
        ("Alibaba",f"https://www.alibaba.com/trade/search?SearchText={q}","#e6380a","rgba(230,56,10,.12)"),
        ("Pinterest",f"https://www.pinterest.com/search/pins/?q={q}","#e60023","rgba(230,0,35,.12)"),
        ("Temu",f"https://www.temu.com/search_result.html?search_key={q}","#ff9f0a","rgba(255,159,10,.12)"),
        ("Google Images",f"https://www.google.com/search?q={q}&tbm=isch","#4285f4","rgba(66,133,244,.12)"),
        ("Amazon",f"https://www.amazon.fr/s?k={q}","#ff9900","rgba(255,153,0,.12)"),
    ]:
        st.markdown(f'<a href="{url}" target="_blank" class="bubble" style="background:{bg};color:{clr};border:1px solid {clr}33;">🔍 {name}</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 9. VIDÉOS ───────────────────────────────────────
with tabs[8]:
    q=urllib.parse.quote(PN)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🎬 Vidéos produit — {PN}</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.78rem;color:#a0a0b0;margin-bottom:1rem;">Cliquez sur un pays pour ouvrir la recherche directement avec votre produit</div>', unsafe_allow_html=True)

    for pname_v,clr,bg,make in [
        ("▶️ YouTube","#ff0000","rgba(255,0,0,.1)",lambda p: f"https://www.youtube.com/results?search_query={q}+{urllib.parse.quote(p)}"),
        ("🎵 TikTok","#69c9d0","rgba(105,201,208,.1)",lambda p: f"https://www.tiktok.com/search?q={q}+{urllib.parse.quote(p)}"),
        ("📌 Pinterest","#e60023","rgba(230,0,35,.1)",lambda p: f"https://www.pinterest.com/search/pins/?q={q}+{urllib.parse.quote(p)}"),
        ("🔍 Google Vidéos","#4285f4","rgba(66,133,244,.1)",lambda p: f"https://www.google.com/search?q={q}+{urllib.parse.quote(p)}&tbm=vid"),
        ("🟠 AliExpress","#ff6010","rgba(255,96,16,.1)",lambda p: f"https://fr.aliexpress.com/wholesale?SearchText={q}"),
    ]:
        st.markdown(f'<div style="margin:.8rem 0;"><div style="font-size:.78rem;font-family:Syne,sans-serif;font-weight:700;color:{clr};letter-spacing:1px;margin-bottom:.4rem;">{pname_v}</div><div class="bubble-wrap">', unsafe_allow_html=True)
        for pays in PAYS:
            url=make(pays)
            st.markdown(f'<a href="{url}" target="_blank" class="bubble" style="background:{bg};color:{clr};border:1px solid {clr}33;">🌍 {pays}</a>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── 10. CONCURRENCE ─────────────────────────────────
with tabs[9]:
    q=urllib.parse.quote(PN)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📚 Bibliothèque Publicitaire Facebook par pays</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.78rem;color:#a0a0b0;margin-bottom:.8rem;">Voyez toutes les publicités actives de vos concurrents — cliquez sur un pays</div>', unsafe_allow_html=True)
    st.markdown('<div class="bubble-wrap">', unsafe_allow_html=True)
    for pays in PAYS:
        code=CODES.get(pays,"")
        url=f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={code}&q={q}&search_type=keyword_unordered"
        st.markdown(f'<a href="{url}" target="_blank" class="bubble" style="background:rgba(24,119,242,.12);color:#1877f2;border:1px solid #1877f233;">🌍 {pays}</a>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    for sname,sclr,sbg,make in [
        ("🛒 Boutiques Facebook Pages","#1877f2","rgba(24,119,242,.1)",lambda p: f"https://www.facebook.com/search/pages/?q={q}+boutique+{urllib.parse.quote(p)}"),
        ("🌐 Google Shopping","#4285f4","rgba(66,133,244,.1)",lambda p: f"https://www.google.com/search?q={q}+boutique+{urllib.parse.quote(p)}&tbm=shop"),
        ("🟠 AliExpress Boutiques","#ff6010","rgba(255,96,16,.1)",lambda p: f"https://fr.aliexpress.com/wholesale?SearchText={q}"),
        ("🔵 Jumia","#f68b1e","rgba(246,139,30,.1)",lambda p: f"https://www.jumia.com/catalog/?q={q}"),
    ]:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-title">{sname}</div>', unsafe_allow_html=True)
        st.markdown('<div class="bubble-wrap">', unsafe_allow_html=True)
        for pays in PAYS:
            url=make(pays)
            st.markdown(f'<a href="{url}" target="_blank" class="bubble" style="background:{sbg};color:{sclr};border:1px solid {sclr}33;">🌍 {pays}</a>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("""<div class="tip">
      💡 <b>Comment lire la concurrence :</b><br>
      +50 pubs actives = marché validé ✅ (mais concurrence forte) &nbsp;|&nbsp;
      0-10 pubs = marché non validé ⚠️ (risque ou opportunité) &nbsp;|&nbsp;
      Inspirez-vous des meilleures accroches et offrez quelque chose de différent.
    </div>""", unsafe_allow_html=True)
