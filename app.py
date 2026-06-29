import streamlit as st
import pandas as pd
import urllib.parse

COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. High-End Premium CSS to match your reference design
st.markdown("""
    <style>
    /* Premium background color & typography */
    .stApp {
        background-color: #F9FBFC;
    }
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #1E293B !important;
    }
    
    /* Clean, minimalistic product cards */
    .product-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(148, 163, 184, 0.05);
    }
    .product-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(148, 163, 184, 0.12);
        border-color: #CBD5E1;
    }
    
    /* Elegant rounded badges */
    .sku-pill {
        background-color: #F1F5F9;
        color: #64748B;
        font-family: monospace;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 30px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .price-text {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        margin: 8px 0;
    }
    
    /* Modal Summary Overlay style card */
    .summary-card {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        border: 2px solid #25D366;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading Pipeline
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ No Excel file found in your repository branch.")
        st.stop()
        
    target_file = excel_files[0]
    try:
        df = pd.read_excel(target_file, sheet_name=0, engine="openpyxl")
    except Exception as e:
        st.error(f"❌ Read Error: {str(e)}")
        st.stop()
        
    df.columns = df.columns.str.strip()
    
    if "SKU ID" not in df.columns:
        for idx, row in df.iterrows():
            row_vals = row.astype(str).str.strip().values
            if "SKU ID" in row_vals:
                df = pd.read_excel(target_file, sheet_name=0, skiprows=idx+1, engine="openpyxl")
                df.columns = df.columns.str.strip()
                break
                
    if "SKU ID" in df.columns:
        df = df.dropna(subset=["SKU ID"])
    else:
        df = df.dropna(subset=[df.columns[0]])
        
    return df

df = load_data()

# 3. Dynamic Fallback Field Setup
sku_list = df["SKU ID"].astype(str).tolist() if "SKU ID" in df.columns else [f"ITEM-{i}" for i in range(len(df))]
name_col = next((c for c in ["Product Name", "Product Name ", "Product_Name", "Name"] if c in df.columns), None)
name_list = df[name_col].astype(str).tolist() if name_col else [f"Premium Bottle {i+1}" for i in range(len(df))]
cat_list = df["Category"].fillna("Drinkware").astype(str).tolist() if "Category" in df.columns else ["Drinkware"] * len(df)
colour_list = df["Colour"].fillna("Standard").astype(str).tolist() if "Colour" in df.columns else ["Standard"] * len(df)
capacity_list = df["Capacity"].fillna("N/A").astype(str).tolist() if "Capacity" in df.columns else ["N/A"] * len(df)
price_list = df["Selling Price"].fillna("").tolist() if "Selling Price" in df.columns else [""] * len(df)
desc_list = df["Description"].fillna("Premium design option.").astype(str).tolist() if "Description" in df.columns else ["Premium Layout."] * len(df)
spec_list = df["Specification"].fillna("High Grade Insulated Build.").astype(str).tolist() if "Specification" in df.columns else ["High Grade Materials."] * len(df)
keyword_list = df["Key Words"].fillna("").astype(str).tolist() if "Key Words" in df.columns else [""] * len(df)
img_list = df["Images"].fillna("").astype(str).tolist() if "Images" in df.columns else [""] * len(df)

products = []
for i in range(len(df)):
    products.append({
        "sku": sku_list[i], "name": name_list[i], "category": cat_list[i], "colour": colour_list[i],
        "capacity": capacity_list[i], "price": price_list[i], "description": desc_list[i],
        "specification": spec_list[i], "keywords": keyword_list[i], "images": img_list[i]
    })

# 4. State Management (Cart & Selected Preview Product)
if "cart" not in st.session_state: st.session_state.cart = {}
if "selected_product" not in st.session_state: st.session_state.selected_product = None

# WHATSAPP PARAMETERS
YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 PLACE YOUR REAL NUMBER HERE

# 5. Clean Top Navigation Layout
st.title(f"✨ {COMPANY_NAME}")
st.markdown("Select any item to look over its technical highlights or save it right down into your layout inquiry list.")

# 6. DYNAMIC OVERVIEW/SUMMARY BOX (Pops open when a product is clicked)
if st.session_state.selected_product:
    p = st.session_state.selected_product
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        # Pull first available picture for summary view frame
        s_img = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
        st.image(s_img, use_container_width=True)
        
    with col_s2:
        st.markdown(f"## 📋 {p['name']} Summary")
        st.markdown(f"🏷️ **SKU Identification Link:** `{p['sku']}`")
        st.markdown(f"🎨 **Color Variant:** {p['colour']}  |  📏 **Volumetric Size:** {p['capacity']}")
        st.markdown(f"### 💰 Pricing Quote: **₹{p['price'] if p['price'] else 'Contact Sales'}**")
        st.markdown("---")
        st.markdown(f"**Description Summary:**\n{p['description']}")
        st.markdown(f"**Technical Build Specifications:**\n{p['specification']}")
        st.markdown("---")
        
        # Actions inside the summary card view box
        btn_sum1, btn_sum2, btn_sum3 = st.columns(3)
        with btn_sum1:
            if st.button("🛒 Add to Inquiry List", key="sum_add"):
                st.session_state.cart[p["sku"]] = {"name": p["name"], "qty": 1}
                st.rerun()
        with btn_sum2:
            single_msg = f"Hi {COMPANY_NAME}! I want to enquire instantly regarding:\n📦 *Product:* {p['name']}\n🆔 *SKU:* {p['sku']}"
            st.link_button("⚡ Instant WhatsApp Chat", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(single_msg)}", use_container_width=True)
        with btn_sum3:
            if st.button("❌ Close Summary View", use_container_width=True):
                st.session_state.selected_product = None
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 7. Sidebar Filter Controls
search_query = st.sidebar.text_input("🔍 Search Catalog", placeholder="Search items...")
unique_categories = sorted(list(set(cat_list)))
selected_category = st.sidebar.selectbox("📂 Category", ["All Categories"] + unique_categories)

filtered_products = []
for p in products:
    if selected_category != "All Categories" and p["category"] != selected_category: continue
    if search_query:
        q = search_query.lower()
        if not (q in p["name"].lower() or q in p["sku"].lower() or q in p["description"].lower() or q in p["specification"].lower() or q in p["keywords"].lower()):
            continue
    filtered_products.append(p)

# 8. Render Main Core Grid 
if not filtered_products:
    st.info("No hydration items matched those filters.")
else:
    cols = st.columns(3)
    for index, p in enumerate(filtered_products):
        sku = p["sku"]
        name = p["name"]
        price_display = f"₹{p['price']}" if p['price'] and str(p['price']).strip() != "" else "Ask for Quote"
        
        # Images verification checks
        img_url = [img.strip() for img in str(p["images"]).split(",")][0] if p["images"] and p["images"] != "nan" else "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"

        with cols[index % 3]:
            st.markdown('<div class="product-box">', unsafe_allow_html=True)
            st.image(img_url, use_container_width=True)
            st.markdown(f'<div class="product-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="sku-pill">SKU: {sku}</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="price-text">{price_display}</div>', unsafe_allow_html=True)
            
            # Interactive Control Switches
            c1, c2 = st.columns(2)
            with c1:
                # Clicking this launches the top overview summary panel natively
                if st.button("🔎 View Summary", key=f"view_{sku}_{index}", use_container_width=True):
                    st.session_state.selected_product = p
                    st.rerun()
            with c2:
                if sku in st.session_state.cart:
                    st.markdown(f'<div style="text-align:center; padding-top:6px; font-weight:bold; color:#25D366;">Added ({st.session_state.cart[sku]["qty"]})</div>', unsafe_allow_html=True)
                else:
                    if st.button("🛒 Add to List", key=f"add_{sku}_{index}", use_container_width=True):
                        st.session_state.cart[sku] = {"name": name, "qty": 1}
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 9. Active Global Cart Floating Window Summary
if st.session_state.cart:
    st.markdown("---")
    st.markdown('<div style="background-color: #E3FCEF; padding: 20px; border-radius: 14px; border-left: 6px solid #25D366;">', unsafe_allow_html=True)
    st.markdown("### 🛒 Active Inquiry List Ready")
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
        items_summary_text += f"{idx}. {item['name']} [{sku_id}]\n"
    compiled_message = f"Hi {COMPANY_NAME}! I want to check details for these batch list products:\n\n{items_summary_text}"
    
    cw1, cw2 = st.columns([3, 1])
    with cw1:
        st.link_button("🟢 Send Consolidated List to WhatsApp", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(compiled_message)}", use_container_width=True)
    with cw2:
        if st.button("🗑️ Clear Bulk Cart List", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
