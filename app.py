import streamlit as st
import pandas as pd
from gspread_pandas import Spread, Client
from datetime import datetime

st.set_page_config(page_title="Stock Ergo Pro", layout="wide")

# Configuration des identifiants en direct
creds = {
    "type": "service_account",
    "project_id": "stock-ergo",
    "private_key_id": "5e62902c2f1be2356209dc3cb16a5059def2dd93",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCXmLNyCfYDgYPk\nQLcRittmVdJOLm4mmlRLmrjva3moMQBdSw36OFdw0w2SLQMhGsxbP7yFaTlAXv4s\nAwH6nF/MOJ1JqFE5gIMIbz18lqbEHEXqMHl80mnXz6ZyreFZrjQfz5yaEpC7k6nf\nzQaX17iQ3iCuBjUR+qcb6TW0xsItJjU4srw8ITA1/EbRmxLnBSEza6EYpm3ZkJqr\nfWGwA4oQAHB5AjeHvy/Wdb3Ji4b6eLDad75ttY6niia9n91GnYrf0mzCHDUvAqNG\nIixGPV4Bt7M/s7o6m8JiLFtgMQ5iPXXDFFVb1xV7yw7AzvESurmwcMbDUH/WLyvU\nlnPqUDLJAgMBAAECgf8gBrfiSmMZhS3CoD63YLPOgChYhqE+sTFIclIfl9UGc1O1\ntzrSDJUXK39HzQ/xg80oeePvS2DiTdnknRNjSSXz6aymTajbPQscUmPrA5NiWuwU\n+FNcy2xmQLgpV2gESjPjhI4mU/BqWwfIVXLPIVkclyYlnaoYjPDrie6OrRmDRVE5\QwF7+xTmjyfk+BOkIGDI09AYK6OtPSv6+YCGDBTTGrDPJhP2htMx2OiqQ0vJQja0\naYw6iCZzuz1vITadtYvg3sV+EtPWk/HN5r0D9ikkKkfE4QhzVA6xJfHPwuWvgmDI\nDtbrST8OemZpvUWX0eLowKampbkyHFP5eNyTauECgYEAyF5po23n0ykxDZ+xBGvj\nVpoNXf53aRM44LwPJI3ZoEJSCLAeBTGRSklpTBYUmqhJ8Rfh2F89bpe+fB+e89jo\n6ab+pIc+K8WxgQ+zEyNUotjdC4oam8wA5SdByFRh0IGwdg6VaMNTYnqhbXk4tRFN\ntFYV1EiYffH3k2ttbNigJHECgYEAwa+0fDn5JmNNICtoBhII2Z2GCRflVS15+Mxr\nj5UcZkS3Z8zOpDL43Dg28wXhnAPScp7iBCggV1x8QuGtYPe8ie3hqubLKpGavcpL\nZUPixO24tW6hjOWY2sRlZEvrcWhKbfV9KwcnzDSP/6yyJ3+cc+YffpKNNk63SR36\nExHxv9kCgYAZpqyTdZCGIfHbsqPw0vcJsTMg42DaHNHdQ3YU0ewYbiUeY52UQKI/\nBmLqkLEWk5DTwqDxGFA/BkImlc29nflDYFOdMIsvA2IUCbR9MLq3FlhGD+oUI+vB\namMriFH1ZYT3uCo8fTUBmH1uDGTMGWj/Oz4ULS8IgJ+XSdt6YckuoQKBgQCjA/Y9\nRDHt3FASjlX8Hfuy5MDmMGWFvkPVYn/5FgAUFyviQl99laUc/HdLLZ0ISbM7Y3xJ\nEVi/DolLZVQetAPMdxmjVKKUjn4V1QiGD4/yPT5j/dwckTWIkxnfQ4LDLYrPZ3nU\n2C3n0imMgFZlpiMQ7RN+3Wva1H+xG3jZyhWVaQKBgCFuQs+EllaHZYS/EVRgKqKs\n/MMrHJyAzJSc5ItUjGJVXDamjy38MKh50mQ6L1iXWmf4ilw8xdWYHhqjfVWYEKWn\nKaCKiw3wJZqpCHZC3ZP+6qAclgxczDe/AStCeYv/c7EU5P7lTLVEQf2XoETqAX6e\nB3pqwbNSZBox8qUCgY5G\n-----END PRIVATE KEY-----\n",
    "client_email": "id-6neuf@stock-ergo.iam.gserviceaccount.com",
    "client_id": "113621753371672377683",
    "auth_uri": "https://accounts.google.com",
    "token_uri": "https://oauth2.googleapis.com",
    "auth_provider_x509_cert_url": "https://www.googleapis.com",
    "client_x509_cert_url": "https://www.googleapis.com"
}

# Initialisation du client Google Sheets
try:
    spread = Spread("11P3mxax78oqjQs_J6nHTM0th-_LlnPf7A_c9rJjkKE8", config=creds)
except Exception as e:
    st.error(f"Erreur de connexion : {e}")

st.title("📦 Stock Ergo - Gestion Directe")

# Chargement des données
df_stock = spread.sheet_to_df(sheet='stock', index=0)

tab1, tab2 = st.tabs(["📋 Inventaire", "➕ Ajouter"])

with tab1:
    st.dataframe(df_stock, use_container_width=True)

with tab2:
    with st.form("add_form"):
        nom = st.text_input("Nom de l'article")
        if st.form_submit_button("Enregistrer"):
            new_row = [len(df_stock)+1, nom, "Achat", "", "Disponible"]
            spread.df_to_sheet(df_stock.append(pd.Series(new_row, index=df_stock.columns), ignore_index=True), sheet='stock', index=False)
            st.success("Ajouté !")
            st.rerun()
