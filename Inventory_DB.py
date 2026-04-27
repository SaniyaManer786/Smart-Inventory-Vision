






import sqlite3
import streamlit as st
from utils import analyze_shelf
from PIL import Image
import numpy as np
import pandas as pd
import time
from datetime import datetime


def app():
    st.title("5️⃣ Inventory Database (POS/ERP) - **PAST DATA PROTECTED** 🔒")
    
    # Connect to database with DATETIME parsing
    conn = sqlite3.connect('inventory.db', check_same_thread=False)
    c = conn.cursor()
    
    # ✅ Table exists check (KEEPS past data!)
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            stock_count INTEGER,
            sku TEXT,
            total_items INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    # 🔥 CLEAR HISTORY BUTTON
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ **CLEAR ALL HISTORY**", type="secondary"):
            c.execute("DELETE FROM inventory")
            conn.commit()
            st.success("✅ **ALL HISTORY CLEARED!**")
            st.rerun()
    
    # Read COMPLETE history + ✅ FIX DATETIME
    df = pd.read_sql("SELECT * FROM inventory ORDER BY timestamp DESC", conn)
    
    # 🔥 CRITICAL FIX: Convert string timestamps to datetime
    if len(df) > 0 and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    st.success(f"📊 **{len(df)} TOTAL RECORDS** preserved from monitoring!")
    
    # 🔥 LIVE MONITORING AUTO-SAVE
    if 'monitoring_data' in st.session_state and st.session_state.monitoring_data.get('last_update', 0) > 0:
        st.info("🔴 **LIVE MONITORING DETECTED** → Auto-saving...")
        
        live_counts = st.session_state.monitoring_data.get('counts', {})
        live_total = st.session_state.monitoring_data.get('total', 0)
        
        if live_counts:
            for sku, count in live_counts.items():
                c.execute('''
                    INSERT INTO inventory (product_name, stock_count, sku, total_items)
                    VALUES (?, ?, ?, ?)
                ''', (f"SKU_{sku}", int(count), str(sku), live_total))
            
            conn.commit()
            st.success(f"✅ **NEW LIVE DATA SAVED!**")  # 🎈 REMOVED!
            
            # Show latest scan
            st.subheader("🔴 **LATEST LIVE SCAN**")
            live_df = pd.DataFrame([
                {'product_name': f"SKU_{sku}", 'stock_count': count, 'sku': sku, 'total_items': live_total}
                for sku, count in live_counts.items()
            ])
            st.dataframe(live_df, use_container_width=True)
            
            # Refresh full table
            df = pd.read_sql("SELECT * FROM inventory ORDER BY timestamp DESC", conn)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 📊 COMPLETE HISTORY TABLE
    st.subheader("📜 **COMPLETE HISTORY** (Never auto-deletes)")
    st.dataframe(df, use_container_width=True, height=500)
    
    # 🔥 STATS - ✅ FIXED DATETIME!
    if len(df) > 0:
        st.markdown("### 📈 **Quick Stats**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total Records", len(df))
        
        with col2:
            recent = df.head(10)
            st.metric("🔴 Live Scans", recent['sku'].nunique())
        
        with col3:
            # ✅ FIXED: Safe datetime conversion
            first_date = df['timestamp'].min()
            if pd.notna(first_date):
                st.metric("⏰ First Record", first_date.strftime('%Y-%m-%d'))
            else:
                st.metric("⏰ First Record", "No data")
        
        with col4:
            last_time = df['timestamp'].max()
            if pd.notna(last_time):
                st.metric("📊 Last Update", last_time.strftime('%H:%M:%S'))
            else:
                st.metric("📊 Last Update", "No data")
    
    conn.close()
    
    st.sidebar.markdown("""
    **✅ DATA PROTECTION:**
    • 🔒 Past data **NEVER** deleted automatically
    • ➕ Live monitoring **ADDS** to history  
    • 🗑️ **Clear button REQUIRED** to delete
    • 📜 **Complete audit trail preserved**
    """)
    
    st.info("**🔒 HISTORY PROTECTED → Only delete when YOU click Clear!**")

if __name__ == "__main__":
    app()










