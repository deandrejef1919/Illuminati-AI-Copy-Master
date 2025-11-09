# 🔺 Illuminati AI Copy Master – Main Streamlit App
# Author: DeAndre Jefferson
# Date: 2025
# Purpose: AI-powered copywriting & marketing dashboard

import streamlit as st
import os
# NOTE: we will import the generator lazily inside the Manual & Assets page


# --- Global UI Setup ---
st.set_page_config(
    page_title="Illuminati AI Copy Master",
    page_icon="🔺",
    layout="wide",
)

# --- Sidebar Navigation ---
st.sidebar.markdown("### 🔺 Illuminati AI Copy Master")
st.sidebar.caption("Strategic Copy & Traffic Command Console")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Generate Copy",
        "Manual & Assets",
        "System Checklist",
        "Settings & Integrations",
    ]
)

# --- Dashboard Page ---
def page_dashboard():
    st.title("🔺 Illuminati AI Copy Master")
    st.subheader("AI-Powered Direct Response Control Panel")

    st.markdown("""
    Welcome to **Illuminati AI Copy Master** — your all-in-one hub for:
    - Legendary copywriting frameworks (Ogilvy, Halbert, Kennedy & more)
    - AI-enhanced generation for headlines, sales letters, and funnels
    - Integrated analytics and A/B simulation
    - Instant PDF and ZIP export of full sales systems  
    ---
    **Tip:** Visit the *Manual & Assets* section to forge your personal Illuminati AI SOP Manual.
    """)

# --- Manual & Assets Page ---
def page_manual_assets():
    st.header("📕 Illuminati AI Copy Master Manual & Assets")
    st.markdown("""
    Generate your **Illuminati AI Copy Master Manual** package:

    - Illustrated PDF manual (SOP + Master Appendix)  
    - Matching high-res cover image  
    - Bundled ZIP package ready to download  
    """)

    # Try to import the generator module here so we can see real errors
    try:
        from generate_illuminati_ai_package import main as generate_illuminati_package_main
    except Exception as e:
        st.error(f"Generator import failed: `{e}`")
        st.stop()

    if st.button("🔺 Forge The Manual of Persuasion"):
        with st.spinner("Forging the manual, cover, and ZIP package..."):
            generate_illuminati_package_main()
        st.success("✅ The manual package has been forged successfully.")

        zip_path = "Illuminati_AI_Package.zip"
        if os.path.exists(zip_path):
            with open(zip_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Illuminati AI Package (ZIP)",
                    data=f,
                    file_name="Illuminati_AI_Package.zip",
                    mime="application/zip",
                )
        else:
            st.error("Package ZIP not found. Please rerun the generator.")


# --- Placeholder Pages ---
def page_generate_copy():
    st.header("🧠 Generate Copy")
    st.info("This section will soon include AI headline & sales copy generation.")

def page_system_checklist():
    st.header("✅ System Checklist")
    st.info("Use this checklist to ensure all Illuminati AI features are ready.")

def page_settings():
    st.header("⚙️ Settings & Integrations")
    st.markdown("""
    - Configure API keys for OpenAI or Gemini
    - Enable rule-based mode to avoid token usage  
    - Adjust AI and system performance options  
    """)

# --- Router ---
if page == "Dashboard":
    page_dashboard()
elif page == "Generate Copy":
    page_generate_copy()
elif page == "Manual & Assets":
    page_manual_assets()
elif page == "System Checklist":
    page_system_checklist()
elif page == "Settings & Integrations":
    page_settings()
