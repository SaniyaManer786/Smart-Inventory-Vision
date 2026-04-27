# import streamlit as st

# # ✅ IMPORT FEATURE FILES (make sure file names match exactly)
# import Analytics
# import Inventory_DB
# import Monitoring
# import Planogram
# import Predictive


# # ---------------------------------------------------
# # PAGE CONFIG
# # ---------------------------------------------------
# st.set_page_config(
#     page_title="🛒 Retail CV Inventory",
#     page_icon="🛒",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.set_option("client.showSidebarNavigation", False)


# # ---------------------------------------------------
# # FORCE DEFAULT PAGE ON EVERY FRESH RUN
# # ---------------------------------------------------
# if "page" not in st.session_state:
#     st.session_state.page = "🏠 Home"


# # ---------------------------------------------------
# # CUSTOM CSS
# # ---------------------------------------------------
# st.markdown("""
# <style>
# [data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #e8f4fd 0%, #b3d9ff 50%, #80bfff 100%);
# }

# .sidebar-title {
#     text-align: center;
#     font-size: 1.6rem;
#     font-weight: 800;
#     color: #0f172a;
#     margin-bottom: 1.5rem;
#     padding-bottom: 0.5rem;
#     border-bottom: 2px solid #1e3a8a;
# }

# div[role="radiogroup"] > label {
#     background-color: rgba(255,255,255,0.4);
#     padding: 0.6rem 1rem;
#     margin: 0.4rem 0;
#     border-radius: 10px;
#     font-weight: 600;
#     color: #0f172a;
#     transition: all 0.3s ease;
# }

# div[role="radiogroup"] > label:hover {
#     background-color: #1e3a8a;
#     color: white;
#     transform: translateX(5px);
# }
# </style>
# """, unsafe_allow_html=True)


# # ---------------------------------------------------
# # SIDEBAR NAVIGATION
# # ---------------------------------------------------
# with st.sidebar:
#     st.markdown("<div class='sidebar-title'>🧭 Navigation</div>", unsafe_allow_html=True)

#     page = st.radio(
#         " ",
#         [
#             "🏠 Home",
#             "📊 Analytics",
#             "📦 Inventory DB",
#             "📡 Monitoring",
#             "📐 Planogram",
#             "🔮 Predictive"
#         ],
#         key="page",
#         label_visibility="collapsed"
#     )


# # ---------------------------------------------------
# # ROUTING
# # ---------------------------------------------------

# if page == "🏠 Home":

#     st.markdown("""
#         <div style="text-align:center; padding:4rem 2rem;
#         background:linear-gradient(135deg,#1e3a8a,#3b82f6);
#         border-radius:25px; color:white; margin:3rem 0;">
#             <h1 style="font-size:4rem;">🛒 Smart Inventory Vision</h1>
#             <h2 style="color:#bfdbfe;">
#                 AI-Powered Retail Shelf Monitoring System
#             </h2>
#             <p style="margin-top:1rem; color:#93c5fd;">
#                 Real-time monitoring, automated audits, and intelligent inventory management
#             </p>
#         </div>
#     """, unsafe_allow_html=True)

# elif page == "📊 Analytics":
#     Analytics.app()

# elif page == "📦 Inventory DB":
#     Inventory_DB.app()

# elif page == "📡 Monitoring":
#     Monitoring.app()

# elif page == "📐 Planogram":
#     Planogram.app()

# elif page == "🔮 Predictive":
#     Predictive.app()







import streamlit as st

# ✅ IMPORT FEATURE FILES (make sure file names match exactly)
import Analytics
import Audit          # ✅ NEW AUDIT IMPORT
import Inventory_DB
import Monitoring
import Planogram
import Predictive

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="🛒 Retail CV Inventory",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.set_option("client.showSidebarNavigation", False)

# ---------------------------------------------------
# FORCE DEFAULT PAGE ON EVERY FRESH RUN
# ---------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e8f4fd 0%, #b3d9ff 50%, #80bfff 100%);
}

.sidebar-title {
    text-align: center;
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #1e3a8a;
}

div[role="radiogroup"] > label {
    background-color: rgba(255,255,255,0.4);
    padding: 0.6rem 1rem;
    margin: 0.4rem 0;
    border-radius: 10px;
    font-weight: 600;
    color: #0f172a;
    transition: all 0.3s ease;
}

div[role="radiogroup"] > label:hover {
    background-color: #1e3a8a;
    color: white;
    transform: translateX(5px);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR NAVIGATION (ADDED AUDIT)
# ---------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🧭 Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        " ",
        [
            "🏠 Home",
            "🔍 Audit",          # ✅ NEW AUDIT PAGE ADDED
            "📊 Analytics",
            "📦 Inventory DB",
            "📡 Monitoring",
            "📐 Planogram",
            "🔮 Predictive"
        ],
        key="page",
        label_visibility="collapsed",
        index=0
    )

# ---------------------------------------------------
# ROUTING (ORIGINAL HOME + NEW AUDIT)
# ---------------------------------------------------
if page == "🏠 Home":
    st.markdown("""
        <div style="text-align:center; padding:4rem 2rem;
        background:linear-gradient(135deg,#1e3a8a,#3b82f6);
        border-radius:25px; color:white; margin:3rem 0;">
            <h1 style="font-size:4rem;">🛒 Smart Inventory Vision</h1>
            <h2 style="color:#bfdbfe;">
                AI-Powered Retail Shelf Monitoring System
            </h2>
            <p style="margin-top:1rem; color:#93c5fd;">
                Real-time monitoring, automated audits, and intelligent inventory management
            </p>
        </div>
    """, unsafe_allow_html=True)

elif page == "🔍 Audit":
    Audit.app()

elif page == "📊 Analytics":
    Analytics.app()

elif page == "📦 Inventory DB":
    Inventory_DB.app()

elif page == "📡 Monitoring":
    Monitoring.app()

elif page == "📐 Planogram":
    Planogram.app()

elif page == "🔮 Predictive":
    Predictive.app()
