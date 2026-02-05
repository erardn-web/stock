import streamlit as st
import pandas as pd
import io
import requests

st.set_page_config(page_title="Stock Ergo", layout="wide")

# URL DE PUBLICATION (On s'assure qu'elle demande du CSV)
URL_CSV = "https://docs.google.com"

@st.cache_data(ttl=5)
def load_data():
    try:
        # On télécharge d'abord le texte brut
        response = requests.get(URL_CSV, timeout=10)
        # On lit le texte ligne par ligne pour filtrer le code Google
        lignes_propres = []
        for line in response.text.splitlines():
            # Une ligne de stock ne contient pas de balises HTML ou CSS
            if "<" not in line and "{" not in line and "var(" not in line:
                lignes_propres.append(line)
        
        # On convertit les lignes filtrées en tableau
        csv_data = "\n".join(lignes_propres)
        df = pd.read_csv(io.StringIO(csv_data), on_bad_lines='skip')
        return df.dropna(how='all')
    except Exception as e:
        return pd.DataFrame()

st.title("📦 Gestion de Stock Ergothérapie")

# Bouton de rafraîchissement
if st.button("🔄 Actualiser"):
    st.cache_data.clear()
    st.rerun()

df_stock = load_data()

if not df_stock.empty and len(df_stock.columns) > 1:
    st.success(f"✅ {len(df_stock)} article(s) trouvé(s)")
    
    # Recherche
    search = st.text_input("🔍 Rechercher un matériel...")
    if search:
        mask = df_stock.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        df_display = df_stock[mask]
    else:
        df_display = df_stock

    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Les données sont en cours de synchronisation...")
    st.info("Vérifiez sur Google Sheets : Fichier > Partager > Publier sur le web. Cliquez sur 'Arrêter la publication' puis 'Publier' à nouveau en choisissant bien 'Valeurs séparées par des virgules (.csv)'.")

st.divider()
st.link_button("➕ Ajouter / Modifier sur Google Sheets", "https://docs.google.com")
