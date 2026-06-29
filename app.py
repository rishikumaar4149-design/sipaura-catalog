import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration & Premium Web-App Theme
COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# Premium UI styling modifications
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #F8F9FA;
    }
    /* Grid Product Showcase Cards */
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
    /* Typography Rules */
    .product-title {
        font-size: 22px;
        font-weight: 700;
        color: #1A1A1A;
        margin-top: 10px;
        margin-bottom: 2px;
    }
    .sku-badge {
        font-family: monospace;
        background-color: #E9ECEF;
        padding: 2px 8px;
        border-radius: 4px;
        color: #495057;
        font-size: 12px;
    }
    /* WhatsApp CTA Button Styling */
    .stButton>button {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #128C7E !important;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
    }
    /* Sticky Shopping Cart Header Widget */
    .cart-widget {
        background-color: #E3FCEF;
        padding: 20px;
        border-radius: 14px;
        border-left: 6px solid #25D366;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Optimized Data Loading Engine
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if 'catalogue' in f.lower() and f.endswith('.xlsx')]
    if not excel_files:
        st.error("Data tracking file error. Ensure 'Product catalogue.xlsx' is present.")
        st.stop()
    df = pd.read_excel(excel_files[0], sheet_name="Catalogue", skiprows=4, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["SKU ID"])
    return df

df = load_data()

# Initialize Shopping Cart State
if "cart" not in st.session_state:
    st.session_state.cart = {}

# 3. Sidebar Brand Navigation & Filtering
st.sidebar.markdown(f"## 💎 {COMPANY_NAME}")
st.sidebar.markdown("*Premium Lifestyle Hydration*")
st.sidebar.markdown("---")

# Dynamic AI search checking Titles, Descriptions, Specs, and Keywords
search_query = st.sidebar.text_input("🔍 Search Catalog", placeholder="Search products, keywords, attributes...")

categories = ["All Categories"] + list(df["Category"].dropna().unique())
selected_category = st.sidebar.selectbox("📂 Filter by Category", categories)

sub_cats = ["All Sub-categories"] + list(df["Sub category"].dropna().unique()) if selected_category == "All Categories" else ["All Sub-categories"] + list(df[df["Category"] == selected_category]["Sub category"].dropna().unique())
selected_sub = st.sidebar.selectbox("🏷️ Filter by Sub-Category", sub_cats)

# WHATSAPP NUMBER CONFIGURATION
YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 Keep your real number mapped here

# 4. Search Filtering Pipeline
filtered_df = df.copy()

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["Product Name "].str.lower().str.contains(q, na=False) |
        filtered_df["Description"].str.lower().str.contains(q, na=False) |
        filtered_df["Specification"].str.lower().str.contains(q, na=False) |
        filtered_df["Key Words"].str.lower().str.contains(q, na=False) |
        filtered_df["SKU ID"].str.lower().str.contains(q, na=False)
    ]

if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]
if selected_sub != "All Sub-categories":
    filtered_df = filtered_df[filtered_df["Sub category"] == selected_sub]

# 5. Header Section
st.title(f"🥤 {COMPANY_NAME} Catalog")
st.markdown("Explore our catalog and build your inquiry list. Click the button to dispatch your list natively to our sales team over WhatsApp.")

# 6. Active Multi-Item Inquiry List Widget
if st.session_state.cart:
    st.markdown('<div class="cart-widget">', unsafe_allow_html=True)
    st.markdown("### 🛒 My Inquiry Cart List")
    
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
        st.write(f"🔹 **{item['name']}** ({item['colour']}) — Quantity: **{item['qty']}**")
        items_summary_text += f"{idx}. {item['name']} [{sku_id}] (Qty: {item['qty']} | Color: {item['colour']})\n"
        
    compiled_message = f"Hi {COMPANY_NAME}! I was browsing your professional digital storefront and want to check stock/pricing for the following list of items:\n\n{items_summary_text}"
    encoded_message = urllib.parse.quote(compiled_message)
    bulk_whatsapp_url = f"https://wa.me/{YOUR_PHONE_NUMBER}?text={encoded_message}"
    
    col_w1, col_w2 = st.columns([3, 1])
    with col_w1:
        st.link_button("🟢 Submit Bulk Inquiry List via WhatsApp", bulk_whatsapp_url, use_container_width=True)
    with col_w2:
        if st.button("🗑️ Clear List", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# 7. Rendering Clean Functional Grid UI
if filtered_df.empty:
    st.info("No hydration items match your active filters. Try restructuring your query fields.")
else:
    cols = st.columns(3)
    for index, row in filtered_df.reset_index().iterrows():
        sku = row.get("SKU ID", "N/A")
        name = row.get("Product Name ", "Premium Drinkware")
        capacity = row.get("Capacity", "N/A")
        colour = row.get("Colour", "N/A")
        price = row.get("Selling Price")
        price_display = f"₹{price}" if pd.notna(price) and str(price).strip() != "" else "Contact for Price"
        
        # New text entries from your spreadsheet updates
        description = row.get("Description")
        if pd.isna(description) or str(description).strip() == "":
            description = "Premium lightweight double-wall insulated construction flask built for lifestyle execution."
            
        specification = row.get("Specification")
        if pd.isna(specification) or str(specification).strip() == "":
            specification = "Grade 304 Stainless Steel | Sweat-Proof Matte Outer Layout | Cold up to 24 hrs / Hot up to 12 hrs"

        # Image mapping structure (Comma split architecture fallback)
        img_column_data = row.get("Images") if "Images" in row else None
        if pd.isna(img_column_data) or str(img_column_data).strip() == "":
            images_list = ["https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"]
        else:
            images_list = [img.strip() for img in str(img_column_data).split(",")]

        with cols[index % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            # Interactive Image Tabs Gallery
            if len(images_list) == 1:
                st.image(images_list[0], use_container_width=True)
            else:
                img_tabs = st.tabs([f"📸 View {i+1}" for i in range(len(images_list))])
                for i, url in enumerate(images_list):
                    with img_tabs[i]:
                        st.image(url, use_container_width=True)
            
            st.markdown(f'<div class="product-title">{name}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="sku-badge">SKU: {sku}</span>', unsafe_allow_html=True)
            st.markdown(f"### {price_display}")
            
            # Professional Tabs for clean distribution of information
            info_tab1, info_tab2 = st.tabs(["📋 Overview", "🔧 Specifications"])
            
            with info_tab1:
                st.write(f"🎨 **Color Attributes:** {colour}")
                st.write(f"📐 **Volume Capacity:** {capacity}")
                st.caption(description)
                
            with info_tab2:
                st.markdown(f"*{specification}*")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Transaction Actions
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if sku in st.session_state.cart:
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
                st.link_button("⚡ Quick Inquiry", single_wa_url, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)
