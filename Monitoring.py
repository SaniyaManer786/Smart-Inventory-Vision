







# import streamlit as st
# import cv2
# import numpy as np
# import subprocess
# import json
# from utils import analyze_shelf
# import time

# # 🔥 PRODUCT CLASS MAPPING: YOLO class ID → Product Name
# PRODUCT_CLASS_MAP = {
#     39: "bottle",        # YOLO class 39 → "bottle" 
#     40: "wine glass",
#     41: "cup", 
#     44: "knife",
#     46: "banana",
#     56: "chair",
#     65: "cell phone",    # YOLO class 65 → "cell phone"
#     73: "laptop",
#     24: "backpack"
# }

# def app():
#     st.markdown(
#         "<h1 style='text-align: center; color: #1e3a8a; font-size: 3rem;'>📸 LIVE SHELF MONITORING</h1>",
#         unsafe_allow_html=True
#     )

#     st.markdown("""
#         <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         </style>
#     """, unsafe_allow_html=True)

#     # ✅ SHARED DATA for Predictive page - NOW USES PRODUCT NAMES!
#     if 'monitoring_data' not in st.session_state:
#         st.session_state.monitoring_data = {
#             'frame': None,
#             'annotated': None,
#             'counts': {},        # {"bottle": 2, "cell phone": 1} - NAMES!
#             'total_products': 0,
#             'total_people': 0,
#             'last_update': 0
#         }
    
#     if 'monitoring_active' not in st.session_state:
#         st.session_state.monitoring_active = False
#     if 'cap' not in st.session_state:
#         st.session_state.cap = None
#     if 'last_alert_time' not in st.session_state:
#         st.session_state.last_alert_time = 0

#     def speak_alert(product_name):
#         alert_msg = f"Attention! Low stock on {product_name}"
#         safe_text = json.dumps(alert_msg)
#         voice_code = f"""
# import pyttsx3
# engine = pyttsx3.init()
# engine.setProperty('rate', 180)
# voices = engine.getProperty('voices')
# if len(voices) > 1:
#     engine.setProperty('voice', voices[1].id)
# engine.say({safe_text})
# engine.runAndWait()
# """
#         subprocess.Popen(["python", "-c", voice_code], 
#                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         return alert_msg

#     # START/STOP BUTTONS
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         if st.button("🚀 START MONITORING", type="primary", use_container_width=True, 
#                     disabled=st.session_state.monitoring_active):
#             st.session_state.monitoring_active = True
#             st.session_state.cap = cv2.VideoCapture(0)
#             st.session_state.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
#             st.session_state.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    
#     with col2:
#         if st.button("⏹️ STOP MONITORING", type="secondary", 
#                     disabled=not st.session_state.monitoring_active):
#             st.session_state.monitoring_active = False
#             if st.session_state.cap:
#                 st.session_state.cap.release()
#                 st.session_state.cap = None
#             st.session_state.monitoring_data = {'last_update': 0}
#             st.session_state.last_alert_time = 0
#             st.success("🛑 Monitoring stopped!")

#     # ✅ MONITORING LOOP - CLASS ID → PRODUCT NAME CONVERSION
#     if st.session_state.monitoring_active and st.session_state.cap:
#         video_frame = st.empty()
#         metrics_frame = st.empty()

#         while st.session_state.monitoring_active:
#             success, frame = st.session_state.cap.read()
#             if not success:
#                 st.error("❌ No camera detected")
#                 break

#             frame = cv2.flip(frame, 1)

#             # YOLO ANALYSIS
#             annotated, all_counts, total_all = analyze_shelf(frame)
            
#             # 🔥 CRITICAL: Convert CLASS IDs → PRODUCT NAMES!
#             counts_by_name = {}
#             for class_id, count in all_counts.items():
#                 if class_id in PRODUCT_CLASS_MAP:
#                     product_name = PRODUCT_CLASS_MAP[class_id]
#                     counts_by_name[product_name] = count
            
#             # Filter people (class 0)
#             total_people = all_counts.get(0, 0)
#             total_products = sum(counts_by_name.values())

#             # ✅ UPDATE SHARED DATA - PRODUCT NAMES for Predictive!
#             st.session_state.monitoring_data = {
#                 'frame': frame,
#                 'annotated': annotated,
#                 'counts': counts_by_name,      # {"bottle": 2, "cell phone": 1} ✅
#                 'total_products': total_products,
#                 'total_people': total_people,
#                 'last_update': time.time()
#             }

#             # DISPLAY VIDEO
#             video_frame.image(annotated, channels="BGR", width=900)

#             # METRICS
#             with metrics_frame.container():
#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     st.metric("📦 **PRODUCTS**", total_products)
#                 with col2:
#                     st.metric("👥 **PEOPLE**", total_people)
#                 with col3:
#                     if counts_by_name:
#                         top_product = max(counts_by_name.items(), key=lambda x: x[1])
#                         st.metric("⭐ **TOP**", f"{top_product[0]}: {top_product[1]}")
#                     else:
#                         st.metric("⭐ **TOP**", "None")

#                 # LOW STOCK ALERT
#                 current_time = time.time()
#                 if total_products < 3:
#                     if (current_time - st.session_state.last_alert_time) > 10:
#                         top_product_name = max(counts_by_name.keys(), key=(lambda k: counts_by_name[k])) if counts_by_name else "shelf"
#                         alert_msg = speak_alert(top_product_name)
#                         st.error(f"🚨 SPOKE: {alert_msg}")
#                         st.session_state.last_alert_time = current_time
#                     else:
#                         st.error("🚨 LOW STOCK - Restock shelf!")
#                 else:
#                     st.success("✅ Good Stock Levels")

#             time.sleep(0.07)

#     # STATUS - Predictive receives LIVE product names!
#     if st.session_state.monitoring_data['last_update'] > 0:
#         st.sidebar.success("✅ Predictive page receiving LIVE product counts!")
#         st.sidebar.metric("📦 Products", st.session_state.monitoring_data.get('total_products', 0))
#         st.sidebar.metric("👥 People", st.session_state.monitoring_data.get('total_people', 0))
        
#         # Show current counts
#         if st.session_state.monitoring_data['counts']:
#             st.sidebar.subheader("📊 LIVE COUNTS")
#             for product, count in st.session_state.monitoring_data['counts'].items():
#                 st.sidebar.metric(product.title(), count)
#     else:
#         st.sidebar.info("👆 Click START MONITORING first")

# if __name__ == "__main__":
#     app()








import streamlit as st
import numpy as np
from PIL import Image
from utils import analyze_shelf
import time

# =========================================================
# PRODUCT CLASS MAPPING
# YOLO class ID -> Product Name
# =========================================================
PRODUCT_CLASS_MAP = {
    39: "bottle",
    40: "wine glass",
    41: "cup",
    44: "knife",
    46: "banana",
    56: "chair",
    65: "cell phone",
    73: "laptop",
    24: "backpack"
}


# =========================================================
# BROWSER VOICE ALERT
# Works on deployed Streamlit app
# =========================================================
def browser_speak(message):
    """
    Speak an alert in the user's browser instead of
    trying to use pyttsx3 on the Render server.
    """

    # Escape characters that could break JavaScript
    safe_message = (
        message
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", " ")
    )

    st.components.v1.html(
        f"""
        <script>
        const message = new SpeechSynthesisUtterance('{safe_message}');
        message.rate = 1.0;
        message.pitch = 1.0;
        message.volume = 1.0;

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(message);
        </script>
        """,
        height=0,
    )


# =========================================================
# MAIN APP
# =========================================================
def app():

    # -----------------------------------------------------
    # PAGE TITLE
    # -----------------------------------------------------
    st.markdown(
        """
        <h1 style="
            text-align:center;
            color:#1e3a8a;
            font-size:3rem;
        ">
            📸 SMART SHELF MONITORING
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .block-container {
            padding-top: 2rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "📷 Take a picture of the shelf. "
        "YOLO will detect products and update the inventory monitoring data."
    )

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "monitoring_data" not in st.session_state:

        st.session_state.monitoring_data = {

            "frame": None,

            "annotated": None,

            # Product names instead of YOLO IDs
            "counts": {},

            "total_products": 0,

            "total_people": 0,

            "last_update": 0
        }

    if "last_alert_time" not in st.session_state:
        st.session_state.last_alert_time = 0

    # =====================================================
    # CAMERA
    # =====================================================

    st.subheader("📷 Shelf Camera")

    camera_image = st.camera_input(
        "Take a photo of the shelf"
    )

    # =====================================================
    # PROCESS CAMERA IMAGE
    # =====================================================

    if camera_image is not None:

        # Convert uploaded camera image to PIL
        image = Image.open(camera_image).convert("RGB")

        # Convert PIL -> NumPy
        frame = np.array(image)

        st.subheader("📸 Captured Shelf")

        st.image(
            image,
            caption="Shelf Image",
            use_container_width=True
        )

        # -------------------------------------------------
        # ANALYZE BUTTON
        # -------------------------------------------------

        if st.button(
            "🔍 ANALYZE SHELF",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 YOLO is analyzing the shelf..."
            ):

                # =========================================
                # YOLO ANALYSIS
                # =========================================

                annotated, all_counts, total_all = (
                    analyze_shelf(frame)
                )

                # =========================================
                # CLASS ID -> PRODUCT NAME
                # =========================================

                counts_by_name = {}

                for class_id, count in all_counts.items():

                    # Convert NumPy / float class IDs to int
                    class_id = int(class_id)

                    if class_id in PRODUCT_CLASS_MAP:

                        product_name = (
                            PRODUCT_CLASS_MAP[class_id]
                        )

                        counts_by_name[product_name] = int(
                            count
                        )

                # =========================================
                # PEOPLE COUNT
                # YOLO COCO class 0 = person
                # =========================================

                total_people = int(
                    all_counts.get(0, 0)
                )

                # =========================================
                # TOTAL PRODUCT COUNT
                # =========================================

                total_products = sum(
                    counts_by_name.values()
                )

                # =========================================
                # SAVE DATA FOR PREDICTIVE PAGE
                # =========================================

                st.session_state.monitoring_data = {

                    "frame": frame,

                    "annotated": annotated,

                    "counts": counts_by_name,

                    "total_products": total_products,

                    "total_people": total_people,

                    "last_update": time.time()
                }

            # =============================================
            # SUCCESS
            # =============================================

            st.success(
                "✅ Shelf analysis completed!"
            )

            # =============================================
            # ANNOTATED IMAGE
            # =============================================

            st.subheader(
                "🤖 YOLO Detection Result"
            )

            # results.plot() from Ultralytics returns BGR
            st.image(
                annotated,
                channels="BGR",
                caption="Detected Products",
                use_container_width=True
            )

            # =============================================
            # METRICS
            # =============================================

            st.subheader(
                "📊 Live Shelf Statistics"
            )

            col1, col2, col3 = st.columns(3)

            # ---------------------------------------------
            # PRODUCTS
            # ---------------------------------------------

            with col1:

                st.metric(
                    "📦 PRODUCTS",
                    total_products
                )

            # ---------------------------------------------
            # PEOPLE
            # ---------------------------------------------

            with col2:

                st.metric(
                    "👥 PEOPLE",
                    total_people
                )

            # ---------------------------------------------
            # TOP PRODUCT
            # ---------------------------------------------

            with col3:

                if counts_by_name:

                    top_product = max(
                        counts_by_name.items(),
                        key=lambda x: x[1]
                    )

                    st.metric(
                        "⭐ TOP PRODUCT",
                        f"{top_product[0].title()}: "
                        f"{top_product[1]}"
                    )

                else:

                    st.metric(
                        "⭐ TOP PRODUCT",
                        "None"
                    )

            # =============================================
            # PRODUCT COUNTS
            # =============================================

            st.subheader(
                "📦 Detected Product Counts"
            )

            if counts_by_name:

                product_columns = st.columns(
                    min(len(counts_by_name), 4)
                )

                for index, (product, count) in enumerate(
                    counts_by_name.items()
                ):

                    with product_columns[
                        index % len(product_columns)
                    ]:

                        st.metric(
                            product.title(),
                            count
                        )

            else:

                st.warning(
                    "⚠️ No mapped products detected."
                )

            # =============================================
            # STOCK STATUS
            # =============================================

            st.subheader(
                "🚨 Stock Status"
            )

            current_time = time.time()

            if total_products < 3:

                # -----------------------------------------
                # Find product for alert
                # -----------------------------------------

                if counts_by_name:

                    top_product_name = max(
                        counts_by_name,
                        key=counts_by_name.get
                    )

                else:

                    top_product_name = "shelf"

                alert_msg = (
                    f"Attention! Low stock on "
                    f"{top_product_name}"
                )

                st.error(
                    f"🚨 LOW STOCK: {alert_msg}"
                )

                # -----------------------------------------
                # Browser voice alert
                # -----------------------------------------

                if (
                    current_time
                    - st.session_state.last_alert_time
                    > 10
                ):

                    browser_speak(alert_msg)

                    st.session_state.last_alert_time = (
                        current_time
                    )

            else:

                st.success(
                    "✅ Good Stock Levels"
                )

    # =====================================================
    # NO CAMERA IMAGE
    # =====================================================

    else:

        st.warning(
            "👆 Open the camera and take a shelf photo "
            "to start monitoring."
        )

    # =====================================================
    # SIDEBAR - SHARED DATA
    # =====================================================

    monitoring_data = (
        st.session_state.monitoring_data
    )

    if monitoring_data.get(
        "last_update", 0
    ) > 0:

        st.sidebar.success(
            "✅ Predictive page receiving product counts!"
        )

        st.sidebar.metric(
            "📦 Products",
            monitoring_data.get(
                "total_products",
                0
            )
        )

        st.sidebar.metric(
            "👥 People",
            monitoring_data.get(
                "total_people",
                0
            )
        )

        # ---------------------------------------------
        # LIVE COUNTS
        # ---------------------------------------------

        counts = monitoring_data.get(
            "counts",
            {}
        )

        if counts:

            st.sidebar.subheader(
                "📊 CURRENT COUNTS"
            )

            for product, count in counts.items():

                st.sidebar.metric(
                    product.title(),
                    count
                )

        # ---------------------------------------------
        # LAST UPDATE
        # ---------------------------------------------

        last_update = monitoring_data.get(
            "last_update",
            0
        )

        if last_update:

            update_time = time.strftime(
                "%H:%M:%S",
                time.localtime(last_update)
            )

            st.sidebar.caption(
                f"Last analysis: {update_time}"
            )

    else:

        st.sidebar.info(
            "📷 Take and analyze a shelf photo first."
        )


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":
    app()
























