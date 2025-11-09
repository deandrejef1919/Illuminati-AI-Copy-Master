# 🔺 Illuminati AI Copy Master – Main App with AI Engines + Checklist Presets + Traffic Networks + Classified Ad Writer
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

if "checklist_presets" not in st.session_state:
    # name -> {key: bool}
    st.session_state["checklist_presets"] = {}

if "campaign_history" not in st.session_state:
    # list of dicts with metrics
    st.session_state["campaign_history"] = []

# --- Sidebar Navigation ---
st.sidebar.markdown("### 🔺 Illuminati AI Copy Master")
st.sidebar.caption("Strategic Copy & Traffic Command Console")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Generate Copy",
        "Classified Ad Writer",
        "Manual & Assets",
        "System Checklist",
        "Traffic & Networks",
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

    # Legacy-style call (works with most OpenAI Python client versions)
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

    # First try a newer model, then gracefully fall back if unsupported
    last_error = None
    for model_name in ["gemini-1.5-flash", "gemini-pro"]:
        try:
            model = genai.GenerativeModel(model_name)
            resp = model.generate_content(prompt)
            text = getattr(resp, "text", "") or ""
            if text.strip():
                return text.strip()
        except Exception as e:
            last_error = e
            continue

    # If we tried all fallbacks and still failed, surface the last error
    raise RuntimeError(f"Gemini generation failed after trying multiple models: {last_error}")



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
- **Classified Ad Writer** – short-form classified ads for traffic sites  
- **Manual & Assets** – generate your Illuminati AI manual package  
- **System Checklist** – launch checklist with presets  
- **Traffic & Networks** – traffic sources & quick analyzer + history  
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


# --- Classified Ad Writer Page ---
# --- Classified Ad Writer Page ---
def page_classified_writer():
    st.header("📢 Classified Ad Writer")

    st.markdown("""
Generate short, punchy classified ads for:

- Free classified sites (Craigslist, Locanto, etc.)  
- Low-friction marketplaces  
- Simple text-based placements  

You can use **Rule-based**, **OpenAI**, or **Gemini** as the engine.
""")

    default_engine = st.session_state.get("engine_mode", "Rule-based")
    engine_choice = st.selectbox(
        "Engine",
        ["Rule-based", "OpenAI", "Gemini"],
        index=["Rule-based", "OpenAI", "Gemini"].index(default_engine),
        help="Rule-based uses local templates. OpenAI / Gemini use AI models if keys are set.",
    )
    st.session_state["engine_mode"] = engine_choice

    with st.form("classified_form"):
        product_name = st.text_input("Product / Service Name", "")
        product_desc = st.text_area(
            "Very Short Description (1–3 sentences)",
            "",
            help="Keep this tight. We'll trim it further so it fits classified formats."
        )
        location = st.text_input("Location / Market (optional)", "Online / Worldwide")
        audience = st.text_area(
            "Ideal Prospect (who should respond?)",
            "",
            help="One or two lines max. If you paste a long avatar, we'll only use the first line."
        )
        benefits_text = st.text_area(
            "Main Benefits (one per line, keep them simple)",
            placeholder="E.g.\nLose 10 lbs without starving\nWork from home part-time\nGet more leads without cold calling",
        )
        contact = st.text_input(
            "Contact or Link (what should they do?)",
            "Reply to this ad or visit YourSite.com",
        )

        awareness = st.selectbox(
            "Audience Awareness Level",
            ["Unaware", "Problem-aware", "Solution-aware", "Product-aware", "Most-aware"],
            index=1,
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

        num_ads = st.slider("How many ad variations?", min_value=3, max_value=8, value=5)

        submitted = st.form_submit_button("🧲 Generate Classified Ads")

    if not submitted:
        st.info("Fill in the details above and click **Generate Classified Ads**.")
        return

    if not product_name or not product_desc or not contact:
        st.error("Please provide at least a product name, short description, and contact/link.")
        return

    # --- Shared helpers ---
    benefits_list = [b.strip() for b in benefits_text.split("\n") if b.strip()]

    # Use only the first line of any long avatar blob
    audience_short = audience.splitlines()[0].strip() if audience.strip() else "people who are ready for a change"

    # Shorten description to keep ads tight
    desc_short = product_desc.strip()
    if len(desc_short) > 220:
        desc_short = desc_short[:217] + "..."

    base_benefit = benefits_list[0] if benefits_list else "get real results without the usual struggle"
    second_benefit = benefits_list[1] if len(benefits_list) > 1 else None

    # Map master to a simple flavor hint
    if master_style == "Gary Halbert":
        style_hint = "emotional, direct-mail style with a strong hook and clear self-interest."
    elif master_style == "David Ogilvy":
        style_hint = "clear benefit, specific promise, and respect for the reader's intelligence."
    elif master_style == "Dan Kennedy":
        style_hint = "no-BS, direct response tone with focus on money, time, and results."
    elif master_style == "John Carlton":
        style_hint = "punchy, street-wise language with urgency and vivid payoff."
    elif master_style == "Joe Sugarman":
        style_hint = "curiosity and a conversational 'slippery slide' feel."
    elif master_style == "Robert Bly":
        style_hint = "simple, useful, ultra-specific phrasing."
    elif master_style == "Neville Medhora":
        style_hint = "short, funny, human lines that feel like a friend wrote them."
    else:
        style_hint = "classic direct response style adapted for short classified ads."

    # RULE-BASED CLASSIFIED ADS
    if engine_choice == "Rule-based":
        ads = []

        for i in range(num_ads):
            pattern_type = i % 3

            if pattern_type == 0:
                # Halbert-style: bold benefit + curiosity
                headline = f"{base_benefit} – {product_name}"
                body_lines = [
                    desc_short,
                    f"Perfect for {audience_short} in {location}.",
                    contact,
                ]
            elif pattern_type == 1:
                # Ogilvy-style: specific, clean promise
                benefit_line = second_benefit or base_benefit
                headline = f"{product_name}: {benefit_line}"
                body_lines = [
                    desc_short,
                    f"If you're {audience_short.lower()}, this was built for you.",
                    contact,
                ]
            else:
                # Kennedy-style: direct offer + urgency
                headline = f"{product_name} – Limited Spots for {audience_short}"
                body_lines = [
                    desc_short,
                    "Serious inquiries only. No hype, just results.",
                    contact,
                ]

            body = " ".join(line.strip() for line in body_lines if line.strip())
            ads.append((headline, body))

        st.markdown("### 📝 Classified Ad Variations (Rule-based)")
        st.caption(f"Style influence: {master_style} – {style_hint}")
        for i, (h, b) in enumerate(ads, start=1):
            st.markdown(f"**Ad {i}: {h}**")
            st.markdown(b)
            st.markdown("---")

        return

    # --- AI-POWERED CLASSIFIED ADS ---
    prompt = f"""
You are a legendary direct response copywriter specializing in short classified ads, channeling the style of {master_style}.

Write in a way that feels like: {style_hint}

TASK:
Write {num_ads} different classified ads for the following offer.

Each ad must:
- Have ONE short headline
- Have 1–3 short sentences of body copy
- Be optimized for response on classified ad sites (e.g., Craigslist, Locanto, etc.)
- Use clear, simple, human language (no corporate jargon)
- Match this awareness level: {awareness}
- End with this clear next step: "{contact}"

CONTEXT:

Product / Service Name:
{product_name}

Very Short Description:
{desc_short}

Location / Market:
{location}

Ideal Prospect (short):
{audience_short}

Main Benefits:
{benefits_text}

OUTPUT FORMAT (IMPORTANT):

AD 1:
Headline: ...
Body: ...

AD 2:
Headline: ...
Body: ...

(Continue up to {num_ads})
""".strip()

    if engine_choice == "OpenAI":
        try:
            ai_text = generate_with_openai(prompt)
        except Exception as e:
            st.error(f"OpenAI classified ad generation failed: {e}")
            return
        st.markdown("### 🤖 OpenAI Classified Ads")
        st.markdown(ai_text)
        return

    if engine_choice == "Gemini":
        try:
            ai_text = generate_with_gemini(prompt)
        except Exception as e:
            st.error(f"Gemini classified ad generation failed: {e}")
            return
        st.markdown("### 🤖 Gemini Classified Ads")
        st.markdown(ai_text)
        return


    # AI-POWERED CLASSIFIED ADS
    prompt = f"""
You are a legendary direct response copywriter specializing in short classified ads, channeling the style of {master_style}.

TASK:
Write {num_ads} different classified ads for the following offer.

Each ad should be:
- 1 short headline
- 1–3 short sentences
- Optimized for response on classified ad sites (e.g., Craigslist, Locanto, etc.)
- Clear, simple language
- Matching this awareness level: {awareness}
- Ending with a clear next step: "{contact}"

CONTEXT:

Product / Service Name:
{product_name}

Very Short Description:
{product_desc}

Location / Market:
{location}

Ideal Prospect:
{audience}

Main Benefits:
{benefits_text}

OUTPUT FORMAT (IMPORTANT):

AD 1:
Headline: ...
Body: ...

AD 2:
Headline: ...
Body: ...

(Continue up to {num_ads})
""".strip()

    if engine_choice == "OpenAI":
        try:
            ai_text = generate_with_openai(prompt)
        except Exception as e:
            st.error(f"OpenAI classified ad generation failed: {e}")
            return
        st.markdown("### 🤖 OpenAI Classified Ads")
        st.markdown(ai_text)
        return

    if engine_choice == "Gemini":
        try:
            ai_text = generate_with_gemini(prompt)
        except Exception as e:
            st.error(f"Gemini classified ad generation failed: {e}")
            return
        st.markdown("### 🤖 Gemini Classified Ads")
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


# --- System Checklist Page (with presets) ---
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

    sections = {
        "Offer & Positioning": [
            "Core offer is clearly defined (who it's for, what it does, main promise).",
            "Main benefit/headline is written and tested for clarity.",
            "Guarantee / risk reversal is decided (or intentionally omitted).",
            "Price and payment structure are final.",
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
            "Test 'purchase' or main conversion flow works end-to-end.",
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

    total_items = 0
    completed_items = 0

    # Render checklist with stateful checkboxes
    for section_name, items in sections.items():
        st.subheader(section_name)
        for idx, item in enumerate(items):
            key = f"checklist_{section_name}_{idx}"
            checked = st.checkbox(item, key=key)
            total_items += 1
            if checked:
                completed_items += 1
        st.markdown("---")

    # Progress summary
    percent = int((completed_items / total_items) * 100) if total_items > 0 else 0
    st.markdown(f"### 📊 Completion: **{completed_items} / {total_items}** items checked ({percent}%)")

    if percent < 50:
        st.info("You’re still early in the setup. Work through the items above before scaling traffic.")
    elif percent < 100:
        st.success("You’re getting close. Tighten any remaining items before pushing harder on ads.")
    else:
        st.balloons()
        st.success("All checklist items complete. You’re ready to carefully test and scale traffic.")

    # --- Preset Save/Load ---
    st.markdown("---")
    st.markdown("### 💾 Checklist Presets (this session only)")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        preset_name = st.text_input("Preset name", "")

    with col2:
        if st.button("Save preset"):
            if not preset_name.strip():
                st.warning("Please enter a preset name before saving.")
            else:
                snapshot = {}
                for section_name, items in sections.items():
                    for idx, _ in enumerate(items):
                        key = f"checklist_{section_name}_{idx}"
                        snapshot[key] = bool(st.session_state.get(key, False))
                st.session_state["checklist_presets"][preset_name.strip()] = snapshot
                st.success(f"Preset '{preset_name.strip()}' saved for this session.")

    with col3:
        if st.button("Clear all"):
            for section_name, items in sections.items():
                for idx, _ in enumerate(items):
                    key = f"checklist_{section_name}_{idx}"
                    st.session_state[key] = False
            st.experimental_rerun()

    # Load preset
    if st.session_state["checklist_presets"]:
        load_name = st.selectbox(
            "Load preset",
            options=["(Select preset)"] + list(st.session_state["checklist_presets"].keys()),
            index=0,
        )
        if load_name != "(Select preset)":
            if st.button("Load selected preset"):
                snapshot = st.session_state["checklist_presets"][load_name]
                for key, val in snapshot.items():
                    st.session_state[key] = bool(val)
                st.success(f"Preset '{load_name}' loaded.")
                st.experimental_rerun()
    else:
        st.caption("No presets saved yet. Save one above to reuse this configuration in this session.")


# --- Traffic & Networks Page ---
def page_traffic_networks():
    st.header("🚦 Traffic & Networks")
    st.markdown("""
This section gives you a **starting map** of places you can get traffic without heavy approval processes,
plus a quick analyzer so you can compare results from:

- Affiliate offers  
- Banner / solo ad vendors  
- Free classified ad sites  

Always double-check each platform’s current policies and terms — they can change anytime.
""")

    tabs = st.tabs([
        "Affiliate Networks",
        "Banner & Solo Ad Networks",
        "Free Classified Sites",
        "Quick Campaign Analyzer",
    ])

    # --- Affiliate Networks ---
    with tabs[0]:
        st.subheader("🌐 Affiliate Networks (Generally Easy to Join)")
        st.markdown("""
These networks typically allow signups with standard registration (no special invite required).  
Always review their current rules and verticals allowed.

- ClickBank  
- JVZoo  
- WarriorPlus  
- Digistore24  
- Impact  
- ShareASale  
- CJ (Commission Junction) – often requires approval per advertiser  
- PartnerStack (for SaaS offers)  
""")
        st.info("Use these to find offers that match your list, niche, or funnel theme. Start with a small test.")

    # --- Banner & Solo Ad Networks ---
    with tabs[1]:
        st.subheader("📢 Banner & Solo Ad Traffic (Lower Barrier Platforms)")

        st.markdown("**Solo Ad Marketplaces:**")
        st.markdown("""
- Udimi  
- TrafficForMe  
- SoloAdsX / similar brokers  
- Individual list sellers (research reputation carefully)  
""")

        st.markdown("**Banner / Display Ad Networks (lower barrier than Google/Meta, but still have policies):**")
        st.markdown("""
- PropellerAds  
- Adsterra  
- HilltopAds  
- RichAds  
- 7Search PPC  
""")

        st.warning(
            "Even if signup is easy, you are still responsible for compliance and truthful advertising. "
            "Avoid banned content and always follow their policies."
        )

    # --- Free Classified Sites ---
    with tabs[2]:
        st.subheader("📋 Free Classified Ad Sites (High or Notable Traffic)")
        st.markdown("""
These platforms often allow free or low-cost classified ads. Availability and rules can vary by country.

- Craigslist (many regions)  
- ClassifiedAds.com  
- Oodle  
- Geebo  
- Locanto  
- Facebook Marketplace / local groups (check group rules)  
- Gumtree (UK / AU)  
- Kijiji (CA)  

Use short, direct ads with a clear benefit and a single next step (click, call, opt in).
""")
        st.info("Write like a human local marketer, not a spam bot. Keep claims realistic and truthful.")

    # --- Quick Campaign Analyzer + History ---
    with tabs[3]:
        st.subheader("📊 Quick Campaign Analyzer")

        st.markdown("""
Use this tool to compare basic performance for campaigns in **Affiliate**, **Banner/Solo**, or **Classifieds**.
Each time you analyze, the result is added to a session-only history below.
""")

        channel = st.selectbox(
            "Channel Type",
            ["Affiliate offer", "Banner / Solo Ads", "Free Classifieds"],
        )

        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign name / label", "")
            source_name = st.text_input("Traffic source / vendor / site", "")
        with col2:
            spend = st.number_input("Ad spend / cost ($)", min_value=0.0, step=1.0)
            clicks = st.number_input("Clicks", min_value=0, step=1)
            conversions = st.number_input("Conversions (leads or sales)", min_value=0, step=1)
            revenue = st.number_input("Revenue generated ($)", min_value=0.0, step=1.0)

        if st.button("Analyze performance"):
            # Basic metrics
            cpc = (spend / clicks) if clicks > 0 else 0.0
            conv_rate = (conversions / clicks * 100.0) if clicks > 0 else 0.0
            cpa = (spend / conversions) if conversions > 0 else 0.0
            epc = (revenue / clicks) if clicks > 0 else 0.0
            roas = (revenue / spend) if spend > 0 else 0.0

            st.markdown("#### Results")

            st.write(f"**Channel:** {channel}")
            if campaign_name:
                st.write(f"**Campaign:** {campaign_name}")
            if source_name:
                st.write(f"**Source / Vendor:** {source_name}")

            st.write(f"- Spend: ${spend:,.2f}")
            st.write(f"- Clicks: {clicks}")
            st.write(f"- Conversions: {conversions}")
            st.write(f"- Revenue: ${revenue:,.2f}")
            st.write(f"- CPC (Cost per click): ${cpc:,.2f}")
            st.write(f"- CPA (Cost per acquisition): ${cpa:,.2f}")
            st.write(f"- EPC (Earnings per click): ${epc:,.2f}")
            st.write(f"- Conversion rate: {conv_rate:.2f}%")
            st.write(f"- ROAS (Return on ad spend): {roas:.2f}x")

            if roas < 1 and conversions == 0:
                st.info("This test lost money and produced no conversions. Consider changing the offer, angle, or traffic source.")
            elif roas < 1:
                st.info("ROAS is below break-even. Look for ways to improve your messaging, targeting, or back-end monetization.")
            elif roas >= 1 and roas < 2:
                st.success("You are near or above break-even. Tighten the funnel and consider controlled scaling.")
            else:
                st.success("Strong ROAS. Monitor closely and scale carefully without violating any platform rules.")

            # Save to history
            entry = {
                "Channel": channel,
                "Campaign": campaign_name or "(unnamed)",
                "Source": source_name or "(unspecified)",
                "Spend": spend,
                "Clicks": clicks,
                "Conversions": conversions,
                "Revenue": revenue,
                "CPC": cpc,
                "CPA": cpa,
                "EPC": epc,
                "ConvRate_%": conv_rate,
                "ROAS": roas,
            }
            st.session_state["campaign_history"].append(entry)
            st.success("Campaign added to this session's history (see below).")

        st.markdown("---")
        st.subheader("📚 Campaign History (this session)")

        history = st.session_state.get("campaign_history", [])
        if not history:
            st.caption("No campaigns analyzed yet. Run the analyzer above to add entries.")
        else:
            filter_channel = st.selectbox(
                "Filter history by channel",
                options=["(All)"] + sorted(list({h["Channel"] for h in history})),
                index=0,
            )
            if filter_channel != "(All)":
                filtered = [h for h in history if h["Channel"] == filter_channel]
            else:
                filtered = history

            # Display as a simple table
            st.table(filtered)

            if st.button("Clear campaign history"):
                st.session_state["campaign_history"] = []
                st.experimental_rerun()


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
elif page == "Classified Ad Writer":
    page_classified_writer()
elif page == "Manual & Assets":
    page_manual_assets()
elif page == "System Checklist":
    page_system_checklist()
elif page == "Traffic & Networks":
    page_traffic_networks()
elif page == "Settings & Integrations":
    page_settings()

