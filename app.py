import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="DJM LeadOps Hub • Carbon County",
    page_icon="🚀",
    layout="wide"
)

# === DJM BRANDING + THEME ===
st.markdown("""
<style>
    .stApp {
        background-color: #0F0F0F;
        color: #FFFFFF;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FF6200;
        border-radius: 8px 8px 0 0;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: 700;
        font-size: 15px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E55A00;
        color: white !important;
        border-radius: 6px;
    }
    .stButton>button {
        background-color: #FF6200;
        color: white;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #E55A00;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://via.placeholder.com/200x80/FF6200/000000?text=DJM+Project+Pro", use_column_width=True)
st.sidebar.title("🚀 DJM LeadOps Hub")
st.sidebar.caption("Licensed & Insured in Pennsylvania")
st.sidebar.caption("Free Estimates • (272) 394-5428 (text preferred)")
st.sidebar.caption("djmprojectpro@gmail.com • djmprojectpro.com")

# Session State Initialization
if "leads" not in st.session_state:
    st.session_state.leads = pd.DataFrame(columns=["Date", "Platform", "Client", "Location", "Phone", "Need", "Status"])

if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame(columns=["Job ID", "Client", "Service", "Location", "Value", "Status", "Date Booked"])

if "settings" not in st.session_state:
    st.session_state.settings = {
        "labor_deck": 38, "labor_fence": 33, "labor_paver": 21,
        "labor_tile": 14, "labor_paint": 3.80, "labor_handyman": 82,
        "buffer": 0.12
    }

# === TABS ===
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📍 Leads", "🔥 Live Scanner", "💰 BuildCost Pro", "📸 Proposals",
    "📧 Outreach", "📊 Analytics", "🎨 Prompt Generator", "🛠️ Jobs", "⚙️ Settings"
])

# ===================== TAB 1: LEADS =====================
with tab1:
    st.header("📍 Leads Management")

    with st.expander("➕ Add New Lead"):
        with st.form("add_lead_form"):
            col1, col2 = st.columns(2)
            with col1:
                platform = st.selectbox("Platform", ["Nextdoor", "Facebook", "Craigslist", "Google", "Referral"])
                client = st.text_input("Client Name")
                location = st.text_input("Location")
                phone = st.text_input("Phone (optional)")
            with col2:
                need = st.text_input("What do they need?")
                status = st.selectbox("Status", ["New", "Contacted", "Quoted", "Booked", "Lost"])

            if st.form_submit_button("Add Lead"):
                new_row = pd.DataFrame([{
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Platform": platform, "Client": client, "Location": location,
                    "Phone": phone, "Need": need, "Status": status
                }])
                st.session_state.leads = pd.concat([st.session_state.leads, new_row], ignore_index=True)
                st.success("Lead added!")
                st.rerun()

    # Search & Filter
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Search")
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "New", "Contacted", "Quoted", "Booked", "Lost"])

    filtered = st.session_state.leads.copy()
    if search:
        filtered = filtered[filtered["Client"].str.contains(search, case=False, na=False) |
                           filtered["Need"].str.contains(search, case=False, na=False)]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    if not filtered.empty:
        st.subheader("Quick Actions")
        idx = st.selectbox("Select Lead", filtered.index)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💰 Send to BuildCost"): st.info("Sent to BuildCost Pro")
        with col2:
            if st.button("🎨 Generate Prompt"): st.info("Prompt generated")
        with col3:
            if st.button("✅ Mark as Booked"):
                st.session_state.leads.loc[idx, "Status"] = "Booked"
                st.success("Marked as Booked!")
                st.rerun()

# ===================== TAB 2: LIVE SCANNER =====================
with tab2:
    st.header("🔥 Live Scanner")
    st.info("Scan social platforms for new leads (simulated for now)")

    if st.button("🚀 Run Scan", use_container_width=True):
        st.success("Scan complete! New leads found.")

# ===================== TAB 3: BUILDCOST PRO =====================
with tab3:
    st.header("💰 BuildCost Pro")

    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting", "Handyman"])
    qty = st.number_input("Quantity", 1, 2000, 100)

    labor_rate = st.session_state.settings.get(f"labor_{service.lower().replace(' ', '_')}", 30)
    labor = qty * labor_rate
    material = qty * 10
    buffer = (labor + material) * st.session_state.settings["buffer"]
    total = labor + material + buffer

    budget = round(total * 0.92)
    good = round(total)
    recommended = round(total * 1.08)

    st.subheader("Cost Breakdown")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Labor", f"${int(labor):,}")
    with col2: st.metric("Materials", f"${int(material):,}")
    with col3: st.metric("Buffer", f"${int(buffer):,}")

    st.subheader("Pricing")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Budget", f"${budget:,}")
    with c2: st.metric("Good", f"${good:,}")
    with c3: st.metric("✅ Recommended", f"${recommended:,}")

    if st.button("📥 Download PDF Quote", use_container_width=True):
        buffer_pdf = BytesIO()
        doc = SimpleDocTemplate(buffer_pdf, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph("DJM PROJECT PRO - QUOTE", styles['Title'])]
        story.append(Paragraph(f"Service: {service} | Total: ${recommended:,}", styles['Normal']))
        doc.build(story)
        buffer_pdf.seek(0)
        st.download_button("Download PDF", buffer_pdf, "DJM_Quote.pdf", mime="application/pdf")

# ===================== TAB 4-9 (Core Structure) =====================
with tab4:
    st.header("📸 Proposals")
    st.info("Create professional proposals here.")

with tab5:
    st.header("📧 Outreach")
    st.info("Communicate with leads (Email/SMS coming soon).")

with tab6:
    st.header("📊 Analytics")
    st.metric("Leads This Month", len(st.session_state.leads))
    st.metric("Jobs Booked", len(st.session_state.jobs))

with tab7:
    st.header("🎨 Prompt Generator")
    st.info("Generate branded quote images and PDFs.")

with tab8:
    st.header("🛠️ Jobs / Active Projects")
    st.info("Manage booked jobs and track progress.")

with tab9:
    st.header("⚙️ Settings")
    st.session_state.settings["labor_deck"] = st.number_input("Deck Labor Rate", value=st.session_state.settings["labor_deck"])
    st.session_state.settings["buffer"] = st.slider("Buffer %", 0.05, 0.20, st.session_state.settings["buffer"], 0.01)
    if st.button("Save Settings"):
        st.success("Settings saved!")

# Footer
st.divider()
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • Free Estimates • (272) 394-5428 (text preferred)")
st.caption("djmprojectpro@gmail.com • djmprojectpro.com")
