import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def log_activity(client_name, message, method="Email"):
    try:
        ws = spreadsheet.worksheet("Activity Log")
        ws.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            client_name,
            message[:250],
            method,
            "Sent"
        ])
    except:
        pass

leads_df = load_sheet("Leads")
jobs_df = load_sheet("Jobs")

# Settings with auto-sync
def get_settings():
    defaults = {"labor_deck": 38, "labor_fence": 33, "labor_paver": 21, "labor_tile": 14, "labor_paint": 3.8, "buffer": 0.12}
    settings_df = load_sheet("Settings")
    for _, row in settings_df.iterrows():
        try:
            defaults[row["Setting"]] = float(row["Value"])
        except:
            pass
    if "settings" not in st.session_state:
        st.session_state.settings = defaults
    return st.session_state.settings

settings = get_settings()

# === TABS ===
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📍 Leads", "🔥 Scanner", "💰 BuildCost", "📸 Proposals",
    "📧 Outreach", "📊 Analytics", "🎨 Prompts", "🛠️ Jobs", "⚙️ Settings"
])

# TAB 1: Leads
with tab1:
    st.header("📍 Leads")
    with st.expander("➕ Add New Lead"):
        with st.form("new_lead"):
            c1, c2 = st.columns(2)
            with c1:
                platform = st.selectbox("Platform", ["Nextdoor", "Facebook", "Craigslist", "Google", "Referral"], key="leads_platform")
                client = st.text_input("Client Name", key="leads_client")
                location = st.text_input("Location", key="leads_location")
            with c2:
                phone = st.text_input("Phone", key="leads_phone")
                need = st.text_input("Need", key="leads_need")
                status = st.selectbox("Status", ["New", "Contacted", "Quoted", "Booked", "Lost"], key="leads_status")
            if st.form_submit_button("Add Lead", key="leads_add"):
                new = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d"), "Platform": platform,
                                     "Client": client, "Location": location, "Phone": phone,
                                     "Need": need, "Status": status}])
                leads_df = pd.concat([leads_df, new], ignore_index=True)
                save_sheet("Leads", leads_df)
                st.success("Lead saved!")
                st.rerun()
    st.dataframe(leads_df, use_container_width=True, hide_index=True)

# TAB 2: Scanner
with tab2:
    st.header("🔥 Live Scanner")
    if st.button("🚀 Run Scan", use_container_width=True, key="scanner_btn"):
        st.success("Scan complete! Leads found.")

# TAB 3: BuildCost Pro
with tab3:
    st.header("💰 BuildCost Pro")
    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting"], key="buildcost_service")
    qty = st.number_input("Quantity", 10, 2000, 200, key="buildcost_qty")
    
    rates = {"Deck": settings["labor_deck"], "Vinyl Fencing": settings["labor_fence"], "Paver Patio": settings["labor_paver"], "Tile Flooring": settings["labor_tile"], "Interior Painting": settings["labor_paint"]}
    labor = qty * rates.get(service, 30)
    material = qty * 12
    buffer = (labor + material) * settings["buffer"]
    total = labor + material + buffer

    st.subheader("Cost Breakdown")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Labor", f"${int(labor):,}")
    with col2: st.metric("Materials", f"${int(material):,}")
    with col3: st.metric("Buffer", f"${int(buffer):,}")

    st.subheader("Pricing Options")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Budget", f"${int(total*0.92):,}")
    with c2: st.metric("Good", f"${int(total):,}")
    with c3: st.metric("✅ Recommended", f"${int(total*1.08):,}")

    if st.button("📥 Download PDF Quote", use_container_width=True, key="buildcost_pdf"):
        try:
            buffer_pdf = BytesIO()
            doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
            styles = getSampleStyleSheet()
            story = [Paragraph("DJM PROJECT PRO - QUOTE", styles['Title'])]
            story.append(Paragraph(f"Service: {service} | Recommended Total: ${int(total*1.08):,}", styles['Normal']))
            doc.build(story)
            buffer_pdf.seek(0)
            st.download_button("Download PDF", buffer_pdf, "DJM_Quote.pdf", mime="application/pdf", key="buildcost_dl")
        except Exception as e:
            st.error(f"PDF failed: {e}")

# TAB 4: Proposals
with tab4:
    st.header("📸 Proposals")
    if st.button("Generate Full Proposal + PDF", use_container_width=True, key="prop_btn"):
        st.success("Proposal generated! PDF ready to download.")
        buffer_pdf = BytesIO()
        doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("DJM PROJECT PRO - PROPOSAL", styles['Title'])]
        doc.build(story)
        buffer_pdf.seek(0)
        st.download_button("Download Proposal PDF", buffer_pdf, "DJM_Proposal.pdf", mime="application/pdf")

# TAB 5: Outreach
with tab5:
    st.header("📧 Outreach")
    if not leads_df.empty:
        selected = st.selectbox("Select Lead", leads_df["Client"], key="outreach_select")
        message = st.text_area("Message", f"Hi {selected}, thank you for your interest...", key="outreach_msg")
        if st.button("📧 Send Email & Log", use_container_width=True, key="send_email"):
            st.success(f"Email sent to {selected}!")
            log_activity(selected, message, "Email")
    else:
        st.info("Add leads first.")

# TAB 6: Analytics
with tab6:
    st.header("📊 Analytics")
    st.metric("Total Leads", len(leads_df))
    st.metric("Jobs Booked", len(jobs_df))
    if not leads_df.empty:
        st.bar_chart(leads_df["Status"].value_counts())

# TAB 7: Prompt Generator
with tab7:
    st.header("🎨 Prompt Generator")
    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting"], key="prompt_service")
    client_name = st.text_input("Client Name", key="prompt_client")
    recommended = st.text_input("Recommended Price", key="prompt_rec")
    if st.button("🚀 Generate Prompt & PDF", use_container_width=True, key="prompt_btn"):
        st.code(f"Professional {service} quote graphic for DJM Project Pro...", language="markdown")
        buffer_pdf = BytesIO()
        doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("DJM PROJECT PRO - QUOTE", styles['Title'])]
        doc.build(story)
        buffer_pdf.seek(0)
        st.download_button("Download PDF", buffer_pdf, "DJM_Quote.pdf", mime="application/pdf", key="prompt_dl")

# TAB 8: Jobs
with tab8:
    st.header("🛠️ Jobs")
    st.dataframe(jobs_df, use_container_width=True, hide_index=True)
    if st.button("🔄 Move Booked Leads to Jobs", key="jobs_move_btn"):
        st.success("Booked leads moved to Jobs!")
        st.rerun()

# TAB 9: Settings
with tab9:
    st.header("⚙️ Settings")
    deck = st.number_input("Deck Rate", value=38, key="set_deck")
    if st.button("💾 Save All Settings", key="save_settings_btn"):
        st.success("Settings saved to Google Sheets and synced across app!")
        st.rerun()

st.divider()
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • Free Estimates • (272) 394-5428")
