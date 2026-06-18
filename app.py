import streamlit as st
import pandas as pd
import urllib.parse

# 1. Page Config
COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 2. Advanced Premium CSS Styling
st.markdown("""
    <style>
    /* Main Background & Clean Typography */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Elegant Product Cards */
    .product-card {
        padding: 20px;
        border-radius: 16px;
        background-color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        border: 1px solid #F1F3F5;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    
    /* WhatsApp Button Styles */
    .stButton>button {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        font-size: 15px !important;
    }
    .stButton>button:hover {
        background-color: #128C7E !important;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
    }
    
    /* Clear Sticky Header for Cart Summary */
    .cart-summary {
        background-color: #E3FCEF;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #25D366;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Data Loading Engine
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if 'catalogue' in f.lower() and f.endswith('.xlsx')]
    if not excel_files:
        st.error("Missing Excel data sheet.")
        st.stop()
    df = pd.read_excel(excel_files[0], sheet_name="Catalogue", skiprows=5, engine="openpyxl")
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["SKU ID"])
    return df

df = load_data()

# Initialize Multi-item Inquiry Cart in session storage if not present
if "cart" not in st.session_state:
    st.session_state.cart = {}

# 4. Sidebar: Smart Filters & Navigation
st.sidebar.markdown(f"## ✨ {COMPANY_NAME}")
st.sidebar.markdown("Premium Hydration Gear Storefront")
st.sidebar.markdown("---")

# Search Filter
search_query = st.sidebar.text_input("🔍 Search Products", placeholder="e.g. Labubu, Matte, Flask")

# Category Filter
categories = ["All Categories"] + list(df["Category"].dropna().unique())
selected_category = st.sidebar.selectbox("📂 Category", categories)

# Sub-Category Filter (Changes dynamically based on category selected)
if selected_category != "All Categories":
    sub_cats = ["All Sub-categories"] + list(df[df["Category"] == selected_category]["Sub category"].dropna().unique())
else:
    sub_cats = ["All Sub-categories"] + list(df["Sub category"].dropna().unique())
selected_sub = st.sidebar.selectbox("🏷️ Sub-Category", sub_cats)

# WHATSAPP NUMBER CONFIGURATION
YOUR_PHONE_NUMBER = "919821352868"  # 👈 Make sure your actual number stays here

# 5. Filter Application Logic
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[
        filtered_df["Product Name "].str.contains(search_query, case=False, na=False) |
        filtered_df["Key Words"].str.contains(search_query, case=False, na=False) |
        filtered_df["SKU ID"].str.contains(search_query, case=False, na=False)
    ]

if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_sub != "All Sub-categories":
    filtered_df = filtered_df[filtered_df["Sub category"] == selected_sub]


# 6. Main Storefront Display & Interactive Multi-Cart
st.title(f"🥤 {COMPANY_NAME}")

# Cart Widget Display: If customer added any items to batch inquiry
if st.session_state.cart:
    st.markdown('<div class="cart-summary">', unsafe_allow_html=True)
    st.markdown("### 🛒 Selected Items for Enquiry")
    
    items_text = ""
    for idx, (sku_id, item_info) in enumerate(st.session_state.cart.items(), 1):
        st.write(f"**{idx}. {item_info['name']}** ({item_info['colour']} | {item_info['capacity']}) — Qty: {item_info['qty']}")
        items_text += f"• {item_info['name']} ({sku_id}) - Qty: {item_info['qty']} - Config: {item_info['colour']}/{item_info['capacity']}\n"
        
    # Bulk message generation
    bulk_msg = f"Hi {COMPANY_NAME}! I am looking through your digital catalog and would love to get a quote/enquire about these items:\n\n{items_text}"
    encoded_bulk = urllib.parse.quote(bulk_msg)
    bulk_wa_link = f"https://wa.me/{YOUR_PHONE_NUMBER}?text={encoded_bulk}"
    
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.link_button("🟢 Send Bulk Enquiry to WhatsApp", bulk_wa_link, use_container_width=True)
    with col_c2:
        if st.button("❌ Clear List"):
            st.session_state.cart = {}
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# 7. Products Grid Layout
st.markdown(f"Showing **{len(filtered_df)}** premium products.")

if filtered_df.empty:
    st.info("No products match your current filters. Try resetting search fields.")
else:
    cols = st.columns(3)
    
    for index, row in filtered_df.reset_index().iterrows():
        sku = row.get("SKU ID", "N/A")
        prod_name = row.get("Product Name ", "Unnamed Product")
        capacity = row.get("Capacity", "N/A")
        colour = row.get("Colour", "N/A")
        price_val = row.get("Selling Price")
        price_display = f"₹{price_val}" if pd.notna(price_val) else "Ask For Price"
        
        specs = row.get("Specification")
        if pd.isna(specs) or str(specs).strip() == "":
            specs = "Double-Walled Premium Vacuum Insulated Design (Hot & Cold)."

        placeholder_image = "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"

        with cols[index % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.image(placeholder_image, use_container_width=True)
            st.markdown(f"### {prod_name}")
            st.markdown(f"**🏷️ Brand SKU:** `{sku}`")
            st.write(f"🎨 **Color/Size:** {colour} | {capacity}")
            st.write(f"💰 **Pricing:** **{price_display}**")
            st.caption(f"_{specs}_")
            
            # Sub-row for Interactive actions
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                # Add to cart list toggle
                if sku in st.session_state.cart:
                    if st.button("➕ More", key=f"add_{sku}_{index}"):
                        st.session_state.cart[sku]["qty"] += 1
                        st.rerun()
                else:
                    if st.button("🛒 Add to List", key=f"cart_{sku}_{index}"):
                        st.session_state.cart[sku] = {
                            "name": prod_name, "colour": colour, "capacity": capacity, "qty": 1
                        }
                        st.rerun()
                        
            with btn_col2:
                # Direct instant query
                single_msg = f"Hi {COMPANY_NAME}! I want to instantly check availability for:\n\n" \
                             f"📦 *Product:* {prod_name}\n" \
                             f"🆔 *SKU:* {sku}\n" \
                             f"🎨 *Colour:* {colour}\n" \
                             f"📏 *Capacity:* {capacity}"
                encoded_single = urllib.parse.quote(single_msg)
                single_wa_link = f"https://wa.me/{YOUR_PHONE_NUMBER}?text={encoded_single}"
                st.link_button("⚡ Quick Buy", single_wa_link, use_container_width=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
