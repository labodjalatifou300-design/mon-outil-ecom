import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuration de l'interface
st.set_page_config(page_title="e-com Family Tool by Labo", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #d90429; color: white; width: 100%; border-radius: 10px; font-weight: bold; }
    h1 { color: #d90429; text-align: center; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #1a1c23; color: white; border: 1px solid #d90429; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ e-com Family Tool by Labo")

# Clé API
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Entre ta clé API ici :", type="password")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Nom du produit")
    purchase_price = st.number_input("Prix d'achat (FCFA)", min_value=0)
    uploaded_file = st.file_uploader("Photo du produit", type=["jpg", "png", "jpeg"])

with col2:
    if purchase_price > 0:
        st.info(f"💰 Vendre entre : {purchase_price + 8000:,} FCFA et {purchase_price + 12000:,} FCFA")
        st.write("Budget Pub conseillé : 4$ à 7$ / jour (1 seule créative).")

if st.button("LANCER L'ANALYSE NEURO-MARKETING") and uploaded_file and api_key:
    try:
        genai.configure(api_key=api_key)
        # CHANGEMENT ICI : On utilise gemini-1.5-flash pour éviter l'erreur NotFound
        model = genai.GenerativeModel('gemini-1.5-flash')
        img = Image.open(uploaded_file)
        
        prompt = f"Analyse ce produit : {product_name}. Trouve les frustrations réelles des gens sur ce produit, leurs peurs et leurs désirs. Puis rédige un score /10, 5 paragraphes de vente Shopify (neuro-marketing), 3 titres chocs, 3 textes pubs Facebook et un script voix-off (Problème-Solution-Témoignage-CTA)."
        
        with st.spinner('Labo AI analyse le marché...'):
            response = model.generate_content([prompt, img])
            st.markdown("---")
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
