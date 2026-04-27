



# import streamlit as st
# import streamlit.components.v1 as components
# import time


# def speak(message):
#     components.html(f"""
#         <script>
#             var msg = new SpeechSynthesisUtterance("{message}");
#             msg.rate = 0.9;
#             msg.pitch = 1;
#             msg.volume = 1;
#             window.speechSynthesis.speak(msg);
#         </script>
#     """, height=0)


# def app():

#     st.markdown(
#         "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>📊 PLANOGRAM COMPLIANCE</h1>",
#         unsafe_allow_html=True
#     )

#     if 'monitoring_data' not in st.session_state:
#         st.error("🚫 Monitoring must be running first!")
#         st.stop()

#     if 'last_audio_alert' not in st.session_state:
#         st.session_state.last_audio_alert = 0

#     raw_counts = st.session_state.monitoring_data.get('counts', {})

#     # COCO class names
#     coco_classes = [
#         "Person","Bicycle","Car","Motorbike","Aeroplane","Bus","Train","Truck","Boat","Traffic Light",
#         "Fire Hydrant","Stop Sign","Parking Meter","Bench","Bird","Cat","Dog","Horse","Sheep","Cow",
#         "Elephant","Bear","Zebra","Giraffe","Backpack","Umbrella","Handbag","Tie","Suitcase","Frisbee",
#         "Skis","Snowboard","Sports Ball","Kite","Baseball Bat","Baseball Glove","Skateboard","Surfboard","Tennis Racket","Bottle",
#         "Wine Glass","Cup","Fork","Knife","Spoon","Bowl","Banana","Apple","Sandwich","Orange",
#         "Broccoli","Carrot","Hot Dog","Pizza","Donut","Cake","Chair","Sofa","Potted Plant","Bed",
#         "Dining Table","Toilet","TV","Laptop","Mouse","Remote","Keyboard","Cell Phone","Microwave","Oven",
#         "Toaster","Sink","Refrigerator","Book","Clock","Vase","Scissors","Teddy Bear","Hair Dryer","Toothbrush"
#     ]

#     # Convert IDs → names
#     clean_counts = {}

#     for key, count in raw_counts.items():
#         class_id = int(float(key))
#         count = int(float(count))

#         if count > 0 and class_id < len(coco_classes):
#             name = coco_classes[class_id]
#             clean_counts[name] = count

#     # Webcam display
#     if clean_counts:
#         webcam_text = ", ".join(
#             [f"{name}({count})" for name, count in clean_counts.items()]
#         )
#     else:
#         webcam_text = "None"

#     st.markdown(f"### 📷 WEBCAM: {webcam_text}")

#     # Misplaced logic (highest count = correct)
#     total_misplaced = 0
#     misplaced_item_name = None
#     misplaced_item_count = 0

#     if len(clean_counts) <= 1:
#         total_misplaced = 0
#     else:
#         correct_item = max(clean_counts.items(), key=lambda x: x[1])

#         for name, count in clean_counts.items():
#             if name != correct_item[0]:
#                 total_misplaced += count
#                 misplaced_item_name = name
#                 misplaced_item_count = count

#     # Display
#     st.markdown(f"### 📦 Misplaced Count: {total_misplaced}")

#     if total_misplaced > 0:
#         st.markdown(f"### 🍟 Misplaced Item: {misplaced_item_name} ({misplaced_item_count})")
#     else:
#         st.markdown("### 🍟 Misplaced Item: None")

#     st.markdown("### 📍 Shelf: A1")

#     current_time = time.time()

#     # Alert system
#     if total_misplaced > 0:

#         message = f"Shelf A1 has {misplaced_item_count} {misplaced_item_name} misplaced"

#         if (current_time - st.session_state.last_audio_alert) > 12:
#             speak(message)
#             st.session_state.last_audio_alert = current_time

#     else:
#         if st.session_state.last_audio_alert != 0:
#             speak("Shelf A1 Perfect")
#             st.session_state.last_audio_alert = 0

#         st.markdown("### ✅ Shelf A1 Perfect")

















import streamlit as st
import streamlit.components.v1 as components
import time

def speak(message):
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{message}");
            msg.rate = 0.9;
            msg.pitch = 1;
            msg.volume = 1;
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

def app():
    st.markdown(
        "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>📊 PLANOGRAM COMPLIANCE</h1>",
        unsafe_allow_html=True
    )

    if 'monitoring_data' not in st.session_state:
        st.error("🚫 Monitoring must be running first!")
        st.stop()

    if 'last_audio_alert' not in st.session_state:
        st.session_state.last_audio_alert = 0

    raw_counts = st.session_state.monitoring_data.get('counts', {})

    # 🔥 FIXED: Handle BOTH class IDs AND product names!
    clean_counts = {}
    
    for key, count in raw_counts.items():
        try:
            # Try parsing as class ID (old format)
            class_id = int(float(key))
            # COCO class names
            coco_classes = [
                "Person","Bicycle","Car","Motorbike","Aeroplane","Bus","Train","Truck","Boat","Traffic Light",
                "Fire Hydrant","Stop Sign","Parking Meter","Bench","Bird","Cat","Dog","Horse","Sheep","Cow",
                "Elephant","Bear","Zebra","Giraffe","Backpack","Umbrella","Handbag","Tie","Suitcase","Frisbee",
                "Skis","Snowboard","Sports Ball","Kite","Baseball Bat","Baseball Glove","Skateboard","Surfboard","Tennis Racket","Bottle",
                "Wine Glass","Cup","Fork","Knife","Spoon","Bowl","Banana","Apple","Sandwich","Orange",
                "Broccoli","Carrot","Hot Dog","Pizza","Donut","Cake","Chair","Sofa","Potted Plant","Bed",
                "Dining Table","Toilet","TV","Laptop","Mouse","Remote","Keyboard","Cell Phone","Microwave","Oven",
                "Toaster","Sink","Refrigerator","Book","Clock","Vase","Scissors","Teddy Bear","Hair Dryer","Toothbrush"
            ]
            
            if class_id < len(coco_classes) and class_id != 0:  # Skip Person
                name = coco_classes[class_id]
                clean_counts[name] = int(count)
                
        except (ValueError, TypeError):
            # NEW FORMAT: Direct product names from updated Monitoring!
            if isinstance(key, str) and count > 0:
                clean_counts[key] = int(count)

    # Display detected products
    if clean_counts:
        webcam_items = [f"{name}({count})" for name, count in clean_counts.items()]
        webcam_text = ", ".join(webcam_items)
    else:
        webcam_text = "None"

    st.markdown(f"### 📷 **WEBCAM DETECTED:** {webcam_text}")

    # Planogram compliance logic
    total_misplaced = 0
    misplaced_item_name = None
    misplaced_item_count = 0

    if len(clean_counts) <= 1:
        total_misplaced = 0
    else:
        # Highest count = "correct" item for shelf A1
        correct_item = max(clean_counts.items(), key=lambda x: x[1])
        
        for name, count in clean_counts.items():
            if name != correct_item[0]:
                total_misplaced += count
                misplaced_item_name = name
                misplaced_item_count = count

    # DASHBOARD
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 **Total Products**", sum(clean_counts.values()))
    with col2:
        st.metric("❌ **Misplaced**", total_misplaced)
    with col3:
        st.metric("✅ **Correct**", sum(clean_counts.values()) - total_misplaced)
    with col4:
        st.metric("📍 **Shelf**", "A1")

    if total_misplaced > 0:
        st.error(f"### 🍟 **MISPLACED:** {misplaced_item_name} ({misplaced_item_count})")
    else:
        st.success("### ✅ **Shelf A1 Perfect!**")

    # AUDIO ALERTS - NO BALLOONS
    current_time = time.time()
    if total_misplaced > 0:
        message = f"Shelf A1 has {misplaced_item_count} {misplaced_item_name} in wrong position"
        if (current_time - st.session_state.last_audio_alert) > 12:
            speak(message)
            st.session_state.last_audio_alert = current_time
            # ❌ NO st.balloons() - Clean alerts only
    else:
        if st.session_state.last_audio_alert != 0:
            speak("Shelf A1 Perfect")
            st.session_state.last_audio_alert = 0

    # LIVE COUNTS TABLE
    if clean_counts:
        st.subheader("📊 **DETECTED PRODUCTS**")
        df_data = [{"Product": name, "Count": count} for name, count in clean_counts.items()]
        st.dataframe(df_data, use_container_width=True)

if __name__ == "__main__":
    app()
