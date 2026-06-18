import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuration
YOUR_PHONE_NUMBER = "919821352868"  # 👈 REPLACE WITH YOUR REAL WHATSAPP NUMBER
COMPANY_NAME = "SIPAURA DRINKWARE"

st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stButton>button {
        background-color: #25D366;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #128C7E;
        color: white;
    }
    .product-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Load and clean the Excel Data directly from "Product catalogue.xlsx"
@st.cache_data
def load_data():
    df = pd.read_excel("Product catalogue.xlsx", sheet_name="Catalogue", skiprows=5)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["SKU ID"])
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Could not read 'Product catalogue.xlsx'. Make sure it is in the same folder as app.py.")
    st.stop()

# 3. Sidebar Brand Header & Filters
st.sidebar.title(f"✨ {COMPANY_NAME}")
st.sidebar.markdown("---")

categories = ["All"] + list(df["Category"].dropna().unique())
selected_category = st.sidebar.selectbox("Filter by Category", categories)

# Filter Data
if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category]
else:
    filtered_df = df

# 4. Main Storefront App Navbar/Header
st.title(f"🥤 {COMPANY_NAME} Digital Storefront")
st.markdown("Browse our premium catalog below. Click any item to instantly send an enquiry via WhatsApp.")
st.markdown("---")

# 5. Render Products Grid
if filtered_df.empty:
    st.warning("No products found.")
else:
    cols = st.columns(3)
    
    for index, row in filtered_df.iterrows():
        price_val = row.get("Selling Price")
        price_display = f"₹{price_val}" if pd.notna(price_val) else "Contact for Price"
        
        prod_name = row.get("Product Name ", "Unnamed Product") # Notice the space from your excel column
        sku = row.get("SKU ID", "N/A")
        capacity = row.get("Capacity", "N/A")
        colour = row.get("Colour", "N/A")
        specs = row.get("Specification", "Premium Insulated Build")
        if pd.isna(specs): specs = "Premium Stainless Steel Insulated Bottle."

        placeholder_image = "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"

        with cols[index % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            st.image(placeholder_image, use_container_width=True)
            st.markdown(f"### {prod_name}")
            st.markdown(f"**SKU:** `{sku}`")
            st.markdown(f"**Specs:** {capacity} | {colour}")
            st.markdown(f"💰 **Price:** **{price_display}**")
            st.caption(f"_{specs}_")
            
            msg = f"Hi {COMPANY_NAME}! I would like to enquire about:\n\n" \
                  f"📦 *Product:* {prod_name}\n" \
                  f"🆔 *SKU:* {sku}\n" \
                  f"📏 *Capacity:* {capacity}\n" \
                  f"🎨 *Colour:* {colour}\n" \
                  f"💸 *Price:* {price_display}"
                  
            encoded_msg = urllib.parse.quote(msg)
            wa_link = f"https://wa.me/{YOUR_PHONE_NUMBER}?text={encoded_msg}"
            
            st.link_button("💬 Send WhatsApp Enquiry", wa_link, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)