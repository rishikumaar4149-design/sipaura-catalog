import streamlit as st
import pandas as pd
import urllib.parse

COMPANY_NAME = "SIPAURA DRINKWARE"
st.set_page_config(page_title=COMPANY_NAME, layout="wide", page_icon="🥤")

# 1. Standard Fallback Data Reader Engine
@st.cache_data
def load_data():
    import os
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and not f.startswith('~$')]
    if not excel_files:
        st.error("❌ No Excel file found in your repository branch.")
        st.stop()
        
    target_file = excel_files[0]
    
    # Read the sheet natively
    try:
        df = pd.read_excel(target_file, sheet_name=0, engine="openpyxl")
    except Exception as e:
        st.error(f"❌ Read Error: {str(e)}")
        st.stop()
        
    # Clean string format spacing metrics from headers
    df.columns = df.columns.str.strip()
    
    # If the headers are pushed down, locate row with SKU ID dynamically
    if "SKU ID" not in df.columns:
        for idx, row in df.iterrows():
            row_vals = row.astype(str).str.strip().values
            if "SKU ID" in row_vals:
                df = pd.read_excel(target_file, sheet_name=0, skiprows=idx+1, engine="openpyxl")
                df.columns = df.columns.str.strip()
                break
                
    # Drop rows without a valid identifier key
    if "SKU ID" in df.columns:
        df = df.dropna(subset=["SKU ID"])
    else:
        # Fallback to absolute first structural layout column if name isn't matching
        df = df.dropna(subset=[df.columns[0]])
        
    return df

df = load_data()

# 2. Extract Data safely with fallback defaults to prevent KeyErrors
sku_list = df["SKU ID"].astype(str).tolist() if "SKU ID" in df.columns else [f"ITEM-{i}" for i in range(len(df))]

# Match possible variations of Product Name
name_col = None
for col in ["Product Name", "Product Name ", "Product_Name", "Name"]:
    if col in df.columns:
        name_col = col
        break
name_list = df[name_col].astype(str).tolist() if name_col else [f"Premium Bottle {i+1}" for i in range(len(df))]

cat_list = df["Category"].fillna("Drinkware").astype(str).tolist() if "Category" in df.columns else ["Drinkware"] * len(df)
colour_list = df["Colour"].fillna("Standard").astype(str).tolist() if "Colour" in df.columns else ["Standard"] * len(df)
capacity_list = df["Capacity"].fillna("N/A").astype(str).tolist() if "Capacity" in df.columns else ["N/A"] * len(df)
price_list = df["Selling Price"].fillna("").tolist() if "Selling Price" in df.columns else [""] * len(df)
desc_list = df["Description"].fillna("Premium Double Wall Vacuum Insulated Layout.").astype(str).tolist() if "Description" in df.columns else ["Premium Layout."] * len(df)
spec_list = df["Specification"].fillna("High Grade Stainless Steel.").astype(str).tolist() if "Specification" in df.columns else ["High Grade Materials."] * len(df)
keyword_list = df["Key Words"].fillna("").astype(str).tolist() if "Key Words" in df.columns else [""] * len(df)
img_list = df["Images"].fillna("").astype(str).tolist() if "Images" in df.columns else [""] * len(df)

# Re-assemble clean rows cleanly
products = []
for i in range(len(df)):
    products.append({
        "sku": sku_list[i],
        "name": name_list[i],
        "category": cat_list[i],
        "colour": colour_list[i],
        "capacity": capacity_list[i],
        "price": price_list[i],
        "description": desc_list[i],
        "specification": spec_list[i],
        "keywords": keyword_list[i],
        "images": img_list[i]
    })

# 3. Session state Initialization
if "cart" not in st.session_state:
    st.session_state.cart = {}

# 4. Filter Dashboard Sidebar System Layouts
st.sidebar.markdown(f"## 💎 {COMPANY_NAME}")
st.sidebar.markdown("---")
search_query = st.sidebar.text_input("🔍 Smart Search Catalog", placeholder="Search items...")

unique_categories = sorted(list(set(cat_list)))
selected_category = st.sidebar.selectbox("📂 Category Group", ["All Categories"] + unique_categories)

# Apply runtime logical filtration steps
filtered_products = []
for p in products:
    # Filter category
    if selected_category != "All Categories" and p["category"] != selected_category:
        continue
    # Filter search text matches query targets
    if search_query:
        q = search_query.lower()
        match = (q in p["name"].lower() or 
                 q in p["sku"].lower() or 
                 q in p["description"].lower() or 
                 q in p["specification"].lower() or 
                 q in p["keywords"].lower())
        if not match:
            continue
            
    filtered_products.append(p)

# WhatsApp Routing Parameter Configuration Settings
YOUR_PHONE_NUMBER = "91XXXXXXXXXX"  # 👈 PLACE YOUR REAL WHATSAPP NUMBER HERE

# 5. Application UI Interface Engine
st.title(f"🥤 {COMPANY_NAME}")

if st.session_state.cart:
    st.markdown('<div style="background-color: #E3FCEF; padding: 20px; border-radius: 14px; border-left: 6px solid #25D366; margin-bottom: 30px;">', unsafe_allow_html=True)
    st.markdown("### 🛒 My Current Inquiry List")
    items_summary_text = ""
    for idx, (sku_id, item) in enumerate(st.session_state.cart.items(), 1):
        st.write(f"🔹 **{item['name']}** — Qty: **{item['qty']}**")
        items_summary_text += f"{idx}. {item['name']} [{sku_id}] (Qty: {item['qty']})\n"
    compiled_message = f"Hi {COMPANY_NAME}! I would love to check availability for these items:\n\n{items_summary_text}"
    st.link_button("🟢 Submit Order Inquiry to WhatsApp", f"https://wa.me/{YOUR_PHONE_NUMBER}?text={urllib.parse.quote(compiled_message)}", use_container_width=True)
    if st.button("🗑️ Clear List"):
        st.session_state.cart = {}
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 6. Grid Renderer Showcase
if not filtered_products:
    st.info("No items match your active search filters.")
else:
    cols = st.columns(3)
    for index, p in enumerate(filtered_products):
        sku = p["sku"]
        name = p["name"]
        price_display = f"₹{p['price']}" if p['price'] and str(p['price']).strip() != "" else "Contact for Quote"
        
        # Parse image list structures
        if not p["images"] or p["images"] == "nan" or p["images"] == "None":
            images_list = ["https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"]
        else:
            images_list = [img.strip() for img in str(p["images"]).split(",")]

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
                st.write(f"🎨 **Color:** {p['colour']} | 📏 **Size:** {p['capacity']}")
                st.caption(p['description'])
            with tab2:
                st.write(p['specification'])
                
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
