import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Stock Ergo Pro", layout="wide")

# 1. Connexion sécurisée via les Secrets TOML
conn = st.connection("gsheets", type=GSheetsConnection)

# Fonction pour charger les données sans cache pour l'écriture
def load_data():
    stock = conn.read(worksheet="stock", ttl=0)
    # On s'assure que l'ID est bien un nombre
    stock['id'] = pd.to_numeric(stock['id'], errors='coerce')
    return stock.dropna(how='all')

df_stock = load_data()

st.title("📦 Gestion de Stock Ergothérapie")

tab1, tab2 = st.tabs(["📋 Inventaire & Actions", "➕ Ajouter un article"])

# --- TAB 1 : INVENTAIRE & ACTIONS ---
with tab1:
    if not df_stock.empty:
        # Barre de recherche
        search = st.text_input("🔍 Rechercher un matériel...")
        df_display = df_stock
        if search:
            df_display = df_stock[df_stock.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("⚙️ Modifier le statut d'un objet")
        
        # Formulaire de modification rapide
        with st.form("update_status"):
            item_to_update = st.selectbox("Choisir l'objet à modifier", df_stock["nom"].tolist())
            nouveau_statut = st.selectbox("Nouveau statut", ["Disponible", "Prêté", "Loué", "Vendu", "Jeté"])
            note_action = st.text_input("Note (ex: Prêté à Mme Martin)")
            
            if st.form_submit_button("Mettre à jour le statut"):
                # Mise à jour dans le DataFrame
                df_stock.loc[df_stock["nom"] == item_to_update, "statut"] = nouveau_statut
                
                # Sauvegarde directe dans Google Sheets
                conn.update(worksheet="stock", data=df_stock)
                st.success(f"✅ Statut de '{item_to_update}' mis à jour !")
                st.rerun()
    else:
        st.info("Le stock est vide.")

# --- TAB 2 : AJOUTER DU MATÉRIEL ---
with tab2:
    st.header("Nouvel enregistrement")
    with st.form("add_item"):
        nom = st.text_input("Nom de l'objet")
        prov = st.selectbox("Provenance", ["Achat", "Prêt fournisseur", "Don", "Autre"])
        opts = st.multiselect("Options", ["Prêtable", "Louable", "Achetable"])
        
        if st.form_submit_button("Enregistrer dans le Google Sheet"):
            if nom:
                # Calcul du prochain ID
                next_id = int(df_stock["id"].max() + 1) if not df_stock.empty else 1
                
                # Création de la nouvelle ligne
                new_row = pd.DataFrame([{
                    "id": next_id,
                    "nom": nom,
                    "provenance": prov,
                    "options": ", ".join(opts),
                    "statut": "Disponible"
                }])
                
                # Fusion et envoi
                df_updated = pd.concat([df_stock, new_row], ignore_index=True)
                conn.update(worksheet="stock", data=df_updated)
                
                st.success(f"✨ '{nom}' ajouté avec succès !")
                st.rerun()
            else:
                st.error("Veuillez entrer un nom d'objet.")

st.divider()
if st.button("🔄 Forcer la synchronisation"):
    st.cache_data.clear()
    st.rerun()
