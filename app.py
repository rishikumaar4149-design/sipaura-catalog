import streamlit as st
import pandas as pd
import urllib.parse

COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. Premium UI & Animation CSS Stylesheet
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

# 2. Resilient Data Pipeline
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ No Excel data file detected in repository.")
        st.stop()
        
    target_file = excel_files[0]
    df = pd.read_excel(target_file, sheet_name=0, engine="openpyxl")
    df.columns = df.columns.str.strip()
    
    if "SKU ID" not in df.columns:
        for idx, row in df.iterrows():
            if "SKU ID" in row.astype(str).str.strip().values:
                df = pd.read_excel(target_file, sheet_name=0, skiprows=idx+1, engine="openpyxl")
                df.columns = df.columns.str.strip()
                break
                
    df = df.dropna(subset=[df.columns[0]])
    return df

df = load_data()

# 3. Dynamic Flexible Column Name Normalization
def find_column(df, choices):
    for c in choices:
        match = [col for col in df.columns if col.lower() == c.lower()]
        if match: return match[0]
    return None

sku_col = find_column(df, ["SKU ID", "sku"])
name_col = find_column(df, ["Product Name", "Product Name ", "Name"])
cat_col = find_column(df, ["Category"])
colour_col = find_column(df, ["Colour", "Color"])
cap_col = find_column(df, ["Capacity"])
desc_col = find_column(df, ["Description"])
spec_col = find_column(df, ["Specification", "Specifications"])
kw_col = find_column(df, ["Key Words", "Keywords"])
img_col = find_column(df, ["Images", "Image Link"])

mrp_col = find_column(df, ["MRP", "Cost Price"])
discount_col = find_column(df, ["Discount", "Discount %"])
final_col = find_column(df, ["Final Listing Price", "Selling Price", "Price"])

products = []
for idx, row in df.iterrows():
    sku_val = str(row[sku_col]) if sku_col else f"SKU-{idx}"
    if pd.isna(row[sku_col]): continue
    
    products.append({
        "sku": sku_val,
        "name": str(row[name_col]) if name_col else "Premium Item",
        "category": str(row[cat_col]) if cat_col else "Drinkware",
        "colour": str(row[colour_col]) if colour_col else "Standard",
        "capacity": str(row[cap_col]) if cap_col else "N/A",
        "description": str(row[desc_col]) if desc_col and pd.notna(row[desc_col]) else "Premium insulated build companion architecture.",
        "specification": str(row[spec_col]) if spec_col and pd.notna(row[spec_col]) else "High Quality Structural Build.",
        "keywords": str(row[kw_col]) if kw_col else "",
        "images": str(row[img_col]) if img_col else "",
        "mrp": row[mrp_col] if mrp_col else None,
        "discount": row[discount_col] if discount_col else None,
        "price": row[final_col] if final_col else None
    })

if "cart" not in st.session_state: st.session_state.cart = {}
if "selected_product" not in st.session_state: st.session_state.selected_product = None

YOUR_PHONE_NUMBER = "919821352868"  # 👈 REPLACE WITH YOUR STORE PHONE NUMBER

# 4. View Header
st.title(f"✨ {COMPANY_NAME}")
st.markdown("Explore our refreshed premium collection with updated retail pricing tiers below.")

# 5. Summary View Box Interface
if st.session_state.selected_product:
    p = st.session_state.selected_product
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        s_img = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
        st.image(s_img, use_container_width=True)
    with col_s2:
        st.markdown(f"## 📋 {p['name']} Summary Overview")
        st.markdown(f'<span class="sku-pill">SKU: {p["sku"]}</span>', unsafe_allow_html=True)
        st.markdown(f"🎨 **Color Attributes:** {p['colour']}  |  📏 **Capacity:** {p['capacity']}")
        
        if pd.notna(p["mrp"]):
            disc_text = f" ({p['discount']} OFF)" if pd.notna(p['discount']) else ""
            st.markdown(f"💰 **Pricing Model:** <span class='mrp-strike'>₹{p['mrp']}</span> <span style='color:#10B981; font-weight:bold; font-size:20px;'>₹{p['price']}</span> <span style='font-size:14px; color:#16803D;'>{disc_text}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"💰 **Pricing Model:** **₹{p['price'] if p['price'] else 'Contact Sales'}**")
            
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

# 6. Sidebar Filtration Tools
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
        
        img_url = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"

        with cols[index % 3]:
            st.markdown('<div class="product-box">', unsafe_allow_html=True)
            st.image(img_url, use_container_width=True)
            st.markdown(f'<div class="product-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="sku-pill">SKU: {sku}</span>', unsafe_allow_html=True)
            
            st.markdown('<div style="margin: 12px 0 4px 0;">', unsafe_allow_html=True)
            if pd.notna(p["mrp"]) and str(p["mrp"]).strip() != "":
                st.markdown(f"<span class='mrp-strike'>₹{p['mrp']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='listing-price'>₹{p['price']}</span>", unsafe_allow_html=True)
                if pd.notna(p["discount"]) and str(p["discount"]).strip() != "":
                    st.markdown(f"<span class='discount-badge'>⚡ {p['discount']} OFF</span>", unsafe_allow_html=True)
            else:
                price_lbl = f"₹{p['price']}" if p['price'] else "Contact for Quote"
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
