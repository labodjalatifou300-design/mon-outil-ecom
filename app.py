import streamlit as st
from groq import Groq
import json

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EcoMaster Labo Pro",
    layout="wide"
)

# ---------------------------------------------------
# STYLE
# ---------------------------------------------------

st.markdown("""
<style>

body {
background-color:#0E0E0E;
color:white;
}

.stButton>button {
background:#D90429;
color:white;
border-radius:8px;
height:45px;
font-weight:bold;
}

.card{
background:#111;
padding:15px;
border-radius:10px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# GROQ
# ---------------------------------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ---------------------------------------------------
# COPY FUNCTION
# ---------------------------------------------------

def copy_button(text, key):

    st.markdown(f"""
    <button onclick="copy_{key}()" style="
    background:#D90429;
    color:white;
    border:none;
    padding:8px;
    border-radius:6px;
    margin-bottom:8px;
    ">
    Copier
    </button>

    <script>
    function copy_{key}(){{
        var text=`{text}`;
        if(navigator.clipboard){{
            navigator.clipboard.writeText(text);
        }}else{{
            var textarea=document.createElement("textarea");
            textarea.value=text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand("copy");
            document.body.removeChild(textarea);
        }}
    }}
    </script>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# IA CALL
# ---------------------------------------------------

def call_groq(product):

    prompt = f"""

Analyse ce produit : {product}

Réponds uniquement en JSON.

Structure exacte :

{{
"score": nombre,
"desirs": ["","",""],
"peurs": ["","",""],

"shopify_titles":[
"",
"",
""
],

"shopify_paragraphs":[
{{"title":"","text":""}},
{{"title":"","text":""}},
{{"title":"","text":""}},
{{"title":"","text":""}},
{{"title":"","text":""}}
],

"facebook_ads":[
"",
"",
""
],

"voice_script":""
}}

Règles :

Paragraphes Shopify :
3 phrases MAXIMUM.

Facebook Ads :
1 phrase choc
1 problème
1 solution
1 preuve
1 CTA

max 5 lignes.

"""

    chat = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )

    raw = chat.choices[0].message.content

    try:
        data = json.loads(raw)
    except:
        st.error("Erreur JSON IA")
        st.write(raw)
        return {}

    return data

# ---------------------------------------------------
# INTERFACE
# ---------------------------------------------------

st.title("🚀 EcoMaster Labo Pro")

st.write("Analyse produit e-commerce automatique")

col1,col2 = st.columns([2,1])

with col1:

    product = st.text_input("Nom du produit")

with col2:

    price = st.number_input("Prix d'achat FCFA",0)

if price:

    min_price = price + 8000
    max_price = price + 12000

    st.success(f"Prix conseillé : {min_price} - {max_price} FCFA")

# ---------------------------------------------------
# IMAGE
# ---------------------------------------------------

images = st.file_uploader(
    "Upload images",
    type=["png","jpg","jpeg"],
    accept_multiple_files=True
)

if images:

    cols = st.columns(len(images))

    for i,img in enumerate(images):
        cols[i].image(img)

# ---------------------------------------------------
# GENERATE
# ---------------------------------------------------

generate = st.button("⚡ Générer Stratégie")

# ---------------------------------------------------
# HISTORY
# ---------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# GENERATION
# ---------------------------------------------------

if generate and product:

    with st.spinner("Analyse IA..."):

        data = call_groq(product)

    if data:

        st.session_state.history.insert(0,{
            "name":product,
            "score":data["score"],
            "data":data
        })

        result = data

else:

    if st.session_state.history:

        result = st.session_state.history[0]["data"]

    else:

        result = None

# ---------------------------------------------------
# DISPLAY
# ---------------------------------------------------

if result:

    tabs = st.tabs([
        "Analyse",
        "Shopify",
        "Facebook Ads",
        "Voix Off"
    ])

# ---------------------------------------------------
# ANALYSE
# ---------------------------------------------------

    with tabs[0]:

        st.subheader("Score produit")

        st.metric("Potentiel",f"{result['score']}/10")

        st.subheader("Désirs clients")

        for d in result["desirs"]:
            st.write("•",d)

        st.subheader("Peurs clients")

        for p in result["peurs"]:
            st.write("•",p)

# ---------------------------------------------------
# SHOPIFY
# ---------------------------------------------------

    with tabs[1]:

        st.subheader("Titres")

        for i,t in enumerate(result["shopify_titles"]):

            st.markdown(f"### {t}")
            copy_button(t,f"title{i}")

        st.subheader("Paragraphes")

        for i,p in enumerate(result["shopify_paragraphs"]):

            text = f"{p['title']}\n{p['text']}"

            st.markdown(f"""
            <div class="card">
            <b>{p['title']}</b><br>
            {p['text']}
            </div>
            """,unsafe_allow_html=True)

            copy_button(text,f"para{i}")

# ---------------------------------------------------
# FACEBOOK ADS
# ---------------------------------------------------

    with tabs[2]:

        ads = result.get("facebook_ads") or []

        if len(ads)==0:

            st.warning("Pas de Facebook Ads générées")

        else:

            for i,ad in enumerate(ads):

                st.markdown(f"""
                <div class="card">{ad}</div>
                """,unsafe_allow_html=True)

                copy_button(ad,f"ad{i}")

# ---------------------------------------------------
# VOICE
# ---------------------------------------------------

    with tabs[3]:

        script = result["voice_script"]

        st.markdown(f"""
        <div class="card">{script}</div>
        """,unsafe_allow_html=True)

        copy_button(script,"voice")

# ---------------------------------------------------
# HISTORY PANEL
# ---------------------------------------------------

st.sidebar.title("Historique")

for i,h in enumerate(st.session_state.history):

    if st.sidebar.button(
        f"{h['name']} | Score {h['score']}/10",
        key=i
    ):
        st.session_state.history.insert(
            0,
            st.session_state.history.pop(i)
        )
        st.rerun()
    
