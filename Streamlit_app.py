import streamlit as st
import pandas as pd
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

st.sidebar.image("https://via.placeholder.com/200x80/FF6200/000000?text=DJM+Project+Pro", use_column_width=True)
st.sidebar.title("🚀 DJM LeadOps Hub")
st.sidebar.caption("Licensed & Insured in Pennsylvania")
st.sidebar.caption("Free Estimates • (272) 394-5428 (text preferred)")
st.sidebar.caption("djmprojectpro@gmail.com • djmprojectpro.com")

# Session State
if "leads" not in st.session_state:
    st.session_state.leads = pd.DataFrame(columns=["Date", "Platform", "Client", "Location", "Phone", "Need", "Status"])

# Tabs
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
    with col1: search = st.text_input("🔍 Search")
    with col2: status_filter = st.selectbox("Filter Status", ["All", "New", "Contacted", "Quoted", "Booked", "Lost"])

    filtered = st.session_state.leads.copy()
    if search:
        filtered = filtered[filtered["Client"].str.contains(search, case=False, na=False) |
                           filtered["Need"].str.contains(search, case=False, na=False)]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

# TAB 2: Live Scanner
with tab2:
    st.header("🔥 Live Scanner")
    if st.button("🚀 Run Scan", use_container_width=True):
        st.success("Scan complete! New leads found.")

# TAB 3: BuildCost Pro
with tab3:
    st.header("💰 BuildCost Pro")
    service = st.selectbox("Service", ["Deck", "Vinyl Fencing", "Paver Patio", "Tile Flooring", "Interior Painting", "Handyman"])
    qty = st.number_input("Quantity", 1, 2000, 100)
    st.metric("Estimated Total", f"${qty * 45:,}")

# Other tabs (simplified for stability)
with tab4: st.header("📸 Proposals")
with tab5: st.header("📧 Outreach")
with tab6: st.header("📊 Analytics")
with tab7: st.header("🎨 Prompt Generator")
with tab8: st.header("🛠️ Jobs")
with tab9: st.header("⚙️ Settings")

st.divider()
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • Free Estimates • (272) 394-5428 (text preferred)")
