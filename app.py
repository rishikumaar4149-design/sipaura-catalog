import streamlit as st
import urllib.parse

COMPANY_NAME = "SipAura"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. Titanium & Silver Jewelry Theme, 4-Column Grid, & Compact Space CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@1,500;1,700&display=swap');
    
    /* Luxury Bright Platinum Studio Background Frame */
    .stApp {
        background-color: #F5F5F7 !important; 
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* -------------------------------------------------- */
    /* FIXED BRUSHED TITANIUM LEFT SIDEBAR PANEL          */
    /* -------------------------------------------------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #202226 0%, #161719 100%) !important; /* Matte Titanium */
        color: #FFFFFF !important;
        position: fixed !important;
        top: 0;
        left: 0;
        width: 23vw !important; /* Slightly leaned layout to allocate more workspace for products */
        height: 100vh !important;
        max-height: 100vh !important; 
        overflow: hidden !important; 
        z-index: 999;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebarUserContent"] {
        display: flex;
        flex-direction: column;
        justify-content: space-between; 
        height: 100vh !important;
        padding: 14px 16px !important;
        box-sizing: border-box;
    }
    
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] label {
        color: #D1D5DB !important;
        font-weight: 500 !important;
        text-align: center !important;
        display: block;
        width: 100%;
        margin-bottom: 2px !important;
        font-size: 13px;
    }
    [data-testid="stSidebar"] .stWidget { margin-bottom: 4px !important; }
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select { text-align: center !important; font-size: 13px !important; }
    
    /* 3D Sterling Silver Rim Logo Frame */
    .sidebar-logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 8px;
        perspective: 1000px;
    }
    .sidebar-logo-container img {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #E5E7EB; /* Sterling Silver Highlight Rim */
        transform: rotateX(6deg) rotateY(-3deg);
        box-shadow: 0 10px 20px rgba(0,0,0,0.35);
    }
    
    /* Jewelry Boutique Intro Box */
    .business-intro-context {
        background-color: #26292E;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 8px;
        border-left: 3px solid #94A3B8; /* Polished Chrome Strip */
    }
    .business-intro-context p {
        font-size: 12px !important;
        line-height: 1.4 !important;
        color: #D1D5DB !important;
        margin: 0 !important;
    }
    
    /* Premium Contact Info Card Layout */
    .premium-contact-card {
        background: linear-gradient(145deg, #26292E, #1A1C1F);
        border: 1px solid #374151;
        border-radius: 14px;
        padding: 12px;
    }
    .contact-title-highlight {
        color: #E5E7EB !important; /* Platinum text highlight */
        font-weight: 700 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px !important;
    }
    .contact-row-entry {
        display: flex;
        align-items: center;
        margin-bottom: 4px;
        font-size: 12.5px;
    }
    .contact-row-entry span {
        color: #9CA3AF !important;
        font-weight: 600;
        width: 60px;
    }
    .contact-row-entry p, .contact-row-entry a { color: #E5E7EB !important; margin: 0 !important; }
    
    .query-call-to-action {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 6px;
        padding: 6px;
        margin-top: 6px;
        font-size: 11px;
        color: #D1D5DB !important;
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
        padding-top: 8px;
    }
    .marquee-scroll-track {
        display: inline-block;
        white-space: nowrap;
        animation: continuousMarquee 15s linear infinite;
    }
    .marquee-text-node {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #525B66 !important;
        padding-right: 40px; 
    }
    
    /* -------------------------------------------------- */
    /* MAIN CATALOG DISPLAY MATRIX (75% CONTAINER SHIFT)  */
    /* -------------------------------------------------- */
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding-top: 20px !important;
        padding-left: 25vw !important; /* Perfectly maps around the 23vw titanium sidebar edge layout */
        padding-right: 25px !important;
    }
    
    /* -------------------------------------------------- */
    /* RECTANGULAR 16:5 LUXURY 3D METALLIC SIGNATURE TEXT  */
    /* -------------------------------------------------- */
    @keyframes strokeWrite {
        to { stroke-dashoffset: 0; }
    }
    @keyframes extrude3D {
        to {
            text-shadow: 
                1px 1px 0px #94A3B8, 2px 2px 0px #94A3B8, 3px 3px 0px #6B7280,
                4px 4px 10px rgba(0,0,0,0.15), 0px 12px 24px rgba(148,163,184,0.15);
            transform: rotateX(8deg) rotateY(-3deg);
        }
    }
    @keyframes subTagFade {
        to { opacity: 0.7; transform: translateY(0); }
    }
    
    .animated-banner-canvas {
        width: 100%;
        background: linear-gradient(135deg, #1A1C1F 0%, #111214 100%); /* Deep Shadow Jewelry Case backdrop */
        border: 1px solid #24282D;
        border-radius: 20px;
        padding: 30px 20px; /* Precise vertical padding compression locks ratio to sleek 16:5 bounds */
        margin-bottom: 25px;
        text-align: center;
        perspective: 1200px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.1);
        box-sizing: border-box;
    }
    
    .signature-path-text {
        font-family: 'Playfair Display', Georgia, serif;
        font-style: italic;
        font-weight: 700;
        font-size: 92px; 
        fill: transparent;
        stroke: #E5E7EB; /* Brilliant Platinum Line */
        stroke-width: 2px;
        stroke-dasharray: 800;
        stroke-dashoffset: 800;
        stroke-linecap: round;
        stroke-linejoin: round;
        display: inline-block;
        animation: 
            strokeWrite 3.5s cubic-bezier(0.4, 0, 0.2, 1) forwards,
            extrude3D 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) 3.3s forwards;
    }
    
    .animated-subtag-banner {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: #94A3B8; /* Polished Silver tracking label subtext */
        letter-spacing: 7px; 
        text-transform: uppercase;
        margin-top: 10px;
        opacity: 0;
        transform: translateY(6px);
        animation: subTagFade 0.8s ease-out 3.8s forwards;
    }
    
    /* -------------------------------------------------- */
    /* ULTRA-COMPACT 4-COLUMN JEWELRY BOX DISPLAY MODULE  */
    /* -------------------------------------------------- */
    .product-box {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        padding: 14px; /* Reduced padding to fit 4 in a row cleanly */
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.01);
        transition: all 0.35s cubic-bezier(0.25, 1, 0.5, 1);
        animation: fadeInUp 0.5s ease-out forwards;
    }
    .product-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 35px rgba(22,23,25,0.06);
        border-color: #94A3B8;
    }
    
    /* Rigid 4:5 Portrait Aspect Ratio Asset Window */
    .bottle-img-container {
        width: 100%;
        position: relative;
        padding-top: 125%; 
        overflow: hidden;
        margin-bottom: 12px;
        border-radius: 12px;
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
        min-height: 165px; /* Compressed content shelf to bring buttons above the fold line */
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .brand-tag {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #9CA3AF;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .product-title {
        font-family: 'Inter', sans-serif;
        font-size: 15px; /* Moderated font scale footprint prevents multi-line overflow errors */
        font-weight: 800;
        color: #111214;
        margin: 2px 0 0px 0;
        line-height: 1.3;
    }
    .by-brand-subscript {
        font-size: 11px;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 4px;
        display: block;
    }
    .sku-text {
        font-family: monospace;
        color: #9CA3AF;
        font-size: 10px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .spec-pill {
        background-color: #F3F4F6;
        color: #374151;
        border: 1px solid #E5E7EB;
        font-size: 10.5px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-right: 4px;
        margin-bottom: 6px;
    }
    
    .price-container {
        margin-top: auto;
        padding-top: 8px;
    }
    .mrp-strike {
        font-size: 12.5px;
        color: #9CA3AF;
        text-decoration: line-through;
        margin-right: 4px;
        font-weight: 500;
    }
    .listing-price {
        font-size: 19px;
        font-weight: 900;
        color: #111214;
        display: inline-block;
    }
    .discount-badge {
        background-color: #374151; /* Premium Dark Silver accent tag badge mapping */
        color: #FFFFFF;
        font-size: 10.5px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
        margin-left: 4px;
    }
    
    /* Titanium Premium Showroom Buttons alignment */
    .stButton>button {
        background-color: #161719 !important; 
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
        padding: 10px 14px !important; /* Compressed margins maximize page alignment specs */
        transition: all 0.25s ease;
    }
    .stButton>button:hover {
        background-color: #4B5563 !important; /* Highlights to platinum slate track sheen */
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .summary-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        border: 2px solid #94A3B8;
        box-shadow: 0 10px 25px rgba(0,0,0,0.02);
        margin-bottom: 25px;
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

# 3. FROZEN SINGLE-PAGE SIDEBAR CONTAINER
LOGO_URL = "https://i.postimg.cc/1t838D2R/logo.jpg"
st.sidebar.markdown(f"""
    <div class="sidebar-logo-container">
        <img src="{LOGO_URL}">
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div class="business-intro-context">
        <p>
            SipAura engineers next-generation temperature-locking luxury drinkware. Every piece blends structural titanium aesthetics with premium ergonomics, transforming daily hydration into an elite active companion.
        </p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔍 Search Master Showroom", placeholder="Search items...")

unique_cats = sorted(list(set([p["category"] for p in products])))
selected_category = st.sidebar.selectbox("📂 Category Collection", ["All Categories"] + unique_cats)

if selected_category != "All Categories":
    unique_subs = sorted(list(set([p["subcategory"] for p in products if p["category"] == selected_category])))
else:
    unique_subs = sorted(list(set([p["subcategory"] for p in products])))
selected_sub = st.sidebar.selectbox("🏷️ Sub-Tier Selection", ["All Sub-Categories"] + unique_subs)

st.sidebar.markdown("""
    <div class="premium-contact-card">
        <div class="contact-title-highlight">📞 Showroom Concierge</div>
        <div class="contact-row-entry">
            <span>💬 Direct:</span>
            <p>+91 93102 34464</p>
        </div>
        <div class="contact-row-entry">
            <span>📧 Inquire:</span>
            <a href="mailto:support@sipaura.com">support@sipaura.com</a>
        </div>
        <div class="query-call-to-action">🙋 Have a custom order request? Feel free to ask your query right now over chat!</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div class="marquee-wrapper-box">
        <div class="marquee-scroll-track">
            <span class="marquee-text-node">💎 Powered by InFlowMart</span>
            <span class="marquee-text-node">💎 Powered by InFlowMart</span>
            <span class="marquee-text-node">💎 Powered by InFlowMart</span>
            <span class="marquee-text-node">💎 Powered by InFlowMart</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. PROCEDURAL HIGH-RESOLUTION SLOW 16:5 WRITING TEXT BANNER
st.markdown("""
    <div class="animated-banner-canvas">
        <svg viewBox="0 0 1000 130" width="100%">
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
            st.markdown(f"💰 **Pricing Tiers:** <span class='mrp-strike'>MRP: ₹{int(float(p['mrp']))}</span> <span style='color:#161719; font-weight:900; font-size:26px;'>₹{int(float(p['price']))}</span> {disc_lbl}", unsafe_allow_html=True)
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

# Grid Layout Generation (LOCKS TO 4 ITEMS IN A SINGLE ROW)
if not filtered_products:
    st.info("No luxury items matched those showroom metrics.")
else:
    cols = st.columns(4) # 👈 FIXED: Force four columns layout structure
    for index, p in enumerate(filtered_products):
        sku = p["sku"]
        name = p["name"]
        img_url = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" and p["images"].strip() != "" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"

        with cols[index % 4]:
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
                if st.button("🔎 View Info", key=f"v_{sku}_{index}", use_container_width=True):
                    st.session_state.selected_product = p
                    st.rerun()
            with c2:
                if sku in st.session_state.cart:
                    st.markdown(f'<div style="text-align:center; padding-top:6px; font-weight:bold; color:#161719; font-size:12px;">Selected ({st.session_state.cart[sku]["qty"]})</div>', unsafe_allow_html=True)
                else:
                    if st.button("🛒 Select", key=f"a_{sku}_{index}", use_container_width=True):
                        st.session_state.cart[sku] = {"name": name, "qty": 1}
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# Inquiry Shopping Cart Footer
if st.session_state.cart:
    st.markdown("---")
    st.markdown('<div style="background-color: #F3F4F6; padding: 20px; border-radius: 14px; border-left: 6px solid #161719;">', unsafe_allow_html=True)
    st.markdown("### 🛒 Showroom Selection Request Summary")
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
        st.write(f"🔹 {item['name']} (Qty: {item['qty']})")
        items_summary_text += f"{idx}. {item['name']} [{sku_id}]\n"
    compiled_message = f"Hi {COMPANY_NAME}! I would love to check showroom availability for this premium product line selection selection:\n\n{items_summary_text}"
    
    cw1, cw2 = st.columns([3, 1])
    with cw1:
        st.link_button("🟢 Request Order Quote via WhatsApp Support", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(compiled_message)}", use_container_width=True)
    with cw2:
        if st.button("🗑️ Clear Selection", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
