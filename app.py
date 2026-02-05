import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Ergo", layout="wide")

# Utilisation de votre ID de document et de votre GID d'onglet spécifique
SHEET_ID = "11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8"
GID_STOCK = "1192360349" 

# Construction de l'URL de lecture directe
URL_STOCK = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid={GID_STOCK}"

def load_data():
    try:
        # Lecture directe du flux CSV
        return pd.read_csv(URL_STOCK)
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

# Bouton de rafraîchissement
if st.button("🔄 Actualiser les données"):
    st.cache_data.clear()
    st.rerun()

df_stock = load_data()

if not df_stock.empty:
    # Zone de recherche
    search = st.text_input("🔍 Rechercher un matériel (ex: Déambulateur)...")
    if search:
        df_stock = df_stock[df_stock.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    # Affichage du tableau
    st.dataframe(df_stock, use_container_width=True, hide_index=True)
else:
    st.warning("Le tableau est vide ou inaccessible. Vérifiez le partage du Google Sheet.")

st.divider()
# Bouton pour aller modifier les données
st.link_button("➕ Ajouter / Modifier sur Google Sheets", f"https://docs.google.com{SHEET_ID}/edit")
