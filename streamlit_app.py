import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(
    page_title="DJM LeadOps Hub • Carbon County",
    page_icon="🚀",
    layout="wide"
)

# === DJM BRANDING + THEME ===
st.markdown("""
<style>
    .stApp { background-color: #0F0F0F; color: #FFFFFF; }
    .stTabs [data-baseweb="tab-list"] { background-color: #FF6200; border-radius: 8px 8px 0 0; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: 700; font-size: 15px; }
    .stTabs [aria-selected="true"] { background-color: #E55A00; color: white !important; border-radius: 6px; }
    .stButton>button { background-color: #FF6200; color: white; border: none; font-weight: 600; }
    .stButton>button:hover { background-color: #E55A00; }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://via.placeholder.com/200x80/FF6200/000000?text=DJM+Project+Pro", use_column_width=True)
st.sidebar.title("🚀 DJM LeadOps Hub")
st.sidebar.caption("Licensed & Insured in Pennsylvania")
st.sidebar.caption("Free Estimates • (272) 394-5428 (text preferred)")
st.sidebar.caption("djmprojectpro@gmail.com • djmprojectpro.com")

# === Google Sheets Connection ===
@st.cache_resource
def connect_to_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client

client = connect_to_sheets()
sheet = client.open("DJM LeadOps Hub - Data")

def load_data(sheet_name):
    try:
        worksheet = sheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

def save_data(sheet_name, df):
    worksheet = sheet.worksheet(sheet_name)
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

# Load data from Google Sheets
leads_df = load_data("Leads")
jobs_df = load_data("Jobs")

# === TABS ===
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📍 Leads", "🔥 Live Scanner", "💰 BuildCost Pro", "📸 Proposals",
    "📧 Outreach", "📊 Analytics", "🎨 Prompt Generator", "🛠️ Jobs", "⚙️ Settings"
])

# TAB 1: Leads
with tab1:
    st.header("📍 Leads Management")

    with st.expander("➕ Add New Lead"):
        with st.form("add_lead"):
            col1, col2 = st.columns(2)
            with col1:
                platform = st.selectbox("Platform", ["Nextdoor", "Facebook", "Craigslist", "Google", "Referral"])
                client_name = st.text_input("Client Name")
                location = st.text_input("Location")
                phone = st.text_input("Phone (optional)")
            with col2:
                need = st.text_input("What do they need?")
                status = st.selectbox("Status", ["New", "Contacted", "Quoted", "Booked", "Lost"])

            if st.form_submit_button("Add Lead"):
                new_row = pd.DataFrame([{
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Platform": platform, "Client": client_name, "Location": location,
                    "Phone": phone, "Need": need, "Status": status
                }])
                leads_df = pd.concat([leads_df, new_row], ignore_index=True)
                save_data("Leads", leads_df)
                st.success("Lead added and saved!")
                st.rerun()

    st.dataframe(leads_df, use_container_width=True, hide_index=True)

# Other tabs (simplified for stability)
with tab2: st.header("🔥 Live Scanner")
with tab3: st.header("💰 BuildCost Pro")
with tab4: st.header("📸 Proposals")
with tab5: st.header("📧 Outreach")
with tab6: st.header("📊 Analytics")
with tab7: st.header("🎨 Prompt Generator")
with tab8: st.header("🛠️ Jobs")
with tab9: st.header("⚙️ Settings")

st.divider()
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • Free Estimates • (272) 394-5428 (text preferred)")
st.caption("djmprojectpro@gmail.com • djmprojectpro.com")
