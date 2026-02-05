import streamlit as st
import pandas as pd
from gspread_pandas import Spread
from datetime import datetime

st.set_page_config(page_title="Stock Ergo Pro", layout="wide")

# --- CLE PRIVEE COMPACTE (Format auto-nettoyant) ---
raw_key = "-----BEGIN PRIVATE KEY-----\\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCXmLNyCfYDgYPk\\nQLcRittmVdJOLm4mmlRLmrjva3moMQBdSw36OFdw0w2SLQMhGsxbP7yFaTlAXv4s\\nAwH6nF/MOJ1JqFE5gIMIbz18lqbEHEXqMHl80mnXz6ZyreFZrjQfz5yaEpC7k6nf\\nzQaX17iQ3iCuBjUR+qcb6TW0xsItJjU4srw8ITA1/EbRmxLnBSEza6EYpm3ZkJqr\\nfWGwA4oQAHB5AjeHvy/Wdb3Ji4b6eLDad75ttY6niia9n91GnYrf0mzCHDUvAqNG\\nIixGPV4Bt7M/s7o6m8JiLFtgMQ5iPXXDFFVb1xV7yw7AzvESurmwcMbDUH/WLyvU\\nlnPqUDLJAgMBAAECgf8gBrfiSmMZhS3CoD63YLPOgChYhqE+sTFIclIfl9UGc1O1\\ntzrSDJUXK39HzQ/xg80oeePvS2DiTdnknRNjSSXz6aymTajbPQscUmPrA5NiWuwU\\n+FNcy2xmQLgpV2gESjPjhI4mU/BqWwfIVXLPIVkclyYlnaoYjPDrie6OrRmDRVE5\\QwF7+xTmjyfk+BOkIGDI09AYK6OtPSv6+YCGDBTTGrDPJhP2htMx2OiqQ0vJQja0\\naYw6iCZzuz1vITadtYvg3sV+EtPWk/HN5r0D9ikkKkfE4QhzVA6xJfHPwuWvgmDI\\nDtbrST8OemZpvUWX0eLowKampbkyHFP5eNyTauECgYEAyF5po23n0ykxDZ+xBGvj\\nVpoNXf53aRM44LwPJI3ZoEJSCLAeBTGRSklpTBYUmqhJ8Rfh2F89bpe+fB+e89jo\\n6ab+pIc+K8WxgQ+zEyNUotjdC4oam8wA5SdByFRh0IGwdg6VaMNTYnqhbXk4tRFN\\ntFYV1EiYffH3k2ttbNigJHECgYEAwa+0fDn5JmNNICtoBhII2Z2GCRflVS15+Mxr\\nj5UcZkS3Z8zOpDL43Dg28wXhnAPScp7iBCggV1x8QuGtYPe8ie3hqubLKpGavcpL\\nZUPixO24tW6hjOWY2sRlZEvrcWhKbfV9KwcnzDSP/6yyJ3+cc+YffpKNNk63SR36\\nExHxv9kCgYAZpqyTdZCGIfHbsqPw0vcJsTMg42DaHNHdQ3YU0ewYbiUeY52UQKI/\\nBmLqkLEWk5DTwqDxGFA/BkImlc29nflDYFOdMIsvA2IUCbR9MLq3FlhGD+oUI+vB\\namMriFH1ZYT3uCo8fTUBmH1uDGTMGWj/Oz4ULS8IgJ+XSdt6YckuoQKBgQCjA/Y9\\nRDHt3FASjlX8Hfuy5MDmMGWFvkPVYn/5FgAUFyviQl99laUc/HdLLZ0ISbM7Y3xJ\\nEVi/DolLZVQetAPMdxmjVKKUjn4V1QiGD4/yPT5j/dwckTWIkxnfQ4LDLYrPZ3nU\\n2C3n0imMgFZlpiMQ7RN+3Wva1H+xG3jZyhWVaQKBgCFuQs+EllaHZYS/EVRgKqKs\\n/MMrHJyAzJSc5ItUjGJVXDamjy38MKh50mQ6L1iXWmf4ilw8xdWYHhqjfVWYEKWn\\nKaCKiw3wJZqpCHZC3ZP+6qAclgxczDe/AStCeYv/c7EU5P7lTLVEQf2XoETqAX6e\\nB3pqwbNSZBox8qUCgY5G\\n-----END PRIVATE KEY-----"

# On nettoie les doubles slashes si nécessaire pour Google
CLE_PROPRE = raw_key.replace("\\\\n", "\\n").encode().decode("unicode_escape")

creds = {
    "type": "service_account",
    "project_id": "stock-ergo",
    "private_key": CLE_PROPRE,
    "client_email": "id-6neuf@stock-ergo.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com",
}

# --- CHARGEMENT ---
try:
    spread = Spread("11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8", config=creds)
    df_stock = spread.sheet_to_df(sheet='stock', index=0).reset_index()
    df_hist = spread.sheet_to_df(sheet='historique', index=0).reset_index()
except Exception as e:
    st.error(f"Erreur technique : {e}")
    st.stop()

st.title("📦 Gestion Stock Ergo")

tab1, tab2, tab3 = st.tabs(["📋 Inventaire", "🔄 Mouvements", "➕ Ajouter"])

with tab1:
    st.dataframe(df_stock, use_container_width=True, hide_index=True)

with tab2:
    if not df_stock.empty:
        with st.form("mouv"):
            art = st.selectbox("Article", df_stock["nom"].unique())
            act = st.selectbox("Action", ["Prêt", "Retour", "Vente"])
            if st.form_submit_button("Valider"):
                stats = {"Prêt": "Prêté", "Retour": "Disponible", "Vente": "Vendu"}
                df_stock.loc[df_stock["nom"] == art, "statut"] = stats[act]
                spread.df_to_sheet(df_stock, sheet='stock', index=False, replace=True)
                st.success("Mis à jour !")
                st.rerun()

with tab3:
    with st.form("add"):
        n = st.text_input("Nom")
        if st.form_submit_button("Ajouter"):
            nid = int(df_stock["id"].max() + 1) if not df_stock.empty else 1
            new = pd.DataFrame([{"id": nid, "nom": n, "statut": "Disponible"}])
            df_stock = pd.concat([df_stock, new], ignore_index=True)
            spread.df_to_sheet(df_stock, sheet='stock', index=False, replace=True)
            st.rerun()
