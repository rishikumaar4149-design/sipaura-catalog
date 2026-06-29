import streamlit as st
import pandas as pd
import urllib.parse

COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. Premium E-Commerce Layout & Spacing CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .company-header {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        letter-spacing: -1.5px;
        background: linear-gradient(to right, #1E293B, #475569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .intro-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF !important;
        border-radius: 28px;
        padding: 35px;
        margin-bottom: 35px;
        box-shadow: 0 12px 30px -10px rgba(15, 23, 42, 0.15);
    }
    
    /* Perfected Product Box Structure */
    .product-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 22px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.015);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out forwards;
    }
    .product-box:hover {
        transform: translateY(-6px);
        box-shadow: 0 25px 35px -10px rgba(15, 23, 42, 0.12);
        border-color: #CBD5E1;
    }
    
    /* Unified Details Section to Stop Overlapping */
    .details-section {
        min-height: 160px; /* Forces equal height for all columns */
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
        margin: 4px 0;
        line-height: 1.3;
    }
    .sku-text {
        font-family: monospace;
        color: #64748B;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    /* Inline specs style formatting */
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
    
    /* Flipkart & Amazon Custom Pricing */
    .price-container {
        margin-top: auto; /* Aligns price to the bottom of details container */
        padding-top: 10px;
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
        background-color: #10B981 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }
    .stButton>button:hover {
        background-color: #059669 !important;
    }
    .summary-card {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        border: 2px solid #10B981;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        margin-bottom: 30px;
    }
    .footer-credit {
        font-size: 11px;
        color: #94A3B8;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 60px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Resilient Auto-Parsing Excel Pipeline
@st.cache_data
def load_data():
    import os
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

YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 REPLACE WITH YOUR ACTUAL WHATSAPP NUMBER HERE

# 3. Sidebar Filtering & Branding Configuration
st.sidebar.markdown(f'<h1 style="font-size:24px; font-weight:800; margin:0; color:#1E293B;">💎 {COMPANY_NAME}</h1>', unsafe_allow_html=True)
st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔍 Smart Search Catalog", placeholder="Search items...")

unique_cats = sorted(list(set([p["category"] for p in products])))
selected_category = st.sidebar.selectbox("📂 Category", ["All Categories"] + unique_cats)

if selected_category != "All Categories":
    unique_subs = sorted(list(set([p["subcategory"] for p in products if p["category"] == selected_category])))
else:
    unique_subs = sorted(list(set([p["subcategory"] for p in products])))
selected_sub = st.sidebar.selectbox("🏷️ Sub-Category", ["All Sub-Categories"] + unique_subs)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Contact Information")
st.sidebar.markdown("💬 **WhatsApp Support:** +91 XXXXX XXXXX")
st.sidebar.markdown("📧 **Email Channels:** support@sipaura.com")

st.sidebar.markdown('<div class="footer-credit">Powered by InFlowMart</div>', unsafe_allow_html=True)

# 4. Main Banner
st.markdown(f'<h1 class="company-header">{COMPANY_NAME} Official</h1>', unsafe_allow_html=True)
st.markdown(f"""
    <div class="intro-banner">
        <p style="font-size: 16px; opacity: 0.95; margin: 0; font-family:'Inter', sans-serif; font-weight:500; line-height:1.5;">
            Discover our premium collection of high-performance insulated lifestyle drinkware, fitness shakers, and luxury flasks. 
            Engineered to keep your beverages temperature-locked while complementing your active workspace lifestyle day after day.
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. Interactive Details Preview Block Panel Drawer
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
            st.markdown(f"💰 **Pricing Tiers:** <span class='mrp-strike'>MRP: ₹{int(float(p['mrp']))}</span> <span style='color:#10B981; font-weight:900; font-size:28px;'>₹{int(float(p['price']))}</span> {disc_lbl}", unsafe_allow_html=True)
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

# 6. Apply Filter Pipelines
filtered_products = []
for p in products:
    if selected_category != "All Categories" and p["category"] != selected_category: continue
    if selected_sub != "All Sub-Categories" and p["subcategory"] != selected_sub: continue
    if search_query:
        q = search_query.lower()
        if not (q in p["name"].lower() or q in p["sku"].lower() or q in p["description"].lower() or q in p["specification"].lower() or q in p["keywords"].lower()):
            continue
    filtered_products.append(p)

# 7. Products Show Grid Rendering
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
            st.image(img_url, use_container_width=True)
            
            # Encapsulated Text Details Box to Protect Layout Alignment
            html_content = f"""
            <div class="details-section">
                <div class="brand-tag">{p['category']} • {p['subcategory']}</div>
                <div class="product-title">{name}</div>
                <div class="sku-text">SKU: {sku}</div>
                <div class="preview-spec-container">
                    <span class="spec-pill">🎨 {p['colour']}</span>
                    <span class="spec-pill">📏 {p['capacity']}</span>
                </div>
                <div class="price-container">
            """
            
            # Dynamic Price Integer Logic Block
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
                    st.markdown(f'<div style="text-align:center; padding-top:6px; font-weight:bold; color:#10B981;">Added ({st.session_state.cart[sku]["qty"]})</div>', unsafe_allow_html=True)
                else:
                    if st.button("🛒 Add to List", key=f"a_{sku}_{index}", use_container_width=True):
                        st.session_state.cart[sku] = {"name": name, "qty": 1}
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 8. Global Active Cart Display Footer
if st.session_state.cart:
    st.markdown("---")
    st.markdown('<div style="background-color: #ECFDF5; padding: 20px; border-radius: 14px; border-left: 6px solid #10B981;">', unsafe_allow_html=True)
    st.markdown("### 🛒 Active Request Inquiry List")
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
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
