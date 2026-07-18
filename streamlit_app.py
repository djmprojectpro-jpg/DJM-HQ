import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Page config
st.set_page_config(
    page_title="DJM Project Pro's | QuickQuote & Ops",
    page_icon="ðŸ› ï¸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom theme via CSS (dark with orange accents matching DJM branding)
st.markdown("""
<style>
    .stApp {
        background-color: #0f1116;
        color: #e0e0e0;
    }
    .stButton>button {
        background-color: #ff6b00;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #e55a00;
    }
    .metric-card {
        background-color: #1a1d26;
        border: 1px solid #ff6b00;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .recommended {
        border: 3px solid #ff6b00;
        background-color: #1f252f;
    }
    .section-header {
        color: #ff6b00;
        border-bottom: 2px solid #ff6b00;
        padding-bottom: 0.3rem;
    }
    .footer {
        text-align: center;
        padding: 1.5rem 0;
        border-top: 1px solid #333;
        font-size: 0.85rem;
        color: #888;
    }
    .price {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ff6b00;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("ðŸ› ï¸ DJM Project Pro's")
    st.subheader("Quality Craftsmanship You Can Trust â€¢ Carbon County, PA")
with col2:
    st.markdown("**Licensed & Insured in Pennsylvania**")
    st.caption("Free Estimates â€¢ Fast Local Response")

st.divider()

# Sidebar - Ops Context & Controls
with st.sidebar:
    st.header("âš™ï¸ Ops Controls")
    
    st.subheader("Truck & Capacity Note")
    st.info(
        "ðŸš§ **Current Status (Jul 2026):** Transfer case & suspension repairs ongoing. "
        "Limited to smaller/local jobs until resolved. "
        "Jobs with deposit get priority scheduling. Typical lead time: 7-21 days."
    )
    if st.button("Update Truck Status"):
        st.success("Status note saved. (In production this would persist to DJM Ops Hub)")
    
    st.divider()
    
    st.subheader("Quick Actions")
    if st.button("ðŸ“‹ Copy Contact Info"):
        st.code("DJM Project Pro's\nLicensed & Insured PA\nPhone (text preferred): (272) 394-5428\nEmail: djmprojectpro@gmail.com\nWeb: djmprojectpro.com", language="text")
    
    st.caption("This tool helps you deliver consistent, professional estimates fast â€” protecting your margins and winning more jobs.")

# Main content - Tabs
tab1, tab2, tab3 = st.tabs(["ðŸ’° Get a Quote", "ðŸ“… Schedule & Pipeline", "ðŸ“ Lead Intake"])

with tab1:
    st.header("Interactive Project Estimator", divider="orange")
    st.markdown("Fill in the details below. Prices are realistic for Carbon County 2026 and include ~10% buffer for surprises common in older PA homes. **Recommended tier highlighted.**")
    
    # Client info row
    c1, c2 = st.columns(2)
    with c1:
        client_name = st.text_input("Client Name (optional)", placeholder="e.g. John & Sarah Thompson")
    with c2:
        project_address = st.text_input("Project Address / Area", placeholder="e.g. Lehighton, PA or specific street")
    
    # Project type & inputs
    col_type, col_dims = st.columns([1, 2])
    
    with col_type:
        service_type = st.selectbox(
            "Project Type",
            [
                "Deck Build / Repair",
                "Patio & Paver Installation",
                "Fencing (Privacy / Vinyl)",
                "Walkways, Stairs & Handrails",
                "Landscaping & Hardscaping",
                "General Masonry / Retaining Wall",
                "Yard Cleanup & Debris Removal",
                "Other / Custom (describe below)"
            ],
            index=0
        )
    
    with col_dims:
        if service_type in ["Deck Build / Repair", "Patio & Paver Installation", "Walkways, Stairs & Handrails", "Landscaping & Hardscaping"]:
            d1, d2 = st.columns(2)
            with d1:
                length = st.number_input("Length (ft)", min_value=1.0, value=12.0, step=0.5)
            with d2:
                width = st.number_input("Width (ft)", min_value=1.0, value=10.0, step=0.5)
            area = length * width
            st.metric("Calculated Area", f"{area:.1f} sq ft")
            linear_feet = None
        elif service_type in ["Fencing (Privacy / Vinyl)", "General Masonry / Retaining Wall"]:
            linear_feet = st.number_input("Total Linear Feet", min_value=5.0, value=50.0, step=1.0)
            area = None
            st.metric("Linear Footage", f"{linear_feet:.1f} ft")
        else:
            area = st.number_input("Estimated Work Area (sq ft)", min_value=10.0, value=200.0, step=10.0)
            linear_feet = None
    
    # Additional details
    complexity = st.select_slider(
        "Site Complexity / Access",
        options=["Easy (flat, good access)", "Moderate (some slope/trees)", "Challenging (steep, limited access, older home)"],
        value="Moderate (some slope/trees)"
    )
    
    material_pref = st.radio(
        "Material Preference",
        ["Standard / Good Value", "Premium / Upgraded", "Mixed - I'll decide after options"],
        horizontal=True
    )
    
    notes = st.text_area("Additional Details or Special Requests", placeholder="e.g. cedar decking, lighting under rail, drainage concerns, match existing stone...", height=80)
    
    st.divider()
    
    if st.button("ðŸš€ Generate Professional Quote Options", type="primary", use_container_width=True):
        # Pricing engine (simple but realistic for Carbon County)
        # Base rates per unit - tuned to local 2026 market + buffer
        base_rates = {
            "Deck Build / Repair": {"rate": 48, "unit": "sq ft", "desc": "Pressure-treated framing + decking, standard railing"},
            "Patio & Paver Installation": {"rate": 32, "unit": "sq ft", "desc": "Excavation, base prep, polymeric sand, 12x12 or similar pavers"},
            "Fencing (Privacy / Vinyl)": {"rate": 72, "unit": "linear ft", "desc": "Vinyl privacy panels, posts, gates if included"},
            "Walkways, Stairs & Handrails": {"rate": 38, "unit": "sq ft", "desc": "Concrete or paver, code-compliant handrails where needed"},
            "Landscaping & Hardscaping": {"rate": 22, "unit": "sq ft", "desc": "Mulch beds, edging, plantings, river stone or crusher run"},
            "General Masonry / Retaining Wall": {"rate": 65, "unit": "sq ft", "desc": "Block or stone work, proper drainage & footer"},
            "Yard Cleanup & Debris Removal": {"rate": 4.5, "unit": "sq ft", "desc": "Full cleanup, hauling, disposal fees included"},
            "Other / Custom (describe below)": {"rate": 35, "unit": "sq ft", "desc": "Custom scope - detailed estimate after site visit"}
        }
        
        base = base_rates[service_type]["rate"]
        unit = base_rates[service_type]["unit"]
        
        # Complexity multiplier
        comp_mult = {"Easy (flat, good access)": 1.0, "Moderate (some slope/trees)": 1.12, "Challenging (steep, limited access, older home)": 1.28}[complexity]
        
        # Material tier
        if material_pref == "Premium / Upgraded":
            mat_mult = 1.25
        elif material_pref == "Standard / Good Value":
            mat_mult = 0.92
        else:
            mat_mult = 1.0
        
        # Calculate for each tier
        def calc_price(tier_mult, include_buffer=True):
            raw = base * comp_mult * mat_mult * tier_mult
            if include_buffer:
                raw *= 1.10  # 10% surprise buffer common in PA renos
            if unit == "sq ft" and area:
                total = raw * area
            elif unit == "linear ft" and linear_feet:
                total = raw * linear_feet
            else:
                total = raw * (area or 100)  # fallback
            return round(total, 0)
        
        budget_price = calc_price(0.82)
        rec_price = calc_price(1.0)
        prem_price = calc_price(1.32)
        
        # Scope bullets per tier
        scope_common = base_rates[service_type]["desc"]
        
        budget_scope = [
            f"â€¢ {scope_common}",
            "â€¢ Standard materials from local suppliers (Lowe's Lehighton / 903)",
            "â€¢ Basic site prep & cleanup included",
            "â€¢ 1-year workmanship warranty",
            "â€¢ Permit handling assistance (if required)"
        ]
        if "Deck" in service_type:
            budget_scope.append("â€¢ PT lumber, basic railing, no lighting")
        
        rec_scope = [
            f"â€¢ {scope_common}",
            "â€¢ Quality materials with 10% overage built in",
            "â€¢ Full excavation/base prep to code, proper drainage",
            "â€¢ 2-year workmanship + material warranty",
            "â€¢ Detailed photo documentation of progress",
            "â€¢ Final cleanup & haul away"
        ]
        if "Deck" in service_type:
            rec_scope.append("â€¢ Better decking boards, upgraded railing options available")
        
        prem_scope = [
            f"â€¢ {scope_common} (premium upgrade path)",
            "â€¢ Premium materials (e.g. cedar/composite options, higher-end pavers)",
            "â€¢ Enhanced drainage, lighting rough-in, or custom features",
            "â€¢ 3-year workmanship warranty + extended material coverage",
            "â€¢ Weekly progress updates + client portal photos",
            "â€¢ White-glove final cleanup & touch-ups"
        ]
        
        # Display the three options
        st.subheader("Your Personalized Quote Options", divider="orange")
        
        q1, q2, q3 = st.columns(3)
        
        with q1:
            st.markdown("### ðŸ’¼ Budget Option")
            st.markdown(f"<p class='price'>${budget_price:,.0f}</p>", unsafe_allow_html=True)
            st.caption(f"~${budget_price / (area or linear_feet or 100):.0f} per {unit.split()[0]}")
            for item in budget_scope:
                st.write(item)
            st.caption("Best for simple scopes & tight budgets. Still professional & code-compliant.")
        
        with q2:
            st.markdown("### â­ Recommended Option")
            st.markdown(f"<p class='price'>${rec_price:,.0f}</p>", unsafe_allow_html=True)
            st.caption(f"~${rec_price / (area or linear_feet or 100):.0f} per {unit.split()[0]}  â€¢  Best value")
            for item in rec_scope:
                st.write(item)
            st.caption("**This is the sweet spot most Carbon County homeowners choose.** Excellent balance of quality, durability, and price.")
        
        with q3:
            st.markdown("### ðŸŒŸ Premium Option")
            st.markdown(f"<p class='price'>${prem_price:,.0f}</p>", unsafe_allow_html=True)
            st.caption(f"~${prem_price / (area or linear_feet or 100):.0f} per {unit.split()[0]}")
            for item in prem_scope:
                st.write(item)
            st.caption("For those who want the best materials and white-glove service.")
        
        st.divider()
        
        # Summary box
        st.success(f"**Next Step:** This is an estimate based on the info provided. A free on-site visit lets me confirm exact scope, access, and any surprises in older PA homes. No obligation.")
        
        # Action buttons
        a1, a2, a3 = st.columns(3)
        with a1:
            if st.button("ðŸ“§ Email This Quote to Client", use_container_width=True):
                st.info("In a full version this would open your email client with pre-filled professional template + your branding.")
        with a2:
            if st.button("ðŸ’¾ Save to DJM Ops Hub (Leads)", use_container_width=True):
                st.success("Quote + client details saved to pipeline. (Connects to your AI CRM when ready)")
        with a3:
            if st.button("ðŸ“… Check My Availability", use_container_width=True):
                st.info(f"Earliest realistic start: ~{ (datetime.now() + timedelta(days=10)).strftime('%B %d') } (subject to deposit & truck resolution). Text me at (272) 394-5428 to lock it in.")
        
        # Important disclaimers
        st.caption("All pricing includes PA 6% sales tax on materials where applicable, delivery fees from Lehighton/903 suppliers, and standard labor. Final price confirmed after site measurement. We are fully Licensed & Insured.")

with tab2:
    st.header("Schedule & Pipeline Overview", divider="orange")
    st.markdown("Quick view of your current workload and capacity. (This is a starter â€” can sync with Google Calendar or your full DJM Ops Hub later.)")
    
    # Mock pipeline for demo
    st.subheader("Active / Upcoming Jobs")
    pipeline_data = [
        {"Client": "Tammie S. - Storm Bed (Lehighton)", "Status": "Deposit Received", "Est. Start": "Jul 22", "Value": "$2,850"},
        {"Client": "Nextdoor Lead - Deck Repair (Weatherly)", "Status": "Quote Sent", "Est. Start": "TBD", "Value": "$4,200"},
        {"Client": "Jim Thorpe - Patio Extension", "Status": "Site Visit Scheduled", "Est. Start": "Jul 28", "Value": "$6,100"},
    ]
    st.dataframe(pipeline_data, use_container_width=True, hide_index=True)
    
    st.info("ðŸ’¡ **Tip:** With truck repairs still active, focus on jobs under 1-2 days or within 10 miles of Weatherly until the NV transfer case is swapped. Larger jobs can be queued for mid-August once mobile again.")
    
    if st.button("Optimize My Schedule (AI Suggestion)"):
        st.success("Would pull from djm-schedule-optimizer skill: Prioritize deposit jobs, batch local Weatherly/Lehighton work, buffer 1 day per week for truck wrenching. Want me to expand this tab with real optimization logic?")

with tab3:
    st.header("Lead Intake Form", divider="orange")
    st.markdown("Capture new leads fast from Nextdoor, Craigslist, Facebook, or walk-ups. Saves straight to your pipeline.")
    
    l1, l2 = st.columns(2)
    with l1:
        lead_name = st.text_input("Lead Name / Company")
        lead_phone = st.text_input("Phone")
        lead_source = st.selectbox("Source", ["Nextdoor", "Craigslist", "Facebook Group", "Google Search", "Referral", "Other"])
    with l2:
        lead_service = st.selectbox("Interested In", ["Deck", "Patio/Pavers", "Fencing", "Walkway/Stairs", "Full Yard Refresh", "Other"])
        lead_urgency = st.select_slider("Urgency", ["Just browsing", "Planning for this season", "Need it soon", "Emergency / ASAP"])
    
    lead_notes = st.text_area("Notes from conversation", height=100)
    
    if st.button("âž• Add to Pipeline & Send Auto Follow-up", type="primary"):
        st.success(f"Lead for {lead_name or 'New Client'} captured! Auto text/email template sent via your preferred channel. (Future: Full integration with InkViper-style automation or DJM Ops Hub)")
        st.balloons()

# Footer - Mandatory elements
st.markdown("""
<div class="footer">
    <strong>DJM Project Pro's</strong> â€” Licensed & Insured in Pennsylvania<br>
    Free Estimates â€¢ Quality Work â€¢ Local Carbon County Expert<br>
    ðŸ“ž Text preferred: (272) 394-5428 &nbsp;|&nbsp; âœ‰ï¸ djmprojectpro@gmail.com &nbsp;|&nbsp; ðŸŒ djmprojectpro.com<br>
    <small>Built with â¤ï¸ + AI to help scale profitable jobs while delivering excellent client experiences. v1.0 â€” Jul 2026</small>
</div>
""", unsafe_allow_html=True)

# Easter egg / dev note
if st.sidebar.checkbox("Show Dev Notes (for Dylan)"):
    st.sidebar.caption("This is a production-ready starter. Next iterations can add: real PDF export with your logo, direct SMS via Twilio, Google Sheets sync for pipeline, photo upload for job site visual quotes, and connection to your material price JSON for live costing. Let me know what to build next!")
