import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GéoStock Ergo", layout="wide")

# Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # On lit les feuilles. Si erreur, on crée des tableaux vides.
    try:
        stock = conn.read(worksheet="stock", ttl=0)
        hist = conn.read(worksheet="historique", ttl=0)
        return stock.dropna(how='all'), hist.dropna(how='all')
    except:
        return pd.DataFrame(columns=["id", "nom", "provenance", "options", "statut"]), pd.DataFrame(columns=["id_materiel", "date", "action", "notes"])

df_stock, df_hist = load_data()

st.title("📦 Gestion de Stock Ergothérapie")

tab1, tab2, tab3 = st.tabs(["📋 Inventaire", "➕ Ajouter", "📜 Historique"])

with tab1:
    if not df_stock.empty:
        st.dataframe(df_stock, use_container_width=True, hide_index=True)
    else:
        st.info("Le stock est vide ou l'onglet 'stock' n'est pas trouvé.")

with tab2:
    with st.form("add_form"):
        nom = st.text_input("Nom du matériel")
        prov = st.selectbox("Provenance", ["Achat", "Prêt fournisseur", "Don"])
        opts = st.multiselect("Options", ["Prêtable", "Louable", "Achetable"])
        if st.form_submit_button("Enregistrer"):
            new_id = int(df_stock["id"].max() + 1) if not df_stock.empty else 1
            new_line = pd.DataFrame([{"id": new_id, "nom": nom, "provenance": prov, "options": ", ".join(opts), "statut": "Disponible"}])
            df_stock = pd.concat([df_stock, new_line], ignore_index=True)
            # Sauvegarde
            conn.update(worksheet="stock", data=df_stock)
            st.success("Matériel ajouté ! Actualisez la page.")
            st.rerun()

with tab3:
    st.dataframe(df_hist, use_container_width=True)
