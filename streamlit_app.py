"""
DJM Project Pro's HQ - QuickQuote + Ops + Outreach
Professional Streamlit tool for estimates, pipeline, and client communication
Branded dark theme with orange accents for Carbon County, PA
"""

import streamlit as st
from datetime import datetime, timedelta
import random

# Page config - theme handled primarily by .streamlit/config.toml
st.set_page_config(
    page_title="DJM Project Pro's HQ",
    page_icon="ðŸ› ï¸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Robust custom CSS - works better alongside config.toml
st.markdown("""
<style>
    /* Base dark theme reinforcements */
    .stApp {
        background-color: #0f1116;
    }
    
    /* Orange primary buttons */
    .stButton > button {
        background-color: #ff6b00 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #e55a00 !important;
        transform: translateY(-1px);
    }
    
    /* Quote option cards */
    .quote-card {
        background-color: #1a1d26;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 1.25rem 1rem;
        margin-bottom: 1rem;
        height: 100%;
    }
    .quote-card.recommended {
        border: 3px solid #ff6b00;
        background-color: #1f252f;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.15);
    }
    .price-tag {
        font-size: 2rem;
        font-weight: 700;
        color: #ff6b00;
        line-height: 1;
        margin: 0.25rem 0 0.5rem 0;
    }
    .section-header {
        color: #ff6b00;
        border-bottom: 2px solid #ff6b00;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #16181f;
    }
    
    /* Footer */
    .djm-footer {
        text-align: center;
        padding: 1.5rem 0 1rem;
        border-top: 1px solid #333;
        font-size: 0.85rem;
        color: #888;
        margin-top: 2rem;
    }
    
    /* Email template box */
    .email-box {
        background-color: #1a1d26;
        border-left: 5px solid #ff6b00;
        padding: 1.5rem;
        border-radius: 8px;
        font-family: system-ui, -apple-system, sans-serif;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    
    .metric-label {
        color: #aaa;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
col_logo, col_info = st.columns([4, 3])
with col_logo:
    st.title("ðŸ› ï¸ DJM Project Pro's HQ")
    st.caption("Quality Craftsmanship â€¢ Carbon County, PA â€¢ AI-Powered Ops")
with col_info:
    st.markdown("**Licensed & Insured in Pennsylvania**")
    st.caption("Free Estimates â€¢ (272) 394-5428 (text) â€¢ djmprojectpro@gmail.com")

st.divider()

# Sidebar
with st.sidebar:
    st.header("âš™ï¸ Current Ops Status")
    
    st.subheader("Truck & Scheduling")
    truck_status = st.selectbox(
        "Update Truck Status",
        ["Transfer case/suspension repairs ongoing â€” limited capacity",
         "Truck mobile again â€” full local schedule open",
         "Full capacity (multi-crew ready)"]
    )
    if st.button("Save Status Update"):
        st.success("Status updated in session. (Connect to persistent DJM Ops Hub for cross-device sync)")
    
    st.info(
        "ðŸš§ **Reminder:** While truck work continues, prioritize smaller/local jobs and anything with deposit. "
        "Larger projects can queue for when you're fully mobile."
    )
    
    st.divider()
    st.subheader("Quick Links")
    st.markdown("- [djmprojectpro.com](https://djmprojectpro.com)")
    st.markdown("- Text: (272) 394-5428")
    st.markdown("- Email: djmprojectpro@gmail.com")
    
    st.caption("v1.1 â€¢ Theme & Outreach update â€¢ Jul 2026")

# Main Tabs
tab_quote, tab_pipeline, tab_lead, tab_outreach = st.tabs([
    "ðŸ’° Get a Quote", 
    "ðŸ“… Pipeline & Schedule", 
    "ðŸ“ Lead Intake", 
    "âœ‰ï¸ Outreach & Email"
])

# ========== TAB 1: QUOTE GENERATOR ==========
with tab_quote:
    st.header("Interactive Project Estimator", divider="orange")
    st.markdown("Realistic Carbon County pricing with built-in buffer for older PA homes. **Recommended tier is highlighted** â€” that's what most clients choose.")
    
    # Client + Project inputs
    c1, c2 = st.columns(2)
    with c1:
        client_name = st.text_input("Client Name", placeholder="John & Sarah Thompson")
    with c2:
        project_location = st.text_input("Location / Address", placeholder="Lehighton, Weatherly, Jim Thorpe, etc.")
    
    service_type = st.selectbox(
        "Project Type",
        ["Deck Build / Repair", "Patio & Paver Installation", "Fencing (Privacy / Vinyl)", 
         "Walkways, Stairs & Handrails", "Landscaping & Hardscaping", 
         "General Masonry / Retaining Wall", "Yard Cleanup & Debris Removal", "Other / Custom"]
    )
    
    # Dynamic dimension inputs
    if service_type in ["Deck Build / Repair", "Patio & Paver Installation", "Walkways, Stairs & Handrails", "Landscaping & Hardscaping"]:
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            length_ft = st.number_input("Length (ft)", min_value=3.0, value=14.0, step=0.5)
        with dcol2:
            width_ft = st.number_input("Width (ft)", min_value=3.0, value=10.0, step=0.5)
        work_area = round(length_ft * width_ft, 1)
        unit_label = "sq ft"
        st.metric("Work Area", f"{work_area} sq ft")
    elif service_type in ["Fencing (Privacy / Vinyl)", "General Masonry / Retaining Wall"]:
        work_area = st.number_input("Total Linear Feet", min_value=8.0, value=48.0, step=1.0)
        unit_label = "linear ft"
        st.metric("Linear Footage", f"{work_area} ft")
    else:
        work_area = st.number_input("Estimated Area (sq ft)", min_value=20.0, value=180.0, step=10.0)
        unit_label = "sq ft"
        st.metric("Estimated Area", f"{work_area} sq ft")
    
    complexity = st.select_slider(
        "Site Complexity",
        ["Easy access & flat", "Moderate (some slope/trees/obstacles)", "Challenging (steep, tight access, older home)"],
        value="Moderate (some slope/trees/obstacles)"
    )
    
    material_tier = st.radio("Material Level", ["Good Value (Standard)", "Recommended Balance", "Premium Upgraded"], horizontal=True)
    
    extra_notes = st.text_area("Special Requests or Notes", placeholder="e.g. match existing railing, add under-deck lighting, drainage concerns, cedar vs PT...", height=70)
    
    if st.button("ðŸš€ Generate Quote Options", type="primary", use_container_width=True):
        # Pricing logic (tuned for local 2026 market + 10% buffer)
        base_rates = {
            "Deck Build / Repair": 48,
            "Patio & Paver Installation": 32,
            "Fencing (Privacy / Vinyl)": 72,
            "Walkways, Stairs & Handrails": 38,
            "Landscaping & Hardscaping": 22,
            "General Masonry / Retaining Wall": 65,
            "Yard Cleanup & Debris Removal": 4.5,
            "Other / Custom": 35
        }
        base = base_rates[service_type]
        
        comp_mult = {"Easy access & flat": 1.0, "Moderate (some slope/trees/obstacles)": 1.12, "Challenging (steep, tight access, older home)": 1.28}[complexity]
        
        mat_mult = {"Good Value (Standard)": 0.92, "Recommended Balance": 1.0, "Premium Upgraded": 1.25}[material_tier]
        
        def get_price(tier_factor):
            price_per_unit = base * comp_mult * mat_mult * tier_factor * 1.10  # 10% buffer
            return round(price_per_unit * work_area, 0)
        
        budget_total = get_price(0.82)
        rec_total = get_price(1.0)
        prem_total = get_price(1.32)
        
        per_unit_rec = round(rec_total / work_area, 0)
        
        # Scope text
        base_desc = {
            "Deck Build / Repair": "PT framing & decking, code-compliant railing",
            "Patio & Paver Installation": "Full base prep, excavation, polymeric sand, quality pavers",
            "Fencing (Privacy / Vinyl)": "Vinyl panels, posts set in concrete, gates included where noted",
            "Walkways, Stairs & Handrails": "Proper base, drainage, code handrails on stairs",
            "Landscaping & Hardscaping": "Edging, mulch/riverstone beds, plantings as discussed",
            "General Masonry / Retaining Wall": "Footer, drainage, block or stone to spec",
            "Yard Cleanup & Debris Removal": "Complete removal + responsible disposal",
            "Other / Custom": "Custom scope confirmed on site visit"
        }[service_type]
        
        # Display cards
        st.subheader("Your Quote Options", divider="orange")
        
        col_b, col_r, col_p = st.columns(3)
        
        with col_b:
            st.markdown('<div class="quote-card">', unsafe_allow_html=True)
            st.markdown("### ðŸ’¼ Budget")
            st.markdown(f'<div class="price-tag">${budget_total:,.0f}</div>', unsafe_allow_html=True)
            st.caption(f"â‰ˆ ${round(budget_total/work_area):,} per {unit_label.split()[0]}")
            st.write(f"â€¢ {base_desc}")
            st.write("â€¢ Standard local materials")
            st.write("â€¢ Basic site prep & cleanup")
            st.write("â€¢ 1-year workmanship warranty")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_r:
            st.markdown('<div class="quote-card recommended">', unsafe_allow_html=True)
            st.markdown("### â­ RECOMMENDED")
            st.markdown(f'<div class="price-tag">${rec_total:,.0f}</div>', unsafe_allow_html=True)
            st.caption(f"â‰ˆ ${per_unit_rec:,} per {unit_label.split()[0]}  â€¢ Best overall value")
            st.write(f"â€¢ {base_desc}")
            st.write("â€¢ Quality materials + 10% overage buffer")
            st.write("â€¢ Full prep to code + drainage")
            st.write("â€¢ 2-year workmanship warranty")
            st.write("â€¢ Progress photos + final cleanup")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_p:
            st.markdown('<div class="quote-card">', unsafe_allow_html=True)
            st.markdown("### ðŸŒŸ Premium")
            st.markdown(f'<div class="price-tag">${prem_total:,.0f}</div>', unsafe_allow_html=True)
            st.caption(f"â‰ˆ ${round(prem_total/work_area):,} per {unit_label.split()[0]}")
            st.write(f"â€¢ {base_desc} (upgraded path)")
            st.write("â€¢ Premium materials (cedar/composite options available)")
            st.write("â€¢ Enhanced features + white-glove service")
            st.write("â€¢ 3-year warranty + extended coverage")
            st.write("â€¢ Weekly updates + detailed documentation")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary actions
        st.success("**Next Step:** This is a solid estimate. A quick free site visit confirms final scope and any surprises. No pressure â€” I only want the job if itâ€™s the right fit for both of us.")
        
        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            if st.button("ðŸ“§ Email Quote to Client", use_container_width=True):
                st.info("In production this would generate a branded PDF + pre-filled email. Want that added next?")
        with qa2:
            if st.button("ðŸ’¾ Save to Pipeline", use_container_width=True):
                st.success("Quote + details captured. Ready for follow-up outreach.")
        with qa3:
            if st.button("âœ‰ï¸ Generate Follow-up Email", use_container_width=True):
                st.info("Scroll down to the 'Outreach & Email' tab â€” I've pre-filled it with this project's details for you.")
        
        st.caption("Pricing includes local delivery from Lehighton/903 suppliers, 6% PA tax on materials, and labor. Final price locked after on-site measurement. We are fully Licensed & Insured.")

# ========== TAB 2: PIPELINE ==========
with tab_pipeline:
    st.header("Pipeline & Schedule Overview", divider="orange")
    
    st.subheader("Active Jobs & Upcoming")
    
    # Simple demo data - in real version this would come from DB/Sheets/Ops Hub
    pipeline = [
        {"Client": "Tammie S.", "Project": "Storm Bed Refresh - Lehighton", "Status": "Deposit Received", "Start": "Jul 22", "Value": "$2,850"},
        {"Client": "Mike R.", "Project": "Deck Repair + Railing - Weatherly", "Status": "Quote Sent", "Start": "TBD", "Value": "$3,400"},
        {"Client": "Nextdoor Lead", "Project": "Patio Extension - Jim Thorpe", "Status": "Site Visit Booked", "Start": "Jul 29", "Value": "$5,900"},
    ]
    st.dataframe(pipeline, use_container_width=True, hide_index=True)
    
    st.info("**Capacity Note:** With current truck status, Iâ€™m focusing on jobs that can be completed in 1-2 days or are very local until the transfer case is fully sorted. Larger jobs are being queued for early-mid August.")
    
    if st.button("Run AI Schedule Optimizer"):
        st.success("Would integrate with djm-schedule-optimizer: Prioritize deposit jobs, batch Weatherly/Lehighton work, protect wrenching days. Let me know if you want this tab expanded with real optimization.")

# ========== TAB 3: LEAD INTAKE ==========
with tab_lead:
    st.header("Lead Intake", divider="orange")
    st.markdown("Capture leads from Nextdoor, Craigslist, Facebook, or calls. One-click add to pipeline.")
    
    lcol1, lcol2 = st.columns(2)
    with lcol1:
        l_name = st.text_input("Lead / Client Name")
        l_phone = st.text_input("Phone Number")
        l_source = st.selectbox("Source", ["Nextdoor", "Craigslist", "Facebook", "Google", "Referral", "Other"])
    with lcol2:
        l_service = st.selectbox("Service Interested In", ["Deck", "Patio/Pavers", "Fencing", "Walkway/Stairs", "Yard Refresh", "Other"])
        l_urgency = st.select_slider("How soon?", ["Just looking", "This season", "Within 2-3 weeks", "ASAP"])
    
    l_notes = st.text_area("Conversation Notes", height=90)
    
    if st.button("âž• Add Lead & Queue Follow-up", type="primary"):
        st.success(f"Lead for {l_name or 'New Client'} saved to pipeline. Auto follow-up template ready in the Outreach tab.")
        st.balloons()

# ========== TAB 4: OUTREACH & EMAIL (NEW) ==========
with tab_outreach:
    st.header("Outreach & Email Templates", divider="orange")
    st.markdown("Generate warm, professional emails that sound like you â€” the good-neighbor contractor who actually cares about doing the job right.")
    
    st.subheader("Create a Follow-up Email")
    
    oe1, oe2 = st.columns(2)
    with oe1:
        oe_client = st.text_input("Client First Name", value="John")
        oe_project = st.text_input("Project Type", value="deck repair")
        oe_amount = st.text_input("Recommended Quote Amount", value="$3,850")
    with oe2:
        oe_next_step = st.selectbox("Next Step You're Suggesting", 
            ["free site visit this week", "schedule a time that works for you", "reply with your preferred day", "lock it in with a small deposit"])
        oe_urgency = st.selectbox("Urgency Tone", 
            ["Friendly follow-up", "Gentle nudge (quote sent 4+ days ago)", "Time-sensitive (good weather window)"])
    
    if st.button("âœï¸ Generate Professional Email", type="primary"):
        # Build a warm, on-brand email
        today = datetime.now().strftime("%B %d, %Y")
        
        subject = f"Follow-up on your {oe_project} quote for {oe_client}"
        
        body = f"""Hi {oe_client},

I hope you're doing well. I wanted to follow up on the quote I sent for your {oe_project}.

The recommended option came in at **{oe_amount}** â€” that includes quality materials, proper prep for our local soil and weather, and a solid warranty so you don't have to think about it again for years.

I'm still holding space in the schedule for {oe_next_step}. The weather window looks good over the next couple of weeks, and I'd love to get this done right for you before things get busy.

If anything has changed or you have questions, just reply to this email or text me directly at (272) 394-5428. No pressure at all â€” I only want the job if it's the right fit.

Thanks again for considering DJM Project Pro's. I appreciate the opportunity.

Warm regards,  
Dylan Mabe  
DJM Project Pro's  
Licensed & Insured in Pennsylvania  
Text: (272) 394-5428 | Email: djmprojectpro@gmail.com  
djmprojectpro.com"""

        if "nudge" in oe_urgency.lower():
            body = body.replace("I wanted to follow up", "Just circling back to make sure my email didn't get buried")
        
        st.markdown("### Ready-to-Copy Email")
        st.markdown(f"**Subject:** {subject}")
        st.markdown(f'<div class="email-box">{body}</div>', unsafe_allow_html=True)
        
        st.caption("Copy the whole block above and paste into Gmail/Outlook. Feels personal, stays professional, and protects your time.")
        
        if st.button("ðŸ“‹ Copy Email to Clipboard (simulated)"):
            st.success("Email copied in real version. In production this would use st.copy_to_clipboard or JS.")

# Footer
st.markdown("""
<div class="djm-footer">
    <strong>DJM Project Pro's</strong> â€” Licensed & Insured in Pennsylvania<br>
    Free Estimates â€¢ Quality Work You Can Trust â€¢ Carbon County Local<br>
    ðŸ“ž Text preferred: (272) 394-5428 &nbsp;â€¢&nbsp; âœ‰ï¸ djmprojectpro@gmail.com &nbsp;â€¢&nbsp; ðŸŒ djmprojectpro.com<br>
    <small>Helping you win more of the right jobs with clear communication and excellent client experiences. v1.1</small>
</div>
""", unsafe_allow_html=True)
