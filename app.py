import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Ergo", layout="wide")

# L'ID de votre document (Vérifié)
SHEET_ID = "11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8"
# L'ID de l'onglet 'stock' (Vérifié via votre URL)
GID_STOCK = "1192360349" 

# Construction propre de l'URL sans espaces
URL_STOCK = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid={GID_STOCK}"

def load_data():
    try:
        # On utilise storage_options pour éviter certains blocages réseau
        df = pd.read_csv(URL_STOCK, sep=',', on_bad_lines='skip')
        return df
    except Exception as e:
        # On affiche l'erreur détaillée pour comprendre si c'est le lien
        st.error(f"Détail de l'erreur : {e}")
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

# Bouton de rafraîchissement
if st.button("🔄 Actualiser l'inventaire"):
    st.cache_data.clear()
    st.rerun()

df_stock = load_data()

if not df_stock.empty:
    # Recherche
    search = st.text_input("🔍 Rechercher (ex: chaise, déambulateur...)")
    if search:
        df_stock = df_stock[df_stock.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    # Affichage
    st.dataframe(df_stock, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Impossible de lire les données.")
    st.info("Vérifiez que l'onglet 'stock' contient bien des données et que le partage est sur 'Tous les utilisateurs disposant du lien'.")

st.divider()
st.link_button("➕ Modifier les données sur Google Sheets", f"https://docs.google.com{SHEET_ID}/edit")
