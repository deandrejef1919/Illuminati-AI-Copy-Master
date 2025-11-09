import streamlit as st
import textwrap
from typing import List, Tuple, Dict

# -------------------------
# Page config & base style
# -------------------------

st.set_page_config(
    page_title="Illuminati AI Copy Master",
    page_icon="🔺",
    layout="wide",
)

# Custom CSS: red / black / gold theme
APP_CSS = """
<style>
/* Global */
body, .stApp {
    background-color: #050506;
    color: #f2f2f2;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Main container */
.block-container {
    padding-top: 1.5rem;
}

/* Illuminati-style header */
.illuminati-header {
    text-align: center;
    padding: 1rem 0 0.5rem 0;
}
.illuminati-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #f5d76e;
    text-shadow: 0 0 12px rgba(245, 215, 110, 0.6);
}
.illuminati-subtitle {
    font-size: 0.95rem;
    color: #f7f7f7;
    opacity: 0.85;
}

/* Pyramid icon container */
.illuminati-pyramid {
    font-size: 2.5rem;
    margin-bottom: 0.25rem;
}

/* Cards */
.illuminati-card {
    border-radius: 12px;
    border: 1px solid rgba(245, 215, 110, 0.18);
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    background: radial-gradient(circle at top, #111113 0, #050506 55%, #000000 100%);
    box-shadow:
        0 0 0 1px rgba(255, 0, 0, 0.05),
        0 0 22px rgba(245, 215, 110, 0.12);
}

/* Accent text */
.illuminati-accent {
    color: #f5d76e;
    font-weight: 600;
}

/* Buttons */
div.stButton > button {
    border-radius: 999px;
    border: 1px solid #f5d76e;
    background: linear-gradient(135deg, #9b111e, #5c020b);
    color: #fff;
    font-weight: 600;
    box-shadow: 0 0 12px rgba(155, 17, 30, 0.7);
}
div.stButton > button:hover {
    border-color: #ffffff;
    box-shadow: 0 0 18px rgba(245, 215, 110, 0.85);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: radial-gradient(circle at top, #1b0a0f 0, #050506 55%, #000000 100%);
}
section[data-testid="stSidebar"] * {
    color: #f5f5f5 !important;
}
</style>
"""

st.markdown(APP_CSS, unsafe_allow_html=True)


# -------------------------
# Copywriting knowledge
# -------------------------

MASTER_FLAVORS: Dict[str, str] = {
    "Gary Halbert": "raw, emotional, street-smart letter that pokes at greed, fear, curiosity, and desire",
    "David Ogilvy": "research-driven, benefit-heavy copy with strong proof and specifics",
    "Dan Kennedy": "no-BS, direct-response copy with clear promises, deadlines, and risk reversal",
    "Claude Hopkins": "scientific advertising with specific, testable claims and strong self-interest",
    "Joe Sugarman": "slippery-slide, curiosity-driven narrative with sensory detail",
    "Eugene Schwartz": "deeply desire-focused copy tuned to the market’s level of awareness",
    "John Carlton": "punchy, conversational, 'killer hook' copy with urgency and attitude",
    "Jay Abraham": "preeminence-based, value-stacking copy that makes your offer a no-brainer",
    "Robert Bly": "classic direct-response with 4U headlines and long-form structure",
    "Neville Medhora": "short, simple, scannable copy with humor and directness",
    "Joanna Wiebe": "voice-of-customer heavy copy that sounds like the reader and feels tested",
    "Hybrid Mix": "a blended style drawing from all the masters above",
}

AWARENESS_ANGLE: Dict[str, str] = {
    "Unaware": "start by dramatizing a problem they’re feeling but haven’t named yet, then reveal the real cause and finally your solution.",
    "Problem-aware": "agitate the pain they already recognize, then introduce your new mechanism as the missing key.",
    "Solution-aware": "contrast your unique mechanism against the usual solutions they’ve likely tried and show why yours is different.",
    "Product-aware": "focus on proof, specifics, and reasons to act now versus postponing the decision.",
    "Most-aware": "focus on offer mechanics, bonuses, scarcity, and a very clear reason to pull the trigger today.",
}

# Niche presets for quick targeting
NICHE_DEFAULTS: Dict[str, Dict[str, List[str]]] = {
    "Natural / Alternative Healing": {
        "audience": [
            "a health-conscious adult who wants natural ways to feel better without living at the doctor’s office"
        ],
        "benefits": [
            "relieve nagging symptoms without harsh drugs",
            "support your body’s natural healing process",
            "follow a simple daily routine you can actually stick to",
        ],
    },
    "Spirituality & Alternative Beliefs": {
        "audience": [
            "a seeker who feels there’s more to life than bills, stress, and endless scrolling"
        ],
        "benefits": [
            "feel calm and centered, even when life is chaotic",
            "develop a deeper sense of purpose and direction",
            "connect with like-minded people who actually get you",
        ],
    },
    "Specific Health Problems": {
        "audience": [
            "someone who’s tired of treating symptoms while the real cause never gets solved"
        ],
        "benefits": [
            "finally understand what’s really driving your symptoms",
            "use step-by-step actions instead of random guessing",
            "feel a real difference in your energy and mood",
        ],
    },
    "Vanity Niches": {
        "audience": [
            "someone who wants to look in the mirror and actually like what they see"
        ],
        "benefits": [
            "turn quiet insecurity into visible confidence",
            "stand out in photos instead of hiding from the camera",
            "get noticed without having to shout for attention",
        ],
    },
    "Relationships": {
        "audience": [
            "someone who’s tired of feeling invisible, unwanted, or misunderstood in love"
        ],
        "benefits": [
            "feel desired and chosen instead of ignored",
            "stop repeating the same painful relationship patterns",
            "create the kind of connection other people envy",
        ],
    },
    "Money & Business": {
        "audience": [
            "an ambitious action-taker who’s sick of watching other people make the money they want"
        ],
        "benefits": [
            "turn scattered effort into focused income-producing action",
            "build assets instead of just trading time for money",
            "finally follow a plan that has a real shot at working",
        ],
    },
    "General Interest & Survival": {
        "audience": [
            "someone who wants to be prepared when things go wrong instead of hoping for the best"
        ],
        "benefits": [
            "protect your family when systems fail",
            "have what you need when other people are scrambling",
            "sleep better knowing you’re not at the mercy of chaos",
        ],
    },
}


# -------------------------
# Small helper functions
# -------------------------

def normalize_audience(audience: str) -> str:
    """
    Make the audience line read naturally after 'If you're ...'.
    """
    if not isinstance(audience, str) or not audience.strip():
        return "someone who needs what you offer"

    raw_aud = audience.splitlines()[0].strip()
    lowered = raw_aud.lower()

    # Starts nicely already?
    if lowered.startswith(("a ", "an ", "the ")):
        return raw_aud

    # Has 'who' or 'and' -> treat as group description
    if " who " in lowered or " and " in lowered:
        return f"someone like {raw_aud}"

    # Fallback
    return f"someone who is {raw_aud}"


def choose_niche_defaults(niche: str) -> Tuple[str, List[str]]:
    """
    Return (audience_line, benefits_list) defaults for a chosen niche.
    """
    data = NICHE_DEFAULTS.get(niche)
    if not data:
        return (
            "someone who needs what you offer",
            [
                "get results without feeling overwhelmed",
                "follow a simple step-by-step plan",
                "feel confident you’re finally doing this right",
            ],
        )
    aud = data["audience"][0]
    benefits = data["benefits"]
    return aud, benefits


def generate_rule_based_copy(
    product_name: str,
    product_desc: str,
    audience: str,
    tone: str,
    benefits_list: List[str],
    cta: str,
    awareness: str,
    master_style: str,
    niche: str,
) -> Tuple[List[str], str]:
    """
    Pure rule-based generator: headlines + sales copy,
    infused with masters & awareness angle.
    """

    # Niche fallbacks if fields are weak
    if not audience.strip():
        niche_aud, _ = choose_niche_defaults(niche)
        audience = niche_aud

    if not benefits_list:
        _, niche_benefits = choose_niche_defaults(niche)
        benefits_list = niche_benefits

    base_benefit = benefits_list[0]
    audience_short = normalize_audience(audience)

    style_flavor = MASTER_FLAVORS.get(
        master_style,
        "direct-response style copy tuned for conversions",
    )
    awareness_angle = AWARENESS_ANGLE.get(
        awareness,
        "meet them where they are and lead them step-by-step toward a buying decision.",
    )

    # --------------------
    # Headlines
    # --------------------
    headlines: List[str] = []

    first_aud_line = audience.splitlines()[0].strip() if audience else "your market"

    headlines.append(
        f"How {first_aud_line.capitalize()} Can {base_benefit.capitalize()} with {product_name}"
    )

    # This is the fixed line that previously caused the syntax error:
    headlines.append(
        f'{product_name}: The "{base_benefit.capitalize()}" Shortcut You Can Use Starting Tonight'
    )

    headlines.append(
        f"Finally: A {product_name} That Helps You {base_benefit.capitalize()} Without The Usual B.S."
    )

    headlines.append(
        f"Do You Make These Mistakes When You Try To {base_benefit.capitalize()}?"
    )

    time_phrase = (
        "30 Days"
        if ("day" in product_desc.lower() or "30" in product_desc)
        else "One Shot"
    )
    headlines.append(
        f"Give Me {time_phrase}, And I’ll Show You How To {base_benefit.capitalize()} With {product_name}"
    )

    headlines.append(
        f"{product_name}: Built For {first_aud_line.capitalize()}, Not For The Masses"
    )

    if len(benefits_list) > 1:
        second_benefit = benefits_list[1]
        headlines.append(
            f"Turn '{second_benefit.capitalize()}' Into Your Unfair Advantage With {product_name}"
        )

    # --------------------
    # Sales copy
    # --------------------
    bullets = "".join([f"- {b}\n" for b in benefits_list])

    sales_copy = textwrap.dedent(
        f"""
        [{master_style}-inspired angle – {style_flavor}]

        ATTENTION

        If you're {audience_short}, there's a good chance the problem is not you...
        it's the message you're putting in front of your market.

        Right now, your prospects are scrolling past *yet another* promise that sounds
        exactly like every other one they’ve seen. And deep down, they’ve learned
        not to believe those.

        INTEREST

        **{product_name}** is built to fix that.

        {product_desc.strip()}

        Instead of shouting into the void, you start speaking directly to what your
        market already obsesses over most. You stop trying to “educate” strangers
        with bland logic, and you begin to tap the emotional, selfish reasons
        they’ll *gladly* say yes.

        In practice, that means you {awareness_angle}

        DESIRE

        Here’s what that looks like when it’s working for you:

        {bullets}

        Each line of copy becomes another little “yes” that stacks in their mind.
        They stop skimming and start imagining actually living with the benefit
        you’re describing.

        ACTION

        If you're serious about {base_benefit.lower()} and ready to use copy that
        finally matches the real value you deliver, this is your move:

        **{cta.strip().rstrip('.')}**

        Don’t wait for “someday traffic” or “someday buyers.”
        You already have visitors. {product_name} helps you turn more of them
        into customers *today*.
        """
    ).strip()

    return headlines, sales_copy


def generate_email_sequence(
    product_name: str,
    product_desc: str,
    audience: str,
    benefits_list: List[str],
    master_style: str,
    awareness: str,
    num_emails: int = 5,
) -> List[Dict[str, str]]:
    """
    Simple long-form sequence generator: problem -> story -> proof -> offer -> last call.
    """
    if not benefits_list:
        benefits_list = [
            "get real, measurable results",
            "stop wasting time on things that don’t move the needle",
            "follow a proven plan instead of guessing",
        ]

    awareness_angle = AWARENESS_ANGLE.get(
        awareness,
        "meet them where they are and lead them toward a confident buying decision.",
    )
    main_benefit = benefits_list[0]

    sequence: List[Dict[str, str]] = []

    # Email 1 – Pattern interrupt / big idea
    subject1 = f"[{master_style}] The painful mistake your {product_name} solves"
    body1 = textwrap.dedent(
        f"""
        Subject: {subject1}

        Hey,

        Chances are, if you’re reading this, you’re {audience or 'someone who’s trying to make real progress without burning out'}.

        And if you’re anything like most people in your situation, you’ve tried
        at least a few different ways to {main_benefit.lower()}…

        • A couple of “miracle” shortcuts  
        • Some advice from random YouTube videos  
        • Maybe even a course or two  

        But somehow, you’re still not where you want to be.

        That’s exactly why **{product_name}** exists.

        It’s not another shiny idea. It’s a structured way to:
        - {benefits_list[0]}
        - {benefits_list[1] if len(benefits_list) > 1 else 'actually feel momentum again'}
        - {benefits_list[2] if len(benefits_list) > 2 else 'have a clear next step every day'}

        In the next few emails, I’ll walk you through how it works, why it’s different,
        and whether it’s right for you.

        Talk soon,
        – Illuminati AI Copy Master
        """
    ).strip()
    sequence.append({"subject": subject1, "body": body1})

    # Email 2 – Story / emotional agitation
    subject2 = f"That moment when you almost gave up on {main_benefit.lower()}…"
    body2 = textwrap.dedent(
        f"""
        Subject: {subject2}

        Hey,

        Every {audience or 'serious action-taker'} has that moment:

        They think, “Maybe this just doesn’t work for me.”

        That’s the moment most people quietly give up.

        What separates the ones who finally break through isn’t willpower or talent…
        it’s having a system that’s actually built for them.

        **{product_name}** was built for that exact turning point.

        Instead of asking you to “try harder,” it helps you:
        - Focus on what actually moves the needle
        - Use a structure that’s been thought through for you
        - See real progress, step by step

        In the next email, I’ll show you what this looks like in practice.

        – Illuminati AI Copy Master
        """
    ).strip()
    sequence.append({"subject": subject2, "body": body2})

    # Email 3 – Proof / mechanism
    subject3 = f"How {product_name} helps you {main_benefit.lower()} (without the usual grind)"
    body3 = textwrap.dedent(
        f"""
        Subject: {subject3}

        Hey,

        Quick breakdown of how **{product_name}** works under the hood:

        1. It starts with where you really are – not a fantasy version.
        2. It maps that to a simple, linear path that makes sense.
        3. It keeps you focused on the one thing that matters this week.

        No more juggling ten tactics at once.

        Remember: the real power here is that we {awareness_angle}

        If that sounds like exactly what you’ve been missing, keep an eye on your inbox.
        Tomorrow, I’ll show you what it looks like to get started.

        – Illuminati AI Copy Master
        """
    ).strip()
    sequence.append({"subject": subject3, "body": body3})

    # Email 4 – Offer reveal
    subject4 = f"Ready to actually {main_benefit.lower()} with {product_name}?"
    body4 = textwrap.dedent(
        f"""
        Subject: {subject4}

        Hey,

        Here’s what you get inside **{product_name}**:

        - A clear, step-by-step path so you’re never guessing what to do next  
        - Tools and templates that save you time and mental energy  
        - A structure you can reuse as you grow  

        If that sounds like what you’ve been looking for, now’s the moment to move.

        ➜ Hit the main CTA on the page and take your next step.

        Talk soon,
        – Illuminati AI Copy Master
        """
    ).strip()
    sequence.append({"subject": subject4, "body": body4})

    # Email 5 – Last call
    subject5 = f"Last call: your next shot at {main_benefit.lower()}"
    body5 = textwrap.dedent(
        f"""
        Subject: {subject5}

        Hey,

        This is the last email in this mini-sequence.

        At this point, you know what **{product_name}** is, who it’s for,
        and how it can help you {main_benefit.lower()}…

        So this comes down to a simple choice:

        • Keep doing what you’ve been doing, and get more of the same  
        • Or take one deliberate step toward the result you say you want  

        If you’re choosing the second option, here’s what to do:

        ➜ Go back to the page and click the main call to action.

        Either way, thanks for reading.

        – Illuminati AI Copy Master
        """
    ).strip()
    sequence.append({"subject": subject5, "body": body5})

    return sequence[:num_emails]


def generate_classified_ads(
    product_name: str,
    product_desc: str,
    audience: str,
    niche: str,
    master_style: str,
    cta: str,
    num_ads: int = 3,
) -> List[str]:
    """
    Short, punchy classified-style ads tuned to niche + master.
    """

    if not audience.strip():
        audience, _ = choose_niche_defaults(niche)
    aud_short = normalize_audience(audience)

    desc_short = product_desc.strip()
    if len(desc_short) > 220:
        desc_short = desc_short[:217].rstrip() + "..."

    template_lines: List[str] = []

    for _ in range(num_ads):
        if master_style == "Gary Halbert":
            hook = f"STOP: {product_name} For {aud_short.capitalize()}"
        elif master_style == "David Ogilvy":
            hook = f"{product_name}: The {niche} Breakthrough You Haven’t Tried Yet"
        elif master_style == "Dan Kennedy":
            hook = f"Serious About {niche}? Read This Before You Waste Another Dollar."
        elif master_style == "Joe Sugarman":
            hook = f"It Started With One Simple {product_name}..."
        elif master_style == "Eugene Schwartz":
            hook = f"Already Tried Everything In {niche}? This Is Different."
        else:
            hook = f"{product_name} For {niche}: Limited Spots."

        body = textwrap.dedent(
            f"""
            {hook}

            {desc_short}

            Built for {aud_short} who want real results, not theory.

            {cta.strip().rstrip('.')}.
            """
        ).strip()

        template_lines.append(body)

    return template_lines


# -------------------------
# UI page functions
# -------------------------

def render_header():
    st.markdown(
        """
        <div class="illuminati-header">
            <div class="illuminati-pyramid">🔺</div>
            <div class="illuminati-title">ILLUMINATI AI COPY MASTER</div>
            <div class="illuminati-subtitle">
                Turn cold traffic into hot buyers with AI-copy inspired by Halbert, Ogilvy, Kennedy & the legends.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def page_dashboard():
    render_header()
    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.markdown(
            """
            <div class="illuminati-card">
            <span class="illuminati-accent">Headline:</span><br/>
            <strong>Unlock Million-Dollar Headlines: Turn Visitors into Buyers with Illuminati AI Copy Master.</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="illuminati-card">
            <p>
            This dashboard is your war room for direct-response campaigns in:
            </p>
            <ul>
                <li>Natural / Alternative Healing</li>
                <li>Spirituality & Alternative Beliefs</li>
                <li>Specific Health Problems & Vanity Niches</li>
                <li>Relationships & Dating</li>
                <li>Money, Investing, Online Business</li>
                <li>General Interest, Survival, DFY, and more</li>
            </ul>
            <p>
            Start on <strong>Generate Copy</strong> to build a long-form sales message,
            then move to <strong>Email Sequences</strong> and the <strong>Classified Ad Writer</strong>
            to light up your cold traffic from every angle.
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="illuminati-card">
            <strong>Quick Start:</strong>
            <ol>
                <li>Go to <strong>🧠 Generate Copy</strong> and fill in your offer brief.</li>
                <li>Pick your niche & master style (Halbert, Ogilvy, Kennedy, etc.).</li>
                <li>Generate headlines + sales copy.</li>
                <li>Turn that into an email sequence and classifieds.</li>
                <li>Use <strong>Traffic & Networks</strong> to grab traffic platforms & affiliate networks.</li>
            </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_generate_copy():
    render_header()
    st.subheader("🧠 Generate Copy")

    st.markdown(
        """
        Use this page to create master-inspired headlines and long-form sales copy
        tuned to your niche, audience awareness, and desired tone.
        """
    )

    engine_choice = st.selectbox(
        "Engine Mode",
        ["Rule-based (local templates)", "OpenAI (coming later)", "Gemini (coming later)"],
        index=0,
    )

    col_top1, col_top2, col_top3 = st.columns(3)
    with col_top1:
        niche = st.selectbox(
            "Primary Niche",
            list(NICHE_DEFAULTS.keys()),
            index=0,
        )
    with col_top2:
        master_style = st.selectbox(
            "Master Style Influence",
            list(MASTER_FLAVORS.keys()),
            index=0,
        )
    with col_top3:
        awareness = st.selectbox(
            "Audience Awareness (Eugene Schwartz)",
            ["Unaware", "Problem-aware", "Solution-aware", "Product-aware", "Most-aware"],
            index=2,
        )

    st.markdown("---")
    st.markdown("### ✍️ Copy Brief")

    with st.form("copy_brief_form"):
        product_name = st.text_input("Product / Service Name", "")
        product_desc = st.text_area(
            "Product / Service Description",
            "",
            help="Short description of what it is and how it works.",
        )

        audience = st.text_area(
            "Target Audience (demographics, psychographics, pain points)",
            "",
            placeholder="Example: busy parents who want more energy without crazy gym routines…",
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
            "",
            placeholder="Example:\nLose 10–20 lbs without starving\nKeep energy high all day\nWorks even if you hate the gym",
        )

        cta = st.text_input(
            "Primary Call To Action (CTA)",
            "Click here to get started",
        )

        submitted = st.form_submit_button("⚡ Generate Headlines & Sales Copy")

    if not submitted:
        st.info("Fill in the brief above and hit **Generate** to see copy.")
        return

    if not product_name or not product_desc:
        st.error("Please provide at least a product name and description.")
        return

    benefits_list = [
        line.strip()
        for line in benefits_text.splitlines()
        if line.strip()
    ]

    if engine_choice != "Rule-based (local templates)":
        st.warning(
            "OpenAI / Gemini engines are not wired in this minimal stable version yet. "
            "Using rule-based copy below."
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
        niche=niche,
    )

    st.markdown("### 🎯 Headline Variations")
    for i, h in enumerate(headlines, start=1):
        st.markdown(f"**{i}. {h}**")

    st.markdown("### 📜 Sales Copy Draft")
    st.markdown(sales_copy)

    st.markdown("---")
    st.caption(
        "Remember Ogilvy: “The consumer isn’t a moron, she’s your wife.” "
        "Respect your reader’s intelligence while still selling hard."
    )


def page_email_sequences():
    render_header()
    st.subheader("📧 Email Sequences")

    st.markdown(
        """
        Turn your core sales message into a multi-email sequence designed to warm up cold leads
        and drive them back to your main offer page.
        """
    )

    with st.form("email_seq_form"):
        product_name = st.text_input("Product / Service Name", "")
        product_desc = st.text_area("Product / Service Description", "")
        audience = st.text_area("Audience (copy from Generate Copy if you like)", "")

        benefits_text = st.text_area(
            "Key Benefits (one per line)",
            "",
            placeholder="Copy the same benefits you used above for consistency.",
        )

        master_style = st.selectbox(
            "Master Style Influence",
            list(MASTER_FLAVORS.keys()),
            index=0,
        )

        awareness = st.selectbox(
            "Audience Awareness Level",
            ["Unaware", "Problem-aware", "Solution-aware", "Product-aware", "Most-aware"],
            index=2,
        )

        num_emails = st.slider("Number of emails", 3, 10, 5)

        submitted = st.form_submit_button("📨 Generate Email Sequence")

    if not submitted:
        st.info("Fill in the fields and click **Generate Email Sequence**.")
        return

    if not product_name or not product_desc:
        st.error("Please enter at least a product name and description.")
        return

    benefits_list = [
        line.strip()
        for line in benefits_text.splitlines()
        if line.strip()
    ]

    sequence = generate_email_sequence(
        product_name=product_name,
        product_desc=product_desc,
        audience=audience,
        benefits_list=benefits_list,
        master_style=master_style,
        awareness=awareness,
        num_emails=num_emails,
    )

    st.markdown("### ✉️ Generated Emails")

    for idx, email in enumerate(sequence, start=1):
        with st.expander(f"Email {idx}: {email['subject']}"):
            st.markdown(f"**Subject:** {email['subject']}")
            st.text(email["body"])

    st.caption(
        "Sugarman reminder: each line’s job is to get the next line read. "
        "Use curiosity and story to keep them moving."
    )


def page_classified_writer():
    render_header()
    st.subheader("📢 Classified Ad Writer")

    st.markdown(
        """
        Create short, punchy classified ads tuned to your niche and favorite master’s style.
        Perfect for free classified sites, solo ad swipes, or quick text-based placements.
        """
    )

    col_top1, col_top2 = st.columns(2)
    with col_top1:
        niche = st.selectbox(
            "Niche / Category",
            list(NICHE_DEFAULTS.keys()),
            index=0,
        )
    with col_top2:
        master_style = st.selectbox(
            "Master Style Influence",
            list(MASTER_FLAVORS.keys()),
            index=0,
        )

    with st.form("classified_form"):
        product_name = st.text_input("Product / Offer Name", "")
        product_desc = st.text_area(
            "Short Product Description",
            "",
            placeholder="1–3 sentences that explain what they get and why it matters.",
        )
        audience = st.text_area(
            "Audience (optional – can leave blank to use niche default)",
            "",
        )
        cta = st.text_input(
            "Call to Action",
            "Click here to learn more",
        )
        num_ads = st.slider("Number of variations", 1, 10, 3)

        submitted = st.form_submit_button("📝 Generate Classified Ads")

    if not submitted:
        st.info("Fill in the fields and click **Generate Classified Ads**.")
        return

    if not product_name or not product_desc:
        st.error("You need at least a product name and description.")
        return

    ads = generate_classified_ads(
        product_name=product_name,
        product_desc=product_desc,
        audience=audience,
        niche=niche,
        master_style=master_style,
        cta=cta,
        num_ads=num_ads,
    )

    st.markdown("### 🧾 Classified Ad Variations")
    for i, ad in enumerate(ads, start=1):
        with st.expander(f"Classified Ad {i}"):
            st.text(ad)

    st.caption(
        "Halbert rule of thumb: the job of a classified ad is not to educate, it’s to get the right person to raise their hand."
    )


def page_manual_assets():
    render_header()
    st.subheader("📚 Manual & Lead Magnet Ideas")

    st.markdown(
        """
        This section gives you structured prompts and outlines for lead magnets (PDFs, checklists, mini-guides)
        that plug directly into your campaigns. You can generate copy here, then paste into your design tool (Canva, Google Docs, etc.).
        """
    )

    st.markdown("### Lead Magnet Framing")

    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Core Offer Name", "")
        niche = st.selectbox("Niche", list(NICHE_DEFAULTS.keys()), index=0)
    with col2:
        lead_magnet_type = st.selectbox(
            "Lead Magnet Type",
            [
                "Checklist",
                "Cheat Sheet",
                "Short PDF Guide (5–10 pages)",
                "Email Mini-Course",
            ],
            index=0,
        )

    if st.button("💡 Generate Lead Magnet Angle & Outline"):
        if not product_name:
            st.error("Please add your core offer name first.")
        else:
            aud, benefits = choose_niche_defaults(niche)
            main_benefit = benefits[0] if benefits else "get better results faster"

            title = f"{main_benefit.capitalize()} – Without The Usual Struggle: A {lead_magnet_type} For {aud.capitalize()}"
            st.markdown("#### Suggested Lead Magnet Title")
            st.markdown(f"**{title}**")

            st.markdown("#### Suggested Outline")
            outline = [
                "Big Promise & What They’ll Get In The Next 10 Minutes",
                "Why Most People Fail (Set Up The Gap)",
                "The New Way / Core Framework",
                "Quick Wins They Can Implement Today",
                "Soft Transition Into Your Core Offer",
            ]
            for i, item in enumerate(outline, start=1):
                st.write(f"{i}. {item}")

            st.caption(
                "Use this as the backbone of a PDF or slide deck. You can host the final file on MediaFire or any cloud host."
            )


def page_traffic_networks():
    render_header()
    st.subheader("🚦 Traffic & Networks")

    st.markdown(
        """
        Below are direct links to affiliate networks, banner/solo ad platforms, and free
        classified sites that generally have **low or no special approval barriers**.
        Always double-check each site’s rules and policies.
        """
    )

    st.markdown("### 💰 Affiliate Networks (no special approval beyond signup)")

    affiliate_networks = [
        {
            "name": "ClickBank",
            "url": "https://accounts.clickbank.com/signup/",
            "note": "Huge digital marketplace across many niches.",
        },
        {
            "name": "JVZoo",
            "url": "https://www.jvzoo.com/register",
            "note": "Digital products, IM, software; instant commissions on many offers.",
        },
        {
            "name": "WarriorPlus",
            "url": "https://warriorplus.com/user/new",
            "note": "Internet marketing and business offers.",
        },
        {
            "name": "Digistore24",
            "url": "https://www.digistore24.com/signup",
            "note": "Global marketplace with many health, finance, and IM products.",
        },
        {
            "name": "MaxBounty",
            "url": "https://affiliates.maxbounty.com/register",
            "note": "Top CPA network. Application required, but no special brand approval to join the network.",
        },
        {
            "name": "CJ (Commission Junction)",
            "url": "https://signup.cj.com/member/signup/publisher/",
            "note": "Big brand offers; you apply to each advertiser within the network.",
        },
        {
            "name": "Impact",
            "url": "https://impact.com/partners/affiliate-partners/",
            "note": "Large performance marketing platform with many brands.",
        },
        {
            "name": "PartnerStack",
            "url": "https://dash.partnerstack.com/",
            "note": "SaaS & software affiliate programs; one login, many offers.",
        },
    ]

    for net in affiliate_networks:
        st.markdown(f"- [{net['name']}]({net['url']}) – {net['note']}")

    st.markdown("---")
    st.markdown("### 📊 Banner & Solo Ad / Traffic Platforms")

    traffic_platforms = [
        {
            "name": "Udimi (Solo Ads)",
            "url": "https://udimi.com/signup",
            "note": "Marketplace for buying solo ads from email list owners.",
        },
        {
            "name": "TrafficForMe",
            "url": "https://www.trafficforme.net/",
            "note": "Managed email traffic (biz opp, MMO, etc.).",
        },
        {
            "name": "PropellerAds",
            "url": "https://partners.propellerads.com/#/auth/signUp",
            "note": "Self-serve network for push, pop, and other formats.",
        },
        {
            "name": "Adsterra",
            "url": "https://adsterra.com/",
            "note": "Large global ad network (display, pop, push, etc.).",
        },
        {
            "name": "RichAds",
            "url": "https://my.richads.com/signup",
            "note": "Performance marketing platform with push, pops, direct clicks.",
        },
        {
            "name": "HilltopAds",
            "url": "https://hilltopads.com/signup",
            "note": "Ad network for publishers and advertisers (various formats).",
        },
        {
            "name": "7Search PPC",
            "url": "https://www.7searchppc.com/",
            "note": "Self-service PPC network with multiple verticals.",
        },
    ]

    for plat in traffic_platforms:
        st.markdown(f"- [{plat['name']}]({plat['url']}) – {plat['note']}")

    st.markdown("---")
    st.markdown("### 📣 Free Classified Ad Sites (high-volume platforms)")

    classified_sites = [
        {
            "name": "Craigslist",
            "url": "https://www.craigslist.org/",
            "note": "Massive local classifieds (check each category’s rules).",
        },
        {
            "name": "ClassifiedAds.com",
            "url": "https://www.classifiedads.com/",
            "note": "Free general classifieds site.",
        },
        {
            "name": "Oodle",
            "url": "https://www.oodle.com/",
            "note": "Aggregated local classified ads for many categories.",
        },
        {
            "name": "Geebo",
            "url": "https://geebo.com/",
            "note": "Job, housing, and general classifieds.",
        },
        {
            "name": "Locanto",
            "url": "https://www.locanto.com/",
            "note": "Free user-to-user classifieds in many countries.",
        },
        {
            "name": "Gumtree",
            "url": "https://my.gumtree.com/create-account",
            "note": "UK & other markets classifieds; account required.",
        },
        {
            "name": "Kijiji (Canada)",
            "url": "https://www.kijiji.ca/",
            "note": "Canadian classifieds with local reach.",
        },
        {
            "name": "Facebook Marketplace",
            "url": "https://www.facebook.com/marketplace/",
            "note": "Huge reach; more local/physical but can support list-building angles.",
        },
    ]

    for site in classified_sites:
        st.markdown(f"- [{site['name']}]({site['url']}) – {site['note']}")

    st.markdown("---")
    st.markdown("### 📦 Lead Magnet Hosting (MediaFire)")

    st.markdown(
        """
        - **MediaFire** – free file hosting you can use for PDF lead magnets and assets:  
          👉 [Sign up for a free MediaFire account](https://www.mediafire.com/upgrade/registration.php?pid=free)
        """
    )

    st.caption(
        "Always respect each platform’s rules. Avoid misleading claims, restricted niches, and anything that violates their TOS."
    )


def page_system_checklist():
    render_header()
    st.subheader("✅ System Checklist")

    st.markdown(
        """
        Use this quick checklist to confirm your funnel is ready before you buy traffic.
        (These toggles are just for your own visual tracking; they don’t persist between sessions.)
        """
    )

    st.markdown("### Funnel Assets")

    col1, col2 = st.columns(2)
    with col1:
        lp_done = st.checkbox("Landing / Sales Page copy done")
        emails_done = st.checkbox("Email sequence written & loaded into ESP")
        lead_magnet_done = st.checkbox("Lead magnet created & hosted (MediaFire, etc.)")
    with col2:
        tracking_done = st.checkbox("Tracking links (affiliate IDs, UTMs) configured")
        pixels_done = st.checkbox("Retargeting pixels / tags installed")
        compliance_done = st.checkbox("Compliance checked (claims, images, affiliate rules)")

    st.markdown("### Traffic & Offers")

    col3, col4 = st.columns(2)
    with col3:
        offer_selected = st.checkbox("Core offer(s) selected from your affiliate networks")
        angle_tested = st.checkbox("At least 2–3 angles / hooks ready for testing")
    with col4:
        classified_ready = st.checkbox("Classified ads written for chosen sites")
        solo_ready = st.checkbox("Solo ad swipe ready for Udimi / TrafficForMe")

    st.markdown("### Mental Check")

    st.write(
        "- Do you have a clear daily traffic plan (how many clicks, from where)?\n"
        "- Do you know how you’ll follow up with leads for 7–30 days?\n"
        "- Do you have at least one backup offer if the first one underperforms?"
    )

    st.caption("Legend wisdom: money is made in preparation and follow-up, not in guessing.")


def page_settings_integrations():
    render_header()
    st.subheader("⚙️ Settings & Integrations")

    st.markdown(
        """
        This simple version of **Illuminati AI Copy Master** is mostly rule-based and doesn’t require configuration.
        But if you want to wire in external AI engines later, here’s how.
        """
    )

    st.markdown("### OpenAI & Gemini (for future use)")
    st.markdown(
        """
        In Streamlit Cloud, go to **App → Settings → Secrets** and add:

        ```toml
        OPENAI_API_KEY = "sk-..."
        GEMINI_API_KEY = "..."
        ```

        Then, in a future upgraded version, the **Engine Mode** dropdown on *Generate Copy*
        can call those APIs instead of (or in addition to) the rule-based templates.
        """
    )

    st.markdown("### ESPs & Funnels")
    st.markdown(
        """
        - You can connect email sequences from this app into any ESP (like SendPulse, AWeber, GetResponse)  
        - Paste the subject lines and bodies into your autoresponder flows  
        - Use the **Traffic & Networks** section to decide where to send paid clicks
        """
    )

    st.caption(
        "This version focuses on copy generation and strategy. Full API-based automation, tracking, and ESP integration can be layered on top as a next phase."
    )


# -------------------------
# Main navigation
# -------------------------

def main():
    with st.sidebar:
        st.markdown("### 🔺 Illuminati AI")
        page = st.radio(
            "Navigate",
            [
                "Dashboard",
                "Generate Copy",
                "Email Sequences",
                "Classified Ad Writer",
                "Manual & Lead Magnet",
                "Traffic & Networks",
                "System Checklist",
                "Settings & Integrations",
            ],
        )

    if page == "Dashboard":
        page_dashboard()
    elif page == "Generate Copy":
        page_generate_copy()
    elif page == "Email Sequences":
        page_email_sequences()
    elif page == "Classified Ad Writer":
        page_classified_writer()
    elif page == "Manual & Lead Magnet":
        page_manual_assets()
    elif page == "Traffic & Networks":
        page_traffic_networks()
    elif page == "System Checklist":
        page_system_checklist()
    elif page == "Settings & Integrations":
        page_settings_integrations()


if __name__ == "__main__":
    main()

