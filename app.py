# 🔺 Illuminati AI Copy Master – Main App with AI Engines
# Author: DeAndre Jefferson

import streamlit as st
import os

# Optional AI libraries
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# --- Global UI Setup ---
st.set_page_config(
    page_title="Illuminati AI Copy Master",
    page_icon="🔺",
    layout="wide",
)

# --- Session Defaults ---
if "engine_mode" not in st.session_state:
    st.session_state["engine_mode"] = "Rule-based"  # "Rule-based", "OpenAI", or "Gemini"

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""

if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = ""

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

# === Helper: API keys from secrets or session ===

def get_openai_key():
    """Get OpenAI API key from Streamlit secrets or session."""
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    key = st.session_state.get("openai_api_key", "").strip()
    return key or None


def get_gemini_key():
    """Get Gemini API key from Streamlit secrets or session."""
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    key = st.session_state.get("gemini_api_key", "").strip()
    return key or None


def generate_with_openai(prompt: str) -> str:
    """Call OpenAI with a chat-style prompt. Returns text or raises an Exception."""
    api_key = get_openai_key()
    if not api_key:
        raise RuntimeError("No OpenAI API key found in secrets or session.")

    if openai is None:
        raise RuntimeError("openai library is not installed.")

    # Legacy-style call (compatible with most OpenAI Python versions)
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a world-class direct response copywriter."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.75,
    )
    return resp["choices"][0]["message"]["content"].strip()


def generate_with_gemini(prompt: str) -> str:
    """Call Gemini with a prompt. Returns text or raises an Exception."""
    api_key = get_gemini_key()
    if not api_key:
        raise RuntimeError("No Gemini API key found in secrets or session.")

    if genai is None:
        raise RuntimeError("google-generativeai library is not installed.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(prompt)
    return (resp.text or "").strip()


def generate_rule_based_copy(
    product_name,
    product_desc,
    audience,
    tone,
    benefits_list,
    cta,
    awareness,
    master_style,
):
    """Local, no-API rule-based generator for headlines and sales copy."""

    base_benefit = (
        benefits_list[0] if benefits_list else "get better results with less effort and stress"
    )

    # Awareness angle
    if awareness == "Unaware":
        awareness_angle = "lead with curiosity and a bold, intriguing promise that wakes them up."
    elif awareness == "Problem-aware":
        awareness_angle = "agitate the pain they already feel and show you truly understand it."
    elif awareness == "Solution-aware":
        awareness_angle = "contrast old frustrating solutions with your better approach."
    elif awareness == "Product-aware":
        awareness_angle = "stack proof, specifics, and reasons to act today with your product."
    else:  # Most-aware
        awareness_angle = "reinforce the offer, sweeten the deal, and remove every ounce of risk."

    style_flavor = {
        "Gary Halbert": "raw, emotional, almost letter-style copy that pokes at greed, fear, curiosity, and desire.",
        "David Ogilvy": "research-driven clarity with a focus on specific, credible benefits.",
        "Dan Kennedy": "no-BS direct response copy with strong offers, deadlines, and risk reversal.",
        "Claude Hopkins": "scientific advertising with testable claims and strong self-interest appeals.",
        "Joe Sugarman": "slippery-slide storytelling with curiosity and sensory details.",
        "Eugene Schwartz": "desire-intensifying copy tuned to market awareness and sophistication.",
        "John Carlton": "punchy, street-wise hooks with vivid payoff and urgency.",
        "Jay Abraham": "preeminence, value stacking, and strategic leverage of every advantage.",
        "Robert Bly": "4 U's: Useful, Urgent, Unique, Ultra-specific, with clear benefits.",
        "Neville Medhora": "simple, scannable, human copy with a hint of humor.",
        "Joanna Wiebe": "voice-of-customer phrasing and sharp conversion-focused microcopy.",
        "Hybrid Mix": "a blend of classic direct response aggression and modern conversion copy.",
    }.get(master_style, "classic direct response flavor.")

    headlines = []

    # 1. Benefit + without pain
    headlines.append(
        f"{base_benefit} — without the usual {'stress' if 'without' not in base_benefit.lower() else 'roadblocks'}"
    )

    # 2. How to + benefit
    headlines.append(
        f"How to {base_benefit.lower()} with {product_name} (Even If You Feel You've Tried Everything)"
    )

    # 3. Curiosity / shortcut
    headlines.append(
        f"The {product_name} Shortcut That Quietly Turns Cold Traffic into Buyers"
    )

    # 4. Direct offer to audience
    first_audience_line = audience.splitlines()[0] if audience else "ambitious entrepreneurs"
    headlines.append(
        f"New for {first_audience_line}: {product_name} That Finally Makes Your Traffic Pay"
    )

    # 5. Ultra-specific style
    headlines.append(
        f"Use {product_name} to {base_benefit.lower()} in the Next 30 Days... Or Less"
    )

    # 6. Optional extra hybrid
    if len(benefits_list) > 1:
        second_benefit = benefits_list[1]
        headlines.append(
            f"Turn {second_benefit.lower()} into your unfair advantage with {product_name}"
        )

    # Bullet list
    bullets = "".join([f"- {b}\n" for b in benefits_list]) if benefits_list else "- Clear, measurable results\n"

    sales_copy = f"""[{master_style}-inspired angle – {style_flavor}]

ATTENTION

If you're {audience or 'struggling to convert attention into actual sales'}, there's a good chance the problem is not you...
it's the message you're putting in front of your market.

INTEREST

{product_name} is built to fix that.

{product_desc}

Instead of shouting into the void, you start speaking directly to what your prospects already care about most. You {awareness_angle}

DESIRE

Here is what that looks like when it is working for you:

{bullets}

ACTION

If you're serious about {base_benefit.lower()} and ready to use copy that finally matches the value you deliver, this is your move:

{cta.strip().rstrip('.')}.
"""

    return headlines, sales_copy


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
- **Generate Copy** – rule-based + AI engines  
- **Manual & Assets** – generate your Illuminati AI manual package  
- **System Checklist** – launch checklist  
- **Settings & Integrations** – configure engine mode & API keys  
""")


# --- Generate Copy Page ---
def page_generate_copy():
    st.header("🧠 Generate Copy")

    # Default engine from session, but allow per-run override
    default_engine = st.session_state.get("engine_mode", "Rule-based")
    engine_choice = st.selectbox(
        "Engine",
        ["Rule-based", "OpenAI", "Gemini"],
        index=["Rule-based", "OpenAI", "Gemini"].index(default_engine),
        help="Rule-based uses local templates only. OpenAI / Gemini use external AI models.",
    )
    # Keep session in sync
    st.session_state["engine_mode"] = engine_choice

    st.markdown(f"**Current engine mode:** `{engine_choice}`")

    st.markdown("---")
    st.markdown("### ✍️ Copy Brief")

    with st.form("copy_brief_form"):
        product_name = st.text_input("Product / Service Name", "")
        product_desc = st.text_area("Product / Service Description", "")
        audience = st.text_area("Target Audience (demographics, psychographics, pain points)", "")
        tone = st.selectbox(
            "Desired Tone",
            [
                "Direct & No-BS",
                "Friendly & Conversational",
                "High-End / Premium",
                "Urgent & Hypey",
                "Calm & Professional",
            ],
            index=0,
        )
        benefits_text = st.text_area(
            "Key Benefits & USPs (one per line)",
            placeholder="E.g.\nLose weight without starving\nSave 5 hours a week\nNo prior experience needed",
        )
        cta = st.text_input("Primary Call To Action (CTA)", "Click here to get started")

        awareness = st.selectbox(
            "Audience Awareness Level (Eugene Schwartz)",
            [
                "Unaware",
                "Problem-aware",
                "Solution-aware",
                "Product-aware",
                "Most-aware",
            ],
            index=2,
        )

        master_style = st.selectbox(
            "Master Style Influence",
            [
                "Gary Halbert",
                "David Ogilvy",
                "Dan Kennedy",
                "Claude Hopkins",
                "Joe Sugarman",
                "Eugene Schwartz",
                "John Carlton",
                "Jay Abraham",
                "Robert Bly",
                "Neville Medhora",
                "Joanna Wiebe",
                "Hybrid Mix",
            ],
            index=0,
        )

        submitted = st.form_submit_button("⚡ Generate Headlines & Sales Copy")

    if not submitted:
        st.info("Fill out the brief and click **Generate** to see headline ideas and a sales copy draft.")
        return

    if not product_name or not product_desc:
        st.error("Please provide at least a product name and description.")
        return

    # Parse benefits
    benefits_list = [b.strip() for b in benefits_text.split("\n") if b.strip()]

    # RULE-BASED ENGINE
    if engine_choice == "Rule-based":
        headlines, sales_copy = generate_rule_based_copy(
            product_name=product_name,
            product_desc=product_desc,
            audience=audience,
            tone=tone,
            benefits_list=benefits_list,
            cta=cta,
            awareness=awareness,
            master_style=master_style,
        )
        st.markdown("### 📰 Headline Variations (Rule-based)")
        for i, h in enumerate(headlines, start=1):
            st.write(f"{i}. {h}")

        st.markdown("---")
        st.markdown("### 📜 Sales Copy Draft")
        st.code(sales_copy, language="markdown")
        return

    # AI PROMPT (used by OpenAI or Gemini)
    prompt = f"""
You are a legendary direct response copywriter channeling the combined wisdom of:

- David Ogilvy
- Gary Halbert
- Claude Hopkins
- Joe Sugarman
- Eugene Schwartz
- John Carlton
- Dan Kennedy
- Jay Abraham
- Robert Bly
- Joanna Wiebe
- Neville Medhora

Write in the primary style of: {master_style}.

Use AIDA (Attention, Interest, Desire, Action), PAS (Problem, Agitate, Solve), and FAB (Features, Advantages, Benefits).

TASK:

1. Generate 5-8 strong headlines optimized for cold traffic, respecting this awareness level:
   {awareness}

2. Then generate a persuasive sales copy draft that:
   - Hooks hard in the first 2–3 sentences
   - Agitates the core pains of this audience
   - Presents {product_name} as the natural solution
   - Uses some bullets for benefits
   - Ends with a strong call-to-action: "{cta}"

CONTEXT:

Product / Service Name:
{product_name}

Product / Service Description:
{product_desc}

Target Audience:
{audience}

Desired Tone:
{tone}

Key Benefits & USPs:
{benefits_text}

OUTPUT FORMAT (IMPORTANT):

HEADLINES:
1. ...
2. ...
3. ...
4. ...
5. ...
(Up to 8)

SALES COPY:
[Write the full sales copy here.]
""".strip()

    # OPENAI ENGINE
    if engine_choice == "OpenAI":
        try:
            ai_text = generate_with_openai(prompt)
        except Exception as e:
            st.error(f"OpenAI generation failed: {e}")
            st.info("Falling back to rule-based copy.")
            headlines, sales_copy = generate_rule_based_copy(
                product_name=product_name,
                product_desc=product_desc,
                audience=audience,
                tone=tone,
                benefits_list=benefits_list,
                cta=cta,
                awareness=awareness,
                master_style=master_style,
            )
            st.markdown("### 📰 Headline Variations (Rule-based fallback)")
            for i, h in enumerate(headlines, start=1):
                st.write(f"{i}. {h}")
            st.markdown("---")
            st.markdown("### 📜 Sales Copy Draft (Rule-based fallback)")
            st.code(sales_copy, language="markdown")
            return

        st.markdown("### 🤖 OpenAI Output")
        st.markdown(ai_text)
        return

    # GEMINI ENGINE
    if engine_choice == "Gemini":
        try:
            ai_text = generate_with_gemini(prompt)
        except Exception as e:
            st.error(f"Gemini generation failed: {e}")
            st.info("Falling back to rule-based copy.")
            headlines, sales_copy = generate_rule_based_copy(
                product_name=product_name,
                product_desc=product_desc,
                audience=audience,
                tone=tone,
                benefits_list=benefits_list,
                cta=cta,
                awareness=awareness,
                master_style=master_style,
            )
            st.markdown("### 📰 Headline Variations (Rule-based fallback)")
            for i, h in enumerate(headlines, start=1):
                st.write(f"{i}. {h}")
            st.markdown("---")
            st.markdown("### 📜 Sales Copy Draft (Rule-based fallback)")
            st.code(sales_copy, language="markdown")
            return

        st.markdown("### 🤖 Gemini Output")
        st.markdown(ai_text)
        return


# --- Manual & Assets Page ---
def page_manual_assets():
    st.header("🔺 Illuminati AI Copy Master Manual & Assets")
    st.markdown("""
Generate your **Illuminati AI Copy Master Manual** package:

- PDF manual (lite version for now)  
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


# --- System Checklist Page ---
def page_system_checklist():
    st.header("✅ System Checklist")

    st.markdown("""
Use this checklist before you send real traffic to your funnel.

Each item helps make sure:
- Your offer is clear  
- Your pages work  
- Your tracking is live  
- Your traffic isn’t being wasted  
    """)

    # Define checklist items grouped by section
    sections = {
        "Offer & Positioning": [
            "Core offer is clearly defined (who it's for, what it does, main promise).",
            "Main benefit/headline is written and tested for clarity.",
            "Guarantee / risk reversal is decided (or intentionally omitted).",
            "Price and payment structure are final (no ‘I’ll decide later’).",
        ],
        "Funnel Assets": [
            "Opt-in page is built and loads correctly on desktop & mobile.",
            "Thank-you / bridge page is built and clearly sets the next step.",
            "Main sales page (or VSL) is live and has a clear CTA.",
            "Email follow-up sequence (at least 3–5 emails) is drafted and scheduled.",
        ],
        "Tracking & Tech": [
            "Primary tracking pixels / tags are installed (if applicable).",
            "UTM parameters or tracking links are set for each traffic source.",
            "Test opt-in completed and confirmed the lead shows up where expected.",
            "Test ‘purchase’ or main conversion flow works end-to-end.",
        ],
        "Traffic Plan": [
            "At least one traffic source is chosen (Solo Ads / Banners / Classifieds / etc.).",
            "Budget for test phase is defined and affordable.",
            "Creative variations are prepared (headlines, angles, images).",
            "Schedule for checking stats (daily/weekly) is set.",
        ],
        "Compliance & Honesty": [
            "All claims in the copy are truthful and not misleading.",
            "Required disclaimers / terms / privacy pages are present (if needed).",
            "Affiliate / promotional relationships are disclosed where required.",
        ],
    }

    # Render checklist with stateful checkboxes
    total_items = 0
    completed_items = 0

    for section_name, items in sections.items():
        st.subheader(section_name)
        for item in items:
            key = f"checklist_{section_name}_{item}"  # unique key per item
            checked = st.checkbox(item, key=key)
            total_items += 1
            if checked:
                completed_items += 1

        st.markdown("---")

    # Progress summary
    if total_items > 0:
        percent = int((completed_items / total_items) * 100)
    else:
        percent = 0

    st.markdown(f"### 📊 Completion: **{completed_items} / {total_items}** items checked ({percent}%)")

    if percent < 50:
        st.info("You’re still early in the setup. Work through the items above before scaling traffic.")
    elif percent < 100:
        st.success("You’re getting close. Tighten any remaining items before pushing harder on ads.")
    else:
        st.balloons()
        st.success("All checklist items complete. You’re ready to carefully test and scale traffic.")


# --- Settings & Integrations Page ---
def page_settings():
    st.header("⚙️ Settings & Integrations")

    st.markdown("### AI Engine Mode")
    engine_mode = st.radio(
        "Choose your default generation engine:",
        ["Rule-based", "OpenAI", "Gemini"],
        index=["Rule-based", "OpenAI", "Gemini"].index(st.session_state["engine_mode"]),
        help="Rule-based uses built-in templates with no tokens. OpenAI/Gemini use external APIs.",
    )

    st.session_state["engine_mode"] = engine_mode

    st.markdown("---")
    st.markdown("### API Keys (Optional for this session)")

    if engine_mode == "OpenAI":
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("openai_api_key", ""),
            help="Used only in this session. For production, prefer Streamlit secrets.",
        )
        st.session_state["openai_api_key"] = openai_key

    elif engine_mode == "Gemini":
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            help="Used only in this session. For production, prefer Streamlit secrets.",
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
