import streamlit as st
import pandas as pd
import urllib.parse

COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# Data Loading Engine
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ No Excel file found in your repository branch.")
        st.stop()
    
    target_file = excel_files[0]
    
    # Read the whole sheet without skipping rows first to find where the headers are
    raw_df = pd.read_excel(target_file, sheet_name=0, engine="openpyxl")
    
    # Smart Header Finder: Look for the row containing "SKU ID"
    header_idx = 0
    for idx, row in raw_df.iterrows():
        row_str = row.astype(str).str.lower().values
        if any('sku id' in s for s in row_str):
            header_idx = idx + 1
            break
            
    # Reload with the correct header position dynamically
    df = pd.read_excel(target_file, sheet_name=0, skiprows=header_idx, engine="openpyxl")
    
    # Clean up column spaces and capitalization rules
    df.columns = df.columns.str.strip().str.lower()
    
    # Drop completely blank rows
    df = df.dropna(how='all')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Structural Read Error: {str(e)}")
    st.stop()

# Match columns safely even if capitalization changed
def get_col_data(dataframe, possible_names, default="N/A"):
    for name in possible_names:
        if name.lower() in dataframe.columns:
            return dataframe[name.lower()]
    return pd.Series([default] * len(dataframe))

# Map required variables safely
sku_series = get_col_data(df, ["SKU ID", "sku"])
name_series = get_col_data(df, ["Product Name", "Product Name "])
cat_series = get_col_data(df, ["Category"])
sub_series = get_col_data(df, ["Sub category", "Subcategory"])
capacity_series = get_col_data(df, ["Capacity"])
colour_series = get_col_data(df, ["Colour", "Color"])
price_series = get_col_data(df, ["Selling Price"])
desc_series = get_col_data(df, ["Description"])
spec_series = get_col_data(df, ["Specification", "Specifications"])
keyword_series = get_col_data(df, ["Key Words", "Keywords"])
img_series = get_col_data(df, ["Images", "Image Link"])

# Build clean working dataframe
clean_df = pd.DataFrame({
    "sku": sku_series, "name": name_series, "category": cat_series,
    "subcategory": sub_series, "capacity": capacity_series, "colour": colour_series,
    "price": price_series, "description": desc_series, "specification": spec_series,
    "keywords": keyword_series, "images": img_series
}).dropna(subset=["sku"])

# Initialize Cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Sidebar Filters
st.sidebar.markdown(f"## 💎 {COMPANY_NAME}")
st.sidebar.markdown("---")
search_query = st.sidebar.text_input("🔍 Smart Search Catalog", placeholder="Search items...")

categories = ["All Categories"] + list(clean_df["category"].dropna().unique())
selected_category = st.sidebar.selectbox("📂 Category Group", categories)

filtered_df = clean_df.copy()

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["name"].astype(str).str.lower().str.contains(q) |
        filtered_df["description"].astype(str).str.lower().str.contains(q) |
        filtered_df["specification"].astype(str).str.lower().str.contains(q) |
        filtered_df["keywords"].astype(str).str.lower().str.contains(q) |
        filtered_df["sku"].astype(str).str.lower().str.contains(q)
    ]

if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

# WhatsApp Destination setup
YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 PLACE YOUR NUMBER HERE

# Main View App
st.title(f"🥤 {COMPANY_NAME}")

if st.session_state.cart:
    st.markdown('<div style="background-color: #E3FCEF; padding: 20px; border-radius: 14px; border-left: 6px solid #25D366; margin-bottom: 30px;">', unsafe_allow_html=True)
    st.markdown("### 🛒 My Current Inquiry List")
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
        st.write(f"🔹 **{item['name']}** — Qty: **{item['qty']}**")
        items_summary_text += f"{idx}. {item['name']} [{sku_id}] (Qty: {item['qty']})\n"
    compiled_message = f"Hi {COMPANY_NAME}! I would love to check availability for these items:\n\n{items_summary_text}"
    encoded_message = urllib.parse.quote(compiled_message)
    st.link_button("🟢 Submit Order Inquiry to WhatsApp", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={encoded_message}", use_container_width=True)
    if st.button("🗑️ Clear List"):
        st.session_state.cart = {}
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Grid Layout Rendering
if filtered_df.empty:
    st.info("No items match your search filters.")
else:
    cols = st.columns(3)
    for index, row in filtered_df.reset_index().iterrows():
        sku = row["sku"]
        name = row["name"]
        price_display = f"₹{row['price']}" if pd.notna(row['price']) else "Contact for Quote"
        
        img_val = row["images"]
        images_list = ["https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"] if pd.isna(img_val) else [img.strip() for img in str(img_val).split(",")]

        with cols[index % 3]:
            st.markdown('<div style="padding: 24px; border-radius: 16px; background-color: #FFFFFF; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); border: 1px solid #E9ECEF;">', unsafe_allow_html=True)
            
            if len(images_list) == 1:
                st.image(images_list[0], use_container_width=True)
            else:
                img_tabs = st.tabs([f"📸 View {i+1}" for i in range(len(images_list))])
                for i, url in enumerate(images_list):
                    with img_tabs[i]: st.image(url, use_container_width=True)
                    
            st.markdown(f"### {name}")
            st.markdown(f"`SKU: {sku}`")
            st.markdown(f"## {price_display}")
            
            tab1, tab2 = st.tabs(["📋 Details", "🔧 Specs"])
            with tab1:
                st.write(f"🎨 **Color:** {row['colour']} | 📏 **Size:** {row['capacity']}")
                st.caption(str(row['description']))
            with tab2:
                st.write(str(row['specification']))
                
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if sku in st.session_state.cart:
                    st.write(f"Selected: **{st.session_state.cart[sku]['qty']}**")
                    if st.button("➕ Add", key=f"inc_{sku}_{index}"):
                        st.session_state.cart[sku]["qty"] += 1
                        st.rerun()
                else:
                    if st.button("🛒 Add to List", key=f"add_{sku}_{index}"):
                        st.session_state.cart[sku] = {"name": name, "qty": 1}
                        st.rerun()
            with btn_col2:
                single_msg = f"Hi {COMPANY_NAME}! I want to check availability for:\n📦 *Product:* {name}\n🆔 *SKU:* {sku}"
                st.link_button("⚡ Quick Buy", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(single_msg)}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
