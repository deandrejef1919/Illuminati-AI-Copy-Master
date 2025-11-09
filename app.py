# 🔺 Illuminati AI Copy Master – Full App with Email Sequences
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
    st.session_state["checklist_presets"] = {}

if "campaign_history" not in st.session_state:
    st.session_state["campaign_history"] = []

# --- Sidebar Navigation ---
st.sidebar.markdown("### 🔺 Illuminati AI Copy Master")
st.sidebar.caption("Strategic Copy & Traffic Command Console")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Generate Copy",
        "Email Sequences",
        "Classified Ad Writer",
        "Manual & Assets",
        "System Checklist",
        "Traffic & Networks",
        "Settings & Integrations",
    ],
)

# === Helpers: API keys from secrets or session ===


def get_openai_key():
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    key = st.session_state.get("openai_api_key", "").strip()
    return key or None


def get_gemini_key():
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    key = st.session_state.get("gemini_api_key", "").strip()
    return key or None


def generate_with_openai(prompt: str) -> str:
    api_key = get_openai_key()
    if not api_key:
        raise RuntimeError("No OpenAI API key found in secrets or session.")

    if openai is None:
        raise RuntimeError("openai library is not installed.")

    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a world-class direct response copywriter.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.75,
    )
    return resp["choices"][0]["message"]["content"].strip()


def generate_with_gemini(prompt: str) -> str:
    api_key = get_gemini_key()
    if not api_key:
        raise RuntimeError("No Gemini API key found in secrets or session.")

    if genai is None:
        raise RuntimeError("google-generativeai library is not installed.")

    genai.configure(api_key=api_key)

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
    base_benefit = (
        benefits_list[0] if benefits_list else "get better results with less effort and stress"
    )

    if awareness == "Unaware":
        awareness_angle = (
            "lead with curiosity and a bold, intriguing promise that wakes them up."
        )
    elif awareness == "Problem-aware":
        awareness_angle = (
            "agitate the pain they already feel and show you truly understand it."
        )
    elif awareness == "Solution-aware":
        awareness_angle = "contrast old frustrating solutions with your better approach."
    elif awareness == "Product-aware":
        awareness_angle = (
            "stack proof, specifics, and reasons to act today with your product."
        )
    else:
        awareness_angle = (
            "reinforce the offer, sweeten the deal, and remove every ounce of risk."
        )

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

    if isinstance(audience, str) and audience.strip():
        audience_short = audience.splitlines()[0].strip()
    else:
        audience_short = "struggling to convert attention into actual sales"

    headlines = []

    headlines.append(
        f"{base_benefit} — without the usual "
        f"{'stress' if 'without' not in base_benefit.lower() else 'roadblocks'}"
    )

    headlines.append(
        f"How to {base_benefit.lower()} with {product_name} "
        "(Even If You Feel You've Tried Everything)"
    )

    headlines.append(
        f"The {product_name} Shortcut That Quietly Turns Cold Traffic into Buyers"
    )

    first_audience_line = (
        audience.splitlines()[0] if audience else "ambitious entrepreneurs"
    )
    headlines.append(
        f"New for {first_audience_line}: {product_name} That Finally Makes Your Traffic Pay"
    )

    headlines.append(
        f"Use {product_name} to {base_benefit.lower()} in the Next 30 Days... Or Less"
    )

    if len(benefits_list) > 1:
        second_benefit = benefits_list[1]
        headlines.append(
            f"Turn {second_benefit.lower()} into your unfair advantage with {product_name}"
        )

    bullets = (
        "".join([f"- {b}\n" for b in benefits_list])
        if benefits_list
        else "- Clear, measurable results\n"
    )

    sales_copy = f"""[{master_style}-inspired angle – {style_flavor}]

ATTENTION

If you're {audience_short}, there's a good chance the problem is not you...
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


def generate_rule_based_email_sequence(
    product_name: str,
    product_desc: str,
    audience: str,
    benefits_list,
    cta: str,
    goal: str,
    seq_type: str,
    master_style: str,
    num_emails: int,
    tone: str,
):
    """Simple rule-based email sequence generator with master-style flavor."""
    if isinstance(audience, str) and audience.strip():
        audience_short = audience.splitlines()[0].strip()
    else:
        audience_short = "people who need this solution"

    main_benefit = benefits_list[0] if benefits_list else "get better results with less effort"
    extra_benefit = benefits_list[1] if len(benefits_list) > 1 else main_benefit

    style_note = {
        "Gary Halbert": "Expect drama, storytelling, and emotional hooks.",
        "David Ogilvy": "Expect clarity, specifics, and strong benefits.",
        "Dan Kennedy": "Expect no-BS, money/results-focused messaging.",
        "Joe Sugarman": "Expect curiosity and slippery-slide storytelling.",
        "Eugene Schwartz": "Expect awareness-based buildup of desire.",
        "John Carlton": "Expect punchy, conversational, street-smart lines.",
        "Jay Abraham": "Expect preeminence and value stacking.",
        "Robert Bly": "Expect clear structure and practical benefits.",
        "Neville Medhora": "Expect short, fun, human-sounding emails.",
        "Joanna Wiebe": "Expect voice-of-customer-driven, sharp microcopy.",
        "Hybrid Mix": "Expect a balanced blend of old-school and modern persuasion.",
    }.get(master_style, "Classic direct response tone.")

    if "launch" in seq_type.lower():
        archetype = "launch"
    elif "welcome" in seq_type.lower():
        archetype = "welcome"
    elif "nurture" in seq_type.lower():
        archetype = "nurture"
    elif "re-engage" in seq_type.lower() or "reengage" in seq_type.lower():
        archetype = "reengage"
    else:
        archetype = "generic"

    emails = []

    for i in range(1, num_emails + 1):
        if archetype == "welcome":
            if i == 1:
                subject = f"Welcome – here’s your {product_name} insider advantage"
                body = f"""Hey there,

Thanks for joining us. If you're like most {audience_short}, you've been looking for a simple way to {main_benefit.lower()}.

{product_name} was built for exactly that.

In the next few days, I'll show you how to:
- {main_benefit}
- {extra_benefit}
- Turn what you already know into real results

For now, take 30 seconds and {cta.strip().rstrip('.')}.
"""
            elif i == 2:
                subject = f"The big problem nobody told {audience_short} about"
                body = f"""Hey,

Let’s talk about the real problem.

Most {audience_short.lower()} don’t fail because they’re lazy. They fail because nobody gave them a simple, proven path.

That’s what {product_name} gives you:
- Clarity on what actually matters
- A step-by-step way to use it
- Confidence that you’re not guessing anymore

If that sounds like what you’ve been missing, {cta.strip().rstrip('.')}.
"""
            else:
                subject = f"Quick win: one simple move to {main_benefit.lower()}"
                body = f"""Hey,

Here’s a quick win for you:

Pick just one tiny piece of {product_name} and put it into action today.
Don’t wait for “perfect” – just start.

You’ll be shocked at how fast small moves add up.

When you’re ready to lean in fully, {cta.strip().rstrip('.')}.
"""
        elif archetype == "launch":
            if i == 1:
                subject = f"NEW: {product_name} is live – built for {audience_short}"
                body = f"""Hey,

This is the first time I’m opening up {product_name} to {audience_short}.

If you’ve ever wanted to {main_benefit.lower()} without the usual frustration and guesswork,
this is your early chance.

Right now, you can:
- Be among the first to use it
- Lock in early pricing
- Start seeing results before everyone else

Get the full story and details here:
{cta.strip().rstrip('.')}.
"""
            elif i == 2:
                subject = f"The real reason {audience_short} struggle with {goal.lower()}"
                body = f"""Hey,

Let’s be blunt.

Most {audience_short.lower()} are stuck because they’re trying to fix the wrong problem.

{product_name} attacks the real issue:
- It simplifies your path to {main_benefit.lower()}
- It shows you exactly what to do next
- It turns “someday” into a concrete plan

This window won’t stay open forever.
{cta.strip().rstrip('.')}.
"""
            elif i == num_emails:
                subject = f"Last call: {product_name} {goal} window closing"
                body = f"""Hey,

This is your last reminder.

The current opportunity for {product_name} is closing, and once it does, you’ll either:
- Have taken your shot, or
- Be watching others get results while you’re still “thinking about it.”

If {main_benefit.lower()} matters to you, do this now:
{cta.strip().rstrip('.')}.
"""
            else:
                subject = f"See {product_name} in action (real-world benefits)"
                body = f"""Hey,

Quick snapshot of what {product_name} can do for you:

Imagine waking up knowing exactly how to {main_benefit.lower()}, without wondering what to try next.
Imagine having a clear, simple path laid out for you.

That’s what this was built for.

See it laid out here:
{cta.strip().rstrip('.')}.
"""
        elif archetype == "reengage":
            if i == 1:
                subject = f"Still interested in {main_benefit.lower()}?"
                body = f"""Hey,

You grabbed information about {product_name} before, but never fully jumped in.

Totally normal.

If {main_benefit.lower()} is still important to you, now’s a good time to take another look.

Here’s the direct link:
{cta.strip().rstrip('.')}.
"""
            else:
                subject = f"If you’re still reading this, here’s your next move"
                body = f"""Hey,

The fact that you’re opening this email tells me you still care about {main_benefit.lower()}.

You don’t need more noise… you need one clear action.

Here it is:
{cta.strip().rstrip('.')}.
"""
        else:  # nurture / generic
            if i == 1:
                subject = f"What every {audience_short} should know about {main_benefit.lower()}"
                body = f"""Hey,

If you’re like most {audience_short}, you’ve been promised the world and given almost nothing.

{product_name} is different because:
- It focuses on {main_benefit.lower()}
- It respects your time
- It gives you a clear, usable process

In the next emails, I’ll show you how to think about {goal.lower()} like the top {master_style} style marketers would.

For now, take a look at what’s possible:
{cta.strip().rstrip('.')}.
"""
            elif i == 2:
                subject = f"The “quiet” mistake that kills {goal.lower()}"
                body = f"""Hey,

There’s a mistake almost nobody talks about.

Most people try to fix {goal.lower()} by adding more complexity:
more tools, more tricks, more hacks.

{product_name} flips that on its head by stripping things down to what actually works.

If you want less noise and more results, start here:
{cta.strip().rstrip('.')}.
"""
            else:
                subject = f"Ready to {main_benefit.lower()} the smarter way?"
                body = f"""Hey,

You don’t need another theory.

You need something that’s:
- Simple
- Proven
- Built for {audience_short.lower()}

That’s what {product_name} was designed to be.

Check it out while it’s still fresh in your mind:
{cta.strip().rstrip('.')}.
"""

        emails.append({"index": i, "subject": subject, "body": body.strip()})

    output_lines = []
    output_lines.append(f"[{master_style}-inspired email sequence] ({seq_type}, {goal})")
    output_lines.append(f"Tone: {tone}")
    output_lines.append(f"Style note: {style_note}")
    output_lines.append("")

    for e in emails:
        output_lines.append(f"Email {e['index']}:")
        output_lines.append(f"Subject: {e['subject']}")
        output_lines.append("")
        output_lines.append(e["body"])
        output_lines.append("\n" + "-" * 40 + "\n")

    return "\n".join(output_lines)


# --- Dashboard Page ---
def page_dashboard():
    st.title("🔺 Illuminati AI Copy Master")
    st.subheader("AI-Powered Direct Response Control Panel")

    st.markdown(
        """
Welcome to **Illuminati AI Copy Master** — your all-in-one hub for:

- Legendary copywriting frameworks (Ogilvy, Halbert, Kennedy & more)  
- AI-enhanced generation for headlines, sales letters, **email sequences**, and classifieds  
- Built-in manual & asset generator (PDF + ZIP)  

---
Use the navigation on the left to access:
- **Dashboard** – overview  
- **Generate Copy** – long-form sales copy & headlines  
- **Email Sequences** – full campaigns based on the masters  
- **Classified Ad Writer** – short ads for free/paid classifieds  
- **Manual & Assets** – Illuminati AI manual package  
- **System Checklist** – launch checklist with presets  
- **Traffic & Networks** – traffic sources & quick analyzer + history  
- **Settings & Integrations** – engine mode & API keys  
"""
    )


# --- Generate Copy Page ---
def page_generate_copy():
    st.header("🧠 Generate Copy")

    default_engine = st.session_state.get("engine_mode", "Rule-based")
    engine_choice = st.selectbox(
        "Engine",
        ["Rule-based", "OpenAI", "Gemini"],
        index=["Rule-based", "OpenAI", "Gemini"].index(default_engine),
        help="Rule-based uses local templates only. OpenAI / Gemini use external AI models.",
    )
    st.session_state["engine_mode"] = engine_choice
    st.markdown(f"**Current engine mode:** `{engine_choice}`")
    st.markdown("---")
    st.markdown("### ✍️ Copy Brief")

    with st.form("copy_brief_form"):
        product_name = st.text_input("Product / Service Name", "")
        product_desc = st.text_area("Product / Service Description", "")
        audience = st.text_area(
            "Target Audience (demographics, psychographics, pain points)", ""
        )
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
            ["Unaware", "Problem-aware", "Solution-aware", "Product-aware", "Most-aware"],
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
        st.info(
            "Fill out the brief and click **Generate** to see headline ideas and a sales copy draft."
        )
        return

    if not product_name or not product_desc:
        st.error("Please provide at least a product name and description.")
        return

    benefits_list = [b.strip() for b in benefits_text.split("\n") if b.strip()]

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

Write primarily in the style of: {master_style}.

Use AIDA, PAS, and FAB frameworks.

Product / Service Name:
{product_name}

Description:
{product_desc}

Audience:
{audience}

Tone:
{tone}

Benefits:
{', '.join(benefits_list) if benefits_list else 'N/A'}

Call to action:
{cta}

Awareness level:
{awareness}

TASK:

1. Generate 5–8 high-converting headlines optimized for cold traffic.
2. Then write a long-form sales copy draft that:
   - Hooks hard in the first 2–3 sentences
   - Agitates the core pains
   - Presents the product as the natural solution
   - Uses bullets for benefits
   - Ends with the CTA above.

OUTPUT:
Write the headlines clearly numbered, then the full sales copy below.
""".strip()

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
        st.markdown("### 📜 Sales Copy Draft (Rule-based)")
        st.code(sales_copy, language="markdown")
        return

    if engine_choice == "OpenAI":
        try:
            ai_text = generate_with_openai(prompt)
            st.markdown("### 🤖 OpenAI Output")
            st.markdown(ai_text)
            return
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

    if engine_choice == "Gemini":
        try:
            ai_text = generate_with_gemini(prompt)
            st.markdown("### 🤖 Gemini Output")
            st.markdown(ai_text)
            return
        except Exception:
            st.warning(
                "Gemini is currently not available from this environment (model 404s). "
                "Using rule-based copy instead. You can switch to OpenAI in Settings for AI-generated copy."
            )
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


# --- Email Sequences Page ---
def page_email_sequences():
    st.header("📨 Email Sequences (Masters-Inspired)")

    st.markdown(
        """
Build complete email sequences influenced by the greats:

- Halbert launch flurries  
- Ogilvy-style onboarding and education  
- Kennedy-style money-talk sequences  
- Sugarman / Schwartz style curiosity + desire ramps  

You can use **Rule-based**, **OpenAI**, or **Gemini** as the engine.
"""
    )

    default_engine = st.session_state.get("engine_mode", "Rule-based")
    engine_choice = st.selectbox(
        "Engine",
        ["Rule-based", "OpenAI", "Gemini"],
        index=["Rule-based", "OpenAI", "Gemini"].index(default_engine),
        help="Rule-based uses templates. OpenAI / Gemini use external AI models.",
    )
    st.session_state["engine_mode"] = engine_choice

    with st.form("email_sequence_form"):
        product_name = st.text_input("Product / Service Name", "")
        product_desc = st.text_area("Product / Service Description", "")
        audience = st.text_area(
            "Target Audience (who are these emails going to?)", ""
        )
        benefits_text = st.text_area(
            "Key Benefits (one per line)",
            placeholder="E.g.\nLose 10 lbs without starving\nWork from home part-time\nGet more leads without cold calling",
        )
        goal = st.text_input(
            "Sequence Goal (e.g. sell main offer, book call, register for webinar)",
            "Sell the main offer",
        )
        cta = st.text_input(
            "Call to Action (plain text - link or instruction)",
            "Click here to get started",
        )
        tone = st.selectbox(
            "Tone",
            [
                "Direct & No-BS",
                "Friendly & Conversational",
                "High-End / Premium",
                "Urgent & Hypey",
                "Calm & Reassuring",
            ],
            index=0,
        )
        seq_type = st.selectbox(
            "Sequence Type",
            [
                "Welcome / Indoctrination",
                "Launch / Open Cart",
                "Nurture / Value-First",
                "Re-engagement / Win-back",
                "Generic Promo Sequence",
            ],
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
        num_emails = st.slider(
            "Number of emails in the sequence", min_value=3, max_value=10, value=5
        )

        submitted = st.form_submit_button("📨 Generate Email Sequence")

    if not submitted:
        st.info("Fill out the brief and click **Generate Email Sequence**.")
        return

    if not product_name or not product_desc or not cta:
        st.error("Please provide at least a product name, description, and CTA.")
        return

    benefits_list = [b.strip() for b in benefits_text.split("\n") if b.strip()]

    if engine_choice == "Rule-based":
        seq_text = generate_rule_based_email_sequence(
            product_name=product_name,
            product_desc=product_desc,
            audience=audience,
            benefits_list=benefits_list,
            cta=cta,
            goal=goal,
            seq_type=seq_type,
            master_style=master_style,
            num_emails=num_emails,
            tone=tone,
        )
        st.markdown("### 🧬 Rule-based Email Sequence Draft")
        st.code(seq_text, language="markdown")
        return

    ai_prompt = f"""
You are a legendary direct response email copywriter, channeling:

- Gary Halbert
- David Ogilvy
- Claude Hopkins
- Joe Sugarman
- Eugene Schwartz
- John Carlton
- Dan Kennedy
- Jay Abraham
- Robert Bly
- Joanna Wiebe
- Neville Medhora

Write primarily in the style of: {master_style}.

TASK:
Write a {num_emails}-email sequence for this offer.

Each email must:
- Start with a compelling subject line
- Have a clear body (short paragraphs, scannable)
- Match this tone: {tone}
- Aim at this sequence goal: {goal}
- End with this call to action: "{cta}"

CONTEXT:

Product / Service Name:
{product_name}

Description:
{product_desc}

Target Audience:
{audience}

Key Benefits:
{benefits_text}

Sequence Type:
{seq_type}

OUTPUT FORMAT (IMPORTANT):

Email 1:
Subject: ...
Body:
...

Email 2:
Subject: ...
Body:
...

(Continue up to Email {num_emails})
""".strip()

    if engine_choice == "OpenAI":
        try:
            ai_text = generate_with_openai(ai_prompt)
            st.markdown("### 🤖 OpenAI Email Sequence")
            st.markdown(ai_text)
            return
        except Exception as e:
            st.error(f"OpenAI email sequence generation failed: {e}")
            return

    if engine_choice == "Gemini":
        try:
            ai_text = generate_with_gemini(ai_prompt)
            st.markdown("### 🤖 Gemini Email Sequence")
            st.markdown(ai_text)
            return
        except Exception:
            st.warning(
                "Gemini is currently not available from this environment (model 404s). "
                "Switch to Rule-based or OpenAI for email sequences."
            )
            return


# --- Classified Ad Writer Page ---
def page_classified_writer():
    st.header("📢 Classified Ad Writer")

    st.markdown(
        """
Generate short, punchy classified ads for:

- Free classified sites (Craigslist, Locanto, etc.)  
- Low-friction marketplaces  
- Simple text-based placements  

You can use **Rule-based**, **OpenAI**, or **Gemini** as the engine.
"""
    )

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
            help="Keep this tight. We'll trim it further so it fits classified formats.",
        )
        location = st.text_input("Location / Market (optional)", "Online / Worldwide")
        audience = st.text_area(
            "Ideal Prospect (who should respond?)",
            "",
            help="One or two lines max. If you paste a long avatar, we'll only use the first line.",
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

        num_ads = st.slider(
            "How many ad variations?", min_value=3, max_value=8, value=5
        )

        submitted = st.form_submit_button("🧲 Generate Classified Ads")

    if not submitted:
        st.info("Fill in the details above and click **Generate Classified Ads**.")
        return

    if not product_name or not product_desc or not contact:
        st.error(
            "Please provide at least a product name, short description, and contact/link."
        )
        return

    benefits_list = [b.strip() for b in benefits_text.split("\n") if b.strip()]
    audience_short = (
        audience.splitlines()[0].strip()
        if isinstance(audience, str) and audience.strip()
        else "people who are ready for a change"
    )

    desc_short = product_desc.strip()
    if len(desc_short) > 220:
        desc_short = desc_short[:217] + "..."

    base_benefit = (
        benefits_list[0] if benefits_list else "get real results without the usual struggle"
    )
    second_benefit = benefits_list[1] if len(benefits_list) > 1 else None

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

    if engine_choice == "Rule-based":
        ads = []

        for i in range(num_ads):
            pattern_type = i % 3

            if pattern_type == 0:
                headline = f"{base_benefit} – {product_name}"
                body_lines = [
                    desc_short,
                    f"Perfect for {audience_short} in {location}.",
                    contact,
                ]
            elif pattern_type == 1:
                benefit_line = second_benefit or base_benefit
                headline = f"{product_name}: {benefit_line}"
                body_lines = [
                    desc_short,
                    f"If you're {audience_short.lower()}, this was built for you.",
                    contact,
                ]
            else:
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

    prompt = f"""
You are a legendary direct response copywriter specializing in short classified ads,
channeling the style of {master_style}.

Write in a way that feels like: {style_hint}

TASK:
Write {num_ads} different classified ads for the following offer.

Each ad must:
- Have ONE short headline
- Have 1–3 short sentences of body copy
- Be optimized for response on classified ad sites (e.g., Craigslist, Locanto, etc.)
- Use clear, simple, human language
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

OUTPUT FORMAT:

AD 1:
Headline: ...
Body: ...

AD 2:
Headline: ...
Body: ...

(and so on)
""".strip()

    if engine_choice == "OpenAI":
        try:
            ai_text = generate_with_openai(prompt)
            st.markdown("### 🤖 OpenAI Classified Ads")
            st.markdown(ai_text)
            return
        except Exception as e:
            st.error(f"OpenAI classified ad generation failed: {e}")
            return

    if engine_choice == "Gemini":
        try:
            ai_text = generate_with_gemini(prompt)
            st.markdown("### 🤖 Gemini Classified Ads")
            st.markdown(ai_text)
            return
        except Exception:
            st.warning(
                "Gemini is currently not available from this environment (model 404s). "
                "Switch to Rule-based or OpenAI for classified ads."
            )
            return


# --- Manual & Assets Page ---
def page_manual_assets():
    st.header("🔺 Illuminati AI Copy Master Manual & Assets")
    st.markdown(
        """
Generate your **Illuminati AI Copy Master Manual** package:

- PDF manual (lite version for now)  
- Bundled ZIP package ready to download  

Click the button below to generate the package.
"""
    )

    try:
        from generate_illuminati_ai_package import main as generate_illuminati_package_main
    except Exception as e:
        st.error(f"Generator import failed: `{e}`")
        st.stop()

    if st.button("🔺 Forge The Manual of Persuasion"):
        with st.spinner("Forging the manual and ZIP package..."):
            generate_illuminati_package_main()
        st.success("🔺 The manual package has been forged successfully.")

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

    st.markdown(
        """
Use this checklist before you send real traffic to your funnel.

Each item helps make sure:
- Your offer is clear  
- Your pages work  
- Your tracking is live  
- Your traffic isn’t being wasted  
"""
    )

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

    for section_name, items in sections.items():
        st.subheader(section_name)
        for idx, item in enumerate(items):
            key = f"checklist_{section_name}_{idx}"
            checked = st.checkbox(item, key=key)
            total_items += 1
            if checked:
                completed_items += 1
        st.markdown("---")

    percent = int((completed_items / total_items) * 100) if total_items > 0 else 0
    st.markdown(
        f"### 📊 Completion: **{completed_items} / {total_items}** items checked ({percent}%)"
    )

    if percent < 50:
        st.info(
            "You’re still early in the setup. Work through the items above before scaling traffic."
        )
    elif percent < 100:
        st.success(
            "You’re getting close. Tighten any remaining items before pushing harder on ads."
        )
    else:
        st.balloons()
        st.success(
            "All checklist items complete. You’re ready to carefully test and scale traffic."
        )

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

    if st.session_state["checklist_presets"]:
        load_name = st.selectbox(
            "Load preset",
            options=["(Select preset)"]
            + list(st.session_state["checklist_presets"].keys()),
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
        st.caption(
            "No presets saved yet. Save one above to reuse this configuration in this session."
        )


# --- Traffic & Networks Page ---
def page_traffic_networks():
    st.header("🚦 Traffic & Networks")
    st.markdown(
        """
This section gives you a **starting map** of places you can get traffic without heavy approval processes,
plus a quick analyzer so you can compare results from:

- Affiliate offers  
- Banner / solo ad vendors  
- Free classified ad sites  

Always double-check each platform’s current policies and terms — they can change anytime.
"""
    )

    tabs = st.tabs(
        [
            "Affiliate Networks",
            "Banner & Solo Ad Networks",
            "Free Classified Sites",
            "Quick Campaign Analyzer",
        ]
    )

    with tabs[0]:
        st.subheader("🌐 Affiliate Networks (Generally Easy to Join)")
        st.markdown(
            """
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
"""
        )
        st.info(
            "Use these to find offers that match your list, niche, or funnel theme. Start with a small test."
        )

    with tabs[1]:
        st.subheader("📢 Banner & Solo Ad Traffic (Lower Barrier Platforms)")

        st.markdown("**Solo Ad Marketplaces:**")
        st.markdown(
            """
- Udimi  
- TrafficForMe  
- SoloAdsX / similar brokers  
- Individual list sellers (research reputation carefully)  
"""
        )

        st.markdown(
            "**Banner / Display Ad Networks (lower barrier than Google/Meta, but still have policies):**"
        )
        st.markdown(
            """
- PropellerAds  
- Adsterra  
- HilltopAds  
- RichAds  
- 7Search PPC  
"""
        )

        st.warning(
            "Even if signup is easy, you are still responsible for compliance and truthful advertising. "
            "Avoid banned content and always follow their policies."
        )

    with tabs[2]:
        st.subheader("📋 Free Classified Ad Sites (High or Notable Traffic)")
        st.markdown(
            """
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
"""
        )
        st.info(
            "Write like a human local marketer, not a spam bot. Keep claims realistic and truthful."
        )

    with tabs[3]:
        st.subheader("📊 Quick Campaign Analyzer")

        st.markdown(
            """
Use this tool to compare basic performance for campaigns in **Affiliate**, **Banner/Solo**, or **Classifieds**.
Each time you analyze, the result is added to a session-only history below.
"""
        )

        channel = st.selectbox(
            "Channel Type",
            ["Affiliate offer", "Banner / Solo Ads", "Free Classifieds"],
        )

        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign name / label", "")
            source_name = st.text_input("Traffic source / vendor / site", "")
        with col2:
            spend = st.number_input(
                "Ad spend / cost ($)", min_value=0.0, step=1.0
            )
            clicks = st.number_input("Clicks", min_value=0, step=1)
            conversions = st.number_input(
                "Conversions (leads or sales)", min_value=0, step=1
            )
            revenue = st.number_input(
                "Revenue generated ($)", min_value=0.0, step=1.0
            )

        if st.button("Analyze performance"):
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
                st.info(
                    "This test lost money and produced no conversions. Consider changing the offer, angle, or traffic source."
                )
            elif roas < 1:
                st.info(
                    "ROAS is below break-even. Look for ways to improve your messaging, targeting, or back-end monetization."
                )
            elif roas >= 1 and roas < 2:
                st.success(
                    "You are near or above break-even. Tighten the funnel and consider controlled scaling."
                )
            else:
                st.success(
                    "Strong ROAS. Monitor closely and scale carefully without violating any platform rules."
                )

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
            st.caption(
                "No campaigns analyzed yet. Run the analyzer above to add entries."
            )
        else:
            filter_channel = st.selectbox(
                "Filter history by channel",
                options=["(All)"] + sorted(
                    list({h["Channel"] for h in history})
                ),
                index=0,
            )
            if filter_channel != "(All)":
                filtered = [h for h in history if h["Channel"] == filter_channel]
            else:
                filtered = history

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
        index=["Rule-based", "OpenAI", "Gemini"].index(
            st.session_state["engine_mode"]
        ),
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
        st.write(
            "**OpenAI key set:**",
            "✅ Yes" if st.session_state["openai_api_key"] else "❌ No",
        )
    elif st.session_state["engine_mode"] == "Gemini":
        st.write(
            "**Gemini key set:**",
            "✅ Yes" if st.session_state["gemini_api_key"] else "❌ No",
        )

    st.markdown(
        """
*Note:* Keys entered here are only kept in memory for this session.
For long-term, secure storage on Streamlit Cloud, use **Settings → Secrets** in the app dashboard.
"""
    )


# --- Router ---
if page == "Dashboard":
    page_dashboard()
elif page == "Generate Copy":
    page_generate_copy()
elif page == "Email Sequences":
    page_email_sequences()
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

