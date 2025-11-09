# 🔺 Illuminati AI Copy Master – Minimal Stable App
# Author: DeAndre Jefferson

import streamlit as st
import os

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
    - Built-in manual & asset generator (PDF + ZIP)  

    ---
    Use the navigation on the left to access:
    - **Dashboard** – overview  
    - **Generate Copy** – (placeholder for copy engine)  
    - **Manual & Assets** – generate your Illuminati AI manual package  
    - **System Checklist** – launch checklist (placeholder)  
    - **Settings & Integrations** – integration notes (placeholder)  
    """)

# --- Generate Copy Page (simple placeholder for now) ---
def page_generate_copy():
    st.header("🧠 Generate Copy")
    st.info("This section is a placeholder. The copy generation engine will be wired here later.")
    st.write("For now, use the **Manual & Assets** section to generate your SOP manual package.")

# --- Manual & Assets Page ---
def page_manual_assets():
    st.header("🔺 Illuminati AI Copy Master Manual & Assets")
    st.markdown("""
    Generate your **Illuminati AI Copy Master Manual** package:

    - PDF manual (simple version for now)  
    - Bundled ZIP package ready to download  

    Click the button below to generate the package.
    """)

    # Import the generator lazily so we see clear errors if something is wrong
    try:
        from generate_illuminati_ai_package import main as generate_illuminati_package_main
    except Exception as e:
        st.error(f"Generator import failed: `{e}`")
        st.stop()

    if st.button("🔺 Forge The Manual of Persuasion"):
        with st.spinner("Forging the manual and ZIP package..."):
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

# --- System Checklist Page (placeholder) ---
def page_system_checklist():
    st.header("✅ System Checklist")
    st.info("This is a placeholder. Later you'll track funnel readiness and launch status here.")

# --- Settings & Integrations Page (placeholder) ---
def page_settings():
    st.header("⚙️ Settings & Integrations")
    st.markdown("""
    This is a placeholder page for future settings, including:

    - OpenAI / Gemini API configuration  
    - Rule-based vs AI engine toggles  
    - Affiliate & ESP integration options  

    For now, no configuration is required. The app runs in minimal mode.
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

