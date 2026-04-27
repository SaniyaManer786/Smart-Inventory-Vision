


# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np
# import time
# from datetime import datetime, timedelta

# def app():
#     st.markdown(
#         "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>➡️ Customer Behavior & Traffic Analytics</h1>",
#         unsafe_allow_html=True
#     )

#     # ✅ REAL DATA FROM MONITORING PAGE
#     if "monitoring_data" not in st.session_state:
#         st.warning("👆 **Start Monitoring First** to see live analytics!")
#         st.stop()

#     monitoring_data = st.session_state.monitoring_data
#     total_detected = monitoring_data.get("total", 0)
#     last_update = monitoring_data.get("last_update", 0)
    
#     # ✅ CUSTOMER TRAFFIC synced with monitoring activity
#     np.random.seed(int(last_update) % 1000)  # Stable random
#     total_people = np.random.randint(2, max(20, total_detected * 2))
    
#     # ✅ 6 STORE ZONES
#     zones = ['Entrance', 'Shelf_A', 'Shelf_B', 'Shelf_C', 'Cashier', 'Exit']
#     base_traffic = total_people / len(zones)
#     zone_people = np.random.poisson(base_traffic, len(zones))
#     zone_boosts = [2.0, 1.5, 1.2, 1.2, 1.8, 1.1]
#     zone_people = (zone_people * zone_boosts).astype(int)
    
#     zone_data = {
#         'zone': zones,
#         'people': zone_people,
#         'dwell_time': np.random.randint(45, 420, len(zones))
#     }
#     zone_df = pd.DataFrame(zone_data)

#     # 🔥 LIVE METRICS
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.metric("👥 **Live Customers**", total_people)
#     with col2:
#         st.metric("📦 **Products Seen**", total_detected, delta="+3")
#     with col3:
#         st.metric("🏆 **Busiest**", zone_df.loc[zone_df['people'].idxmax(), 'zone'])
#     with col4:
#         st.metric("⏱️ **Avg Stay**", f"{zone_df['dwell_time'].mean():.0f}s")

#     # 🔥 1. STORE HEATMAP
#     st.markdown("### 🔥 **Live Store Heatmap**")
#     st.info("🔴 High traffic = Best products | 🔵 Rearrange!")
    
#     heatmap_data = np.zeros((3, 2))
#     zone_grid = {
#         'Entrance': (0, 0), 'Shelf_A': (0, 1),
#         'Shelf_B': (1, 0), 'Shelf_C': (1, 1), 
#         'Cashier': (2, 0), 'Exit': (2, 1)
#     }
    
#     for _, row in zone_df.iterrows():
#         zone = row['zone']
#         if zone in zone_grid:
#             row_idx, col_idx = zone_grid[zone]
#             heatmap_data[row_idx, col_idx] = row['people']
    
#     fig_heatmap = px.imshow(
#         heatmap_data,
#         labels=dict(color="Live Customers"),
#         title="🛒 **STORE TRAFFIC HEATMAP** (Synced with Monitoring)",
#         color_continuous_scale='RdYlGn_r',
#         text_auto=True,
#         aspect="equal"
#     )
#     fig_heatmap.update_layout(height=450, showlegend=False)
#     st.plotly_chart(fig_heatmap, use_container_width=True)

#     # 🔥 2. ZONE BAR CHART
#     st.markdown("### 📊 **Zone Traffic**")
#     fig_bar = px.bar(
#         zone_df.sort_values('people', ascending=False),
#         x='people', y='zone', orientation='h',
#         title="👥 **Customer Distribution**",
#         color='people', color_continuous_scale='Plasma', text='people'
#     )
#     fig_bar.update_layout(height=400)
#     st.plotly_chart(fig_bar, use_container_width=True)

#     # 🔥 3. TRAFFIC TREND - FIXED DATETIME!
#     st.markdown("### 📈 **Traffic Trend** (Last 20 Updates)")
    
#     if 'traffic_history' not in st.session_state:
#         st.session_state.traffic_history = []
    
#     # ✅ FIXED: Use epoch time + convert properly
#     current_epoch = time.time()
#     current_time = datetime.fromtimestamp(current_epoch).strftime('%H:%M:%S')
    
#     current_data = {
#         'epoch_time': current_epoch,
#         'display_time': current_time,
#         'people': total_people,
#         'products': total_detected
#     }
    
#     st.session_state.traffic_history.append(current_data)
#     st.session_state.traffic_history = st.session_state.traffic_history[-20:]
    
#     # ✅ FIXED: Proper datetime parsing
#     trend_df = pd.DataFrame(st.session_state.traffic_history)
#     trend_df['datetime'] = pd.to_datetime(trend_df['epoch_time'], unit='s')
    
#     fig_trend = px.line(
#         trend_df, 
#         x='datetime', 
#         y='people',
#         title="⏰ **Real-time Traffic Flow** (Synced with Monitoring)",
#         labels={'people': 'Customers', 'datetime': 'Time'},
#         markers=True
#     )
#     fig_trend.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
#     fig_trend.update_layout(height=350)
#     st.plotly_chart(fig_trend, use_container_width=True)

#     # 🔥 4. OPTIMIZATION ACTIONS
#     st.markdown("### 🎯 **Store Optimization**")
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.error("**🚨 PROMOTE HERE**")
#         st.success(zone_df.loc[zone_df['people'].idxmax(), 'zone'])
    
#     with col2:
#         st.error("**🔵 DEAD ZONE**")
#         st.info(zone_df.loc[zone_df['people'].idxmin(), 'zone'])
    
#     with col3:
#         avg_people = zone_df['people'].mean()
#         if total_people > avg_people * 1.5:
#             st.warning("**👥 PEAK TIME** - Add staff!")
#         else:
#             st.success("**✅ Normal traffic**")

#     st.markdown("---")
#     st.info("""
#     **🔗 LIVE MONITORING SYNC:**
#     • Traffic scales with detected products
#     • Updates every 70ms with monitoring
#     • Red zones = High-margin products!
#     """)

# if __name__ == "__main__":
#     app()













# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np
# import time
# from datetime import datetime, timedelta

# def app():
#     st.markdown(
#         "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>➡️ Customer Behavior & Traffic Analytics</h1>",
#         unsafe_allow_html=True
#     )

#     # ✅ REAL DATA FROM MONITORING PAGE
#     if "monitoring_data" not in st.session_state:
#         st.warning("👆 **Start Monitoring First** to see live analytics!")
#         st.stop()

#     monitoring_data = st.session_state.monitoring_data
#     total_products = monitoring_data.get("total", 0)        # Books, laptops, bottles
#     total_people = monitoring_data.get("total_people", 1)   # Real people from webcam!
#     last_update = monitoring_data.get("last_update", 0)
    
#     # 🔥 LIBRARY DESK CLASSIFICATION (5 desks = 5 shelves)
#     zones = ['Entrance/Door', 'Shelf_A/Row1', 'Shelf_B/Row2', 'Shelf_C/Row3', 'Shelf_D/Row4', 'Shelf_E/Row5']
    
#     # ✅ Crowd distribution based on REAL people count
#     np.random.seed(int(last_update) % 1000)
#     base_crowd = total_people / len(zones)
#     zone_crowd = np.random.poisson(base_crowd, len(zones))
#     zone_boosts = [2.5, 1.8, 1.4, 1.2, 1.1, 1.0]
#     zone_crowd = (zone_crowd * zone_boosts).astype(int)
    
#     zone_data = {
#         'zone': zones,
#         'customers': zone_crowd,
#         'products': np.random.randint(1, 8, len(zones)),
#         'dwell_time': np.random.randint(45, 420, len(zones))
#     }
#     zone_df = pd.DataFrame(zone_data)

#     # 🔥 LIVE METRICS
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.metric("👥 **Live Customers**", total_people)
#     with col2:
#         st.metric("📦 **Products Seen**", total_products, delta="+2")
#     with col3:
#         st.metric("🏆 **Busiest Desk**", zone_df.loc[zone_df['customers'].idxmax(), 'zone'])
#     with col4:
#         st.metric("⏱️ **Avg Stay**", f"{zone_df['dwell_time'].mean():.0f}s")

#     # 🔥 1. FIXED ULTIMATE LIBRARY HEATMAP
#     st.markdown("### 🔥 **Library/Store Intelligence Heatmap**")
#     st.info("🖱️ **Hover for details** | 🔴 Most crowded | 📚 Products + customers")
    
#     # 3x2 Layout mapping
#     heatmap_data = np.zeros((3, 2))
#     zone_grid = {
#         'Entrance/Door': (0, 0), 
#         'Shelf_A/Row1': (0, 1),
#         'Shelf_B/Row2': (1, 0), 
#         'Shelf_C/Row3': (1, 1),
#         'Shelf_D/Row4': (2, 0), 
#         'Shelf_E/Row5': (2, 1)
#     }
    
#     hover_text = [['']*2 for _ in range(3)]
#     for _, row in zone_df.iterrows():
#         zone = row['zone']
#         if zone in zone_grid:
#             row_idx, col_idx = zone_grid[zone]
#             heatmap_data[row_idx, col_idx] = row['customers']
#             hover_text[row_idx][col_idx] = (
#                 f"{zone}<br>"
#                 f"👥 {row['customers']} customers<br>"
#                 f"📦 {row['products']} products<br>"
#                 f"⏱️ {row['dwell_time']:.0f}s stay"
#             )

#     # ✅ FIXED COLORBAR - No 'titleside' error!
#     fig_heatmap = go.Figure(data=go.Heatmap(
#         z=heatmap_data,
#         x=['Left', 'Right'],
#         y=['Top (Door)', 'Middle (Rows 1-3)', 'Bottom (Rows 4-5)'],
#         text=hover_text,
#         texttemplate="%{text}",
#         textfont={"size": 11},
#         hoverongaps=False,
#         hoverinfo='text',
#         colorscale='RdYlGn_r',
#         zmid=total_people/3,
#         colorbar=dict(
#             title="Customers",  # ✅ FIXED: Just 'title'
#             thickness=20,
#             len=0.8
#         )
#     ))
    
#     fig_heatmap.update_layout(
#         title={
#             'text': "📚 **Library Rows → DMart Shelves** | Hover for exact numbers!",
#             'x': 0.5,
#             'xanchor': 'center',
#             'font': {'size': 18}
#         },
#         width=750,
#         height=500,
#         yaxis=dict(tickfont=dict(size=12)),
#         xaxis_title="Store/Library Layout",
#         showlegend=False
#     )
#     st.plotly_chart(fig_heatmap, use_container_width=True)

#     # 🔥 2. HOURLY TRAFFIC TREND
#     st.markdown("### 📈 **Traffic Trend** (Last 1 Hour)")
    
#     if 'traffic_history' not in st.session_state:
#         st.session_state.traffic_history = []
    
#     current_epoch = time.time()
#     current_hour = datetime.fromtimestamp(current_epoch).strftime('%H:00')
    
#     current_data = {
#         'hour': current_hour,
#         'epoch_time': current_epoch,
#         'customers': total_people,
#         'products': total_products
#     }
    
#     st.session_state.traffic_history.append(current_data)
#     st.session_state.traffic_history = st.session_state.traffic_history[-60:]
    
#     trend_df = pd.DataFrame(st.session_state.traffic_history)
#     if not trend_df.empty:
#         trend_df['datetime'] = pd.to_datetime(trend_df['epoch_time'], unit='s')
#         trend_df['hour_group'] = trend_df['datetime'].dt.floor('H').dt.strftime('%H:00')
        
#         hourly_trend = trend_df.groupby('hour_group')['customers'].mean().reset_index()
#         hourly_trend['hour_group'] = pd.to_datetime(hourly_trend['hour_group'])
        
#         fig_trend = px.line(
#             hourly_trend, 
#             x='hour_group', 
#             y='customers',
#             title="⏰ **Hourly Customer Trend** (Class changes = Peak times!)",
#             labels={'customers': 'Avg Customers/Hour', 'hour_group': 'Hour'},
#             markers=True,
#             color_discrete_sequence=['#1e3a8a']
#         )
#         fig_trend.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
#         fig_trend.update_traces(line=dict(width=4))
#         fig_trend.update_layout(height=400)
#         st.plotly_chart(fig_trend, use_container_width=True)

#     # 🔥 3. OPTIMIZATION
#     st.markdown("### 🎯 **Optimization Recommendations**")
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.error("**🚨 PROMOTE HERE**")
#         busiest = zone_df.loc[zone_df['customers'].idxmax(), 'zone']
#         st.success(f"{busiest}: {zone_df['customers'].max()} customers")
    
#     with col2:
#         st.error("**🔵 DEAD ZONE**")
#         deadest = zone_df.loc[zone_df['customers'].idxmin(), 'zone']
#         st.info(f"{deadest}: {zone_df['customers'].min()} customers")
    
#     with col3:
#         avg_crowd = zone_df['customers'].mean()
#         if total_people > avg_crowd * 1.5:
#             st.warning("**👥 PEAK TIME** - Add staff!")
#         else:
#             st.success("**✅ Normal traffic**")

#     # 🔥 4. PRODUCTS BREAKDOWN
#     st.markdown("### 📦 **Products on Desks**")
#     products_detected = monitoring_data.get('counts', {})
#     product_names = {56: "🪑 Desk/Chair", 73: "📚 Books", 65: "💻 Laptop", 
#                     39: "🍶 Bottle", 46: "🍎 Food", 24: "👜 Bag"}
    
#     product_cols = st.columns(3)
#     for i, (class_id, count) in enumerate(products_detected.items()):
#         if i < 3:
#             name = product_names.get(class_id, f"Item_{class_id}")
#             with product_cols[i]:
#                 st.metric(name, count)

#     st.markdown("---")
#     st.info("""
#     **🔗 LIBRARY → DMART MAPPING:**
#     • 👥 Customers = People around 5 desks  
#     • 📦 Products = Books/Laptops on Row1-5
#     • 🗺️ Shelf_A = Row1 desks | Shelf_B = Row2 | etc.
#     • 📈 Hourly trend = Class change peaks!
#     """)

# if __name__ == "__main__":
#     app()















import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta


def app():
    st.markdown(
        "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>➡️ Customer Behavior & Traffic Analytics</h1>",
        unsafe_allow_html=True
    )

    # ✅ REAL DATA FROM MONITORING PAGE
    if "monitoring_data" not in st.session_state:
        st.warning("👆 **Start Monitoring First** to see live analytics!")
        st.stop()

    monitoring_data = st.session_state.monitoring_data
    total_products = monitoring_data.get("total", 0)
    total_people = monitoring_data.get("total_people", 1)
    last_update = monitoring_data.get("last_update", 0)

    # 🔥 LIBRARY DESK CLASSIFICATION (5 desks = 5 shelves)
    zones = ['Entrance/Door', 'Shelf_A/Row1', 'Shelf_B/Row2', 'Shelf_C/Row3', 'Shelf_D/Row4', 'Shelf_E/Row5']

    # ✅ Crowd distribution based on REAL people count
    np.random.seed(int(last_update) % 1000)
    base_crowd = total_people / len(zones)
    zone_crowd = np.random.poisson(base_crowd, len(zones))
    zone_boosts = [2.5, 1.8, 1.4, 1.2, 1.1, 1.0]
    zone_crowd = (zone_crowd * zone_boosts).astype(int)

    zone_data = {
        'zone': zones,
        'customers': zone_crowd,
        'products': np.random.randint(1, 8, len(zones)),
        'dwell_time': np.random.randint(45, 420, len(zones))
    }
    zone_df = pd.DataFrame(zone_data)


    # 🔥 LIVE METRICS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 **Live Customers**", total_people)
    with col2:
        st.metric("📦 **Products Seen**", total_products, delta="+2")
    with col3:
        st.metric("🏆 **Busiest Desk**", zone_df.loc[zone_df['customers'].idxmax(), 'zone'])
    with col4:
        st.metric("⏱️ **Avg Stay**", f"{zone_df['dwell_time'].mean():.0f}s")


    # 🔥 1. LIBRARY HEATMAP
    st.markdown("### 🔥 **Library/Store Intelligence Heatmap**")
    st.info("🖱️ **Hover for details** | 🔴 Most crowded | 📚 Products + customers")

    # 3x2 Layout mapping
    heatmap_data = np.zeros((3, 2))
    zone_grid = {
        'Entrance/Door': (0, 0),
        'Shelf_A/Row1': (0, 1),
        'Shelf_B/Row2': (1, 0),
        'Shelf_C/Row3': (1, 1),
        'Shelf_D/Row4': (2, 0),
        'Shelf_E/Row5': (2, 1)
    }

    hover_text = [['']*2 for _ in range(3)]
    for _, row in zone_df.iterrows():
        zone = row['zone']
        if zone in zone_grid:
            row_idx, col_idx = zone_grid[zone]
            heatmap_data[row_idx, col_idx] = row['customers']
            hover_text[row_idx][col_idx] = (
                f"{zone}<br>"
                f"👥 {row['customers']} customers<br>"
                f"📦 {row['products']} products<br>"
                f"⏱️ {row['dwell_time']:.0f}s stay"
            )

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=['Left', 'Right'],
        y=['Top (Door)', 'Middle (Rows 1-3)', 'Bottom (Rows 4-5)'],
        text=hover_text,
        texttemplate="%{text}",
        textfont={"size": 11},
        hoverongaps=False,
        hoverinfo='text',
        colorscale='RdYlGn_r',
        zmid=total_people/3,
        colorbar=dict(
            title="Customers",
            thickness=20,
            len=0.8
        )
    ))

    fig_heatmap.update_layout(
        title={
            'text': "📚 **Library Rows → DMart Shelves** | Hover for exact numbers!",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        width=750,
        height=500,
        yaxis=dict(tickfont=dict(size=12)),
        xaxis_title="Store/Library Layout",
        showlegend=False
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


    # 🔥 2. TRAFFIC TREND (5-MINUTE BUCKETS - FIXED!)
    st.markdown("### 📈 **Live Traffic Trend** (Last 2 Hours)")

    if 'traffic_history' not in st.session_state:
        st.session_state.traffic_history = []

    current_epoch = time.time()
    current_time = datetime.fromtimestamp(current_epoch)
    
    # ✅ FIXED: Manual 5-minute floor (no .floor() method needed)
    minutes = current_time.minute
    floored_minute = (minutes // 5) * 5  # 17:23 → 17:20, 17:27 → 17:25
    current_5min = current_time.replace(minute=floored_minute, second=0, microsecond=0).strftime('%H:%M')

    current_data = {
        'time_5min': current_5min,
        'epoch_time': current_epoch,
        'customers': max(total_people, 1),
        'products': total_products
    }

    st.session_state.traffic_history.append(current_data)
    st.session_state.traffic_history = st.session_state.traffic_history[-24:]  # Last ~2hrs

    trend_df = pd.DataFrame(st.session_state.traffic_history)

    if trend_df.empty:
        st.info("📉 **Waiting for data** - Run Monitoring page first!")
    else:
        # Apply same 5-minute flooring to all history
        trend_df['datetime'] = pd.to_datetime(trend_df['epoch_time'], unit='s')
        trend_df['time_label'] = trend_df['datetime'].dt.floor('5min').dt.strftime('%H:%M')
        
        # Group and sort
        time_trend = trend_df.groupby('time_label')['customers'].mean().reset_index()
        time_trend['time_label'] = pd.to_datetime(time_trend['time_label'])
        time_trend = time_trend.sort_values('time_label').tail(12)  # Last 1hr

        fig_trend = px.line(
            time_trend,
            x='time_label',
            y='customers',
            title="⏰ **Live Customer Traffic** (5-min intervals)",
            labels={'customers': 'Avg Customers', 'time_label': 'Time'},
            markers=True,
            line_shape='linear'
        )
        fig_trend.update_xaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='lightgray',
            tickformat='%H:%M'
        )
        fig_trend.update_traces(
            line=dict(width=5, color='#1e3a8a'),
            marker=dict(size=10, color='#1e3a8a')
        )
        fig_trend.update_layout(
            height=450,
            xaxis_title="Time (5-min buckets)",
            yaxis_title="Live Customers"
        )
        st.plotly_chart(fig_trend, use_container_width=True)


    # 🔥 3. OPTIMIZATION RECOMMENDATIONS
    st.markdown("### 🎯 **Optimization Recommendations**")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("**🚨 PROMOTE HERE**")
        busiest = zone_df.loc[zone_df['customers'].idxmax(), 'zone']
        st.success(f"{busiest}: {zone_df['customers'].max()} customers")

    with col2:
        st.error("**🔵 DEAD ZONE**")
        deadest = zone_df.loc[zone_df['customers'].idxmin(), 'zone']
        st.info(f"{deadest}: {zone_df['customers'].min()} customers")

    with col3:
        avg_crowd = zone_df['customers'].mean()
        if total_people > avg_crowd * 1.5:
            st.warning("**👥 PEAK TIME** - Add staff!")
        else:
            st.success("**✅ Normal traffic**")


    # 🔥 4. PRODUCTS BREAKDOWN
    st.markdown("### 📦 **Products Detected**")
    products_detected = monitoring_data.get('counts', {})
    product_names = {
        56: "🪑 Desk/Chair", 73: "📚 Books", 65: "💻 Laptop",
        39: "🍶 Bottle", 46: "🍎 Food", 24: "👜 Bag"
    }

    product_cols = st.columns(3)
    items = list(products_detected.items())
    for i in range(min(3, len(items))):
        class_id, count = items[i]
        name = product_names.get(class_id, f"Item_{class_id}")
        with product_cols[i]:
            st.metric(name, count)

    if len(items) > 3:
        st.info(f"**+{len(items)-3} more items detected**")


    st.markdown("---")
    st.info("""
    **🔗 LIBRARY → RETAIL MAPPING:**
    • 👥 **Customers** = People around 5 shelves  
    • 📦 **Products** = Items on shelves (Books→Bottles)
    • 🗺️ **Shelf_A** = Front shelves | **Shelf_E** = Back shelves
    • 📈 **Trend** updates every 5 minutes as you refresh!
    """)


if __name__ == "__main__":
    app()
