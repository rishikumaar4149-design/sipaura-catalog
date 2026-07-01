import streamlit as st
import urllib.parse

COMPANY_NAME = "SipAura"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. Advanced Full HD Theme, 3D Typography Engine, Sticky Layout, & Infinite Marquee CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@1,600;1,800&display=swap');
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* STICKY SIDEBAR ENGINE (Pins Left Side Elements Natively) */
    [data-testid="stSidebar"] {
        background-color: #131921 !important;
        color: #FFFFFF !important;
        position: fixed !important;
        top: 0;
        left: 0;
        width: 25vw !important; 
        height: 100vh !important;
        max-height: 100vh !important; 
        overflow: hidden !important; 
        z-index: 999;
    }
    [data-testid="stSidebarUserContent"] {
        display: flex;
        flex-direction: column;
        justify-content: space-between; 
        height: 100vh !important;
        padding: 12px 16px !important;
        box-sizing: border-box;
    }
    
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-weight: 500 !important;
        text-align: center !important;
        display: block;
        width: 100%;
        margin-bottom: 2px !important;
    }
    [data-testid="stSidebar"] .stWidget { margin-bottom: 6px !important; }
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select { text-align: center !important; }
    
    /* 3D Sidebar Circular Logo Frame */
    .sidebar-logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 10px;
        perspective: 1000px;
    }
    .sidebar-logo-container img {
        width: 115px;
        height: 115px;
        border-radius: 50%;
        object-fit: cover;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transform: rotateX(8deg) rotateY(-4deg);
        box-shadow: 0 8px 16px rgba(0,0,0,0.25), 0 16px 32px rgba(0,0,0,0.3);
    }
    
    /* Compact Business Context Intro Panel Box */
    .business-intro-context {
        background-color: #1E293B;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 4px solid #10B981;
    }
    .business-intro-context p {
        font-size: 12.5px !important;
        line-height: 1.4 !important;
        color: #CBD5E1 !important;
        margin: 0 !important;
        text-align: left !important;
    }
    
    /* Premium Contact Info Card */
    .premium-contact-card {
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border: 1px solid #2D3748;
        border-radius: 16px;
        padding: 14px;
        margin-top: 5px;
    }
    .contact-title-highlight {
        color: #10B981 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        margin-bottom: 8px !important;
    }
    .contact-row-entry {
        display: flex;
        align-items: center;
        margin-bottom: 6px;
        font-size: 13px;
    }
    .contact-row-entry span {
        color: #94A3B8 !important;
        font-weight: 600;
        width: 65px;
    }
    .contact-row-entry p, .contact-row-entry a { color: #F1F5F9 !important; margin: 0 !important; }
    .query-call-to-action {
        background: rgba(16, 185, 129, 0.05);
        border: 1px dashed rgba(16, 185, 129, 0.2);
        border-radius: 8px;
        padding: 6px;
        margin-top: 8px;
        font-size: 11.5px;
        color: #A7F3D0 !important;
        text-align: center;
    }
    
    /* INFINITE CONTINUOUS MARQUEE ENGINE */
    @keyframes continuousMarquee {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-50%, 0, 0); }
    }
    .marquee-wrapper-box {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        padding-top: 10px;
        padding-bottom: 2px;
    }
    .marquee-scroll-track {
        display: inline-block;
        white-space: nowrap;
        animation: continuousMarquee 12s linear infinite;
    }
    .marquee-text-node {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #64748B !important;
        text-transform: uppercase;
        padding-right: 40px; 
    }
    
    /* -------------------------------------------------- */
    /* MAIN INTERFACE CONTENT FRAMEWAY RE-ALIGNMENT 75%  */
    /* -------------------------------------------------- */
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding-top: 25px !important;
        padding-left: 27vw !important; 
        padding-right: 30px !important;
    }
    
    /* -------------------------------------------------- */
    /* PROCEDURAL HORI BANNER TEXT WRITING ENGINE (3D)    */
    /* -------------------------------------------------- */
    @keyframes strokeWrite {
        to { stroke-dashoffset: 0; }
    }
    @keyframes extrude3D {
        to {
            text-shadow: 
                1px 1px 0px #3B4B20, 2px 2px 0px #3B4B20, 3px 3px 0px #3B4B20,
                4px 4px 0px #3B4B20, 5px 5px 0px #2D3715, 6px 6px 0px #2D3715,
                7px 7px 12px rgba(0,0,0,0.35), 0px 15px 30px rgba(85,107,47,0.25);
            transform: rotateX(12deg) rotateY(-6deg) translateY(0);
        }
    }
    @keyframes subTagFade {
        to { opacity: 0.85; transform: translateY(0); }
    }
    
    .animated-banner-canvas {
        width: 100%;
        background: linear-gradient(135deg, #FDFBF7 0%, #EFECE6 100%);
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 40px 20px;
        margin-bottom: 35px;
        text-align: center;
        perspective: 1200px;
        box-shadow: 0 10px 25px rgba(15,23,42,0.04);
        box-sizing: border-box;
    }
    
    /* Handdrawn SVG Stroke Vector Styles */
    .signature-path-text {
        font-family: 'Playfair Display', Georgia, serif;
        font-style: italic;
        font-weight: 800;
        font-size: 96px; /* Grand Full HD presentation metric footprint scale */
        fill: transparent;
        stroke: #556B2F; /* Luxury Olive Green Core */
        stroke-width: 2px;
        stroke-dasharray: 700;
        stroke-dashoffset: 700;
        stroke-linecap: round;
        stroke-linejoin: round;
        display: inline-block;
        
        /* Execution Phase Order: Write out borders, then pop 3D dimensions */
        animation: 
            strokeWrite 2.2s cubic-bezier(0.4, 0, 0.2, 1) forwards,
            extrude3D 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) 2s forwards;
    }
    
    /* Elegant E-Commerce Tagline */
    .animated-subtag-banner {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: #1E293B;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 15px;
        opacity: 0;
        transform: translateY(8px);
        animation: subTagFade 0.6s ease-out 2.4s forwards;
    }
    
    /* Interactive Product Grid Box */
    .product-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 24px; 
        margin-bottom: 28px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.01);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out forwards;
    }
    .product-box:hover {
        transform: translateY(-6px);
        box-shadow: 0 25px 40px -10px rgba(15, 23, 42, 0.12);
        border-color: #CBD5E1;
    }
    
    /* Strict 4:5 Portrait Aspect Ratio Container Logic */
    .bottle-img-container {
        width: 100%;
        position: relative;
        padding-top: 125%; 
        overflow: hidden;
        margin-bottom: 16px;
        border-radius: 16px;
        background-color: #FAFAFA;
    }
    .bottle-img-container img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover; 
    }
    
    .details-section {
        min-height: 190px; 
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .brand-tag {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #94A3B8;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .product-title {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 800;
        color: #0F172A;
        margin: 4px 0 0px 0;
        line-height: 1.3;
    }
    .by-brand-subscript {
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
        margin-bottom: 8px;
        display: block;
    }
    .sku-text {
        font-family: monospace;
        color: #94A3B8;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    .spec-pill {
        background-color: #F8FAFC;
        color: #334155;
        border: 1px solid #E2E8F0;
        font-size: 12px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 8px;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 8px;
    }
    
    .price-container {
        margin-top: auto;
        padding-top: 12px;
    }
    .mrp-strike {
        font-size: 14px;
        color: #94A3B8;
        text-decoration: line-through;
        margin-right: 6px;
        font-weight: 500;
    }
    .listing-price {
        font-size: 24px;
        font-weight: 900;
        color: #0F172A;
        display: inline-block;
    }
    .discount-badge {
        background-color: #25D366;
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-left: 6px;
    }
    
    .stButton>button {
        background-color: #1E293B !important; 
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #0F172A !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }
    .summary-card {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        border: 2px solid #1E293B;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Resilient Auto-Parsing Excel Pipeline
@st.cache_data
def load_data():
    import os
    import pandas as pd
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ No Product Spreadsheet detected inside the Repository root.")
        st.stop()
        
    target_file = excel_files[0]
    raw_df = pd.read_excel(target_file, sheet_name=0, engine="openpyxl")
    header_row = 0
    for idx, row in raw_df.iterrows():
        if "sku id" in row.astype(str).str.strip().str.lower().values:
            header_row = idx + 1
            break
            
    df = pd.read_excel(target_file, sheet_name=0, skiprows=header_row, engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

def get_clean_col(dataframe, keys, default=""):
    import pandas as pd
    for k in keys:
        match = [c for c in dataframe.columns if c.lower().strip() == k.lower().strip()]
        if match: return dataframe[match[0]]
    return pd.Series([default] * len(dataframe))

sku_s = get_clean_col(df, ["SKU ID", "sku"])
name_s = get_clean_col(df, ["Product Name", "Name"])
cat_s = get_clean_col(df, ["Category"]).fillna("Drinkware")
sub_s = get_clean_col(df, ["Sub category", "Subcategory"]).fillna("General")
cap_s = get_clean_col(df, ["Capacity"]).fillna("N/A")
col_s = get_clean_col(df, ["Colour", "Color"]).fillna("Standard")
mrp_s = get_clean_col(df, ["MRP", "Cost Price"])
disc_s = get_clean_col(df, ["Discount"])
price_s = get_clean_col(df, ["Final Price", "Final Listing Price", "Selling Price"])
desc_s = get_clean_col(df, ["Description"]).fillna("Premium hydration gear companion structure.")
spec_s = get_clean_col(df, ["Specification", "Specifications"]).fillna("Premium structural metrics build.")
kw_s = get_clean_col(df, ["Key Words", "Keywords"]).fillna("")
img_s = get_clean_col(df, ["Images", "Image Link"]).fillna("")

import pandas as pd
products = []
for i in range(len(df)):
    if pd.isna(sku_s.iloc[i]) or str(sku_s.iloc[i]).strip() == "nan":
        continue
    products.append({
        "sku": str(sku_s.iloc[i]), "name": str(name_s.iloc[i]), "category": str(cat_s.iloc[i]),
        "subcategory": str(sub_s.iloc[i]), "capacity": str(cap_s.iloc[i]), "colour": str(col_s.iloc[i]),
        "mrp": mrp_s.iloc[i] if pd.notna(mrp_s.iloc[i]) else None,
        "discount": disc_s.iloc[i] if pd.notna(disc_s.iloc[i]) else None,
        "price": price_s.iloc[i] if pd.notna(price_s.iloc[i]) else None,
        "description": str(desc_s.iloc[i]), "specification": str(spec_s.iloc[i]),
        "keywords": str(kw_s.iloc[i]), "images": str(img_s.iloc[i])
    })

if "cart" not in st.session_state: st.session_state.cart = {}
if "selected_product" not in st.session_state: st.session_state.selected_product = None

YOUR_PHONE_NUMBER = "919310234464"

# 3. STATIC / FROZEN LEFT SIDEBAR LAYOUT
LOGO_URL = "https://i.postimg.cc/1t838D2R/logo.jpg"
st.sidebar.markdown(f"""
    <div class="sidebar-logo-container">
        <img src="{LOGO_URL}">
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div class="business-intro-context">
        <p>
            SipAura is a premium marketplace specializing in next-generation vacuum-insulated drinkware. Every piece balances ergonomics with temperature-locking engineering to keep your hydration flawlessly fresh.
        </p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔍 Smart Search Catalog", placeholder="Search items...")

unique_cats = sorted(list(set([p["category"] for p in products])))
selected_category = st.sidebar.selectbox("📂 Category", ["All Categories"] + unique_cats)

if selected_category != "All Categories":
    unique_subs = sorted(list(set([p["subcategory"] for p in products if p["category"] == selected_category])))
else:
    unique_subs = sorted(list(set([p["subcategory"] for p in products])))
selected_sub = st.sidebar.selectbox("🏷️ Sub-Category", ["All Sub-Categories"] + unique_subs)

st.sidebar.markdown("""
    <div class="premium-contact-card">
        <div class="contact-title-highlight">📞 Help desk channels</div>
        <div class="contact-row-entry">
            <span>💬 Chat:</span>
            <p>+91 93102 34464</p>
        </div>
        <div class="contact-row-entry">
            <span>📧 Email:</span>
            <a href="mailto:support@sipaura.com">support@sipaura.com</a>
        </div>
        <div class="query-call-to-action">🙋 Have a custom order request? Feel free to ask your query right now over chat!</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div class="marquee-wrapper-box">
        <div class="marquee-scroll-track">
            <span class="marquee-text-node">⚡ Powered by InFlowMart</span>
            <span class="marquee-text-node">⚡ Powered by InFlowMart</span>
            <span class="marquee-text-node">⚡ Powered by InFlowMart</span>
            <span class="marquee-text-node">⚡ Powered by InFlowMart</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. PROCEDURAL 3D WRITING BANNER REPLACEMENT (Replaces image layout dynamically)
st.markdown("""
    <div class="animated-banner-canvas">
        <svg viewBox="0 0 1000 140" width="100%">
            <text x="50%" y="95" text-anchor="middle" class="signature-path-text">SipAura</text>
        </svg>
        <div class="animated-subtag-banner">Bring Your Own</div>
    </div>
""", unsafe_allow_html=True)

# Details Preview Drawer
if st.session_state.selected_product:
    p = st.session_state.selected_product
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        s_img = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" and p["images"].strip() != "" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
        st.image(s_img, use_container_width=True)
    with col_s2:
        st.markdown(f"<span class='brand-tag'>{p['category']} • {p['subcategory']}</span>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin-top:0; margin-bottom:4px;'>📋 {p['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f'<span class="sku-pill">SKU CODE: {p["sku"]}</span>', unsafe_allow_html=True)
        st.markdown(f"🎨 **Color Option:** {p['colour']}  |  📏 **Capacity Metric:** {p['capacity']}")
        
        if p["mrp"] and p["price"]:
            try:
                m_val = float(p['mrp'])
                p_val = float(p['price'])
                pct = int(round(((m_val - p_val) / m_val) * 100))
                disc_lbl = f"<span class='discount-badge'>{pct}% OFF</span>" if pct > 0 else ""
            except:
                disc_lbl = ""
            st.markdown(f"💰 **Pricing Tiers:** <span class='mrp-strike'>MRP: ₹{int(float(p['mrp']))}</span> <span style='color:#1E293B; font-weight:900; font-size:28px;'>₹{int(float(p['price']))}</span> {disc_lbl}", unsafe_allow_html=True)
        else:
            st.markdown(f"💰 **Pricing Tiers:** **₹{int(float(p['price'])) if p['price'] else 'Contact Sales'}**")
            
        st.markdown("---")
        st.markdown(f"**Description Summary:**\n{p['description']}")
        st.markdown(f"**Technical Specifications:**\n{p['specification']}")
        st.markdown("---")
        
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🛒 Add to My Bulk Inquiry List", key="s_add"):
                st.session_state.cart[p["sku"]] = {"name": p["name"], "qty": 1}
                st.rerun()
        with b2:
            single_msg = f"Hi {COMPANY_NAME}! I want to enquire regarding details for:\n📦 *Product:* {p['name']}\n🆔 *SKU:* {p['sku']}"
            st.link_button("⚡ Instant Order Enquiry", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(single_msg)}", use_container_width=True)
        with b3:
            if st.button("❌ Close Panel View", use_container_width=True):
                st.session_state.selected_product = None
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Filter Processing
filtered_products = []
for p in products:
    if selected_category != "All Categories" and p["category"] != selected_category: continue
    if selected_sub != "All Sub-Categories" and p["subcategory"] != selected_sub: continue
    if search_query:
        q = search_query.lower()
        if not (q in p["name"].lower() or q in p["sku"].lower() or q in p["description"].lower() or q in p["specification"].lower() or q in p["keywords"].lower()):
            continue
    filtered_products.append(p)

# Grid Layout Generation
if not filtered_products:
    st.info("No hydration items matched those metrics.")
else:
    cols = st.columns(3)
    for index, p in enumerate(filtered_products):
        sku = p["sku"]
        name = p["name"]
        img_url = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" and p["images"].strip() != "" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"

        with cols[index % 3]:
            st.markdown('<div class="product-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="bottle-img-container"><img src="{img_url}"></div>', unsafe_allow_html=True)
            
            html_content = f"""
            <div class="details-section">
                <div class="brand-tag">{p['category']} • {p['subcategory']}</div>
                <div class="product-title">{name}</div>
                <div class="by-brand-subscript">by SipAura</div>
                <div class="sku-text">SKU: {sku}</div>
                <div class="preview-spec-container">
                    <span class="spec-pill">🎨 {p['colour']}</span>
                    <span class="spec-pill">📏 {p['capacity']}</span>
                </div>
                <div class="price-container">
            """
            
            if p["mrp"] and p["price"] and str(p["mrp"]).strip() != "None":
                try:
                    mrp_int = int(float(p['mrp']))
                    price_int = int(float(p['price']))
                    pct_val = int(round(((mrp_int - price_int) / mrp_int) * 100))
                    
                    html_content += f"<span class='mrp-strike'>₹{mrp_int}</span>"
                    html_content += f"<span class='listing-price'>₹{price_int}</span>"
                    if pct_val > 0:
                        html_content += f"<span class='discount-badge'>{pct_val}% OFF</span>"
                except:
                    html_content += f"<span class='listing-price'>₹{p['price']}</span>"
            else:
                price_lbl = f"₹{int(float(p['price'])) if isinstance(p['price'], (int,float)) else p['price']}" if p['price'] else "Contact for Quote"
                html_content += f"<span class='listing-price'>{price_lbl}</span>"
                
            html_content += "</div></div>"
            st.markdown(html_content, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔎 View Summary", key=f"v_{sku}_{index}", use_container_width=True):
                    st.session_state.selected_product = p
                    st.rerun()
            with c2:
                if sku in st.session_state.cart:
                    st.markdown(f'<div style="text-align:center; padding-top:6px; font-weight:bold; color:#1E293B;">Added ({st.session_state.cart[sku]["qty"]})</div>', unsafe_allow_html=True)
                else:
                    if st.button("🛒 Add to List", key=f"a_{sku}_{index}", use_container_width=True):
                        st.session_state.cart[sku] = {"name": name, "qty": 1}
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# Inquiry Shopping Cart Footer
if st.session_state.cart:
    st.markdown("---")
    st.markdown('<div style="background-color: #ECFDF5; padding: 20px; border-radius: 14px; border-left: 6px solid #1E293B;">', unsafe_allow_html=True)
    st.markdown("### 🛒 Active Request Inquiry List")
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
        st.write(f"🔹 {item['name']} (Qty: {item['qty']})")
        items_summary_text += f"{idx}. {item['name']} [{sku_id}]\n"
    compiled_message = f"Hi {COMPANY_NAME}! I would love to check stock/orders availability for this selection list:\n\n{items_summary_text}"
    
    cw1, cw2 = st.columns([3, 1])
    with cw1:
        st.link_button("🟢 Send Consolidated List to WhatsApp", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(compiled_message)}", use_container_width=True)
    with cw2:
        if st.button("🗑️ Clear Request List", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
