import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration & Premium Theme Engine
COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# Premium UI Custom Styling Rules
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
    }
    .product-card {
        padding: 24px;
        border-radius: 16px;
        background-color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #E9ECEF;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    }
    .product-title {
        font-size: 20px;
        font-weight: 700;
        color: #1A1A1A;
        margin-top: 10px;
        margin-bottom: 4px;
        line-height: 1.3;
    }
    .sku-badge {
        font-family: monospace;
        background-color: #E9ECEF;
        padding: 3px 8px;
        border-radius: 4px;
        color: #495057;
        font-size: 11px;
        font-weight: bold;
    }
    .category-pill {
        background-color: #E8F0FE;
        color: #1A73E8;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 20px;
        margin-left: 5px;
    }
    .stButton>button {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
    }
    .stButton>button:hover {
        background-color: #128C7E !important;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
    }
    .qty-display {
        background-color: #F1F3F5;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        font-weight: bold;
        color: #212529;
    }
    .cart-widget {
        background-color: #E3FCEF;
        padding: 20px;
        border-radius: 14px;
        border-left: 6px solid #25D366;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Resilient Data Loading Pipeline
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ Error: No Excel file (.xlsx) found in your repository.")
        st.stop()
    
    target_file = excel_files[0]
    df = pd.read_excel(target_file, sheet_name=0, skiprows=4, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["SKU ID"])
    return df

df = load_data()

# Initialize Multi-Item Inquiry Cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

# 3. Sidebar Filtering & AI Search Parameters
st.sidebar.markdown(f"## 💎 {COMPANY_NAME}")
st.sidebar.markdown("*Premium Lifestyle Hydration*")
st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔍 Smart Search Catalog", placeholder="Search items, keywords, travel, office...")

categories = ["All Categories"] + list(df["Category"].dropna().unique())
selected_category = st.sidebar.selectbox("📂 Category Group", categories)

sub_cats = ["All Sub-categories"] + list(df["Sub category"].dropna().unique()) if selected_category == "All Categories" else ["All Sub-categories"] + list(df[df["Category"] == selected_category]["Sub category"].dropna().unique())
selected_sub = st.sidebar.selectbox("🏷️ Sub-Category Style", sub_cats)

# WHATSAPP INQUIRY REDIRECTION CONFIGURATION
YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 PLACE YOUR REAL WHATSAPP NUMBER HERE

# 4. Search Filter Strategy
filtered_df = df.copy()

name_col = "Product Name" if "Product Name" in filtered_df.columns else "Product Name "

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df[name_col].str.lower().str.contains(q, na=False) |
        filtered_df["Description"].str.lower().str.contains(q, na=False) |
        filtered_df["Specification"].str.lower().str.contains(q, na=False) |
        filtered_df["Key Words"].str.lower().str.contains(q, na=False) |
        filtered_df["SKU ID"].str.lower().str.contains(q, na=False)
    ]

if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]
if selected_sub != "All Sub-categories":
    filtered_df = filtered_df[filtered_df["Sub category"] == selected_sub]

# 5. Application View Layout
st.title(f"🥤 {COMPANY_NAME}")
st.markdown("Browse our catalog. Add multiple items to build an inquiry list, then dispatch it seamlessly to WhatsApp.")

# 6. Active Inquiry Cart Widget Render
if st.session_state.cart:
    st.markdown('<div class="cart-widget">', unsafe_allow_html=True)
    st.markdown("### 🛒 My Current Inquiry List")
    
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
        st.write(f"🔹 **{item['name']}** ({item['colour']}) — Qty: **{item['qty']}**")
        items_summary_text += f"{idx}. {item['name']} [{sku_id}] (Qty: {item['qty']} | Color: {item['colour']})\n"
        
    compiled_message = f"Hi {COMPANY_NAME}! I am reviewing your digital catalog link and would love to check availability/pricing for these items:\n\n{items_summary_text}"
    encoded_message = urllib.parse.quote(compiled_message)
    bulk_whatsapp_url = f"https://wa.me/{YOUR_PHONE_NUMBER}?text={encoded_message}"
    
    col_w1, col_w2 = st.columns([3, 1])
    with col_w1:
        st.link_button("🟢 Submit Order Inquiry to WhatsApp", bulk_whatsapp_url, use_container_width=True)
    with col_w2:
        if st.button("🗑️ Clear List", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# 7. Main Core Grid
if filtered_df.empty:
    st.info("No drinkware items found matching these tracking targets.")
else:
    cols = st.columns(3)
    for index, row in filtered_df.reset_index().iterrows():
        sku = row.get("SKU ID", "N/A")
        name = row.get(name_col, "Premium Drinkware")
        capacity = row.get("Capacity", "N/A")
        colour = row.get("Colour", "N/A")
        cat_label = row.get("Category", "Drinkware")
        price = row.get("Selling Price")
        price_display = f"₹{price}" if pd.notna(price) and str(price).strip() != "" else "Contact for Quote"
        
        description = row.get("Description")
        if pd.isna(description) or str(description).strip() == "":
            description = "Premium lightweight double-walled design optimized for travel insulation layout."
            
        specification = row.get("Specification")
        if pd.isna(specification) or str(specification).strip() == "":
            specification = "Grade 304 Stainless Steel | Thermal Insulation Hot & Cold Travel Companion."

        # Comma-split dynamic multiple image gallery support
        img_column_data = row.get("Images") if "Images" in row else None
        if pd.isna(img_column_data) or str(img_column_data).strip() == "":
            images_list = ["https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"]
        else:
            images_list = [img.strip() for img in str(img_column_data).split(",")]

        with cols[index % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            # Slide Gallery Renderer Tabs
            if len(images_list) == 1:
                st.image(images_list[0], use_container_width=True)
            else:
                img_tabs = st.tabs([f"📸 View {i+1}" for i in range(len(images_list))])
                for i, url in enumerate(images_list):
                    with img_tabs[i]:
                        st.image(url, use_container_width=True)
            
            st.markdown(f'<div class="product-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="sku-badge">SKU: {sku}</span><span class="category-pill">{cat_label}</span>', unsafe_allow_html=True)
            st.markdown(f"### {price_display}")
            
            # Nested Tabs Layout for Clean Overview
            tab_overview, tab_specs = st.tabs(["📋 Overview", "🔧 Technical Specs"])
            with tab_overview:
                st.write(f"🎨 **Color Spec:** {colour}")
                st.write(f"📏 **Volume Capacity:** {capacity}")
                st.caption(description)
            with tab_specs:
                st.markdown(f"*{specification}*")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Interactive Action Triggers
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if sku in st.session_state.cart:
                    current_qty = st.session_state.cart[sku]["qty"]
                    # Sub-layout grid to change quantity cleanly or add more
                    q_col1, q_col2 = st.columns([1, 1])
                    with q_col1:
                        st.markdown(f'<div class="qty-display">Selected: {current_qty}</div>', unsafe_allow_html=True)
                    with q_col2:
                        if st.button("➕ Add More", key=f"inc_{sku}_{index}"):
                            st.session_state.cart[sku]["qty"] += 1
                            st.rerun()
                else:
                    if st.button("🛒 Add to List", key=f"add_{sku}_{index}"):
                        st.session_state.cart[sku] = {"name": name, "colour": colour, "qty": 1}
                        st.rerun()
                        
            with btn_col2:
                single_msg = f"Hi {COMPANY_NAME}! I want to instantly check availability for:\n\n" \
                             f"📦 *Product:* {name}\n" \
                             f"🆔 *SKU:* {sku}\n" \
                             f"🎨 *Colour:* {colour}\n" \
                             f"📏 *Capacity:* {capacity}"
                encoded_single = urllib.parse.quote(single_msg)
                single_wa_url = f"https://wa.me/{YOUR_PHONE_NUMBER}?text={encoded_single}"
                st.link_button("⚡ Quick Buy", single_wa_url, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
