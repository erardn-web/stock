import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Ergo", layout="wide")

# URL DE PUBLICATION CSV
URL_CSV = "https://docs.google.com"

@st.cache_data(ttl=5)
def load_data():
    try:
        df = pd.read_csv(URL_CSV)
        return df.dropna(how='all')
    except:
        return pd.DataFrame()

# --- INTERFACE ---
st.title("📦 Gestion de Stock Ergothérapie")

# Barre d'actions en haut
col_search, col_add = st.columns([3, 1])

with col_add:
    # Bouton principal pour ajouter
    st.link_button("➕ Ajouter un article", 
                   "https://docs.google.com",
                   type="primary",
                   use_container_width=True)

with col_search:
    search = st.text_input("🔍 Rechercher un matériel (nom, provenance, statut...)", placeholder="Ex: Déambulateur")

# Chargement des données
df_stock = load_data()

if not df_stock.empty:
    # Filtrage si recherche
    if search:
        mask = df_stock.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        df_display = df_stock[mask]
    else:
        df_display = df_stock

    # Affichage des statistiques
    st.write(f"**{len(df_display)}** article(s) correspondant(s)")
    
    # Tableau
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Bouton de rafraîchissement discret
    if st.button("🔄 Actualiser la liste"):
        st.cache_data.clear()
        st.rerun()
else:
    st.warning("⚠️ Aucune donnée trouvée. Vérifiez que votre Google Sheet n'est pas vide.")

st.divider()
st.caption("Application de gestion légère - 2026")
