# import streamlit as st
# import pandas as pd
# import time
# import os

# # YOLO COCO class names → for mapping detections to products
# COCO_CLASSES = {
#     39: 'bottle', 40: 'wine glass', 41: 'cup', 44: 'knife', 46: 'banana',
#     56: 'chair', 65: 'cell phone', 73: 'laptop', 24: 'backpack'
# }

# def load_warehouse():
#     """Load warehouse - returns empty if no valid data"""
#     if not os.path.exists("warehouse_stock.csv"):
#         return pd.DataFrame(columns=["product_id", "product_name", "current_stock"])
    
#     try:
#         df = pd.read_csv("warehouse_stock.csv")
#         df = df[df['product_id'] >= 1].reset_index(drop=True)
#         if df.empty:
#             return df
#         df['product_id'] = df['product_id'].astype(int)
#         df['current_stock'] = df['current_stock'].astype(int)
#         return df
#     except:
#         return pd.DataFrame(columns=["product_id", "product_name", "current_stock"])

# def app():
#     st.markdown(
#         "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>🔮 PREDICTIVE REORDERING</h1>",
#         unsafe_allow_html=True
#     )

#     # Initialize warehouse in session_state
#     if "warehouse_stock" not in st.session_state:
#         st.session_state.warehouse_stock = load_warehouse()

#     # Safe dict getters
#     def safe_dict_get(state_key, default_dict):
#         if state_key not in st.session_state:
#             st.session_state[state_key] = default_dict.copy()
#         return st.session_state[state_key]

#     def safe_remove_from_dict(dict_obj, key):
#         dict_obj.pop(key, None)

#     total_stock = safe_dict_get("total_stock", {})
#     total_sold = safe_dict_get("total_sold", {})
#     previous_shelf = safe_dict_get("previous_shelf", {})
#     last_alert = safe_dict_get("last_alert", {})

#     warehouse_df = st.session_state.warehouse_stock.copy()

#     # Sync session state with warehouse
#     for _, row in warehouse_df.iterrows():
#         pid = int(row["product_id"])
#         total_stock[pid] = int(row["current_stock"])
#         total_sold.setdefault(pid, 0)

#     tab1, tab2 = st.tabs(["📊 Live Dashboard", "➕ Setup Stock"])

#     with tab1:
#         st.subheader("🔴 LIVE TRACKING")
        
#         if warehouse_df.empty:
#             st.info("👆 **No products yet** - Add from Setup tab!")
#         else:
#             monitoring_active = "monitoring_data" in st.session_state and st.session_state.monitoring_data.get("last_update", 0) > 0

#             for idx, row in warehouse_df.iterrows():
#                 product_id = int(row["product_id"])
#                 product_name = row["product_name"].lower()
                
#                 total_stock_count = total_stock.get(product_id, 0)
#                 total_sold_count = total_sold.get(product_id, 0)

#                 # LIVE SHELF COUNT
#                 shelf_count = 0
#                 if monitoring_active:
#                     counts = st.session_state.monitoring_data["counts"]
#                     for cls_id, cls_name in COCO_CLASSES.items():
#                         if cls_name in product_name or product_name in cls_name:
#                             shelf_count = int(counts.get(cls_id, 0))
#                             break

#                 # SALE DETECTION - Only decrease
#                 prev_shelf = previous_shelf.get(product_id, shelf_count)
#                 sold_now = 0
#                 if prev_shelf > shelf_count and prev_shelf > 0:
#                     sold_now = prev_shelf - shelf_count
#                     total_sold[product_id] = total_sold_count + sold_now
#                     total_stock[product_id] = total_stock_count - sold_now

#                 previous_shelf[product_id] = shelf_count

#                 # DASHBOARD ROW
#                 col1, col2, col3, col4, col5, col6 = st.columns([1,2,2,2,2,1])
#                 with col1: st.metric("🆔", product_id)
#                 with col2: st.metric("📦", product_name.title())
#                 with col3: st.metric("🏬 TOTAL", total_stock.get(product_id, 0))
#                 with col4: st.metric("🛒 Shelf", shelf_count, delta=f"-{sold_now}" if sold_now > 0 else None)
#                 with col5: st.metric("📉 Sold", total_sold.get(product_id, 0))
#                 with col6:
#                     if st.button(f"🗑️", key=f"del_{product_id}"):
#                         # Safe delete
#                         safe_remove_from_dict(total_stock, product_id)
#                         safe_remove_from_dict(total_sold, product_id)
#                         safe_remove_from_dict(previous_shelf, product_id)
#                         safe_remove_from_dict(last_alert, product_id)
                        
#                         # Update warehouse
#                         st.session_state.warehouse_stock = st.session_state.warehouse_stock[
#                             st.session_state.warehouse_stock["product_id"] != product_id
#                         ].reset_index(drop=True)
#                         st.session_state.warehouse_stock.to_csv("warehouse_stock.csv", index=False)
#                         st.success(f"✅ Deleted {product_name.title()}")
#                         st.rerun()

#                 st.divider()

#     with tab2:
#         st.subheader("➕ TOTAL STOCK SETUP")
        
#         # FORM - ALWAYS VISIBLE
#         with st.form("stock_form", clear_on_submit=True):
#             col1, col2, col3 = st.columns(3)
#             with col1: pid = st.number_input("Product ID", value=1, min_value=1, key="pid")
#             with col2: pname = st.text_input("Name", value="bottle", key="pname")
#             with col3: total_stk = st.number_input("TOTAL Stock", value=400, min_value=0, key="total_stk")
            
#             if st.form_submit_button("💾 SAVE TOTAL STOCK"):
#                 # Create/update warehouse
#                 if st.session_state.warehouse_stock.empty:
#                     new_df = pd.DataFrame({
#                         "product_id": [pid], "product_name": [pname], "current_stock": [total_stk]
#                     })
#                 else:
#                     mask = st.session_state.warehouse_stock["product_id"] == pid
#                     if mask.any():
#                         new_df = st.session_state.warehouse_stock.copy()
#                         new_df.loc[mask, "current_stock"] = total_stk
#                         total_sold[pid] = 0  # Reset sold
#                     else:
#                         new_row = pd.DataFrame({
#                             "product_id": [pid], "product_name": [pname], "current_stock": [total_stk]
#                         })
#                         new_df = pd.concat([st.session_state.warehouse_stock, new_row], ignore_index=True)
#                         total_stock[pid] = total_stk
#                         total_sold[pid] = 0
                
#                 # SAVE EVERYWHERE
#                 st.session_state.warehouse_stock = new_df
#                 new_df.to_csv("warehouse_stock.csv", index=False)
#                 st.session_state.total_stock = total_stock.copy()
#                 st.session_state.total_sold = total_sold.copy()
                
#                 st.success(f"✅ {pname}: TOTAL={total_stk}")
#                 st.rerun()

#         # Show current stock
#         if not st.session_state.warehouse_stock.empty:
#             st.subheader("📋 Current Products")
#             st.dataframe(st.session_state.warehouse_stock)

#     st.sidebar.info("""
# **🎯 TEST FLOW:**
# 1. Setup → ID=1, bottle, 400 → SAVE
# 2. Dashboard → Shows instantly!
# 3. Monitor → Shelf updates live
#     """)

# def reorder_alert(product_id, product_name, total_stock, shelf_count):
#     st.error(f"🚨 LOW STOCK {product_name} (ID:{product_id}) - TOTAL:{total_stock}")

# if __name__ == "__main__":
#     app()






















import streamlit as st
import pandas as pd
import time
import os

def load_warehouse():
    """Load warehouse - returns empty if no valid data"""
    if not os.path.exists("warehouse_stock.csv"):
        return pd.DataFrame(columns=["product_id", "product_name", "current_stock"])
    
    try:
        df = pd.read_csv("warehouse_stock.csv")
        df = df[df['product_id'] >= 1].reset_index(drop=True)
        if df.empty:
            return df
        df['product_id'] = df['product_id'].astype(int)
        df['current_stock'] = df['current_stock'].astype(int)
        return df
    except:
        return pd.DataFrame(columns=["product_id", "product_name", "current_stock"])

def app():
    st.markdown(
        "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>🔮 PREDICTIVE REORDERING</h1>",
        unsafe_allow_html=True
    )

    # Initialize warehouse in session_state
    if "warehouse_stock" not in st.session_state:
        st.session_state.warehouse_stock = load_warehouse()

    # Safe dict getters
    def safe_dict_get(state_key, default_dict):
        if state_key not in st.session_state:
            st.session_state[state_key] = default_dict.copy()
        return st.session_state[state_key]

    def safe_remove_from_dict(dict_obj, key):
        dict_obj.pop(key, None)

    total_stock = safe_dict_get("total_stock", {})
    total_sold = safe_dict_get("total_sold", {})
    previous_shelf = safe_dict_get("previous_shelf", {})
    last_alert = safe_dict_get("last_alert", {})

    warehouse_df = st.session_state.warehouse_stock.copy()

    # Sync session state with warehouse
    for _, row in warehouse_df.iterrows():
        pid = int(row["product_id"])
        total_stock[pid] = int(row["current_stock"])
        total_sold.setdefault(pid, 0)

    tab1, tab2 = st.tabs(["📊 Live Dashboard", "➕ Setup Stock"])

    with tab1:
        st.subheader("🔴 LIVE TRACKING")
        
        if warehouse_df.empty:
            st.info("👆 **No products yet** - Add from Setup tab!")
        else:
            monitoring_active = "monitoring_data" in st.session_state and st.session_state.monitoring_data.get("last_update", 0) > 0

            for idx, row in warehouse_df.iterrows():
                product_id = int(row["product_id"])
                product_name = row["product_name"].lower()
                
                total_stock_count = total_stock.get(product_id, 0)
                total_sold_count = total_sold.get(product_id, 0)

                # 🔥 FIXED: Direct product name matching!
                shelf_count = 0
                if monitoring_active:
                    counts = st.session_state.monitoring_data["counts"]  # {"bottle": 2}
                    # Direct name match - NO class ID lookup!
                    shelf_count = int(counts.get(product_name, 0))

                # SALE DETECTION - Only decrease
                prev_shelf = previous_shelf.get(product_id, shelf_count)
                sold_now = 0
                if prev_shelf > shelf_count and prev_shelf > 0:
                    sold_now = prev_shelf - shelf_count
                    total_sold[product_id] = total_sold_count + sold_now
                    total_stock[product_id] = total_stock_count - sold_now

                previous_shelf[product_id] = shelf_count
                
                # 🔥 SAVE STATE AFTER EVERY PRODUCT
                st.session_state.total_stock = total_stock.copy()
                st.session_state.total_sold = total_sold.copy()
                st.session_state.previous_shelf = previous_shelf.copy()

                # DASHBOARD ROW
                col1, col2, col3, col4, col5, col6 = st.columns([1,2,2,2,2,1])
                with col1: st.metric("🆔", product_id)
                with col2: st.metric("📦", product_name.title())
                with col3: st.metric("🏬 TOTAL", total_stock.get(product_id, 0))
                with col4: st.metric("🛒 Shelf", shelf_count, delta=f"-{sold_now}" if sold_now > 0 else None)
                with col5: st.metric("📉 Sold", total_sold.get(product_id, 0))
                with col6:
                    if st.button(f"🗑️", key=f"del_{product_id}"):
                        # Safe delete
                        safe_remove_from_dict(total_stock, product_id)
                        safe_remove_from_dict(total_sold, product_id)
                        safe_remove_from_dict(previous_shelf, product_id)
                        safe_remove_from_dict(last_alert, product_id)
                        
                        # Update warehouse
                        st.session_state.warehouse_stock = st.session_state.warehouse_stock[
                            st.session_state.warehouse_stock["product_id"] != product_id
                        ].reset_index(drop=True)
                        st.session_state.warehouse_stock.to_csv("warehouse_stock.csv", index=False)
                        st.success(f"✅ Deleted {product_name.title()}")
                        st.rerun()

                st.divider()

    with tab2:
        st.subheader("➕ TOTAL STOCK SETUP")
        
        # FORM - ALWAYS VISIBLE
        with st.form("stock_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1: pid = st.number_input("Product ID", value=1, min_value=1, key="pid")
            with col2: pname = st.text_input("Name", value="bottle", key="pname")
            with col3: total_stk = st.number_input("TOTAL Stock", value=400, min_value=0, key="total_stk")
            
            if st.form_submit_button("💾 SAVE TOTAL STOCK"):
                # Create/update warehouse
                if st.session_state.warehouse_stock.empty:
                    new_df = pd.DataFrame({
                        "product_id": [pid], "product_name": [pname], "current_stock": [total_stk]
                    })
                else:
                    mask = st.session_state.warehouse_stock["product_id"] == pid
                    if mask.any():
                        new_df = st.session_state.warehouse_stock.copy()
                        new_df.loc[mask, "current_stock"] = total_stk
                        total_sold[pid] = 0  # Reset sold
                    else:
                        new_row = pd.DataFrame({
                            "product_id": [pid], "product_name": [pname], "current_stock": [total_stk]
                        })
                        new_df = pd.concat([st.session_state.warehouse_stock, new_row], ignore_index=True)
                        total_stock[pid] = total_stk
                        total_sold[pid] = 0
                
                # SAVE EVERYWHERE
                st.session_state.warehouse_stock = new_df
                new_df.to_csv("warehouse_stock.csv", index=False)
                st.session_state.total_stock = total_stock.copy()
                st.session_state.total_sold = total_sold.copy()
                
                st.success(f"✅ {pname}: TOTAL={total_stk}")
                st.rerun()

        # Show current stock
        if not st.session_state.warehouse_stock.empty:
            st.subheader("📋 Current Products")
            st.dataframe(st.session_state.warehouse_stock)

    st.sidebar.info("""
**🎯 NOW UPDATES LIVE:**
1. Setup → ID=1, "bottle", 400 → SAVE
2. Monitor → Detects bottles → Shelf=2 instantly!
3. Remove bottle → Sold=1, TOTAL=399 ✅
    """)

def reorder_alert(product_id, product_name, total_stock, shelf_count):
    st.error(f"🚨 LOW STOCK {product_name} (ID:{product_id}) - TOTAL:{total_stock}")

if __name__ == "__main__":
    app()
