import streamlit as st
import textwrap
import re
from typing import List, Tuple, Dict

# Optional HTTP for Zapier test hook
try:
    import requests  # type: ignore
except ImportError:
    requests = None

# Optional AI SDKs (all fail gracefully if not installed or keys missing)
try:
    import openai  # type: ignore
except ImportError:
    openai = None

try:
    import anthropic  # type: ignore
except ImportError:
    anthropic = None

try:
    from groq import Groq  # type: ignore
except ImportError:
    Groq = None

try:
    import cohere  # type: ignore
except ImportError:
    cohere = None


# =========================
# Page config & base styles
# =========================

st.set_page_config(
    page_title="Illuminati AI Copy Master",
    page_icon="🔺",
    layout="wide",
)

APP_CSS = """
<style>
/* Global */
body, .stApp {
    background-color: #050506;
    color: #f2f2f2;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.block-container { padding-top: 1.5rem; }

/* Illuminati header */
.illuminati-header { text-align:center; padding: 1rem 0 0.5rem 0; }
.illuminati-title {
    font-size: 2.1rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase;
    color: #f5d76e;
    text-shadow: 0 0 14px rgba(245,215,110,.95), 0 0 26px rgba(155,17,30,.80);
}
.illuminati-subtitle { font-size: .95rem; color:#f7f7f7; opacity:.85; }
.illuminati-pyramid {
    font-size: 2.5rem; margin-bottom: .25rem;
    text-shadow: 0 0 14px rgba(245,215,110,.95), 0 0 26px rgba(155,17,30,.75);
}
/* Sidebar brand */
.sidebar-logo {
    text-align:center; font-size:1.1rem; font-weight:700; margin:.5rem 0 1.2rem 0; color:#f5d76e;
    text-shadow: 0 0 12px rgba(245,215,110,.9), 0 0 24px rgba(155,17,30,.7);
}

/* Cards */
.illuminati-card {
    border-radius: 12px; border:1px solid rgba(245,215,110,.18);
    padding: 1rem 1.2rem; margin-bottom: .75rem;
    background: radial-gradient(circle at top, #111113 0, #050506 55%, #000 100%);
    box-shadow: 0 0 0 1px rgba(255,0,0,.05), 0 0 22px rgba(245,215,110,.12);
}

.illuminati-accent { color:#f5d76e; font-weight:600; }

/* War-room red class */
.war-room-red { color:#ff2d2d; font-weight:800; text-shadow: 0 0 10px rgba(255,45,45,.6); }

/* Buttons */
div.stButton > button {
    border-radius: 999px; border: 1px solid #f5d76e;
    background: linear-gradient(135deg, #9b111e, #5c020b);
    color:#fff; font-weight:600; box-shadow: 0 0 12px rgba(155,17,30,.7);
}
div.stButton > button:hover {
    border-color:#fff; box-shadow: 0 0 18px rgba(245,215,110,.85);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: radial-gradient(circle at top, #1b0a0f 0, #050506 55%, #000 100%);
}
section[data-testid="stSidebar"] * { color:#f5f5f5 !important; }

/* Footer */
.illuminati-footer {
    text-align:center; font-size:.8rem; color:#aaa; margin-top:2.5rem; padding-top:.75rem;
    border-top:1px solid rgba(245,215,110,.18); opacity:.9;
}

/* Login card */
.login-card {
    max-width: 480px; margin: 0 auto; padding: 1.2rem 1.4rem;
    border:1px solid rgba(245,215,110,.2); border-radius:12px;
    background: radial-gradient(circle at top, #111113 0, #050506 55%, #000 100%);
    box-shadow: 0 0 22px rgba(245,215,110,.12);
}
.login-title { text-align:center; font-weight:700; color:#f5d76e; margin-bottom: .5rem; }
/* Sidebar video glow */
section[data-testid="stSidebar"] [data-testid="stVideo"] {
    padding: 4px;
    border-radius: 14px;
    background: radial-gradient(circle at top, #1b0a0f 0, #050506 55%, #000 100%);
    box-shadow:
        0 0 10px rgba(245,215,110,0.5),
        0 0 18px rgba(155,17,30,0.8);
    border: 1px solid rgba(245,215,110,0.4);
    margin-top: 0.5rem;
}
/* Sidebar Illuminati glowing pulse for video */
section[data-testid="stSidebar"] [data-testid="stVideo"] {
    padding: 5px;
    border-radius: 16px;
    background: radial-gradient(circle at top, #1a0004 0%, #0a0000 55%, #000 100%);
    border: 1px solid rgba(245,215,110,0.5);
    box-shadow:
        0 0 12px rgba(245,215,110,0.8),
        0 0 20px rgba(155,17,30,0.7),
        inset 0 0 10px rgba(245,215,110,0.4);
    animation: pulse-glow 4s ease-in-out infinite alternate;
}

/* Pulse keyframes for Illuminati glow */
@keyframes pulse-glow {
    0% {
        box-shadow:
            0 0 10px rgba(245,215,110,0.4),
            0 0 15px rgba(155,17,30,0.3),
            inset 0 0 8px rgba(245,215,110,0.3);
    }
    100% {
        box-shadow:
            0 0 20px rgba(245,215,110,1),
            0 0 30px rgba(155,17,30,1),
            inset 0 0 12px rgba(245,215,110,0.8);
    }
}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)


# =========================
# Copywriting knowledge
# =========================

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

NICHE_DEFAULTS: Dict[str, Dict[str, List[str]]] = {
    "Natural / Alternative Healing": {
        "audience": ["a busy parent who wants natural ways to feel better without pills"],
        "benefits": [
            "cost-effective health independence (saves hundreds on pharmacy bills)",
            "relieve nagging symptoms without harsh drugs",
            "support your body’s natural healing process",
            "follow a simple daily routine you can actually stick to",
        ],
    },
    "Spirituality & Alternative Beliefs": {
        "audience": ["a seeker who feels there’s more to life than bills, stress, and endless scrolling"],
        "benefits": [
            "feel calm and centered, even when life is chaotic",
            "develop a deeper sense of purpose and direction",
            "connect with like-minded people who actually get you",
        ],
    },
    "Specific Health Problems": {
        "audience": ["someone who’s tired of treating symptoms while the real cause never gets solved"],
        "benefits": [
            "finally understand what’s really driving your symptoms",
            "use step-by-step actions instead of random guessing",
            "feel a real difference in your energy and mood",
        ],
    },
    "Vanity Niches": {
        "audience": ["someone who wants to look in the mirror and actually like what they see"],
        "benefits": [
            "turn quiet insecurity into visible confidence",
            "stand out in photos instead of hiding from the camera",
            "get noticed without having to shout for attention",
        ],
    },
    "Relationships": {
        "audience": ["someone who’s tired of feeling invisible, unwanted, or misunderstood in love"],
        "benefits": [
            "feel desired and chosen instead of ignored",
            "stop repeating the same painful relationship patterns",
            "create the kind of connection other people envy",
        ],
    },
    "Money & Business": {
        "audience": ["an ambitious action-taker who’s sick of watching other people make the money they want"],
        "benefits": [
            "turn scattered effort into focused income-producing action",
            "build assets instead of just trading time for money",
            "finally follow a plan that has a real shot at working",
        ],
    },
    "General Interest & Survival": {
        "audience": ["someone who wants to be prepared when things go wrong instead of hoping for the best"],
        "benefits": [
            "protect your family when systems fail",
            "have what you need when other people are scrambling",
            "sleep better knowing you’re not at the mercy of chaos",
        ],
    },
}


# =========================
# Auth helpers
# =========================

def is_authenticated() -> bool:
    return bool(st.session_state.get("auth_ok", False))

def require_secrets() -> Tuple[str, str]:
    user = st.secrets.get("ADMIN_USERNAME", "")
    pw = st.secrets.get("ADMIN_PASSWORD", "")
    return user, pw

def login_page():
    # Header logo
    st.markdown(
        """
        <div class="illuminati-header">
            <div class="illuminati-pyramid">🔺</div>
            <div class="illuminati-title">ILLUMINATI AI COPY MASTER</div>
            <div class="illuminati-subtitle">Admin Access Only</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔒 Admin Login</div>', unsafe_allow_html=True)

    username = st.text_input("Admin Name", placeholder="DeAndre Jefferson")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        admin_user, admin_pw = require_secrets()
        if not admin_user or not admin_pw:
            st.error("Admin credentials are not set. Add ADMIN_USERNAME and ADMIN_PASSWORD in Streamlit secrets.")
        elif username == admin_user and password == admin_pw:
            st.session_state["auth_ok"] = True
            st.success("Access granted. Loading your war room…")
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="illuminati-footer">
            © 2025 <strong>DeAndre Jefferson</strong><br/>
            Strategic Copy, AI, and Influence Engineering.<br/>
            Built with Python + Streamlit + OpenAI + Gemini + Claude (Anthropic).
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# Utility & scoring helpers
# =========================

def normalize_audience(audience: str) -> str:
    if not isinstance(audience, str) or not audience.strip():
        return "someone who needs what you offer"
    raw = audience.splitlines()[0].strip()
    low = raw.lower()
    if low.startswith(("a ", "an ", "the ")):
        return raw
    if " who " in low or " and " in low:
        return f"someone like {raw}"
    if re.match(r"^\\d", raw):
        return f"someone aged {raw}"
    return f"someone who is {raw}"

def choose_niche_defaults(niche: str) -> Tuple[str, List[str]]:
    data = NICHE_DEFAULTS.get(niche)
    if not data:
        return (
            "someone who needs what you offer",
            ["get results without overwhelm", "follow a simple plan", "feel confident doing it right"],
        )
    return data["audience"][0], data["benefits"]

def send_zapier_webhook(url: str, payload: Dict) -> Tuple[bool, str]:
    if not url:
        return False, "No Zapier URL provided."
    if requests is None:
        return False, "The 'requests' library is not available."
    try:
        resp = requests.post(url, json=payload, timeout=10)
        return True, f"Webhook sent. HTTP {resp.status_code}"
    except Exception as e:
        return False, f"Error sending webhook: {e}"

EMOTIONAL_TRIGGERS = [
    "secret","secrets","discover","finally","weird","shocking","hidden","proven","guaranteed","guarantee",
    "instantly","suddenly","fear","greed","curiosity","strange","little-known","breakthrough","odd",
    "easy","fast","quick","now","today","limited","scarcity","deadline","risk-free","no risk","exclusive",
]
CTA_PHRASES = [
    "click here","tap here","join now","buy now","order now","get started","sign up","enroll now",
    "start now","act now","claim your","grab your",
]
STRUCTURE_MARKERS = [
    "attention","interest","desire","action","problem","agitate","solution","guarantee","testimonial",
    "proof","bonus","faq",
]

def analyze_copy_score(copy_text: str) -> Dict[str, float]:
    if not copy_text or not copy_text.strip():
        return {k:0.0 for k in ["total_score","length_score","emotion_score","structure_score","cta_score","specificity_score"]}

    text = copy_text.strip()
    words = re.findall(r"\\w+", text)
    n_words = len(words)

    if n_words < 80: length_score = 20.0
    elif n_words < 200: length_score = 20 + (n_words - 80) / 120 * 40
    elif n_words <= 1500: length_score = 60 + min((n_words - 200) / 1300 * 30, 30)
    else:
        over = min((n_words - 1500) / 1500, 1.0)
        length_score = 90 - 30 * over

    low = text.lower()
    emo_hits = sum(1 for t in EMOTIONAL_TRIGGERS if t in low)
    emo_score = min(emo_hits / 15.0, 1.0) * 100
    struct_hits = sum(1 for m in STRUCTURE_MARKERS if m in low)
    struct_score = min(struct_hits / 8.0, 1.0) * 100
    cta_hits = sum(1 for p in CTA_PHRASES if p in low)
    if "http://" in low or "https://" in low: cta_hits += 1
    cta_score = min(cta_hits / 4.0, 1.0) * 100

    digits = len(re.findall(r"\\d", text))
    percents = len(re.findall(r"\\d+%", text))
    dollars = len(re.findall(r"\\$", text))
    timeframes = len(re.findall(r"\\bday\\b|\\bdays\\b|\\bweek\\b|\\bweeks\\b|\\bmonth\\b|\\bmonths\\b", low))
    spec_raw = digits + percents + dollars + timeframes
    spec_score = min(spec_raw / 15.0, 1.0) * 100

    total = length_score*0.20 + emo_score*0.25 + struct_score*0.20 + cta_score*0.15 + spec_score*0.20
    total_score = max(1.0, min(100.0, total))
    return {
        "total_score": round(total_score,1),
        "length_score": round(length_score,1),
        "emotion_score": round(emo_score,1),
        "structure_score": round(struct_score,1),
        "cta_score": round(cta_score,1),
        "specificity_score": round(spec_score,1),
    }


# =========================
# AI calls (OpenAI / Claude / Groq / Cohere)
# =========================

def call_llm_openai(prompt: str, model: str = "gpt-4o-mini") -> Tuple[bool, str]:
    if openai is None:
        return False, "OpenAI SDK not installed."
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        return False, "Missing OPENAI_API_KEY in secrets."
    try:
        openai.api_key = api_key
        resp = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a world-class direct-response copywriter."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return True, resp.choices[0].message.content.strip()
    except Exception as e:
        return False, f"OpenAI error: {e}"

def call_llm_claude(prompt: str, model: str = "claude-3-5-sonnet-latest") -> Tuple[bool, str]:
    if anthropic is None:
        return False, "Anthropic SDK not installed."
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return False, "Missing ANTHROPIC_API_KEY in secrets."
    try:
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=1400,
            temperature=0.7,
            system="You are a world-class direct-response copywriter who writes in master styles.",
            messages=[{"role": "user", "content": prompt}],
        )
        return True, "".join([b.text for b in resp.content if hasattr(b, "text")])
    except Exception as e:
        return False, f"Claude error: {e}"

def call_llm_groq(prompt: str, model: str = "llama-3.1-8b-instant") -> Tuple[bool, str]:
    if Groq is None:
        return False, "Groq SDK not installed."
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        return False, "Missing GROQ_API_KEY in secrets."
    try:
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a world-class direct-response copywriter."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return True, resp.choices[0].message.content.strip()
    except Exception as e:
        return False, f"Groq error: {e}"

def call_llm_cohere(prompt: str, model: str = "command-r") -> Tuple[bool, str]:
    if cohere is None:
        return False, "Cohere SDK not installed."
    api_key = st.secrets.get("COHERE_API_KEY", "")
    if not api_key:
        return False, "Missing COHERE_API_KEY in secrets."
    try:
        client = cohere.Client(api_key)
        resp = client.chat(model=model, message=prompt, temperature=0.7)
        text = getattr(resp, "text", None) or getattr(getattr(resp, "response", None), "text", "")
        return True, (text or "").strip()
    except Exception as e:
        return False, f"Cohere error: {e}"


# =========================
# Generators (rule-based)
# =========================

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
    if not audience.strip():
        niche_aud, _ = choose_niche_defaults(niche)
        audience = niche_aud
    if not benefits_list:
        _, niche_benefits = choose_niche_defaults(niche)
        benefits_list = niche_benefits

    raw_base = benefits_list[0].strip()
    base_benefit_short = raw_base
    base_benefit_detail = ""
    if "(" in raw_base and ")" in raw_base:
        before = raw_base.split("(", 1)[0].strip()
        inside = raw_base.split("(", 1)[1].split(")", 1)[0].strip()
        if before: base_benefit_short = before
        base_benefit_detail = inside

    audience_short = normalize_audience(audience)
    style_flavor = MASTER_FLAVORS.get(master_style, "direct-response style tuned for conversions")
    awareness_angle = AWARENESS_ANGLE.get(awareness, "meet them where they are and lead them step-by-step to a decision")
    first_aud_line = audience.splitlines()[0].strip() if audience else "your market"
    if re.match(r"^\\d", first_aud_line):
        first_aud_line = f"people aged {first_aud_line}"

    headlines: List[str] = []
    benefit_for_headline = base_benefit_short.capitalize()
    headlines.append(f"Finally: {product_name} That Helps You {benefit_for_headline} Without The Struggle")
    headlines.append(f"How {first_aud_line.capitalize()} Can {benefit_for_headline} with {product_name}")
    headlines.append(f'{product_name}: The "{benefit_for_headline}" Shortcut You Can Start Using Today')
    headlines.append(f"Do You Make These Mistakes When Trying to {benefit_for_headline}?")
    headlines.append(f"The Hidden Shortcut to {benefit_for_headline} No One Told You About")
    if len(benefits_list) > 1:
        second = benefits_list[1].strip()
        headlines.append(f'Turn "{second}" Into Your Edge With {product_name}')

    cta_map = {
        "Natural / Alternative Healing": "Because your body was never designed to be at war with itself.",
        "Spirituality & Alternative Beliefs": "Because your soul has been asking for more — this is you answering.",
        "Specific Health Problems": "Your future self will thank you for not ignoring this moment.",
        "Vanity Niches": "The mirror doesn’t have to be your enemy anymore.",
        "Relationships": "Love rarely fixes itself — it responds when you do.",
        "Money & Business": "Your bank account will remember the choices you make today.",
        "General Interest & Survival": "You don’t rise to the occasion; you fall to your level of preparation.",
    }
    cta_phrase = cta_map.get(niche, "Take action now while you’re still thinking about it.")

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

    bullets = "\\n".join([f"- {b}" for b in benefits_list])
    detail_sentence = f" In plain English: it {base_benefit_detail}." if base_benefit_detail else ""

    sales_copy = textwrap.dedent(
        f"""
        [{master_style}-inspired angle – {style_flavor}]

        ATTENTION

        {emotion_intro}

        If you're {audience_short}, you’ve probably tried to {base_benefit_short.lower()} before —
        but no matter what you’ve done, something always felt off. There’s a good chance
        the problem isn’t you... it’s the promises you’ve been sold.

        Right now, your ideal prospects are scrolling past yet another “too good to be true”
        claim that sounds exactly like every other one they’ve seen. Deep down, they’ve
        trained themselves not to believe those promises.

        INTEREST

        **{product_name}** is built to slice through that skepticism.

        {product_desc.strip()}{detail_sentence}

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

        If you're serious about {base_benefit_short.lower()} and ready to use copy that finally
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
    if not benefits_list:
        benefits_list = [
            "get real, measurable results",
            "stop wasting time on things that don’t move the needle",
            "follow a proven plan instead of guessing",
        ]
    awareness_angle = AWARENESS_ANGLE.get(
        awareness, "meet them where they are and lead them toward a confident buying decision"
    )
    main_benefit = benefits_list[0]
    seq: List[Dict[str, str]] = []

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
    seq.append({"subject": subject1, "body": body1})

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
    seq.append({"subject": subject2, "body": body2})

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
    seq.append({"subject": subject3, "body": body3})

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
    seq.append({"subject": subject4, "body": body4})

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
    seq.append({"subject": subject5, "body": body5})
    return seq[:num_emails]


def generate_classified_ads(
    product_name: str,
    product_desc: str,
    audience: str,
    niche: str,
    master_style: str,
    cta: str,
    num_ads: int = 3,
) -> List[str]:
    if not audience.strip():
        audience, _ = choose_niche_defaults(niche)
    aud_short = normalize_audience(audience)
    desc_short = product_desc.strip()
    if len(desc_short) > 220:
        desc_short = desc_short[:217].rstrip() + "..."
    out: List[str] = []

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
        out.append(body)
    return out


def generate_vsl_webinar_script(
    product_name: str,
    product_desc: str,
    audience: str,
    benefits_list: List[str],
    master_style: str,
    awareness: str,
    niche: str,
    script_type: str,
) -> str:
    if not audience.strip():
        audience, _ = choose_niche_defaults(niche)
    aud_short = normalize_audience(audience)
    if not benefits_list:
        _, niche_b = choose_niche_defaults(niche)
        benefits_list = niche_b
    main_benefit = benefits_list[0]
    extra_bullets = "\\n".join([f"- {b}" for b in benefits_list])
    style_flavor = MASTER_FLAVORS.get(master_style, "direct-response style tuned for conversions")
    awareness_angle = AWARENESS_ANGLE.get(awareness, "meet them where they are and lead them step-by-step to a decision")

    if master_style == "Gary Halbert":
        hook_line = "Let me start with a simple, slightly uncomfortable truth."
    elif master_style == "David Ogilvy":
        hook_line = "If you care about results, the next few minutes deserve your full attention."
    elif master_style == "Dan Kennedy":
        hook_line = "I’m not here to entertain you. I’m here to show you how to make more money."
    elif master_style == "Joe Sugarman":
        hook_line = "This story starts with something small, almost trivial… and turns into a complete turning point."
    elif master_style == "Eugene Schwartz":
        hook_line = "Right now, there is a powerful desire already burning in your market."
    elif master_style == "John Carlton":
        hook_line = "Here’s the ugly truth no one else will say out loud."
    else:
        hook_line = "Let’s cut through the noise and talk about what actually matters."

    secrets_block = "\\n".join([f"Secret #{i+1}: {b}" for i, b in enumerate(benefits_list[:3])])

    if script_type == "VSL Script":
        script = textwrap.dedent(
            f"""
            [VSL SCRIPT – {master_style} style – {niche} – {awareness} awareness]

            SECTION 1 – COLD OPEN HOOK

            {hook_line}
            If you're {aud_short}, and you want to {main_benefit.lower()}, but you’re sick of
            hype and half-truths, you’re in exactly the right place.

            In the next few minutes, I’m going to show you a way to {main_benefit.lower()}
            that {awareness_angle}.

            SECTION 2 – BIG PROMISE & WHAT THEY’LL GET

            Imagine being able to:
            {extra_bullets}

            That’s what **{product_name}** was built to do.

            By the end of this short video, you’ll know:
            - What’s really been blocking you from {main_benefit.lower()}
            - The new mechanism behind {product_name}
            - Exactly how to get started if it’s right for you

            SECTION 3 – CREDIBILITY / WHY LISTEN TO ME

            Over the years, we’ve worked with {niche.lower()} offers and {aud_short} just like you,
            testing what actually moves the needle and what’s just noise.

            {product_desc.strip()}

            SECTION 4 – PROBLEM / AGITATION (PAS)

            The real problem isn’t that you’re lazy, undisciplined, or broken.
            It’s that most {niche.lower()} offers:
            - Over-promise results that almost nobody gets
            - Hide the work involved
            - Use the wrong mechanism for someone like you

            SECTION 5 – THE NEW MECHANISM

            Here’s where **{product_name}** is different:
            - What you actually do day to day
            - Why it works for {aud_short}
            - How it builds momentum instead of draining you

            SECTION 6 – PROOF / VISUALIZATION

            Picture this in your own life:
            {extra_bullets}

            SECTION 7 – THE OFFER

            When you say “yes” to **{product_name}**, you get:
            - Clear, step-by-step guidance for {aud_short}
            - Tools/templates focused on {main_benefit.lower()}
            - A path that respects your time and energy

            SECTION 8 – STACK & VALUE

            If all this did was help you {main_benefit.lower()}, would it be worth it?
            What if it also helped you:
            {extra_bullets}

            SECTION 9 – URGENCY & CTA

            1) Click the main button near this video
            2) Pick your option
            3) Start inside **{product_name}** and follow through this time
            """
        ).strip()
    else:
        script = textwrap.dedent(
            f"""
            [WEBINAR SCRIPT – {master_style} style – {niche} – {awareness} awareness]

            WELCOME & PROMISE

            Today we’re going to talk about how {aud_short} can finally {main_benefit.lower()}
            without the usual stress, confusion, or burnout.

            INTRO & AGENDA

            - Why most attempts to {main_benefit.lower()} fall apart
            - The new mechanism behind **{product_name}**
            - How to apply this immediately

            YOUR STORY / AUTHORITY (brief, relevant)
            Tie your story back to {aud_short} so they see themselves in it.

            THE 3 SECRETS (CONTENT)
            {secrets_block}

            TRANSITION TO OFFER
            If you want help implementing this, that’s exactly what **{product_name}** was built for.

            THE OFFER
            {extra_bullets}

            VALUE STACK, GUARANTEE, BONUSES
            - Core program value
            - Bonus #1
            - Bonus #2
            - Guarantee / reassurance

            CLOSE & CTA
            Click the button near this webinar window and choose your best option.
            """
        ).strip()
    return script


# =========================
# UI helpers
# =========================

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


# =========================
# Pages
# =========================

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
            This dashboard is your <span class="war-room-red">war room</span> for direct-response campaigns in:
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
            <strong>VSL & Webinar Scripts</strong> and the <strong>A/B Split Tester</strong>
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
                <li>Turn that into an email sequence, VSL script, and classifieds.</li>
                <li>Use <strong>Traffic & Networks</strong> + <strong>Classified Sites</strong> for offers and clicks.</li>
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
        "Use this page to create master-inspired headlines and long-form sales copy tuned to your niche and audience."
    )

    engine_choice = st.selectbox(
        "Engine Mode",
        ["Rule-based (local templates)"],
        index=0,
    )

    col_top1, col_top2, col_top3 = st.columns(3)
    with col_top1:
        niche = st.selectbox("Primary Niche", list(NICHE_DEFAULTS.keys()), index=0)
    with col_top2:
        master_style = st.selectbox("Master Style Influence", list(MASTER_FLAVORS.keys()), index=0)
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
        product_desc = st.text_area("Product / Service Description", "")
        audience = st.text_area("Target Audience", "")
        tone = st.selectbox(
            "Desired Tone",
            ["Direct & No-BS", "Friendly & Conversational", "High-End / Premium", "Urgent & Hypey", "Calm & Professional"],
            index=0,
        )
        benefits_text = st.text_area("Key Benefits & USPs (one per line)", "")
        cta = st.text_input("Primary Call To Action (CTA)", "Click here to get started")
        submitted = st.form_submit_button("⚡ Generate Headlines & Sales Copy")

    if not submitted:
        st.info("Fill in the brief above and hit **Generate** to see copy.")
        return
    if not product_name or not product_desc:
        st.error("Please provide at least a product name and description.")
        return

    benefits_list = [ln.strip() for ln in benefits_text.splitlines() if ln.strip()]
    headlines, sales_copy = generate_rule_based_copy(
        product_name, product_desc, audience, tone, benefits_list, cta, awareness, master_style, niche
    )

    st.markdown("### 🎯 Headline Variations")
    for i, h in enumerate(headlines, start=1):
        st.markdown(f"**{i}. {h}**")

    st.markdown("### 📜 Sales Copy Draft")
    st.markdown(sales_copy)

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

    st.markdown("---")
    st.markdown("### 🧠 Smart Rewrite (AI-Enhanced)")

    provider = st.selectbox(
        "Enhance with",
        ["OpenAI", "Claude (Anthropic)", "Groq (Llama)", "Cohere"],
        index=1,
        help="Select a model provider to rewrite and strengthen your copy.",
    )

    if st.button("✨ Enhance This Copy"):
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
""".strip()

        prompt = f"""
You are a world-class direct-response copywriter.

You will be given a brief and a sales page draft.

<BRIEF>
{brief}
</BRIEF>

<DRAFT>
{sales_copy}
</DRAFT>

Rewrite ONLY the draft to be clearer, more emotionally compelling, more specific (numbers, proof),
and stronger in direct response persuasion (AIDA, PAS, strong CTAs). Maintain the style influence of {master_style},
the niche {niche}, and the awareness level {awareness}. Do NOT include the brief or any commentary—return the improved copy only.
""".strip()

        if provider == "OpenAI":
            ok, result = call_llm_openai(prompt)
        elif provider == "Claude (Anthropic)":
            ok, result = call_llm_claude(prompt)
        elif provider == "Groq (Llama)":
            ok, result = call_llm_groq(prompt)
        else:
            ok, result = call_llm_cohere(prompt)

        if ok and result:
            st.success(f"{provider} enhancement complete.")
            st.markdown("#### 🧠 AI-Enhanced Version")
            st.markdown(result)
        else:
            st.error(result or "Enhancement failed.")


def page_email_sequences():
    render_header()
    st.subheader("📧 Email Sequences")
    st.markdown("Turn your core sales message into a multi-email sequence designed to warm up cold leads.")

    with st.form("email_seq_form"):
        product_name = st.text_input("Product / Service Name", "")
        product_desc = st.text_area("Product / Service Description", "")
        audience = st.text_area("Audience (copy from Generate Copy if you like)", "")
        benefits_text = st.text_area("Key Benefits (one per line)", "")
        master_style = st.selectbox("Master Style Influence", list(MASTER_FLAVORS.keys()), index=0)
        awareness = st.selectbox("Audience Awareness Level", ["Unaware","Problem-aware","Solution-aware","Product-aware","Most-aware"], index=2)
        num_emails = st.slider("Number of emails", 3, 10, 5)
        submitted = st.form_submit_button("📨 Generate Email Sequence")

    if not submitted:
        st.info("Fill in the fields and click **Generate Email Sequence**.")
        return
    if not product_name or not product_desc:
        st.error("Please enter at least a product name and description.")
        return

    benefits_list = [ln.strip() for ln in benefits_text.splitlines() if ln.strip()]
    seq = generate_email_sequence(product_name, product_desc, audience, benefits_list, master_style, awareness, num_emails)
    st.markdown("### ✉️ Generated Emails")
    for idx, email in enumerate(seq, start=1):
        with st.expander(f"Email {idx}: {email['subject']}"):
            st.markdown(f"**Subject:** {email['subject']}")
            st.text(email["body"])


def page_vsl_webinar():
    render_header()
    st.subheader("🎥 VSL & Webinar Scripts")
    st.markdown("Generate long-form VSL or webinar scripts inspired by the masters.")

    col1, col2, col3 = st.columns(3)
    with col1:
        script_type = st.selectbox("Script Type", ["VSL Script", "Webinar Script"], index=0)
    with col2:
        niche = st.selectbox("Primary Niche", list(NICHE_DEFAULTS.keys()), index=0)
    with col3:
        master_style = st.selectbox("Master Style Influence", list(MASTER_FLAVORS.keys()), index=0)

    st.markdown("---")
    with st.form("vsl_webinar_form"):
        product_name = st.text_input("Product / Offer Name", "")
        product_desc = st.text_area("Product / Offer Description", "")
        audience = st.text_area("Target Audience", "")
        benefits_text = st.text_area("Core Benefits (one per line)", "")
        awareness = st.selectbox("Audience Awareness Level", ["Unaware","Problem-aware","Solution-aware","Product-aware","Most-aware"], index=2)
        submitted = st.form_submit_button("🎬 Generate Script")

    if not submitted:
        st.info("Fill out the fields and click **Generate Script**.")
        return
    if not product_name or not product_desc:
        st.error("Please add at least a product name and description.")
        return

    benefits_list = [ln.strip() for ln in benefits_text.splitlines() if ln.strip()]
    script = generate_vsl_webinar_script(product_name, product_desc, audience, benefits_list, master_style, awareness, niche, script_type)
    st.markdown("### 📜 Script Draft")
    st.text(script)


def page_classified_writer():
    render_header()
    st.subheader("📢 Classified Ad Writer")
    st.markdown("Create punchy classified ads tuned to your niche and master’s style.")

    col_top1, col_top2 = st.columns(2)
    with col_top1:
        niche = st.selectbox("Niche / Category", list(NICHE_DEFAULTS.keys()), index=0)
    with col_top2:
        master_style = st.selectbox("Master Style Influence", list(MASTER_FLAVORS.keys()), index=0)

    with st.form("classified_form"):
        product_name = st.text_input("Product / Offer Name", "")
        product_desc = st.text_area("Short Product Description", "")
        audience = st.text_area("Audience (optional)", "")
        cta = st.text_input("Call to Action", "Click here to learn more")
        num_ads = st.slider("Number of variations", 1, 10, 3)
        submitted = st.form_submit_button("📝 Generate Classified Ads")

    if not submitted:
        st.info("Fill in the fields and click **Generate Classified Ads**.")
        return
    if not product_name or not product_desc:
        st.error("You need at least a product name and description.")
        return

    ads = generate_classified_ads(product_name, product_desc, audience, niche, master_style, cta, num_ads)
    st.markdown("### 🧾 Classified Ad Variations")
    for i, ad in enumerate(ads, start=1):
        with st.expander(f"Classified Ad {i}"):
            st.text(ad)


def page_manual_assets():
    render_header()
    st.subheader("📚 Manual & Lead Magnet Ideas")
    st.markdown("Generate outlines for checklists, cheat sheets, and short PDFs that plug into your funnel.")

    st.markdown("### Lead Magnet Framing")
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Core Offer Name", "")
        niche = st.selectbox("Niche", list(NICHE_DEFAULTS.keys()), index=0)
    with col2:
        lead_magnet_type = st.selectbox("Lead Magnet Type", ["Checklist","Cheat Sheet","Short PDF Guide (5–10 pages)","Email Mini-Course"], index=0)

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


def page_traffic_networks():
    render_header()
    st.subheader("🚦 Traffic & Networks")
    st.markdown("Links to affiliate networks, banner/solo ad platforms, and free classified sites (low/no special approval).")

    st.markdown("### 💰 Affiliate Networks")
    affiliate_networks = [
        {"name":"ClickBank","url":"https://accounts.clickbank.com/signup/","note":"Huge digital marketplace."},
        {"name":"JVZoo","url":"https://www.jvzoo.com/register","note":"Digital products, IM, software."},
        {"name":"WarriorPlus","url":"https://warriorplus.com/user/new","note":"IM and biz-op offers."},
        {"name":"Digistore24","url":"https://www.digistore24.com/signup","note":"Global marketplace."},
        {"name":"MaxBounty","url":"https://affiliates.maxbounty.com/register","note":"Top CPA network (application required)."},
        {"name":"CJ","url":"https://signup.cj.com/member/signup/publisher/","note":"Big brand offers."},
        {"name":"Impact","url":"https://impact.com/partners/affiliate-partners/","note":"Large platform with many brands."},
        {"name":"PartnerStack","url":"https://dash.partnerstack.com/","note":"SaaS and software programs."},
    ]
    for n in affiliate_networks:
        st.markdown(f"- [{n['name']}]({n['url']}) – {n['note']}")

    st.markdown("---")
    st.markdown("### 📊 Banner & Solo Ad / Traffic Platforms")
    traffic_platforms = [
        {"name":"Udimi (Solo Ads)","url":"https://udimi.com/signup","note":"Buy solo ads from list owners."},
        {"name":"TrafficForMe","url":"https://www.trafficforme.net/","note":"Managed email traffic."},
        {"name":"PropellerAds","url":"https://partners.propellerads.com/#/auth/signUp","note":"Push, pop, display formats."},
        {"name":"Adsterra","url":"https://adsterra.com/","note":"Global ad network."},
        {"name":"RichAds","url":"https://my.richads.com/signup","note":"Push, pops, direct clicks."},
        {"name":"HilltopAds","url":"https://hilltopads.com/signup","note":"Display formats network."},
        {"name":"7Search PPC","url":"https://www.7searchppc.com/","note":"Self-service PPC network."},
        {"name":"20DollarBanners","url":"https://www.20dollarbanners.com/","note":"Affordable custom banner design."},
    ]
    for p in traffic_platforms:
        st.markdown(f"- [{p['name']}]({p['url']}) – {p['note']}")

    st.markdown("---")
    st.markdown("### 📦 Lead Magnet Hosting")
    st.markdown(
        "- **MediaFire** – free file hosting for your PDFs: "
        "[Create free account](https://www.mediafire.com/upgrade/registration.php?pid=free)"
    )


def page_classified_sites():
    """
    New tab: full high-traffic classified sites list, grouped like your document.
    """
    render_header()
    st.subheader("📣 High-Traffic Classified Ad Sites")

    st.markdown(
        "This tab maps out your **100+ free / high-traffic classified sites**, plus automation tools "
        "and posting best practices, organized by section so you can build your **Medicinal Garden Kit** "
        "and other offers into a serious distribution machine."
    )

    # Top 20 Global
    with st.expander("📊 Top 20 Global High-Traffic Sites", expanded=True):
        st.markdown(
            """
1. ⭐ **Craigslist** – GENERAL, HEALTH, LOCAL – ~157M visits  
   👉 <https://www.craigslist.org>  

2. ⭐ **Facebook Marketplace** – GENERAL, HEALTH, LOCAL – ~1.2B users  
   👉 <https://www.facebook.com/marketplace>  

3. **eBay Classifieds** – GENERAL – 50M+ visits  
   👉 <https://www.ebay.com/classifieds>  

4. ⭐ **Oodle** – GENERAL, HEALTH – 15M+ visits  
   👉 <https://www.oodle.com>  

5. **Gumtree (UK/AU)** – GENERAL – 30M+ visits  
   👉 <https://www.gumtree.com>  

6. **Locanto** – GENERAL – 8M+ visits  
   👉 <https://www.locanto.com>  

7. **Geebo** – GENERAL – 2M+ visits  
   👉 <https://www.geebo.com>  

8. **ClassifiedAds** – GENERAL – 5M+ visits  
   👉 <https://www.classifiedads.com>  

9. **Hoobly** – GENERAL – 3M+ visits  
   👉 <https://www.hoobly.com>  

10. **PennySaverUSA** – GENERAL – 4M+ visits  
    👉 <https://www.pennysaverusa.com>  

11. **Advertise Era** – GENERAL – 1M+ visits  
    👉 <https://www.advertiseera.com>  

12. **WallClassifieds** – GENERAL – 800K+ visits  
    👉 <https://www.wallclassifieds.com>  

13. **AdPost** – GENERAL – 2M+ visits  
    👉 <https://www.adpost.com>  

14. **DomesticSale** – GENERAL – 1.5M+ visits  
    👉 <https://www.domesticsale.com>  

15. **Recycler** – GENERAL – 3M+ visits  
    👉 <https://www.recycler.com>  

16. **Bedpage** – GENERAL – 10M+ visits  
    👉 <https://www.bedpage.com>  

17. **ClassifiedsFactor** – GENERAL – 500K+ visits  
    👉 <https://www.classifiedsfactor.com>  

18. **USNetAds** – GENERAL – 1M+ visits  
    👉 <https://www.usnetads.com>  

19. **Yakaz** – GENERAL – 2M+ visits  
    👉 <https://www.yakaz.com>  

20. **eBizMBA** – SERVICES – 500K+ visits  
    👉 <https://www.ebizmba.com>  
            """
        )

    # USA-focused
    with st.expander("🇺🇸 USA-Focused Classified Sites (21–40)"):
        st.markdown(
            """
21. ⭐ **OfferUp** – GENERAL, HEALTH, LOCAL – 20M+ visits  
    👉 <https://offerup.com>  

22. **5Miles** – GENERAL, LOCAL – 5M+ visits  
    👉 <https://www.5miles.com>  

23. ⭐ **VarageSale** – GENERAL, HEALTH, LOCAL – 3M+ visits  
    👉 <https://www.varagesale.com>  

24. **Trovit** – GENERAL – 15M+ visits  
    👉 <https://www.trovit.com>  

25. **Vast** – GENERAL – 2M+ visits  
    👉 <https://www.vast.com>  

26. **AdLandPro** – SERVICES – 800K+ visits  
    👉 <https://www.adlandpro.com>  

27. **USFreeAds** – GENERAL – 1.5M+ visits  
    👉 <https://www.usfreeads.com>  

28. **AmericanListed** – GENERAL – 2M+ visits  
    👉 <https://www.americanlisted.com>  

29. **FreeAdsTime** – GENERAL – 600K+ visits  
    👉 <https://www.freeadstime.org>  

30. **Classi4U** – GENERAL – 400K+ visits  
    👉 <https://www.classi4u.com>  

31. **Adoos** – GENERAL – 1M+ visits  
    👉 <https://www.adoos.com>  

32. **Click.in** – GENERAL – 5M+ visits  
    👉 <https://www.click.in>  

33. **BuySellCommunity** – GENERAL – 300K+ visits  
    👉 <https://www.buysellcommunity.com>  

34. **iNetGiant** – GENERAL – 800K+ visits  
    👉 <https://www.inetgiant.com>  

35. **SaleSpider** – SERVICES – 500K+ visits  
    👉 <https://www.salespider.com>  

36. **Kugli** – GENERAL – 600K+ visits  
    👉 <https://www.kugli.com>  

37. **BackPageAd** – GENERAL – 2M+ visits  
    👉 <https://www.backpagead.com>  

38. **ClassifiedSubmissions** – GENERAL – 400K+ visits  
    👉 <https://www.classifiedsubmissions.com>  

39. **AdsGlobe** – GENERAL – 500K+ visits  
    👉 <https://www.adsglobe.com>  

40. **FreeClassifiedsSite** – GENERAL – 300K+ visits  
    👉 <https://www.freeclassifiedssite.com>  
            """
        )

    # International
    with st.expander("🌍 International Classified Sites (41–55)"):
        st.markdown(
            """
41. **OLX (Global)** – GENERAL – 300M+ visits  
    👉 <https://www.olx.com>  

42. **Quikr (India)** – GENERAL – 30M+ visits  
    👉 <https://www.quikr.com>  

43. **Vivastreet** – GENERAL – 25M+ visits  
    👉 <https://www.vivastreet.com>  

44. **Expatriates** – GENERAL – 2M+ visits  
    👉 <https://www.expatriates.com>  

45. **AddonFace** – GENERAL – 500K+ visits  
    👉 <https://www.addonface.com>  

46. **Cifiyah** – GENERAL – 400K+ visits  
    👉 <https://www.cifiyah.com>  

47. **Kijiji (Canada)** – GENERAL – 20M+ visits  
    👉 <https://www.kijiji.ca>  

48. **FreeAdsUK** – GENERAL – 1M+ visits  
    👉 <https://www.freeadsuk.co.uk>  

49. **Friday-Ad (UK)** – GENERAL – 2M+ visits  
    👉 <https://www.friday-ad.co.uk>  

50. **AdTrader (UK)** – GENERAL – 1.5M+ visits  
    👉 <https://www.adtrader.co.uk>  

51. **FreeAds (UK)** – GENERAL – 3M+ visits  
    👉 <https://www.freeads.co.uk>  

52. **PostAdverts (UK)** – GENERAL – 800K+ visits  
    👉 <https://www.postadverts.com>  

53. **Gumtree Australia** – GENERAL – 15M+ visits  
    👉 <https://www.gumtree.com.au>  

54. **TradeMe (New Zealand)** – GENERAL – 5M+ visits  
    👉 <https://www.trademe.co.nz>  

55. **DealMarkaz (Pakistan)** – GENERAL – 1M+ visits  
    👉 <https://www.dealmarkaz.pk>  
            """
        )

    # Business & Services
    with st.expander("💼 Business & Services Directories (56–70)"):
        st.markdown(
            """
56. **Sulekha** – SERVICES – 5M+ visits  
    👉 <https://www.sulekha.com>  

57. **Thumbtack** – SERVICES – 30M+ visits  
    👉 <https://www.thumbtack.com>  

58. **Angie's List** – SERVICES – 10M+ visits  
    👉 <https://www.angieslist.com>  

59. **Bark** – SERVICES – 8M+ visits  
    👉 <https://www.bark.com>  

60. **HomeAdvisor** – SERVICES – 25M+ visits  
    👉 <https://www.homeadvisor.com>  

61. **Porch** – SERVICES – 5M+ visits  
    👉 <https://www.porch.com>  

62. **Houzz** – SERVICES – 40M+ visits  
    👉 <https://www.houzz.com>  

63. **ServiceMagic** – SERVICES – 3M+ visits  
    👉 <https://www.servicemagic.com>  

64. **Guru** – SERVICES – 2M+ visits  
    👉 <https://www.guru.com>  

65. **Freelancer** – SERVICES – 50M+ visits  
    👉 <https://www.freelancer.com>  

66. **Upwork** – SERVICES – 70M+ visits  
    👉 <https://www.upwork.com>  

67. **Fiverr** – SERVICES – 80M+ visits  
    👉 <https://www.fiverr.com>  

68. **PeoplePerHour** – SERVICES – 3M+ visits  
    👉 <https://www.peopleperhour.com>  

69. **TaskRabbit** – SERVICES – 5M+ visits  
    👉 <https://www.taskrabbit.com>  

70. **Zaarly** – SERVICES – 500K+ visits  
    👉 <https://www.zaarly.com>  
            """
        )

    # Specialty / Niche
    with st.expander("🎯 Specialty / Niche & Local (71–80)"):
        st.markdown(
            """
71. ⭐ **Nextdoor** – LOCAL, HEALTH – 37M+ visits  
    👉 <https://www.nextdoor.com>  

72. **Bookoo** – LOCAL – 2M+ visits  
    👉 <https://www.bookoo.com>  

73. **GarageSaleHunter** – LOCAL – 500K+ visits  
    👉 <https://www.garagesalehunter.com>  

74. **YardSaleSearch** – LOCAL – 800K+ visits  
    👉 <https://www.yardsalesearch.com>  

75. **PetClassifieds** – GENERAL – 300K+ visits  
    👉 <https://www.petclassifieds.us>  

76. **PuppyFind** – GENERAL – 2M+ visits  
    👉 <https://www.puppyfind.com>  

77. **ApartmentGuide** – SERVICES – 10M+ visits  
    👉 <https://www.apartmentguide.com>  

78. **Zillow** – SERVICES – 200M+ visits  
    👉 <https://www.zillow.com>  

79. **Trulia** – SERVICES – 30M+ visits  
    👉 <https://www.trulia.com>  

80. **Realtor.com** – SERVICES – 100M+ visits  
    👉 <https://www.realtor.com>  
            """
        )

    # Additional High-DA
    with st.expander("➕ Additional High-DA Sites (81–100)"):
        st.markdown(
            """
81. **ClickIndia** – GENERAL – 5M+ visits  
    👉 <https://www.clickindia.com>  

82. **IndiaList** – GENERAL – 2M+ visits  
    👉 <https://www.indialist.com>  

83. **Khojle** – GENERAL – 1M+ visits  
    👉 <https://www.khojle.in>  

84. **PostJobFree** – SERVICES – 1.5M+ visits  
    👉 <https://www.postjobfree.com>  

85. **H1Ad** – GENERAL – 300K+ visits  
    👉 <https://www.h1ad.com>  

86. **GiganticList** – GENERAL – 600K+ visits  
    👉 <https://www.giganticlist.com>  

87. **Claz.org** – GENERAL – 400K+ visits  
    👉 <https://www.claz.org>  

88. **SaudiAds** – GENERAL – 800K+ visits  
    👉 <https://www.saudiads.com>  

89. **TuffClassified** – GENERAL – 500K+ visits  
    👉 <https://www.tuffclassified.com>  

90. **Classifieds24x7** – GENERAL – 300K+ visits  
    👉 <https://www.classifieds24x7.com>  

91. **MyFavoriteClassifieds** – GENERAL – 200K+ visits  
    👉 <https://www.myfavoriteclassifieds.com>  

92. **MaxBizPages** – SERVICES – 400K+ visits  
    👉 <https://www.maxbizpages.com>  

93. **AskAds** – GENERAL – 300K+ visits  
    👉 <https://www.askads.com>  

94. **WebClassifieds** – GENERAL – 250K+ visits  
    👉 <https://www.webclassifieds.us>  

95. **FreeAdsList** – GENERAL – 350K+ visits  
    👉 <https://www.freeadslist.com>  

96. **AdSitePro** – GENERAL – 200K+ visits  
    👉 <https://www.adsitepro.com>  

97. **ClickBazaar** – GENERAL – 500K+ visits  
    👉 <https://www.clickbazaar.com>  

98. **GlobalFreeClassifiedAds** – GENERAL – 300K+ visits  
    👉 <https://www.globalfreeclassifiedads.com>  

99. **TopClassifieds** – GENERAL – 250K+ visits  
    👉 <https://www.topclassifieds.com>  

100. **ClassifiedAdsUSA** – GENERAL – 400K+ visits  
     👉 <https://www.classifiedadsusa.com>  
            """
        )

    # Automation tools
    with st.expander("🤖 Automated Posting Tools & Software"):
        st.markdown(
            """
- **ClassifiedSubmissions.com** – Web-based posting to 100+ sites, scheduling  
  👉 <https://www.classifiedsubmissions.com>  

- **PostLister** – Desktop software, bulk posting, templates  

- **Claz Automated Poster** – Free basic posting, paid bulk options  
  👉 <https://www.claz.org>  

- **Classified Ad Posting Software (various)** – Multi-site posting, image mgmt  

- **Craigslist Auto Poster** – Use carefully (Craigslist is strict)  

- **IFTTT** – Automation platform, can connect social to some sites  
  👉 <https://ifttt.com>  

- **Zapier** – Automation platform for workflows  
  👉 <https://zapier.com>  

- **Buffer** – Schedules social posts; useful for Marketplace-style traffic  
  👉 <https://buffer.com>  

- **Hootsuite** – Multi-platform scheduling  
  👉 <https://hootsuite.com>  
            """
        )

    # Posting tips
    with st.expander("✅ Posting Tips for Best Results"):
        st.markdown(
            """
1. **Post Consistently** – New ads every 2–3 days, renew expired ads.  
2. **Use Multiple Sites** – Don’t rely on one; start with ⭐ sites first.  
3. **Include Quality Images** – Clear, well-lit, relevant to your Medicinal Garden Kit offer.  
4. **Write Compelling Titles** – Use benefit + keywords:  
   - *“Medicinal Garden Kit – Grow Your Own Natural Remedies At Home”*  
5. **Add Your Website URL** – Always include your landing page or funnel, ideally with UTM tracking.  
6. **Track Performance** – UTM tags + your Analytics tab to see what sites actually bring leads/sales.  
7. **Follow Site Rules** – Avoid bans; read guidelines.  
8. **Optimize for Local** – Use city/region + “natural health”, “herbal remedies”, etc.  
9. **Test Ad Copy** – Use your Classified Ad Writer + A/B Split Tester to find winners.  
10. **Respond Quickly** – Same day replies build trust and conversions.  
            """
        )

    with st.expander("🎯 Top 10 Priority Sites for Medicinal Herbal Garden Kit", expanded=False):
        st.markdown(
            """
Start with these 10 platforms before you expand to all 100+:

1. **Craigslist** – Local & health-conscious shoppers.  
2. **Facebook Marketplace** – Massive reach, easy discovery.  
3. **OfferUp** – App-driven local buyers.  
4. **Nextdoor** – Community trust + neighborhood context.  
5. **Oodle** – General + health categories.  
6. **VarageSale** – Community-based group selling.  
7. **Gumtree** – UK/AU, perfect for international testing.  
8. **OLX** – Huge global audience for scale.  
9. **Locanto** – Easy posting, worldwide.  
10. **ClassifiedAds.com** – Simple interface, solid traffic.  
            """
        )


def page_ab_split_tester():
    render_header()
    st.subheader("🧪 A/B Split Tester")
    st.markdown("Compare two variants with CTR, CVR, EPC, and ROI.")

    test_type = st.selectbox("Test Type", ["Headline","Sales Page / VSL","Email Subject","Display Ad / Banner","Classified Ad","Other"], index=0)

    with st.form("ab_test_form"):
        st.markdown("### Variant Details")
        col_a, col_b = st.columns(2)
        with col_a:
            name_a = st.text_input("Name A", f"{test_type} A")
            copy_a = st.text_area("Copy / Notes A", "", key="copy_a")
            imp_a = st.number_input("Impressions A", min_value=0, step=1, value=0)
            clicks_a = st.number_input("Clicks A", min_value=0, step=1, value=0)
            conv_a = st.number_input("Conversions A", min_value=0, step=1, value=0)
            rev_a = st.number_input("Revenue A (optional)", min_value=0.0, step=1.0, value=0.0)
        with col_b:
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

    def calc(imp, clk, conv, rev):
        ctr = (clk/imp*100) if imp>0 else 0.0
        cvr = (conv/clk*100) if clk>0 else 0.0
        cr  = (conv/imp*100) if imp>0 else 0.0
        epc = (rev/clk) if clk>0 else 0.0
        roi = ((rev-imp)/imp*100) if imp>0 and rev>0 else 0.0
        return ctr, cvr, cr, epc, roi

    ctr_a, cvr_a, cr_a, epc_a, roi_a = calc(imp_a, clicks_a, conv_a, rev_a)
    ctr_b, cvr_b, cr_b, epc_b, roi_b = calc(imp_b, clicks_b, conv_b, rev_b)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {name_a}")
        st.write(f"CTR: {ctr_a:.2f}% | Click→Conv: {cvr_a:.2f}% | Imp→Conv: {cr_a:.2f}% | EPC: ${epc_a:.2f} | ROI: {roi_a:.2f}%")
    with col2:
        st.markdown(f"#### {name_b}")
        st.write(f"CTR: {ctr_b:.2f}% | Click→Conv: {cvr_b:.2f}% | Imp→Conv: {cr_b:.2f}% | EPC: ${epc_b:.2f} | ROI: {roi_b:.2f}%")


def page_analytics():
    render_header()
    st.subheader("📈 Analytics & Campaign Tracker")
    st.markdown("Track CPC, CPL, CPS, EPC, and ROI. Data is session-only.")

    if "analytics_history" not in st.session_state:
        st.session_state["analytics_history"] = []

    with st.form("analytics_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            campaign_name = st.text_input("Campaign Name", "Default Campaign")
            channel = st.selectbox("Channel", ["Affiliate","Solo Ads","Banner / Display","Classifieds","Email","Other"], index=0)
        with col2:
            spend = st.number_input("Ad Spend / Cost ($)", min_value=0.0, step=1.0, value=0.0)
            clicks = st.number_input("Clicks", min_value=0, step=1, value=0)
        with col3:
            leads = st.number_input("Leads / Opt-ins", min_value=0, step=1, value=0)
            sales = st.number_input("Sales / Actions", min_value=0, step=1, value=0)
        revenue = st.number_input("Revenue / Payout ($)", min_value=0.0, step=1.0, value=0.0)
        submitted = st.form_submit_button("➕ Add / Update Campaign Snapshot")

    if submitted:
        cpc = (spend/clicks) if clicks>0 else 0.0
        cpl = (spend/leads) if leads>0 else 0.0
        cps = (spend/sales) if sales>0 else 0.0
        epc = (revenue/clicks) if clicks>0 else 0.0
        roi = ((revenue-spend)/spend*100) if spend>0 else 0.0
        snap = {
            "Campaign":campaign_name,"Channel":channel,"Spend":spend,"Clicks":clicks,"Leads":leads,"Sales":sales,
            "Revenue":revenue,"CPC":round(cpc,4),"CPL":round(cpl,4),"CPS":round(cps,4),"EPC":round(epc,4),"ROI%":round(roi,2)
        }
        st.session_state["analytics_history"].append(snap)
        st.success("Snapshot added.")

    if st.session_state["analytics_history"]:
        st.markdown("### 📊 Campaign History (This Session)")
        st.dataframe(st.session_state["analytics_history"])
    else:
        st.info("No campaign snapshots yet.")


def page_system_checklist():
    render_header()
    st.subheader("✅ System Checklist")
    st.markdown("Use this quick checklist before buying traffic.")

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Landing / Sales Page copy done")
        st.checkbox("Email sequence loaded into ESP")
        st.checkbox("Lead magnet created & hosted")
    with col2:
        st.checkbox("Tracking links (affiliate IDs, UTMs)")
        st.checkbox("Retargeting pixels / tags installed")
        st.checkbox("Compliance checked")

    col3, col4 = st.columns(2)
    with col3:
        st.checkbox("Core offer(s) selected")
        st.checkbox("2–3 hooks ready for testing")
    with col4:
        st.checkbox("Classified ads ready")
        st.checkbox("Solo ad swipe ready")


def page_copy_analyzer():
    render_header()
    st.subheader("🧮 Copy Analyzer & Variant Comparer")

    mode = st.radio("Mode", ["Single Copy Score", "Compare Two Variants (A/B)"], index=0)
    if mode == "Single Copy Score":
        text = st.text_area("Paste your copy here", "", height=260)
        if st.button("🔍 Analyze Copy"):
            if not text.strip():
                st.error("Please paste some copy first.")
                return
            analysis = analyze_copy_score(text)
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
    else:
        col1, col2 = st.columns(2)
        with col1:
            text_a = st.text_area("Variant A", "", height=240)
        with col2:
            text_b = st.text_area("Variant B", "", height=240)
        if st.button("⚔️ Compare A vs B (Heuristic)"):
            if not text_a.strip() or not text_b.strip():
                st.error("Please paste copy for both variants.")
                return
            a = analyze_copy_score(text_a)
            b = analyze_copy_score(text_b)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Variant A")
                st.metric("Overall", f"{a['total_score']} / 100")
                st.write(f"Len: {a['length_score']:.1f} | Emo: {a['emotion_score']:.1f} | Struct: {a['structure_score']:.1f} | CTA: {a['cta_score']:.1f} | Spec: {a['specificity_score']:.1f}")
            with col_b:
                st.markdown("#### Variant B")
                st.metric("Overall", f"{b['total_score']} / 100")
                st.write(f"Len: {b['length_score']:.1f} | Emo: {b['emotion_score']:.1f} | Struct: {b['structure_score']:.1f} | CTA: {b['cta_score']:.1f} | Spec: {b['specificity_score']:.1f}")


def page_settings_integrations():
    render_header()
    st.subheader("⚙️ Settings & Integrations")
    st.markdown("This build supports rule-based generation plus optional AI enhancements via **OpenAI**, **Claude**, **Groq (Llama)**, and **Cohere**.")
    st.markdown("Add API keys in Streamlit secrets to enable each provider.")

    st.markdown("### 🤖 API Keys (add in Settings → Secrets)")
    st.code(
        'ADMIN_USERNAME = "DeAndre Jefferson"\n'
        'ADMIN_PASSWORD = "your-strong-password"\n'
        'OPENAI_API_KEY = "sk-..."\n'
        'ANTHROPIC_API_KEY = "sk-ant-..."\n'
        'GROQ_API_KEY = "gsk_..."\n'
        'COHERE_API_KEY = "..."',
        language="ini",
    )

    st.markdown("### 🔗 Zapier Webhooks")
    zap_url = st.text_input("Zapier Catch Hook URL", st.session_state.get("zapier_url",""))
    st.session_state["zapier_url"] = zap_url
    test_payload = {"event":"test_ping","source":"Illuminati AI Copy Master"}
    if st.button("🚀 Send Test Webhook"):
        ok, msg = send_zapier_webhook(zap_url, test_payload)
        st.success(msg) if ok else st.error(msg)


# =========================
# Main (auth-gated)
# =========================

def main():
    if not is_authenticated():
        # Login-only view; sidebar: logo + mindset video
        with st.sidebar:
            st.markdown('<div class="sidebar-logo">🔺 Illuminati AI</div>', unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("##### 🎧 Mindset Fuel")
            # Reliable video playback: st.video with YouTube URL.
            # If you get a Wistia share URL later, you can just replace this string.
            st.video("https://www.youtube.com/watch?v=IN2H8U9Zr3k")
            st.caption("🎧 Earl Nightingale – \"The Strangest Secret\"")
        login_page()
        return

    # Authenticated UI with full nav
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🔺 Illuminati AI</div>', unsafe_allow_html=True)
        page = st.radio(
            "Navigate",
            [
                "Dashboard",
                "Generate Copy",
                "Email Sequences",
                "VSL & Webinar Scripts",
                "Classified Ad Writer",
                "Manual & Lead Magnet",
                "Traffic & Networks",
                "Classified Sites",
                "A/B Split Tester",
                "Analytics",
                "System Checklist",
                "Copy Analyzer",
                "Settings & Integrations",
            ],
        )
        st.markdown("---")
        st.markdown("##### 🎧 Mindset Fuel")
        st.video("https://youtu.be/l1gXZu1i8TM?si=2D_D5KvB6t8fxxUj")
        st.caption("🎧 Earl Nightingale – \"The Strangest Secret\"")
        if st.button("🚪 Logout"):
            st.session_state["auth_ok"] = False
            st.success("Logged out.")
            st.rerun()

    if page == "Dashboard":
        page_dashboard()
    elif page == "Generate Copy":
        page_generate_copy()
    elif page == "Email Sequences":
        page_email_sequences()
    elif page == "VSL & Webinar Scripts":
        page_vsl_webinar()
    elif page == "Classified Ad Writer":
        page_classified_writer()
    elif page == "Manual & Lead Magnet":
        page_manual_assets()
    elif page == "Traffic & Networks":
        page_traffic_networks()
    elif page == "Classified Sites":
        page_classified_sites()
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

    st.markdown(
        """
        <div class="illuminati-footer">
            © 2025 <strong>DeAndre Jefferson</strong><br/>
            Strategic Copy, AI, and Influence Engineering.<br/>
            Built with Python + Streamlit + OpenAI + Gemini + Claude (Anthropic).
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
