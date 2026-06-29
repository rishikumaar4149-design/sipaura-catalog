import streamlit as st
import pandas as pd
import urllib.parse

COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. Premium UI Styling & Animations
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .product-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
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
        font-size: 19px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 12px;
        margin-bottom: 4px;
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
    }
    .mrp-strike {
        font-size: 14px;
        color: #94A3B8;
        text-decoration: line-through;
        margin-right: 8px;
    }
    .listing-price {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        display: inline-block;
    }
    .discount-badge {
        background-color: #DCFCE7;
        color: #15803D;
        font-size: 12px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 8px;
        display: inline-block;
        margin-left: 10px;
    }
    .stButton>button {
        background-color: #10B981 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #059669 !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    .summary-card {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        border: 2px solid #10B981;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        margin-bottom: 30px;
        animation: fadeInUp 0.3s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Hardened Data Engine
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ No Excel data file detected in repository.")
        st.stop()
        
    target_file = excel_files[0]
    
    # Force search row by row to find where headers start natively
    raw_df = pd.read_excel(target_file, sheet_name=0, engine="openpyxl")
    header_row = 0
    for idx, row in raw_df.iterrows():
        if "sku id" in row.astype(str).str.strip().str.lower().values:
            header_row = idx + 1
            break
            
    # Load sheet precisely aligned with the discovered header row
    df = pd.read_excel(target_file, sheet_name=0, skiprows=header_row, engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Helper function to grab columns regardless of trailing spaces
def get_clean_col(dataframe, keys, default=""):
    for k in keys:
        match = [c for c in dataframe.columns if c.lower().strip() == k.lower().strip()]
        if match:
            return dataframe[match[0]]
    return pd.Series([default] * len(dataframe))

# Safe Column Mapping
sku_s = get_clean_col(df, ["SKU ID", "sku"])
name_s = get_clean_col(df, ["Product Name", "Name"])
cat_s = get_clean_col(df, ["Category"]).fillna("Drinkware")
sub_s = get_clean_col(df, ["Sub category", "Subcategory"]).fillna("General")
cap_s = get_clean_col(df, ["Capacity"]).fillna("N/A")
col_s = get_clean_col(df, ["Colour", "Color"]).fillna("Standard")
mrp_s = get_clean_col(df, ["MRP"])
disc_s = get_clean_col(df, ["Discount"])
price_s = get_clean_col(df, ["Final Price", "Final Listing Price", "Selling Price", "Cost Price"])
desc_s = get_clean_col(df, ["Description"]).fillna("Premium hydration gear.")
spec_s = get_clean_col(df, ["Specification", "Specifications"]).fillna("Premium insulated build.")
kw_s = get_clean_col(df, ["Key Words", "Keywords"]).fillna("")
img_s = get_clean_col(df, ["Images", "Image Link"]).fillna("")

products = []
for i in range(len(df)):
    if pd.isna(sku_s.iloc[i]) or str(sku_s.iloc[i]).strip() == "nan":
        continue
    products.append({
        "sku": str(sku_s.iloc[i]),
        "name": str(name_s.iloc[i]),
        "category": str(cat_s.iloc[i]),
        "subcategory": str(sub_s.iloc[i]),
        "capacity": str(cap_s.iloc[i]),
        "colour": str(col_s.iloc[i]),
        "mrp": mrp_s.iloc[i] if pd.notna(mrp_s.iloc[i]) else None,
        "discount": str(disc_s.iloc[i]) if pd.notna(disc_s.iloc[i]) else None,
        "price": price_s.iloc[i] if pd.notna(price_s.iloc[i]) else None,
        "description": str(desc_s.iloc[i]),
        "specification": str(spec_s.iloc[i]),
        "keywords": str(kw_s.iloc[i]),
        "images": str(img_s.iloc[i])
    })

if "cart" not in st.session_state: st.session_state.cart = {}
if "selected_product" not in st.session_state: st.session_state.selected_product = None

YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 MAKE SURE YOUR REAL WHATSAPP NUMBER IS PASSED HERE

# 4. App Main Layout Headers
st.title(f"✨ {COMPANY_NAME}")
st.markdown("Explore our refreshed premium collection with updated retail pricing tiers below.")

# 5. Summary View Box Interface Drawer Panel
if st.session_state.selected_product:
    p = st.session_state.selected_product
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        s_img = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" and p["images"].strip() != "" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
        st.image(s_img, use_container_width=True)
    with col_s2:
        st.markdown(f"## 📋 {p['name']} Summary Overview")
        st.markdown(f'<span class="sku-pill">SKU: {p["sku"]}</span>', unsafe_allow_html=True)
        st.markdown(f"🎨 **Color Attributes:** {p['colour']}  |  📏 **Capacity:** {p['capacity']}")
        
        if p["mrp"]:
            disc_text = f" ({p['discount']} OFF)" if p['discount'] and p['discount'] != "nan" else ""
            st.markdown(f"💰 **Pricing Model:** <span class='mrp-strike'>₹{p['mrp']}</span> <span style='color:#10B981; font-weight:bold; font-size:24px;'>₹{p['price']}</span> <span style='font-size:14px; color:#15803D; font-weight:bold;'>{disc_text}</span>", unsafe_allow_html=True)
        else:
            price_lbl = f"₹{p['price']}" if p['price'] else "Contact Sales"
            st.markdown(f"💰 **Pricing Model:** **{price_lbl}**")
            
        st.markdown("---")
        st.markdown(f"**Detailed Information Summary:**\n{p['description']}")
        st.markdown(f"**Technical Build Specifications:**\n{p['specification']}")
        st.markdown("---")
        
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🛒 Add to My Bulk List", key="s_add"):
                st.session_state.cart[p["sku"]] = {"name": p["name"], "qty": 1}
                st.rerun()
        with b2:
            single_msg = f"Hi {COMPANY_NAME}! I want to enquire regarding pricing for:\n📦 *Product:* {p['name']}\n🆔 *SKU:* {p['sku']}"
            st.link_button("⚡ Instant Order Enquiry", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(single_msg)}", use_container_width=True)
        with b3:
            if st.button("❌ Close View Frame", use_container_width=True):
                st.session_state.selected_product = None
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 6. Sidebar Filters
search_query = st.sidebar.text_input("🔍 Premium Smart Search", placeholder="Search categories, items...")
unique_cats = sorted(list(set([p["category"] for p in products])))
selected_category = st.sidebar.selectbox("📂 Category", ["All Categories"] + unique_cats)

filtered_products = []
for p in products:
    if selected_category != "All Categories" and p["category"] != selected_category: continue
    if search_query:
        q = search_query.lower()
        if not (q in p["name"].lower() or q in p["sku"].lower() or q in p["description"].lower() or q in p["specification"].lower() or q in p["keywords"].lower()):
            continue
    filtered_products.append(p)

# 7. Products Show Grid Rendering
if not filtered_products:
    st.info("No drinkware units matched those filters.")
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
            
            st.markdown('<div style="margin: 12px 0 4px 0;">', unsafe_allow_html=True)
            if p["mrp"] and str(p["mrp"]).strip() != "None":
                st.markdown(f"<span class='mrp-strike'>₹{int(float(p['mrp'])) if isinstance(p['mrp'], (int, float)) else p['mrp']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='listing-price'>₹{int(float(p['price'])) if isinstance(p['price'], (int, float)) else p['price']}</span>", unsafe_allow_html=True)
                if p["discount"] and p["discount"] != "nan" and str(p["discount"]).strip() != "":
                    st.markdown(f"<span class='discount-badge'>⚡ {p['discount']} OFF</span>", unsafe_allow_html=True)
            else:
                price_lbl = f"₹{int(float(p['price'])) if isinstance(p['price'], (int, float)) else p['price']}" if p['price'] else "Contact for Quote"
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
    st.markdown("### 🛒 Active Request List Details")
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
