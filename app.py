import streamlit as st
import pandas as pd
import urllib.parse

COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. Premium UI & E-Commerce Animation Stylesheet
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    /* Intro Banner Design Box */
    .intro-banner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: #FFFFFF !important;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1);
    }
    /* E-Commerce Minimal Product Box */
    .product-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.02);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out forwards;
    }
    .product-box:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.08);
        border-color: #CBD5E1;
    }
    .product-title {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #1E293B;
        margin-top: 10px;
        margin-bottom: 4px;
        line-height: 1.4;
        min-height: 52px;
    }
    .sku-pill {
        background-color: #F1F5F9;
        color: #475569;
        font-family: monospace;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 30px;
        display: inline-block;
        margin-bottom: 12px;
    }
    /* Amazon & Flipkart Specific Pricing Schema */
    .mrp-strike {
        font-size: 14px;
        color: #94A3B8;
        text-decoration: line-through;
        margin-right: 6px;
    }
    .listing-price {
        font-size: 22px;
        font-weight: 800;
        color: #212529;
        display: inline-block;
    }
    .discount-badge {
        background-color: #25D366;
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-left: 8px;
        vertical-align: middle;
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
    /* Footer Style */
    .footer-credit {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Dynamic Structural Data Pipeline
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ No Excel data file detected in repository.")
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

# WHATSAPP NUMBER CONFIGURATION
YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 PLACE YOUR REAL NUMBER HERE

# 3. Sidebar Filtering, Contact Fields & Powered By InFlowMart
st.sidebar.markdown(f"## 💎 {COMPANY_NAME}")
st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔍 Smart Search Catalog", placeholder="Search products...")

# Categories & Subcategories Logic
unique_cats = sorted(list(set([p["category"] for p in products])))
selected_category = st.sidebar.selectbox("📂 Category", ["All Categories"] + unique_cats)

if selected_category != "All Categories":
    unique_subs = sorted(list(set([p["subcategory"] for p in products if p["category"] == selected_category])))
else:
    unique_subs = sorted(list(set([p["subcategory"] for p in products])))
selected_sub = st.sidebar.selectbox("🏷️ Sub-Category", ["All Sub-Categories"] + unique_subs)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Contact Information")
st.sidebar.markdown("💬 **WhatsApp:** +91 XXXXX XXXXX")
st.sidebar.markdown("📧 **Email:** support@sipaura.com")
st.sidebar.markdown("🌐 **Location:** India Office")

# LOWER LEFT CORNER BRANDING ATTRIBUTION
st.sidebar.markdown('<div class="footer-credit">⚡ Powered by InFlowMart</div>', unsafe_allow_html=True)

# 4. Main Window Content Showcase
st.markdown(f"""
    <div class="intro-banner">
        <h1 style="color: white !important; margin-bottom: 8px;">Welcome to {COMPANY_NAME}</h1>
        <p style="font-size: 16px; opacity: 0.9; margin: 0;">
            Discover our premium range of high-performance insulated lifestyle drinkware, fitness shakers, and flasks. 
            Engineered to keep your beverages temperature-locked while complementing your active lifestyle day after day.
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
        st.markdown(f"## 📋 {p['name']}")
        st.markdown(f'<span class="sku-pill">SKU: {p["sku"]}</span>', unsafe_allow_html=True)
        st.markdown(f"🎨 **Color Variant:** {p['colour']} | 📏 **Capacity Size:** {p['capacity']}")
        
        # Format clean percentage calculation metrics in description block view
        if p["mrp"] and p["price"]:
            try:
                pct = int(round(p['discount'])) if p['discount'] else int(round(((p['mrp'] - p['price']) / p['mrp']) * 100))
                disc_lbl = f"<span class='discount-badge'>{pct}% OFF</span>"
            except:
                disc_lbl = ""
            st.markdown(f"💰 **Price Matrix:** <span class='mrp-strike'>MRP: ₹{int(float(p['mrp']))}</span> <span style='color:#10B981; font-weight:800; font-size:26px;'>₹{int(float(p['price']))}</span> {disc_lbl}", unsafe_allow_html=True)
        else:
            st.markdown(f"💰 **Price Matrix:** **₹{p['price'] if p['price'] else 'Contact Sales'}**")
            
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
            st.markdown(f'<div class="product-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="sku-pill">SKU: {sku}</span>', unsafe_allow_html=True)
            
            # --- RENDER NEW PRICE STRUCTURAL COMPONENT TO AMAZON/FLIPKART TIERS ---
            st.markdown('<div style="margin: 4px 0 16px 0; line-height:1.2;">', unsafe_allow_html=True)
            if p["mrp"] and p["price"] and str(p["mrp"]).strip() != "None":
                try:
                    mrp_int = int(float(p['mrp']))
                    price_int = int(float(p['price']))
                    pct_val = int(round(float(p['discount']))) if p['discount'] and p['discount'] != 'nan' else int(round(((mrp_int - price_int) / mrp_int) * 100))
                    
                    st.markdown(f"<span class='mrp-strike'>₹{mrp_int}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='listing-price'>₹{price_int}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='discount-badge'>{pct_val}% OFF</span>", unsafe_allow_html=True)
                except:
                    st.markdown(f"<span class='listing-price'>₹{p['price']}</span>", unsafe_allow_html=True)
            else:
                price_lbl = f"₹{int(float(p['price'])) if isinstance(p['price'], (int,float)) else p['price']}" if p['price'] else "Contact for Quote"
                st.markdown(f"<span class='listing-price'>{price_lbl}</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
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
