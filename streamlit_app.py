import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="DJM LeadOps Hub", page_icon="🚀", layout="wide")

# === THEME ===
st.markdown("""
<style>
    .stApp { background-color: #0F0F0F; color: #FFFFFF; }
    .stTabs [data-baseweb="tab-list"] { background-color: #FF6200; border-radius: 8px 8px 0 0; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: 700; }
    .stTabs [aria-selected="true"] { background-color: #E55A00; }
    .stButton>button { background-color: #FF6200; color: white; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://via.placeholder.com/200x80/FF6200/000000?text=DJM+Project+Pro", use_column_width=True)
st.sidebar.title("🚀 DJM LeadOps Hub")
st.sidebar.caption("Licensed & Insured in Pennsylvania • (272) 394-5428")

# === Google Sheets ===
SPREADSHEET_ID = "1pt5FX6y2lVXVcgqKaA-d6zlW37eZQXLz0DPslSRCCOY"

@st.cache_resource
def get_client():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    return gspread.authorize(creds)

client = get_client()
spreadsheet = client.open_by_key(SPREADSHEET_ID)

def load_sheet(name):
    try:
        return pd.DataFrame(spreadsheet.worksheet(name).get_all_records())
    except:
        return pd.DataFrame()

def save_sheet(name, df):
    try:
        ws = spreadsheet.worksheet(name)
        ws.clear()
        if not df.empty:
            ws.update([df.columns.tolist()] + df.values.tolist())
    except Exception as e:
        st.error(f"Error saving {name}: {e}")

leads_df = load_sheet("Leads")
jobs_df = load_sheet("Jobs")

# === TABS ===
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📍 Leads", "🔥 Scanner", "💰 BuildCost", "📸 Proposals",
    "📧 Outreach", "📊 Analytics", "🎨 Prompts", "🛠️ Jobs", "⚙️ Settings"
])

# TAB 1: Leads (with Migration Logic)
with tab1:
    st.header("📍 Leads")

    with st.expander("➕ Add New Lead"):
        with st.form("new_lead"):
            c1, c2 = st.columns(2)
            with c1:
                platform = st.selectbox("Platform", ["Nextdoor", "Facebook", "Craigslist", "Google", "Referral"])
                client = st.text_input("Client Name")
                location = st.text_input("Location")
            with c2:
                phone = st.text_input("Phone")
                need = st.text_input("Need")
                status = st.selectbox("Status", ["New", "Contacted", "Quoted", "Booked", "Lost"])
            if st.form_submit_button("Add Lead"):
                new = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d"), "Platform": platform,
                                     "Client": client, "Location": location, "Phone": phone,
                                     "Need": need, "Status": status}])
                leads_df = pd.concat([leads_df, new], ignore_index=True)
                save_sheet("Leads", leads_df)
                st.success("Lead added!")
                st.rerun()

    st.dataframe(leads_df, use_container_width=True, hide_index=True)

    # === Lead to Job Migration ===
    st.subheader("🔄 Convert Booked Lead to Job")
    booked_leads = leads_df[leads_df["Status"] == "Booked"]

    if not booked_leads.empty:
        selected_idx = st.selectbox("Select Booked Lead to Convert", booked_leads.index)
        selected_lead = booked_leads.loc[selected_idx]

        with st.form("convert_to_job"):
            service = st.selectbox("Service Type", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting"])
            value = st.number_input("Estimated Job Value ($)", min_value=0, value=5000)
            notes = st.text_area("Notes (optional)")

            if st.form_submit_button("Convert to Job"):
                # Create new job
                new_job = pd.DataFrame([{
                    "Job ID": f"JOB-{datetime.now().strftime('%Y%m%d%H%M')}",
                    "Client": selected_lead["Client"],
                    "Service": service,
                    "Location": selected_lead["Location"],
                    "Value": value,
                    "Status": "Scheduled",
                    "Date Booked": datetime.now().strftime("%Y-%m-%d"),
                    "Notes": notes
                }])
                jobs_df = pd.concat([jobs_df, new_job], ignore_index=True)
                save_sheet("Jobs", jobs_df)

                # Update lead status
                leads_df.loc[selected_idx, "Status"] = "Converted to Job"
                save_sheet("Leads", leads_df)

                st.success(f"Lead for {selected_lead['Client']} converted to Job!")
                st.rerun()
    else:
        st.info("No booked leads available to convert.")

# TAB 8: Jobs (Improved)
with tab8:
    st.header("🛠️ Jobs / Active Projects")
    st.dataframe(jobs_df, use_container_width=True, hide_index=True)

# Other tabs
with tab2: st.header("🔥 Live Scanner")
with tab3: st.header("💰 BuildCost")
with tab4: st.header("📸 Proposals")
with tab5: st.header("📧 Outreach")
with tab6: st.header("📊 Analytics")
with tab7: st.header("🎨 Prompt Generator")
with tab9: st.header("⚙️ Settings")

st.divider()
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • (272) 394-5428")
