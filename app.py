# 🔺 Illuminati AI Copy Master – Minimal Stable App
# Author: DeAndre Jefferson

import streamlit as st
import os
# --- Session Defaults ---
if "engine_mode" not in st.session_state:
    st.session_state["engine_mode"] = "Rule-based"  # or "OpenAI" / "Gemini"

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = ""

# --- Global UI Setup ---
st.set_page_config(
    page_title="Illuminati AI Copy Master",
    page_icon="🔺",
    layout="wide",
)

# --- Sidebar Navigation ---
st.sidebar.markdown("### 🔺 Illuminati 
AI Copy Master")
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

    st.markdown(f"**Current engine mode:** `{st.session_state.get('engine_mode', 'Rule-based')}`")

    if st.session_state.get("engine_mode") == "OpenAI":
        st.info("OpenAI mode selected. This page will later call OpenAI using your API key.")
    elif st.session_state.get("engine_mode") == "Gemini":
        st.info("Gemini mode selected. This page will later call Gemini using your API key.")
    else:
        st.info("Rule-based mode selected. This page will later use built-in, no-token templates.")

    st.write("For now, this is a placeholder. Use **Manual & Assets** to generate your SOP manual package.")

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

    st.markdown("### AI Engine Mode")
    engine_mode = st.radio(
        "Choose your default generation engine:",
        ["Rule-based", "OpenAI", "Gemini"],
        index=["Rule-based", "OpenAI", "Gemini"].index(st.session_state["engine_mode"]),
        help="Rule-based uses built-in templates with no tokens. OpenAI/Gemini use external APIs."
    )

    st.session_state["engine_mode"] = engine_mode

    st.markdown("---")
    st.markdown("### API Keys (Optional for this session)")

    if engine_mode == "OpenAI":
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("openai_api_key", ""),
            help="Used only in this session. For production, prefer Streamlit secrets."
        )
        st.session_state["openai_api_key"] = openai_key

    elif engine_mode == "Gemini":
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            help="Used only in this session. For production, prefer Streamlit secrets."
        )
        st.session_state["gemini_api_key"] = gemini_key

    else:
        st.info("Rule-based mode is active. No external AI engine is required.")

    st.markdown("---")
    st.markdown("### Current Settings")

    st.write(f"**Engine mode:** `{st.session_state['engine_mode']}`")

    if st.session_state["engine_mode"] == "OpenAI":
        st.write("**OpenAI key set:**", "✅ Yes" if st.session_state["openai_api_key"] else "❌ No")
    elif st.session_state["engine_mode"] == "Gemini":
        st.write("**Gemini key set:**", "✅ Yes" if st.session_state["gemini_api_key"] else "❌ No")

    st.markdown("""
    *Note:* Keys entered here are only kept in memory for this session.
    For long-term, secure storage on Streamlit Cloud, use **Settings → Secrets** in the app dashboard.
    """)

