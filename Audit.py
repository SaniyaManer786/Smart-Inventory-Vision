





# import sqlite3
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import numpy as np
# from datetime import datetime, timedelta

# def app():
#     st.markdown(
#         "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>🔍 BUSINESS AUDIT DASHBOARD</h1>",
#         unsafe_allow_html=True
#     )

#     # Connect & fetch data
#     conn = sqlite3.connect('inventory.db', check_same_thread=False)
#     df = pd.read_sql("SELECT * FROM inventory ORDER BY timestamp ASC", conn)
#     conn.close()
    
#     if df.empty:
#         st.warning("👆 Run Monitoring first!")
#         st.stop()

#     # Data prep
#     df['timestamp'] = pd.to_datetime(df['timestamp'])
#     df['hour'] = df['timestamp'].dt.hour
#     df['date'] = df['timestamp'].dt.date
#     df['sku_name'] = 'SKU_' + df['sku'].astype(str).str.zfill(2)
    
#     st.success(f"📊 **{len(df)} records** | **{df['sku'].nunique()} products**")

#     # Simulate sales
#     df_sorted = df.sort_values(['sku', 'timestamp']).copy()
#     df_sorted['stock_change'] = df_sorted.groupby('sku')['stock_count'].diff()
#     df_sorted['sales'] = -df_sorted['stock_change'].fillna(np.random.randint(0, 3)).clip(lower=0)
    
#     # Force minimum sales
#     if df_sorted['sales'].sum() == 0:
#         for i, sku in enumerate(df_sorted['sku'].unique()[:3]):
#             mask = df_sorted['sku'] == sku
#             df_sorted.loc[mask, 'sales'] = np.random.randint(1, 8, mask.sum())

#     # 🔥 1. THEFT DETECTION
#     st.markdown("### 🚨 Theft Detection")
#     theft_events = df_sorted[df_sorted['stock_change'] < -2][
#         ['sku_name', 'timestamp', 'stock_count', 'stock_change']
#     ].head(10)
    
#     if not theft_events.empty:
#         st.error(f"🚨 **{len(theft_events)} THEFTS!**")
#         st.dataframe(theft_events)
#     else:
#         st.success("✅ No theft")

#     # 🔥 2. SALES VELOCITY - 🌈 EACH PRODUCT DIFFERENT COLOR!
#     st.markdown("### 🚀 Sales Velocity")
#     today_sales = df_sorted[df_sorted['date'] == df_sorted['date'].max()]
#     daily_sales = today_sales.groupby('sku_name')['sales'].sum().reset_index()
    
#     if daily_sales.empty:
#         daily_sales = pd.DataFrame({
#             'sku_name': [f'SKU_0{i}' for i in range(1, 4)],
#             'sales': [12, 8, 3]
#         })

#     # ✅ MAGIC: color='sku_name' = Different color per product!
#     fig_sales = px.bar(
#         daily_sales.sort_values('sales'),
#         x='sales', 
#         y='sku_name', 
#         orientation='h',
#         color='sku_name',  # 🌈 EACH PRODUCT UNIQUE COLOR!
#         title="📊 **Sales Velocity** (Each Product = Different Color)",
#         text='sales',
#         color_discrete_sequence=px.colors.qualitative.Set3  # Beautiful palette
#     )
#     fig_sales.update_layout(height=400, showlegend=True)
#     st.plotly_chart(fig_sales, use_container_width=True)

#     # 🔥 3. DEMAND FORECASTING - 🌈 EACH PRODUCT DIFFERENT COLOR!
#     st.markdown("### 📊 Demand Forecasting")
#     hourly_sales = df_sorted.groupby(['sku_name', 'hour'])['sales'].sum().reset_index()
#     hourly_sales['time_label'] = hourly_sales['hour'].astype(str).str.zfill(2) + ":00"
    
#     if hourly_sales.empty:
#         hourly_sales = pd.DataFrame({
#             'sku_name': ['SKU_01', 'SKU_02', 'SKU_01', 'SKU_03', 'SKU_02'],
#             'hour': [12, 14, 18, 10, 16],
#             'sales': [8, 6, 5, 4, 3]
#         })
#         hourly_sales['time_label'] = hourly_sales['hour'].astype(str).str.zfill(2) + ":00"

#     # ✅ MAGIC: color='sku_name' = Different color per product!
#     fig_forecast = px.bar(
#         hourly_sales.sort_values('sales'),
#         x='sales', 
#         y='time_label', 
#         orientation='h',
#         color='sku_name',  # 🌈 EACH PRODUCT UNIQUE COLOR!
#         title="🕐 **Peak Hours** (Hover: Product + Time + Count)",
#         text='sales',
#         color_discrete_sequence=px.colors.qualitative.Set1  # Different palette
#     )
#     fig_forecast.update_layout(height=400, showlegend=True)
#     st.plotly_chart(fig_forecast, use_container_width=True)

#     # 🔥 4. ACTION ITEMS
#     st.markdown("### ✅ Action Items")
#     fast_sellers = daily_sales.nlargest(2, 'sales')['sku_name'].tolist()
#     slow_sellers = daily_sales.nsmallest(2, 'sales')['sku_name'].tolist()
    
#     col1, col2 = st.columns(2)
#     with col1:
#         st.error("🔴 **RESTOCK**")
#         for sku in fast_sellers:
#             st.info(f"• {sku}")
#     with col2:
#         st.warning("🔵 **DISCOUNT**")
#         for sku in slow_sellers:
#             st.info(f"• {sku}")

#     st.sidebar.markdown("""
#     **🌈 COLOR CODING:**
#     • Each **SKU_01, SKU_02, SKU_03** = **Unique Color**
#     • **Legend** shows product-color mapping  
#     • **Set1/Set3** = Professional palettes
    
#     **🖱️ Hover:** Product + Time + Sales Count
#     """)

# if __name__ == "__main__":
#     app()



import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta


def app():
    st.markdown(
        "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>🔍 BUSINESS AUDIT DASHBOARD</h1>",
        unsafe_allow_html=True
    )

    # Connect & fetch data
    try:
        conn = sqlite3.connect('inventory.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory';")
        if not cursor.fetchall():
            st.error("⚠️ Table 'inventory' not found in inventory.db")
            st.stop()

        df = pd.read_sql("SELECT * FROM inventory ORDER BY timestamp ASC", conn)
        conn.close()

        if df.empty:
            st.warning("👆 Run Monitoring first!")
            st.stop()

    except Exception as e:
        st.error(f"⚠️ Error reading inventory.db: {e}")
        st.stop()

    # Data prep
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['date'] = df['timestamp'].dt.date
    df['sku_name'] = 'SKU_' + df['sku'].astype(str).str.zfill(2)

    st.success(f"📊 **{len(df)} records** | **{df['sku'].nunique()} products**")

    # Simulate sales
    df_sorted = df.sort_values(['sku', 'timestamp']).copy()
    df_sorted['stock_change'] = df_sorted.groupby('sku')['stock_count'].diff()
    df_sorted['sales'] = -df_sorted['stock_change'].fillna(np.random.randint(0, 3)).clip(lower=0)

    # Force minimum sales overall
    if df_sorted['sales'].sum() == 0:
        for i, sku in enumerate(df_sorted['sku'].unique()[:3]):
            mask = df_sorted['sku'] == sku
            df_sorted.loc[mask, 'sales'] = np.random.randint(1, 8, mask.sum())

    # 🔥 1. THEFT DETECTION
    st.markdown("### 🚨 Theft Detection")
    theft_events = df_sorted[df_sorted['stock_change'] < -2][
        ['sku_name', 'timestamp', 'stock_count', 'stock_change']
    ].head(10)

    if not theft_events.empty:
        st.error(f"🚨 **{len(theft_events)} THEFTS!**")
        st.dataframe(theft_events)
    else:
        st.success("✅ No theft")

    # 🔥 2. SALES VELOCITY
    st.markdown("### 🚀 Sales Velocity")

    # Use latest date in data, not necessarily “today”
    latest_date = df_sorted['date'].max()
    today_sales = df_sorted[df_sorted['date'] == latest_date]

    daily_sales = today_sales.groupby('sku_name')['sales'].sum().reset_index()
    daily_sales = daily_sales.sort_values('sales', ascending=True)

    # Debug: let you see what is going into the chart
    # st.write("DEBUG: daily_sales", daily_sales.head(10))

    if daily_sales.empty or daily_sales['sales'].sum() == 0:
        st.warning("No real sales today; using fake data for demo.")
        daily_sales = pd.DataFrame({
            'sku_name': [f'SKU_0{i}' for i in range(1, 4)],
            'sales': [12, 8, 3]
        })

    fig_sales = px.bar(
        daily_sales,
        x='sales',
        y='sku_name',
        orientation='h',
        color='sku_name',
        title="📊 Sales Velocity (Latest Day's Sales)",
        text='sales',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_sales.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig_sales, use_container_width=True)


    # 🔥 3. DEMAND FORECASTING
    st.markdown("### 📊 Demand Forecasting")

    hourly_sales = df_sorted.groupby(['sku_name', 'hour'])['sales'].sum().reset_index()
    hourly_sales['time_label'] = hourly_sales['hour'].astype(str).str.zfill(2) + ":00"

    if hourly_sales.empty or hourly_sales['sales'].sum() == 0:
        st.warning("No hourly sales data; using fake data for demo.")
        hourly_sales = pd.DataFrame({
            'sku_name': ['SKU_01', 'SKU_02', 'SKU_01', 'SKU_03', 'SKU_02'],
            'hour': [12, 14, 18, 10, 16],
            'sales': [8, 6, 5, 4, 3]
        })
        hourly_sales['time_label'] = hourly_sales['hour'].astype(str).str.zfill(2) + ":00"

    fig_forecast = px.bar(
        hourly_sales.sort_values('sales', ascending=True),
        x='sales',
        y='time_label',
        orientation='h',
        color='sku_name',
        title="🕐 Peak Hours (Hover: Product + Time + Count)",
        text='sales',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_forecast.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig_forecast, use_container_width=True)


    # 🔥 4. ACTION ITEMS
    st.markdown("### ✅ Action Items")
    fast_sellers = daily_sales.nlargest(2, 'sales')['sku_name'].tolist()
    slow_sellers = daily_sales.nsmallest(2, 'sales')['sku_name'].tolist()

    col1, col2 = st.columns(2)
    with col1:
        st.error("🔴 **RESTOCK**")
        for sku in fast_sellers:
            st.info(f"• {sku}")
    with col2:
        st.warning("🔵 **DISCOUNT**")
        for sku in slow_sellers:
            st.info(f"• {sku}")

    # Sidebar note
    st.sidebar.markdown("""
    **🌈 COLOR CODING:**
    • Each **SKU_01, SKU_02, SKU_03** = **Unique Color**
    • **Legend** shows product-color mapping  
    • **Set1/Set3** = Professional palettes
    
    **🖱️ Hover:** Product + Time + Sales Count
    """)


if __name__ == "__main__":
    app()
