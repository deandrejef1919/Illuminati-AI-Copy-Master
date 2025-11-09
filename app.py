import streamlit as st
import textwrap
import re
from typing import List, Tuple, Dict

# Try to import requests for Zapier webhooks (fail gracefully if missing)
try:
    import requests  # type: ignore
except ImportError:
    requests = None

# -------------------------
# Page config & base style
# -------------------------

st.set_page_config(
    page_title="Illuminati AI Copy Master",
    page_icon="🔺",
    layout="wide",
)

# Custom CSS: red / black / gold theme with glow + footer
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
    text-shadow:
        0 0 14px rgba(245, 215, 110, 0.95),
        0 0 26px rgba(155, 17, 30, 0.80);
}
.illuminati-subtitle {
    font-size: 0.95rem;
    color: #f7f7f7;
    opacity: 0.85;
}

/* Pyramid icon container with glow */
.illuminati-pyramid {
    font-size: 2.5rem;
    margin-bottom: 0.25rem;
    text-shadow:
        0 0 14px rgba(245, 215, 110, 0.95),
        0 0 26px rgba(155, 17, 30, 0.75);
}

/* Sidebar logo glow */
.sidebar-logo {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0.5rem 0 1.2rem 0;
    color: #f5d76e;
    text-shadow:
        0 0 12px rgba(245, 215, 110, 0.9),
        0 0 24px rgba(155, 17, 30, 0.7);
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

/* Footer */
.illuminati-footer {
    text-align: center;
    font-size: 0.8rem;
    color: #aaaaaa;
    margin-top: 2.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(245, 215, 110, 0.18);
    opacity: 0.9;
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
    "Unaware": "start by dramatizing a problem they’re feeling but haven’t named yet, then reveal the real cause and finally your solution",
    "Problem-aware": "agitate the pain they already recognize, then introduce your new mechanism as the missing key",
    "Solution-aware": "contrast your unique mechanism against the usual solutions they’ve likely tried and show why yours is different",
    "Product-aware": "focus on proof, specifics, and reasons to act now versus postponing the decision",
    "Most-aware": "focus on offer mechanics, bonuses, scarcity, and a very clear reason to pull the trigger today",
}

# Niche presets for quick targeting
NICHE_DEFAULTS: Dict[str, Dict[str, List[str]]] = {
    "Natural / Alternative Healing": {
        "audience": [
            "a busy parent who wants natural ways to feel better without pills"
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
# Helper functions
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


def send_zapier_webhook(url: str, payload: Dict) -> Tuple[bool, str]:
    """
    Minimal helper to POST JSON to a Zapier Catch Hook URL.
    If 'requests' is not available, return a graceful error.
    """
    if not url:
        return False, "No Zapier URL provided."

    if requests is None:
        return False, "The 'requests' library is not available on this server."

    try:
        resp = requests.post(url, json=payload, timeout=10)
        return True, f"Webhook sent. HTTP status: {resp.status_code}"
    except Exception as e:
        return False, f"Error sending webhook: {e}"


# -------------------------
# Optional OpenAI integration (smart brain)
# -------------------------

try:
    import openai
except ImportError:
    openai = None


def call_llm_openai(prompt: str, model: str = "gpt-4o-mini") -> Tuple[bool, str]:
    """
    Call OpenAI with a single prompt. Returns (ok, text_or_error).
    Gracefully handles missing library or missing API key.
    """
    if openai is None:
        return False, "OpenAI library not installed. Add 'openai' to requirements.txt."

    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if not api_key:
        return False, "Missing OPENAI_API_KEY in Streamlit secrets."

    try:
        openai.api_key = api_key
        resp = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a world-class direct-response copywriter combining "
                        "the strengths of Halbert, Ogilvy, Kennedy, Sugarman, Schwartz, "
                        "and modern conversion experts. You improve copy for conversions."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        text = resp.choices[0].message.content.strip()
        return True, text
    except Exception as e:
        return False, f"OpenAI error: {e}"


# -------------------------
# Heuristic copy scoring
# -------------------------

EMOTIONAL_TRIGGERS = [
    "secret", "secrets", "discover", "finally", "weird", "shocking", "hidden",
    "proven", "guaranteed", "guarantee", "instantly", "suddenly", "fear",
    "greed", "curiosity", "strange", "little-known", "breakthrough", "odd",
    "easy", "fast", "quick", "now", "today", "limited", "scarcity",
    "deadline", "risk-free", "no risk", "exclusive",
]

CTA_PHRASES = [
    "click here", "tap here", "join now", "buy now", "order now", "get started",
    "sign up", "enroll now", "start now", "act now", "claim your", "grab your",
]

STRUCTURE_MARKERS = [
    "attention", "interest", "desire", "action",  # AIDA
    "problem", "agitate", "solution",            # PAS
    "guarantee", "testimonial", "proof", "bonus", "faq",
]

def analyze_copy_score(copy_text: str) -> Dict[str, float]:
    """
    Very rough heuristic scoring from 1–100 on likely conversion strength.
    This is NOT a true predictive model, just a structured gut-check.
    """

    if not copy_text or not copy_text.strip():
        return {
            "total_score": 0.0,
            "length_score": 0.0,
            "emotion_score": 0.0,
            "structure_score": 0.0,
            "cta_score": 0.0,
            "specificity_score": 0.0,
        }

    text = copy_text.strip()
    words = re.findall(r"\w+", text)
    n_words = len(words)

    # 1) Length score (very rough – ideal 200–1500 words)
    if n_words < 80:
        length_score = 20.0
    elif n_words < 200:
        # ramp up
        length_score = 20 + (n_words - 80) / (200 - 80) * 40  # up to 60
    elif n_words <= 1500:
        length_score = 60 + min((n_words - 200) / (1500 - 200) * 30, 30)  # up to 90
    else:
        # penalize too long
        over = min((n_words - 1500) / 1500, 1.0)
        length_score = 90 - 30 * over  # down to 60

    # 2) Emotional trigger score
    lower = text.lower()
    emo_hits = sum(1 for trig in EMOTIONAL_TRIGGERS if trig in lower)
    # Cap at 15 hits
    emo_score = min(emo_hits / 15.0, 1.0) * 100

    # 3) Structure markers (AIDA / PAS / proof cues)
    struct_hits = sum(1 for marker in STRUCTURE_MARKERS if marker in lower)
    struct_score = min(struct_hits / 8.0, 1.0) * 100

    # 4) CTA score
    cta_hits = sum(1 for phrase in CTA_PHRASES if phrase in lower)
    if "http://" in lower or "https://" in lower:
        cta_hits += 1
    cta_score = min(cta_hits / 4.0, 1.0) * 100

    # 5) Specificity: digits, %, $, timeframes
    digits = len(re.findall(r"\d", text))
    percents = len(re.findall(r"\d+%", text))
    dollars = len(re.findall(r"\$", text))
    timeframes = len(re.findall(r"\bday\b|\bdays\b|\bweek\b|\bweeks\b|\bmonth\b|\bmonths\b", lower))

    spec_raw = digits + percents + dollars + timeframes
    spec_score = min(spec_raw / 15.0, 1.0) * 100

    # Weighted total
    # Length 20%, emotion 25%, structure 20%, CTA 15%, specificity 20%
    total = (
        length_score * 0.20 +
        emo_score * 0.25 +
        struct_score * 0.20 +
        cta_score * 0.15 +
        spec_score * 0.20
    )

    # Normalize to 0–100
    total_score = max(1.0, min(100.0, total))

    return {
        "total_score": round(total_score, 1),
        "length_score": round(length_score, 1),
        "emotion_score": round(emo_score, 1),
        "structure_score": round(struct_score, 1),
        "cta_score": round(cta_score, 1),
        "specificity_score": round(spec_score, 1),
    }


# -------------------------
# Core copy generators
# -------------------------

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
    Rule-based generator: headlines + sales copy
    with smoother, more congruent master-style flow.
    """

    # --- Defaults from niche if missing ---
    if not audience.strip():
        niche_aud, _ = choose_niche_defaults(niche)
        audience = niche_aud
    if not benefits_list:
        _, niche_benefits = choose_niche_defaults(niche)
        benefits_list = niche_benefits

    base_benefit = benefits_list[0]
    audience_short = normalize_audience(audience)

    style_flavor = MASTER_FLAVORS.get(
        master_style, "direct-response style tuned for conversions"
    )
    awareness_angle = AWARENESS_ANGLE.get(
        awareness, "meet them where they are and lead them step-by-step to a decision"
    )

    # --- Headlines ---
    headlines: List[str] = []

    first_aud_line = audience.splitlines()[0].strip() if audience else "your market"

    headlines.append(
        f"Finally: {product_name} That Helps You {base_benefit.capitalize()} Without The Struggle"
    )
    headlines.append(
        f"How {first_aud_line.capitalize()} Can {base_benefit.capitalize()} with {product_name}"
    )
    headlines.append(
        f'{product_name}: The "{base_benefit.capitalize()}" Shortcut You Can Start Using Today'
    )
    headlines.append(
        f"Do You Make These Mistakes When Trying to {base_benefit.capitalize()}?"
    )
    headlines.append(
        f"The Hidden Shortcut to {base_benefit.capitalize()} No One Told You About"
    )

    if len(benefits_list) > 1:
        headlines.append(
            f'Turn "{benefits_list[1].capitalize()}" Into Your Edge With {product_name}'
        )

    # --- CTA Tone by niche ---
    cta_map = {
        "Natural / Alternative Healing": "Because your body was never designed to be at war with itself.",
        "Spirituality & Alternative Beliefs": "Because your soul has been asking for more — this is you answering.",
        "Specific Health Problems": "Your future self will thank you for not ignoring this moment.",
        "Vanity Niches": "The mirror doesn’t have to be your enemy anymore.",
        "Relationships": "Love rarely fixes itself — it responds when you do.",
        "Money & Business": "Your bank account will remember the choices you make today.",
        "General Interest & Survival": "You don’t rise to the occasion; you fall to your level of preparation.",
    }
    cta_phrase = cta_map.get(
        niche, "Take action now while you’re still thinking about it."
    )

    # --- Emotional intro by master ---
    emotion_intro = {
        "Gary Halbert": "Let’s cut through the noise for a second.",
        "David Ogilvy": "Here’s a fact few advertisers ever admit.",
        "Dan Kennedy": "I’ll be blunt — most people get this part completely wrong.",
        "Joe Sugarman": "Let me tell you a quick story that changed everything.",
        "Eugene Schwartz": "The key isn’t desire — it’s understanding where that desire already lives.",
        "John Carlton": "Here’s the ugly little truth nobody else will say out loud.",
        "Jay Abraham": "If you’re serious about leverage, this next part matters.",
        "Robert Bly": "Let’s break this down like a classic direct-response pro.",
        "Neville Medhora": "Okay, here’s the simple version no one is telling you.",
        "Joanna Wiebe": "Let’s talk about what your customers are actually saying in their heads.",
        "Hybrid Mix": "Let’s mix hard-hitting direct response with what your market really cares about.",
    }.get(master_style, "Here’s the real story no one else is telling you.")

    # --- Sales Copy Body ---
    bullets = "\n".join([f"- {b}" for b in benefits_list])

    sales_copy = textwrap.dedent(
        f"""
        [{master_style}-inspired angle – {style_flavor}]

        ATTENTION

        {emotion_intro}

        If you're {audience_short}, you’ve probably tried to {base_benefit.lower()} before —
        but no matter what you’ve done, something always felt off. There’s a good chance
        the problem isn’t you... it’s the message you’ve been fed.

        Right now, your ideal prospects are scrolling past yet another promise that sounds
        exactly like every other one they’ve seen. Deep down, they’ve trained themselves
        not to believe those promises.

        INTEREST

        **{product_name}** is built to slice through that skepticism.

        {product_desc.strip()}

        It works because it speaks directly to what your market already obsesses over most.
        You’re not begging for attention — you’re joining the conversation in their head.

        In practice, that means you {awareness_angle}. Instead of sounding like everybody else,
        you become the only obvious choice.

        DESIRE

        Imagine this actually working for you:

        {bullets}

        Each line of copy becomes another little “yes” that stacks in their mind.
        They stop skimming and start picturing themselves living with the benefits
        you’re describing.

        ACTION

        If you're serious about {base_benefit.lower()} and ready to use copy that finally
        matches the real value you deliver, this is your move:

        👉 {cta.strip().rstrip('.')}

        {cta_phrase}
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
        "meet them where they are and lead them toward a confident buying decision",
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

        Remember: the real power here is that we {awareness_angle}.

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
# UI page helpers
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


# -------------------------
# Pages
# -------------------------

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
            then move to <strong>Email Sequences</strong>, the <strong>Classified Ad Writer</strong>,
            and <strong>A/B Split Tester</strong> to light up your cold traffic from every angle.
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
                <li>Use <strong>Traffic & Networks</strong> for offers and clicks.</li>
                <li>Use <strong>A/B Split Tester</strong> & <strong>Analytics</strong> to judge what wins.</li>
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
            "OpenAI / Gemini engines are not fully wired into engine selection yet. "
            "Using rule-based copy below, then optionally enhancing with OpenAI."
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

    # Heuristic conversion score for this draft
    st.markdown("---")
    st.markdown("### 🔍 Conversion Potential (Heuristic Score)")

    analysis = analyze_copy_score(sales_copy)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Overall Score", f"{analysis['total_score']} / 100")
        st.metric("Length & Depth", f"{analysis['length_score']:.1f}")
    with col_b:
        st.metric("Emotional Triggers", f"{analysis['emotion_score']:.1f}")
        st.metric("Structure (AIDA / PAS)", f"{analysis['structure_score']:.1f}")
    with col_c:
        st.metric("CTAs & Closers", f"{analysis['cta_score']:.1f}")
        st.metric("Specificity & Proof", f"{analysis['specificity_score']:.1f}")

    st.caption(
        "This is a heuristic score based on length, emotional words, structure cues, CTAs, and specificity. "
        "Always test in the real world — the market is the final judge."
    )

    # --- Optional AI enhancement ---
    st.markdown("---")
    st.markdown("### 🧠 Smart Rewrite (AI-Enhanced)")

    if st.button("✨ Enhance This Copy With OpenAI"):
        brief = f"""
        Niche: {niche}
        Master Style: {master_style}
        Awareness Level: {awareness}
        Desired Tone: {tone}
        Product: {product_name}
        Description: {product_desc}
        Audience: {audience}
        Benefits: {benefits_list}
        CTA: {cta}
        """

        prompt = f"""
        You are a world-class direct-response copywriter.

        1. Read the BRIEF carefully.
        2. Read the DRAFT COPY.
        3. Rewrite the copy to:
           - Keep the same big promise and offer
           - Stay in the style of: {master_style}
           - Improve clarity, emotional pull, and conversion potential
           - Keep it suitable for {niche} and awareness level: {awareness}

        BRIEF:
        {brief}

        DRAFT COPY:
        {sales_copy}

        Now output ONLY the improved copy. No explanation, no notes, just the final copy.
        """

        ok, result = call_llm_openai(prompt)
        if ok:
            st.success("AI-enhanced version generated below.")
            st.markdown("#### 🧠 AI-Enhanced Version")
            st.markdown(result)
        else:
            st.error(result)

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
        classified sites that generally have low or no special approval barriers.
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
        {
            "name": "20DollarBanners",
            "url": "https://www.20dollarbanners.com/",
            "note": "Affordable custom banner design service you can use for your display campaigns.",
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


def page_ab_split_tester():
    render_header()
    st.subheader("🧪 A/B Split Tester")

    st.markdown(
        """
        Use this to compare two variants of a headline, sales page, email, ad, or funnel.
        Enter impressions, clicks, and conversions to see CTR, CVR, EPC, ROI, and which variant is winning.
        """
    )

    test_type = st.selectbox(
        "Test Type",
        ["Headline", "Sales Page / VSL", "Email Subject", "Display Ad / Banner", "Classified Ad", "Other"],
        index=0,
    )

    with st.form("ab_test_form"):
        st.markdown("### Variant Details")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Variant A**")
            name_a = st.text_input("Name A", f"{test_type} A")
            copy_a = st.text_area("Copy / Notes A", "", key="copy_a")
            imp_a = st.number_input("Impressions A", min_value=0, step=1, value=0)
            clicks_a = st.number_input("Clicks A", min_value=0, step=1, value=0)
            conv_a = st.number_input("Conversions A", min_value=0, step=1, value=0)
            rev_a = st.number_input("Revenue A (optional)", min_value=0.0, step=1.0, value=0.0)

        with col_b:
            st.markdown("**Variant B**")
            name_b = st.text_input("Name B", f"{test_type} B")
            copy_b = st.text_area("Copy / Notes B", "", key="copy_b")
            imp_b = st.number_input("Impressions B", min_value=0, step=1, value=0)
            clicks_b = st.number_input("Clicks B", min_value=0, step=1, value=0)
            conv_b = st.number_input("Conversions B", min_value=0, step=1, value=0)
            rev_b = st.number_input("Revenue B (optional)", min_value=0.0, step=1.0, value=0.0)

        submitted = st.form_submit_button("📊 Calculate A/B Results")

    if not submitted:
        st.info("Fill in the numbers for A and B, then click **Calculate**.")
        return

    def calc_metrics(imp, clicks, conv, rev):
        ctr = (clicks / imp * 100) if imp > 0 else 0.0
        cvr = (conv / clicks * 100) if clicks > 0 else 0.0
        cr_total = (conv / imp * 100) if imp > 0 else 0.0
        epc = (rev / clicks) if clicks > 0 else 0.0
        roi = ((rev - imp) / imp * 100) if imp > 0 and rev > 0 else 0.0  # impressions ~ cost proxy
        return ctr, cvr, cr_total, epc, roi

    ctr_a, cvr_a, cr_a, epc_a, roi_a = calc_metrics(imp_a, clicks_a, conv_a, rev_a)
    ctr_b, cvr_b, cr_b, epc_b, roi_b = calc_metrics(imp_b, clicks_b, conv_b, rev_b)

    st.markdown("### Results")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {name_a}")
        st.write(f"Impressions: {imp_a}")
        st.write(f"Clicks: {clicks_a}")
        st.write(f"Conversions: {conv_a}")
        st.write(f"CTR: {ctr_a:.2f}%")
        st.write(f"Click-to-Conversion: {cvr_a:.2f}%")
        st.write(f"Impression-to-Conversion: {cr_a:.2f}%")
        st.write(f"EPC: ${epc_a:.2f}")
        st.write(f"ROI (rough): {roi_a:.2f}%")

    with col2:
        st.markdown(f"#### {name_b}")
        st.write(f"Impressions: {imp_b}")
        st.write(f"Clicks: {clicks_b}")
        st.write(f"Conversions: {conv_b}")
        st.write(f"CTR: {ctr_b:.2f}%")
        st.write(f"Click-to-Conversion: {cvr_b:.2f}%")
        st.write(f"Impression-to-Conversion: {cr_b:.2f}%")
        st.write(f"EPC: ${epc_b:.2f}")
        st.write(f"ROI (rough): {roi_b:.2f}%")

    # Determine winners
    winner_ctr = "A" if ctr_a > ctr_b else ("B" if ctr_b > ctr_a else "Tie")
    winner_cvr = "A" if cvr_a > cvr_b else ("B" if cvr_b > cvr_a else "Tie")
    winner_epc = "A" if epc_a > epc_b else ("B" if epc_b > epc_a else "Tie")

    st.markdown("---")
    st.markdown("### 🏆 Quick Verdict")

    verdict_lines = []
    verdict_lines.append(f"- Higher CTR: **Variant {winner_ctr}**" if winner_ctr != "Tie" else "- CTR: **Tie**")
    verdict_lines.append(f"- Better click-to-conversion rate: **Variant {winner_cvr}**" if winner_cvr != "Tie" else "- Click-to-conversion: **Tie**")
    verdict_lines.append(f"- Higher EPC: **Variant {winner_epc}**" if winner_epc != "Tie" else "- EPC: **Tie**")

    for line in verdict_lines:
        st.markdown(line)

    st.caption(
        "Rule of thumb: Use CTR to judge hooks/headlines, and EPC or overall conversion to judge offers and funnels."
    )


def page_analytics():
    render_header()
    st.subheader("📈 Analytics & Campaign Tracker")

    st.markdown(
        """
        Track key numbers for your campaigns (affiliate offers, solo ads, banners, classifieds)
        and see basic metrics like CPC, CPL, CPS, EPC, and ROI. Data is stored only in your session.
        """
    )

    if "analytics_history" not in st.session_state:
        st.session_state["analytics_history"] = []

    with st.form("analytics_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            campaign_name = st.text_input("Campaign Name", "Default Campaign")
            channel = st.selectbox(
                "Channel",
                ["Affiliate", "Solo Ads", "Banner / Display", "Classifieds", "Email", "Other"],
                index=0,
            )
        with col2:
            spend = st.number_input("Ad Spend / Cost ($)", min_value=0.0, step=1.0, value=0.0)
            clicks = st.number_input("Clicks", min_value=0, step=1, value=0)
        with col3:
            leads = st.number_input("Leads / Opt-ins", min_value=0, step=1, value=0)
            sales = st.number_input("Sales / Actions", min_value=0, step=1, value=0)

        revenue = st.number_input("Revenue / Payout ($)", min_value=0.0, step=1.0, value=0.0)

        submitted = st.form_submit_button("➕ Add / Update Campaign Snapshot")

    if submitted:
        # Calculate metrics
        cpc = (spend / clicks) if clicks > 0 else 0.0
        cpl = (spend / leads) if leads > 0 else 0.0
        cps = (spend / sales) if sales > 0 else 0.0
        epc = (revenue / clicks) if clicks > 0 else 0.0
        roi = ((revenue - spend) / spend * 100) if spend > 0 else 0.0

        snapshot = {
            "Campaign": campaign_name,
            "Channel": channel,
            "Spend": spend,
            "Clicks": clicks,
            "Leads": leads,
            "Sales": sales,
            "Revenue": revenue,
            "CPC": round(cpc, 4),
            "CPL": round(cpl, 4),
            "CPS": round(cps, 4),
            "EPC": round(epc, 4),
            "ROI%": round(roi, 2),
        }

        st.session_state["analytics_history"].append(snapshot)
        st.success("Snapshot added to your analytics history for this session.")

    if st.session_state["analytics_history"]:
        st.markdown("### 📊 Campaign History (This Session)")
        st.dataframe(st.session_state["analytics_history"])
    else:
        st.info("No campaign snapshots yet. Add one above to start tracking.")

    st.caption(
        "Use this tab to judge which traffic sources and offers are actually worth scaling."
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
        st.checkbox("Landing / Sales Page copy done")
        st.checkbox("Email sequence written & loaded into ESP")
        st.checkbox("Lead magnet created & hosted (MediaFire, etc.)")
    with col2:
        st.checkbox("Tracking links (affiliate IDs, UTMs) configured")
        st.checkbox("Retargeting pixels / tags installed")
        st.checkbox("Compliance checked (claims, images, affiliate rules)")

    st.markdown("### Traffic & Offers")

    col3, col4 = st.columns(2)
    with col3:
        st.checkbox("Core offer(s) selected from your affiliate networks")
        st.checkbox("At least 2–3 angles / hooks ready for testing")
    with col4:
        st.checkbox("Classified ads written for chosen sites")
        st.checkbox("Solo ad swipe ready for Udimi / TrafficForMe")

    st.markdown("### Mental Check")

    st.write(
        "- Do you have a clear daily traffic plan (how many clicks, from where)?\n"
        "- Do you know how you’ll follow up with leads for 7–30 days?\n"
        "- Do you have at least one backup offer if the first one underperforms?"
    )

    st.caption("Legend wisdom: money is made in preparation and follow-up, not in guessing.")


def page_copy_analyzer():
    render_header()
    st.subheader("🧮 Copy Analyzer & Variant Comparer")

    st.markdown(
        """
        Paste any copy (headline, email, sales page, VSL script, ad) and get a heuristic
        **Conversion Potential Score (1–100)** based on:
        - Length & depth
        - Emotional trigger words
        - AIDA / PAS structure cues
        - CTAs & closing drive
        - Specific numbers, time frames, and proof

        This is not a real predictive AI model — it’s a structured gut-check tool.
        Always validate with live traffic.
        """
    )

    mode = st.radio(
        "Mode",
        ["Single Copy Score", "Compare Two Variants (A/B)"],
        index=0,
    )

    if mode == "Single Copy Score":
        text = st.text_area(
            "Paste your copy here",
            "",
            height=260,
            placeholder="Paste your sales letter, email, ad, or headline + intro here...",
        )

        if st.button("🔍 Analyze Copy"):
            if not text.strip():
                st.error("Please paste some copy first.")
                return

            analysis = analyze_copy_score(text)
            st.markdown("### Results")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Overall Score", f"{analysis['total_score']} / 100")
                st.metric("Length & Depth", f"{analysis['length_score']:.1f}")
            with col_b:
                st.metric("Emotional Triggers", f"{analysis['emotion_score']:.1f}")
                st.metric("Structure (AIDA / PAS)", f"{analysis['structure_score']:.1f}")
            with col_c:
                st.metric("CTAs & Closers", f"{analysis['cta_score']:.1f}")
                st.metric("Specificity & Proof", f"{analysis['specificity_score']:.1f}")

            st.caption(
                "Use this to spot obvious weak spots. For example, low emotional triggers or no clear CTA usually means low response."
            )

            # Optional AI critique
            if st.checkbox("🧠 Get AI Critique (OpenAI)", value=False):
                prompt = f"""
                You are a world-class direct-response copywriter.

                Here is some copy. Give me a short critique focused on conversions:

                1. 3–5 bullet points of strengths.
                2. 3–5 bullet points of weaknesses.
                3. 3–5 specific changes I should test (headlines, leads, CTAs, proof, etc).

                Copy:
                {text}
                """

                ok, feedback = call_llm_openai(prompt)
                if ok:
                    st.markdown("#### AI Critique")
                    st.markdown(feedback)
                else:
                    st.error(feedback)

    else:
        col1, col2 = st.columns(2)
        with col1:
            text_a = st.text_area(
                "Variant A",
                "",
                height=240,
                placeholder="Paste Variant A copy here...",
            )
        with col2:
            text_b = st.text_area(
                "Variant B",
                "",
                height=240,
                placeholder="Paste Variant B copy here...",
            )

        if st.button("⚔️ Compare A vs B (Heuristic)"):
            if not text_a.strip() or not text_b.strip():
                st.error("Please paste copy for both Variant A and Variant B.")
                return

            analysis_a = analyze_copy_score(text_a)
            analysis_b = analyze_copy_score(text_b)

            st.markdown("### Variant Scores")

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Variant A")
                st.metric("Overall", f"{analysis_a['total_score']} / 100")
                st.write(f"Length & Depth: {analysis_a['length_score']:.1f}")
                st.write(f"Emotional Triggers: {analysis_a['emotion_score']:.1f}")
                st.write(f"Structure: {analysis_a['structure_score']:.1f}")
                st.write(f"CTAs: {analysis_a['cta_score']:.1f}")
                st.write(f"Specificity: {analysis_a['specificity_score']:.1f}")

            with col_b:
                st.markdown("#### Variant B")
                st.metric("Overall", f"{analysis_b['total_score']} / 100")
                st.write(f"Length & Depth: {analysis_b['length_score']:.1f}")
                st.write(f"Emotional Triggers: {analysis_b['emotion_score']:.1f}")
                st.write(f"Structure: {analysis_b['structure_score']:.1f}")
                st.write(f"CTAs: {analysis_b['cta_score']:.1f}")
                st.write(f"Specificity: {analysis_b['specificity_score']:.1f}")

            better = "A" if analysis_a["total_score"] > analysis_b["total_score"] else (
                "B" if analysis_b["total_score"] > analysis_a["total_score"] else "Tie"
            )

            st.markdown("---")
            if better == "Tie":
                st.markdown("### 🏁 Verdict: **Tie** (on heuristic score)")
            else:
                st.markdown(f"### 🏁 Verdict: **Variant {better}** looks stronger on paper")

            st.caption(
                "Use this with the A/B Split Tester: this tab helps you pre-qualify ideas; "
                "the Split Tester plus real clicks tells you who the real winner is."
            )


def page_settings_integrations():
    render_header()
    st.subheader("⚙️ Settings & Integrations")

    st.markdown(
        """
        This version of **Illuminati AI Copy Master** uses rule-based generation plus optional OpenAI enhancements.
        To enable OpenAI, add your key in Streamlit secrets.
        """
    )

    st.markdown("### 📬 SendPulse – Recommended ESP")
    st.markdown(
        """
        **SendPulse** is a multi-channel email marketing and automation platform with a generous free tier.

        - Create a free SendPulse account:  
          👉 [SendPulse Registration](https://sendpulse.com/register)
        - Once you have an account, you can:
            - Import the email sequences generated in this app  
            - Set up autoresponder flows  
            - Connect forms, chatbots, and landing pages to your funnels
        """
    )

    st.markdown("---")
    st.markdown("### 🤖 OpenAI API Setup (Optional)")

    st.markdown(
        """
        To use the Smart Rewrite and AI Critique features:

        1. Go to your Streamlit app dashboard.
        2. Open **Settings → Secrets**.
        3. Add a new entry:

        ```ini
        OPENAI_API_KEY = "sk-..."
        ```

        4. Save and reload the app.

        If the key is missing or invalid, the app will fall back gracefully and show a clear error message.
        """
    )

    st.markdown("---")
    st.markdown("### 🔗 Zapier Webhooks (for future automations)")

    st.markdown(
        """
        In Zapier, create a Zap with **Webhooks by Zapier** → **Catch Hook** to get a unique URL.  
        Paste that URL below and you can send simple JSON payloads from this app (for example, when you finalize a winning variant).
        """
    )

    zap_url = st.text_input(
        "Zapier Catch Hook URL",
        st.session_state.get("zapier_url", ""),
        help="Example: https://hooks.zapier.com/hooks/catch/123456/abcde",
    )
    st.session_state["zapier_url"] = zap_url

    test_payload = {
        "event": "test_ping",
        "source": "Illuminati AI Copy Master",
        "note": "You can customize this payload in the code for real events.",
    }

    if st.button("🚀 Send Test Webhook"):
        if not zap_url:
            st.error("Please paste your Zapier Catch Hook URL first.")
        else:
            ok, msg = send_zapier_webhook(zap_url, test_payload)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    st.caption(
        "Treat your Zapier URL like a password. Don’t expose it publicly. "
        "Once it’s set, you can extend this code to send real campaign events."
    )


# -------------------------
# Main navigation
# -------------------------

def main():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-logo">
                🔺 Illuminati AI
            </div>
            """,
            unsafe_allow_html=True,
        )
        page = st.radio(
            "Navigate",
            [
                "Dashboard",
                "Generate Copy",
                "Email Sequences",
                "Classified Ad Writer",
                "Manual & Lead Magnet",
                "Traffic & Networks",
                "A/B Split Tester",
                "Analytics",
                "System Checklist",
                "Copy Analyzer",
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
    elif page == "A/B Split Tester":
        page_ab_split_tester()
    elif page == "Analytics":
        page_analytics()
    elif page == "System Checklist":
        page_system_checklist()
    elif page == "Copy Analyzer":
        page_copy_analyzer()
    elif page == "Settings & Integrations":
        page_settings_integrations()

    # Global footer
    st.markdown(
        """
        <div class="illuminati-footer">
            © 2025 <strong>DeAndre Jefferson</strong><br/>
            Strategic Copy, AI, and Influence Engineering.<br/>
            Built with Python + Streamlit + OpenAI + Gemini APIs.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

