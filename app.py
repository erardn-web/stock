import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="GéoStock Ergo", layout="wide")

st.title("📦 Gestion de Matériel Ergothérapie")

# 1. Connexion au Google Sheet
# L'URL du sheet doit être configurée dans les "Secrets" de Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection)

# Fonction pour charger les données
def load_data():
    stock = conn.read(worksheet="stock", ttl=0) # ttl=0 pour éviter le cache
    hist = conn.read(worksheet="historique", ttl=0)
    return stock, hist

df_stock, df_hist = load_data()

tab1, tab2, tab3 = st.tabs(["📋 Inventaire", "➕ Ajouter Matériel", "📜 Historique"])

# --- TAB 2 : AJOUTER DU MATÉRIEL ---
with tab2:
    st.header("Nouvel objet")
    with st.form("ajout_objet"):
        nom = st.text_input("Nom de l'objet (ex: Déambulateur Rollator)")
        
        col1, col2 = st.columns(2)
        with col1:
            prov = st.selectbox("Mode d'obtention", ["Achat", "Prêt fournisseur", "Don"])
        with col2:
            options = st.multiselect("Options possibles", ["Prêtable", "Louable", "Achetable"])
        
        submit = st.form_submit_button("Enregistrer dans le stock")
        
        if submit and nom:
            # Créer la nouvelle ligne de stock
            new_id = len(df_stock) + 1
            new_item = pd.DataFrame([{
                "id": new_id,
                "nom": nom,
                "provenance": prov,
                "options": ", ".join(options),
                "statut": "Disponible"
            }])
            
            # Créer la ligne d'historique
            new_hist = pd.DataFrame([{
                "id_materiel": new_id,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "action": "Création",
                "notes": f"Entrée en stock via {prov}"
            }])
            
            # Mise à jour globale
            updated_stock = pd.concat([df_stock, new_item], ignore_index=True)
            updated_hist = pd.concat([df_hist, new_hist], ignore_index=True)
            
            # Envoi vers Google Sheets
            conn.update(worksheet="stock", data=updated_stock)
            conn.update(worksheet="historique", data=updated_hist)
            
            st.success(f"'{nom}' a été ajouté et sauvegardé !")
            st.rerun()

# --- TAB 1 : INVENTAIRE ---
with tab1:
    st.header("Matériel disponible")
    if not df_stock.empty:
        # Affichage propre des données
        st.dataframe(df_stock, use_container_width=True, hide_index=True)
    else:
        st.info("L'inventaire est vide. Allez dans l'onglet 'Ajouter' pour commencer.")

# --- TAB 3 : HISTORIQUE ---
with tab3:
    st.header("Parcours d'un élément")
    if not df_stock.empty:
        choix = st.selectbox("Sélectionner un objet pour voir son historique", df_stock["nom"].unique())
        
        # Trouver l'ID correspondant au nom
        id_choisi = df_stock[df_stock["nom"] == choix]["id"].values[0]
        
        # Filtrer l'historique
        if not df_hist.empty:
            parcours = df_hist[df_hist["id_materiel"] == id_choisi]
            if not parcours.empty:
                st.table(parcours[["date", "action", "notes"]])
            else:
                st.warning("Aucun historique pour cet objet.")
    else:
        st.write("Aucune donnée.")
