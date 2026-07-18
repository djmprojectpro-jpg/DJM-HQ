"""
DJM Project Pro's HQ - Professional Ops Dashboard
Clean, maintainable Streamlit app for home improvement contractor in Carbon County, PA
"""

import streamlit as st
from datetime import datetime
import sqlite3
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import os
import stripe

# ==================== CONFIG ====================
st.set_page_config(
    page_title="DJM Project Pro's HQ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme CSS
st.markdown("""
<style>
    .stApp { background-color: #0f1116; color: #ffffff; }
    .stButton > button {
        background-color: #ff6b00 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover { background-color: #e55a00 !important; }
    .quote-card { background-color: #1a1d26; border: 1px solid #333; border-radius: 14px; padding: 1rem; }
    .quote-card.recommended { border: 3px solid #ff6b00; background-color: #1f252f; }
    .price-tag { font-size: 1.8rem; font-weight: 700; color: #ff6b00; }
    .djm-footer { text-align: center; padding: 1rem 0; border-top: 1px solid #333; font-size: 0.85rem; color: #888; }
    .email-box { background-color: #1a1d26; border-left: 5px solid #ff6b00; padding: 1rem; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE ====================
DB_PATH = "djm_ops_hub.db"  # Relative path works on Streamlit Cloud

def init_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, service TEXT,
        source TEXT, notes TEXT, score INTEGER DEFAULT 50, status TEXT DEFAULT 'New',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pipeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT, client TEXT, service TEXT, value REAL,
        status TEXT, start_date TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Seed sample jobs if pipeline is empty (for easier testing)
    c.execute("SELECT COUNT(*) FROM pipeline")
    if c.fetchone()[0] == 0:
        sample_jobs = [
            ("Tammie S.", "Storm Bed Refresh - Lehighton", 2850, "Deposit Received", "2026-07-22", "Priority - deposit paid"),
            ("Mike R.", "Deck Repair + Railing - Weatherly", 3400, "Quoted", None, "Waiting on deposit"),
            ("Jim Thorpe Home", "Patio Extension", 5900, "Scheduled", "2026-07-29", "Weather dependent"),
        ]
        c.executemany("INSERT INTO pipeline (client, service, value, status, start_date, notes) VALUES (?, ?, ?, ?, ?, ?)", sample_jobs)
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def get_leads(limit=50):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM leads ORDER BY created_at DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    return data

def add_lead(name, phone, service, source, notes, score=50):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO leads (name, phone, service, source, notes, score, status) VALUES (?, ?, ?, ?, ?, ?, 'New')",
              (name, phone, service, source, notes, score))
    conn.commit()
    conn.close()

def get_pipeline_jobs():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM pipeline ORDER BY created_at DESC")
    data = c.fetchall()
    conn.close()
    return data

def add_pipeline_job(client, service, value, status="Quoted", start_date=None, notes=""):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO pipeline (client, service, value, status, start_date, notes) VALUES (?, ?, ?, ?, ?, ?)",
              (client, service, value, status, start_date, notes))
    conn.commit()
    conn.close()

def update_job_status(job_id, new_status):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE pipeline SET status = ? WHERE id = ?", (new_status, job_id))
    conn.commit()
    conn.close()

init_database()

# ==================== PDF GENERATION ====================
def generate_quote_pdf(client_name, project_location, service_type, work_area, complexity, material_pref,
                       budget_price, rec_price, prem_price, scope_common):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.6*inch, leftMargin=0.6*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=HexColor('#ff6b00'),
                                 alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11, textColor=HexColor('#333333'),
                                    alignment=TA_CENTER, spaceAfter=12)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=13, textColor=HexColor('#ff6b00'),
                                   spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=13)
    
    story = []
    story.append(Paragraph("DJM PROJECT PRO'S", title_style))
    story.append(Paragraph("Licensed & Insured • Carbon County, PA", subtitle_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(f"<b>Prepared For:</b> {client_name or 'Valued Client'}", body_style))
    story.append(Paragraph(f"<b>Location:</b> {project_location or 'Carbon County, PA'}", body_style))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Paragraph(f"<b>Service:</b> {service_type}", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("PROJECT DETAILS", section_style))
    story.append(Paragraph(f"Work Area: {work_area} sq ft | Complexity: {complexity} | Material: {material_pref}", body_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("PRICING OPTIONS", section_style))
    pricing_data = [
        ['Option', 'Total', 'Best For'],
        ['Budget', f'${budget_price:,.0f}', 'Basic materials'],
        ['RECOMMENDED', f'${rec_price:,.0f}', 'Best value'],
        ['Premium', f'${prem_price:,.0f}', 'Top-tier finish']
    ]
    table = Table(pricing_data, colWidths=[2*inch, 1.5*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#ff6b00')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#fff5eb')),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("WHAT'S INCLUDED", section_style))
    story.append(Paragraph(f"• {scope_common}<br/>• Professional installation<br/>• 10% buffer for surprises<br/>• Final cleanup included", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("NEXT STEPS", section_style))
    story.append(Paragraph("This is an estimate. A free site visit confirms final scope. Text (272) 394-5428 to schedule.", body_style))
    story.append(Spacer(1, 15))
    
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=HexColor('#666666'), alignment=TA_CENTER)
    story.append(Paragraph("DJM Project Pro's • Licensed & Insured in Pennsylvania • djmprojectpro.com", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==================== STRIPE ====================
stripe.api_key = st.secrets.get("stripe", {}).get("api_key") if "stripe" in st.secrets else None

def create_stripe_deposit_link(amount, client_name, project_description):
    if not stripe.api_key:
        return None, "Stripe key not configured in secrets."
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Deposit - {project_description}'},
                    'unit_amount': int(amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://djm-hq.streamlit.app?payment=success',
            cancel_url='https://djm-hq.streamlit.app?payment=cancelled',
        )
        return session.url, None
    except Exception as e:
        return None, str(e)

# ==================== HEADER + ALERTS ====================
col1, col2 = st.columns([4, 3])
with col1:
    st.title("🛠️ DJM Project Pro's HQ")
    st.caption("Quality Craftsmanship • Carbon County, PA")
with col2:
    st.markdown("**Licensed & Insured in Pennsylvania**")
    st.caption("Free Estimates • (272) 394-5428 • djmprojectpro@gmail.com")

st.divider()

# Smart Alerts
conn = get_db_connection()
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM leads WHERE status='New'")
new_leads = c.fetchone()[0] or 0
conn.close()

truck_status = "In Repair - Limited Capacity"
if "Repair" in truck_status:
    st.warning(f"🚧 Truck Status: {truck_status} — Prioritize small/local jobs + deposits.")
else:
    st.success(f"✅ Truck Status: {truck_status} — Full capacity available.")

if new_leads > 0:
    st.info(f"📬 {new_leads} new leads waiting for follow-up.")

# ==================== TABS ====================
tab_dash, tab_quote, tab_leads, tab_pipeline, tab_photos, tab_materials, tab_outreach = st.tabs([
    "📊 Dashboard", "💰 Quick Quote", "📝 Leads", "📋 Pipeline", "📸 Photos & Marketing", "🧱 Materials", "✉️ Outreach"
])

# --- DASHBOARD ---
with tab_dash:
    st.header("Business Overview Dashboard", divider="orange")
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM leads WHERE date(created_at) >= date('now', '-7 days')")
    leads_week = c.fetchone()[0] or 0
    c.execute("SELECT SUM(value) FROM pipeline")
    pipeline_value = c.fetchone()[0] or 12450
    conn.close()
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("New Leads (7d)", leads_week, "+3")
    k2.metric("Pipeline Value", f"${pipeline_value:,.0f}", "+$2,800")
    k3.metric("Active Jobs", 4, "2 starting soon")
    k4.metric("Est. Win Rate", "68%", "+4%")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Pipeline Value by Status")
        status_df = pd.DataFrame({
            "Status": ["Quoted", "Deposit Received", "Scheduled", "In Progress", "Completed"],
            "Value": [4850, 6200, 3100, 8900, 12450]
        })
        fig = px.bar(status_df, x="Status", y="Value", color="Status", color_discrete_sequence=["#ff6b00"]*5)
        fig.update_layout(height=280, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Leads by Source")
        source_df = pd.DataFrame({"Source": ["Nextdoor", "Referral", "Facebook", "Google", "Craigslist"], "Count": [12, 8, 5, 4, 3]})
        fig2 = px.pie(source_df, values="Count", names="Source", hole=0.45, color_discrete_sequence=["#ff6b00", "#e55a00", "#ff8533", "#ffb366", "#ffd9b3"])
        fig2.update_layout(height=280)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    st.subheader("⚡ Quick Actions")
    qa = st.columns(4)
    qa[0].button("➕ New Lead", use_container_width=True)
    qa[1].button("💰 New Quote", use_container_width=True)
    qa[2].button("📅 Schedule Job", use_container_width=True)
    qa[3].button("📸 Upload Photos", use_container_width=True)

# --- QUICK QUOTE ---
with tab_quote:
    st.header("Quick Quote Estimator", divider="orange")
    
    client_name = st.text_input("Client Name (optional)")
    project_location = st.text_input("Project Location", value="Lehighton, PA")
    service_type = st.selectbox("Service Type", ["Deck Build / Repair", "Patio & Paver Installation", "Fencing (Privacy / Vinyl)", 
                                                 "Walkways, Stairs & Handrails", "Landscaping & Hardscaping", "Yard Cleanup & Debris Removal"])
    
    work_area = st.number_input("Work Area (sq ft or linear ft)", min_value=10.0, value=200.0, step=10.0)
    complexity = st.select_slider("Complexity", ["Easy access & flat", "Moderate", "Challenging (older home)"], value="Moderate")
    material_pref = st.selectbox("Material Preference", ["Good Value (Standard)", "Recommended Balance", "Premium Upgraded"])
    
    if st.button("🚀 Generate Quote Options", type="primary", use_container_width=True):
        base_rates = {"Deck Build / Repair": 48, "Patio & Paver Installation": 32, "Fencing (Privacy / Vinyl)": 72,
                      "Walkways, Stairs & Handrails": 38, "Landscaping & Hardscaping": 22, "Yard Cleanup & Debris Removal": 4.5}
        base = base_rates.get(service_type, 35)
        comp_mult = {"Easy access & flat": 1.0, "Moderate": 1.12, "Challenging (older home)": 1.28}[complexity]
        mat_mult = {"Good Value (Standard)": 0.92, "Recommended Balance": 1.0, "Premium Upgraded": 1.25}[material_pref]
        
        def get_price(factor):
            return round(base * comp_mult * mat_mult * factor * 1.10 * work_area, 0)
        
        budget = get_price(0.82)
        rec = get_price(1.0)
        prem = get_price(1.32)
        
        st.session_state['last_quote'] = {
            'client_name': client_name, 'project_location': project_location, 'service_type': service_type,
            'work_area': work_area, 'complexity': complexity, 'material_pref': material_pref,
            'budget_price': budget, 'rec_price': rec, 'prem_price': prem,
            'scope_common': f"{service_type} - Professional installation with 10% buffer"
        }
        
        col_b, col_r, col_p = st.columns(3)
        with col_b:
            st.markdown("### 💼 Budget")
            st.markdown(f'<div class="price-tag">${budget:,.0f}</div>', unsafe_allow_html=True)
        with col_r:
            st.markdown('<div class="quote-card recommended">', unsafe_allow_html=True)
            st.markdown("### ⭐ RECOMMENDED")
            st.markdown(f'<div class="price-tag">${rec:,.0f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_p:
            st.markdown("### 🌟 Premium")
            st.markdown(f'<div class="price-tag">${prem:,.0f}</div>', unsafe_allow_html=True)
        
        # PDF Export
        if st.button("📄 Download Professional PDF Quote", type="primary"):
            pdf = generate_quote_pdf(client_name, project_location, service_type, work_area, complexity, material_pref,
                                     budget, rec, prem, st.session_state['last_quote']['scope_common'])
            st.download_button("⬇️ Download PDF", pdf, f"DJM_Quote_{client_name or 'Client'}.pdf", "application/pdf")
        
        # Stripe Deposit
        st.subheader("💳 Request Deposit via Stripe")
        dep_pct = st.slider("Deposit %", 20, 50, 30)
        dep_amt = int(rec * (dep_pct / 100))
        st.metric("Deposit Amount", f"${dep_amt:,}")
        
        if st.button("💳 Create Stripe Deposit Link", type="primary"):
            if stripe.api_key:
                url, err = create_stripe_deposit_link(dep_amt, client_name or "Client", service_type)
                if url:
                    st.success("✅ Checkout link created!")
                    st.code(url)
                else:
                    st.error(err)
            else:
                st.warning("Add your Stripe key to .streamlit/secrets.toml")

# --- LEADS ---
with tab_leads:
    st.header("Lead Intake", divider="orange")
    c1, c2 = st.columns(2)
    with c1:
        l_name = st.text_input("Client Name")
        l_phone = st.text_input("Phone")
        l_source = st.selectbox("Source", ["Nextdoor", "Referral", "Facebook", "Google", "Craigslist", "Other"])
    with c2:
        l_service = st.selectbox("Service", ["Deck", "Patio/Pavers", "Fencing", "Walkway/Stairs", "Yard Refresh", "Other"])
        l_urgency = st.select_slider("Urgency", ["Just looking", "This season", "2-3 weeks", "ASAP"])
    l_notes = st.text_area("Notes")
    
    if st.button("➕ Add Lead", type="primary"):
        score = 50
        if l_source == "Referral": score += 25
        elif l_source == "Nextdoor": score += 15
        if l_urgency in ["ASAP", "2-3 weeks"]: score += 15
        if l_service in ["Deck", "Patio/Pavers"]: score += 10
        add_lead(l_name or "New Client", l_phone, l_service, l_source, l_notes, min(score, 100))
        st.success(f"Lead saved! Score: {min(score, 100)}/100")

# --- PIPELINE ---
with tab_pipeline:
    st.header("Pipeline & Schedule", divider="orange")
    jobs = get_pipeline_jobs()
    if jobs:
        for job in jobs:
            job_id, client, service, value, status, start_date, notes, _ = job
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 2, 2])
                with c1:
                    st.write(f"**{client}** — {service}")
                    st.caption(f"Value: ${value:,.0f} | Start: {start_date or 'TBD'}")
                with c2:
                    new_status = st.selectbox("Status", ["Quoted", "Deposit Received", "Scheduled", "In Progress", "Completed"],
                                              index=["Quoted", "Deposit Received", "Scheduled", "In Progress", "Completed"].index(status),
                                              key=f"status_{job_id}")
                with c3:
                    if st.button("Update Status", key=f"update_{job_id}"):
                        update_job_status(job_id, new_status)
                        st.success(f"Updated {client} to {new_status}")
                        st.rerun()
    else:
        st.info("No jobs yet. Sample jobs are seeded automatically on first run.")
    
    st.subheader("💳 Request Deposit on Existing Job")
    if jobs:
        sel = st.selectbox("Job", [f"{j[1]} - {j[2]} (${j[3]:,.0f})" for j in jobs])
        damt = st.number_input("Deposit Amount", value=1000)
        if st.button("Create Deposit Link"):
            if stripe.api_key:
                url, err = create_stripe_deposit_link(damt, sel.split(" - ")[0], sel.split(" - ")[1])
                if url: st.code(url)
            else: st.warning("Add Stripe key to secrets.")

# --- PHOTOS & MARKETING ---
with tab_photos:
    st.header("Photos & Marketing Tools", divider="orange")
    up = st.file_uploader("Upload Job Photos", type=["jpg","png"], accept_multiple_files=True)
    if up:
        for f in up:
            with open(f"/home/workdir/artifacts/uploads/{f.name}", "wb") as out:
                out.write(f.read())
        st.success(f"Saved {len(up)} photos.")
        proj = st.selectbox("Project Type", ["Deck Transformation", "Patio Installation", "Fence Installation"])
        if st.button("Generate Ad Captions"):
            st.code(f"Just finished this {proj.lower()} in Lehighton, PA. Quality work from DJM Project Pro's. Text (272) 394-5428 for yours!")

# --- MATERIALS ---
with tab_materials:
    st.header("Current Material
