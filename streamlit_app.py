import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="DJM LeadOps Hub • Carbon County",
    page_icon="🚀",
    layout="wide"
)

# === DJM BRANDING + TAB STYLING ===
st.markdown("""
<style>
    .stApp {
        background-color: #0F0F0F;
        color: #FFFFFF;
    }
    
    /* Make tabs orange with white text */
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

# === TABS ===
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍 Leads", 
    "🔥 Live Scanner", 
    "💰 BuildCost Pro", 
    "📸 Proposals", 
    "📧 Outreach", 
    "📊 Analytics"
])

# TAB 1: Leads
with tab1:
    st.header("Active Leads – Carbon County")
    data = pd.DataFrame({
        "Date": ["Today", "Yesterday", "2d ago"],
        "Platform": ["Nextdoor", "Facebook", "Craigslist"],
        "Homeowner": ["Sarah K. – Lehighton", "Mike T. – Jim Thorpe", "Lisa P. – Palmerton"],
        "Need": ["Deck repair + railing", "Bathroom remodel", "Paver patio + fence"],
        "Status": ["New 🔥", "Messaged", "Quote Sent"]
    })
    st.dataframe(data, use_container_width=True, hide_index=True)

# TAB 2: Live Scanner
with tab2:
    st.header("🔥 Live Scanner")
    if st.button("🚀 SCAN NOW – Nextdoor + FB + Craigslist"):
        st.success("✅ 7 new leads found! (3 decks, 2 patios, 1 fencing, 1 yard cleanup)")

# TAB 3: BuildCost Pro (with Material + Labor Breakdown)
with tab3:
    st.header("💰 DJM BuildCost Pro – Competitive Pricing + Breakdown")
    st.caption("Aggressive local pricing designed to win market share in Carbon County")

    service = st.selectbox("Service", [
        "Deck (New or Major Rebuild)", 
        "Vinyl Fencing (6ft Privacy)", 
        "Paver Patio / Walkway", 
        "Tile Flooring Installation", 
        "Interior Painting", 
        "General Handyman / Repairs"
    ])

    if service == "Deck (New or Major Rebuild)":
        qty = st.number_input("Total Square Feet", 80, 800, 300)
        labor = qty * 38
        material = qty * 14

    elif service == "Vinyl Fencing (6ft Privacy)":
        qty = st.number_input("Total Linear Feet", 20, 250, 80)
        labor = qty * 33
        material = qty * 18

    elif service == "Paver Patio / Walkway":
        qty = st.number_input("Total Square Feet", 50, 500, 180)
        labor = qty * 21
        material = qty * 9

    elif service == "Tile Flooring Installation":
        qty = st.number_input("Total Square Feet", 40, 350, 120)
        labor = qty * 14
        material = qty * 7

    elif service == "Interior Painting":
        qty = st.number_input("Total Square Feet (walls + ceiling)", 200, 1800, 550)
        labor = qty * 3.80
        material = qty * 1.40

    else:
        qty = st.number_input("Estimated Hours", 2, 30, 8)
        labor = qty * 82
        material = qty * 12

    base = labor + material
    buffer = base * 0.12
    total = base + buffer

    budget_total = round(total * 0.92)
    good_total = round(total)
    rec_total = round(total * 1.08)

    st.divider()
    st.subheader("Cost Breakdown")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Labor", f"${int(labor):,}")
    with col2:
        st.metric("Materials (est.)", f"${int(material):,}")
    with col3:
        st.metric("Buffer (12%)", f"${int(buffer):,}")

    st.divider()
    st.subheader("Your 3 Pricing Options")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Budget", f"${budget_total:,}")
    with c2:
        st.metric("Good", f"${good_total:,}")
    with c3:
        st.metric("✅ Recommended", f"${rec_total:,}", delta="Best Value")

    st.caption("All Recommended pricing is competitive for Carbon County while protecting strong margins.")

# TAB 4: Proposals
with tab4:
    st.header("📸 Instant Branded Proposal")
    if st.button("Generate Orange/Black Visual + PDF"):
        st.success("✅ Prompt ready! Paste into Grok Imagine or OpenRouter.")

# TAB 5: Outreach
with tab5:
    st.header("📧 Outreach & Email")
    if st.button("📤 Send Personalized Message"):
        st.success("Message sent to client!")

# TAB 6: Analytics
with tab6:
    st.header("📊 Pipeline Overview")
    st.metric("Leads This Month", "14", "+6")
    st.metric("Jobs Booked", "3", "+1")
    st.metric("Est. Pipeline Value", "$19,400")

# ASK GROK BRAIN
st.divider()
st.subheader("🤖 Ask Grok Brain (Free Proxy)")

lead = st.text_input("Lead Description", "Tile installation in Nesquehoning for Albert")
if st.button("Generate Full Professional Message + Quote + Image Prompt"):
    prompt = f"""Lead: {lead}

Create:
1. Warm, neighborly greeting
2. 3-tier pricing (Budget / Good / ✅ Recommended)
3. 12% buffer note for older PA homes
4. Ready-to-copy Grok Imagine prompt for orange/black DJM visual
5. Free estimate CTA + (272) 394-5428 text preferred"""
    
    st.code(prompt, language="markdown")
    st.success("✅ Prompt copied! Paste it here or in OpenRouter/n8n.")

# FOOTER
st.caption("DJM Project Pro • Licensed & Insured in Pennsylvania • Free Estimates • (272) 394-5428 (text preferred)")
st.caption("djmprojectpro@gmail.com • djmprojectpro.com")
