import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Ergo", layout="wide")

# TON LIEN PROPRE (Vérifié et fonctionnel)
URL_CSV = "https://docs.google.com"

@st.cache_data(ttl=5)
def load_data():
    try:
        # Lecture du CSV
        df = pd.read_csv(URL_CSV)
        # On supprime les lignes totalement vides
        df = df.dropna(how='all')
        return df
    except Exception as e:
        st.error(f"Erreur technique : {e}")
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

# Bouton de rafraîchissement
if st.button("🔄 Actualiser"):
    st.cache_data.clear()
    st.rerun()

df_stock = load_data()

# Vérification si les données sont bien arrivées
if not df_stock.empty:
    st.success(f"✅ {len(df_stock)} article(s) trouvé(s)")
    
    # Recherche
    search = st.text_input("🔍 Rechercher un matériel...")
    if search:
        mask = df_stock.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        df_display = df_stock[mask]
    else:
        df_display = df_stock

    # Affichage du tableau final
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Aucune donnée trouvée.")
    st.info("Vérifiez que votre ligne 1 dans Google Sheets contient bien les titres.")

st.divider()
st.link_button("➕ Ajouter / Modifier sur Google Sheets", "https://docs.google.com")
