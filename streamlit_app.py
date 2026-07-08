import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

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

# TAB 1: Leads
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
                st.success("Lead added and saved!")
                st.rerun()
    st.dataframe(leads_df, use_container_width=True, hide_index=True)

# TAB 3: BuildCost Pro (Advanced)
with tab3:
    st.header("💰 BuildCost Pro")
    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting"])
    qty = st.number_input("Quantity", 10, 2000, 200)
    
    rates = {"Deck": 38, "Vinyl Fencing": 33, "Paver Patio": 21, "Tile Flooring": 14, "Interior Painting": 3.8}
    labor = qty * rates.get(service, 30)
    material = qty * 12
    buffer = (labor + material) * 0.12
    total = labor + material + buffer

    st.subheader("Cost Breakdown")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Labor", f"${int(labor):,}")
    with col2: st.metric("Materials", f"${int(material):,}")
    with col3: st.metric("Buffer (12%)", f"${int(buffer):,}")

    st.subheader("Pricing Options")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Budget", f"${int(total*0.92):,}")
    with c2: st.metric("Good", f"${int(total):,}")
    with c3: st.metric("✅ Recommended", f"${int(total*1.08):,}")

    if st.button("📥 Download PDF Quote", use_container_width=True):
        buffer_pdf = BytesIO()
        doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("DJM PROJECT PRO - QUOTE", styles['Title'])]
        story.append(Paragraph(f"Service: {service} | Recommended Total: ${int(total*1.08):,}", styles['Normal']))
        doc.build(story)
        buffer_pdf.seek(0)
        st.download_button("Download PDF", buffer_pdf, "DJM_Quote.pdf", mime="application/pdf")

# TAB 7: Prompt Generator (Advanced)
with tab7:
    st.header("🎨 Prompt Generator")
    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting"])
    client_name = st.text_input("Client Name")
    location = st.text_input("Location")
    size = st.text_input("Size / Quantity")
    budget = st.text_input("Budget Price")
    good = st.text_input("Good Price")
    recommended = st.text_input("Recommended Price")

    if st.button("🚀 Generate Prompt & PDF", use_container_width=True):
        prompt = f"""Professional {service} quote graphic for DJM Project Pro. 
Glowing orange circular logo on charcoal black background, clean modern contractor style.

Job details:
- Client: {client_name}
- Location: {location}
- Size: {size}
- Pricing:
  - Budget: {budget}
  - Good: {good}
  - ✅ Recommended: {recommended}

Clean, trustworthy, high-end contractor feel. Include free estimate CTA and (272) 394-5428."""

        st.code(prompt, language="markdown")

        # Generate PDF
        buffer_pdf = BytesIO()
        doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("DJM PROJECT PRO - QUOTE", styles['Title'])]
        story.append(Paragraph(f"Service: {service} | Client: {client_name}", styles['Normal']))
        story.append(Paragraph(f"Recommended Total: {recommended}", styles['Normal']))
        doc.build(story)
        buffer_pdf.seek(0)
        st.download_button("📥 Download PDF Quote", buffer_pdf, "DJM_Quote.pdf", mime="application/pdf")

# TAB 8: Jobs (Improved)
with tab8:
    st.header("🛠️ Jobs / Active Projects")
    st.dataframe(jobs_df, use_container_width=True, hide_index=True)
    if st.button("🔄 Refresh Jobs from Leads (Booked)"):
        booked = leads_df[leads_df["Status"] == "Booked"]
        st.info(f"Found {len(booked)} booked leads. (Feature under development)")

# Other tabs
with tab2: st.header("🔥 Live Scanner")
with tab4: st.header("📸 Proposals")
with tab5: st.header("📧 Outreach")
with tab6: st.header("📊 Analytics")
with tab9: st.header("⚙️ Settings")

st.divider()
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • (272) 394-5428")
