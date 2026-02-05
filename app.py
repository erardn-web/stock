import streamlit as st
import pandas as pd

st.set_page_config(page_title="GéoStock Ergo", layout="wide")

# ID de ton sheet
SHEET_ID = "11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8"
# URL d'export CSV (Fonctionne si le partage est "Tous les utilisateurs disposant du lien")
URL_STOCK = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid=0"

def load_data():
    try:
        # Lecture directe sans connecteur complexe
        df = pd.read_csv(URL_STOCK)
        return df
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return pd.DataFrame()

df_stock = load_data()

st.title("📦 Gestion de Stock Ergothérapie")

tab1, tab2 = st.tabs(["📋 Inventaire & Historique", "➕ Ajouter du matériel"])

with tab1:
    if not df_stock.empty:
        st.subheader("Articles en stock")
        # Recherche simple
        search = st.text_input("🔍 Rechercher un matériel...")
        if search:
            display_df = df_stock[df_stock['nom'].str.contains(search, case=False, na=False)]
        else:
            display_df = df_stock
            
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Le stock semble vide ou le fichier est inaccessible.")

with tab2:
    st.header("Ajouter un nouvel élément")
    st.info("Pour garantir la sécurité de vos données, l'ajout se fait directement dans le tableau sécurisé.")
    
    # Bouton qui ouvre ton Google Sheet directement au bon endroit
    st.link_button("👉 Ouvrir le Google Sheet pour ajouter / modifier", 
                   f"https://docs.google.com{SHEET_ID}/edit")
    
    st.markdown("""
    **Instructions :**
    1. Clique sur le bouton ci-dessus.
    2. Ajoute ta ligne dans l'onglet **stock**.
    3. Reviens ici et rafraîchis la page (Touche R) pour voir le changement.
    """)

# Affichage de l'historique (si l'onglet existe)
st.divider()
if st.button("🔄 Rafraîchir les données"):
    st.rerun()
