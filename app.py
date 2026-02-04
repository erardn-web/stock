import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="GéoStock Ergo", layout="wide")

st.title("📦 Gestion de Matériel Ergothérapie")

# 1. Connexion au Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Fonction pour charger les données sans cache pour voir les modifs en temps réel
def load_data():
    try:
        stock = conn.read(worksheet="stock", ttl=0)
        hist = conn.read(worksheet="historique", ttl=0)
        # Nettoyage des colonnes au cas où
        stock = stock.dropna(how='all')
        hist = hist.dropna(how='all')
        return stock, hist
    except Exception as e:
        st.error("Erreur de lecture du Google Sheet. Vérifiez les noms d'onglets 'stock' et 'historique'.")
        return pd.DataFrame(), pd.DataFrame()

df_stock, df_hist = load_data()

tab1, tab2, tab3 = st.tabs(["📋 Inventaire & Actions", "➕ Ajouter Matériel", "📜 Historique Complet"])

# --- TAB 1 : INVENTAIRE & ACTIONS ---
with tab1:
    st.header("État du stock")
    if not df_stock.empty:
        # On affiche le stock avec un sélecteur pour agir sur un objet
        selected_item_name = st.selectbox("Sélectionner un objet pour changer son statut :", 
                                        ["---"] + df_stock["nom"].tolist())
        
        if selected_item_name != "---":
            item_data = df_stock[df_stock["nom"] == selected_item_name].iloc[0]
            st.info(f"Statut actuel : **{item_data['statut']}** | Origine : {item_data['provenance']}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🤝 Prêter"):
                    new_status, action = "Prêté", "Prêt"
            with col2:
                if st.button("🔄 Retourner"):
                    new_status, action = "Disponible", "Retour"
            with col3:
                if st.button("💰 Vendre"):
                    new_status, action = "Vendu", "Vente"
            with col4:
                if st.button("🗑️ Jeter"):
                    new_status, action = "Jeté", "Mise au rebut"

            # Logique de mise à jour si un bouton est cliqué
            if 'new_status' in locals():
                # Mise à jour du stock
                df_stock.loc[df_stock["nom"] == selected_item_name, "statut"] = new_status
                
                # Ajout à l'historique
                new_h = pd.DataFrame([{
                    "id_materiel": item_data["id"],
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "action": action,
                    "notes": f"Passage au statut {new_status}"
                }])
                df_hist = pd.concat([df_hist, new_h], ignore_index=True)
                
                # Sauvegarde
                conn.update(worksheet="stock", data=df_stock)
                conn.update(worksheet="historique", data=df_hist)
                st.success(f"Statut mis à jour : {new_status}")
                st.rerun()

        st.divider()
        st.dataframe(df_stock, use_container_width=True, hide_index=True)
    else:
        st.info("L'inventaire est vide.")

# --- TAB 2 : AJOUTER DU MATÉRIEL ---
with tab2:
    st.header("Nouvel objet")
    with st.form("ajout_objet"):
        nom = st.text_input("Nom de l'objet (ex: Déambulateur Rollator)")
        col_a, col_b = st.columns(2)
        with col_a:
            prov = st.selectbox("Mode d'obtention", ["Achat", "Prêt fournisseur", "Don"])
        with col_b:
            options = st.multiselect("Options possibles", ["Prêtable", "Louable", "Achetable"])
        
        submit = st.form_submit_button("Enregistrer")
        
        if submit and nom:
            new_id = int(df_stock["id"].max() + 1) if not df_stock.empty else 1
            new_item = pd.DataFrame([{
                "id": new_id, "nom": nom, "provenance": prov, 
                "options": ", ".join(options), "statut": "Disponible"
            }])
            new_h = pd.DataFrame([{
                "id_materiel": new_id, "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "action": "Création", "notes": f"Entrée initiale ({prov})"
            }])
            
            df_stock = pd.concat([df_stock, new_item], ignore_index=True)
            df_hist = pd.concat([df_hist, new_h], ignore_index=True)
            
            conn.update(worksheet="stock", data=df_stock)
            conn.update(worksheet="historique", data=df_hist)
            st.success("Objet ajouté !")
            st.rerun()

# --- TAB 3 : HISTORIQUE ---
with tab3:
    st.header("Historique des mouvements")
    if not df_hist.empty:
        # On fusionne avec le stock pour avoir le nom de l'objet au lieu de l'ID
        df_display = df_hist.merge(df_stock[['id', 'nom']], left_on='id_materiel', right_on='id', how='left')
        st.dataframe(df_display[['date', 'nom', 'action', 'notes']].sort_index(ascending=False), use_container_width=True)
    else:
        st.write("Aucun historique disponible.")
