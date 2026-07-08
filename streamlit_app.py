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

# === Google Sheets Connection ===
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

# Load data
leads_df = load_sheet("Leads")
jobs_df = load_sheet("Jobs")

# === Persistent Settings with Auto Sync ===
def get_settings():
    if "settings" not in st.session_state:
        settings_df = load_sheet("Settings")
        defaults = {
            "labor_deck": 38,
            "labor_fence": 33,
            "labor_paver": 21,
            "labor_tile": 14,
            "labor_paint": 3.8,
            "buffer": 0.12
        }
        if not settings_df.empty:
            for _, row in settings_df.iterrows():
                try:
                    defaults[row["Setting"]] = float(row["Value"])
                except:
                    pass
        st.session_state.settings = defaults
    return st.session_state.settings

settings = get_settings()

def save_settings(new_settings):
    df = pd.DataFrame([{"Setting": k, "Value": v} for k, v in new_settings.items()])
    save_sheet("Settings", df)
    st.session_state.settings = new_settings  # Update immediately
    st.rerun()  # Auto sync across tabs

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

# TAB 3: BuildCost Pro (Uses live settings)
with tab3:
    st.header("💰 BuildCost Pro")
    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting"], key="buildcost_service")
    qty = st.number_input("Quantity", 10, 2000, 200, key="buildcost_qty")
    
    # Always use latest settings
    current_settings = get_settings()
    rates = {
        "Deck": current_settings["labor_deck"],
        "Vinyl Fencing": current_settings["labor_fence"],
        "Paver Patio": current_settings["labor_paver"],
        "Tile Flooring": current_settings["labor_tile"],
        "Interior Painting": current_settings["labor_paint"]
    }
    labor = qty * rates.get(service, 30)
    material = qty * 12
    buffer = (labor + material) * current_settings["buffer"]
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
        buffer_pdf = BytesIO()
        doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("DJM PROJECT PRO - QUOTE", styles['Title'])]
        story.append(Paragraph(f"Service: {service} | Recommended Total: ${int(total*1.08):,}", styles['Normal']))
        doc.build(story)
        buffer_pdf.seek(0)
        st.download_button("Download PDF", buffer_pdf, "DJM_Quote.pdf", mime="application/pdf", key="buildcost_download")

# TAB 5: Outreach
with tab5:
    st.header("📧 Outreach")
    if not leads_df.empty:
        selected_client = st.selectbox("Select Lead", leads_df["Client"], key="outreach_client")
        template = st.selectbox("Template", ["New Lead Follow-up", "Quote Sent", "Booking Confirmation", "Custom"], key="outreach_template")
        default_msg = f"Hi {selected_client}, thank you for reaching out regarding your project."
        message = st.text_area("Message", default_msg, key="outreach_message")

        if st.button("📧 Send Email & Log", use_container_width=True, key="outreach_send"):
            try:
                sender_email = st.secrets["email"]["sender_email"]
                app_password = st.secrets["email"]["app_password"]
                receiver_email = "djmprojectpro@gmail.com"

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = f"DJM Project Pro - {template}"
                msg.attach(MIMEText(message, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                server.quit()

                st.success(f"Email sent to {selected_client}!")
                log_activity(selected_client, message, "Email")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
    else:
        st.info("Add leads first.")

# TAB 6: Analytics
with tab6:
    st.header("📊 Analytics")
    total_leads = len(leads_df)
    booked = len(leads_df[leads_df["Status"] == "Booked"]) if not leads_df.empty else 0
    conversion = round((booked / total_leads * 100), 1) if total_leads > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total Leads", total_leads)
    with col2: st.metric("Jobs Booked", booked)
    with col3: st.metric("Conversion Rate", f"{conversion}%")

    if not leads_df.empty:
        st.subheader("Leads by Status")
        st.bar_chart(leads_df["Status"].value_counts())

# TAB 7: Prompt Generator
with tab7:
    st.header("🎨 Prompt Generator")
    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting"], key="prompt_service")
    client_name = st.text_input("Client Name", key="prompt_client")
    location = st.text_input("Location", key="prompt_location")
    size = st.text_input("Size / Quantity", key="prompt_size")
    budget = st.text_input("Budget Price", key="prompt_budget")
    good = st.text_input("Good Price", key="prompt_good")
    recommended = st.text_input("Recommended Price", key="prompt_recommended")

    if st.button("🚀 Generate Prompt & PDF", use_container_width=True, key="prompt_generate"):
        prompt = f"""Professional {service} quote graphic for DJM Project Pro.
Glowing orange circular logo on charcoal black background.

Job details:
- Client: {client_name}
- Location: {location}
- Size: {size}
- Pricing:
  - Budget: {budget}
  - Good: {good}
  - ✅ Recommended: {recommended}

Clean, trustworthy contractor style. Include (272) 394-5428."""

        st.code(prompt, language="markdown")

        buffer_pdf = BytesIO()
        doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("DJM PROJECT PRO - QUOTE", styles['Title'])]
        story.append(Paragraph(f"Service: {service} | Client: {client_name}", styles['Normal']))
        story.append(Paragraph(f"Recommended Total: {recommended}", styles['Normal']))
        doc.build(story)
        buffer_pdf.seek(0)
        st.download_button("📥 Download PDF Quote", buffer_pdf, "DJM_Quote.pdf", mime="application/pdf", key="prompt_download")

# TAB 8: Jobs
with tab8:
    st.header("🛠️ Jobs / Active Projects")
    st.dataframe(jobs_df, use_container_width=True, hide_index=True)

    if st.button("🔄 Move Booked Leads to Jobs", key="jobs_move"):
        booked = leads_df[leads_df["Status"] == "Booked"]
        for _, row in booked.iterrows():
            new_job = pd.DataFrame([{
                "Job ID": f"JOB-{datetime.now().strftime('%Y%m%d%H%M')}",
                "Client": row["Client"],
                "Service": row["Need"],
                "Location": row["Location"],
                "Value": 0,
                "Status": "Scheduled",
                "Date Booked": datetime.now().strftime("%Y-%m-%d")
            }])
            jobs_df = pd.concat([jobs_df, new_job], ignore_index=True)
        save_sheet("Jobs", jobs_df)
        st.success(f"Moved {len(booked)} leads to Jobs!")
        st.rerun()

# TAB 9: Settings (Auto Sync)
with tab9:
    st.header("⚙️ Settings")
    st.subheader("Labor Rates (per unit)")

    deck = st.number_input("Deck Rate", value=settings["labor_deck"], key="set_deck")
    fence = st.number_input("Vinyl Fencing Rate", value=settings["labor_fence"], key="set_fence")
    paver = st.number_input("Paver Patio Rate", value=settings["labor_paver"], key="set_paver")
    tile = st.number_input("Tile Flooring Rate", value=settings["labor_tile"], key="set_tile")
    paint = st.number_input("Interior Painting Rate", value=settings["labor_paint"], key="set_paint")
    buf = st.slider("Buffer %", 5, 20, int(settings["buffer"] * 100), key="set_buffer")

    if st.button("💾 Save Settings", key="settings_save"):
        new_settings = {
            "labor_deck": deck,
            "labor_fence": fence,
            "labor_paver": paver,
            "labor_tile": tile,
            "labor_paint": paint,
            "buffer": buf / 100
        }
        save_settings(new_settings)  # Auto sync + rerun

# Footer
st.divider()
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • (272) 394-5428")
